from pybrain.rl.environments.task import Task
import numpy as np


class TetroTask(Task):

    def __init__(self, environment):
        self.env = environment
        self.lastreward = 0
        rewards = np.array([0,1,2,3,4,5,6]).reshape(7,1)*np.ones((7,4))

    def performAction(self, action):
        self.env.performAction(action)

    def getObservation(self):
        sensors = self.env.getSensors()
        return sensors

    def getReward(self):
        reward = np.sum(np.abs(newstate - oldstate) * self.rewards)
        cur_reward = self.lastreward
        self.lastreward = reward
        return cur_reward

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim