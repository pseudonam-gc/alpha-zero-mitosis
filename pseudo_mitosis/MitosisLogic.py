from collections import defaultdict
from termcolor import colored
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
        self.pieces = [0] * self.space_count

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
            self.pieces[index] = 1
        for cell in p2_cells:
            index = self.indices[cell[0]][cell[1]]
            self.pieces[index] = -1

    def reset(self):
        """Reset the board to the initial state."""
        self.pieces = [None]*self.space_count
        self.pieces = [0] * self.space_count

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

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
        if self[space] != color:
            return False
        # Check if the move creates new tiles on only valid spaces
        forward, back = self._action_cells(space, dir)
        if forward is None or back is None:
            return False
        forward = self.indices[forward[0]][forward[1]]
        back = self.indices[back[0]][back[1]]
        # Check if both tiles are empty
        if self[forward] != 0 or self[back] != 0:
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
    
    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color of the piece to play (1=white,-1=black)
        """
        assert self.is_move_legal(move // 3, move % 3, color), \
            "Illegal move: {} for color {}".format(move, color)
        forward, back = self._action_cells(move // 3, move % 3)
        forward = self.indices[forward[0]][forward[1]]
        back = self.indices[back[0]][back[1]]

        self.pieces[forward] = color
        self.pieces[back] = color
        self.pieces[move//3] = 0

    def display(self):
        # display the hex grid
        ind = 0
        piece_symbols = {0: ".", 1: colored("O", "red"), -1: colored("X", "blue")}
        for i in range(0, 2*self.n-1): #2n-1 rows 
            lower_bound = max(0, i-self.n+1)
            upper_bound = min(self.n-1, i)+self.n-1
            row = ""
            for j in range(lower_bound, upper_bound+1): 
                row += piece_symbols[self.pieces[ind]] + " "
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
    