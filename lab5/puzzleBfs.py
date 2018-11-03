from __future__ import print_function
import numpy as np
import copy
from Queue import Queue
class matrixObj(object):
	def __init__(self, M):
		self.M = M

	def __eq__(self, other):
		n = other.M.shape[0]
		for i in range(n):
			for j in range(n):
				if other.M[i, j] != self.M[i, j]:
					return False
		return True

	def __hash__(self):
		return hash(str(self.M))

class Person(object):
    def __init__(self, name, age):
        self.name, self.age = name, age

action = ["left", "right", "up", "down"]

# class queueNode:
# 	def __init__(self, stateMat, action, emptyBlockPos):
# 		self.stateMat = stateMat
# 		self.prevAction = action
# 		self.emptyBlockPos = emptyBlockPos

q = Queue()
obj = Person("amit", 21)
q.put(obj)
temp = q.get()
print(temp.name, temp.age)
