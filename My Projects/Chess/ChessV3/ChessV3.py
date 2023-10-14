"""
Created on Tue 14 Mar 16:35 2023
Finished on
@author: Cpt.Ender
                                  """
from ChessBoard import Board

board = Board('Chess game', [640, 640])

while board.running():
    # print(board.clock.tick())
    board.logig()
    board.draw()

