
import copy

class Action:
	
	def __init__(self, description):
		self.description = description
	
	def precondition(self, **state):
		raise NotImplementedError
	
	def effect(self, **state):
		raise NotImplementedError
	
	def cost(self):
		return 1

	def __str__(self):
		return self.description



def prepairSuccessor(state, action):
	successor = copy.deepcopy(state)
	successor.F = None
	successor.G = 0
	successor.parent = state
	successor.action = action
	return successor
	

class MoveAction(Action):
	
	def __init__(self, agent, direction):
		super().__init__(f"Move({direction})")
		self.agtTo = agent.location.fromDirection(direction)
		self.agent = agent
		
	def targets(self):
		return [self.agent.location, self.agtTo]
	
	def precondition(self, state):
		return state.free(self.agtTo)
	
	def effect(self, state):
		successor = prepairSuccessor(state, self)
		successor.changeAgent(copy.deepcopy(self.agent), self.agtTo)
		return successor
	
	def getSuccessors(state):
		successors = []
		for direct in ["N", "E", "S", "W"]:
			action = MoveAction(state.agent, direct)
			if(action.precondition(state)):
				successors.append(action.effect(state))
		return successors
		


class PushAction(Action):
	
	def __init__(self, agent, box, direction):
		super().__init__(f"Push({agent.location.direction(box.location)},{direction})")
		self.boxTo = box.location.fromDirection(direction)
		self.agent = agent
		self.box = box
	
	def targets(self):
		return [self.agent.location, self.box.location, self.boxTo]
	
	def precondition(self, state):
		return state.free(self.boxTo) and self.agent.location.isNeighbor(self.box.location) and self.box.colour == self.agent.colour
	
	def effect(self, state):
		successor = prepairSuccessor(state, self)
		successor.changeAgent(copy.deepcopy(self.agent), self.box.location)
		successor.changeBox(copy.deepcopy(self.box), self.boxTo)
		return successor
	
	def getSuccessors(state):
		successors = []
		for neighbor in state.agent.location.getNeighbors():
			if(neighbor in state.boxes):
				for direction in ["N", "E", "S", "W"]:
					action = PushAction(state.agent, state.boxes.get(neighbor), direction)
					if(action.precondition(state)):
						successors.append(action.effect(state))
		return successors


class PullAction(Action):
	
	def __init__(self, agent, direction, box):
		super().__init__(f"Pull({direction},{agent.location.direction(box.location)})")
		self.agtTo = agent.location.fromDirection(direction)
		self.agent = agent
		self.box = box
	
	def targets(self):
		return [self.agent.location, self.box.location, self.agtTo]
	
	def precondition(self, state):
		return state.free(self.agtTo) and self.agent.location.isNeighbor(self.box.location) and self.box.colour == self.agent.colour
	
	def effect(self, state):
		successor = prepairSuccessor(state, self)
		successor.changeAgent(copy.deepcopy(self.agent), self.agtTo)
		successor.changeBox(copy.deepcopy(self.box), self.agent.location)
		return successor

	def getSuccessors(state):
		successors = []
		for neighbor in state.agent.location.getNeighbors():
			if(neighbor in state.boxes):
				for direction in ["N", "E", "S", "W"]:
					action = PullAction(state.agent, direction, state.boxes.get(neighbor))
					if(action.precondition(state)):
						successors.append(action.effect(state))
		return successors

