from utils import dotdict
import sys, math, numpy as np
sys.path.append('..')

from Game import Game
from Arena import Arena
from MCTS import MCTS 

from pseudo_ttt.TTTGame import TTTGame as Game
from pseudo_ttt.TTTLogic import Board
from pseudo_ttt.TTTPlayers import *
from pseudo_ttt.pytorch.NNet import NNetWrapper as nn


args = dotdict({
    'numIters': 10,
    'numEps': 15,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': math.inf,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    'load_folder_file': ('./temp', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

    'player1': 'nnet',
    'player2': 'random',
})

g = Game(3)

def init_players():
    if args.player1 == 'random':
        p1 = RandomPlayer(g)
    elif args.player1 == 'human':
        p1 = HumanTTTPlayer(g)
    elif args.player1 == 'greedy':
        p1 = GreedyTTTPlayer(g)
    elif args.player1 == 'nnet':
        p1net = nn(g)
        p1net.load_checkpoint(folder=args.checkpoint, filename=args.load_folder_file[1])
        p1mcts = MCTS(g, p1net, args)
        p1 = lambda x: np.argmax(p1mcts.getActionProb(x, temp=0))
    else:
        raise ValueError("Unknown player1 type: {}".format(args.player1))

    if args.player2 == 'random':
        p2 = RandomPlayer(g)
    elif args.player2 == 'human':
        p2 = HumanTTTPlayer(g)
    elif args.player2 == 'greedy':
        p2 = GreedyTTTPlayer(g)
    elif args.player2 == 'nnet':
        p2net = nn(g)
        p2net.load_checkpoint(folder=args.checkpoint, filename=args.load_folder_file[1])
        p2mcts = MCTS(g, p2net, args)
        p2 = lambda x: np.argmax(p2mcts.getActionProb(x, temp=0))
    else:
        raise ValueError("Unknown player2 type: {}".format(args.player2))
    return p1, p2

p1, p2 = init_players()

a = Arena(p1, p2, g, display=Game.display)

w,l,d = a.playGames(10,True)
print (w,l,d)
