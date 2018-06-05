
import queue

class Strategy:
	
	def __init__(self):
		self.explored = {}
		self.frontierLookUp = {}
		self.frontier = queue.PriorityQueue()
	
	def reset(self):
		self.explored = {}
		self.frontier = queue.PriorityQueue()
	
	def fronterEmpty(self):
		return self.frontier.empty()
	
	def getLeaf(self):
		node = self.frontier.get_nowait()
		self.frontierLookUp.pop(node)
		return node
		
	def addToFrontier(self, node):
		self.frontier.put_nowait(node)
		self.frontierLookUp[node] = ""
		
	def addToExplored(self, node):
		self.explored[node] = node
		
	def known(self, node):
		return self.inExplored(node) or self.inFrontier(node)

	def inExplored(self, node):
		return node in self.explored
	
	def inFrontier(self, node):
		return node in self.frontierLookUp
		