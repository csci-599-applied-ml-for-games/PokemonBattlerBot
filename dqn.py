'''
As of Oct. 8, 2019, Code is based on 
https://pythonprogramming.net/deep-q-learning-dqn-reinforcement-learning-python-tutorial/
and 
https://pythonprogramming.net/training-deep-q-learning-dqn-reinforcement-learning-python-tutorial/?completed=/deep-q-learning-dqn-reinforcement-learning-python-tutorial/
'''
import random
random.seed()
import os
from collections import deque
from enum import Enum, auto

from gamestate import POKEMON_NAME_TO_INDEX, MOVE_NAME_TO_INDEX

import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

DISCOUNT = 0.85
REPLAY_MEMORY_SIZE = 15_000 #TODO: this should probably not be global
MIN_REPLAY_MEMORY_SIZE = 1000
MINIBATCH_SIZE = 64

class ActionType(Enum):
	Move = auto()
	Switch = auto()

#TODO: handle mega
MAX_ACTION_SPACE_SIZE = (MOVE_NAME_TO_INDEX['Count'] + 
	POKEMON_NAME_TO_INDEX['Count'])

def create_model(input_shape):
	model = Sequential()

	model.add(Dense(2048, input_shape=input_shape)) 
	model.add(Dense(128, activation='relu'))
	model.add(Dense(128, activation='relu')) 
	model.add(Dense(MAX_ACTION_SPACE_SIZE, activation='linear'))
	model.compile(loss='mse', optimizer=Adam(lr=0.001), 
		metrics=['accuracy'])
	return model

class DQNAgent():
	def __init__(self, input_shape, log_path=None, replay_memory_path=None, 
		model_path=None, training=True, epsilon=1, epsilon_decay=0.99, 
		random_moves=None, copy_target_model=True, replay_memory=None):

		self.current_epoch = 0
		self.decay_iterations = 0
		self.min_epsilon_iterations = 0

		self.input_shape = input_shape

		self.model = self.create_model()

		self.target_model = self.create_model()
		if copy_target_model:
			self.target_model.set_weights(self.model.get_weights())

		#TODO: don't initialize dequeue if not training
		if replay_memory == None:
			self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
		else:
			self.replay_memory = replay_memory

		self.epsilon = epsilon
		self.epsilon_decay = epsilon_decay
		self.min_epsilon = 0.001

		self.target_update_counter = 0
		self.update_target_every = 5

		self.log_path = log_path
		self.replay_memory_path = replay_memory_path
		self.model_path = model_path

		self.training = training
		if random_moves == None:
			self.random_moves = self.training
		else:
			self.random_moves = random_moves

	def create_model(self):
		return create_model(self.input_shape)

	def update_replay_memory(self, transition):
		self.replay_memory.append(transition)

	def get_qs(self, state):
		#NOTE: let gamestate class handle normalization
		return self.model.predict(state)

	def decay_epsilon(self):
		self.log('decay_epsilon')
		if self.epsilon > self.min_epsilon:
			self.log(f'Epsilon was {self.epsilon}')
			self.epsilon *= self.epsilon_decay
			self.epsilon = max(self.min_epsilon, self.epsilon)
			self.log(f'Epsilon is now {self.epsilon}')

	def get_action(self, state, valid_actions):
		'''
		Chooses an action based on the current state. Assumes DQN output is 
		organized in the following way (with n possible moves in the game and
		m possible pokemon to switch to). The action chosen will be the action
		in valid_actions with the highest q value 

		move_0
		.
		.
		.
		move_n
		switch_pokemon_0
		.
		.
		.
		switch_pokemon_m
		'''
		rv = random.choice(valid_actions) + (None,) 

		#NOTE: grab zeroth element b/c we only passed in one state
		qs = self.get_qs(np.array([state]))[0] 

		formatted_actions = []
		for action_index, action_name, action_type in valid_actions:
			if action_type == ActionType.Move:
				try:
					action_q_index = (MOVE_NAME_TO_INDEX[action_name] - 
						MOVE_NAME_TO_INDEX['Min'])
				except KeyError:
					return rv
			elif action_type == ActionType.Switch:
				try:
					action_q_index = (MOVE_NAME_TO_INDEX['Count'] + 
						(POKEMON_NAME_TO_INDEX[action_name] - 
							POKEMON_NAME_TO_INDEX['Min']))
				except KeyError:
					return rv
			else:
				self.log(f'Unexpected action_type {action_type}')
				return rv

			try:
				q_value = qs[action_q_index]
			except IndexError:
				q_value = 0
				self.log(f'Unexpected index {action_q_index}')

			formatted_actions.append((action_q_index, 
				q_value, 
				(action_index, action_name, action_type)))

		#NOTE: As epsilon grows small, we make fewer random choices
		if (self.training or self.random_moves) and random.random() <= self.epsilon: 
			self.log(f'Making random choice (epsilon {self.epsilon})')
			q_index, q_value, action = random.choice(formatted_actions)
		else:
			self.log(f'Making q-valued choice (epsilon {self.epsilon})')
			formatted_actions = sorted(formatted_actions, key=lambda x: x[1])
			q_index, q_value, action = formatted_actions[-1]
		self.log(f'Actions available were {formatted_actions}')
		self.log(f'Choice was {action}')
		return action + (q_index,)

	def write_replay_memory(self):
		with open(self.replay_memory_path, 'w') as fd:
			fd.write(f'{self.replay_memory}')

	def train_only(self, minibatch_size, min_replay_memory_size):
		self.log('Saving replay_memory')
		if self.replay_memory_path:
			self.write_replay_memory()

		self.log('Saved replay_memory')

		if len(self.replay_memory) < min_replay_memory_size:
			self.log(f'Not enough transitions to train. '
				f'Only {len(self.replay_memory)} transitions')
			return

		minibatch = random.sample(self.replay_memory, minibatch_size)

		current_states = np.array([transition[0] for transition in minibatch])
		current_qs_list = self.model.predict(current_states)

		new_states = np.array([transition[3] for transition in minibatch])
		future_qs = self.target_model.predict(new_states)
		
		X = []
		y = []

		for index, (current_state, action, reward, new_state, done) in \
			enumerate(minibatch):

			if not done:
				max_future_q = np.max(future_qs[index])
				new_q = reward + DISCOUNT * max_future_q
			else:
				new_q = reward

			current_qs = current_qs_list[index]
			current_qs[action] = new_q

			X.append(current_state)
			y.append(current_qs)

		history = self.model.fit(np.array(X), np.array(y), 
			batch_size=minibatch_size, verbose=0, shuffle=False) 
		return history

	def train(self, terminal_state, minibatch_size=MINIBATCH_SIZE, 
		min_replay_memory_size=MIN_REPLAY_MEMORY_SIZE):
		
		if not self.training:
			return False

		self.train_only(minibatch_size, min_replay_memory_size)

		if terminal_state:
			self.target_update_counter += 1
			self.decay_epsilon()
			if self.epsilon > self.min_epsilon:
				self.decay_iterations += 1
			else:
				self.min_epsilon_iterations += 1

		if self.target_update_counter >= self.update_target_every:
			self.log('Updating target model')
			self.target_model.set_weights(self.model.get_weights())
			self.target_update_counter = 0

		return True

	def save_model(self, path=None):
		if path == None:
			path = self.model_path
		self.model.save(path)

	def load_model(self, path):
		self.model = load_model(path)

	def log(self, *args):
		if self.log_path == None:
			return 

		l = [str(arg) for arg in args]
		prefix = '[DQN]'
		string = '{} {}'.format(prefix, ' '.join(l))
		with open(self.log_path, 'a') as fd:
			fd.write(f'{string}\n')

	def update_epoch(self):
		self.log('update_epoch')
		self.log(f'decay_iterations: {self.decay_iterations}')
		self.log(f'min_epsilon_iterations: {self.min_epsilon_iterations}')
		if (self.epsilon <= self.min_epsilon and 
			self.decay_iterations <= self.min_epsilon_iterations):
			
			self.current_epoch += 1
		self.log(f'current_epoch is now {self.current_epoch}')
		return self.current_epoch

	def restart_epoch(self):
		self.log('restart epoch')
		self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
		self.decay_iterations = 0
		self.min_epsilon_iterations = 0
		self.epsilon = 1