	# Name         : Kuldeep Singh Bhandari (111601009)
#              : Amit Vikram Singh (111601001)

import numpy as np
from queue import Queue
import copy

# class <Node> represents a state which possess informations like
# <M> which is matrix of the current state,
# <pos> which is the coordinate of current position of the empty block,
# <action> which is action taken by parent to reach this state
# <parent> which is the parent state of this state
class Node :
    def __init__(self, M, pos, action, parent) :
        self.M = M
        self.pos = pos                   # type : <Coordinate> class
        self.action = action
        self.parent = parent             # type : <Node> class

# class <Coordinate> represents the x-coordinate and y-coordinate of a block
class Coordinate :

    def __init__(self, x, y) :
        self.r = x
        self.c = y

def I (exp) :
    return int(exp)

def mod(a, b) :
    return a % b;

def d(coord, n) :
    return (n-coord.r) + (n-coord.c)

def parity(coord, M, n) :
    sum = 0
    for i in range(n*n) :
        if(M[i//n][i%n] == n*n) : continue
        for j in range(i+1, n*n) :
            sum += I(M[i//n][i%n] > M[j//n][j%n])
    return mod(d(coord, n-1) + sum, 2)

def printPath(curr) :
    if(curr is None) : return
    printPath(curr.parent)
    print(curr.action, "\n", curr.M)
    

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

    # overriding hashing function
    def __hash__(self) :
        return hash(str(self.M))

class Environment :

    def __init__(self, n, M) :
        self.coord = Coordinate(n-1, n-1);
        self.n = n
        self.M = M
        
    def updateState (self, action) :
#        print("updateState fired...")
        r = self.coord.r               #row number of empty block
        c = self.coord.c               #column number of empty block
        if(action == 'left') :         #move empty block left 
            if(c <= 0) : return False        #if action is invalid
            self.M[r][c], self.M[r][c-1] = (
                    self.M[r][c-1], self.M[r][c])
            self.coord = Coordinate(r, c-1);   #update position of empty block
            return True
        elif (action == 'right') :     #move empty block right
            if(c >= self.n-1) : return False   #if action is invalid
            self.M[r][c], self.M[r][c+1] = (
                    self.M[r][c+1], self.M[r][c])
            self.coord = Coordinate(r, c+1);    #update position of empty block
            return True
        elif (action == 'up') :        #move empty block up
            if(r <= 0) : return  False      #if action is invalid
            self.M[r-1][c], self.M[r][c] = (
                    self.M[r][c], self.M[r-1][c])
            self.coord = Coordinate(r-1, c);   #update position of empty block
            return True
        elif (action == 'down') :         #move empty block down
            if(r >= self.n-1) : return False      #if action is invalid
            self.M[r+1][c], self.M[r][c] = (
                    self.M[r][c], self.M[r+1][c])
            self.coord = Coordinate(r+1, c);  #update position of empty block
            return True
        else : return False
        
    def providePerception(self) :         #check if agent has reached goal
        for i in range(0, self.n) :
            for j in range(0, self.n) :
                if(i*self.n+j+1 != self.M[i][j]) : return False
        return True
    
class Agent :
    
    def takeAction(self, envObj, action) :
        return envObj.updateState(action)

    def getPerception(self, envObj) :
        return envObj.providePerception()

# stores explored states
s = set()
q = Queue()
n = 3   # defines size  of matrix n*n
#M = np.array([[3, 1], [2, 4]])
M = np.array([[3, 1, 2], [4, 5, 8], [6, 7, 9]]) # elements from 1 to n*n
# check if parity of the given matrix is odd
if(parity(Coordinate(n-1, n-1), M, n) == 1) :
    print("Odd Parity")
else :    
    envObj = Environment(n, M)
    agent = Agent()
    actionList = ['left', 'right', 'up', 'down']
    curr = Node(M.copy(), Coordinate(2, 2), 'None', None)
    q.put(curr)        # rows and columns from 0 to n-1
    # make matrix M explored
    s.add(Matrix(M))
    check = False
    while(not q.empty()) :
        curr = q.get()
        # update environment matrix with new matrix of state <curr>
        envObj.M = curr.M.copy()
        # update coordinate of enviroment empty block with that of state <curr>
        envObj.coord = copy.copy(curr.pos)
        # if requried state is found, then break
        if(agent.getPerception(envObj)) :
            destination = curr
            break
    
        # going through all possible actions
        for action in actionList :
            # update environment matrix with new matrix of state <curr>
            envObj.M = curr.M.copy()
            # update coordinate of enviroment empty block with that of state <curr>
            envObj.coord = copy.copy(curr.pos)
            flag = agent.takeAction(envObj, action)
            m = Matrix(copy.copy(envObj.M))
    #        print("flag", flag, "visited", m not in s)
            if(flag and (m not in s)) :
                q.put(Node(envObj.M.copy(), copy.copy(envObj.coord), action, curr)) 
                s.add(m)
    
    print("The path is as follows : \n")
    printPath(curr)
