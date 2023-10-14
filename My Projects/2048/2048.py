"""
Created on Wed 14 Oct 22:29 2020
Finished on Wed 28 Oct 21:30 2020
@author: Cpt.Ender

Working but no colours
                                  """
import game_module_2048 as gm

if __name__ == '__main__':
    Board = gm.Board([600, 600], [4, 4])
    while Board.running:
        Board.logig()
        Board.draw()
    Board.quit()