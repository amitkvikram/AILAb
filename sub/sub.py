
# Name : Amit Vikram Singh
# Roll No: 111601001
from __future__ import print_function
import numpy as np
import math
from Queue import PriorityQueue
import copy


class State:
    def __init__(self, mat, pos):
        self.mat = mat
        self.pos = pos                   # type : <Coordinate> class, coordinate of empty block(n2 - 1)

    def __eq__(self, other):
        return (self.mat == other.mat)

    def __cmp__(self, other):
        return cmp(self.mat, other.mat)

    # overriding hashing function
    def __hash__(self) :
        return hash(str(self.mat.M))
# class <Node> represents a state which possess informations like
# <M> which is matrix of the current state,
# <pos> which is the coordinate of current position of the empty block,
# <action> which is action taken by parent to reach this state
# <parent> which is the parent state of this state
class QueueNode :
    def __init__(self, state, action, parent, g, priority) :
        self.state = state
        self.action = action
        self.parent = parent             # type : <Node> class
        self.g = g
        self.priority = priority    

    #define compare function to compare the priority
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

# class <Coordinate> represents the x-coordinate and y-coordinate of a block
class Coordinate :

    def __init__(self, x, y) :
        self.r = x
        self.c = y

    def __eq__(self, other):
        return (self.r == other.r and self.c == other.c)


def I (exp) :
    return int(exp)

def mod(a, b) :
    return a % b;

def d(coord, n) :
    return (n-coord.r) + (n-coord.c)

def parity(coord, M, n) :
    sum = 0
    for i in range(n*n) :
        # if(M[i//n][i%n] == n*n) : continue
        for j in range(i+1, n*n) :
            sum += I(M[i//n][i%n] > M[j//n][j%n])
    return mod(d(coord, n-1) + sum, 2)

#Calculate Heuristic
def manhattanHeuristic(envObj, state):
    heuristic = 0
    for i in range(envObj.n):
        for j in range(envObj.n):
            row = (state.mat.M[i][j] - 1)/envObj.n 
            col = (state.mat.M[i][j] - 1)%envObj.n
            heuristic+=abs(row - i) + abs(col - j)

    return heuristic

    

class Matrix :

    def __init__(self, M) :
        self.M = M

    # function <__eq__> overrides "==" operator so whenever we write 
    # "matrix1 == matrx2", it will check whether all corresponding elements
    # of both matrices are equal
    def __eq__(self, other) :
        n = other.M.shape[0]
        for i in range(n) :
            for j in range(n) :
                if(self.M[i, j] != other.M[i,j]) :
                    return False
        return True

    def getCopy(self):
        return Matrix(self.M.copy())

class Environment :

    def __init__(self, n, mat, emptyblockPos1, emptyblockPos2) :
        self.emptyblockPos1 = emptyblockPos1
        self.emptyblockPos2 = emptyblockPos2
        self.mat = mat
        self.n = n
        
    def updateState (self, action) :
#        print("updateState fired...")
        r = self.emptyblockPos2.r               #row number of empty block
        c = self.emptyblockPos2.c               #column number of empty block
        # print(type(self.mat))
        if(action == 'left') :         #move empty block left 
            if(c <= 0) : return False        #if action is invalid
            self.mat.M[r][c], self.mat.M[r][c-1] = (
                    self.mat.M[r][c-1], self.mat.M[r][c])
            self.emptyblockPos2 = Coordinate(r, c-1);   #update position of empty block
            return True
        elif (action == 'right') :     #move empty block right
            if(c >= self.n-1) : return False   #if action is invalid
            self.mat.M[r][c], self.mat.M[r][c+1] = (
                    self.mat.M[r][c+1], self.mat.M[r][c])
            self.emptyblockPos2 = Coordinate(r, c+1);    #update position of empty block
            return True
        elif (action == 'up') :        #move empty block up
            if(r <= 0) : return  False      #if action is invalid
            self.mat.M[r-1][c], self.mat.M[r][c] = (
                    self.mat.M[r][c], self.mat.M[r-1][c])
            self.emptyblockPos2 = Coordinate(r-1, c);   #update position of empty block
            return True
        elif (action == 'down') :         #move empty block down
            if(r >= self.n-1) : return False      #if action is invalid
            self.mat.M[r+1][c], self.mat.M[r][c] = (
                    self.mat.M[r][c], self.mat.M[r+1][c])
            self.emptyblockPos2 = Coordinate(r+1, c);  #update position of empty block
            return True
        else : return False
        
    def providePerception(self) :         #check if agent has reached goal
        for i in range(0, self.n) :
            for j in range(0, self.n) :
                if(i*self.n+j+1 != self.mat.M[i][j]) : return False
        return True

    def parity(self):
        sum = 0
        for i in range(self.n*self.n) :
            # if(M[i//n][i%n] == n*n) : continue
            for j in range(i+1, n*n) :
                sum += I(self.mat.M[i//n][i%n] > self.mat.M[j//n][j%n])
        return mod(d(self.emptyblockPos2, self.n - 1) + sum, 2)

    #If parity is odd then make it even by swapping 15 with a block which is not (n2 - 1)
    def makeParityEven(self):
        print("Making Parity Even by swaping (n2 - 1) with an adjacent block which is not (n2)")
        row = self.emptyblockPos1.r
        col = self.emptyblockPos1.c
        if(row + 1 < self.n and col < n and (not (Coordinate(row + 1, col) == self.emptyblockPos2))):
            self.mat.M[row][col], self.mat.M[row + 1][col] = self.mat.M[row + 1][col], self.mat.M[row][col]

        elif(row < self.n and col + 1 < n and (not (Coordinate(row, col + 1) == self.emptyblockPos2))):
            self.mat.M[row][col], self.mat.M[row][col + 1] = self.mat.M[row][col + 1], self.mat.M[row][col]

        elif(row < self.n and col - 1 < n and (not (Coordinate(row , col - 1) == self.emptyblockPos2))):
            self.mat.M[row][col], self.mat.M[row][col - 1] = self.mat.M[row][col - 1], self.mat.M[row][col]

        elif(row -1 < self.n and col < n and (not (Coordinate(row - 1, col) == self.emptyblockPos2))):
            self.mat.M[row][col], self.mat.M[row - 1][col] = self.mat.M[row - 1][col], self.mat.M[row][col]

        print("New Board = ", self.mat.M)


    
class Agent :
    def __init__(self):
        self.exploredStates = set()
    
    def takeAction(self, envObj, action) :
        return envObj.updateState(action)

    def getPerception(self, envObj) :
        return envObj.providePerception()

    def addInExploredState(self, state):
        self.exploredStates.add(state)

    def isExplored(self, state):
        return (state in self.exploredStates)

#Print Path
def printPath(curr) :
    if(curr is None) : return 0
    cost = printPath(curr.parent)
    print(curr.action, "\n", curr.state.mat.M)
    return cost  + 1

pq  = PriorityQueue()
#Take input
n = int(raw_input())
#M = np.array([[3, 1], [2, 4]])
print(n)
M = np.zeros((n, n), dtype = np.int)
for i in range(n):
    a = raw_input().split()
    for j in range(len(a)):
        M[i][j] = int(a[j])

Mat = Matrix(M)
#Initialize Environment Object
x, y = map(int, raw_input().split())
emptyblockPos1 = Coordinate(x, y)
x, y = map(int, raw_input().split())
emptyblockPos2 = Coordinate(x, y)

envObj = Environment(n, Mat,emptyblockPos1, emptyblockPos2)
agent = Agent()
print("Board = ", envObj.mat.M)

# check if parity of the given matrix is odd
if(envObj.parity() == 1) :
    print("Odd Parity")
    envObj.makeParityEven()
print("Parity = ", envObj.parity())

print("======================================")
actionList = ['left', 'right', 'up', 'down']
state = State(copy.copy(envObj.mat), copy.copy(envObj.emptyblockPos2))
curr = QueueNode(state, "None", None, 0, 0)
pq.put(curr)        # rows and columns from 0 to n-1

while(not pq.empty()):
    curr = pq.get()
    # update environment matrix with new matrix of state <curr>
    envObj.mat = curr.state.mat.getCopy()
    # update coordinate of enviroment empty block with that of state <curr>
    envObj.coord = copy.copy(curr.state.pos)
    # if requried state is found, then break
    if(agent.isExplored(curr.state)):
        continue
    if(agent.getPerception(envObj)) :
        destination = curr
        break

    agent.addInExploredState(curr.state)

    # going through all possible actions
    for action in actionList :
        # update environment matrix with new matrix of state <curr>
        envObj.mat = curr.state.mat.getCopy()
        # update coordinate of enviroment empty block with that of state <curr>
        envObj.emptyblockPos2 = copy.copy(curr.state.pos)
        flag = agent.takeAction(envObj, action)
        nextState = State(envObj.mat.getCopy(), copy.copy(envObj.emptyblockPos2))
#        print("flag", flag, "visited", m not in s)
        if(flag and (not agent.isExplored(nextState))) :
            g = curr.g 
            h = manhattanHeuristic(envObj, nextState)
            priority = g + h
            pq.put(QueueNode(nextState, action, curr, g, priority))
    
print("The path is as follows : \n")
cost = printPath(curr)
print(cost)
