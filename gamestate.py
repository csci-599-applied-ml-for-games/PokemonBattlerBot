'''
This class holds the game state
'''

import pokemoninfo

class PlayerState():

	def __init__(self, team):
		self.active_pokemon = None
		self.team = {}
		self.team_status = {}
		self.team_type_map = {}
		self.team_abilities = {} # this will have to be tracked through damage
		self.team_moves = {}
		self.team_mega = {} # Pokemon that has an active mega evolution.
		self.team_zpower = {} # Pokemon that has already used a Zpower
		self.pokemon_items = {}

	def __parse_pokemon_names(self, team):
		for pokemon in team:
			pokemon_name = str(pokemon.rstrip(', M').rstrip(', F'))
			pokemon_obj = pokemoninfo.Pokemon(pokemon_name)
			self.team[pokemon_name] = pokemon_obj
			self.team_status[pokemon_name] = None
	# end __parse_pokemon_names

	# create empty movelist array for each pokemon
	def __create_movelist(self):
		for pokemon in self.team_status:
            # using normal dict
			self.team_moves[pokemon] = []
	# end __create__movelist			

	def update_active(self, active):
		self.active_pokemon = active
	# end update_active	
	
	# used specifically to track the enemy move state
	def update_moves_list(self, pokemon, move):
		if move not in self.team_moves[pokemon]:
			self.team_moves[pokemon].append(move)
	# end update_moves_list

	def update_abilities(self, pokemon, ability):
		self.team_abilities[str(pokemon)] = ability
	# end update_abilities
	
	def update_team_mega(self, pokemon):
		self.team_mega[pokemon] = True
		# TODO: Megas go inactive once the pokemon faints... add code to switch if pokemon faints
	# end update_team_mega

	def update_used_zpower(self, pokemon):
		self.team_zpower[pokemon] = True

# JK this is not a template don't delete.
class EnemyState(PlayerState):
	# class to track the enemy state
	#
	def __init__(self, opp_team):
		super().__init__(opp_team)
	# end __init__

	# create empty movelist array for each pokemon
	def __create_movelist(self):
		for pokemon in self.team_status:
			self.team_moves[pokemon] = []
	# end __create__movelist			
	
	def update_moves_list(self, pokemon, move):
		if move not in self.team_moves[pokemon]:
			self.team_moves[pokemon].append(move)
	# end update_moves_list