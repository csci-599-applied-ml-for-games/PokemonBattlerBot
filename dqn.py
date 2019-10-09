'''
As of Oct. 8, 2019, Code is based on 
https://pythonprogramming.net/deep-q-learning-dqn-reinforcement-learning-python-tutorial/
and 
https://pythonprogramming.net/training-deep-q-learning-dqn-reinforcement-learning-python-tutorial/?completed=/deep-q-learning-dqn-reinforcement-learning-python-tutorial/
'''
import os

from keras.models import Sequential
from keras.layers import Dense
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1000
MINIBATCH_SIZE = 64

#5 pokemon to switch to, 4 moves for active pokemon
#TODO: handle mega
MAX_ACTION_SPACE_SIZE = 9
class DQNAgent():
	def __init__(self, type):
		self.model = self.create_model()

		self.target_model = self.create_model()
		self.target_model.set_weights(self.model.get_weights())

		self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

		self.epsilon = 1 
		self.epsilon_decay = 0.99975
		self.min_epsilon = 0.001

		self.target_update_counter = 0
		self.update_target_every = 5

	def create_model(self):
		model = Sequential()

		model.add(Dense(64))
		model.add(Dense(MAX_ACTION_SPACE_SIZE, activation='relu'))

		model.compile()
		return model

	def update_replay_memory(self, transition):
		self.replay_memory.append(transition)

	def get_qs(self, state):
		#NOTE: let gamestate class handle normalization
		return self.model.predict(state)

	def get_action(self, state, actions):

	def train(self, terminal_state):
		if len(self.replay_memory) < MIN_REPLAY_SIZE:
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
			self.target_model.set_weights(self.model.get_weights())
			self.target_update_counter = 0

