import os
import time
from multiprocessing import Process
from collections import deque

from keras.models import load_model

from dqn import DQNAgent, REPLAY_MEMORY_SIZE, create_model
from gamestate import GameState
from bot import RandomAgent, BotClient, RunType

ASYNC_TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

INPUT_SHAPE = (GameState.vector_dimension(),)

MIN_REPLAY_MEMORY_SIZE = 3000

class GameInfo():
	def __init__(self):
		self.start_time = 0.0
		self.processes = []
		self.bots = []

def make_bot(un, pw, expected_opponent, team, challenge, 
	trainer, replay_memory, games_info, game_index, epsilon=None, 
	model_path=None, target_model_path=None):
	
	if trainer:
		if model_path:
			agent = DQNAgent(INPUT_SHAPE, training=False)
		else:
			agent = RandomAgent()
	else:
		agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, random_moves=True, 
			training=False, copy_target_model=False, 
			replay_memory=replay_memory)
		agent.load_model(model_path)
		if target_model_path != None:
			agent.target_model = load_model(target_model_path)
		else:
			agent.target_model.set_weights(agent.model.get_weights())

	bot = BotClient(name=un, password=pw, 
		expected_opponent=expected_opponent, team=team, 
		challenge=challenge, runType=RunType.Iterations, runTypeData=1, 
		agent=agent, trainer=trainer, save_model=False)
	games_info[game_index].bots.append(bot)
	bot.start()

if __name__ == '__main__':
	timeout = 1200
	epsilon = 1
	epsilon_decay = 0.99
	min_epsilon = 0.001
	epochs = 1
	games_to_play = 1
	games_info = [GameInfo() for _ in range(games_to_play)]
	accounts = [
		('USCBot9', 'USCBot9'),
		('USCBot10', 'USCBot10')
	]

	with open(os.path.join(ASYNC_TRAIN_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()

	
	agent = None
	update_target_every = 5
	for epoch in range(epochs):
		replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
		if epoch == 0:
			model = create_model(INPUT_SHAPE)
		else:
			model = agent.model

		iteration = 0
		original_model_path = os.path.join(LOGS_DIR, f'Epoch{epoch}_Iteration{iteration}.model')
		model.save(original_model_path)
		model_path = original_model_path
		target_model_path = model_path

		target_update_counter = 0

		while True:
			#NOTE: start two processes for each game 
			for game_index in range(games_to_play): 
				#NOTE: get the account information
				account1 = accounts[2 * game_index]
				account2 = accounts[2 * game_index + 1]
				un1, pw1 = account1
				un2, pw2 = account2
				
				games_info[game_index].bots = []
				games_info[game_index].processes = []

				bot1_process = Process(target=make_bot, 
					args=(
						un1, pw1, un2, team, False,  False, replay_memory, 
						games_info, game_index
					), 
					kwargs={
						'model_path': model_path, 
						'target_model_path': target_model_path,
						'epsilon': epsilon
					}, 
					daemon=True)
				bot1_process.start()

				time.sleep(5) #NOTE: the challenger needs to come a little after the other bot is set up

				if epoch == 0:
					trainer_model_path = None
				else:
					trainer_model_path = original_model_path
				bot2_process = Process(target=make_bot, 
					args=(
						un2, pw2, un1, team, False,  False, replay_memory, 
						games_info, game_index
					),
					kwargs={'model_path': model_path}, 
					daemon=True) #TODO: add the model_path
				bot2_process.start()

				games_info[game_index].start_time = time.time()
				games_info[game_index].processes.append(bot1_process)
				games_info[game_index].processes.append(bot2_process)

			#NOTE: wait until all games finish
			any_alive = True
			while any_alive:
				any_alive = False
				#NOTE: check if any bots have stalled for more than the timeout
				for game_info in games_info:
					if time.time() - game_info.start_time > timeout:
						for bot in game_info.bots:
							bot.kill() 
					else:
						for process in game_info.processes:
							if process.is_alive():
								any_alive = True

			#NOTE: train
			#NOTE: create/load DQN and target DQN in main thread
			agent = DQNAgent(
				INPUT_SHAPE, training=True, replay_memory=replay_memory, 
				copy_target_model=False
			)
			agent.target_model = load_model(target_model_path)
			#NOTE: train newly loaded model
			history = agent.train_only(MIN_REPLAY_MEMORY_SIZE, MIN_REPLAY_MEMORY_SIZE)

			#NOTE: decay epsilon
			if epsilon > min_epsilon and len(replay_memory) > MIN_REPLAY_MEMORY_SIZE:
				epsilon *= epsilon_decay
				if epsilon < min_epsilon:
					epsilon = min_epsilon
					min_epsilon_iterations = 0
			elif epsilon <= min_epsilon:
				min_epsilon_iterations += 1


			#NOTE: check if we should update target models
			if target_update_counter > update_target_every:
				target_update_counter = 0
				target_model_path = model_path
			elif len(replay_memory) > MIN_REPLAY_MEMORY_SIZE:
				target_update_counter += 1

			#NOTE: update model_path
			iteration += 1
			model_path = os.path.join(LOGS_DIR, f'Epoch{epoch}_Iteration{iteration}.model')
			agent.save_model(model_path)

			#NOTE: check if we should move to the next epoch
			#TODO: implement checking for next epoch
			# print(history.history.keys())
			break