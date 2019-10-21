'''
Usage:
	bot.py <username> <password> <expected_opponent> [--forever|--iterations=<iterations>|--epochs=<epochs>] [--challenge] [--modeltype=<modeltype>] [--load_model=<model_path>] [--epsilondecay=<epsilondecay>] [--notraining|--trainer] [--printstats]

Arguments:
	<username> 			Username for the client
	<password>			Password for the account <username>
	<expected_opponent> The account name for the expected opponent
	<modeltype>			The type of model to use for the test
	<epsilondecay>		The decay rate for epsilon 
	<model_path> 		Path to a model to load into DQN agent 
Options:
	--epochs			The number of epochs to train for 
	--iterations 		The number of iterations to play against the opponent. 
	--forever			Run until someone kills the process 
	--challenge 		Challenge the expected_opponent when not playing a game
	--notraining		Just run with the model. No training
	--trainer  			If acting as a trainer for another process
	--printstats 		Prints the win/loss rate of this process 
'''

import sys
import os
import random 
import json 
import csv
import time
from datetime import datetime
from enum import Enum, auto

from docopt import docopt 

import showdown 

from gamestate import GameState
from dqn import DQNAgent, ActionType

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
BOT_DIR = os.path.dirname(__file__)
TYPE_MAP = {}

class RandomModel():
	def __init__(self):
		pass

	def get_action(self, state, valid_actions):
		#NOTE: Adding the None tuple is for compatibility with DQN 
		return random.choice(valid_actions) + (None,)

	def update_replay_memory(*args, **kwargs):
		pass

	def train(*args, **kwargs):
		pass

class RunType(Enum):
	Iterations = auto()
	Epochs = auto()
	Forever = auto()

class BotClient(showdown.Client):
	def __init__(self, name='', password='', loop=None, max_room_logs=5000,
		server_id='showdown', server_host=None, expected_opponent=None,
		team=None, challenge=False, runType=RunType.Iterations, runTypeData=1,
		agent=None, print_stats=False, trainer=False):

		if expected_opponent == None:
			raise Exception("No expected opponent found in arguments")
		else:
			self.expected_opponent = expected_opponent
		if team == None:
			raise Exception("No team found in arguments")
		else:
			self.team_text = team

		self.iterations_run = 0

		self.runType = runType 
		if self.runType == RunType.Iterations:
			self.iterations = runTypeData 
		elif self.runType == RunType.Epochs:
			self.epochs = runTypeData

		if agent == None:
			self.agent = RandomModel()
		else:
			self.agent = agent
		self.state_vl = None
		self.action = None

		self.logs_dir = LOGS_DIR
		if not os.path.exists(self.logs_dir):
			os.mkdir(self.logs_dir)
		self.datestring = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
		self.update_log_paths()

		self.challenge = challenge
		self.has_challenged = False

		self.wins = 0
		self.losses = 0
		self.print_stats = print_stats

		self.trainer = trainer

		super().__init__(name=name, password=password, loop=loop, 
			max_room_logs=max_room_logs, server_id=server_id, 
			server_host=server_host)

	def update_log_paths(self):
		self.log_file = os.path.join(self.logs_dir, 
			f'{self.datestring}_Iteration{self.iterations_run}.txt')
		self.agent.log_path = self.log_file
		self.agent.replay_memory_path = os.path.join(self.logs_dir, 
			f'{self.datestring}_Iteration{self.iterations_run}_'
			'replaymemory.txt')
		self.agent.model_path = os.path.join(self.logs_dir, 
			f'{self.datestring}_Iteration{self.iterations_run}.model')

	def log(self, *args):
		now = datetime.now()
		l = [str(arg) for arg in args]
		string = ' '.join(l)
		with open(self.log_file, 'a') as fd:
			fd.write(f'[{datetime.now()}] {string}\n')

	def should_play_new_game(self):
		if self.runType == RunType.Iterations:
			return self.iterations_run < self.iterations
		elif self.runType == RunType.Epochs:
			return self.agent.current_epoch < self.epochs
		elif self.runType == RunType.Forever:
			return True
		else:
			self.log(f'Unexpected run type {self.runType}')
			raise Exception('Unexpected run type')
	
	@staticmethod
	def get_team_info(data):
		return data['side']['pokemon']

	async def switch_pokemon(self, room_obj, data):
		team_info = self.get_team_info(data)
		switch_available = []
		for pokemon_index, pokemon_info in enumerate(team_info):
			if 'fnt' not in pokemon_info['condition']:
				switch_available.append(pokemon_index + 1)
		switch_index = random.choice(switch_available)
		await room_obj.switch(switch_index)

	async def take_action(self, room_obj, data):
		self.log(f'data: {data}')
		moves = data.get('active')[0].get('moves')
		self.log(f'Moves: {moves}')
		valid_actions = []
		for move_index, move_data in enumerate(moves):
			if move_data.get('pp', 0) > 0:
				valid_actions.append((move_index + 1, 
					move_data['move'], 
					ActionType.Move))
		move_count = len(moves)

		team_info = self.get_team_info(data)
		for pokemon_index, pokemon_info in enumerate(team_info):
			fainted = 'fnt' in pokemon_info.get('condition')
			if (not pokemon_info.get('active', False) and 
				not fainted):
				self.log('cleaning name')
				pokemon_name = self.gs.pokemon_name_clean(pokemon_info['details'])
				self.log('appending')
				valid_actions.append((pokemon_index + 1 , 
					pokemon_name, 
					ActionType.Switch))
		
		self.log(f'valid_actions: {valid_actions}')

		action_index, action_string, action_type, self.action = \
			self.agent.get_action(self.gs.vector_list, valid_actions)

		if action_type == ActionType.Move:
			await room_obj.move(action_index) 
		elif action_type == ActionType.Switch:
			await room_obj.switch(action_index)
		else:
			self.log(f'Unexpected action type {action_type}')

	def own_pokemon(self, pokemon_data):
		return pokemon_data.startswith(self.position)

	@staticmethod
	def get_owner(pokemon_data):
		return pokemon_data.split(':')[0].strip()

	@staticmethod
	def get_pokemon(pokemon_data):
		return pokemon_data.split(':')[1].strip()

	def add_status(self, statuses, pokemon_name, status):
		pokemon_statuses = statuses.get(pokemon_name, [])
		pokemon_statuses.append(status)
		statuses[pokemon_name] = pokemon_statuses
		
		self.log('Self Status', self.statuses)
		self.log('Opp Status', self.opp_statuses)

	def remove_status(self, statuses, pokemon_name, status):
		pokemon_statuses = statuses.get(pokemon_name, [])
		try:
			pokemon_statuses.remove(status)
		except ValueError:
			pass
		statuses[pokemon_name] = pokemon_statuses

		self.log('Self Status', self.statuses)
		self.log('Opp Status', self.opp_statuses)

	async def challenge_expected(self):
		self.log("Challenging {}".format(self.expected_opponent))
		await self.cancel_challenge()
		time.sleep(1)
		await self.send_challenge(self.expected_opponent, self.team_text, 
			'gen7ou')

	def set_and_check_team(self, player, team):
		self.gs.set_team(player, team)
		for position, member in enumerate(team):
			vector_pokemon = self.gs.check_team_position(player, position)
			self.log(f'Vector team member: {vector_pokemon}')

			if member != vector_pokemon:
				self.log('WARNING: mismatched pokemon')
			else:
				types = TYPE_MAP.get(vector_pokemon)
				self.log(f'{vector_pokemon} has types from TYPE_MAP: {types}')
				self.gs.set_types(player, vector_pokemon, types)
				has_types = self.gs.check_types(player, vector_pokemon)
				if set(has_types) != set(types):
					self.log(f'WARNING: {vector_pokemon} has unexpected types')
				self.log(f'{vector_pokemon} has types {has_types}')

	async def on_receive(self, room_id, inp_type, params):
		self.log(f'Input type: {inp_type}')
		self.log(f'Params: {params}')

		room_obj = self.rooms.get(room_id)
		if room_obj and room_obj.id.startswith('battle-'):
			if inp_type == 'poke':
				owner = params[0]
				pokename = GameState.pokemon_name_clean(params[1])
				if owner == self.position:
					self.team.append(pokename)
				else:
					self.opp_team.append(pokename)

				if (len(self.team) == self.teamsize and
					len(self.opp_team) == self.opp_teamsize):

					self.log(f'Team: {self.team}')
					self.log(f'Opp team: {self.opp_team}')
					
					self.gs = GameState()
					self.set_and_check_team(GameState.Player.one, self.team)
					self.set_and_check_team(GameState.Player.two, self.opp_team)

					#NOTE: Select starting pokemon here 
					start_index = random.randint(1, self.teamsize)
					await room_obj.start_poke(start_index)

			elif inp_type == 'teamsize':
				position = params[0]
				if position == self.position:
					self.teamsize = int(params[1])
					self.team = []
				else:
					self.opp_teamsize = int(params[1])
					self.opp_team = []

			elif inp_type == 'player':
				name = params[1]
				position = params[0] 
				if name == self.name:
					self.position = position

			elif inp_type == 'turn':
				self.turn_number = int(params[0])
				if self.turn_number == 1:
					self.state_vl = self.gs.vector_list
					self.reward = 0
					reward = self.reward
				else:
					#NOTE: this should be changed if using other reward functions besides win or lose the game
					reward = self.reward
					self.reward = 0
					
					last_state = [element for element in self.state_vl]
					self.state_vl = self.gs.vector_list
					done = False

					transition = (last_state, 
						self.action, 
						reward, 
						self.state_vl, 
						done)
					self.log(f'Updating replay memory with {transition}')
					self.agent.update_replay_memory(transition)
					self.log(f'Successfully updated replay memory')
					self.agent.train(False)
					self.log(f'Trained')
				self.log(f'This transition\'s reward was {reward}')
			elif inp_type == 'request':
				json_string = params[0]
				data = json.loads(json_string)
				self.last_request_data = data
				team_info = self.get_team_info(data)
				self.team_abilities = {}
				self.team_items = {}
				self.team_moves = {}
				for pokemon_info in team_info:
					self.log('info', pokemon_info)
					pokemon_name = GameState.pokemon_name_clean(pokemon_info['details'])
					# get the ability for each pokemon
					self.team_abilities[pokemon_name] = pokemon_info['ability']
					# track the items each pokemon
					self.team_items[pokemon_name] = pokemon_info['item']
					# track the team movelist?
					self.team_moves[pokemon_name] = pokemon_info['moves']
					# if pokemon_info.get('active'):
						# self.active_pokemon = pokemon_info['details'].rstrip(', M').rstrip(', F')
						# self.log('active_pokemon', self.active_pokemon)
						# self.log('active_pokemon types', TYPE_MAP.get(self.active_pokemon))
						#break // removed this line so it would get all the moves and stuff and things ya know
				self.log('team abilities', self.team_abilities)
				self.log('team items', self.team_items)
				self.log('team moves', self.team_moves)	
				force_switch = data.get('forceSwitch', [False])[0]
				if force_switch == True:
					# switch_available = []
					# for pokemon_index, pokemon_info in enumerate(team_info):
					# 	if 'fnt' not in pokemon_info['condition']:
					# 		switch_available.append(pokemon_index + 1)
					# switch_index = random.choice(switch_available)
					# await room_obj.switch(switch_index)

					await self.switch_pokemon(room_obj, data)
				else:
					await self.take_action(room_obj, data)
			
			elif inp_type == '-status':
				'''
				NOTE: statuses
				brn
				par
				slp
				frz
				psn
				tox
				confusion
				flinch
				trapped
				trapper
				partiallytrapped
				lockedmove
				twoturnmove
				choicelock
				mustrecharge
				futuremove
				healreplacement
				stall
				gem
				raindance
				primordialsea
				sunnyday
				desolateland
				sandstorm
				hail
				deltastream
				arceus
				silvally
				'''
				pokemon_data = params[0]
				pokemon_name = self.get_pokemon(pokemon_data)
				status = params[1]
				if self.own_pokemon(pokemon_data):
					self.add_status(self.statuses, pokemon_name, status)
				else:
					self.add_status(self.opp_statuses, pokemon_name, status)

			elif inp_type == '-start':
				pokemon_data = params[0]
				pokemon_name = self.get_pokemon(pokemon_data)
				status = params[1]
				if self.own_pokemon(pokemon_data):
					self.add_status(self.statuses, pokemon_name, status)
				else:
					self.add_status(self.opp_statuses, pokemon_name, status)

			elif inp_type == '-end':
				pokemon_data = params[0]
				pokemon_name = self.get_pokemon(pokemon_data)
				status = params[1]
				if self.own_pokemon(pokemon_data):
					self.remove_status(self.statuses, pokemon_name, status)
				else:
					self.remove_status(self.opp_statuses, pokemon_name, status)

			elif inp_type == '-curestatus':
				pokemon_data = params[0]
				pokemon_name = self.get_pokemon(pokemon_data)
				status = params[1]
				if self.own_pokemon(pokemon_data):
					self.remove_status(self.statuses, pokemon_name, status)
				else:
					self.remove_status(self.opp_statuses, pokemon_name, status)

			elif inp_type == 'switch':
				name_with_owner = params[0]
				name_with_details = params[1]
				my_pokemon = self.own_pokemon(name_with_owner)

				volatile_statuses = ['confusion', 'curse']
				if my_pokemon:
					pokemon_name = self.active_pokemon
					statuses = self.statuses
				else:
					pokemon_name = self.opp_active_pokemon
					statuses = self.opp_statuses
				for volatile_status in volatile_statuses:
					self.remove_status(statuses, pokemon_name, volatile_status)

				new_active_name = GameState.pokemon_name_clean(name_with_details)
				if not my_pokemon:
					self.opp_active_pokemon = new_active_name
					self.log('Opp active', self.opp_active_pokemon)
					self.set_active(GameState.Player.two, self.opp_active_pokemon)
					if not self.gs.check_active(GameState.Player.two, 
						self.opp_active_pokemon):
						
						self.log(f'WARNING: {self.opp_active_pokemon}'
							' was not active as expected')
				else:
					self.active_pokemon = new_active_name
					self.log('active_pokemon', self.active_pokemon)
					self.set_active(GameState.Player.one, self.active_pokemon)
					if not self.gs.check_active(GameState.Player.one, 
						self.active_pokemon):
						
						self.log(f'WARNING: {self.active_pokemon}'
							' was not active as expected')

			elif inp_type == 'weather':
				self.weather = params[0]
				self.log('New weather: {}'.format(self.weather))

			elif inp_type == '-sidestart':
				position = params[0].split(':')[0]
				hazard = params[1].lstrip('move: ')
				if position.startswith(self.position):
					self.sidestart.append(hazard)
				else:
					self.opp_sidestart.append(hazard)

				self.log('Self sidestart', self.sidestart)
				self.log('Opp sidestart', self.opp_sidestart)

			elif inp_type == '-sideend':
				position = params[0].split(':')[0]
				if position.startswith(self.position):
					try:
						self.sidestart.remove(params[1])
					except ValueError:
						pass
				else:
					try:
						self.opp_sidestart.remove(params[1])
					except ValueError:
						pass

				self.log('Self sidestart', self.sidestart)
				self.log('Opp sidestart', self.opp_sidestart)

			elif inp_type == 'error':
				if params[0].startswith('[Invalid choice]'):
					if ("Can't switch: You can't switch to an active Pokémon" 
						in params[0]):
						await self.switch_pokemon(room_obj, 
							self.last_request_data)
					else:
						await self.take_action(room_obj, self.last_request_data)

			elif inp_type == 'win':
				done = True

				winner = params[0]
				if winner == self.name:
					self.wins += 1
					self.log("We won")
					reward = 12 
				else:
					self.losses += 1
					self.log("We lost")
					reward = -12

				last_state = [element for element in self.state_vl]
				self.state_vl = self.gs.vector_list
				
				transition = (last_state, 
					self.action, 
					reward, 
					self.state_vl, 
					done)
				self.log(f'Updating replay memory with {transition}')
				self.agent.update_replay_memory(transition)
				self.log(f'Successfully updated replay memory')
				trained = self.agent.train(True)
				if trained:
					self.log(f'Trained')
					path = self.agent.save_model()
					old_epoch = self.agent.current_epoch
					epoch = self.agent.update_epoch()
					if old_epoch < epoch:
						self.log('Saving epoch model')
						epoch_model_path = os.path.join(self.logs_dir, 
							f'Epoch{epoch}.model')
						self.agent.save_model(path=epoch_model_path)
						self.agent.restart_epoch()
				else:
					self.log(f'Not trained')
					
				await room_obj.leave()
				self.iterations_run += 1
				self.update_log_paths()
				
				if self.should_play_new_game():
					self.log("Starting iteration {}".format(self.iterations_run))
					if self.challenge:
						time.sleep(5)
						await self.challenge_expected()
				else:
					if self.print_stats:
						win_ratio = (float(self.wins) / 
							float(self.wins + self.losses))
						print(f'Win ratio: {win_ratio}')
					sys.exit(0)

			elif inp_type == '-ability':
				# might work to track some abilities but so far weather abilities and other abilities
				# are only made known when a specific game action is made.
				self.log('ability')
				#self.log(params)
			
			elif inp_type == '-damage':
				player = params[0][0:2]
				pokemon = params[0].strip('p1a: ').strip('p2a ')
				health = params[1]
				if 'fnt' in health:
					self.log(f'{player}\'s {pokemon} has fainted')
					if (player == self.position):
						self.reward = -1
					else:
						self.reward = 1

					#TODO: add faint to gamestate

				# this section to track the enemy abilities
				if (len(params) == 4):
					pokemon = params[3].strip('[of] p1a: ')
					ability = params[2].strip('[from] ability: ')
					# self.enemy_state.update_abilities(pokemon, ability)
					self.log('Pokemon: ', pokemon, 'Enemy Ability: ', self.enemy_state.team_abilities[pokemon])
			
			elif inp_type == '-mega':
				if ('p1a' in str(params[0])):
					# Opposing player Mega 
					# TODO: Add which pokemon used 
					pokemon = params[0].strip('p1a: ') # just easier to read this way
					# self.enemy_state.update_team_mega(pokemon)
					self.opp_mega = True
					self.log('Enemy Mega Active: ', self.enemy_state.team_mega[pokemon])
				else:
					# AI uses mega
					self.mega = True

			elif inp_type == '-item':
				# how do we use items I don't get it...
				self.log('item')
				#self.log(params)

			elif inp_type == 'move':
				if ('p1a' in str(params[0])):
					# player 1 active pokemon used move.
					pokemon = params[0].strip('p1a: ')
					# self.enemy_state.update_moves_list(pokemon, params[1])
					self.log('P1 used: ', params[1])
					self.log('Enemy Moves State:', self.enemy_state.team_moves)
				else:
					# player 2 pokemon used move.
					my_move = params[1]
					self.log('P2 used: ', my_move)

			elif inp_type == '-zpower':
				if ('p1a' in str(params[0])):
					# opposing player used Z Power
					pokemon = params[0].strip('p1a: ')
					# self.enemy_state.update_used_zpower(pokemon)
					self.opp_zpower = True
				else:
					# Add which pokemon used the zpower obviously but should discuss data structure 
					# and design of objects first.
					self.z_power = True

			elif inp_type == '-weather':
				self.log('weather', params)
		else:
			if inp_type == 'updateuser':
				if (self.name == params[0].strip() and self.challenge and 
					not self.has_challenged):
					self.has_challenged = True
					time.sleep(1)
					await self.challenge_expected()

	async def on_private_message(self, pm):
		if pm.recipient == self:
			await pm.reply(pm.content)

	async def on_challenge_update(self, challenge_data):
		incoming = challenge_data.get('challengesFrom', {})
		if self.expected_opponent.lower() in incoming:
			if self.trainer:
				model_paths = [os.path.join(self.logs_dir, content) 
					for content in os.listdir(self.logs_dir) 
					if content.endswith('.model') and 
						content.startswith('Epoch')]
				if len(model_paths) > 0:
					sorted_model_paths = sorted(model_paths, 
						key=lambda x: 
							int(os.path.basename(x).lstrip('Epoch').rstrip('.model')))
					model_to_load = sorted_model_paths[-1]
					self.log(f'Loading model {model_to_load}')
					self.agent.load_model(model_to_load)
			await self.accept_challenge(self.expected_opponent, self.team_text)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			self.log(f'Room ID: {room_obj.id}')
			self.active_pokemon = None
			self.statuses = {}
			self.sidestart = []

			self.opp_active_pokemon = None
			self.opp_statuses = {}
			self.opp_sidestart = []

			self.weather = 'none'

def main():
	args = docopt(__doc__) 

	username = args['<username>']
	password = args['<password>']
	expected_opponent = args['<expected_opponent>']
	
	forever = args['--forever']
	if not forever:
		iterations = (int(args['--iterations']) if args['--iterations'] != None 
			else None)
		if not iterations:
			epochs = (int(args['--epochs']) if args['--epochs'] != None 
				else None)
			runType = RunType.Epochs
			runTypeData = epochs
		else:
			runType = RunType.Iterations
			runTypeData = iterations
			epochs = None
	else:
		runType = RunType.Forever
		runTypeData = None
		iterations = None
		epochs = None

	challenge = args['--challenge']
	model_type = args['--modeltype'] if args['--modeltype'] != None else 'dqn'
	epsilon_decay = (float(args['--epsilondecay']) 
		if args['--epsilondecay'] != None 
		else 0.99)
	trainer = args['--trainer']
	if trainer:
		is_training = False
	else:
		is_training = not args['--notraining'] 

	load_model_path = args.get('--load_model')
	print_stats = args.get('--printstats')

	with open(os.path.join(BOT_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()
	
	with open(os.path.join(BOT_DIR, 'data/PokemonTypes.csv'), 'r') as typefile:
		reader = csv.reader(typefile, delimiter=',')		
		for row in reader:
			name = row[1]
			type1 = row[2]
			type2 = row[3]
			TYPE_MAP[name] = []
			if type1 != '':
				TYPE_MAP[name].append(type1)
			if type2 != '':
				TYPE_MAP[name].append(type2)

	if model_type == 'dqn':
		input_shape = (GameState.vector_dimension(),)

		agent = DQNAgent(input_shape, epsilon_decay=epsilon_decay, 
			training=is_training)
		if load_model_path:
			agent.load_model(load_model_path)


		BotClient(name=username, password=password, 
			expected_opponent=expected_opponent, team=team, 
			challenge=challenge, runType=runType, runTypeData=runTypeData, 
			agent=agent, print_stats=print_stats, trainer=trainer).start()
	elif model_type == 'random':
		input_shape = (GameState.vector_dimension(),)
		BotClient(name=username, password=password, 
			expected_opponent=expected_opponent, team=team, 
			challenge=challenge, runType=RunType.Iterations, 
			runTypeData=iterations, agent=None, print_stats=print_stats).start()

if __name__ == '__main__':
	random.seed()
	main()