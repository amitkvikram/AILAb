import numpy as np
import pickle

class mainListItem:
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

	def __init__(self, vehicleNo):
		self.vehicleNo = vehicleNo
		print(vehicleMat)

	def calcSpeed(self, x):
		return np.exp(.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))

	def createTimeStamp(self):
		self.timeStamp = []
		lastEntryTime = time[self.vehicleNo, 0]
		for i in range(0, 5):
			currentNode = self.vehicleMat[self.vehicleNo, i]
			entryTime =0 
    def processCurrentVehicle()





