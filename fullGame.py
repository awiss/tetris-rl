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
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
import random
import copy


# Initialize state space
table = ActionValueTable(2**15, 15)
table.initialize(0.)
print sys.argv
# create learner and agent
learner = Q(.3, 0.0)
epsilon = .3
learner._setExplorer(EpsilonGreedyExplorer(epsilon))
agent = LearningAgent(table, learner)
print epsilon
# create environment, task, and experiment
env = TetroEnv(tetromino4.getBlankBoard())
task = TetroTask(env)
experiment = Experiment(task, agent)
# Train the learner
num_iter = 1000000
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

while True:
    foo = raw_input('Agent is done training. Enter to test, d then enter to display')

    # New external game code
    if foo == "d":
        if main == False:
            tetrominoFull.main()
            display = True
            main = True

    # gets full sized blank board
    board = tetrominoFull.getBlankBoard()

    # makes a list filled with small empty game boards
    boardSlices = list()
    for i in range(7):
        boardSlices.append(tetromino4.getBlankBoard())
    # gets first piece
    pieces = [0, 1, 2, 3, 4, 5, 6]
    piece = random.choice(pieces)
    oldPiece = piece

    # sets score to zero
    score = 0
    num_iter = 10000
    for i in range(num_iter):
        if main:
            time.sleep(2)


        currReward = -10000
# sets the current slice to a blank board
        currSlice = copy.deepcopy(boardSlices[0])
# chooses a piece
        pieces = [0, 1, 2, 3, 4, 5, 6]
        nextPiece = random.choice(pieces)

# Evaluates each board slice for piece placement
        iters = 0
        # for i in range(7):
        #     print tetromino4.boardToState(boardSlices[i], i)
        # print 'double'
        # for i in range(7):
        #     print tetromino4.boardToState(boardSlices[i], i)
        noTocar = copy.deepcopy(boardSlices)

        print 'div'

        # for i in range(7):
        #     envi = TetroEnv(boardSlices[iters])
        #     envi.totallines = 0
        #     task = TetroTask(envi)
        #     envi.piece = piece
        #     exp = Experiment(task, agent)
        #     exp.doInteractions(1)
        #     print tetromino4.boardToState(noTocar[i], i)

        for slyce in boardSlices:
            envi = TetroEnv(boardSlices[iters])
            envi.totallines = 0
            task = TetroTask(envi)
            envi.piece = piece
            exp = Experiment(task, agent)
            exp.doInteractions(1)
            # picks the slice with the best reward
            # print iters
            # print tetromino4.boardToState(boardSlices[iters], iters)
            # print tetromino4.boardToState(envi.board, 1)
            # print 'reward', task.multiReward(tetromino4.boardToState(noTocar[iters], 1),
            #                                  tetromino4.boardToState(envi.board, 1))
            if task.getReward() > currReward:
                currReward = task.getReward()
                slyceNum = iters
                newSlice = copy.deepcopy(envi.board)
                newscore = envi.score
            agent.reset()
            iters += 1
        # updates the score and large board
        score += newscore
        # boardSlices[slyceNum] = newSlice
        for i in range(4):
            board[i + slyceNum] = copy.deepcopy(newSlice[i])
        cnt = 0
        for slyce in boardSlices:
            for i in range(4):
                boardSlices[cnt][i] = copy.deepcopy(board[i + cnt])
            cnt += 1
        # ite = 0
        # for slyce in boardSlices:
        #     boardSlices[ite] = board[0 + ite:3 + ite]
        #     ite += 1
        # print slyceNum
        # print newSlice
        # print board
        tetrominoFull.rlAction(board, nextPiece, score)
        score2, board = tetrominoFull.removeCompleteLines(board)
        time.sleep(1)
        tetrominoFull.rlAction(board, nextPiece, score)
        oldPiece = copy.deepcopy(piece)
        piece = copy.deepcopy(nextPiece)
        if tetrominoFull.getHighestRow(board)<=2:
            break
    print 'Total lines in %d score: %d' % (num_iter, score)


print "Done"

