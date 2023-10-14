"""
Created on Mon 06 Sep 16:47 2021
Finished on
@author: Cpt.Ender
                                  """
from DrawingModule import Board

nono = [((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,))]

if __name__ == "__main__":
    Game = Board('Nonogram', [600, 700], nono)
    while Game.running():
        Game.logig()
        Game.draw()
