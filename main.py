import logging
import math

from Coach import Coach
#from pseudo_ttt.TTTGame import TTTGame as Game
#from pseudo_ttt.pytorch.NNet import NNetWrapper as nn

#from pseudo_c4.C4Game import C4Game as Game
#from pseudo_c4.pytorch.NNet import NNetWrapper as nn

from pseudo_mitosis.MitosisGame import MitosisGame as Game
from pseudo_mitosis.pytorch.NNet import NNetWrapper as nn

#from connect4.Connect4Game import Connect4Game as Game
#from connect4.keras.NNet import NNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

args = dotdict({
    'numIters': 50,
    'numEps': 30,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': math.inf,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 50,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 30,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    #'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'load_folder_file': ('./temp', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def main():
    log.info('Loading %s...', Game.__name__)
    g = Game(4)
    #g = Game(5)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
