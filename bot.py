import sys
import os
import random 
import json 
import csv

import showdown 

BOT_DIR = os.path.dirname(__file__)
TYPE_MAP = {}

class BotClient(showdown.Client):
	def __init__(self, name='', password='', loop=None, max_room_logs=5000,
		server_id='showdown', server_host=None, expected_opponent=None,
		team=None, challenge=False):

		if expected_opponent == None:
			raise Exception("No expected opponent found in arguments")
		else:
			self.expected_opponent = expected_opponent
		if team == None:
			raise Exception("No team found in arguments")
		else:
			self.team = team

		self.challenge = challenge
		self.has_challenged = False

		super().__init__(name=name, password=password, loop=loop, 
			max_room_logs=max_room_logs, server_id=server_id, 
			server_host=server_host)
	
	@staticmethod
	def get_team_info(data):
		return data['side']['pokemon']

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

		action = random.randint(1, action_count)
		if action <= move_count:
			await room_obj.move(action) 
		else:
			switch_index = switch_available[action - (move_count + 1)]
			await room_obj.switch(switch_index)

	def own_pokemon(self, pokemon_data):
		return pokemon_data.startswith(self.position)

	@staticmethod
	def get_pokemon(pokemon_data):
		return pokemon_data.split(':')[1].strip()

	def add_status(self, statuses, pokemon_name, status):
		pokemon_statuses = statuses.get(pokemon_name, [])
		pokemon_statuses.append(status)
		statuses[pokemon_name] = pokemon_statuses
		
		print('Self Status', self.statuses)
		print('Opp Status', self.opp_statuses)

	def remove_status(self, statuses, pokemon_name, status):
		pokemon_statuses = statuses.get(pokemon_name, [])
		try:
			pokemon_statuses.remove(status)
		except ValueError:
			pass
		statuses[pokemon_name] = pokemon_statuses

		print('Self Status', self.statuses)
		print('Opp Status', self.opp_statuses)

	async def on_receive(self, room_id, inp_type, params):
		if self.challenge and not self.has_challenged:
			#NOTE: Sorry for this hack...wasn't sure how best to approach this
			self.has_challenged = True
			await self.cancel_challenge()
			await self.send_challenge(self.expected_opponent, self.team, 
				'gen7ou')

		print(inp_type)
		print(params)

		room_obj = self.rooms[room_id]	
		if room_obj.id.startswith('battle-'):
			if inp_type == 'poke':
				owner = params[0]
				pokename = params[1]
				if owner == self.position:
					self.team.append(pokename)
				else:
					self.opp_team.append(pokename)

				if (len(self.team) == self.teamsize and
					len(self.opp_team) == self.opp_teamsize):

					print(f'Team: {self.team}')
					print(f'Opp team: {self.opp_team}')
					
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
					print('info', pokemon_info)
					# get the ability for each pokemon
					self.team_abilities[str(pokemon_info['details'].rstrip(', M').rstrip(', F'))] = pokemon_info['ability']
					# track the items each pokemon
					self.team_items[str(pokemon_info['details'].rstrip(', M').rstrip(', F'))] = pokemon_info['item']
					# track the team movelist?
					self.team_moves[str(pokemon_info['details'].rstrip(', M').rstrip(', F'))] = pokemon_info['moves']
					# if pokemon_info.get('active'):
						# self.active_pokemon = pokemon_info['details'].rstrip(', M').rstrip(', F')
						# print('active_pokemon', self.active_pokemon)
						# print('active_pokemon types', TYPE_MAP.get(self.active_pokemon))
						#break // removed this line so it would get all the moves and stuff and things ya know
				print('team abilities', self.team_abilities)
				print('team items', self.team_items)
				print('team moves', self.team_moves)	
				force_switch = data.get('forceSwitch', [False])[0]
				if force_switch == True: #TODO: can this request arrive when opponent's pokemon faints?
					switch_available = []
					for pokemon_index, pokemon_info in enumerate(team_info):
						if 'fnt' not in pokemon_info['condition']:
							switch_available.append(pokemon_index + 1)
					switch_index = random.choice(switch_available)
					await room_obj.switch(switch_index)
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
				pokemon_data = params[0]

				volatile_statuses = ['confusion', 'curse']
				if self.own_pokemon(pokemon_data):
					pokemon_name = self.active_pokemon
					statuses = self.statuses
				else:
					pokemon_name = self.opp_active_pokemon
					statuses = self.opp_statuses
				for volatile_status in volatile_statuses:
					self.remove_status(statuses, pokemon_name, volatile_status)

				if not self.own_pokemon(pokemon_data):
					self.opp_active_pokemon = self.get_pokemon(pokemon_data)
					print('Opp active', self.opp_active_pokemon)
				else:
					self.active_pokemon = self.get_pokemon(pokemon_data)
					print('active_pokemon', self.active_pokemon)
					print('active_pokemon types', TYPE_MAP.get(self.active_pokemon))

			elif inp_type == 'weather':
				self.weather = params[0]
				print('New weather: {}'.format(self.weather))

			elif inp_type == '-sidestart':
				position = params[0].split(':')[0]
				hazard = params[1].lstrip('move: ')
				if position.startswith(self.position):
					self.sidestart.append(hazard)
				else:
					self.opp_sidestart.append(hazard)

				print('Self sidestart', self.sidestart)
				print('Opp sidestart', self.opp_sidestart)

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

				print('Self sidestart', self.sidestart)
				print('Opp sidestart', self.opp_sidestart)

			elif inp_type == 'error':
				if params[0].startswith('[Invalid choice]'):
					await self.action(room_obj, self.last_request_data)

			elif inp_type == 'win':
				winner = params[0]
				if winner == self.name:
					print("We won")
				else:
					print("We lost")
				sys.exit(0)

	async def on_challenge_update(self, challenge_data):
		incoming = challenge_data.get('challengesFrom', {})
		if self.expected_opponent.lower() in incoming:
			await self.accept_challenge(self.expected_opponent, self.team)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			self.active_pokemon = None
			self.statuses = {}
			self.sidestart = []

			self.opp_active_pokemon = None
			self.opp_statuses = {}
			self.opp_sidestart = []

			self.weather = 'none'

def main():
	if len(sys.argv) != 4 and len(sys.argv) != 5:
		print('Usage: python bot.py <username> <password> <expected_opponent> '
			'[--challenge]')
		return 

	username = sys.argv[1]
	password = sys.argv[2]
	expected_opponent = sys.argv[3]
	challenge = len(sys.argv) == 5

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
		challenge=challenge).start()

if __name__ == '__main__':
	random.seed()
	main()