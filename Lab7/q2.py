#!usr/bin/python
# import numpy as np
from __future__ import print_function
import math
from Queue import PriorityQueue
import enum

class Mode(enum.Enum):
	bus = 0
	cycle = 1

class State:
	def __init__(self, nodeIndex, mode = Mode.bus, budget = 1000000):
		self.nodeIndex = nodeIndex
		self.mode = mode  #mode by which agent reaches in current state
		self.budget = budget
	def __eq__(self, other): 
		print("check")
		return (self.nodeIndex == other.nodeIndex
		and self.mode == other.mode and self.budget == other.budget)

	def __hash__(self):
		return hash(self.mode.value * 1000 + self.nodeIndex + self.budget)
		
	def toString(self):
		return (str(self.nodeIndex) + ", " + str(self.mode) + ", " + str(self.budget))

class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def toString(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

def calcEuclideanHeuristic(coord1, coord2):
	return math.sqrt((coord2.x - coord1.x)**2 + (coord2.y - coord1.y)**2)

class Edge:
	def __init__(self, destination, wt):
		self.destination = destination
		self.wt = wt

class GraphNode:
	def __init__(self, coord, explored = False, heuristic = 0):
		self.adjList = []
		self.heuristic = heuristic
		self.coord = coord
	
class QueueNode:
	def __init__(self, ind, g, priority, parent, state):
		self.ind = ind
		self.g = g
		self.priority = priority
		self.parent = parent
		self.state = state
		
	def __cmp__(self, other):
		return cmp(self.priority, other.priority)

class Environment:
	def __init__(self, numVertices, numEdges, source, goal, congestion = 0):
		self.numVertices = numVertices
		self.numEdges = numEdges
		self.congestion = congestion
		self.source = source
		self.goal = goal
		self.graph = []

	def getCongestion(self):
		return self.congestion
	
	def addNode(self, coord):
		self.graph.append(GraphNode(coord))
		
	def isGoal(self, curr):
		return self.goal == curr

class Agent:
	def __init__(self, budget = 5):
		self.explored = set()
		self.cycleSpeed = 5
		self.busMaxSpeed = 50.0
		self.busMinSpeed = 10.0
		self.busFare = 10
		self.budget = budget

	def getBusSpeed(self, envObj):
		# print(self.busMaxSpeed, envObj.getCongestion())
		return self.busMaxSpeed - ((self.busMaxSpeed - self.busMinSpeed) / 100) * envObj.getCongestion()
		
	def getCycleSpeed(self):
		return self.cycleSpeed

	def addInExplored(self, state):
		print(type(state))
		self.explored.add(state)

	def isExplored(self, state):
		return state in self.explored

def printPath(envObj, currNode):
	if (currNode.parent is None):
		# print(currNode.state.toString())
		print(envObj.graph[currNode.ind].coord.toString())
		return

	printPath(envObj, currNode.parent)
	# print(currNode.ind)
	# print(currNode.state.toString())
	print(currNode.state.mode, "----> ", envObj.graph[currNode.ind].coord.toString())

#----------------------Pre Calculate Heuristic Using Dijksrta---------------
def calcHeuristic( envObj, agent):
	exploredState = set()   #set to store explored states
	#We will assume that agent always takes bus
	pq = PriorityQueue()
	pq.put(QueueNode(envObj.goal, 0, 0, None, State(envObj.goal, Mode.bus)))

	while (not pq.empty()):
		curr = pq.get()
		if (curr.ind in exploredState):
			continue
		envObj.graph[curr.ind].heuristic = curr.g     #save heuristic for curr.ind

		exploredState.add(curr.ind)
		for edge in envObj.graph[curr.ind].adjList:
			if edge.destination in exploredState:
				continue
			g = curr.g + edge.wt
			pq.put(QueueNode(edge.destination, g, g, curr, State(curr.ind, Mode.bus)))
	
	for node in envObj.graph:                 
		node.heuristic = node.heuristic / agent.busMaxSpeed

#--------------------------Heuristic Calculated-------------------------
			
[n, m] = map(int, raw_input().split())
#Take input of goal and source(index of source and goal not the coordinate)
[source, goal] = map(int, raw_input().split())
#initialize environment
envObj = Environment(n, m, source - 1, goal - 1)
# envObj.initializeGraph()

#Take coordinate of each node
for i in range(n):
	[a, b] = map(int, raw_input().split())
	envObj.addNode(Coord(a, b))
	
#Take input of edges
for i in range(envObj.numEdges):
	[a, b, wt] = map(float, raw_input().split())
	a-=1
	b -= 1
	a = int(a)
	b = int(b)
	# print("a, b, wt", a, b,  wt, envObj.graph[a].coord.toString())
	envObj.graph[a].adjList.append(Edge(b, wt))
	envObj.graph[b].adjList.append(Edge(a, wt))

#agent.budget =  int(raw_input())
#envObj.congestion = int(raw_input())

# Calculate heuristic-----------------------DIJKSTRA----
#We will assume that agent always takes bus except when dist<3
agent = Agent(5)	 #agent(budget)
calcHeuristic(envObj, agent)

#-------------------------------------------

for i in range(3):
	print("===============================================")
	destinationNode = None
	pq = PriorityQueue()
	pq.put(QueueNode(envObj.source, 0, 0, None, State(envObj.source,Mode.bus, agent.budget)))
	agent = Agent(10)  #agent(budget)
	envObj.congestion = (2 - i) * 50
	print("Congestion = ", envObj.getCongestion(),"%")
	print("Budget = ", agent.budget)
	print("Source = ", envObj.graph[envObj.source].coord.toString())
	print("Goal = ", envObj.graph[envObj.goal].coord.toString())
	print("BusSpeed = ", agent.getBusSpeed(envObj))
	print("BusFare = ", agent.busFare)
	print("CycleSpeed = ", agent.getCycleSpeed())
	while(not pq.empty()):
		curr = pq.get()
		# print(curr.state.toString())
		if(envObj.isGoal(curr.ind)):           #if agent reached the goal
			destinationNode = curr
			print("Reached Goal")
			break
		if(agent.isExplored(curr.state)):       #if curr state is already explored continue;
			continue
		
		agent.addInExplored(curr.state)         #mark curr state as explored
		
		for edge in envObj.graph[curr.ind].adjList:
			for mode in Mode:                   
				if(edge.wt <= 3 and mode is Mode.bus): #if current road lenght <=3 then agent can not take bus
					continue
				if mode is Mode.bus:                  #if agent is taking bus to go from curr.ind -> edge.destination
						time = edge.wt / agent.getBusSpeed(envObj)
						budget = curr.state.budget - time * agent.busFare    #calculate budget left with agent
						if (budget < 0):            #if budget is not sufficient to take bus 
							continue
				else:                                #agent is taking cycle to go from curr.ind -> edge.destination
					time = edge.wt / agent.getCycleSpeed()
					budget = curr.state.budget      
				nextState = State(edge.destination, mode, budget)
				if (not agent.isExplored(nextState)):    #if nextState is not explored
					priority = envObj.graph[edge.destination].heuristic + time + curr.g    #calulate g+h
					pq.put(QueueNode(edge.destination, time + curr.g, priority, curr, nextState))   #push next State
				
	if destinationNode is None:    #if there exist no possible way to go from goal to source
		print("Unreachable")

	else:
		print("------PATH------")
		printPath(envObj, destinationNode)
		print("Time = ", destinationNode.g)
	print("===============================================")
