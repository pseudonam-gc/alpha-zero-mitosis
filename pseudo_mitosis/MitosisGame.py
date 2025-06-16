from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .MitosisLogic import Board
import numpy as np
import torch

class MitosisGame(Game):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return MitosisGame.square_content[piece]

    def __init__(self, n):
        # n = grid size
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)
    
    def getBoardSize(self):
        return (1 + 3 * self.n * (self.n - 1))

    def getActionSize(self):
        # return number of actions
        return 3 * (1 + 3 * self.n * (self.n - 1))

    def getEdgeIndex(self):
        # return all edge indices as a torch tensor
        src = []
        dst = []
        dirs = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]
        b = Board(self.n)
        cell_set = set(b.cells)
        # loop through ALL indices in board
        for (x,y) in b.cells:
            for (dx, dy) in dirs:
                # get the adjacent cell
                adj_x = x + dx
                adj_y = y + dy
                if (adj_x, adj_y) in cell_set:
                    src.append(b.indices[x][y])
                    dst.append(b.indices[adj_x][adj_y])
        # return (np.array(src, dtype=np.int64), np.array(dst, dtype=np.int64))
        # make [2, num_messages] integer tensor 
        return torch.tensor([src, dst], dtype=torch.long)
                

    def getNextState(self, board, player, action):
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.execute_move(action, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        for move in legalMoves:
            valids[move] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.get_game_ended(player)

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        #print (self.getSymmetries(board, [1]*self.getActionSize()))
        b = Board(self.n)
        b.pieces = np.copy(board)
        return player*board

    def rotate60(self, board, pi):
        """Rotate the board 60 degrees clockwise."""
        # Create copy of board and policy vector to rotate
        b = Board(self.n)
        b.pieces = np.copy(board)
        new_board = np.copy(board)
        new_pi = np.copy(pi)

        # Starting from the innermost ring, rotate each ring 60 degrees
        for ring_size in range(1, self.n):

            # starting cell on ring
            curr_cell = (self.n-1-ring_size, self.n-1-ring_size)
            ring_coords = []

            # loop around, change directions every ring_size steps
            for (dx, dy) in [(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]:
                for i in range(ring_size):
                    ring_coords.append(curr_cell)
                    curr_cell = (curr_cell[0] + dx, curr_cell[1] + dy)

            # locate indices in 1D ring array
            ring_indices = [b.indices[coord[0]][coord[1]] for coord in ring_coords]

            # swap cells around the ring
            for i in range(len(ring_indices)):
                new_board[ring_indices[i]] = board[ring_indices[(i - ring_size) % len(ring_indices)]]
                new_pi[ring_indices[i]] = pi[ring_indices[(i - ring_size) % len(ring_indices)]]

        return new_board, new_pi

    def reflectHorizontally(self, board, pi):
        """Reflect the board horizontally."""
        b = Board(self.n)
        b.pieces = np.copy(board)
        new_board = np.copy(board)
        new_pi = np.copy(pi)
        # Loop through rows
        for i in range(0, 2*self.n-1): #2n-1 rows 
            lower_bound = max(0, i-self.n+1)
            upper_bound = min(self.n-1, i)+self.n-1
            # For each row, reverse the order of the pieces
            while lower_bound < upper_bound:
                # swap the two
                left = b.indices[i][lower_bound]
                right = b.indices[i][upper_bound]
                new_board[left], new_board[right] = new_board[right], new_board[left]
                new_pi[left], new_pi[right] = new_pi[right], new_pi[left]
                lower_bound += 1
                upper_bound -= 1
        return new_board, new_pi

    def getSymmetries(self, board, pi):
        l = []
            
        # The board is isomorphic to D6 - 12 symmetries (2 reflections for 6 rotations)
        curr_board = np.copy(board)
        curr_pi = np.copy(pi)
        for i in range(6):
            curr_board, curr_pi = self.rotate60(curr_board, curr_pi)
            l += [(curr_board, curr_pi)]
            # add the reflection
            new_board, new_pi = self.reflectHorizontally(curr_board, curr_pi)
            l += [(new_board, new_pi)]
        
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    @staticmethod
    def display(board):
        # figure out the size of the board
        n = 1
        while n * (n - 1) * 3 + 1 < board.size:
            n += 1
        if n * (n - 1) * 3 + 1 != board.size:
            raise ValueError("Invalid board size")
        print("-----------------------")
        b = Board(n)
        b.pieces = np.copy(board)
        b.display()
        print("-----------------------")
