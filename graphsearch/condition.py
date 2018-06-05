
class Condition:
	
	def __init__(self):
		pass

	def check(self, node):
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError



class GoalCondition(Condition):
	
	def __init__(self, goal):
		super().__init__()
		self.goal = goal
	
	def check(self, node):
		if(self.goal.location in node.boxes):
			return node.boxes.get(self.goal.location).id.lower() == self.goal.id
		return False

	def __str__(self):
		return str(self.goal)
