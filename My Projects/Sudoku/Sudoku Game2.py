"""
Created on Fri 03 Mar 15:46 2023
Finished on Mon 07 Mar 23:30 2023
@author: Cpt.Ender

Things to be added:
- Make better Sudoku creators (if the clues of a selected difficulty are more that the previous diff
                                then scrap that sudoku and remake it)
                                                                                                      """
from Sudoku_Board import Board

board = Board("Sudoku", [630, 630])

while board.events():
    board.logig()
    board.draw()
