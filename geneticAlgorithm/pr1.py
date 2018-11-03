#--------------------------LOGIC---------------
# 
#
#
#

import copy
import numpy as np
from Queue import PriorityQueue
targetString = "amitlovesgeneticalgorithm"

class People:
	def __init__(self, str):
		self.str = str

	def __cmp__(self, other):
		target = People(targetString)
		return cmp(s(self, target), s(other, target))

	def __len__(self):
		return len(self.str)

	def __eq__(self, other):
		# print("equal called")
		return self.str == other.str



target = People("amitlovesgeneticalgorithm")
population = []
poolsize = 100
numPeople = 2

## L2 distance between str1 and str2
def s(people1, people2):
	# print(type(people1))
	a = 0
	str1, str2 = people1.str, people2.str
	for i in range(len(str1)):
		a+=((ord(str1[i]) - ord(str2[i])) **2)
	
	return np.sqrt(a)
	
#if target string is found in population the return iindex of target string in poulation
#... else returns -1
def foundGoal():
	print("foundGoal ")
	for i in range(len(population)):
		if((population[i] == target)):
			return i
	return -1
	
#take target string and return random string of same length as target string
def getRandomString(target):
	s = ""
	for i in range(len(target)):
		num = np.random.randint(ord('a'), ord('z') + 1)
		s+= chr(num)
	
	return s
	
#initialize population with random string
def initializePopulation():
	for i in range(numPeople):	population.append(People(getRandomString(target)))
	
	
#Mutation: takes a string and changes one character of it randomly
def mutation(str1):
	r_ind = np.random.randint(len(str1))
	r_char = chr(np.random.randint(ord('a'), ord('z') + 1))
	
	sList = list(str1)
	sList[r_ind] = r_char
	return ''.join(sList)
	
#Takes list of string and returns fittest one(returns People(class) List)
def selection(stringList, num = 2):
	# print("==========selection===============")
	# print(stringList)
	q = PriorityQueue()
	for x in stringList:
		# print("s = ", s(People(x), target))
		q.put(People(x))

	retList = []
	for _ in range(num):
		if(q.empty()):
			break
		fittest = q.get()
		retList.append(fittest)
		# print("fittest = ", s(fittest, target))
	
	# print("return = ", retList)		
	return retList
	
def doCrossOver():
	return np.random.rand() > 0.5
	
def doMutation():
	return np.random.rand() > 0.5

#One point Crossover, takes a string and returns two string by doing crossover	
def crossOver(str1, str2):
	ind = np.random.randint(len(str1))
	offSpring1 = str1[:ind] + str2[ind:]
	offSpring2 = str2[:ind] + str1[ind:]
	
	return offSpring1, offSpring2

#Main function which takes two People s1 and s2 then perfoms crossover, mutation and returns
#.... two offspring
def v(s1, s2):
	s1, s2 = s1.str, s2.str
	if(doCrossOver()): s1, s2 = crossOver(s1, s2)
	offSpringList1 = []
	offSpringList2 = []
	
	for i in range(poolsize):
		#Pool1
		if(doMutation()):
			offSpringList1.append(mutation(s1))
		else: 
			offSpringList1.append(s1)
		
		#Pool2
		if(doMutation()):
			offSpringList2.append(mutation(s2))
		else: 
			offSpringList2.append(s2)
			
		#Selection
	return selection(offSpringList1 + offSpringList2)
		
def geneticAlgorithm():
	initializePopulation()
	iter = 0
	while(foundGoal() == -1 and iter < 1000):
		parent1, parent2 = np.random.randint(0, numPeople, size = (2))
		print(population[parent1].str, population[parent2].str)
		[population[parent1], population[parent2]] = v(population[parent1], population[parent2])
		iter+=1
		
	print("Found Goal in iteration = " , iter, "Goal = ", population[foundGoal()].str)
	

##CHECK
geneticAlgorithm()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


