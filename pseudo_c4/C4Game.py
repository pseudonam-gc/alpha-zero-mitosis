from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .C4Logic import Board
import numpy as np

class C4Game(Game):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return C4Game.square_content[piece]

    def __init__(self, n,m,x):
        # n = rows
        # m = cols 
        # x = number of cells in a row to win
        self.n = n
        self.m = m
        self.x = x

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n, self.m, self.x)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.m)

    def getActionSize(self):
        # return number of actions
        return self.m

    def getNextState(self, board, player, action):
        b = Board(self.n, self.m, self.x)
        b.pieces = np.copy(board)
        b.execute_move(action, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n, self.m, self.x)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        for move in legalMoves:
            valids[move] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost, minor for draw
        if sum(self.getValidMoves(board, player)) == 0:
            return -0.01
        
        b = Board(self.n, self.m, self.x)
        b.pieces = np.copy(board)

        game_ended = b.get_game_ended(board)
        
        return game_ended

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.m)
        assert(board.shape == (self.n, self.m))

        l = []
        """
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()))]"""
        
        l += [(board, pi)]  # no symmetries for now
        l += [(np.fliplr(board), np.flip(pi))]  # horizontal flip
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n, self.m, self.x)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    @staticmethod
    def display(board):
        n, m = board.shape
        print("   ", end="")
        for y in range(m):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(m):
                piece = board[y][x]    # get the piece to print
                print(C4Game.square_content[piece], end=" ")
            print("|")

        print("-----------------------")
