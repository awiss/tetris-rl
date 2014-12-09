__author__ = 'Jake Buglione and Alex Wissmann'

from TetroEnv import TetroEnv
from TetroTask import TetroTask
import tetromino4
import time
import sys
from sys import stdout
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer



main = False
# Initialize state space
table = ActionValueTable(2**15, 15)
table.initialize(0.)
print sys.argv
# create learner and agent
alpha = .3
gamma = 0.0
learner = Q(alpha, gamma)
print alpha
print gamma
epsilon = .5
#tetromino4.main()
#main = True
learner._setExplorer(EpsilonGreedyExplorer(epsilon))
agent = LearningAgent(table, learner)
print epsilon
# create environment, task, and experiment
env = TetroEnv(tetromino4.getBlankBoard())
task = TetroTask(env)
experiment = Experiment(task, agent)
#env.setDisplay(True)
# Train the learner
num_iter = 1000
for i in range(num_iter):
    if i % (num_iter/100) == 0:
        stdout.write("\rTraining %d%% complete" % (i * 100 / num_iter))
        stdout.flush()
    if main:
        time.sleep(2)
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()

print "Done Learning"
agent.learning = False
env.setLearning(False)
env.reset()

display = False

print epsilon
while True:
    foo = raw_input('Agent is done training. Enter to test, d then enter to display')
    if foo == "d":
        if main == False:
            tetromino4.main()
            env.setDisplay(True)
            main = True

    env.totallines = 0
    num_iter = 10000
    for i in range(num_iter):
        if main:
            time.sleep(2)
        experiment.doInteractions(1)
        agent.reset()
    print 'Total lines in %d iterations: %d' % (num_iter, env.totallines)


print "Done"

