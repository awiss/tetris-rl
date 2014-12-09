from pybrain.rl.environments.task import Task
import numpy as np
from math import log, ceil

class TetroTask(Task):

    def __init__(self, environment):
        self.env = environment
        self.lastreward = 0
        self.last_val = 0
        self.oldstate = None
        self.newstate = None
        rewards = np.array([0,1,2,3,4,5,6]).reshape(7,1)*np.ones((7,4))
        self.highestRow = None
        self.oldRow = 6

    def performAction(self, action):
        self.env.performAction(action)

    def getObservation(self):
        sensors, self.highestRow = self.env.getSensors()
        self.oldstate = obsToArray(sensors[0])
        return sensors

    def getReward(self):
        old = np.array(self.oldstate[0:-3]).reshape(4, 3)
        rewardData = self.env.rewardData
        new = np.array(rewardData[0:-3]).reshape(4, 3)
        old = (old * np.matrix([1, 2, 4]).reshape(3, 1)).A1
       # print "Old is ", old
       # print "Val is ", sum([val**2 for val in old])
       # print self.last_val
        new = (new * np.matrix([1, 2, 4]).reshape(3, 1)).A1
       # print "New is ", new
       # print "New Val is ", sum([val**2 for val in new]);
        reward = 10 - sum([val**2 for val in new]) + sum([val**2 for val in old])
        self.last_val = sum([val**2 for val in new]);
        cur_reward = self.lastreward
        self.lastreward = reward
        return cur_reward

    def multiReward(self, old, new):
        old = np.array(old)
        new = np.array(new)
        vals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                12, 13, 14, 15, 16, 17, 18, 19, 20]).reshape(20, 1)
        # print old.T
        # print vals
        old = (old.T * vals)

        new = (new.T * vals)
        # print old
        # print np.sum(old)
       # print "New is ", new
       # print "New Val is ", sum([val**2 for val in new]);
        return np.sum(new - old)

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim


def obsToArray(x):
    arr = []
    for i in reversed(range(0, 15)):
        if x >= pow(2, i):
            x -= pow(2, i)
            arr.insert(0, 1)
        else:
            arr.insert(0, 0)
    return arr

def arrayToObs(arr):
    return int(''.join(reversed([str(i) for i in arr])), base=2)

