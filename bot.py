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
import util
from datetime import datetime
from enum import Enum, auto
import re
import asyncio
import traceback

from docopt import docopt 

import showdown 

from gamestate import GameState, health_sum, ko_count, clean_move_name
from dqn import DQNAgent, ActionType

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
REPLAY_MEMORY_DIR = os.path.join(LOGS_DIR, 'replay_memory')
BOT_DIR = os.path.dirname(__file__)
TYPE_MAP = {}
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

INPUT_SHAPE = (GameState.vector_dimension(),)
		
class RandomAgent():
	def __init__(self):
		pass

	def get_action(self, state, valid_actions):
		#NOTE: Adding the None tuple is for compatibility with DQN 
		return random.choice(valid_actions) + (None,)

	def update_replay_memory(*args, **kwargs):
		pass

	def train(*args, **kwargs):
		return False

class RunType(Enum):
	Iterations = auto()
	Epochs = auto()
	Forever = auto()

def hack_name(pokemon):
	if pokemon == 'Tornadus': 
		return 'Tornadus-Therian'
	else:
		return pokemon

def calculate_reward(bot, last_state, current_state, health_change=1.0,
	opp_health_change=-1.0, knock_out=-4.0, opp_knock_out=4.0):
	'''
	last_state: vector list from previous turn's gamestate
	
	current_state: vector list from current turn's gamestate
	
	health_change: float. default value 1.0. 
	multiplied by sum of normalized health change for all of player's pokemon 
	as a part of episode reward

	opp_health_change: float. default value 1.0.
	multiplied by sum of normalized health change for all of opponent's pokemon
	as a part of episode reward

	knock_out: float. default value -4.0.
	multiplied by the number of player's pokemon which have been knocked out 
	since last_state

	knock_out_penalty: float. default value 4.0
	multiplied by the number of opponent's pokemon which have been knocked out
	since last_state 
	'''
	reward = 0
	p1_health_change = (health_sum(current_state, GameState.Player.one) - 
		health_sum(last_state, GameState.Player.one))
	bot.log(f'p1_health_change: {p1_health_change}')
	reward += health_change * p1_health_change
	bot.log(f'reward is now {reward}')

	p2_health_change = (health_sum(current_state, GameState.Player.two) - 
		health_sum(last_state, GameState.Player.two))
	bot.log(f'p2_health_change: {p2_health_change}')
	reward += opp_health_change * p2_health_change
	bot.log(f'reward is now {reward}')
	
	p1_ko_change = (ko_count(current_state, GameState.Player.one) - 
		ko_count(last_state, GameState.Player.one))
	bot.log(f'p1_ko_change: {p1_ko_change}')
	reward += knock_out * p1_ko_change
	bot.log(f'reward is now {reward}')

	p2_ko_change = (ko_count(current_state, GameState.Player.two) - 
		ko_count(last_state, GameState.Player.two))
	bot.log(f'p2_ko_change: {p2_ko_change}')
	reward += opp_knock_out * p2_ko_change
	bot.log(f'reward is now {reward}')

	return reward

class BotClient(showdown.Client):
	health_regex = re.compile(r'(?P<numerator>[0-9]+)/(?P<denominator>[0-9]+)')

	def __init__(self, name='', password='', loop=None, max_room_logs=5000,
		server_id='showdown', server_host=None, expected_opponent=None,
		team=None, challenge=False, runType=RunType.Iterations, runTypeData=1,
		agent=None, print_stats=False, trainer=False, save_model=True,
		should_write_replay=False
	):
		self.should_write_replay = should_write_replay
		self.done = False
		
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
			self.agent = RandomAgent()
		else:
			self.agent = agent
		self.state_vl = None
		self.action = None

		self.logs_dir = LOGS_DIR
		if not os.path.exists(self.logs_dir):
			os.mkdir(self.logs_dir)
		
		self.replay_memory_dir = REPLAY_MEMORY_DIR
		if not os.path.exists(self.replay_memory_dir):
			os.mkdir(self.replay_memory_dir)
		self.datestring = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
		self.update_log_paths()

		self.challenge = challenge
		self.has_challenged = False

		# flag used to detect the first 'request' inp_type
		# first request is used to initialize moves for gamestate
		# Rreset to false for every battle
		self.is_first_request = True

		# Keep a track of zmoves used, as each pokemon can use z moves only once
		# per battle, we update each zmove here used per battle so it can't be used
		# again. Reset to empty list after battle ends
		# type: [{pokemon_name : zmove}]
		self.zmoves_tracker = []

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
		self.agent.replay_memory_path = os.path.join(
			self.logs_dir, 
			'replay_memory', 
			f'{self.datestring}_Iteration{self.iterations_run}_replaymemory.txt'
		)
		self.agent.model_path = os.path.join(self.logs_dir, 
			f'{self.datestring}_Iteration{self.iterations_run}.model')

	def write_replay_memory(self):
		self.agent.write_replay_memory()

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

	def save_replay(self, room_obj):
		replays_dir = os.path.join(BOT_DIR, 'replays')
		if not os.path.exists(replays_dir):
			os.mkdir(replays_dir)
		replay_file = f'{self.datestring}_Iteration{self.iterations_run}.html'
		with open(os.path.join(replays_dir, replay_file), 'wb') as f:
			f.write(util.get_replay_header())
			joined = '\n'.join(room_obj.logs)
			f.write('\n'.join(room_obj.logs).encode('utf-8'))
			f.write(util.get_replay_footer())
	
	@staticmethod
	def get_team_info(data):
		return data['side']['pokemon']

	async def switch_pokemon(self, room_obj, data):
		'''
		For use with forceswitch scenarios
		'''
		try:
			valid_actions = []
			team_info = self.get_team_info(data)
			for pokemon_index, pokemon_info in enumerate(team_info):
				fainted = 'fnt' in pokemon_info.get('condition')
				if (not pokemon_info.get('active', False) and 
					not fainted):

					pokemon_name = self.gs.pokemon_name_clean(pokemon_info['details'])
					valid_actions.append((pokemon_index + 1 , 
						pokemon_name, 
						ActionType.Switch))
			
			self.log(f'valid_actions: {valid_actions}')

			action_index, action_string, action_type, _ = \
				self.agent.get_action(self.gs.vector_list, valid_actions)
		except Exception as err:
			self.log_error(err)

		if action_type == ActionType.Switch:
			await room_obj.switch(action_index)
		else:
			self.log(f'Unexpected action type {action_type}')

	async def take_action(self, room_obj, data, delay=0):
		await asyncio.sleep(delay) 
		#NOTE: delay is here to make sure we get all the data before taking action
		try:
			moves = data.get('active')[0].get('moves')
			valid_actions = []
			for move_index, move_data in enumerate(moves):
				if (( move_data.get('pp', 0) > 0 and not move_data.get('disabled'))
					or move_data.get('move') == 'Struggle'):
					
					valid_actions.append((move_index + 1, 
						clean_move_name(move_data['move']), 
						ActionType.Move))
			move_count = len(moves)

			team_info = self.get_team_info(data)
			for pokemon_index, pokemon_info in enumerate(team_info):
				fainted = 'fnt' in pokemon_info.get('condition')
				if (not pokemon_info.get('active', False) and 
					not fainted):

					pokemon_name = self.gs.pokemon_name_clean(pokemon_info['details'])
					valid_actions.append((pokemon_index + 1 , 
						pokemon_name, 
						ActionType.Switch))
			
			self.log(f'valid_actions: {valid_actions}')

			action_index, action_string, action_type, self.action = \
				self.agent.get_action(self.gs.vector_list, valid_actions)
		except Exception as err:
			self.log_error(err)

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

	def add_status(self, player_name, pokemon_name, status):
		self.gs.set_status(player_name, pokemon_name, status)

	def remove_status(self, player_name, pokemon_name, status):
		self.gs.remove_status(player_name, pokemon_name, status)
		
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

	def log_error(self, err):
		self.log('ERROR')
		self.log(''.join(traceback.format_tb(err.__traceback__)))

	def update_replay_memory(self, transition):
		self.agent.update_replay_memory(transition)
		
	async def on_receive(self, room_id, inp_type, params):
		try:
			self.log(f'Input type: {inp_type}')
			self.log(f'Params: {params}')
		except Exception as err:
			self.log_error(err)
		
		try:
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
						
						self.gs = GameState()
						self.set_and_check_team(GameState.Player.one, self.team)
						self.set_and_check_team(GameState.Player.two, self.opp_team)

						self.gs.init_health(GameState.Player.one)
						self.gs.init_health(GameState.Player.two)

						self.gs.reset_boosts(GameState.Player.one)
						self.gs.reset_boosts(GameState.Player.two)

						#NOTE: Select starting pokemon here 
						valid_actions = []
						for pokemon_index, pokemon_name in enumerate(self.team):
							pokemon_name = self.gs.pokemon_name_clean(pokemon_name)
							valid_actions.append((pokemon_index + 1 , 
								pokemon_name, 
								ActionType.Switch))
						
						action_index, action_string, action_type, _ = \
							self.agent.get_action(self.gs.vector_list, valid_actions)

						if action_type == ActionType.Switch:
							await room_obj.start_poke(action_index)
						else:
							self.log(f'Unexpected action type {action_type}') 
						
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
					
					self.log(f'Weather: {self.gs.all_weather()}')

					self.log(f'P1 Boosts: {self.gs.all_boosts(GameState.Player.one)}')
					self.log(f'P2 Boosts: {self.gs.all_boosts(GameState.Player.two)}')

					active_pokemon = self.gs.all_active(GameState.Player.one)
					self.log(f'P1 active: {active_pokemon}')
					if len(active_pokemon) > 1:
						self.log('ERROR: More than one active pokemon')

					active_pokemon = self.gs.all_active(GameState.Player.two)
					self.log(f'P2 active: {active_pokemon}')
					if len(active_pokemon) > 1:
						self.log('ERROR: More than one active pokemon')

					self.log(f'P1 health: {self.gs.all_health(GameState.Player.one)}')
					self.log(f'P2 health: {self.gs.all_health(GameState.Player.two)}')

					self.log(f'P1 fainted: {self.gs.all_fainted(GameState.Player.one)}')
					self.log(f'P2 fainted: {self.gs.all_fainted(GameState.Player.two)}')

					self.log(f'P1 types: {self.gs.all_types(GameState.Player.one)}')
					self.log(f'P2 types: {self.gs.all_types(GameState.Player.two)}')

					self.log(f'P1 statuses: {self.gs.all_statuses(GameState.Player.one)}')
					self.log(f'P2 statuses: {self.gs.all_statuses(GameState.Player.two)}')

					self.log(f'P1 moves: {self.gs.all_moves(GameState.Player.one)}')
					self.log(f'P2 moves: {self.gs.all_moves(GameState.Player.two)}')

					self.log(f'P1 active slot check: {self.gs.check_active_slot(GameState.Player.one)}')
					self.log(f'P2 active slot check: {self.gs.check_active_slot(GameState.Player.two)}')

					if self.turn_number == 1:
						self.state_vl = self.gs.vector_list
						reward = 0
					else:
						last_state = [element for element in self.state_vl]
						self.state_vl = [element for element in self.gs.vector_list]
						done = False

						reward = calculate_reward(self, last_state, self.state_vl)
						transition = (last_state, 
							self.action, 
							reward, 
							self.state_vl, 
							done)
						self.update_replay_memory(transition)
						self.agent.train(False)
					self.log(f'This transition\'s reward was {reward}')
					
				elif inp_type == 'request':
					json_string = params[0]
					data = json.loads(json_string)
					wait = data.get('wait', False)
					if not wait:
						team_info = self.get_team_info(data)
						self.last_request_data = data

						# Initialize all available pokemon moves for game stats
						if self.is_first_request:
							for pokemon_info in team_info:
								pokemon_name = GameState.pokemon_name_clean(pokemon_info['details'])						
								for move_name in pokemon_info['moves']:
									# Initially PP = Max PP, so pseudo PP, Max PP values to set move
									# as PP, Max PP are available for only active Pokemons
									self.gs.set_move(GameState.Player.one, pokemon_name, move_name, 1.0, 1.0)

							self.is_first_request = False
							
						# Update PP for the active pokemon only
						else:
							for pokemon_info in team_info:
								pokemon_name = GameState.pokemon_name_clean(pokemon_info['details'])		
								if pokemon_info['active'] == True:
									if 'active' in data:
										moves = data['active'][0]['moves']
										for move in moves:
											self.gs.set_move(GameState.Player.one, pokemon_name, move['id'],
												move['pp'], move['maxpp'])
										
										if 'canZMove' in data['active'][0]:
											if pokemon_name not in self.zmoves_tracker:
												zmove_id = util.move_name_to_id(data['active'][0]['canZMove'][1]['move'])
												self.gs.set_move(GameState.Player.one, pokemon_name, zmove_id, 1.0, 1.0)

						# Update pokemon stat and items for game state
						for pokemon_info in team_info:
							pokemon_name = GameState.pokemon_name_clean(pokemon_info['details'])		
							stats = pokemon_info['stats']
							for stat_name in stats:
								self.gs.set_stat(GameState.Player.one, pokemon_name, stat_name, stats[stat_name])

							item = pokemon_info['item']
							# If item key has empty string if no item possesed by Pokemon,
							# item could have been knocked out or used my Pokemon
							if item == '':
								self.gs.clear_all_items(GameState.Player.one, pokemon_name)
							
							# Else update item with the current item even if there is no change
							# clear old item and set new item as a Pokemon can possess only an item at a time
							else:
								self.gs.clear_all_items(GameState.Player.one, pokemon_name)
								self.gs.set_item(GameState.Player.one, pokemon_name, item)	

						force_switch = data.get('forceSwitch', [False])[0]
						if force_switch == True:
							await self.switch_pokemon(room_obj, data)

						else:
							await self.take_action(room_obj, data, delay=0.3)
				
				elif inp_type == '-status':
					pokemon_data = params[0]
					pokemon_name = self.get_pokemon(pokemon_data)
					#TODO: remove this hack and have a good way of handling
					#TODO: detailed vs. non-detailed pokemon names
					pokemon_name = hack_name(pokemon_name)
					status = params[1]
					if self.own_pokemon(pokemon_data):
						self.add_status(GameState.Player.one, pokemon_name, status)

					else:
						self.add_status(GameState.Player.two, pokemon_name, status)

				elif inp_type == '-start':
					pokemon_data = params[0]
					pokemon_name = self.get_pokemon(pokemon_data)
					status = params[1]
					if self.own_pokemon(pokemon_data):
						self.add_status(GameState.Player.one, pokemon_name, status)

					else:
						self.add_status(GameState.Player.two, pokemon_name, status)

				elif inp_type == '-end':
					pokemon_data = params[0]
					pokemon_name = self.get_pokemon(pokemon_data)
					status = params[1]
					if self.own_pokemon(pokemon_data):
						self.remove_status(GameState.Player.one, pokemon_name, 
							status)

					else:
						self.remove_status(GameState.Player.two, pokemon_name, 
							status)

				elif inp_type == '-curestatus':
					pokemon_data = params[0]
					pokemon_name = self.get_pokemon(pokemon_data)
					status = params[1]
					if self.own_pokemon(pokemon_data):
						self.remove_status(GameState.Player.one, pokemon_name, 
							status)

					else:
						self.remove_status(GameState.Player.two, pokemon_name, 
							status)

				elif inp_type == 'switch':
					name_with_owner = params[0]
					name_with_details = params[1]
					my_pokemon = self.own_pokemon(name_with_owner)

					volatile_statuses = ['confusion', 'curse']
					if my_pokemon:
						pokemon_name = self.active_pokemon
						gs_player = GameState.Player.one
					else:
						pokemon_name = self.opp_active_pokemon
						gs_player = GameState.Player.two

					self.gs.reset_boosts(gs_player)
					
					if pokemon_name != None:
						for volatile_status in volatile_statuses:
							self.remove_status(gs_player, pokemon_name, 
								volatile_status)

					new_active_name = GameState.pokemon_name_clean(name_with_details)
					if not my_pokemon:
						self.opp_active_pokemon = new_active_name
						self.gs.set_active(GameState.Player.two, self.opp_active_pokemon)
						if not self.gs.check_active(GameState.Player.two, 
							self.opp_active_pokemon):
							
							self.log(f'WARNING: {self.opp_active_pokemon}'
								' was not active as expected')
					else:
						self.active_pokemon = new_active_name
						self.gs.set_active(GameState.Player.one, self.active_pokemon)
						if not self.gs.check_active(GameState.Player.one, 
							self.active_pokemon):
							
							self.log(f'WARNING: {self.active_pokemon}'
								' was not active as expected')

				elif inp_type == '-sidestart':
					position = params[0].split(':')[0]
					hazard = params[1].lstrip('move: ')
					if position.startswith(self.position):
						self.gs.increment_entry_hazard(GameState.Player.one, hazard)

					else:
						self.gs.increment_entry_hazard(GameState.Player.two, hazard)

				elif inp_type == '-sideend':
					position = params[0].split(':')[0]
					hazard = params[1]
					if position.startswith(self.position):
						self.gs.clear_entry_hazard(GameState.Player.one, hazard)
					
					else:
						self.gs.clear_entry_hazard(GameState.Player.two, hazard)

				elif inp_type == 'error':
					self.save_replay(room_obj)
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
						reward = 96
					else:
						self.losses += 1
						self.log("We lost")
						reward = -96

					last_state = [element for element in self.state_vl]
					self.state_vl = self.gs.vector_list
					
					transition = (last_state, 
						self.action, 
						reward, 
						self.state_vl, 
						done)
					self.update_replay_memory(transition)
					trained = self.agent.train(True)
					if trained and self.save_model:
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
						self.is_first_request = True
						self.zmoves_tracker = []
						self.log("Starting iteration {}".format(self.iterations_run))
						if self.challenge:
							time.sleep(5)
							await self.challenge_expected()
					else:
						if self.print_stats:
							win_ratio = (float(self.wins) / 
								float(self.wins + self.losses))
							print(f'Win ratio: {win_ratio}')
						self.done = True
						if self.should_write_replay:
							self.write_replay_memory()
						sys.exit(0)

				elif inp_type == '-ability':
					# might work to track some abilities but so far weather abilities and other abilities
					# are only made known when a specific game action is made.
					self.log('ability')
					#self.log(params)
				
				elif inp_type == 'faint':
					player = params[0][0:2]
					pokemon = params[0][4:].strip()

					#TODO: remove this hack and have a good way of handling
					#TODO: detailed vs. non-detailed pokemon names
					pokemon = hack_name(pokemon)

					self.log(f'{player}\'s {pokemon} has fainted')
					if player == self.position:
						gs_player = GameState.Player.one
					else:
						gs_player = GameState.Player.two

					self.gs.set_fainted(gs_player, pokemon)
					self.log('set_fainted called successfully')
					if not self.gs.check_fainted(gs_player, pokemon):
						self.log('ERROR: Gamestate fainted was not set as '
							f'expected for {pokemon}')

				elif inp_type == '-damage':
					if len(params) <= 3:
						player = params[0][0:2]
						pokemon = params[0].lstrip('p1a: ').lstrip('p2a: ').strip()
						pokemon = hack_name(pokemon)
						health_data = params[1]
						match = self.health_regex.search(health_data)
						if match:
							normalized_health = (float(match.group('numerator')) / 
								float(match.group('denominator')))
							self.log(f'{pokemon} has health {normalized_health}')
							if player == self.position:
								gs_player = GameState.Player.one
							else:
								gs_player = GameState.Player.two

							self.gs.set_health(gs_player, pokemon, normalized_health)
						else:
							self.log(f'Could not track health for pokemon {pokemon}')
					
					# this section to track the enemy abilities
					elif len(params) == 4:
						pokemon = params[3].strip('[of] p1a: ')
						ability = params[2].strip('[from] ability: ')
						# self.enemy_state.update_abilities(pokemon, ability)
						self.log('Pokemon: ', pokemon, 'Enemy Ability: ', self.enemy_state.team_abilities[pokemon])
				
				elif inp_type == '-heal':
					player = params[0][0:2]
					pokemon = params[0].lstrip('p1a: ').lstrip('p2a: ').strip()
					pokemon = hack_name(pokemon)
					health_data = params[1]

					match = self.health_regex.search(health_data)
					if match:
						normalized_health = (float(match.group('numerator')) / 
							float(match.group('denominator')))
						self.log(f'{pokemon} has health {normalized_health}')
						if player == self.position:
							gs_player = GameState.Player.one
						else:
							gs_player = GameState.Player.two

						self.gs.set_health(gs_player, pokemon, normalized_health)
					else:
						self.log(f'Could not track health for pokemon {pokemon}')

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
					'''
					-item|POKEMON|ITEM
					The ITEM held by the POKEMON has been changed or revealed due to a move or ability. 
					In addition, Air Balloon reveals itself when the Pokémon holding it switches in, so it will also cause this message to appear.
					'''
					position = self.get_owner(params)
					pokemon_name = self.get_pokemon(params)
					item = util.item_name_to_id(params[1])
					if position.startswith(self.position):
						self.gs.set_item(GameState.Player.one, pokemon_name, item)
					
					else:
						self.gs.set_item(GameState.Player.two, pokemon_name, item)


				elif inp_type == '-enditem':
					'''
					-enditem|POKEMON|ITEM
					The ITEM held by POKEMON has been destroyed, and it now holds no item. 
					This can be because of an item's own effects (consumed Berries, Air Balloon), or by a move or ability, like Knock Off. 
					If a berry is consumed, it also has an additional modifier |[eat] to indicate that it was consumed. 
					This message does not appear if the item's ownership was changed (with a move or ability like Thief or Trick), 
					even if the move or ability would result in a Pokémon without an item.

					Note:
						Kept for legacy and inclusiveness reasons
						Actual tracking of this hook done based on changed
						Item in 'request' inp_type
					'''
					pass


				elif inp_type == 'move':
					'''
					move|POKEMON|MOVE|TARGET
					The specified Pokémon has used move MOVE at TARGET. 
					If a move has multiple targets or no target, TARGET should be ignored. 
					If a move targets a side, TARGET will be a (possibly fainted) Pokémon on that side.
					If |[miss] is present, the move missed.
					'''
					if len(params) == 4:
						if params[3] == '[zeffect]':
							if self.get_owner(params[0]) == 'p1a':
								pokemon_name = self.get_pokemon(params[0])
								zmove_id = util.move_name_to_id(params[1])
								# Add (pokemon : zmove) in the zmove_tracker to
								# ensure, this pokemon can't re-use zmove
								self.zmoves_tracker[pokemon_name] = zmove_name
								self.gs.set_move(GameState.Player.one, pokemon_name, zmove_id, 0.0, 1.0)

				elif inp_type == '-zpower':
					'''
					|-zpower|POKEMON
					The Pokémon POKEMON has used the z-move version of its move.

					Note:
						Kept for legacy and inclusiveness reasons
						Actual tracking of zpower done in the '-move'
						hook
					'''
					pass

				elif inp_type == '-weather':
					weather_name = params[0]
					if weather_name == 'none':
						self.gs.clear_all_weather()
					else:
						self.gs.set_weather(weather_name)

				elif inp_type == '-boost':
					mine = params[0].startswith(self.position)
					if mine:
						gs_player = GameState.Player.one
					else:
						gs_player = GameState.Player.two
					boost_name = params[1]
					stages = float(params[2])
					self.gs.add_boost(gs_player, boost_name, stages)

				elif inp_type == '-unboost':
					mine = params[0].startswith(self.position)
					if mine:
						gs_player = GameState.Player.one
					else:
						gs_player = GameState.Player.two
					boost_name = params[1]
					stages = float(params[2])
					self.gs.add_boost(gs_player, boost_name, -1 * stages)

			else:
				if inp_type == 'updateuser':
					if (self.name == params[0].strip() and self.challenge and 
						not self.has_challenged):
						self.has_challenged = True
						time.sleep(1)
						await self.challenge_expected()
				elif inp_type == 'popup':
					if 'Due to high load, you are limited to 12 battles and team validations every 3 minutes.' in params[0]:
						self.log('killing')
						self.kill()
		except Exception as err:
			self.log_error(err)

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
					self.agent = DQNAgent(INPUT_SHAPE, training=False)
					self.agent.load_model(model_to_load)
			await self.accept_challenge(self.expected_opponent, self.team_text)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			self.log(f'Room ID: {room_obj.id}')
			self.active_pokemon = None
			self.opp_active_pokemon = None
			self.weather = 'none'

	def kill(self):
		sys.exit(0)


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

	if model_type == 'dqn':
		if not trainer:
			agent = DQNAgent(INPUT_SHAPE, epsilon_decay=epsilon_decay, 
				training=is_training)
			if load_model_path:
				agent.load_model(load_model_path)
		else:
			if load_model_path:
				agent = DQNAgent(INPUT_SHAPE, training=False)
				agent.load_model(load_model_path)
			else:
				agent = RandomAgent()

		BotClient(name=username, password=password, 
			expected_opponent=expected_opponent, team=team, 
			challenge=challenge, runType=runType, runTypeData=runTypeData, 
			agent=agent, print_stats=print_stats, trainer=trainer).start()
	elif model_type == 'random':
		BotClient(name=username, password=password, 
			expected_opponent=expected_opponent, team=team, 
			challenge=challenge, runType=RunType.Iterations, 
			runTypeData=iterations, agent=None, print_stats=print_stats).start()

if __name__ == '__main__':
	random.seed()
	main()