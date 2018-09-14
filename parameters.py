# Program parameters

# Graphics in pixels
WINDOW_WIDTH = 600
LINE_WIDTH = 5
SYMBOL_WIDTH = WINDOW_WIDTH/15

# Symbol Size is relative size of symbol with respect to the size of a single cell
# i.e SYMBOL_SIZE = size of a cell/size of the symbol
RELATIVE_SYMBOL_SIZE = 0.5

# Setting color of the symbols
X_COLOR = 'blue'
O_COLOR = 'red'

# Set colors
# DRAW_SCREEN_COLOR: color displayed in the end when game becomes draw
# LINE_COLOR: color of the grid
# BG_COLOR: background color of the grid
DRAW_SCREEN_COLOR = 'light sea green'
LINE_COLOR = 'grey'
BG_COLOR = 'white'

# Set which player plays first move
# 1 => X, -1 => O
FIRST_PLAYER = 1 # 1 - X, 2 = O

# Set size of the cell with relative to window size
CELL_SIZE = WINDOW_WIDTH / 3

# Set states of the game
# 0 means the game has not yet started
# 1 means X turn, -1 means 0 turn and 3 means the game is over
STATE_START_SCREEN = 0
STATE_X_TURN = 1
STATE_O_TURN = -1
STATE_GAME_OVER = 3

# Values in the grid representing the board structure
EMPTY = 0
X = 1
O = -1
