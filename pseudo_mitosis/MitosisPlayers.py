import math
import numpy as np
import subprocess

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

    def __call__(self, board):
        return self.play(board)

# maximizes move difference, also wins if it can
class GreedyMitosisPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidate = -1
        best_move_diff = -math.inf
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            # simulate the move
            next_board, _ = self.game.getNextState(board, 1, a)
            if self.game.getGameEnded(next_board, 1) == 1:
                return a
            # calculate move difference
            move_diff = self.game.getValidMoves(next_board, 1).sum() - self.game.getValidMoves(next_board, -1).sum()
            if move_diff > best_move_diff:
                best_move_diff = move_diff
                candidate = a
        return candidate

    def __call__(self, board):
        return self.play(board)

class HumanMitosisPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        print ([i for i in range(self.game.getActionSize()) if valid[i] == 1])
        while True:
            input_move = input()
            if input_move.isdigit():
                a = int(input_move)
                if a >= 0 and a < self.game.getActionSize() and valid[a] == 1:
                    break
            print("Invalid move, try again.")
        return a

    def __call__(self, board):
        return self.play(board)