from pybrain.rl.environments.environment import Environment
from tetromino4 import *
import random
import numpy as np
class TetroEnv(Environment):
    # number of actions
    indim = 15
    # number of states output by sensor
    outdim = 2**15

    def __init__(self):
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.piece = random.choice(self.pieces)
        self.ActionValid = True
        self.highestRow = None

    def getSensors(self):

        bin_state_arr, highestRow = boardToState(self.board, self.piece)
        print highestRow
        if highestRow <= 2:
            self.reset()
            bin_state_arr, highestRow = boardToState(self.board, self.piece)
        convstate = sum(np.array(bin_state_arr)*np.array([0, 1, 2, 2**2, 2**4,
                        2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12,
                        2**13, 2**14]))
        self.highestRow = highestRow
        return [int(convstate)]

    def getRewardData(self, highestRow):
        board, highestRow = boardToState(self.board, self.piece, highestRow)
        return board

    def getActionValid(self):
        return self.ActionValid

    def getHighestRow(self):
        return self.highestRow

    def performAction(self, action):
        action = int(action[0])
        if actionIsValid(action, self.piece, self.board):
            self.ActionValid = True
            lines = addAndClearLines(self.board, action, self.piece)
            if len(self.pieces) == 1:
                self.piece = self.pieces[0]
                self.pieces = [0, 1, 2, 3, 4, 5, 6]
            else:
                self.piece = random.choice(self.pieces)
                self.pieces.remove(self.piece)
        else:
            self.ActionValid = False

    def reset(self):
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.piece = random.choice(self.pieces)
