
from graphsearch.node import Node
from graphsearch.location import Location
from graphsearch import action
from graphsearch.entity import Agent, Box
from graphsearch import world

class State(Node):
	
	def __init__(self, parent = None, action = None, agent = None):
		super().__init__(parent, action)
		
		self.HASH = None
		
		self.agentsByLocation = {}
		self.agentsByColour = {}
		self.agentsById = {}
		
		self.boxesByLocation = {}
		self.boxesByColour = {}
		self.boxesById = {}
		self.goalConditions = []
		
		if(parent):
			self.copyConstructor(parent)
		else:
			self.agent = agent
	
	def copyConstructor(self, other):
		self.agent = Agent.copyConstructor(other.agent)
		self.agentsByLocation = {agent.location : agent for agent in other.agentsByLocation.values()}
		self.boxesByLocation = {box.location : box for box in other.boxesByLocation.values()}
		self.goalConditions = other.goalConditions
		self.setUpBoxes()
		self.setUpAgents()
	
	
	def isGoal(self):
		for condition in self.goalConditions:
			if(not condition.check(self)):
				return False
		return True
	
	def h(self):
		h = 0
		agentlocation = self.agent.location
		for condition in self.goalConditions:
			box = self.getClosetsBox(condition.goal.location, condition.goal.id)
			h += box.location.manhattanDistance(agentlocation) + condition.goal.location.manhattanDistance(box.location)
			agentlocation = condition.goal.location
		self.H = h
		return h
	
	def free(self, location):
		return not (location in self.agentsByLocation or location in self.boxesByLocation or location in world.walls)

	def changeAgent(self, agentLocation, location):
		agent = Agent.copyConstructor(self.getAgent(agentLocation))
		del self.agentsByLocation[agentLocation]
		agent.location = location
		agent.HASH = None
		if(self.agent.id == agent.id):
			self.agent = agent
		self.agentsByLocation[location] = agent
	
	def changeBox(self, boxLocation, location):
		box = Box.copyConstructor(self.getBox(boxLocation))
		del self.boxesByLocation[boxLocation]
		boxes = self.getBox(box.id)
		boxes.remove(box)
		box.location = location
		box.HASH = None
		boxes.append(box)
		self.boxesByLocation[location] = box
	
	def getSuccessors(self):
		successors = [*action.MoveAction.getSuccessors(self), *action.PushAction.getSuccessors(self), *action.PullAction.getSuccessors(self)]
		return successors
	
	def getBox(self, key):
		if(type(key) == str):
			if(len(key) == 1):
				return self.boxesById[key]
			else:
				return self.boxesByColour[key]
		
		if(type(key) == Location):
			return self.boxesByLocation[key]
	
	def getAgent(self, key):
		if(type(key) == str):
			if(len(key) == 1):
				return self.agentsById[key]
			else:
				return self.agentsByColour[key]
		
		if(type(key) == Location):
			return self.agentsByLocation[key]
		
	
	def setUpBoxes(self):
		for pos, box in self.boxesByLocation.items():
			if(box.colour not in self.boxesByColour):
				self.boxesByColour[box.colour] = []
			if(box.id not in self.boxesById):
				self.boxesById[box.id] = []
			self.boxesByColour[box.colour].append(box)
			self.boxesById[box.id].append(box)
	
	
	def setUpAgents(self):
		for pos, agent in self.agentsByLocation.items():
			if(agent.colour not in self.agentsByColour):
				self.agentsByColour[agent.colour] = []
			self.agentsByColour[agent.colour].append(agent)
			self.agentsById[agent.id] = agent
			
	
	def getClosetsBox(self, location, id):
		closest = None
		distance = None
		for box in self.getBox(id.upper()):
			if(not closest or distance > location.manhattanDistance(box.location)):
				closest = box
				distance = location.manhattanDistance(box.location)
		return closest
	
	
	def __eq__(self, other):
		for pos, agent in self.agentsByLocation.items():
			if(pos not in other.agentsByLocation or other.agentsByLocation.get(pos) != agent):
				return False
			
		for pos, box in self.boxesByLocation.items():
			if(pos not in other.boxesByLocation or other.boxesByLocation.get(pos) != box):
				return False
		
		return True
	
	def __hash__(self):
		if(not self.HASH):
			self.HASH = hash((frozenset(self.agentsByLocation.values()), frozenset(self.boxesByLocation.values())))
		return self.HASH
	
	def __str__(self):
		combined = {}
		for pos in world.walls:
			combined[pos] = "+"
		for pos, goal in world.goals.items():
			combined[pos] = goal.id
			
		for pos, box in self.boxesByLocation.items():
			combined[pos] = box.id
		for pos, agent in self.agentsByLocation.items():
			combined[pos] = agent.id
		
		string = ""
		previous = Location(-1, 0)
		for pos, id in sorted(combined.items()):
			if(previous.y < pos.y):
				string += "\n" + (" " * (pos.x if pos.x > 0 else 0)) + id
			else:
				string += (" " * (pos.x - previous.x - 1 if pos.x - previous.x - 1 > 0 else 0)) + id
			previous = pos
		return string
		
	
	
	
	
	
	