
import math

class Location:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.HASH = None
	
	def isNeighbor(self, other):
		return self.manhattanDistance(other) == 1
	
	def manhattanDistance(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y)
	
	def euclideanDistance(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
		
	def fromDirection(self, direction):
		translations = {"E":[1,0], "W":[-1,0], "S":[0,1], "N":[0,-1]}
		i, j = translations.get(direction)
		return Location(self.x + i, self.y + j)
	
	def direction(self, other):
		translations = {(1,0):"E", (-1,0):"W", (0,1):"S", (0,-1):"N"}
		return translations.get((self.x - other.x, self.y - other.y))
	
	def getNeighbors(self):
		neighbors = []
		for i, j in [[1,0], [-1,0], [0,1], [0,-1]]:
			neighbors.append(Location(self.x + i, self.y + j))
		return neighbors
	
	def __lt__(self, other):
		return (self.y < other.y) or (self.y == other.y and self.x < other.x)
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	
	def __hash__(self):
		if(not self.HASH):
			self.HASH = hash((self.x, self.y))
		return self.HASH

	def __str__(self):
		return f"({self.x}, {self.y})"