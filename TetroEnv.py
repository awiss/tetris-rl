from pybrain.rl.environments.environment import Environment
from tetromino4 import *
import random
from TetroTask import arrayToObs
import numpy as np


class TetroEnv(Environment):
    # number of actions
    indim = 15
    # number of states output by sensor
    outdim = 2**15

    def __init__(self):
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.piece = 0
        self.ActionValid = True
        self.highestRow = None
        self.rewardData = None
        self.num_resets = 0
        self.totallines = 0
        self.score = 0
        self.display = False
        self.curr_learning = True
        self.ended = False
        self.getNewPiece()

    def getSensors(self):

        bin_state_arr, highestRow = boardToState(self.board, self.piece)
        convstate = arrayToObs(bin_state_arr)
        self.highestRow = highestRow
        return [int(convstate)], highestRow

    def getRewardData(self, highestRow):
        board, highestRow = boardToState(self.board, self.piece, highestRow)
        return board

    def getActionValid(self):
        return self.ActionValid

    def setLearning(self, flag):
        self.curr_learning = flag

    def getHighestRow(self):
        return self.highestRow
    
    def setDisplay(self, disp):
        self.display = disp

    def performAction(self, action):
        self.ended = False
        action = int(action[0])
        #print "action", action
        while not actionIsValid(action, self.piece, self.board):
            action = (action + 1) % 16

        highestRow = getHighestRow(self.board)
        self.score += addAndClearLines(self.board, action, self.piece, self.curr_learning)
        self.getNewPiece()
        self.rewardData, _ = boardToState(self.board, self.piece, highestRow)
        new_highestRow = getHighestRow(self.board)
        if new_highestRow <= 2:
            self.ended = True
            self.reset()

        if self.display:
            rlAction(self.board, self.piece, self.score)

    def getNewPiece(self):

        if len(self.pieces) == 1:
            self.piece_piece = self.pieces[0]
            self.pieces = [0, 1, 2, 3, 4, 5, 6]
        else:
            self.piece = random.choice(self.pieces)
            self.pieces.remove(self.piece)


    def reset(self):
        self.totallines += self.score
        self.score = 0
        self.num_resets += 1
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.getNewPiece()
