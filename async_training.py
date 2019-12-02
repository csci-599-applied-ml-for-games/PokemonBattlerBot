'''
Usage:
	asyn_training.py [--start_epsilon=<start_epsilon>] [--load_model=<load_model>]

Options:
	--start_epsilon A tool for continuing after a crash. Sets the starting epsilon for the first epoch
	--load_model 	A tool for continuing after a crash. Sets the starting model for the first epoch
'''

import os
from datetime import datetime
import time
from multiprocessing import Process
from collections import deque
import re

from docopt import docopt 
import keras
from keras.models import load_model

from dqn import DQNAgent, REPLAY_MEMORY_SIZE, create_model
from gamestate import GameState
from bot import RandomAgent, BotClient, RunType, REPLAY_MEMORY_DIR

DEBUG = True

ASYNC_TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

INPUT_SHAPE = (GameState.vector_dimension(),)

def debug_log(*args):
	if DEBUG:
		now = datetime.now()
		l = [str(arg) for arg in args]
		string = ' '.join(l)
		with open(os.path.join(LOGS_DIR, 'async_train.txt'), 'a') as fd:
			fd.write(f'[{datetime.now()}] {string}\n')

class GameInfo():
	def __init__(self):
		self.start_time = 0.0
		self.processes = []

def make_bot(un, pw, expected_opponent, team, challenge, trainer, epsilon=None, 
	model_path=None, target_model_path=None
):
	
	if trainer:
		if model_path:
			agent = DQNAgent(INPUT_SHAPE, training=False)
		else:
			agent = RandomAgent()
	else:
		agent = DQNAgent(
			INPUT_SHAPE, epsilon=epsilon, random_moves=True, training=False, 
			copy_target_model=False
		)
		agent.load_model(model_path)
		if target_model_path != None:
			agent.target_model = load_model(target_model_path)
		else:
			agent.target_model.set_weights(agent.model.get_weights())

	bot = BotClient(
		name=un, password=pw, expected_opponent=expected_opponent, team=team, 
		challenge=challenge, runType=RunType.Iterations, runTypeData=1, 
		agent=agent, trainer=trainer, save_model=False, 
		should_write_replay=(not trainer)
	)
	bot.start()

if __name__ == '__main__':
	args = docopt(__doc__)

	if args.get('--start_epsilon'):
		start_epsilon = float(args['--start_epsilon'])
	else:
		start_epsilon = 1

	start_model = args.get('--load_model')

	timeout = 180
	epsilon_decay = 0.95
	min_epsilon = 0.01
	epochs = 2
	games_to_play = 5
	MINIBATCH_SIZE = 64
	MIN_REPLAY_MEMORY_SIZE = 1000 
	games_info = [GameInfo() for _ in range(games_to_play)]
	accounts = [
		('USCBot1', 'USCBot1'),
		('USCBot2', 'USCBot2'),
		('USCBot4', 'USCBot4'),
		('USCBot5', 'USCBot5'),
		('USCBot9', 'USCBot9'),
		('USCBot10', 'USCBot10'),
		('USCBot11', 'USCBot11'),
		('USCBot12', 'USCBot12'),
		('USCBot13', 'USCBot13'),
		('USCBot14', 'USCBot14')
	]

	with open(os.path.join(ASYNC_TRAIN_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()

	keep_model_list = [] 
	loss_history = []
	agent = None
	update_target_every = 2
	for epoch in range(epochs):
		replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
		if epoch == 0:
			epsilon = start_epsilon
		else:
			epsilon = 1
		iteration = 0

		if epoch == 0:
			trainer_model_path = None
		else:
			max_iteration = -1
			for content in os.listdir(LOGS_DIR):
				if (content.startswith(f'Epoch{epoch - 1}') and 
					content.endswith('.model')
				):
					result = re.search(r'Iteration(?P<iteration>[0-9]+)', 
						content
					)
					content_iteration = int(result.group('iteration'))
					if content_iteration > max_iteration:
						trainer_model_path = os.path.join(LOGS_DIR, content) 
						max_iteration = content_iteration
			keep_model_list.append(trainer_model_path)
			#NOTE: clean up logs and models from last epoch
			for content in os.listdir(LOGS_DIR):
				content_path = os.path.join(LOGS_DIR, content) 
				if (content_path not in keep_model_list and 
					(content.endswith('Iteration0.txt') or 
						content.endswith('.model')
					)
				):
					if not os.path.isdir(content_path):
						os.remove(content_path)

		#NOTE: model is reused from previous AN iteration if possible
		if epoch == 0:
			if start_model == None:
				model = create_model(INPUT_SHAPE)
			else:
				debug_log(f'Loading model at {start_model}')
				model = load_model(start_model)
		else:
			model = agent.model
		original_model_path = os.path.join(LOGS_DIR, 
			f'Epoch{epoch}_Iteration{iteration}.model'
		)
		model.save(original_model_path)
		model_path = original_model_path
		target_model_path = model_path

		target_update_counter = 0
		loss_history.append([])
		debug_log(f'Starting adversarial network iteration {epoch}')
		debug_log(f'trainer_model_path {trainer_model_path}')
		while True:
			debug_log(f'Starting iteration {iteration}')
			debug_log(f'model_path {model_path}')
			debug_log(f'target_model_path {target_model_path}')

			#NOTE: start two processes for each game 
			for game_index in range(games_to_play): 
				#NOTE: get the account information
				account1 = accounts[2 * game_index]
				account2 = accounts[2 * game_index + 1]
				un1, pw1 = account1
				un2, pw2 = account2
				
				games_info[game_index].processes = []

				bot1_process = Process(target=make_bot, 
					args=(un1, pw1, un2, team, False,  False), 
					kwargs={
						'model_path': model_path, 
						'target_model_path': target_model_path,
						'epsilon': epsilon
					}, 
					daemon=True)
				bot1_process.start()

				time.sleep(30) #NOTE: the challenger needs to come a little after the other bot is set up
				#NOTE: 30 seconds because model can be slow to load at times

				bot2_process = Process(target=make_bot, 
					args=(un2, pw2, un1, team, True, True),
					kwargs={'model_path': trainer_model_path}, 
					daemon=True) #TODO: add the model_path
				bot2_process.start()

				games_info[game_index].start_time = time.time()
				games_info[game_index].processes.append(bot1_process)
				games_info[game_index].processes.append(bot2_process)

				time.sleep(1)

			time.sleep(5)
			
			start = time.time()
			while True:
				time.sleep(1)
				all_dead = True

				for game_info in games_info:
					any_dead = False
					for process in game_info.processes:
						if not process.is_alive():
							any_dead = True

					if any_dead:
						for process in game_info.processes:
							if process.is_alive():
								process.join(10)
								process.terminate()
					else:
						all_dead = False

				if len(os.listdir(REPLAY_MEMORY_DIR)) >= games_to_play:
					debug_log('Found all replays. Exiting')
					break
				elif (time.time() - start) >= timeout:
					debug_log('Timing out. Exiting.')
					break
				elif all_dead:
					debug_log('All processes are dead. Exiting.')
					break
			
			#NOTE: kill any lingering processes
			for game_info in games_info:
				for process in game_info.processes:
					join_timeout = timeout - (time.time() - start) 
					if join_timeout > 0:
						process.join(join_timeout)
					if process.is_alive():
						process.terminate()

			#NOTE: clear out the replay memory directory
			minibatch = deque()
			for content in os.listdir(REPLAY_MEMORY_DIR):
				file_path = os.path.join(REPLAY_MEMORY_DIR, content)
				debug_log('Extending with file {}'.format(file_path))
				with open(file_path, 'r') as fd:
					s = fd.read()
				try:
					data = eval(s)
					minibatch.extend(data)
				except SyntaxError:
					debug_log('hit syntax error')
					debug_log(f'file content with syntax error\n{s}')
					debug_log('')

				for i in range(5):
					try:
						os.remove(file_path)
						break
					except PermissionError:
						debug_log('Permission error when removing the file')
						time.sleep(1)

			#NOTE: train
			#NOTE: create/load DQN and target DQN in main thread
			keras.backend.clear_session()
			agent = DQNAgent(INPUT_SHAPE, training=True, 
				replay_memory=minibatch, copy_target_model=False
			)
			agent.target_model = load_model(target_model_path)
			#NOTE: train newly loaded model on new data
			if len(minibatch) > 0:
				minibatch_history = agent.train_only(len(minibatch), len(minibatch))
				if minibatch_history == None:
					debug_log('ERROR: Unable to train on iteration\'s data')
				replay_memory.extend(minibatch)
			else:
				debug_log('WARNING: Skipping minibatch training since no new data was found')

			#NOTE: train newly loaded model on random selection of old data
			agent.replay_memory = replay_memory
			sum_loss = 0
			if len(replay_memory) > MIN_REPLAY_MEMORY_SIZE: 
				train_loops = 50
				for train_iteration in range(train_loops):
					history = agent.train_only(MINIBATCH_SIZE, 
						MIN_REPLAY_MEMORY_SIZE
					)
					sum_loss += history.history.get('loss', [0])[0]
				average_loss = sum_loss / float(train_loops)
			else:
				history = None

			debug_log(f'on iteration {iteration}, replay_memory has size {len(replay_memory)}')

			#NOTE: decay epsilon
			if epsilon > min_epsilon:
				if len(replay_memory) > MIN_REPLAY_MEMORY_SIZE:
					epsilon *= epsilon_decay
					if epsilon < min_epsilon:
						epsilon = min_epsilon
				else:
					min_epsilon_iterations = 0
			elif epsilon <= min_epsilon:
				min_epsilon_iterations += 1

			debug_log(f'epsilon is now {epsilon}')

			#NOTE: check if we should update target models
			target_update_counter += 1
			if target_update_counter >= update_target_every:
				target_update_counter = 0
				target_model_path = model_path				

			#NOTE: update model_path
			model_path = os.path.join(
				LOGS_DIR, 
				f'Epoch{epoch}_Iteration{iteration}.model'
			)
			agent.save_model(model_path)
			iteration += 1

			if history != None:
				loss = average_loss
				debug_log(f'Average Loss over 50 trainings: {loss}')
				if loss != None:
					loss_history[epoch].append(loss)

				rolling_average_window = 20
				if len(loss_history[epoch]) > rolling_average_window:
					rolling_window_average_loss = (
						sum(loss_history[epoch][-1 * rolling_average_window:]) / 
						float(rolling_average_window)
					)
					debug_log(f'Rolling average (w={rolling_average_window}) loss: {rolling_window_average_loss}')
					if ((rolling_window_average_loss < 0.001) or 
						(min_epsilon_iterations >= 50)
					):
						debug_log('Moving on to next adversarial network iteration')
						break

			#NOTE: clean unused models 
			for content in os.listdir(LOGS_DIR):
				content_path = os.path.join(LOGS_DIR, content) 
				if (content_path not in keep_model_list and 
					content.endswith('.model') and 
					content_path != model_path and
					content_path != trainer_model_path and 
					content_path != target_model_path  
				):
					if not os.path.isdir(content_path):
						os.remove(content_path)

	with open(os.path.join(LOGS_DIR, 'loss_history.csv'), 'w') as fd:
		fd.write('Adversarial Network Iteration,Game Iteration,Loss\n')
		for epoch_index, epoch_history in enumerate(loss_history):
			for game_iteration, loss in enumerate(epoch_history):
				fd.write(f'{epoch_index},{game_iteration},{loss}\n')