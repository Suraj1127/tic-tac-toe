#!/usr/bin/env python3

"""
Author: Suraj Regmi
Date: 23rd August, 2018
Description: Tic Tac Toe game using minimax AI algorithm

Creative Commons Licence attribution:
[Code from following stackexchange answer has been taken as reference for the UI]
https://codereview.stackexchange.com/questions/155692/simple-tic-tac-toe-using-tkinter

The licence with which the distribution is made is:
https://creativecommons.org/licenses/by-sa/3.0/
"""

import numpy as np
inf = np.inf

from tkinter import *

from ai import *

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


class Game(Tk):
    """
    Main Game class inheriting Tk class from tkinter.
    """
    def __init__(self):
        Tk.__init__(self)
        self.canvas = Canvas(
            height=WINDOW_WIDTH, width=WINDOW_WIDTH,
            bg=BG_COLOR)

        self.title('Tic Tac Toe')
        self.canvas.pack()

        self.bind('<x>', self.exit)
        self.canvas.bind('<Button-1>', self.click)

        self.gamestate = STATE_START_SCREEN
        self.start_screen()

        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]

    def start_screen(self):
        """
        Method to display the start screen
        """
        # Just in case
        self.canvas.delete('all')

        self.canvas.create_rectangle(
            0, 0,
            WINDOW_WIDTH, WINDOW_WIDTH,
            width=int(WINDOW_WIDTH/15),
            fill='#ddd',
            outline='#555',
        )

        self.canvas.create_text(
            WINDOW_WIDTH/2,
            4*WINDOW_WIDTH/10,
            text='TIC TAC TOE', fill='#222',
            font=('Times New Roman', int(-WINDOW_WIDTH/12), 'bold')
        )

        self.canvas.create_text(
            int(WINDOW_WIDTH/2),
            int(WINDOW_WIDTH/2),
            text='<< Play >>', fill='#111',
            font=('Franklin Gothic', int(-WINDOW_WIDTH/25)))

    def new_board(self):
        """
        Clears canvas and draw the new board in the canvas.
        """

        # Delete all the objects in the canvas
        self.canvas.delete('all')

        # Make the board empty
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

        # Draw the grid(vertical and horizontal lines) in the board
        for n in range(1, 3):
            # For vertical lines
            self.canvas.create_line(
                CELL_SIZE*n, 0,
                CELL_SIZE*n, WINDOW_WIDTH,
                width=LINE_WIDTH, fill=LINE_COLOR,
            )

            # For horizontal lines
            self.canvas.create_line(
                0, CELL_SIZE*n,
                WINDOW_WIDTH, CELL_SIZE*n,
                width=LINE_WIDTH, fill=LINE_COLOR,
            )

    def gameover_screen(self, outcome):
        """
        The view to be displayed when the game is over.
        """

        # Clear the board in the canvas.
        self.canvas.delete('all')

        if outcome == 'X WINS':
            wintext = 'You won!'
            wincolor = X_COLOR

        elif outcome == 'O WINS':
            wintext = 'AI won!'
            wincolor = O_COLOR

        elif outcome == 'DRAW':
            wintext = 'Draw!'
            wincolor = DRAW_SCREEN_COLOR

        self.canvas.create_rectangle(
            0, 0,
            WINDOW_WIDTH, WINDOW_WIDTH,
            fill=wincolor, outline='',
        )

        self.canvas.create_text(
            int(WINDOW_WIDTH/2), int(2*WINDOW_WIDTH/5),
            text=wintext, fill='white',
            font=('Times New Roman', int(-WINDOW_WIDTH/10), 'bold')
        )

        self.canvas.create_text(
                int(WINDOW_WIDTH/2), int(WINDOW_WIDTH/2),
                text='<< Play Again >>', fill='white',
                font=('Franklin Gothic', int(-WINDOW_WIDTH/25))
        )

    def click(self, event):
        """
        When user clicks in anywhere in the screen, this method
        is called.  Event is the click event.
        """
        x = self.ptgrid(event.x)
        y = self.ptgrid(event.y)

        if self.gamestate == STATE_START_SCREEN:
            self.new_board()
            self.gamestate = FIRST_PLAYER


        # Ensure that the turn is of X and the place where clicked
        # in grid is empty
        elif (self.gamestate == STATE_X_TURN and
                self.board[y][x] == EMPTY):
            self.new_move(X, x, y)

            if self.has_won(X):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('X WINS')

            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')
            else:
                self.gamestate = STATE_O_TURN

            if self.is_a_draw() or self.has_won(X):
                return

            # For AI turn
            self.click(event)

        elif (self.gamestate == STATE_O_TURN):
            # x and y to change by AI
            y, x, _ = minimax(self.board, -1)
            self.new_move(O, x, y)

            if self.has_won(O):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('O WINS')

            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')

            else:
                self.gamestate = STATE_X_TURN

        elif self.gamestate == STATE_GAME_OVER:
            #reset
            self.new_board()
            self.gamestate = FIRST_PLAYER

    def new_move(self, player, grid_x, grid_y):
        """
        Player is either X or O
        x and y are 0-based grid coordinates

          0 1 2
        0 _|_|_
        1 _|_|_
        2  | |

        """
        #duplication /!\
        if player == X:
            self.draw_X(grid_x, grid_y)
            self.board[grid_y][grid_x] = X

        elif player == O:

            self.draw_O(grid_x, grid_y)
            self.board[grid_y][grid_x] = O

    def draw_X(self, grid_x, grid_y):
        """
        draw the X symbol at x, y in the grid
        """

        x = self.gtpix(grid_x)
        y = self.gtpix(grid_y)
        delta = CELL_SIZE/2*RELATIVE_SYMBOL_SIZE

        self.canvas.create_line(
            x-delta, y-delta,
            x+delta, y+delta,
            width=SYMBOL_WIDTH, fill=X_COLOR
        )

        self.canvas.create_line(
            x+delta, y-delta,
            x-delta, y+delta,
            width=SYMBOL_WIDTH, fill=X_COLOR
        )

    def draw_O(self, grid_x, grid_y):
        """
        draw an O symbol at x, y in the grid

        note : a big outline value appears to cause a visual glitch in tkinter
        """

        x = self.gtpix(grid_x)
        y = self.gtpix(grid_y)
        delta = CELL_SIZE/2*RELATIVE_SYMBOL_SIZE

        self.canvas.create_oval(
            x-delta, y-delta,
            x+delta, y+delta,
            width=SYMBOL_WIDTH, outline=O_COLOR)

    def has_won(self, symbol):
        for y in range(3):
            if self.board[y] == [symbol, symbol, symbol]:
                return True

        for x in range(3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x] == symbol:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            return True

        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            return True

        # no win sequence found
        return False

    def is_a_draw(self):
        for row in self.board:
            if EMPTY in row:
                return False

        #no empty cell left, the game is a draw
        return True

    def gtpix(self, grid_coord):
        # gtpix = grid_to_pixels
        # for a grid coordinate, returns the pixel coordinate of the center
        # of the corresponding cell

        pixel_coord = grid_coord * CELL_SIZE + CELL_SIZE / 2
        return pixel_coord

    def ptgrid(self, pixel_coord):
        # ptgrid = pixels_to_grid
        # the opposit of gtpix()

        # somehow the canvas has a few extra pixels on the right and bottom side
        if pixel_coord >= WINDOW_WIDTH:
            pixel_coord = WINDOW_WIDTH - 1

        grid_coord = int(pixel_coord / CELL_SIZE)
        return grid_coord

    def exit(self, event):
        self.destroy()

def main():

    # Create instance of Game class and call the mainloop method inherited from Tk class
    root = Game()
    root.mainloop()

if __name__ == "__main__":
    main()