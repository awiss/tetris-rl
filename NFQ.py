__author__ = 'Jake Buglione and Alex Wissman'

from TetroEnv import TetroEnv
from TetroTask import TetroTask
import tetromino4
import time
import sys
from sys import stdout
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import BoltzmannExplorer



# Initialize state space
table = ActionValueNetwork(2**12, 15)
table.initialize(0.)
print sys.argv
# create learner and agent
learner = NFQ()
learner.explorer.epsilon = .3
agent = LearningAgent(table, learner)
# create environment, task, and experiment
env = TetroEnv(tetromino4.getBlankBoard())
task = TetroTask(env)
experiment = Experiment(task, agent)
# Train the learner
num_iter = 10000
for i in range(num_iter):
    if i % (num_iter/100) == 0:
        stdout.write("\rTraining %d%% complete" % (i * 100 / num_iter))
        stdout.flush()
 
    experiment.doInteractions(1)
    agent.learn(1)
    agent.reset()

print "Done Learning"
agent.learning = False
env.setLearning(False)
env.reset()

display = False
main = False

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

