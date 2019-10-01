''' 
Classes to hold pokemon info
'''

# We should add a pokemon object with everything.
# Template
class Pokemon():
	# Pokemon object... useful maybe?
	def __init__(self, name):
        self.name = name
		self.health_points = None
		self.status = None			
		self.type = None
		self.ability = None	
		self.move_list = {}
        # Holds the z_power name if there is one otherwise is none
		self.z_power = None
		self.mega = None
		self.items = None

    def update_move(self, move):
        if move not in self.move_list:
            self.move_list[move] = Moves(move)
    
	def update_health(self, health):
		self.health_points = health
	
	def update_status(self, status):
		self.status = status

    def get_name(self):
        return self.name
    
    def get_health(self):
        return self.health
    
    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

# holds moves and information about moves
# only call this class from Pokemon
# currently only tracks self moves
class Moves():
	# inits the moves
	def __init__(self, _id):
		self.move_id = _id
		self.current_pp = None
		self.max_pp = None
		self.target = None
		self.is_disabled = False

	# updates the Pee pee of the move
	def update_pp(self, pp):
		self.current_pp = pp

	# updates whether a move is disabled or not
	def update_move_status(self, status):
		self.is_disabled = status

    def update_target(self, target):
        self.target = target

    def update_max_pp(self, maxpp):
        self.max_pp = maxpp

# End Class Move()