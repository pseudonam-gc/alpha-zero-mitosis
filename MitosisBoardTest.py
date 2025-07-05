import random
from pseudo_mitosis.MitosisLogic import Board 
from pseudo_mitosis.MitosisGame import MitosisGame
from pseudo_mitosis.pytorch.NNet import NNetWrapper as nn
from pseudo_mitosis.MitosisPlayers import * 
from Arena import Arena

g = MitosisGame(3)  # Create a game instance with a 3-size board

def generate_random_board(n):
    """Generate a random board for testing."""
    b = Board(n)
    # Randomly place pieces on the board
    cutoff = 0.25
    for i in range(b.space_count):
        randn = np.random.rand()
        if randn < cutoff:
            b.pieces[i] = 1  # Player 1's piece
        elif randn < 2*cutoff:
            b.pieces[i] = -1
        else:
            b.pieces[i] = 0
    # the number of TRIANGLES WITH 1's is higher than the number of TRIANGLES WITH -1's
    counts = [0,0]
    for i in range(b.space_count):
        # convert to (i,j) coordinates
        xi, yi = b.cells[i]
        # confirm that both it and the space directly to the right is occupied by the same value 
        xi2, yi2 = xi, yi + 1
        if xi2 < 0 or xi2 >= 2*n-1 or yi2 < 0 or yi2 >= 2*n-1:
            continue
        if b.indices[xi2][yi2] is None:
            continue
        if b.pieces[i] != b.pieces[b.indices[xi2][yi2]] or b.pieces[i] == 0:
            continue

        cells = [(xi-1, yi), (xi+1, yi+1)]
        # check if these cells are within bounds
        for (x,y) in cells:
            if x < 0 or x >= 2*n-1 or y < 0 or y >= 2*n-1:
                continue
            if b.indices[x][y] is None:
                continue
            if b.pieces[b.indices[x][y]] == b.pieces[i]:
                ind = 0 if b.pieces[i] == 1 else 1
                counts[ind] += 1


    pi = np.random.dirichlet(np.ones(g.getActionSize()))
    if min(counts) > 0 or max(counts) == 0:
        return None
    
    if counts[0] > counts[1]:
        v = 1 
    elif counts[0] < counts[1]:
        v = -1
    
    return (b.pieces, pi, v)


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

import torch
from utils import dotdict

nnet = nn(g)
example_count = 1e6
examples = []
while len(examples) < example_count:
    res = generate_random_board(3)
    if res is not None:
        examples.append(res)
print ("Examples size:", len(examples))
train_frac = 0.8
train_examples = examples[:int(len(examples) * train_frac)]  # Use 80% for training
test_examples = examples[int(len(examples) * train_frac):]  # Use 20% for testing

nnet.train(train_examples)

# test loop
correct = 0
for (board,pi,v) in test_examples:
    board = np.array(board).astype(np.float64)
    pi_pred, v_pred = nnet.predict(board)
    v_pred = v_pred.item()
    if (v_pred * v) > 0:
        correct += 1
        
accuracy = correct / len(test_examples)
print(f"Test accuracy: {accuracy * 100:.2f}%")



# run on testset