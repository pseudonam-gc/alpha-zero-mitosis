from pseudo_mitosis.MitosisLogic import Board 
from pseudo_mitosis.MitosisGame import MitosisGame
#from pseudo_mitosis.pytorch.NNet import NNetWrapper as n
from pseudo_mitosis.MitosisPlayers import * 
from Arena import Arena

# Testing suite

b = Board(5)  

# Number of moves = hexhex4 * 3 + 3*6 = 129
# Subtract 48 for the moves blocked by starting positions

assert len(b.get_legal_moves(0)) == (81) # Get legal moves for player 0 (nonexistent 'blank' player)

# Start Arena game

g = MitosisGame(3)  # Create a game instance with a 5-size board
a = Arena(RandomPlayer(g), GreedyMitosisPlayer(g), g, display=MitosisGame.display)
p1, p2, draws = a.playGames(4, verbose=True) 
assert draws == 0, "There should be no draws in Mitosis" 
print (f"Player 1 won {p1} games, Player 2 won {p2} games, and there were {draws} draws.")