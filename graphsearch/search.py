
import time

class GraphSearch:
	
	def __init__(self, strategy):
		self.strategy = strategy
	
	def search(self, initial):
		#f = open("search.txt", "w")
		start = time.process_time()
		count = 1
		
		self.strategy.reset()
		self.strategy.addToFrontier(initial)
		
		while(not self.strategy.fronterEmpty()):
			leaf = self.strategy.getLeaf()
			
			self.strategy.addToExplored(leaf)
			
			#f.write(f"f: {leaf.F}, g: {leaf.G}, h: {leaf.H}\n{leaf}\n")
			
			if(leaf.isGoal()):
				#f.close()
				return leaf
			
			if((count % 10000) == 0):
				self.searchStatus(start)
			count += 1
			
			if(count > 10000):
				return leaf
			
			for successor in leaf.getSuccessors():
				if(not self.strategy.known(successor)):
					successor.f()
					self.strategy.addToFrontier(successor)

	def searchStatus(self, start):
		explored = len(self.strategy.explored)
		frontier = len(self.strategy.frontierLookUp)
		print(f"#Explored: {explored}, #Frontier: {frontier}, #Generated: {explored + frontier}, Time: {time.process_time() - start}")