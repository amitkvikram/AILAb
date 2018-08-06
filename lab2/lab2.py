import numpy as np
import pickle

class timeStamp:
	def __init__(node, entryTime):
		self.node = node
		self.entryTime = entryTime

def loadVehicleData():
	print "Loading Vehicle Matrix"
	return np.load("vehicle", allow_pickle = True)

def loadRoadData():
	print "Loading Road Matrix"
	return np.load("road", allow_pickle = True)

def loadTimeData():
	print "Loading Time Data"
	return np.load("time", allow_pickle = True)

class Vehicle:
    
	vehicleMat = loadVehicleData
	timeMat = loadTimeData
	roadMat = loadRoadData

	def __init__(self, vehicleNo):
		slef.vehicleNo = vehicleNo

	def calcSpeed(self, x):
		return np.exp(.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))

	def createTimeStamp(self):
		self.timeStamp = []
		








