### File Structure

All code is based on Othello -- see original code there. Changes made outside of the pseudo_ttt folder are minimal.
However, there are a few changes made to ensure compatibility with the specific Python / Torch versions. Recommended to keep rather than starting from scratch.

python main.py runs the MCTS trainer. It creates a Coach() which begins the training process.

Coach() will run MCTS() to train the model. Coach() will then run Arena() to test the model (via gameplay).

pseudo_ttt:
TTTGame has the Game object itself.
TTTLogic has the Board. 
TTTPlayers has the agents. To create a 

TTTRun.py (in the main folder) has a script that runs practice games against the Arena, but it's 
more of a minimal example than anything else.

To change the game, modify the Game and Wrapper imports in main.py.

Keras/pytorch are both NN options for the game. I use PyTorch because TF sucks for game playing.

For a new game, maintain the following:

### Curriculum Learning

Not necessary.

### Parallelization

Looks like it could be very useful. Will look into it.

### Hyperparameters

All hyperparameters worth tuning are in:
* main.py 
    - numIters is the number of attempts to outperform the current model
    - numEps is the number of games played
    - tempThreshold will change the number of moves in a single game instance before
        the temperature is dropped to 0 (it plays deterministically). 
    - load_model determines whether a model is loaded or not.     
    - arenaCompare is the number of tests.
    - updateThreshold determines what percentage W/(W+L) (draws ignored) has to be to switch models.
* pseudo_ttt/pytorch/TTTNNet.py is contains the model and some of its parameters. 
    - Beware about size and padding, especially on small boards.
* pseudo_ttt/pytorch/NNet.py contains training stuff (epochs, etc)