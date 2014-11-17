from pybrain.rl.environments.task import Task
import numpy as np


class TetroTask(Task):

    def __init__(self, environment):
        self.env = environment
        self.lastreward = 0
        self.oldstate = np.zeros((7, 3))
        self.newstate = None
        rewards = np.array([0,1,2,3,4,5,6]).reshape(7,1)*np.ones((7,4))
        self.highestRow = None
        self.oldRow = 6

    def performAction(self, action):
        self.env.performAction(action)

    def getObservation(self):
        sensors, self.highestRow = self.env.getSensors()
        self.newstate = sensors
        return sensors

    def getReward(self):
        if self.env.getActionValid():
            old = np.array(self.oldstate[0:-3]).reshape(3, 4)
            new = np.array(self.env.getRewardData(self.highestRow)[0:-3]).reshape(3, 4)
            old = old * np.array([4, 2, 1]).reshape(3, 1)
            new = new * np.array([4, 2, 1]).reshape(3, 1)
            vals = (1 / (np.sum(old, axis=0)+1)) * 7
            reward = np.sum(np.where(old != new, vals, np.zeros((1,4))))

        else:
            reward = -10000
        cur_reward = self.lastreward
        self.lastreward = reward
        print cur_reward
        return cur_reward

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim
