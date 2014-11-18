__author__ = 'Jake Buglione and Alex Wissman'

from TetroEnv import TetroEnv
from TetroTask import TetroTask
import tetromino4
import time
from sys import stdout
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer



# Initialize state space
table = ActionValueTable(2**15, 15)
table.initialize(0.)

# create learner and agent
learner = Q(.3, 0.0)
epsilon = .5
learner._setExplorer(EpsilonGreedyExplorer(epsilon))
agent = LearningAgent(table, learner)
print epsilon
# create environment, task, and experiment
env = TetroEnv()
task = TetroTask(env)
experiment = Experiment(task, agent)
# Train the learner
num_iter = 500000
for i in range(num_iter):
    if i % (num_iter/100) == 0:
        stdout.write("\rTraining %d%% complete" % (i * 100 / num_iter))
        stdout.flush()
 
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()

print "Done Learning"
agent.learning = False
env.setLearning(False)
env.reset()
tetromino4.main()

print epsilon
while True:
    foo = raw_input('Agent is done training. Press any key to test...')
    env.totallines = 0
    num_iter = 500
    for i in range(num_iter):
        time.sleep(.4)
        experiment.doInteractions(1)
        agent.reset()
    print 'Total lines in %d iterations: %d' % (num_iter, env.totallines)


print "Done"

