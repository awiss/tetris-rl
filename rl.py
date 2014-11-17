__author__ = 'Jake Buglione and Alex Wissman'

from pybrain.rl.environments.TetroTask import TetroTask
from pybrain.rl.environments.TetroEnv import TetroEnv
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer

# Initialize state space
table = ActionValueTable(2**15, 16)
table.initialize(0.)

# create learner and agent
learner = Q(.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent = LearningAgent(table, learner)

# create environment, task, and experiment
env = TetroEnv()
task = TetroTask(env)
experiment = Experiment(task, agent)

# Train the learner
While True:
	experiment.doInteractions(1)
	agent.learn()
	agent.reset()
