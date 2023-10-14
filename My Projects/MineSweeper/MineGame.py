"""
Created on Sun 20 Mar 19:56 2022
Finished on Wednesday 23 Mar 19:30 2022
@author: Cpt.Ender
                                  """
from MineClass import mineSweep

if __name__ == '__main__':
    game = mineSweep(750, 750, 15, 15)
    while game.running():
        if not game.gameOver:
            game.logig()
            game.draw()
    game.quit()