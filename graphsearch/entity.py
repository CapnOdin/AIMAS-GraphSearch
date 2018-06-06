
class Entity:
	
	def __init__(self, id, location):
		self.id = id
		self.location = location
	
	def __hash__(self):
		raise NotImplementedError
	
	def __eq__(self):
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError
	

class Agent(Entity):
	
	def __init__(self, id, location, colour):
		super().__init__(id, location)
		self.colour = colour
	
	def copyConstructor(other):
		return Agent(other.id, other.location, other.colour)
		
	def __hash__(self):
		return hash((self.id, self.location, self.colour))

	def __eq__(self, other):
		return self.id == other.id and self.location == other.location and self.colour == other.colour
		
	def __str__(self):
		return f"Agent({self.id}, {self.colour}, {str(self.location)})"



class Box(Entity):
	
	def __init__(self, id, location, colour):
		super().__init__(id, location)
		self.colour = colour
	
	def copyConstructor(other):
		return Box(other.id, other.location, other.colour)
	
	def __hash__(self):
		return hash((self.id, self.location, self.colour))

	def __eq__(self, other):
		return self.id == other.id and self.location == other.location and self.colour == other.colour
		
	def __str__(self):
		return f"Box({self.id}, {self.colour}, {str(self.location)})"



class Goal(Entity):
	
	def __init__(self, id, location):
		super().__init__(id, location)
	
	def __hash__(self):
		return hash((self.id, self.location))
	
	def __eq__(self, other):
		return self.id == other.id and self.location == other.location
	
	def __str__(self):
		return f"Goal({self.id}, {str(self.location)})"

