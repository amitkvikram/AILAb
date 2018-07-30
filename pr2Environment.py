import queue

class bunnyState:
	def __init__(self, currentPosition, left, right):
		self.currentPosition = currentPosition;
		self.lastLeft = left;
		self.lastRight = right;
		self.lastMove = "none"

# Environment
class Environment:

	def __init__(self, shoreCoordinate):
		self.state = bunnyState(-10, -10, -10);                     #False, if bunny is in sea And True, if bunny is on ground
		self.shoreCoordinate = shoreCoordinate;
		self.bunnyOnShore = False

	def updateState(self, action):
		if(action == "left"):
			self.state.lastRight = self.state.currentPosition;
			self.state.currentPosition = self.state.lastLeft - 1;
		elif(action == "right"):
			self.state.lastLeft = self.state.currentPosition
			self.state.currentPosition = self.state.lastRight + 1;

		if(self.state.currentPosition >= self.shoreCoordinate):
			self.bunnyOnShore = True;

	def providePercept(self):
		return self.bunnyOnShore;


#Agent
class Bunny:

	def __init__(self, step):
		self.state = bunnyState(0, 0, 0);
		self.step = step

	def queryForPercept(self, environmentObj):
		return environmentObj.providePercept();

	def takeAction(self, action):
		if(action == "left"):
			self.state.lastRight = self.state.currentPosition;
			self.state.lastMove = "left"
			self.state.currentPosition = self.state.lastLeft - 1;
		elif(action == "right"):
			self.state.lastLeft = self.state.currentPosition;
			self.state.lastMove = "right"
			self.state.currentPosition = self.state.lastRight + 1;


bunny = Bunny(1)
environment = Environment(0)

print("Current Location w.r.t Bunny "  + "Bunny's state", "  Percept" + "  action", "   Current Location w.r.t Environment")

while(bunny.queryForPercept(environment) == False):
	if(bunny.state.lastMove == "right" or bunny.state.lastMove == "none"):
		print(str(bunny.state.currentPosition) + "  " + str(bunny.state.lastMove) + "  " + str(bunny.queryForPercept(environment)) + "  " + "left  " + str(environment.state.currentPosition))
		environment.updateState("left");
		bunny.takeAction("left")

	else:
		print(str(bunny.state.currentPosition) + "  " + str(bunny.state.lastMove) + "  " + str(bunny.queryForPercept(environment)) + "  " + "right  " + str(environment.state.currentPosition))
		environment.updateState("right")
		bunny.takeAction("right")

print(str(bunny.state.currentPosition) + " " + str(bunny.state.lastMove) + " " + str(bunny.queryForPercept(environment)) + " " + "none  " + str(environment.state.currentPosition))
print("\nReached at Shore");

