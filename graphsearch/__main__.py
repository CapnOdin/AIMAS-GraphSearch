
from graphsearch import communicator, search, strategy, condition, world

import profile

def main():
	state = communicator.loadFile("D:\GitHubProjects\JMAI-AIMAS\environment\levels\SAsimple2.lvl")
	#state = communicator.loadFile("D:\GitHubProjects\JMAI-AIMAS\environment\levels\SAanagram.lvl")
	#state = communicator.loadFile("D:\GitHubProjects\JMAI-AIMAS\environment\levels\SAAlphabet.lvl")
	graphsearch = search.GraphSearch(strategy.Strategy())
	
	state.agent = list(state.agents.items())[0][1]
	
	for i, goal in world.goals.items():
		state.goalConditions.append(condition.GoalCondition(goal))
	result = graphsearch.search(state)
	
	print(result)





profile.run('main()')
input("Press Enter to Terminate the process")