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

GAME_INFO = []
class GameInfo():
	start_time = 0.0
	threads = []
	bots = []

def make_bot(un, pw, expected_opponent, team, challenge, 
	trainer, replay_memory, game_index, model_path=None, target_model_path=None):
	
	if trainer:
		if model_path:
			agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, random_moves=True, 
				training=False)
		else:
			agent = RandomAgent()
	else:
		agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, random_moves=True, 
			training=False, copy_target_model=False, 
			replay_memory=replay_memory)
		agent.load_model(model_path)
		if target_model_path == None:
			agent.target_model = load_model(target_model_path)
		else:
			agent.target_model.set_weights(agent.model.get_weights())

	bot = BotClient(name=un, password=pw, 
		expected_opponent=expected_opponent, team=team, 
		challenge=challenge, runType=RunType.Iterations, runTypeData=1, 
		agent=agent, trainer=trainer, save_model=False)
	GAME_INFO[game_index].bots.append(bot)
	bot.start()

if __name__ == '__main__':
	timeout = 1200
	epsilon = 1
	epsilon_decay = 0.99
	min_epsilon = 0.001
	epochs = 1

	with open(os.path.join(ASYNC_TRAIN_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()

	#NOTE: get the account information
	un1, pw1 = ('USCBot9', 'USCBot9')
	un2, pw2 = ('USCBot10', 'USCBot10')
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
			#TODO: define model_path
			#NOTE: start two threads for each game 
			game_index = 0
			GAME_INFO[game_index].start_time = time.time()
			GAME_INFO[game_index].bots = []

			bot1_thread = Process(target=make_bot, 
				args=(un1, pw1, un2, team, False,  False, replay_memory, game_index), 
				kwargs={'model_path': model_path, 'target_model_path': target_model_path}, 
				daemon=True)
			bot1_thread.start()

			time.sleep(5) #NOTE: the challenger needs to come a little after the other bot is set up

			if epoch == 0:
				trainer_model_path = None
			else:
				trainer_model_path = original_model_path
			bot2_thread = Process(target=make_bot, 
				args=(un2, pw2, un1, team, False,  False, replay_memory, game_index),
				kwargs={'model_path': model_path}, 
				daemon=True) #TODO: add the model_path
			bot2_thread.start()
			
			#NOTE: wait until all games finish
			any_alive = True
			while any_alive:
				any_alive = False
				#NOTE: check if any bots have stalled for more than 20 minutes
				for game_info in GAME_INFO:
					if time.time() - game_info.start_time > timeout:
						for bot in game_info.bots:
							bot.kill() #TODO: define kill in bot.py
					else:
						for thread in game_info.threads:
							if thread.is_alive():
								any_alive = True

			#NOTE: train
			#NOTE: create/load DQN and target DQN in main thread
			agent = DQNAgent(INPUT_SHAPE, training=True, replay_memory=replay_memory)
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
			print(history.history.keys())
			break