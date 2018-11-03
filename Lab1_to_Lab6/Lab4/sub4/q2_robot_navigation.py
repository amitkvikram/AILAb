# Name         : Kuldeep Singh Bhandari
# Roll No.     : 111601009

class Coordinate :

    def __init__(self, x, y) :
        self.r = x
        self.c = y
        
#    def equal(self, other) :
#        return self.r == other.r and self.c == other.c
    
class Environment :
    
    def __init__(self, M, n, startx, starty, finishx, finishy) :
        self.coord = Coordinate(startx, starty)     #coordinate of agent
        self.goal = Coordinate(finishx, finishy)    #coordinate of goal
        self.M = M                                  #Matrix
        self.n = n                                  #no of rows/no of columns
        
    def updateState(self, action) :
        r = self.coord.r                    #row number of agent
        c = self.M.coord.c                  #column number of agent
        if(action == 'left') :
            if(c <= 1 or self.M[r][c-1] == 0) : return    #if action is invalid 
            self.M[r][c], self.M[r][c-1] = self.M[r][c-1], self.M[r][c]
            self.coord = Coordinate(r, c-1)    #update position of agent
        elif(action == 'right') :
            if(c >= self.n or self.M[r][c+1] == 0) : return  #if action is invalid
            self.M[r][c], self.M[r][c+1] = self.M[r][c+1], self.M[r][c]
            self.coord = Coordinate(r, c+1)    #update position of agent 
        elif(action == 'up') :
            if(r <= 1 or self.M[r-1][c] == 0) : return     #if action is invalid
            self.M[r][c], self.M[r-1][c] = self.M[r-1][c], self.M[r][c]
            self.coord = Coordinate(r-1, c)    #update position of agent
        elif(action == 'down') :
            if(r >= self.n or self.M[r+1][c] == 0) : return   #if action is invalid
            self.M[r][c], self.M[r+1][c] = self.M[r+1][c], self.M[r][c]
            self.coord = Coordinate(r+1, c)    #update position of agent
        else : return
        
    def providePerception(self) :        #check if agent has reached goal
        return self.coord.equal(self.goal)
        
class Agent :
    
    def takeAction(self, envObj, action):
        envObj.updateState(action)
        
    def getPerception(self, envObj):
        return envObj.providePerception()
    
        