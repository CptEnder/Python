"""
Created on Sat 19 Sep 20:36 2020
Finished on Sat 19 Sep 20:40 2020
@author: Cpt.Ender
                                  """
import matplotlib.pyplot as plt


def draw(x, y):
    plt.clf()
    plt.bar(x, y)
    plt.show()
    plt.pause(1 / 1000)
