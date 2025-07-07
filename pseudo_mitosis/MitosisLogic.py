from collections import defaultdict
from termcolor import colored
import random
import numpy as np
'''
Author: Josiah K
Board class.
Board data:
  1=white, -1=black, 0=empty
  (row,col)
     pieces[1][1] is the square in column 1,
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
class Board():

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # hex board has 1+(6+12...6*(n-1)) pieces
        # = 1+(6*(n)(n-1)/2) = 1+3*n*(n-1)
        # Create the empty board array.
        self.space_count = (1+3*n*(n-1))
        self.hex_pieces = [0] * self.space_count

        """
                (0,0) (0,1) (0,2) (0,3) (0,4)
             (1,0) (1,1) (1,2) (1,3) (1,4) (1,5)
          (2,0) (2,1) (2,2) (2,3) (2,4) (2,5) (2,6)
       (3,0) (3,1) (3,2) (3,3) (3,4) (3,5) (3,6) (3,7)
    (4,0) (4,1) (4,2) (4,3) (4,4) (4,5) (4,6) (4,7) (4,8)
       (5,1) (5,2) (5,3) (5,4) (5,5) (5,6) (5,7) (5,8)
          (6,2) (6,3) (6,4) (6,5) (6,6) (6,7) (6,8)
             (7,3) (7,4) (7,5) (7,6) (7,7) (7,8)
                (8,4) (8,5) (8,6) (8,7) (8,8)
        """

        # two-way mapping between (i,j) and index in piece
        self.cells = []
        self.indices = [[None for i in range(2*n-1)] for i in range(2*n-1)]
        for i in range(0, 2*n-1): #2n-1 rows 
            lower_bound = max(0, i-n+1)
            upper_bound = min(n-1, i)+n-1
            for j in range(lower_bound, upper_bound+1): 
                self.cells.append((i, j))
                self.indices[i][j] = len(self.cells)-1

        self.pieces = self.make_rectangular(self.hex_pieces)

        # adjacent tiles
        self.adj = [(0, 1), (1, 0), (1, 1)]

        if n == 5:
            # set up the starting cells 
            p1_cells = [(2,2),(6,4),(4,6)]
            p2_cells = [(2,4),(6,6),(4,2)]
        else:
            p1_cells = [(1, 1)]
            p2_cells = [(2*n-3, 2*n-3)]
        for cell in p1_cells:
            index = self.indices[cell[0]][cell[1]]
            self.hex_pieces[index] = 1
        for cell in p2_cells:
            index = self.indices[cell[0]][cell[1]]
            self.hex_pieces[index] = -1

    def reset(self):
        """Reset the board to the initial state."""
        self.hex_pieces = [None]*self.space_count
        self.hex_pieces = [0] * self.space_count
        self.pieces = self.make_rectangular(self.hex_pieces)

    def set_pieces(self, pieces):
        """Set the pieces on the board."""
        #assert len(pieces) == self.space_count, \
            #"Pieces must be of length {}".format(self.space_count)
        self.hex_pieces = pieces
        self.pieces = self.make_rectangular(self.hex_pieces)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        # TODO: make self.pieces
        return self.hex_pieces[index]

    def _action_cells(self, space, dir):
        """Find the two cells corresponding to the given move.
        Outputs the forward and back cells as (x,y) tuples."""
        forward = (self.cells[space][0] + self.adj[dir][0],
                   self.cells[space][1] + self.adj[dir][1])
        back = (self.cells[space][0] - self.adj[dir][0],
                self.cells[space][1] - self.adj[dir][1])
        if 0 <= forward[0] < 2*self.n-1 and \
                0 <= forward[1] < 2*self.n-1:
            if 0 <= back[0] < 2*self.n-1 and \
                    0 <= back[1] < 2*self.n-1:
                if self.indices[forward[0]][forward[1]] is not None and \
                        self.indices[back[0]][back[1]] is not None:
                    # return the indices of the forward and back cells    
                    return forward, back
        return None, None # invalid move

    def is_move_legal(self, space, dir, color):
        """Check if the move is legal."""
        # Check if the starting cell is the same color as the player
        #print (space, self.hex_pieces[space], color)
        #print (space, dir, colored)
        if self.hex_pieces[space] != color:
            return False
        # Check if the move creates new tiles on only valid spaces
        forward, back = self._action_cells(space, dir)
        if forward is None or back is None:
            return False
        forward = self.indices[forward[0]][forward[1]]
        back = self.indices[back[0]][back[1]]
        # Check if both tiles are empty
        if self.hex_pieces[forward] != 0 or self.hex_pieces[back] != 0:
            return False
        return True

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = []  # stores the legal moves.

        # Loops through all moves
        for space in range(self.space_count):
            for dir in range(3):
                if self.is_move_legal(space, dir, color):
                    moves.append(space * 3 + dir)
        return list(moves)

    def has_legal_moves(self, color):
        return (self.get_legal_moves(color) != [])
    
    def get_game_ended(self, color):
        """If a player has no legal moves ON THEIR TURN, they lose."""
                
        if not self.has_legal_moves(color):
            return -color
        return 0
    
        # other variant
        #if not self.has_legal_moves(color):
            #return 0.01
        # otherwise return the player controlling most of the board corners
        # that is, (0,0), (0,2), (2,4), (4,4), (4,2), (2,0)
        corners = [(0, 0), (0, 3), (3, 6), (6, 6), (6, 3), (3, 0)]
        p1_corners = 0
        p2_corners = 0
        for corner in corners:
            index = self.indices[corner[0]][corner[1]]
            if self.hex_pieces[index] == 1:
                p1_corners += 1
            elif self.hex_pieces[index] == -1:
                p2_corners += 1
        if p1_corners >= 3:
            return 1
        elif p2_corners >= 3:
            return -1

        return 0
    
    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color of the piece to play (1=white,-1=black)
        """
        try:
            assert self.is_move_legal(move // 3, move % 3, color), \
                "Illegal move: {} for color {}".format(move, color)
        except:
            # display board
            print("Illegal move: {} for color {}".format(move, color))
            self.display_indices()
        forward, back = self._action_cells(move // 3, move % 3)
        forward = self.indices[forward[0]][forward[1]]
        back = self.indices[back[0]][back[1]]
        self.hex_pieces[forward] = color
        self.hex_pieces[back] = color
        self.hex_pieces[move//3] = 0
        self.pieces = self.make_rectangular(self.hex_pieces)
        # display rect board
        
    def make_rectangular(self, hex_pieces=None):
        if hex_pieces is None:
            hex_pieces = self.hex_pieces
        grid_x = (4*self.n-3)
        grid_y = (2*self.n-1)
        new_board = [0] * (grid_x * grid_y)
        # loop through the piece coordinates
        for (x, y) in self.cells:
            value = hex_pieces[self.indices[x][y]]
            new_board[x*grid_x + 2*y + (self.n-1-x)] = value
        return np.array(new_board)

    def display(self, hex_pieces=None):
        if hex_pieces is None:
            hex_pieces = self.hex_pieces
        # display the hex grid
        ind = 0
        piece_symbols = {0: ".", 1: colored("O", "red"), -1: colored("X", "blue")}
        for i in range(0, 2*self.n-1): #2n-1 rows 
            lower_bound = max(0, i-self.n+1)
            upper_bound = min(self.n-1, i)+self.n-1
            row = ""
            for j in range(lower_bound, upper_bound+1): 
                row += piece_symbols[hex_pieces[ind]] + " "
                ind += 1
            # add space to left of row
            print(" " * (abs(self.n-1-i)) + row)

    def display_indices(self):
        # display the hex grid with indices
        ind = 0
        for i in range(0, 2*self.n-1):
            lower_bound = max(0, i-self.n+1)
            upper_bound = min(self.n-1, i)+self.n-1
            row = ""
            for j in range(lower_bound, upper_bound+1):
                if len(str(self.indices[i][j])) == 1:
                    row += str(self.indices[i][j]) + "   "
                else:
                    row += str(self.indices[i][j]) + "  "
                ind += 1
            # add space to left of row
            print("  " * (abs(self.n-1-i)) + row)
    
    def display_rectangular(self, hex_pieces=None):
        # display the rectangular board
        b = self.make_rectangular(hex_pieces)
        x = (4*self.n-3)
        y = (2*self.n-1)
        ind = 0
        piece_symbols = {0: ".", 1: colored("O", "red"), -1: colored("X", "blue")}
        for i in range(0, y):
            row = ""
            for j in range(0, x):
                row += piece_symbols[b[ind]] + " "
                ind += 1
            print(row)  

    def random_fill(self):
        """Randomly fill the board with pieces."""
        for i in range(self.space_count):
            if random.random() < 0.5:
                self.hex_pieces[i] = 1
            else:
                self.hex_pieces[i] = -1