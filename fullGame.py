__author__ = 'Jake Buglione and Alex Wissman'

from TetroEnv import TetroEnv
from TetroTask import TetroTask
import tetromino4
import tetrominoFull
import time
import sys
from sys import stdout
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import SARSA
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
import random



# Initialize state space
table = ActionValueTable(2**15, 15)
table.initialize(0.)
print sys.argv
# create learner and agent
learner = SARSA(.3, 0.0)
epsilon = .3
learner._setExplorer(EpsilonGreedyExplorer(epsilon))
agent = LearningAgent(table, learner)
print epsilon
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
    agent.learn()
    agent.reset()

print "Done Learning"
agent.learning = False
env.setLearning(False)
env.reset()

display = False
main = False

print epsilon
board = tetrominoFull.getBlankBoard()
boardSlices = list()
for i in range(6):
    boardSlices.append(tetromino4.getBlankBoard)
while True:
    foo = raw_input('Agent is done training. Enter to test, d then enter to display')

    # New external game code
    if foo == "d":
        if main == False:
            tetrominoFull.main()
            display = True
            main = True

    env.totallines = 0
    score = 0
    num_iter = 10000
    for i in range(num_iter):
        if main:
            time.sleep(2)

        currReward = 0
        currSlice = boardSlices[0]
        pieces = [0, 1, 2, 3, 4, 5, 6]
        piece = random.choice(pieces)
        iters = 0
        for slyce in boardSlices:
            envi = TetroEnv(slyce)
            exp = Experiment(task, envi)
            exp.doInteractions(1)
            if task.lastreward > currReward:
                currReward = task.lastreward
                slyceNum = iters
                newSlice = envi.board
                newscore = envi.score
            agent.reset()
            iters += 1
        score += newscore
        boardSlices[slyceNum] = newSlice
        board = tetrominoFull.main.board
        board[0 + slyceNum:3 + slyceNum] = newSlice
        tetrominoFull.rlAction(board, piece, self.score)
        if tetrominoFull.getHighestRow(board)<=2:
            break
    print 'Total lines in %d score: %d' % (num_iter, score)


print "Done"

