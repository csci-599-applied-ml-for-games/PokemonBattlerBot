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

from GameState import POKEMON_NAME_TO_INDEX, MOVE_NAME_TO_INDEX

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1000
MINIBATCH_SIZE = 64

class ActionType(Enum):
	Move = auto()
	Switch = auto()

#5 pokemon to switch to, 4 moves for active pokemon
#TODO: handle mega
MAX_ACTION_SPACE_SIZE = 9
class DQNAgent():
	def __init__(self, input_shape, log_path=None, replay_memory_path=None, 
		training=True):

		self.input_shape = input_shape

		self.model = self.create_model()

		self.target_model = self.create_model()
		self.target_model.set_weights(self.model.get_weights())

		self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

		self.epsilon = 1 
		self.epsilon_decay = 0.99975
		self.min_epsilon = 0.001

		self.target_update_counter = 0
		self.update_target_every = 5

		self.log_path = log_path
		self.replay_memory_path = replay_memory_path

		self.training = training

	def create_model(self):
		model = Sequential()

		#NOTE: the current unit count (64) is chosen somewhat arbitrarily
		model.add(Dense(64, input_shape=self.input_shape)) 
		model.add(Dense(MAX_ACTION_SPACE_SIZE, activation='linear'))
		model.compile(loss='mse', optimizer=Adam(lr=0.001), 
			metrics=['accuracy'])
		return model

	def update_replay_memory(self, transition):
		self.replay_memory.append(transition)

	def get_qs(self, state):
		#NOTE: let gamestate class handle normalization
		return self.model.predict(state)

	def decay_epsilon(self):
		if self.epsilon > self.min_epsilon:
			self.epsilon *= self.epsilon_decay
			self.epsilon = max(self.min_epsilon, self.epsilon)

	def get_action(self, state, valid_actions):
		rv = random.choice(valid_actions) + (None,) 

		qs = self.get_qs(np.array([state]))
		
		#NOTE: sort actions so that our output indices always match the actions 
		sorted_actions = []
		for action_index, action_name, action_type in valid_actions:
			try:
				if action_type == ActionType.Move:
					action_dqn_index = MOVE_NAME_TO_INDEX[action_name]
				elif action_type == ActionType.Switch:
					action_dqn_index = POKEMON_NAME_TO_INDEX[action_name]
				else:
					self.log('ERROR: Somehow found invalid action type: '
						f'{action_type}')
					return rv
			except KeyError:
				self.log(f'ERROR: Unrecognized action_name {action_name} ' 
					f'with type {action_type}')
				return rv

			sorted_actions.append((action_dqn_index, action_index, action_name, 
				action_type))
		
		sorted_actions = sorted(sorted_actions, key=lambda x: x[0])
		
		#NOTE: now sort by q values
		formatted_actions = []
		for q_index, action_dqn_index, action_index, action_name, action_type \
			in enumerate(sorted_actions):

			try:
				formatted_actions.append(q_index, qs[q_index], 
					(action_index, action_name, action_type))
			except IndexError:
				self.log(f'ERROR: Bad q_index {q_index}')
				return rv

		#NOTE: As epsilon grows small, we make fewer random choices
		if self.training and random.random() <= epsilon: 
			self.log(f'Making random choice (epsilon {epsilon})')
			q_index, q_value, action = random.choice(formatted_actions)
		else:
			self.log(f'Making q-valued choice (epsilon {epsilon})')
			formatted_actions = sorted(formatted_actions, key=lambda x: x[1])
			q_index, q_value, action = formatted_actions[-1]
		
		return action, q_index

	def train(self, terminal_state):
		if not self.training:
			return

		self.log('Saving replay_memory')
		if self.replay_memory_path:
			with open(self.replay_memory_path, 'w') as fd:
				fd.write(f'{self.replay_memory}')
		self.log('Saved replay_memory')

		if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
			self.log(f'Not enough transitions to train. '
				f'Only {len(self.replay_memory)} transitions')
			return

		minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

		current_states = np.array([transition[0] for transition in minibatch])
		current_qs_list = self.target_model.predict(current_states)

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

		self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, 
			verbose=0, shuffle=False) 

		if terminal_state:
			self.target_update_counter += 1

		if self.target_update_counter >= self.update_target_every:
			self.log('Updating target model')
			self.target_model.set_weights(self.model.get_weights())
			self.target_update_counter = 0

			self.decay_epsilon()

	def log(self, *args):
		if self.log_path == None:
			return 

		l = [str(arg) for arg in args]
		prefix = '[DQN]'
		string = '{} {}'.format(prefix, ' '.join(l))
		with open(self.log_path, 'a') as fd:
			fd.write(f'{string}\n')