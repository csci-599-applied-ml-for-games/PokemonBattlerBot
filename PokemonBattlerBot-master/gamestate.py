'''
This class holds the game state
'''

from enum import IntEnum, auto

INDEX_TRACKER = 0
def increment_index():
	global INDEX_TRACKER
	INDEX_TRACKER += 1
	return INDEX_TRACKER

SHARED_INDEX_TRACKER = 0
def increment_shared_index():
	global SHARED_INDEX_TRACKER
	SHARED_INDEX_TRACKER += 1
	return SHARED_INDEX_TRACKER

TEAM_INDEX_TRACKER = 0
def increment_team_index():
	global TEAM_INDEX_TRACKER
	TEAM_INDEX_TRACKER += 1
	return TEAM_INDEX_TRACKER


def attribute_dict_setup(attribute_dict):
	reversed_dict = {v: k for k, v in attribute_dict.items()}
	our_min = min([v for k, v in attribute_dict.items()])
	attribute_dict['Count'] = len(attribute_dict)
	attribute_dict['Min'] = our_min
	return attribute_dict, reversed_dict 

WEATHER_NAME_TO_INDEX = {
	'RainDance': SHARED_INDEX_TRACKER,
	'PrimordialSea': increment_shared_index(),
	'SunnyDay': increment_shared_index(),
	'DesolateLand': increment_shared_index(),
	'Sandstorm': increment_shared_index(),
	'Hail': increment_shared_index(),
	'DeltaStream': increment_shared_index(),
	'NotFound': increment_shared_index()
}
_, INDEX_TO_WEATHER_NAME = attribute_dict_setup(WEATHER_NAME_TO_INDEX)

SHARED_ATTRIBUTES_COUNT = SHARED_INDEX_TRACKER + 1

MAX_BOOST = 12.0
MIN_BOOST = 0.0
ACTIVE_POKEMON_BOOST = {
	'atk': TEAM_INDEX_TRACKER,
	'def': increment_team_index(),
	'spa': increment_team_index(),
	'spd': increment_team_index(),
	'spe': increment_team_index(),
	'accuracy': increment_team_index(),
	'evasion': increment_team_index(), 
	'NotFound': increment_team_index()
}

# Magic number to normalize the quantity of an entry hazard for 
# input vactor. For eg. 3 spikes => 3/10 = 0.3 value in vector
MAX_ENTRY_HAZARD_COUNT = 10
ENTRY_HAZARD_TO_INDEX = {
	'Spikes': increment_team_index(),
	'Stealth Rock': increment_team_index(),
	'Toxic Spikes': increment_team_index(),
	'Sticky Web': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, INDEX_TO_ENTRY_HAZARD = attribute_dict_setup(ENTRY_HAZARD_TO_INDEX)

TEAM_ATTRIBUTES_COUNT = TEAM_INDEX_TRACKER + 1

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

STATUS_NAME_TO_INDEX = {
	'brn': increment_index(),
	'par': increment_index(),
	'slp': increment_index(),
	'frz': increment_index(),
	'psn': increment_index(),
	'tox': increment_index(),
	'confusion': increment_index(),
	'flinch': increment_index(),
	'trapped': increment_index(),
	'trapper': increment_index(),
	'partiallytrapped': increment_index(),
	'lockedmove': increment_index(),
	'twoturnmove': increment_index(),
	'choicelock': increment_index(),
	'mustrecharge': increment_index(),
	'futuremove': increment_index(),
	'healreplacement': increment_index(),
	'stall': increment_index(),
	'gem': increment_index(),
	'raindance': increment_index(),
	'primordialsea': increment_index(),
	'sunnyday': increment_index(),
	'desolateland': increment_index(),
	'sandstorm': increment_index(),
	'hail': increment_index(),
	'deltastream': increment_index(),
	'arceus': increment_index(),
	'silvally': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_STATUS_NAME = attribute_dict_setup(STATUS_NAME_TO_INDEX)

ACTIVE_STATE = increment_index()

FAINTED_STATE = increment_index()

NORMALIZED_HEALTH = increment_index()

ATTRIBUTES_PER_POKEMON = INDEX_TRACKER + 1

def start_of_pokemon(player, team_position):
	return (SHARED_ATTRIBUTES_COUNT + 
		player * GameState.num_player_elements + 
		TEAM_ATTRIBUTES_COUNT +
		team_position * ATTRIBUTES_PER_POKEMON)

def health_sum(vector_list, player):
	total = 0
	for position in range(GameState.max_team_size):
		total += vector_list[start_of_pokemon(player, position) + 
			NORMALIZED_HEALTH]
	return total

def ko_count(vector_list, player):
	total = 0
	for position in range(GameState.max_team_size):
		total += vector_list[start_of_pokemon(player, position) + FAINTED_STATE]
	return total

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

	num_player_elements = (TEAM_ATTRIBUTES_COUNT + 
		max_team_size * ATTRIBUTES_PER_POKEMON)

	@staticmethod
	def vector_dimension():
		return (SHARED_ATTRIBUTES_COUNT + 
			GameState.Player.count * GameState.num_player_elements)

	def __init__(self):
		self.vector_list = [0.0 for _ in range(GameState.vector_dimension())]

		#NOTE: for easy access to pokemon team position in the future
		self.name_to_position = [{}, {}] 
		self.team_abilities = [{}, {}] #TODO: remove and pack in vector_list
		self.team_mega = [{}, {}]

	def _set_weather(self, weather_name, value):
		position = WEATHER_NAME_TO_INDEX.get(weather_name, 
			WEATHER_NAME_TO_INDEX['NotFound'])
		self.vector_list[position] = value

	def set_player_attribute(self, player, attribute_index, value):
		self.vector_list[SHARED_ATTRIBUTES_COUNT + 
			player * GameState.num_player_elements + 
			attribute_index] = value

	def get_player_attribute(self, player, attribute_index):
		return self.vector_list[SHARED_ATTRIBUTES_COUNT + 
			player * GameState.num_player_elements + 
			attribute_index]

	def set_pokemon_attribute(self, player, team_position, attribute_index, 
		value):
		
		self.vector_list[start_of_pokemon(player, team_position) + 
			attribute_index] = value

	def get_pokemon_attribute(self, player, team_position, attribute_index):
		return self.vector_list[start_of_pokemon(player, team_position) 
			+ attribute_index]

	def set_weather(self, weather_name):
		self.clear_all_weather()
		self._set_weather(weather_name, 1.0)

	def clear_all_weather(self):
		for weather_name in WEATHER_NAME_TO_INDEX:
			self._set_weather(weather_name, 0.0)

	def clear_weather(self, weather_name):
		self.vector_list[WEATHER_NAME_TO_INDEX[weather_name]] = 0.0

	def check_weather(self, weather_name):
		return self.vector_list[WEATHER_NAME_TO_INDEX[weather_name]] == 1.0

	def all_weather(self):
		weathers = []
		for weather_name in WEATHER_NAME_TO_INDEX:
			if weather_name == 'Min' or weather_name == 'Count':
				continue
			if self.check_weather(weather_name):
				weathers.append(weather_name)
		return weathers

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
			self.set_pokemon_attribute(player, team_position, pokemon_index, 
				1.0)

	def _set_health(self, player, position, value):
		self.set_pokemon_attribute(player, position, NORMALIZED_HEALTH, value)

	def set_health(self, player, name, value):
		position = self.name_to_position[player][name]
		self._set_health(player, position, value)

	def init_health(self, player):
		for team_position in range(len(self.name_to_position[player])):
			self._set_health(player, team_position, 1.0)

	def check_health(self, player, name):
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return self.get_pokemon_attribute(player, position, NORMALIZED_HEALTH)

	def all_health(self, player):
		health_list = []
		team = self.name_to_position[player]
		for name in team:
			health_list.append((name, self.check_health(player, name)))
		return health_list 

	def check_team_position(self, player, position):
		'''
		Returns a string of the pokemon that's in the position passed in. 
		Probably only useful for debugging

		player: member of Player enum
		position: the position that the pokemon takes on the team. zero-indexed
		'''
		start_checking = start_of_pokemon(player, position) 
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
		self.set_pokemon_attribute(player, position, ACTIVE_STATE, value)

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
		return self.get_pokemon_attribute(player, position, ACTIVE_STATE)

	def all_active(self, player):
		active_pokemon = []
		team = self.name_to_position[player]
		for name in team:
			if self.check_active(player, name):
				active_pokemon.append(name)
		return active_pokemon

	def _set_fainted(self, player, position, value):
		self.set_pokemon_attribute(player, position, FAINTED_STATE, value)

	def set_fainted(self, player, name):
		team_position = self.name_to_position[player][name]
		self._set_active(player, team_position, 0.0)
		self._set_health(player, team_position, 0.0)
		self._set_fainted(player, team_position, 1.0)

	def check_fainted(self, player, name):
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return self.get_pokemon_attribute(player, position, FAINTED_STATE) == 1.0
	
	def all_fainted(self, player):
		'''
		Returns all of the fainted pokemon for player as a list of strings
		'''
		fainted = []
		team = self.name_to_position[player]
		for name in team:
			if self.check_fainted(player, name):
				fainted.append(name)
		return fainted

	def _set_move(self, player, position, move_position, value):
		self.set_pokemon_attribute(player, position, move_position, value)

	def set_move(self, player, name, move_name):
		team_position = self.name_to_position[player][name]
		move_position = MOVE_NAME_TO_INDEX.get(move_name, MOVE_NAME_TO_INDEX['NotFound'])
		self._set_move(player, team_position, move_position, 1.0)

	def check_moves(self, player, name):
		name = GameState.pokemon_name_clean(name)
		moves = []
		position = self.name_to_position[player][name]
		start_checking = (start_of_pokemon(player, position) + 
			MOVE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + MOVE_NAME_TO_INDEX['Count']

		start_of_move_indices = start_of_pokemon(player, position)
		for move_index in range(start_checking, end_checking):
			if self.vector_list[move_index] == 1.0:
				moves.append(INDEX_TO_MOVE_NAME[move_index - 
					start_of_move_indices])
		return moves

	def _set_type(self, player, position, type_position, value):
		self.set_pokemon_attribute(player, position, type_position, value)

	def set_type(self, player, name, type_name):
		team_position = self.name_to_position[player][name]
		type_position = TYPE_NAME_TO_INDEX.get(type_name, TYPE_NAME_TO_INDEX['NotFound'])
		self._set_type(player, team_position, type_position, 1.0)

	def set_types(self, player, name, type_names):
		for type_name in type_names:
			self.set_type(player, name, type_name)
			
	def check_types(self, player, name):
		name = GameState.pokemon_name_clean(name)
		types = []
		position = self.name_to_position[player][name]
		start_checking = (start_of_pokemon(player, position) + 
			TYPE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + TYPE_NAME_TO_INDEX['Count']
		
		start_of_type_indices = start_of_pokemon(player, position)
		
		for type_index in range(start_checking, end_checking):
			if self.vector_list[type_index] == 1.0:
				types.append(INDEX_TO_TYPE_NAME[type_index - 
					start_of_type_indices])
		return types
	
	def _set_status(self, player, team_position, status_position, value):
		self.set_pokemon_attribute(player, team_position, status_position, value)

	def set_status(self, player, name, status_name):
		team_position = self.name_to_position[player][name]
		type_position = STATUS_NAME_TO_INDEX.get(status_name, STATUS_NAME_TO_INDEX['NotFound'])
		self._set_status(player, team_position, type_position, 1.0)
	
	def remove_status(self, player, name, status_name):
		team_position = self.name_to_position[player][name]
		type_position = STATUS_NAME_TO_INDEX.get(status_name, STATUS_NAME_TO_INDEX['NotFound'])
		self._set_status(player, team_position, type_position, 0.0)

	def check_status(self, player, name):
		name = GameState.pokemon_name_clean(name)
		statuses = []
		position = self.name_to_position[player][name]
		start_checking = (start_of_pokemon(player, position) + 
			STATUS_NAME_TO_INDEX['Min'])
		end_checking = start_checking + STATUS_NAME_TO_INDEX['Count']
		
		start_of_status_indices = start_of_pokemon(player, position)
		
		for status_index in range(start_checking, end_checking):
			if self.vector_list[status_index] == 1.0:
				statuses.append(INDEX_TO_STATUS_NAME[status_index - 
					start_of_status_indices])
		return statuses

	def all_statuses(self, player):
		statuses = []
		team = self.name_to_position[player]
		for name in team:
			statuses.append((name, self.check_status(player, name)))
		return statuses

	def reset_boosts(self, player):
		for boost_name in ACTIVE_POKEMON_BOOST:
			self.set_boost(player, boost_name, 0.5)

	def _set_boost(self, player, boost_position, value):
		self.set_player_attribute(player, boost_position, value)

	def set_boost(self, player, boost_name, value):
		boost_position = ACTIVE_POKEMON_BOOST[boost_name]
		if value < 0.0:
			value = 0.0
		elif value > 1.0:
			value = 1.0
		self._set_boost(player, boost_position, value)

	def get_boost(self, player, boost_name):
		boost_position = ACTIVE_POKEMON_BOOST[boost_name]
		return self.get_player_attribute(player, boost_position)

	def add_boost(self, player, boost_name, delta):
		normalized_delta = delta / MAX_BOOST
		current_boost = self.get_boost(player, boost_name)
		self.set_boost(player, boost_name, normalized_delta + current_boost)

	def all_boosts(self, player):
		boosts = []
		for boost_name in ACTIVE_POKEMON_BOOST:
			boosts.append((boost_name, self.get_boost(player, boost_name)))
		return boosts

	def _set_entry_hazard(self, player, entry_hazard_position, value):
		self.set_player_attribute(player, entry_hazard_position, value)

	def set_entry_hazard(self, player, entry_hazard, value):
		entry_hazard_position = ENTRY_HAZARD_TO_INDEX.get(entry_hazard, ENTRY_HAZARD_TO_INDEX['NotFound'])
		self._set_entry_hazard(player, entry_hazard_position, value)
	
	def get_entry_hazard(self, player, entry_hazard):
		entry_hazard_position = ENTRY_HAZARD_TO_INDEX.get(entry_hazard, ENTRY_HAZARD_TO_INDEX['NotFound'])
		return self.get_player_attribute(player, entry_hazard_position)

	def increment_entry_hazard(self, player, entry_hazard):
		current_entry_hazard = self.get_entry_hazard(player, entry_hazard)
		if (current_entry_hazard + 1.0/MAX_ENTRY_HAZARD_COUNT) > 1.0:
			self.set_entry_hazard(player, entry_hazard, 1.0)
		
		else:
			self.set_entry_hazard(player, entry_hazard, current_entry_hazard + 1.0/MAX_ENTRY_HAZARD_COUNT)

	def clear_entry_hazard(self, player, entry_hazard):
		self.set_entry_hazard(player, entry_hazard, 0.0)
	
	def all_entry_hazard(self, player):
		entry_hazards = []
		for entry_hazard in ENTRY_HAZARD_TO_INDEX:
			if entry_hazard not in ['Min', 'Count']:
				entry_hazards.append((entry_hazard, self.get_entry_hazard(player, entry_hazard)))

		return entry_hazards

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

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
		expected_health = [
			('Pelipper', 1.0),
			('Greninja', 1.0),
			('Swampert', 1.0),
			('Manaphy', 1.0),
			('Ferrothorn', 1.0),
			('Tornadus', 1.0)
		]
		gs.init_health(player)
		gs_health = gs.all_health(player)
		if set(gs_health) != set(expected_health):
			print(gs_health)
			print('gs_health had unexpected values when testing init_health')

		for (index, data) in enumerate(expected_health):
			pokemon, _ = data
			gs.set_health(player, pokemon, 0.0)
			new_expected = [element for element in expected_health]
			new_expected[index] = (pokemon, 0.0)
			gs_health = gs.all_health(player)
			if set(gs_health) != set(new_expected):
				print('gs_health had unexpected values when testing set_health')
				print(f'Got {gs_health}')
				print(f'Expected {new_expected}')
			gs.set_health(player, pokemon, 1.0)

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue

		gs.init_health(player)
		player_health_sum = health_sum(gs.vector_list, player)
		if player_health_sum != 6.0:
			print(f'ERROR: unexpected health sum {player_health_sum} after init')
		for position in range(len(gs.name_to_position[player])):
			gs._set_health(player, position, 0.0)

			player_health_sum = health_sum(gs.vector_list, player)
			expected_sum = 6.0 - (position + 1)
			if player_health_sum != expected_sum:
				print('ERROR: unexpected health sum. ' 
					f'Expected {expected_sum} but had {player_health_sum}')


	for player in GameState.Player:
		if player == GameState.Player.count:
			continue

		for position in range(len(gs.name_to_position[player])):
			gs._set_fainted(player, position, 0.0)

		player_ko_count = ko_count(gs.vector_list, player)
		if player_ko_count != 0.0:
			print('ERROR: unexpected player_ko_count after setup')

		if player == GameState.Player.one: 
			team = team1 
		else:
			team = team2
		for expected_index, expected_name in enumerate(team): 
			gs.set_fainted(player, expected_name)		
			player_ko_count = ko_count(gs.vector_list, player)
			expected_ko_count = expected_index + 1
			if player_ko_count != expected_ko_count:
				print(f'ERROR: expected {expected_ko_count} KOs but had '
					f'{player_ko_count}')


	def check_statuses(player, pokemon, status_names):
		has_statuses = gs.check_status(player, pokemon)
		if set(has_statuses) != set(status_names):
			print(f'{pokemon} has types {has_statuses} instead of {status_names}')

	def test_statuses(player, pokemon, status_names):
		for status_name in status_names:
			gs.set_status(player, pokemon, status_name)
		check_statuses(player, pokemon, status_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
		
		#Note: just a test input, such a combination of statuses is unlikely
		pokemon_statuses = [
			('Pelipper', ['brn', 'par', 'slp', 'frz', 'psn', 'tox']),
			('Greninja', ['confusion', 'flinch', 'trapped', 'trapper']),
			('Swampert', ['partiallytrapped', 'lockedmove', 'twoturnmove', 'choicelock']),
			('Manaphy', ['mustrecharge', 'futuremove', 'healreplacement', 'stall', 'gem']),
			('Ferrothorn', ['raindance', 'primordialsea', 'sunnyday', 'desolateland']),
			('Tornadus', ['sandstorm', 'hail', 'deltastream', 'arceus', 'silvally'])
		]
		for pokemon, status_names in pokemon_statuses:
			test_statuses(player, pokemon, status_names)
		for pokemon, status_names in pokemon_statuses:
			check_statuses(player, pokemon, status_names)

	weathers = gs.all_weather()
	if weathers != []:
		print(f'Weathers was {weathers} instead of []')
	gs.set_weather('RainDance')
	weathers = gs.all_weather()
	if len(weathers) > 1 or 'RainDance' not in weathers:
		print(f'Weathers was {weathers} not [\'RainDance\']')

	gs.set_weather('SunnyDay')
	weathers = gs.all_weather()
	if len(weathers) > 1 or 'SunnyDay' not in weathers:
		print(f'Weathers was {weathers} not [\'SunnyDay\']')

	gs.clear_all_weather()
	weathers = gs.all_weather()
	if weathers != []:
		print(f'Weathers was {weathers} instead of []')

	def reset_and_check(gs, player, expected_boosts):
		gs.reset_boosts(player)
		boosts = gs.all_boosts(player) 
		if set(boosts) != set(expected_boosts):
			print('Unexpected boost values')

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		expected_boosts = (('atk', 0.5),
			('def', 0.5), 
			('spa', 0.5), 
			('spd', 0.5), 
			('spe', 0.5), 
			('accuracy', 0.5), 
			('evasion', 0.5),
			('NotFound', 0.5)) 
		reset_and_check(gs, player, expected_boosts)

		for index, boost_name in enumerate(ACTIVE_POKEMON_BOOST):
			reset_and_check(gs, player, expected_boosts)

			new_expected_boosts = [old_boost for old_boost in expected_boosts]
			
			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 0.75)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 1.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 1.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.75)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.5)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.25)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')
			
			break
	
	# Test case for entry hazard names
	test_entry_hazards = ['Spikes', 'Toxic Spikes', 'Stealth Rock', 'Sticky Web']
	for entry_hazard in ENTRY_HAZARD_TO_INDEX.keys():
		if entry_hazard not in test_entry_hazards and entry_hazard not in ['Min', 'Count', 'NotFound']:
			print(f'Unexpected entry hazard: {entry_hazard}')

	# Test case entry hazard increment and decrement
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		# Increment entry hazard value once for all entry hazards
		for entry_hazard in test_entry_hazards:
			gs.increment_entry_hazard(player, entry_hazard)
		
		# Check incremented value with expected value
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 1.0/MAX_ENTRY_HAZARD_COUNT
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_increment for player {player}')
				print(f'Expected: {expected_entry_hazard_value} value for {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')
		
		# clear entry hazard value once for all entry hazards
		for entry_hazard in test_entry_hazards:
			gs.clear_entry_hazard(player, entry_hazard)
		
		# Check cleared value with expected value (= 0.0)
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 0.0
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_clear for {player}')
				print(f'Expected: {expected_entry_hazard_value} value for player {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')
				
		# Increment entry hazard value MAX_ENTRY_HAZARD_COUNT + 1 times to check entry hazard value can't exceed 1.0
		for entry_hazard in test_entry_hazards:
			for _ in range(MAX_ENTRY_HAZARD_COUNT + 1):
				gs.increment_entry_hazard(player, entry_hazard)	
		
		# Check max entry hazard value can be 1.0
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 1.0
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_increment for player {player}, got > 1.0 value')
				print(f'Expected: {expected_entry_hazard_value} value for {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')