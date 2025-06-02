from collections import defaultdict
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

    def __init__(self, n, m, x):
        "Set up initial board configuration."

        self.n = n
        self.m = m
        self.x = x
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.m  

    def reset(self):
        """Reset the board to the initial state."""
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.m

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares whose top cells are 0
        for x in range(self.m):
            if self.pieces[0][x] == 0:
                # If the top cell is empty, then the column is a legal move.
                moves.add(x)
        return list(moves)

    def has_legal_moves(self):
        return (0 in self[0])
    
    def get_game_ended(self, color):
        """ Check if there is an x in a row/col/diag of 1's or -1's"""
        # Rows
        for i in range(self.n):
            count = 0
            for j in range(self.m):
                if self[i][j] == 0:
                    count = 0
                if self[i][j] * count < 0:
                    count = 0
                count += self[i][j]
                if count >= self.x:
                    return 1
                if count <= -self.x:
                    return -1
        # Columns
        for j in range(self.m):
            count = 0
            for i in range(self.n):
                if self[i][j] == 0:
                    count = 0
                if self[i][j] * count < 0:
                    count = 0
                count += self[i][j]
                if count >= self.x:
                    return 1
                if count <= -self.x:
                    return -1
        # Diagonals
        # Create lists consisting of all diagonals 
        pos_slope_diagonals = [[] for _ in range(self.n + self.m - 1)]
        neg_slope_diagonals = [[] for _ in range(self.n + self.m - 1)]
        for i in range(self.n):
            for j in range(self.m):
                pos_slope_diagonals[i-j+self.m-1].append(self[i][j])
                neg_slope_diagonals[i+j].append(self[i][j])

        # Check all diagonals for a win
        for diag in pos_slope_diagonals:
            count = 0
            for cell in diag:
                if cell == 0:
                    count = 0
                if cell * count < 0:
                    count = 0
                count += cell
                if count >= self.x:
                    return 1
                if count <= -self.x:
                    return -1
                
        for diag in neg_slope_diagonals:
            count = 0
            for cell in diag:
                if cell == 0:
                    count = 0
                if cell * count < 0:
                    count = 0
                count += cell
                if count >= self.x:
                    return 1
                if count <= -self.x:
                    return -1

        if not self.has_legal_moves():
            return None # Draw condition, no legal moves left for either player
        else:
            return 0

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color of the piece to play (1=white,-1=black)
        """
        assert self[0][move] == 0, "Cannot play on a full column!"
        
        for y in range(self.n-1, -1, -1):
            if self[y][move] == 0:
                self[y][move] = color
                break

