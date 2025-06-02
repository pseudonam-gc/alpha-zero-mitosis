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

# if it sees the win it will take the win
class GreedyC4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            # simulate the move
            next_board, _ = self.game.getNextState(board, 1, a)
            if self.game.getGameEnded(next_board, 1) == 1:
                return a
            candidates.append(a)
        candidates.sort()
        return np.random.choice(candidates)

    def __call__(self, board):
        return self.play(board)

# doesn't let the opponent win in one
class GreedyV2C4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        non_losing_candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            # simulate the move
            next_board, _ = self.game.getNextState(board, 1, a)
            if self.game.getGameEnded(next_board, 1) == 1:
                return a
            
            for a2 in range(self.game.getActionSize()):
                if a2 == a or valids[a2] == 0:
                    continue
                next_board2, _ = self.game.getNextState(next_board, -1, a2)
                if self.game.getGameEnded(next_board2, -1) == -1:
                    break
            else:
                non_losing_candidates.append(a)
            candidates.append(a)
        candidates.sort()
        non_losing_candidates.sort()

        if len(non_losing_candidates) > 0:
            return np.random.choice(non_losing_candidates)
        return np.random.choice(candidates)

    def __call__(self, board):
        return self.play(board)

class HumanC4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
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