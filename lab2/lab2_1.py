import numpy as np
import pickle

class MainListItem:
    def __init__(self, vehicle_no, start_time, source, destination):
        self.vehicle_no = vehicle_no
        self.start_time =start_time
        self.source = source
        self.destination = destination
    def printObject(self):
        print(self.vehicle_no, self.start_time, self.source, self.destination);

class RoadItem:
    def __init__(self,departure_time):      
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
	traffic = np.zeros((vehicleMat.shape[0],vehicleMat.shape[1] + 1))
	roadCarList = [[[] for j in range(roadMat.shape[0])] for k in range(roadMat.shape[1])]
	mainList = []

	def __init__(self):
        # //Initialize mainList
		for i in range(0, self.timeMat.shape[0]):
			src = self.vehicleMat[i,0]
			dest = self.vehicleMat[i,1]
			self.mainList.append(MainListItem(i, self.timeMat[i, 0], src, dest))
			self.traffic[:,1] = self.timeMat[:, 0]

	def calcSpeed(self, x):
		return np.exp(.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))

	def createTrafiicDetail(self):
		while len(self.mainList)!=0:
			self.mainList.sort(key = lambda x:x.start_time, reverse = True)
			currObj = self.mainList.pop()   #Type MainListItem
			currRoadCarList = self.roadCarList[currObj.source][currObj.destination]     #Type: RoadItem
			timeTaken = self.processCurrentVehicle(currObj)
			#push current Car in current roadList
			self.roadCarList[currObj.source][currObj.destination].append(RoadItem(currObj.start_time + timeTaken))
			#update traffic detail
			self.traffic[currObj.vehicle_no][0] = self.traffic[currObj.vehicle_no][0].astype(np.int)+1
			rootNumber = self.traffic[currObj.vehicle_no][0].astype(np.int)
			self.traffic[currObj.vehicle_no][rootNumber + 1] = currObj.start_time + timeTaken
			#Update mainList
			if self.traffic[currObj.vehicle_no][0] != 4:
				st = currObj.start_time + timeTaken
				self.mainList.append(MainListItem(currObj.vehicle_no,
            st,
            currObj.destination,
            self.vehicleMat[currObj.vehicle_no][self.traffic[currObj.vehicle_no][0].astype(np.int) + 1]))
	def processCurrentVehicle(self, mainListItem):
		timeTaken = 0;   #final value will be equal to time taken to travel current road
		carAhead = 0;
		roadLength = self.roadMat[mainListItem.source, mainListItem.destination]
		startTime = mainListItem.start_time
		currRoadCarList = self.roadCarList[mainListItem.source][mainListItem.destination]   #Type: RoadItem
		currRoadCarList.sort(key = lambda x:x.departure_time, reverse = False)
		
		topInd = len(currRoadCarList)
		for i in range(len(currRoadCarList)):
			if(startTime < currRoadCarList[topInd - 1].departure_time):
			    carAhead = carAhead + 1
			    topInd -= 1
			else:
			    break;
		  
		lastTime = startTime
		ind = topInd
		#print("carAhead = ", carAhead, "lengthCurr= ",len(currRoadCarList), "ind = ", ind)
		while(carAhead>0 and roadLength > 0):
			currTravel = self.calcSpeed(carAhead) * (currRoadCarList[ind].departure_time - lastTime)
			#print("CurrTravel = ", currTravel, "roadLength = ",roadLength, "departure_time =",currRoadCarList[ind].departure_time, "lastTime = ",lastTime)
			if(currTravel <= roadLength):
				roadLength = roadLength - currTravel
				timeTaken = timeTaken + currRoadCarList[ind].departure_time - lastTime
				lastTime = currRoadCarList[ind].departure_time
			else:
				timeTaken = timeTaken + (roadLength/self.calcSpeed(carAhead))
				roadLength = 0
			carAhead-=1;
			ind+=1;
		if(roadLength>0.0):
			timeTaken += roadLength/self.calcSpeed(0)
		return timeTaken
		     	
	def saveTraffic(self):
		self.traffic[:,0] = np.arange(self.traffic.shape[0])
		#print(self.traffic)
		np.savetxt('trafic.csv', self.traffic, '%5.10f', delimiter=',', header='Vehicle, site1,site2,site3,site4,site5')


environment = Environment()
environment.createTrafiicDetail()
environment.saveTraffic()




