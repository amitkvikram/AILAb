#!usr/bin/python
# import numpy as np
from __future__ import print_function
import math
from Queue import PriorityQueue

#Class for state of node
class State:
	def __init__(self, nodeIndex):
		self.nodeIndex = nodeIndex

	def __eq__(self, other):
		return self.nodeIndex == other.nodeIndex

	def __hash__(self):
		return hash(self.nodeIndex)
	
#Class to store coordinate
class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def toString(self):
		return str(self.x) + " " + str(self.y)

#Calculate Euclidean distance between two coordinates
def calcEuclideanHeuristic(coord1, coord2):
	return math.sqrt((coord2.x - coord1.x)**2 + (coord2.y - coord1.y)**2)

#info about edge
class Edge:
	def __init__(self, destination, wt):
		self.destination = destination   
		self.wt = wt        #Edge Weight(length)

#Info about each graph node
class GraphNode:
	def __init__(self, coord, heuristic = 0):
		self.adjList = []
		self.heuristic = heuristic
		self.coord = coord
	
#Info about each node in QueueNode
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
	def __init__(self, numVertices, numEdges, source, goal):
		self.numVertices = numVertices
		self.numEdges = numEdges
		self.source = source
		self.goal = goal
		self.graph = []
	
	def addNode(self, coord):              #add a node in graph
		self.graph.append(GraphNode(coord))
		
	def isGoal(self, curr):              #check is curr is goal
		return self.goal == curr

class Agent:
	def __init__(self):
		self.explored = set()     #Set to store state which are explored

	def addInExplored(self, state):
		self.explored.add(state)     #add state in explored states

	def isExplored(self, state):
		return state in self.explored      #check if state is explored is not

def printPath(envObj1, currNode):
	if(currNode.parent is None):           #if currNode is source
		print(envObj1.graph[currNode.ind].coord.toString())
		return

	printPath(envObj1, currNode.parent)
	# print(currNode.ind)
	print((envObj1.graph[currNode.ind].coord).toString())

			
[n, m] = map(int, raw_input().split())
#Take input of goal and source(index of source and goal not the coordinate)
[source, goal] = map(int, raw_input().split())
#initialize environment
envObj = Environment(n, m, source - 1, goal - 1)
#initialize Agent
agent = Agent()

#Take coordinate of each node from input.txt
for i in range(n):
	[a, b] = map(int, raw_input().split())
	envObj.addNode(Coord(a, b))

# Store heuristic
for i in range(n):
	envObj.graph[i].heuristic=calcEuclideanHeuristic(envObj.graph[i].coord,
						 envObj.graph[envObj.goal].coord)
	
#Take input of edges
for i in range(envObj.numEdges):
	[a, b, wt] = map(float, raw_input().split())
	a-=1
	b -= 1
	a = int(a)
	b = int(b)
	envObj.graph[a].adjList.append(Edge(b, wt))
	envObj.graph[b].adjList.append(Edge(a, wt))

destinationNode = None
pq = PriorityQueue()
#FORMAT = pq.put(QueuNode(indexOfGraphNode, g, g + heuristic, parent, State(index)))
pq.put(QueueNode(envObj.source, 0, 0, None, State(envObj.source)))      #Push Source in priority queue

#Run A* Algorithm
while(not pq.empty()):
	curr = pq.get()
	if(envObj.isGoal(curr.ind)):           #Agent reached the goal
		destinationNode = curr
		print("Reached Goal", destinationNode.ind)
		break
		
	if(agent.isExplored(curr.state)):       #if current state is already explored coninue for next state
		continue
	agent.addInExplored(curr.state)         #add current state in explored set
		
	for edge in envObj.graph[curr.ind].adjList:       #traverse adjacency list of current grpahnode
		nextState = State(edge.destination)
		if(not agent.isExplored(nextState)):         #if next state is not already explored
			priority = envObj.graph[edge.destination].heuristic + edge.wt + curr.g
			pq.put(QueueNode(edge.destination, edge.wt + curr.g, priority, curr, nextState))

if destinationNode is None:      #There is not path between source and goal
	print("Unreachable goal")
else:
	 printPath(envObj, destinationNode)
	 print("cost = ", destinationNode.g)