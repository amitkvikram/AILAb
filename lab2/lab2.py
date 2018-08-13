import numpy as np
import pickle

class MainListItem:
    def __init__(self, vehicle_no, start_time, source, departure):
        self.vehicle_no = vehicle_no
        self.start_time =start_time
        self.source = source
        self.destination = departure
    def printObject(self):
        print(self.vehicle_no, self.start_time, self.source, self.destination);

class RoadItem:
    def __init__(self, vehicle_no, arrival_time, departure_time):
        self.vehicle_no = vehicle_no
        self.arrival_time = arrival_time
        self.departure_time = departure_time
    def printObject(self):
        print(self.vehicle_no, self.arrival_time, self.departure_time)

def loadVehicleData():
	#print "Loading Vehicle Matrix"
	return np.array(np.load('vehicle'))

def loadRoadData():
	#print "Loading Road Matrix"
	return np.array(np.load('road')).astype(np.float)

def loadTimeData():
	#print "Loading Time Data"
	return np.array(np.load('time', encoding = 'latin1')).astype(np.float)/60

class Environment:
	vehicleMat = loadVehicleData()
	timeMat = loadTimeData()
	roadMat = loadRoadData()
    trafiic = np.zeros(vehicleMat.shape)
    roadList = [[[] for j in range(roadMat.shape[0])] for k in range(roadMat.shape[1])]
    mainList = []

	def __init__(self, vehicleNo):
		self.vehicleNo = vehicleNo
        //Initialize mainList
        for i in range(0, time.shape[0]):
            src = vehicle[i,0]
            dest = vehicle[i,1]
            mainList.append(MainListItem(i, timeMat[i, 0], src, dest))

	def calcSpeed(self, x):
		return np.exp(.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))
    
    def createTrafiicDetail():
        while len(mainList)!=0:
            mainList.sort(key = lambda x:x.start_time, reverse = True)
            currObj = mainList.pop()   #Type MainListItem
            currRoadCarList = roadList[currObj.source][currObj.destination]     #Type: RoadItem
            #push current Car in current roadList
            roadList[currObj.source][currObj.destination].append(RoadItem(currObj.vehicle_no,
                                                                  currObj.start_time, 
                                                                  currObj.start_time + timeTaken))
            
            #update traffic detail
            traffic[currObj.vehicle_no][0] = traffic[currObj.vehicle_no][0].astype(np.int)+1
            rootNumber = output[currObj.vehicle_no][0].astype(np.int)
            output[currObj.vehicle_no][ind1] = currObj.start_time + timeTaken
            
            #Update mainList
            if output[currObj.vehicle_no][0] != 4:
                st = currObj.start_time + timeTaken
                mainList.append(mainListItem(currObj.vehicle_no,
                                st[0],
                                currObj.destination,
                                vehicle[currObj.vehicle_no][output[currObj.vehicle_no][0].astype(np.int) + 1]))
   
    def processCurrentVehicle():





