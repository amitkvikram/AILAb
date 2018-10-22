#LOGIC
# Initially choose k numbers between -10 and 10
# While function doesn't converge choose two numbers from population and pass it to function v
# convert number to binary do cross over, mutation and selction 

import copy
import numpy as np
from heapq import nlargest
target = "amitlovesgeneticalgorithm"
population = []
poolsize = 5
numPeople = 2
numBits = 3

def func1(num):
	return num**2
	
def func2(num):
	return (num - 2)**2

def s(str1):
	#print("str1 = ", str1)
	num1 = int(str1, 2)
	return (func1(num1)**2 + func2(num1)**2)**(1/2)
	
def foundGoal():
	for i in range(len(population)):
		if((population[i] == target)):
			return i
	return -1

def intToBinary(num):
	binary = bin(num)
	s = ""
	if(binary[0] == '-'):
		s +="-"
	
	temp = binary.split('b')[1]

	for i in range(4 - len(temp)):
		s+='0'

	s = s+temp

	return s

def binaryToInt(binary):
	return int(binary, 2)

def isNegative(binary):
	return binary[0] == '-'

def getPositive(binary):
	if(isNegative(binary)):
		return binary[1:]
	else: return binary

def getRandomNumber():
	s = ""
	num = np.random.randint(-10, 11)
	return num
	
def initializePopulation():
	for i in range(numPeople):	population.append(getRandomNumber())
	
	
def mutation(num):

	binary = intToBinary(num)
	r_ind = np.random.randint(len(binary))
	r_char = str(np.random.randint(0, 2))
	
	sList = list(str1)
	sList[r_ind] = r_char
	binary = ''.join(sList)
	return binaryToInt(binary)
	
#Takes two string and returns fittest one
def selection(stringList):
	minIndex = -1
	minDist = 100000000
	for i in range(len(stringList)):
		currDist = s(stringList[i])
		if(currDist < minDist):
			minDist = currDist
			minIndex = i
	print("ss = ", nlargest(2, stringList))
	return nlargest(2, stringList)
	#return stringList[minIndex]
	
def doCrossOver():
	return np.random.rand() > 0.5
	
def doMutation():
	return np.random.rand() > 0.5

#One point Crossover	
def crossOver(num1, num2):
	binary1 = intToBinary(num1)
	binary2 = intToBinary(num2)
	print("binary1 = ", binary1, binary2)
	ind = np.random.randint(len(binary1))

	binary1_1 = getPositive(binary1)
	binary2_1 = getPositive(binary2)

	offSpring1 = binary1_1[:ind] + binary2_1[ind:]
	offSpring2 = binary2_1[:ind] + binary1_1[ind:]
	if(isNegative(binary1)):
		offSpring1 = '-'+offSpring1

	if(isNegative(binary2)):
		offSpring2 = "-" + offSpring2
	print(offSpring1, offSpring2)
	return binaryToInt(offSpring1), binaryToInt(offSpring2)
	
def v(s1, s2):
	p1, p2 = s1, s2
	s1 = bin(s1).split('b')[1]
	s2 = bin(s2).split('b')[1]
	if(len(s1) < 4):
		s1 = "0"*(4-len(s1))+s1
	if(len(s2) < 4):
		s2 = "0"*(4-len(s2))+s2
	print("s1 = ", s1, s2)
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
	offSpringList1.append(p1)
	offSpringList1+=offSpringList2
	offSpringList1.append(p2)
	return selection(offSpringList1)
		
def geneticAlgorithm():
	initializePopulation()
	print(population)
	parent1 = 0
	parent2 = 1
	iter = 0
	while(iter < 10000):
		#parent1, parent2 = np.random.randint(0, numPeople, size = (2))
		print(parent1, parent2)
		print(population[parent1], population[parent2])
		[population[parent1], population[parent2]] = v(population[parent1], population[parent2])
		iter+=1
		
	print("Found Goal in iteration = " , iter, "Goal = ", int(population[parent1], 2), int(population[parent2], 2))
	

##CHECK
# geneticAlgorithm()
print(crossOver(-2, -10))

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


