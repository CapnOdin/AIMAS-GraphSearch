
from graphsearch.node import Node
from graphsearch.location import Location
from graphsearch.condition import GoalCondition
from graphsearch.action import MoveAction, PushAction, PullAction
from graphsearch import world

class State(Node):
	
	def __init__(self, parent = None, action = None, agent = None):
		super().__init__(parent, action)
		self.agent = agent
		if(parent):
			self.agents = parent.agents
			self.boxes = parent.boxes
			self.goalConditions = parent.goalConditions
		else:
			self.agents = {}
			self.boxes = {}
			self.goalConditions = []
	
	def isGoal(self):
		for condition in self.goalConditions:
			if(not condition.check(self)):
				return False
		return True
	
	def h(self):
		h = 0
		agentlocation = self.agent.location
		for condition in self.goalConditions:
			box = self.getClosetsBox(condition.goal.location, condition.goal.id, self.agent.colour)
			h += box.location.manhattanDistance(agentlocation)
			h += condition.goal.location.manhattanDistance(box.location)
			agentlocation = condition.goal.location
		self.H = h
		return h
	
	def free(self, location):
		return not (location in self.agents or location in self.boxes or location in world.walls)

	def changeAgent(self, agent, location):
		del self.agents[agent.location]
		agent.location = location
		if(self.agent.id == agent.id):
			self.agent = agent
		self.agents[location] = agent
	
	def changeBox(self, box, location):
		del self.boxes[box.location]
		box.location = location
		self.boxes[location] = box
	
	def getSuccessors(self):
		successors = [*MoveAction.getSuccessors(self), *PushAction.getSuccessors(self), *PullAction.getSuccessors(self)]
		return successors
	
	def getClosetsBox(self, location, id, colour = False):
		closest = None
		distance = None
		for pos, box in self.boxes.items():
			if((not colour and id == box.id.lower()) or (colour == box.colour and id == box.id.lower())):
				if(not closest or distance > location.manhattanDistance(box.location)):
					closest = box
					distance = location.manhattanDistance(box.location)
		return closest
	
	def __eq__(self, other):
		for pos, agent in self.agents.items():
			if(pos not in other.agents or other.agents.get(pos) != agent):
				return False
			
		for pos, box in self.boxes.items():
			if(pos not in other.boxes or other.boxes.get(pos) != box):
				return False
		
		return True
	
	def __hash__(self):
		return hash((frozenset(self.agents.items()), frozenset(self.boxes.items())))
	
	def __str__(self):
		combined = {}
		for pos in world.walls:
			combined[pos] = "+"
		for pos, goal in world.goals.items():
			combined[pos] = goal.id
			
		for pos, box in self.boxes.items():
			combined[pos] = box.id
		for pos, agent in self.agents.items():
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
		
	
	
	
	
	
	