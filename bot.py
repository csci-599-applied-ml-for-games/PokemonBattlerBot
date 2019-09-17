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
		team=None):

		if expected_opponent == None:
			raise Exception("No expected opponent found in arguments")
		else:
			self.expected_opponent = expected_opponent
		if team == None:
			raise Exception("No team found in arguments")
		else:
			self.team = team

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

	async def on_receive(self, room_id, inp_type, params):
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
				for pokemon_info in team_info:
					if pokemon_info.get('active'):
						self.active_pokemon = pokemon_info['details'].rstrip(', M').rstrip(', F')
						print('active_pokemon', self.active_pokemon)
						print('active_pokemon types', TYPE_MAP.get(self.active_pokemon))
						break 
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
			elif inp_type == 'error':
				if params[0].startswith('[Invalid choice]'):
					await self.action(room_obj, self.last_request_data)

	async def on_private_message(self, pm):
		if pm.recipient == self:
			await pm.reply(pm.content)

	async def on_challenge_update(self, challenge_data):
		incoming = challenge_data.get('challengesFrom', {})
		if self.expected_opponent.lower() in incoming:
			await self.accept_challenge(self.expected_opponent, self.team)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			self.active_pokemon = None

def main():
	if len(sys.argv) != 4:
		print('Usage: python bot.py <username> <password> <expected_opponent>')
		return 

	username = sys.argv[1]
	password = sys.argv[2]
	expected_opponent = sys.argv[3]

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
		expected_opponent=expected_opponent, team=team).start()

if __name__ == '__main__':
	random.seed()
	main()