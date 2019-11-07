
from __future__ import print_function
import numpy as np
import itertools
import random
import time

## QUIZ: 02
## Problem Name: Optimal Bowling First Strategy
## Name: Amit Vikram Singh
#
# Logic: State is a function of (overLeft, wicketLeft, bowler1QuotaLeft, bowler2QuotaLeft, bowler3QuotaLeft, bowler4QuotaLeft, bowler5QuotaLeft).
#        Problem is solved using bottom-up dynamic programming, because we know the value(run scored) for terminal states where terminal state is 
#        defined as state is which any one of overLeft, wicketLeft, bowler1QuotaLeft, bowler2QuotaLeft, bowler3QuotaLeft, bowler4QuotaLeft, bowler5QuotaLeft
#        is 0.
#       
#        We iterate over all the state and choose optimal action and then update the polic and value function.
#        
#        Command: python2 quiz2.py >a.txt
##





economy = [3, 3.5, 4, 4.5, 5]
strike = [33, 30, 24, 18, 15]

def probWicket(player):
    return 6.0/strike[player]

minNum = -100000
maxNum = 1000000
totalOver = 10
totalBalls = 60
totalWicket = 3

gridSize = (11, 4, 3, 3, 3, 3, 3)
value = np.zeros(gridSize)
policy = np.ones(gridSize, dtype = np.int8)*-2

actionSet = [0, 1, 2, 3, 4]
b = [0, 1, 2]

for overLeft in range(1, 11):
    for wicketLeft in range(1, 4):
        for(b1, b2, b3, b4, b5) in itertools.product(b, b, b, b , b):
                            optimalValue = maxNum
                            currState = (overLeft, wicketLeft, b1, b2, b3, b4, b5)
                            for action in actionSet:
                                if(currState[2+action] == 0):
                                    continue
                                currVal = economy[action]
                                nextState = [overLeft - 1, wicketLeft -1 , b1, b2, b3, b4, b5]
                                nextState[action+2] -=  1
                                currVal += probWicket(action)*(value[nextState[0], nextState[1], nextState[2],
                                 nextState[3], nextState[4], nextState[5], nextState[6]])

                                #If wicket doesn't fall
                                nextState[1]+=1
                                currVal += (1 - probWicket(action)) * (value[nextState[0], nextState[1], nextState[2],
                                 nextState[3], nextState[4], nextState[5], nextState[6]])

                                if currVal < optimalValue:
                                    optimalValue = currVal
                                    policy[currState] = action

                            if(optimalValue != maxNum): value[currState] = optimalValue
                            else: value[currState] = 0


# print("=============Policy===============")
# print("(overLeft, wicketLeft, b1OverLeft, b2OverLeft, b3OverLeft, b4OverLeft, b5OverLeft) |  Bowler")
# for overLeft in range(1, 11):
#     for wicketLeft in range(1, 4):
#         for(b1, b2, b3, b4, b5) in itertools.product(b, b, b, b , b):
#             currState = (overLeft, wicketLeft, b1, b2, b3, b4, b5)
#             print(currState, "Bowler = ", policy[currState] + 1, "Value = {0:.2f}".format(value[currState]))
            # print("OverLeft =", currState[0], "WicketLeft = ", currState[1], 
            #     "Bowler1Quota = ", currState[2], "Bowler2Quota = ", currState[3], "Bowler3Quota = ", currState[4]
            #     ,"Bowler4Quota = ", currState[5], "Bowler5Quota = ", currState[6], "Bowler = ", policy[currState] + 1, "Value = ", value[currState])

def isTerminalState(wicketLeft, overLeft):
    if(wicketLeft <= 0 or overLeft <=0):
        return True
    else:
        return False

print("======Simulating Match============")
bowlerQuota = [2, 2, 2, 2, 2]
overLeft = 10
wicketLeft = 3
runScored = 0

def gotWicket(bowler):
    # print(int(time.time()))
    print("Seed = ", np.random.randint(1, int(time.time())))
    np.random.seed(np.random.randint(int(time.time())))
    prob = probWicket(bowler)
    randNum = np.random.rand()
    print("prob = ", prob)
    print("randomNumber = ", randNum)
    return randNum < prob

while(not isTerminalState(wicketLeft, overLeft)):
    currState = (overLeft, wicketLeft, bowlerQuota[0], bowlerQuota[1], bowlerQuota[2], bowlerQuota[3], bowlerQuota[4])
    bowler = policy[currState]
    print("over = ", 11 - overLeft, "wicket = ", 3 - wicketLeft, "bowler = ", bowler+1)

    if(gotWicket(bowler)):
        wicketLeft -= 1

    overLeft-=1

    bowlerQuota[bowler] -= 1

    runScored+=economy[bowler]

print("Run Scored = ", runScored)





        
# np.savetxt("policy.txt", Policy, fmt = "%i")
# np.savetxt("value.txt", Value, fmt = "%i")
