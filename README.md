# tic-tac-toe
Tic Tac Toe game using Minimax AI algorithm.

## Short Description:

The repository is implementation of AI in Tic Tac Toe game using Minimax algorithm.

## Requirements:
- Python 3
- tkinter (Python GUI library)
- Numpy (Python scientific computing library)

## Instructions:
* Run python program game.py and start the program.
* Select the 'Human Turn' to decide who plays first.  After human's each move, AI move would be automatically played.

## Improvements:
* Here, first player is always set to human.  We can have user set the configurations.
* No of steps is not taken into consideration while calculating evaluation function/state.  We can take it into account.  Though for this game, it is not super useful, but for other complex games like chess, bagchal, etc, it is mandatory to finish up the game sooner.

## Possible Improvements:
* Alpha Beta pruning is not used for reducing time.  As the depth and breadth is not quite large, speed has not been an issue.  But it can be implemented as a practice here too.  Alpha Beta pruning is super useful for complex programs.
