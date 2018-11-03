# Name 		: Kuldeep Singh Bhandari
# Roll No.  : 111601009
# Aim       : To implement Simple Traffic Simulator with varying speed
import numpy as np
import sys

# to load Road text file
def loadRoad() :
    print("Loading road...")
#    return pickle.load(open('road', 'r'))
    return np.array(np.loadtxt('road.txt'))

# to load Vehicle text file
def loadVehicle() :
    print("Loading vehicle...")
#    return pickle.load(open('vehicle', 'r'))
    return np.array(np.loadtxt('vehicle.txt'))

# to load Time text file
def loadTime() :
    print("Loading time...")
    return np.array(np.loadtxt('time.txt'))

# to calculate speed of a vehicle
# parameter <x> dentoes number of vehicles ahead of current vehicle
def calcSpeed(x) :
    return np.exp(0.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))

# Environment class which possess informations about Roads, Vehicles,
# Vehicle's starting departure time, etc
class Environment :

    def __init__ (self) :
        self.data = 0
        # <R> stores road adjacent matrix
        self.R = loadRoad().astype(int)
        # <V> stores the vehicle path
        self.V = loadVehicle().astype(int)
        # <T> stores the departure time of vehicles from source
        self.T = loadTime()
        # converting time from minutes to hours
        self.T = self.T/60
        # manager <M> to choose the appropiate vehicle 
        # first column stores the time at which vehicle will move
        # ith row corresponds to ith vehicle
        # second column stores the current state of the vehicle 
        # second column can contain values [0, 1, 2, 3, 4]
        # which represents the current position of the vehicle in the
        # path from source to destination which includes five nodes
        self.M = np.zeros((self.V.shape[0], 2))   
        # setting first column of M to be the departure time of vehicles
        # from source
        self.M[:, 0] = self.T

# creating object of class Environment
env = Environment()

# roadList is a list of list of lists
# roadList[i][j] gives a list containing endtimes of all the vehicles
# which passed through road (i, j)
roadList = [[[] for i in range(env.R.shape[0])] for j in range(env.R.shape[0])]

# <TOT_RUN> stores the number of times manager needs to choose a vehicle
TOT_RUN = env.V.shape[0] * (env.V.shape[1] - 1)
# <out> stores the final output matrix 
# first column stores the vehicle number from 0 to (V.row_size-1)
# the remaining part of <out> is a matrix of size V.row_size * V.column_size
# ith row of this part of the matrix stores the time at which jth node in its
# path
out = np.zeros((env.V.shape[0], env.V.shape[1]+1))
out[:, 0] = [ int(x) for x in list(range(env.V.shape[0])) ]
out[:, 1] = env.T

# running loop for <TOT_RUN> times because we need to make
# exact <TOT_RUN> number of changes in the first column of <M>
for i in range(0, TOT_RUN) :
    
    # <x> stores the row index of minimum element of first column of <M>
    # <x> is basically the vehicle which will run in nearest time
    x = np.where(env.M[:, 0] == np.min(env.M[:, 0]))[0][0]
    # <cnt> stores number of vehicles which are ahead of current vehicle <x>
    cnt = 0 
    # <y> stores the node column number at which vehicle <x> is present
    # <y> can contain values [0, 1, 2, 3, 4]
    y = int(env.M[x, 1])
    # <startTime> stores the time at which vehicle <x> reaches node column number <y>
    startTime = env.M[x, 0]
    # <ind1> stores the node at which vehicle <x> is present
    ind1 = env.V[x, y]
    # <ind2> stores the node at which vehicle <x> will reach from <ind1>
    ind2= env.V[x, y+1]
    # <aheadVehicles> stores the list of departure time of vehicles from road (i, j)
    aheadVehicles = []
    # <speed> stores number of vehicles ahead of a vehicles in the list 
    # <aheadVehicles>
    speed = 0
    # loop to count number of vehicles which are ahead of current vehicle <x>
    # and store the list of departure time of vehicles 
    for time in roadList[ind1][ind2] :
        if(time > startTime) :
            cnt += 1
            aheadVehicles.append(time)

    # <endTime> stores the time at which vehicle <x> stores the departure time
    # from road (i, j) --> initialise with <startTime>
    endTime = startTime
    # <totDist> stores the distance travelled from starting point
    totDist = 0
    # loop to calculate the distance travelled and time taken when the other vehicles
    # were also present
    for time in aheadVehicles :
        # calculate the distance travelled by vehicle <x> when <cnt> vehicles were
        # ahead
        totDist += calcSpeed(cnt) * (time - endTime)
        # add time to travel distance when <cnt> vehicle were present to when <cnt> 
        # vehicle were present to <endTime>
        endTime += (time - endTime)
        # decrease number of vehicle ahead of vehicle <x>
        cnt -= 1
           
    endTime += (env.R[ind1, ind2] - totDist) / calcSpeed(cnt)
    # saving start time of vehicle <x> at node <ind2>
    out[x][y+2] = endTime
    # changing start time of vehicle <x> which is now equal to <endTime> 
    env.M[x, 0] = endTime
    # incrementing the node column number to update position of vehicle <x>
    env.M[x, 1] += 1
    # append the departure time of vehicle <x> in the roadList for road 
    # (<ind1>, <ind2>)
    roadList[ind1][ind2].append(endTime)
    
    # if vehicle is currently at column node number equal to (V.column_size-1)
    # then set starting time for vehicle <x> to be Maximum system size so that
    # vehicle <x> will not used by manager anymore
    if(int(env.M[x, 1]) == env.V.shape[1]-1) :
        env.M[x, 0] = sys.maxsize

# print <out> matrix
print(out)
# save matrix <out> as csv file
np.savetxt('output2.csv', np.asarray(out), '%5.10f', delimiter=',', 
           header='Vehicle, site1,site2,site3,site4,site5')
print('Saving output in text file <output.csv>...')


