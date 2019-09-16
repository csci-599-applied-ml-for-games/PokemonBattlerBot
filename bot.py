import sys
import os
import random 

import showdown 

TEAMS_DIR = os.path.dirname(__file__)

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

	async def on_receive(self, room_id, inp_type, params):
		if inp_type == 'poke':
			owner = params[0]
			pokename = params[1]
			if owner == self.position:
				self.team.append(pokename)
			else:
				self.opp_team.append(pokename)

			if (len(self.team) == self.teamsize and
				len(self.opp_team) == self.opp_teamsize):
				
				#NOTE: Select starting pokemon here 
				room_obj = self.rooms[room_id]
				await room_obj.start_poke(random.randint(1, self.teamsize))
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

	async def on_private_message(self, pm):
		if pm.recipient == self:
			await pm.reply(pm.content)

	async def on_challenge_update(self, challenge_data):
		incoming = challenge_data.get('challengesFrom', {})
		if self.expected_opponent.lower() in incoming:
			await self.accept_challenge(self.expected_opponent, self.team)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			pass

def main():
	if len(sys.argv) != 4:
		print('Usage: python bot.py <username> <password> <expected_opponent>')
		return 

	username = sys.argv[1]
	password = sys.argv[2]
	expected_opponent = sys.argv[3]

	with open(os.path.join(TEAMS_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()

	BotClient(name=username, password=password, 
		expected_opponent=expected_opponent, team=team).start()

if __name__ == '__main__':
	random.seed()
	main()