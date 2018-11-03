
# Name : Amit Vikram Singh
# Roll No: 111601001
from __future__ import print_function
import numpy as np
import math
from Queue import PriorityQueue
import copy


#==========================Class to represent state of a configuration=================================
class State:
    def __init__(self, mat, pos1, pos2):
        self.mat = mat
        self.pos1 = pos1                   # type : <Coordinate> class, coordinate of empty block(n2 - 1)
        self.pos2 = pos2

    def __eq__(self, other):
        return (self.mat == other.mat)

    def __cmp__(self, other):
        return cmp(self.mat, other.mat)

    # overriding hashing function
    def __hash__(self) :
        return hash(str(self.mat.M))
#=======================================================================================================
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

#=====================================Function to Calculate Heuristic===================================
def manhattanHeuristic(envObj, state):
    heuristic = 0
    for i in range(envObj.n):
        for j in range(envObj.n):
            if(state.mat.M[i][j] == (envObj.n * envObj.n) or state.mat.M[i][j] == (envObj.n * envObj.n - 1)):
                continue
            row = int((state.mat.M[i][j] - 1)/envObj.n )
            col = int((state.mat.M[i][j] - 1)%envObj.n)
            heuristic+=(abs(row - i) + abs(col - j))

    return heuristic
#=======================================================================================================
#======================================Matrix Class represents configuration============================
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
                if(i == n - 1 and j == n - 2): continue
                if(i ==  n - 1 and j == n - 1): continue
                if(self.M[i, j] != other.M[i,j]) :
                    return False
        return True

    def getCopy(self):
        return Matrix(self.M.copy())
#=======================================================================================================
#===============================================ENVIRONMENT=============================================
class Environment :
    def __init__(self, n, mat, emptyblockPos1, emptyblockPos2) :
        self.emptyblockPos1 = emptyblockPos1
        self.emptyblockPos2 = emptyblockPos2
        self.mat = mat
        self.n = n
        
    def updateState (self, action, block) :
#        print("updateState fired...")
       
        if(block == 0):                             #First empty block is being moved
            r = self.emptyblockPos1.r               #row number of empty block
            c = self.emptyblockPos1.c               #column number of empty block
            # print(type(self.mat))
            if(action == 'left') :         #move empty block left 
                if(c <= 0) : return False        #if action is invalid
                if(Coordinate(r, c-1) == self.emptyblockPos2):
                    return False;
                self.mat.M[r][c], self.mat.M[r][c-1] = (
                        self.mat.M[r][c-1], self.mat.M[r][c])
                self.emptyblockPos1 = Coordinate(r, c-1);   #update position of empty block
                return True
            elif (action == 'right') :     #move empty block right
                if(c >= self.n-1) : return False   #if action is invalid
                if(Coordinate(r, c+1) == self.emptyblockPos2):
                    return False;
                self.mat.M[r][c], self.mat.M[r][c+1] = (
                        self.mat.M[r][c+1], self.mat.M[r][c])
                self.emptyblockPos1 = Coordinate(r, c+1);    #update position of empty block
                return True
            elif (action == 'up') :        #move empty block up
                if(r <= 0) : return  False      #if action is invalid
                if(Coordinate(r - 1, c) == self.emptyblockPos2):
                    return False;
                self.mat.M[r-1][c], self.mat.M[r][c] = (
                        self.mat.M[r][c], self.mat.M[r-1][c])
                self.emptyblockPos1 = Coordinate(r-1, c);   #update position of empty block
                return True
            elif (action == 'down') :         #move empty block down
                if(r >= self.n-1) : return False      #if action is invalid
                if(Coordinate(r + 1, c) == self.emptyblockPos2):
                    return False;
                self.mat.M[r+1][c], self.mat.M[r][c] = (
                        self.mat.M[r][c], self.mat.M[r+1][c])
                self.emptyblockPos1 = Coordinate(r+1, c);  #update position of empty block
                return True
            else : return False

        else:                                       #Second empty block is being moved
            r = self.emptyblockPos2.r               #row number of empty block
            c = self.emptyblockPos2.c               #column number of empty block
            if(action == 'left') :         #move empty block left 
                if(c <= 0) : return False        #if action is invalid
                if(Coordinate(r, c-1) == self.emptyblockPos1):
                    return False;
                self.mat.M[r][c], self.mat.M[r][c-1] = (
                        self.mat.M[r][c-1], self.mat.M[r][c])
                self.emptyblockPos2 = Coordinate(r, c-1);   #update position of empty block
                return True
            elif (action == 'right') :     #move empty block right
                if(c >= self.n-1) : return False   #if action is invalid
                if(Coordinate(r, c + 1) == self.emptyblockPos1):
                    return False;
                self.mat.M[r][c], self.mat.M[r][c+1] = (
                        self.mat.M[r][c+1], self.mat.M[r][c])
                self.emptyblockPos2 = Coordinate(r, c+1);    #update position of empty block
                return True
            elif (action == 'up') :        #move empty block up
                if(r <= 0) : return  False      #if action is invalid
                if(Coordinate(r - 1, c) == self.emptyblockPos1):
                    return False;
                self.mat.M[r-1][c], self.mat.M[r][c] = (
                        self.mat.M[r][c], self.mat.M[r-1][c])
                self.emptyblockPos2 = Coordinate(r-1, c);   #update position of empty block
                return True
            elif (action == 'down') :         #move empty block down
                if(r >= self.n-1) : return False      #if action is invalid
                if(Coordinate(r + 1, c) == self.emptyblockPos1):
                    return False;
                self.mat.M[r+1][c], self.mat.M[r][c] = (
                        self.mat.M[r][c], self.mat.M[r+1][c])
                self.emptyblockPos2 = Coordinate(r+1, c);  #update position of empty block
                return True
            else : return False
        
    def providePerception(self) :         #check if agent has reached goal
        for i in range(0, self.n) :
            for j in range(0, self.n) :
                if(i == self.n - 1 and j == self.n - 2): continue
                if(i == self.n- 1 and j == self.n - 1): continue
                if((i*self.n+j+1) != self.mat.M[i][j]) : return False
        return True

#==================================================================================
#========================================AGENT=====================================
class Agent :
    def __init__(self):
        self.exploredStates = set()
    
    def takeAction(self, envObj, action, block) :           #Take action, block is used to check which one of the empty block is moved
        return envObj.updateState(action, block)

    def getPerception(self, envObj) :
        return envObj.providePerception()

    def addInExploredState(self, state):                   #add state in explored set
        self.exploredStates.add(state)

    def isExplored(self, state):                          #Return true if state is already explored
        return (state in self.exploredStates)
#=================================================================================================

#function to Print Path
def printPath(curr) :
    if(curr is None) : return 0
    cost = printPath(curr.parent)
    print(curr.action, "\n", curr.state.mat.M)
    return cost + 1

pq  = PriorityQueue()                #Priority queue to store fringe

#=============================TAKE INPUT==========================================
#Take input
n = int(raw_input())                 #No of rows or columns in matrix
#M = np.array([[3, 1], [2, 4]])
M = np.zeros((n, n), dtype = np.int)         #Board
for i in range(n):                         #Take input of initial board configuration
    a = raw_input().split()
    for j in range(len(a)):
        M[i][j] = int(a[j])

Mat = Matrix(M)
#Initialize Environment Object
x, y = map(int, raw_input().split())             #Take input of coordinate of first empty block
emptyblockPos1 = Coordinate(x, y)
x, y = map(int, raw_input().split())             #Take input of coordinate of second empty block
emptyblockPos2 = Coordinate(x, y)
#====================================================================================

envObj = Environment(n, Mat,emptyblockPos1, emptyblockPos2)            #Initialize environment
agent = Agent()                                                        #Initialize Agent
print("Board = ", envObj.mat.M)
print("======================================")
actionList = ['left', 'right', 'up', 'down']                   #Action Space

#---------------------Push Initial States-----------------------------
state = State(copy.copy(envObj.mat), copy.copy(envObj.emptyblockPos1), copy.copy(envObj.emptyblockPos2))
h = manhattanHeuristic(envObj, state) 
curr = QueueNode(state, "None", None, 0, h)
pq.put(curr)        # rows and columns from 0 to n-1
#--------------------------------------------------------------------

#===================================A*===============================================
while(not pq.empty()):
    curr = pq.get()
    # update environment matrix with new matrix of state <curr>
    envObj.mat = curr.state.mat.getCopy()
    if(agent.isExplored(curr.state)):
        continue
    # if requried state is found, then break
    if(agent.getPerception(envObj)) :                              #If agent has reache the goal break the loop
        print("Reached")
        destination = curr
        break

    agent.addInExploredState(curr.state)

    # going through all possible actions
                          #select one of the empty block to move
    for action in actionList :
        for block in range(2): 
            # update environment matrix with new matrix of state <curr>
            envObj.mat = curr.state.mat.getCopy()
            # update coordinate of enviroment empty block with that of state <curr>
            envObj.emptyblockPos2 = copy.copy(curr.state.pos2)      #moving first empty
            envObj.emptyblockPos1 = copy.copy(curr.state.pos1)                #Moving second empty block                 
            flag = agent.takeAction(envObj, action, block)

            #Get next state
            nextState = State(envObj.mat.getCopy(), copy.copy(envObj.emptyblockPos1), copy.copy(envObj.emptyblockPos2))   #moving first empty
            # else: nextState = State(envObj.mat.getCopy(), copy.copy(envObj.emptyblockPos1), copy.copy(envObj.emptyblockPos2))     #Moving second empty block 
    #        print("flag", flag, "visited", m not in s)
            if(flag and (not agent.isExplored(nextState))) :
                g = curr.g + 1
                h = manhattanHeuristic(envObj, nextState)             #Calculate heuristic corresponding to next state
                priority = g + h                              
                agent.addInExploredState(curr.state)   
                pq.put(QueueNode(nextState, action, copy.copy(curr), g, priority))      #Push next state in priority queue
        
#=======================================================================================================

#--------------------------------Print Path and cost--------------------
print("The path is as follows : \n")
cost = 0
cost= printPath(curr)
print("Cost = ", cost)
