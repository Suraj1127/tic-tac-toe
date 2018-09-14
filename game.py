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

from ui import *


def main():

    # Create instance of Game class and call the mainloop method inherited from Tk class
    root = Game()
    root.mainloop()

if __name__ == "__main__":
    main()