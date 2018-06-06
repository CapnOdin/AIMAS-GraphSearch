
from graphsearch.state import State
from graphsearch.location import Location
from graphsearch.entity import Agent, Box, Goal
from graphsearch import world

import re


def loadFile(path):
	f = open(path, "r")
	return parseMap(f.readlines(), {})


def parseMap(strMap, colours):
	initial = State()
	for row in range(0, len(strMap)):
		for column in range(0, len(strMap[row])):
			pos = Location(column, row)
			if(strMap[row][column] == "+"):
				world.walls[pos] = True
			elif(re.match("[0-9]", strMap[row][column])):
				initial.agentsByLocation[pos] = Agent(strMap[row][column], pos, colours.get(strMap[row][column], "Red"))
			elif(re.match("[A-Z]", strMap[row][column])):
				initial.boxesByLocation[pos] = Box(strMap[row][column], pos, colours.get(strMap[row][column], "Red"))
			elif(re.match("[a-z]", strMap[row][column])):
				world.goals[pos] = Goal(strMap[row][column], pos)
	initial.setUpAgents()
	initial.setUpBoxes()
	return initial

