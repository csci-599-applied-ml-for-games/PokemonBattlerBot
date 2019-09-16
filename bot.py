import sys
import os

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
		"""
		|coro|

		Hook for subclasses. Called when the client receives any data from the
		server.
	
		Args:
			room_id (:obj:`str`) : ID of the room with which the information is 
				associated with. Messages with unspecified IDs default to '
				lobby', though may not necessarily be associated with 'lobby'.
			inp_type (:obj:`str`) : The type of information received.
				Ex: 'l' (user leave), 'j' (user join), 'c:' (chat message)
			params (:obj:`list`) : List of the parameters associated with the 
				inp_type. Ex: a user leave has params of ['zarel'], where 'zarel'
				represents the user id of the user that left.

		Notes:
			Does nothing by default.
		"""
		pass

	async def on_private_message(self, pm):
		if pm.recipient == self:
			await pm.reply(pm.content)

	async def on_challenge_update(self, challenge_data):
		incoming = challenge_data.get('challengesFrom', {})
		if self.expected_opponent.lower() in incoming:
			await self.accept_challenge(self.expected_opponent, self.team)

	async def on_room_init(self, room_obj):
		if room_obj.id.startswith('battle-'):
			await room_obj.start_poke(1)

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
	main()