'''
This class holds the game state
'''

from enum import IntEnum, auto

INDEX_TRACKER = 0
def increment_index():
	global INDEX_TRACKER
	INDEX_TRACKER += 1
	return INDEX_TRACKER

def attribute_dict_setup(attribute_dict):
	reversed_dict = {v: k for k, v in attribute_dict.items()}
	our_min = min([v for k, v in attribute_dict.items()])
	attribute_dict['Count'] = len(attribute_dict)
	attribute_dict['Min'] = our_min
	return attribute_dict, reversed_dict 

POKEMON_NAME_TO_INDEX = {
	'Pelipper': INDEX_TRACKER,
	'Greninja': increment_index(), 
	'Swampert': increment_index(),
	'Manaphy': increment_index(),
	'Ferrothorn': increment_index(),
	'Tornadus': increment_index(),
	'Tornadus-Therian': increment_index(), 
	'NotFound': increment_index(), 
}
_, INDEX_TO_POKEMON_NAME = attribute_dict_setup(POKEMON_NAME_TO_INDEX)

MOVE_NAME_TO_INDEX = {
	'Knock Off': increment_index(),
	'U-turn': increment_index(),
	'Scald': increment_index(),
	'Roost': increment_index(),
	'Hydro Pump': increment_index(),  
	'Dark Pulse': increment_index(),
	'Water Shuriken': increment_index(),
	'Spikes': increment_index(),
	'Waterfall': increment_index(),
	'Earthquake': increment_index(),
	'Ice Punch': increment_index(),
	'Superpower': increment_index(),
	'Tail Glow': increment_index(),
	'Surf': increment_index(),
	'Ice Beam': increment_index(),
	'Rest': increment_index(), 
	'Stealth Rock': increment_index(),
	'Toxic': increment_index(),
	'Power Whip': increment_index(),
	'Hurricane': increment_index(),
	'Defog': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_MOVE_NAME = attribute_dict_setup(MOVE_NAME_TO_INDEX)

TYPE_NAME_TO_INDEX = {
	'Normal': increment_index(),
	'Fire': increment_index(),
	'Water': increment_index(),
	'Grass': increment_index(),
	'Electric': increment_index(),
	'Ice': increment_index(),
	'Fighting': increment_index(),
	'Poison': increment_index(),
	'Ground': increment_index(),
	'Flying': increment_index(),
	'Psychic': increment_index(),
	'Bug': increment_index(),
	'Ghost': increment_index(),
	'Dark': increment_index(),
	'Dragon': increment_index(),
	'Steel': increment_index(),
	'Fairy': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_TYPE_NAME = attribute_dict_setup(TYPE_NAME_TO_INDEX)

ACTIVE_STATE = increment_index()

FAINTED_STATE = increment_index()

ATTRIBUTES_PER_POKEMON = INDEX_TRACKER + 1

class GameState():
	class Player(IntEnum):
		'''
		player one corresponds to local player, not necessarily P1 as determined 
		by the client
		'''
		one = 0 
		two = auto()
		count = auto()

	max_team_size = 6

	num_player_elements = max_team_size * ATTRIBUTES_PER_POKEMON

	def __init__(self):
		self.vector_list = [0.0 for _ in range(GameState.Player.count * 
			GameState.num_player_elements)]

		#NOTE: for easy access to pokemon team position in the future
		self.name_to_position = [{}, {}] 
		self.team_abilities = [{}, {}] #TODO: remove and pack in vector_list
		self.team_mega = [{}, {}]

	@staticmethod
	def pokemon_name_clean(pokemon_name):
		return pokemon_name.rstrip(', M').rstrip(', F')

	def set_team(self, player, team):
		'''
		player: member of Player enum
		team: list of pokemon names as strings. 
			If updating for some reason, don't change the order in which you 
			pass in the pokemon
		'''
		for team_position, pokemon_name in enumerate(team):
			pokemon_name = GameState.pokemon_name_clean(pokemon_name)
			
			self.name_to_position[player][pokemon_name] = team_position

			pokemon_index = POKEMON_NAME_TO_INDEX.get(pokemon_name, 
				POKEMON_NAME_TO_INDEX['NotFound'])
			self.vector_list[player * GameState.num_player_elements +
				team_position * ATTRIBUTES_PER_POKEMON + pokemon_index] = 1.0

	def check_team_position(self, player, position):
		'''
		Returns a string of the pokemon that's in the position passed in. 
		Probably only useful for debugging

		player: member of Player enum
		position: the position that the pokemon takes on the team. zero-indexed
		'''
		start_checking = (player * GameState.num_player_elements + 
			position * ATTRIBUTES_PER_POKEMON)
		end_checking = start_checking + POKEMON_NAME_TO_INDEX['Count']
		for pokemon_index in range(start_checking, end_checking):
			if self.vector_list[pokemon_index] == 1.0:
				return INDEX_TO_POKEMON_NAME[pokemon_index - start_checking]
		else:
			raise Exception('We somehow couldn\'t find the pokemon')

	def _set_active(self, player, position, value):
		'''
		Sets a pokemon in a position to a value 
		(0.0 for inactive and 1.0 for active)  
		Probably only useful for debugging

		player: member of Player enum
		position: the position that the pokemon takes on the team. zero-indexed
		value: float for value
		'''
		self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + ACTIVE_STATE] = value

	def set_active(self, player, name):
		'''
		Sets a pokemon with a name a position to a value 
		(0.0 for inactive and 1.0 for active)  
		Probably only useful for debugging

		player: member of Player enum
		name: string for the name of the pokemon
		'''
		name = GameState.pokemon_name_clean(name)
		for team_position in range(GameState.max_team_size):
			self._set_active(player, team_position, 0.0)

		team_position = self.name_to_position[player][name]
		self._set_active(player, team_position, 1.0)

	def check_active(self, player, name):
		'''
		Returns a boolean for whether the pokemon is active

		player: member of Player enum
		name: string for the name of the pokemon
		'''
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return (self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + ACTIVE_STATE] == 1.0)

	def _set_fainted(self, player, position, value):
		self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + FAINTED_STATE] = value

	def set_fainted(self, player, name):
		team_position = self.name_to_position[player][name]
		self._set_fainted(player, team_position, 1.0)

	def check_fainted(self, player, name):
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return (self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + FAINTED_STATE] == 1.0)

	def _set_move(self, player, position, move_position, value):
		self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + move_position] = value

	def set_move(self, player, name, move_name):
		team_position = self.name_to_position[player][name]
		move_position = MOVE_NAME_TO_INDEX.get(move_name, MOVE_NAME_TO_INDEX['NotFound'])
		self._set_move(player, team_position, move_position, 1.0)

	def check_moves(self, player, name):
		name = GameState.pokemon_name_clean(name)
		moves = []
		position = self.name_to_position[player][name]
		start_checking = (player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + MOVE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + MOVE_NAME_TO_INDEX['Count']
		
		start_of_move_indices = (player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON)
		for move_index in range(start_checking, end_checking):
			if self.vector_list[move_index] == 1.0:
				moves.append(INDEX_TO_MOVE_NAME[move_index - 
					start_of_move_indices])
		return moves

	def _set_type(self, player, position, type_position, value):
		self.vector_list[player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + type_position] = value

	def set_type(self, player, name, type_name):
		team_position = self.name_to_position[player][name]
		type_position = TYPE_NAME_TO_INDEX.get(type_name, TYPE_NAME_TO_INDEX['NotFound'])
		self._set_type(player, team_position, type_position, 1.0)

	def check_types(self, player, name):
		name = GameState.pokemon_name_clean(name)
		types = []
		position = self.name_to_position[player][name]
		start_checking = (player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON + TYPE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + TYPE_NAME_TO_INDEX['Count']
		
		start_of_type_indices = (player * GameState.num_player_elements +
			position * ATTRIBUTES_PER_POKEMON)
		
		for type_index in range(start_checking, end_checking):
			if self.vector_list[type_index] == 1.0:
				types.append(INDEX_TO_TYPE_NAME[type_index - 
					start_of_type_indices])
		return types

	def update_abilities(self, player, pokemon, ability):
		#TODO: replace implementation with packing into vector list
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_abilities[player][pokemon_name] = ability

	def update_team_mega(self, player, pokemon):
		# TODO: replace implementation with packing into vector list
		# TODO: Megas go inactive once the pokemon faints... add code to switch if pokemon faints
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_mega[player][pokemon_name] = True
		
	def update_used_zpower(self, pokemon):
		# TODO: replace implementation with packing into vector list
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_zpower[player][pokemon_name] = True

	#set weather state

	#set status


if __name__ == '__main__':
	#NOTE: tests for GameState data
	gs = GameState()
	team1 = ['Pelipper', 'Greninja', 'Swampert', 'Manaphy', 'Tornadus', 
			'Ferrothorn']
	gs.set_team(GameState.Player.one, team1)
	for position, expected_name in enumerate(team1):
		name = gs.check_team_position(GameState.Player.one, position)
		if name != expected_name:
			print(f'Incorrect pokemon {name} at position {position}. '
				f'Expected: {expected_name}')

	team2 = ['Pelipper', 'Greninja', 'Swampert', 'Manaphy', 'Ferrothorn',
			'Tornadus']
	gs.set_team(GameState.Player.two, team2)
	for position, expected_name in enumerate(team2):
		name = gs.check_team_position(GameState.Player.two, position)
		if name != expected_name:
			print(f'Incorrect pokemon {name} at position {position}. '
				f'Expected: {expected_name}')

	for expected_name in team1: 
		gs.set_active(GameState.Player.one, expected_name)
		for name in team1:
			result = gs.check_active(GameState.Player.one, name)
			if result:
				if name != expected_name:
					print(f'{GameState.Player.one}: '
						f'Pokemon {name} was unexpectedly active.')
			else:
				if name == expected_name:
					print(f'{GameState.Player.one}: ' 
						f'Pokemon {name} was unexpectedly inactive')

	for expected_name in team2: 
		gs.set_active(GameState.Player.two, expected_name)
		for name in team2:
			result = gs.check_active(GameState.Player.two, name)
			if result:
				if name != expected_name:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly active.')
			else:
				if name == expected_name:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly inactive')


	for expected_index, expected_name in enumerate(team1): 
		gs.set_fainted(GameState.Player.one, expected_name)
		for name_index, name in enumerate(team1):
			result = gs.check_fainted(GameState.Player.one, name)
			if result:
				if name_index > expected_index:
					print(f'{GameState.Player.one}: '
						f'Pokemon {name} was unexpectedly fainted.')
			else:
				if name_index <= expected_index:
					print(f'{GameState.Player.one}: ' 
						f'Pokemon {name} was unexpectedly alive')

	for expected_index, expected_name in enumerate(team2): 
		gs.set_fainted(GameState.Player.two, expected_name)
		for name_index, name in enumerate(team2):
			result = gs.check_fainted(GameState.Player.two, name)
			if result:
				if name_index > expected_index:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly fainted.')
			else:
				if name_index <= expected_index:
					print(f'{GameState.Player.two}: ' 
						f'Pokemon {name} was unexpectedly alive')

	def check_moves(player, pokemon, move_names):
		has_moves = gs.check_moves(player, pokemon)
		if set(has_moves) != set(move_names):
			print(f'{pokemon} has moves {has_moves} instead of {move_names}')

	def test_moves(player, pokemon, move_names):
		for move_name in move_names:
			gs.set_move(player, pokemon, move_name)
		check_moves(player, pokemon, move_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
			
		pokemon_moves = [
			('Pelipper', ['Knock Off', 'U-turn', 'Scald', 'Roost']),
			('Greninja', ['Hydro Pump', 'Dark Pulse', 'Water Shuriken', 'Spikes']),
			('Swampert', ['Waterfall', 'Earthquake', 'Ice Punch', 'Superpower']),
			('Manaphy', ['Tail Glow', 'Surf', 'Ice Beam', 'Rest']),
			('Ferrothorn', ['Stealth Rock', 'Knock Off', 'Toxic', 'Power Whip']),
			('Tornadus', ['Hurricane', 'Knock Off', 'U-turn', 'Defog'])
		]
		for pokemon, move_names in pokemon_moves:
			test_moves(player, pokemon, move_names)
		for pokemon, move_names in pokemon_moves:
			check_moves(player, pokemon, move_names)

	def check_types(player, pokemon, type_names):
		has_types = gs.check_types(player, pokemon)
		if set(has_types) != set(type_names):
			print(f'{pokemon} has types {has_types} instead of {type_names}')

	def test_types(player, pokemon, type_names):
		for type_name in type_names:
			gs.set_type(player, pokemon, type_name)
		check_types(player, pokemon, type_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
		pokemon_types = [
			('Pelipper', ['Water', 'Flying']),
			('Greninja', ['Water', 'Dark']),
			('Swampert', ['Water', 'Ground']),
			('Manaphy', ['Water']),
			('Ferrothorn', ['Grass', 'Steel']),
			('Tornadus', ['Flying'])
		]
		for pokemon, type_names in pokemon_types:
			test_types(player, pokemon, type_names)
		for pokemon, type_names in pokemon_types:
			check_types(player, pokemon, type_names)