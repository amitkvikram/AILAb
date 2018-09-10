#!usr/bin/python
# import numpy as np
from __future__ import print_function
from Queue import PriorityQueue

class Edge:
	def __init__(self, destination, wt):
		self.destination = destination
		self.wt = wt

class GraphNode:
	def __init__(self, adjList = [], explored = False, heuristic = 0):
		self.adjList = adjList
		self.explored = explored
		self.heuristic = heuristic
	

class QueueNode:
	def __init__(self, ind, g, priority, parent):
		self.ind = ind
		self.g = g
		self.priority = priority
		self.parent = parent
		
	def __cmp__(self, other):
		return cmp(self.priority, other.priority)
	

class Environment:
	def __init__(self, numVertices, numEdges, source, goal):
		self.numVertices = numVertices
		self.numEdges = numEdges
		self.source = source
		self.goal = goal
	
	def initializeGraph(self):
		self.graph = [GraphNode() for i in range(self.numVertices)]
		
	def isGoal(self, curr):
		return self.goal == curr

def printPath(currNode):
	if(currNode.parent is None):
		print(currNode.ind)
		return

	printPath(currNode.parent)
	print(currNode.ind, " ")

			
[n, m] = map(int, raw_input().split())
#Take input of goal and source
[source, goal] = map(int, raw_input().split())
envObj = Environment(n, m, source - 1, goal - 1)
envObj.initializeGraph()

#Take input of heuristic
# for i in range(n):
# 	h = 
	
#Take input of edges
for i in range(envObj.numEdges	):
	[a, b, wt] = map(int, raw_input().split())
	a-=1
	b-=1
	envObj.graph[a].adjList.append(Edge(b, wt))
	# envObj.graph[b].adjList.append(Edge(a, wt))

destinationNode = None
pq = PriorityQueue()
pq.put(QueueNode(envObj.source, 0, 0, None))

while(not pq.empty()):
	curr = pq.get()
	print("currInd = ",curr.ind)
	if(envObj.isGoal(curr.ind)):
		destinationNode = curr
		print("Reached Goal", destinationNode.ind)
		break
		
	envObj.graph[curr.ind].explored = True
		
	for edge in envObj.graph[curr.ind].adjList:
		if(not envObj.graph[edge.destination].explored):
			print("push = ", edge.destination)
			pq.put(QueueNode(edge.destination, edge.wt + curr.g, envObj.graph[edge.destination].heuristic + edge.wt + curr.g, curr))
if destinationNode is None:
	print("Unreachable goal")
else: printPath(destinationNode)