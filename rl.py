############################################################################
# PyBrain Tutorial "Reinforcement Learning"
#
# Author: Thomas Rueckstiess, ruecksti@in.tum.de
############################################################################

__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

"""
A reinforcement learning (RL) task in pybrain always consists of a few
components that interact with each other: Environment, Agent, Task, and
Experiment. In this tutorial we will go through each of them, create
the instances and explain what they do.
But first of all, we need to import some general packages and the RL
components from PyBrain:
"""

from scipy import * #@UnusedWildImport
import pylab

from pybrain.rl.environments.mazes import Maze, MDPMazeTask
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA #@UnusedImport
from pybrain.rl.experiments import Experiment


"""
For later visualization purposes, we also need to initialize the
plotting engine.
"""

pylab.gray()
pylab.ion()


"""
The Environment is the world, in which the agent acts. It receives input
with the .performAction() method and returns an output with
.getSensors(). All environments in PyBrain are located under
pybrain/rl/environments.
One of these environments is the maze environment, which we will use for
this tutorial. It creates a labyrinth with free fields, walls, and an
goal point. An agent can move over the free fields and needs to find the
goal point. Let's define the maze structure, a simple 2D numpy array, where
1 is a wall and 0 is a free field:
"""
structure = array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]])


environment = Maze(structure, (7, 7))


controller = ActionValueTable(81, 4)
controller.initialize(1.)

learner = Q()
agent = LearningAgent(controller, learner)

task = MDPMazeTask(environment)

experiment = Experiment(task, agent)

while True:
    experiment.doInteractions(100)
    agent.learn()
    agent.reset()

    pylab.pcolor(controller.params.reshape(81,4).max(1).reshape(9,9))
    pylab.draw()

