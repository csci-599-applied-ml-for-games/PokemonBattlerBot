import sys
import os
import random 
import json 
import csv
import time
from datetime import datetime
from enum import Enum, auto

import showdown 

from gamestate import GameState

BOT_DIR = os.path.dirname(__file__)
TYPE_MAP = {}

#EXLORATION SETTINGS
epsilon = 1  # not a constant, going to be decayed
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

class Model(Enum):
	Random = auto()
	DQN = auto()

class BotClient(showdown.Client):
	def __init__(self, name='', password='', loop=None, max_room_logs=5000,
		server_id='showdown', server_host=None, expected_opponent=None,
		team=None, challenge=False, iterations=1, model=Model.Random):

		if expected_opponent == None:
			raise Exception("No expected opponent found in arguments")
		else:
			self.expected_opponent = expected_opponent
		if team == None:
			raise Exception("No team found in arguments")
		else:
			self.team_text = team

		self.challenge = challenge
		self.has_challenged = False

		self.iterations_run = 0
		self.iterations = iterations 

		self.datestring = datetime.now().strftime('%y-%m-%d-%H-%M-%S')

		self.model = model
		
		super().__init__(name=name, password=password, loop=loop, 
			max_room_logs=max_room_logs, server_id=server_id, 
			server_host=server_host)

	def log(self, *args):
		l = [str(arg) for arg in args]
		string = ' '.join(l)
		logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
		if not os.path.exists(logs_dir):
			os.mkdir(logs_dir)
		log_file = f'{self.datestring}_Iteration{self.iterations_run}.txt'
		with open(os.path.join(logs_dir, log_file), 'a') as fd:
			fd.write(f'{string}\n')
	
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

	async def action(self, room_obj, data):
		moves = data.get('active')[0].get('moves')
		move_count = len(moves)
		action_count = move_count

		team_info = self.get_team_info(data)
		switch_available = []
		for pokemon_index, pokemon_info in enumerate(team_info):
			fainted = 'fnt' in pokemon_info.get('condition')
			if (not pokemon_info.get('active', False) and 
				not fainted):
				
				switch_available.append(pokemon_index + 1)

		action_count += len(switch_available)

		if self.model == Model.Random:
			action = random.randint(1, action_count)
		elif self.model == Model.DQN:
			self.log('Using DQN')
			action = random.randint(1, action_count)

		if action <= move_count:
			await room_obj.move(action) 
		else:
			switch_index = switch_available[action - (move_count + 1)]
			await room_obj.switch(switch_index)

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
					await self.action(room_obj, data)
			
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
						await self.action(room_obj, self.last_request_data)

			elif inp_type == 'win':
				winner = params[0]
				if winner == self.name:
					self.log("We won")
				else:
					self.log("We lost")
				await room_obj.leave()
				self.iterations_run += 1
				
				if self.iterations_run < self.iterations:
					self.log("Starting iteration {}".format(self.iterations_run))
					if self.challenge:
						time.sleep(5)
						await self.challenge_expected()
				else:
					sys.exit(0)

			elif inp_type == '-ability':
				# might work to track some abilities but so far weather abilities and other abilities
				# are only made known when a specific game action is made.
				self.log('ability')
				#self.log(params)
			
			elif inp_type == '-damage':
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
	if len(sys.argv) != 5 and len(sys.argv) != 6:
		print('Usage: python bot.py <iterations> <username> <password> <expected_opponent> '
			'[--challenge]')
		return 

	iterations = int(sys.argv[1])
	username = sys.argv[2]
	password = sys.argv[3]
	expected_opponent = sys.argv[4]
	challenge = len(sys.argv) == 6

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


	BotClient(name=username, password=password, 
		expected_opponent=expected_opponent, team=team, 
		challenge=challenge, iterations=iterations, model=Model.DQN).start()

if __name__ == '__main__':
	random.seed()
	main()