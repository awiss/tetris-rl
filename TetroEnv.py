from pybrain.rl.environments.environment import Environment
from tetromino4 import *
import random
class TeteroEnv(Environment):
    # number of actions
    indim = 16
    # number of states output by sensor
    outdim = 2**15

    def __init__(self):
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.piece = random.choice(self.pieces)

    def getSensors(self):
        return boardToState(self.board, piece)

    def performAction(self, action):

        [self.board, lines] = addAndClearLines(self.board, self.piece)
        if len(self.pieces) == 1:
            self.piece = self.pieces[0]
            self.pieces = [0, 1, 2, 3, 4, 5, 6]
        else:
            self.piece = random.choice(self.pieces)
            self.pieces.remove(self.piece)

    def reset(self):
        self.board = getBlankBoard()
        self.pieces = [0, 1, 2, 3, 4, 5, 6]
        self.piece = random.choice(self.pieces)
