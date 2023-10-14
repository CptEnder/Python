"""
Created on Tue 29 Jun 00:15 2021
Finished on Tue 29 Jun 00:30 2021
@author: Cpt.Ender
                                  """

# from turtle import *
#
#
# def tree(length, level, angle):
#     if level == 0:
#         return
#
#     forward(length)
#     right(angle)
#
#     tree(length * 0.7, level - 1, angle)
#
#     left(angle * 2)
#
#     tree(length * 0.7, level - 1, angle)
#
#     right(angle)
#     backward(length)
#
#
# penup()
# setheading(90)
# sety(-200)
# speed(0)
# pendown()
#
# tree(150, 8, 30)
# mainloop()

import math
import matplotlib.pyplot as plt


def drawTree(x1, y1, angle, depth):
    fork_angle = 20
    base_len = 10.0
    if depth > 0:
        x2 = x1 - int(math.cos(math.radians(angle)) * depth * base_len)
        y2 = y1 - int(math.sin(math.radians(angle)) * depth * base_len)
        array[0].append([x1, x2])
        x.append(x2)
        array[1].append([y1, y2])
        y.append(y2)
        drawTree(x2, y2, angle - fork_angle, depth - 1)
        drawTree(x2, y2, angle + fork_angle, depth - 1)


array = [[], []]
x, y = [[300], [550]]
drawTree(x[0], y[0], -90, 8)
plt.plot(x, y, '.g')
for i in range(len(array[0])):
    plt.plot(array[0][i], array[1][i], '--', color=(0.1, 0.2, 0.5, 0.5))
