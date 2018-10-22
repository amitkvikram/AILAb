
# coding: utf-8

# #### Cricket Match Problem

# In[22]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[25]:


minNum = -100000
totalBalls = 301
totalWicket = 10
shotToIndex = {1:0, 2:1, 3:2, 4:3, 6:4}
shots = [1, 2, 3, 4, 6]
pw_min = [0.01, 0.02, 0.03, 0.1, 0.3]
pw_max = [0.1, 0.2, 0.3, 0.5, 0.7]
pr_min = 0.5
pr_max = 0.8

def getPr(wicketLeft):
    return pr_min + (pr_max - pr_min)*((wicketLeft - 1)/9)

def getPw(wicketLeft, shot):
    ind = shotToIndex[shot]
    return pw_max[ind] + (pw_min[ind] - pw_max[ind])*((wicketLeft - 1)/9)

Value = np.zeros((totalBalls + 1, totalWicket + 1))   #121, 11
Policy = np.zeros((totalBalls + 1, totalWicket + 1))  #121, 11

for ballLeft in range(1, totalBalls+1):
    for wicketLeft in range(1, totalWicket + 1):
        optimalValue = minNum
        optimalShot = -1
        for shot in shots:
            currValue = 0
            #if player lose wicket
            pw = getPw(wicketLeft, shot)
            currValue += pw*0 + pw*Value[ballLeft - 1, wicketLeft - 1]
            
            #If Player doesn't lose wicket and shot was successful
            pr = getPr(wicketLeft)
            currValue += (1 - pw)*(pr * shot + pr* Value[ballLeft - 1, wicketLeft])
            
            #if player doesn't lose wicket and shot was unsuccessful
            currValue += (1 - pw)*((1 - pr)*(0 + Value[ballLeft - 1, wicketLeft]))
            
            if currValue > optimalValue:
                optimalValue = currValue
                optimalShot = shot
        Policy[ballLeft][wicketLeft] = optimalShot
        Value[ballLeft][wicketLeft] = optimalValue
        
#         print(Value)
        
np.savetxt("policy.txt", Policy, fmt = "%i")
np.savetxt("value.txt", Value, fmt = "%i")

