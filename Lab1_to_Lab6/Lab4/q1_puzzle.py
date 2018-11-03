# Name         : Kuldeep Singh Bhandari
# Roll No.  : 111601009

class Coordinate :

    def __init__(self, x, y) :
        self.r = x
        self.c = y

def I (exp) :
    return int(exp)

def mod(a, b) :
    return a % b;

def d(coord, n) :
    return (n-coord.x) + (n-coord.y)

def parity(coord, M, n) :
    sum = 0
    for i in range(n*n) :
        if(M[i/4][i%4] == n*n) : continue
        for j in range(i+1, n*n) :
            sum += I(M[i/4][i%4] > M[j/4][j%4])
    return mod(d(coord) + sum, 2)

class Environment :

    def __init__(self, n, M) :
        self.coord = Coordinate(n, n);
        self.n = n
        self.M = M
        
    def updateState (self, action) :
        r = self.coord.r               #row number of empty block
        c = self.coord.c               #column number of empty block
        if(action == 'left') :         #move empty block left 
            if(c <= 1) : return        #if action is invalid
            self.M[r][c], self.M[r][c-1] = (
                    self.M[r][c-1], self.M[r][c])
            self.coord = Coordinate(r, c-1);   #update position of empty block
        elif (action == 'right') :     #move empty block right
            if(c >= self.n) : return   #if action is invalid
            self.M[r][c], self.M[r][c+1] = (
                    self.M[r][c+1], self.M[r][c])
            self.coord = Coordinate(r, c+1);    #update position of empty block
        elif (action == 'up') :        #move empty block up
            if(r <= 1) : return        #if action is invalid
            self.M[r-1][c], self.M[r][c] = (
                    self.M[r][c], self.M[r-1][c])
            self.coord = Coordinate(r-1, c);   #update position of empty block
        elif (action == 'down') :         #move empty block down
            if(r >= self.n) : return      #if action is invalid
            self.M[r+1][c], self.M[r][c] = (
                    self.M[r][c], self.M[r+1][c])
            self.coord = Coordinate(r+1, c);  #update position of empty block
        else : return
        
    def providePerception(self) :         #check if agent has reached goal
        for i in range(1, self.n+1) :
            for j in range(1, self.n+1) :
                if((i-1)*self.n+j != self.M[i][j]) : return False
        return True
    
class Agent :
    
    def takeAction(self, envObj, action) :
        envObj.updateState(action)
    def getPerception(self, envObj) :
        return envObj.providePerception()
