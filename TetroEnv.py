from pybrain.rl.environments.environment import Environment
from tetromino4 import *
import random
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

    def getSensors(self):
        return boardToState(self.board, self.piece)

    def getActionValid():
        return self.ActionValid

    def performAction(self, action):
        if actionIsValid(self.board, self.piece, action):
            self.ActionValid = True
            [self.board, lines] = addAndClearLines(self.board, self.piece)
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
