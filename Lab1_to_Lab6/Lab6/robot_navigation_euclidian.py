# Name         : Kuldeep Singh Bhandari (111601009)
#              : Amit Vikram Singh (111601001)

import numpy as np
from Queue import PriorityQueue
import copy
import math

# class <Node> represents a node in a graph which possess informations like
# <pos> which is the coordinate of current position of tge node,
# <action> which is action taken by parent to reach the node
# <parent> which is the parent of the node
class Node :
    # constructor for class <Node>
    def __init__(self, pos, action, parent, g, h) :
        self.pos = pos             # type : <Coordinate> class
        self.action = action
        self.parent = parent        # type : <Node> class
        self.g = g
        self.h = h

    def __cmp__(self, other) :
        return cmp(self.g+self.h, other.g+other.h)

# class <Coordinate> represents the x-coordinate and y-coordinate of a node        
class Coordinate :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
        
    # function <__eq__> overrides "==" operator so whenever we write 
    # "coord1 == coord2", it will check whether x- and y-coordinate of coord1
    # and coord2 are equal, respectively
    def __eq__(self, other) :
        return self.x == other.x and self.y == other.y
    
    # to return coordinate in parenthesis
    def toString(self) :
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
# function <printPath> prints path using recursion from <destination> node
# and going back to the starting node and start printing nodes from starting
# node to destination node
def printPath(destination) :
    if(destination is None) : return 0
    temp = printPath(destination.parent)
    print(destination.action, destination.pos.toString())
    return 1 + temp
        
#class Environment contains five fields
# M => matrix which represents the graph in matrix-form
# agentPos => current position of agent in the graph
# goalPos => destination position of agent in graph    
class Environment :
    
    def __init__(self, M, pos, goalPos) :
        self.M = M                # type : m*n Matrix
        self.agentPos = pos       # type : <Coordinate> class
        self.goalPos = goalPos    # type : <Coordinate> class
        self.m = M.shape[0]       # number of rows of M
        self.n = M.shape[1]       # number of columns of M
    
    def updateState(self, action, curr) :
        r = curr.x               #row number of empty block
        c = curr.y               #column number of empty block
        if(action == 'left') :         #move empty block left 
            if(c <= 0 or self.M[r][c-1] == 1) : return False        #if action is invalid
            self.agentPos = Coordinate(r, c-1);   #update position of agent
            return True
        elif (action == 'right') :     #move empty block right
            if(c >= self.n-1 or self.M[r][c+1] == 1) : return False   #if action is invalid
            self.agentPos = Coordinate(r, c+1);    #update position of agent
            return True
        elif (action == 'up') :        #move empty block up
            if(r <= 0 or self.M[r-1][c] == 1) : return  False      #if action is invalid
            self.agentPos = Coordinate(r-1, c);   #update position of agent
            return True
        elif (action == 'down') :         #move empty block down
            if(r >= self.m-1 or self.M[r+1][c] == 1) : return False      #if action is invalid
            self.agentPos = Coordinate(r+1, c);  #update position of agent
            return True
        elif (action == 'left-up') :
            if(r <= 0 or c <= 0 or self.M[r-1][c-1]) : return False
            self.agentPos = Coordinate(r-1, c-1)
            return True
        elif (action == 'right-up') :
            if(c >= self.n-1 or r <= 0 or self.M[r-1][c+1]) : return False
            self.agentPos = Coordinate(r-1, c+1)
            return True
        elif (action == 'left-down') : 
            if(c <= 0 or r >= self.m-1 or self.M[r+1][c-1]) : return False
            self.agentPos = Coordinate(r+1, c-1)
            return True
        elif (action == 'right-down') :
            if(c >= self.n-1 or r >= self.m-1 or self.M[r+1][c+1]) : return False
            self.agentPos = Coordinate(r+1, c+1)
            return True
        else : return False
        
    def providePerception(self, currPos) :
        # <__eq__> function of class <Coordinate> will be called
        return currPos == self.goalPos    

    def euclidDist(self, curr) :
        return math.sqrt(self.sumOfSquares(curr, self.goalPos))
    def sumOfSquares(self, curr, goal) :
        return (curr.x - goal.x)*(curr.x-goal.x) + (curr.y - goal.y)*(curr.y-goal.y)
        
class Agent :
    
    def takeAction(self, envObj, action, curr) :
        return envObj.updateState(action, curr)

    def getPerception(self, envObj, currPos) :
        return envObj.providePerception(currPos)
        
q = PriorityQueue() # initialize priority queue
# <M> is the matrix representing the graph
# 1 represents blocked positions
# 0 represents walkable positions
M = np.array([[1, 0, 0, 1, 1, 1, 0, 1, 1, 1 ],
              [1, 0, 0, 0, 1, 1, 1, 0, 1, 1 ],
              [1, 1, 0, 0, 1, 1, 0, 1, 0, 1 ],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
              [1, 1, 1, 0, 0, 1, 1, 0, 1, 0 ],
              [1, 0, 0, 1, 0, 1, 0, 1, 0, 0 ],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
              [1, 0, 1, 0, 1, 0, 0, 1, 1, 1 ],
              [1, 1, 0, 0, 0, 0, 1, 0, 0, 1 ]])
# <start> represents starting position 
print "__________________________"
print "GRID"
print M
print "__________________________"
print "Heuristic = Euclidean Distance"
print "Moves Allowed = left,right,up,down,leftUp,leftDown,rightUp,rightDown"
start = Coordinate(6, 4)
print "__________________________"
print "Source = ", start.toString()
# <end> represents goal position
end = Coordinate(1, 1)
print "Goal = ", end.toString()
# creating an instance <envObj> of class Environment initialized with matrix M,
# starting position <start> and goal position <end>
envObj = Environment(M, start, end)
agent = Agent()
# putting <start> node into queue
A_Track = M.copy().astype(np.float)
A_Track[A_Track == 1] = float('Inf')
q.put(Node(start, 'None', None, 0, envObj.euclidDist(start)))
# envObj.M[start.x][start.y] = 1
destination = None
c = 1
# print("TRACKING A* ALGORITHM : ")
while(not q.empty()) :
    curr = q.get()
    # print('('+str(curr.pos.x) + ',', str(curr.pos.y) + ')')
    # if destination is reached, save that node in <destination> and break
    if(agent.getPerception(envObj, curr.pos)) : 
        A_Track[curr.pos.x][curr.pos.y] = c
        destination = curr
        break
    actionList = ['left', 'right', 'up', 'down', 'left-up', 'right-up', 
                  'left-down', 'right-down']
    currPos = curr.pos
    if(envObj.M[currPos.x][currPos.y] == 1) : continue
    # print("c = ", c, "curr.pos.x = ", curr.pos.x, "curr.pos.y = ", curr.pos.y)
    A_Track[curr.pos.x][curr.pos.y] = c
    c+=1
    envObj.M[currPos.x][currPos.y] = 1
    for action in actionList :
        # flag checks if the action was valid or not
        flag = agent.takeAction(envObj, action, copy.copy(currPos))
        if flag :
            # if action is valid, then put that node into the queue
            q.put(Node(copy.copy(envObj.agentPos), action, curr, curr.g+1, envObj.euclidDist(envObj.agentPos)))
if(destination is None) :
    print("Not reachable")
else :
    print "__________________________"
    print "SHORTEST PATH:"
    cost = printPath(destination)
    print "__________________________"
    print "cost = ",cost - 1
    print "__________________________"
    print("A* Track")
    print(A_Track)
