#!/usr/bin/env python3

"""
UI for the Tic Tac Toe game.
"""

import numpy as np
inf = np.inf

from tkinter import *

from parameters import *
from ai import *

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

        # for configuration of who plays first

        menubar = Menu(self)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="First", command=self.human_first)
        filemenu.add_command(label="Second", command=self.computer_first)
        menubar.add_cascade(label="Human Turn", menu=filemenu)

        # create a quit menu, and add it to the menu bar
        menubar.add_command(label='Quit', command=self.quit)

        # display the menu
        self.config(menu=menubar)

        self.bind('<x>', self.exit)
        self.canvas.bind('<Button-1>', self.click)

        self.gamestate = STATE_START_SCREEN
        self.start_screen()

        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]

        # functions for setting who plays first

    def human_first(self):
        self.first = 'HUMAN'

    def computer_first(self):
        self.first = 'COMPUTER'

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
            font=('Franklin Gothic', int(-WINDOW_WIDTH/25))
        )

        self.canvas.create_text(
            int(WINDOW_WIDTH / 2),
            int(2*WINDOW_WIDTH / 3.5),
            text='*Please select the \'Human Turn\' and click on the << Play >> button.', fill='#111',
            font=('Franklin Gothic', int(-WINDOW_WIDTH / 40))
        )

    def new_board(self):
        """
        Clears canvas and draw the new board in the canvas.
        """

        # set who plays first
        self.first

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

    def click(self, event=None):
        """
        When user clicks in anywhere in the screen, this method
        is called.  Event is the click event.
        """
        x = self.ptgrid(event.x)
        y = self.ptgrid(event.y)

        if self.gamestate == STATE_START_SCREEN:

            self.new_board()
            self.gamestate = FIRST_PLAYER

            if self.first == 'COMPUTER':
                move = np.random.choice([0, 1, 2], 2)

                self.new_move(O, move[0], move[1])
                self.gamestate = STATE_X_TURN


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
            y, x, _ = minimax(self.board, -1, 0)
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

            # reset by destroying the created object and run the program again
            self.destroy()
            main()
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