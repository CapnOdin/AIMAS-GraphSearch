
from graphsearch import state

class Action:
	
	def __init__(self, description):
		self.description = description
	
	def precondition(self, **node):
		raise NotImplementedError
	
	def effect(self, **node):
		raise NotImplementedError
	
	def cost(self):
		return 1

	def __str__(self):
		return self.description



def prepairSuccessor(node, action):
	successor = state.State(node)
	successor.F = None
	successor.G = 0
	successor.parent = node
	successor.action = action
	return successor
	

class MoveAction(Action):
	
	def __init__(self, agent, direction):
		super().__init__(f"Move({direction})")
		self.agtTo = agent.location.fromDirection(direction)
		self.agent = agent
		
	def targets(self):
		return [self.agent.location, self.agtTo]
	
	def precondition(self, node):
		return node.free(self.agtTo)
	
	def effect(self, node):
		successor = prepairSuccessor(node, self)
		successor.changeAgent(self.agent.location, self.agtTo)
		return successor
	
	def getSuccessors(node):
		successors = []
		for direct in ["N", "E", "S", "W"]:
			action = MoveAction(node.agent, direct)
			if(action.precondition(node)):
				successors.append(action.effect(node))
		return successors
		


class PushAction(Action):
	
	def __init__(self, agent, box, direction):
		super().__init__(f"Push({agent.location.direction(box.location)},{direction})")
		self.boxTo = box.location.fromDirection(direction)
		self.agent = agent
		self.box = box
	
	def targets(self):
		return [self.agent.location, self.box.location, self.boxTo]
	
	def precondition(self, node):
		return node.free(self.boxTo) and self.agent.location.isNeighbor(self.box.location) and self.box.colour == self.agent.colour
	
	def effect(self, node):
		successor = prepairSuccessor(node, self)
		successor.changeAgent(self.agent.location, self.box.location)
		successor.changeBox(self.box.location, self.boxTo)
		return successor
	
	def getSuccessors(node):
		successors = []
		for neighbor in node.agent.location.getNeighbors():
			if(neighbor in node.boxes):
				for direction in ["N", "E", "S", "W"]:
					action = PushAction(node.agent, node.boxes.get(neighbor), direction)
					if(action.precondition(node)):
						successors.append(action.effect(node))
		return successors


class PullAction(Action):
	
	def __init__(self, agent, direction, box):
		super().__init__(f"Pull({direction},{agent.location.direction(box.location)})")
		self.agtTo = agent.location.fromDirection(direction)
		self.agent = agent
		self.box = box
	
	def targets(self):
		return [self.agent.location, self.box.location, self.agtTo]
	
	def precondition(self, node):
		return node.free(self.agtTo) and self.agent.location.isNeighbor(self.box.location) and self.box.colour == self.agent.colour
	
	def effect(self, node):
		successor = prepairSuccessor(node, self)
		successor.changeAgent(self.agent.location, self.agtTo)
		successor.changeBox(self.box.location, self.agent.location)
		return successor

	def getSuccessors(node):
		successors = []
		for neighbor in node.agent.location.getNeighbors():
			if(neighbor in node.boxes):
				for direction in ["N", "E", "S", "W"]:
					action = PullAction(node.agent, direction, node.boxes.get(neighbor))
					if(action.precondition(node)):
						successors.append(action.effect(node))
		return successors

