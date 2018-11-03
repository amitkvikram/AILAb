# Name 		: Kuldeep Singh Bhandari
# Roll No.  : 111601009
# Aim  		: With environment "sea", with agent "bunny", help bunny to reach to the shore
# Idea      : The idea is that bunny will assume that he is at position 0 and will move
#             to position 1 and if he is not at shore, he will move to position -1 then
#             he will again check... if he is not at shore, he will move to position 2
#             and so on until he reaches the shore.
# Format   : <bunny's position> <shore's position> 
# Sample Input :
#2 8
# Sample output :
#Current Location, Bunny's Location, Perception, Action, Shore Location
#2 , 0 , False , None, 8
#3 , 1 , False , right, 8
#1 , -1 , False , left, 8
#4 , 2 , False , right, 8
#0 , -2 , False , left, 8
#5 , 3 , False , right, 8
#-1 , -3 , False , left, 8
#6 , 4 , False , right, 8
#-2 , -4 , False , left, 8
#7 , 5 , False , right, 8
#-3 , -5 , False , left, 8
#8 , 6 , True , right, 8
#Bunny reached Shore

class Environment :

	def __init__(self, coord, shore) :
		self.coord = coord
		self.shore = shore

	def updateState(self, move) :
		self.coord += move

	def providePerception(self) :
		return self.coord == self.shore

class Agent :

	def __init__(self) :
		self.move = 0

	def getPerception(self, envObj) :
		return envObj.providePerception()

	def takeAction(self, envObj) :
		if self.move == 0 :
			self.move += 1

		elif self.move < 0 :
			self.move = -(self.move - 1)

		else :
			self.move = -(self.move + 1)

		envObj.updateState(self.move)

[currentPos, shorePos] = list(map(int, input().split()))

agentObj = Agent()
envObj = Environment(currentPos, shorePos)
# print("current position = ", envObj.coord)
# print("shore position = ", envObj.shore)


print("Current Location, Bunny's Location, Perception, Action, Shore Location")
print(envObj.coord ,",", agentObj.move, ",", agentObj.getPerception(envObj), ", None,", envObj.shore)


while(agentObj.getPerception(envObj) == False) :
	
	x = agentObj.getPerception(envObj)
	agentObj.takeAction(envObj)
	print(envObj.coord, ",", (envObj.coord-currentPos) , ",", agentObj.getPerception(envObj), ",", "right,"*(agentObj.move > 0) + "left,"*(agentObj.move < 0), envObj.shore)

print("Bunny reached Shore")