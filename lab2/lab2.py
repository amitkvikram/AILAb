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
    def __init__(self, vehicle_no, arrival_time, departure_time):
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

	def __init__(self, vehicleNo):
		self.vehicleNo = vehicleNo
        # //Initialize mainList
        for i in range(0, time.shape[0]):
            src = vehicle[i,0]
            dest = vehicle[i,1]
            mainList.append(MainListItem(i, timeMat[i, 0], src, dest))
            traffic[:,1] = vehicleMat

	def calcSpeed(self, x):
		return np.exp(.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))

	def createTrafiicDetail():
		while len(mainList)!=0:
			mainList.sort(key = lambda x:x.start_time, reverse = True)
			currObj = mainList.pop()   #Type MainListItem
			currRoadCarList = roadList[currObj.source][currObj.destination]     #Type: RoadItem
			processCurrentVehicle(mainListItem)
                                        
            #push current Car in current roadList
            roadCarList[currObj.source][currObj.destination].append(RoadItem(currObj.start_time + timeTaken))
            
            #update traffic detail
            traffic[currObj.vehicle_no][0] = traffic[currObj.vehicle_no][0].astype(np.int)+1
            rootNumber = output[currObj.vehicle_no][0].astype(np.int)
            traffic[currObj.vehicle_no][ind1 + 1] = currObj.start_time + timeTaken
            
            #Update mainList
            if traffic[currObj.vehicle_no][0] != 4:
                st = currObj.start_time + timeTaken
                mainList.append(mainListItem(currObj.vehicle_no,
                                st[0],
                                currObj.destination,
                                vehicle[currObj.vehicle_no][output[currObj.vehicle_no][0].astype(np.int) + 1]))
   
    def processCurrentVehicle(mainListItem):
        timeTaken = 0;   #final value will be equal to time taken to travel current road
        carAhead = 0;
        roadLength = road[currObj.source, currObj.destination]
        startTime = currObj.start_time
        currRoadCarList = roadList[mainListItem.source][mainListItem.destination]   #Type: RoadItem
        
        topInd = len(currRoadCarList)
        for i in range(len(currRoadCarList)):
            if(start_time < currRoadCarList[topInd - 1].departure_time):
                carAhead = carAhead + 1
                topInd -= 1
            else:
                break;
        
        lastTime = startTime
        ind = 0
        while(carAhead>0 and length > 0):
            currTravel = calcSpeed(tot) * (currRoadCarList[ind].departure_time - last_time)
            if(currTravel >= length):
                length = length - currTravel
                timeTaken = timeTaken + currRoadCarList[ind].departure_time - last_time
                last_time = currRoadCarList[ind].departure_time
            else:
                timeTaken = timeTaken + (length/calcSpeed(tot))
                length = 0
            carAhead-=1;
            ind+=1;
        if(length>0.0):
        timeTaken += length/calcSpeed(0)
    return timeTaken

    def saveTraffic():
    	traffic[:,0] = np.arange(traffic.shape[0])
    	np.savetxt('trafic.csv', trafic, '%5.10f', delimiter=',', header='Vehicle, site1,site2,site3,site4,site5')





