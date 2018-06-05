
class Node:
	
	def __init__(self, parent, action):
		self.action = action
		self.parent = parent
		self.F = None
		self.G = 0
		self.H = None
	
	def f(self):
		if(self.F == None):
			self.F = self.g() + self.h() * 1.001
		return self.F
	
	def g(self):
		if(self.parent and not self.G):
			self.G = self.parent.G + self.action.cost()
		return self.G

	def h(self):
		raise NotImplementedError

	def getSuccessors(self):
		raise NotImplementedError
	
	def __hash__(self):
		raise NotImplementedError

	def __lt__(self, other):
		return self.f() < other.f()
