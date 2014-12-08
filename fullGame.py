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
# print sys.argv
# create learner and agent
learner = Q(.3, 0.0)
epsilon = .3
learner._setExplorer(EpsilonGreedyExplorer(epsilon))
agent = LearningAgent(table, learner)
# print epsilon
# create environment, task, and experiment
env = TetroEnv(tetromino4.getBlankBoard())
task = TetroTask(env)
experiment = Experiment(task, agent)
# Train the learner
num_iter = 5000
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
num_itr = 100
while True:
    foo = raw_input('Agent is done training.\nPress ENTER to test. Insert X and press enter to close.\n')

    # New external game code
    if foo is "X":
        print '\n\nExiting...'
        sys.exit(0)
    if main is False:
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
            time.sleep(.5)

            currReward = -10000
# sets the current slice to a blank board
            currSlice = copy.deepcopy(boardSlices[0])
# chooses a piece
            nextPiece = random.choice(pieces)
            pieces.remove(nextPiece)
            if len(pieces) == 0:
                pieces = [0, 1, 2, 3, 4, 5, 6]

# Evaluates each board slice for piece placement
        iters = 0
        # for i in range(7):
        #     print tetromino4.boardToState(boardSlices[i], i)
        # print 'double'
        # for i in range(7):
        #     print tetromino4.boardToState(boardSlices[i], i)
        noTocar = copy.deepcopy(boardSlices)

        # print 'div'

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
                ended = envi.ended
            agent.reset()
            iters += 1
        # updates the large board
        # boardSlices[slyceNum] = newSlice
        for j in range(4):
            board[j + slyceNum] = copy.deepcopy(newSlice[j])
        cnt = 0
        for slyce in boardSlices:
            for k in range(4):
                boardSlices[cnt][k] = copy.deepcopy(board[k + cnt])
            cnt += 1
        # ite = 0
        # for slyce in boardSlices:
        #     boardSlices[ite] = board[0 + ite:3 + ite]
        #     ite += 1
        # print slyceNum
        # print newSlice
        # print board
        tetrominoFull.rlAction(board, nextPiece, score)
        newScore, board = tetrominoFull.removeCompleteLines(board)
        # change slices if board is changed from line removal
        if newScore > 0:
            cnt = 0
            for slyce in boardSlices:
                for k in range(4):
                    boardSlices[cnt][k] = copy.deepcopy(board[k + cnt])
                cnt += 1
        score += newScore
        time.sleep(.1)
        tetrominoFull.rlAction(board, nextPiece, score)
        oldPiece = copy.deepcopy(piece)
        piece = copy.deepcopy(nextPiece)
        # print tetrominoFull.getHighestRow(board)

        # if tetrominoFull.getHighestRow(board) <= 3:
        if ended:
            break
    print 'In %d moves, score: %d' % (i + 1, score)
print "Done"
