"""
Created on Fri 18 Sep 22:46 2020
Finished on Fri 18 Sep 23:00 2020
@author: plabc

Visualization of a Double Bubble
Sorting Algorithm
                                  """
import random
from Draw_module import draw

n = 100
x = [i for i in range(1, n)]
y = x[:]
random.shuffle(y)


def swap(lst: list, index1: int, index2: int):
    temp = lst[index1]
    lst[index1] = lst[index2]
    lst[index2] = temp


def double_bubble(lst: list):
    end = len(lst)
    start = 0
    while start < end:
        for i in range(start, end - 1):
            if lst[i] > lst[i + 1]:
                swap(lst, i, i + 1)
            draw(x, lst)

        for i in range(end - 2, start, -1):
            if lst[i] < lst[i - 1]:
                swap(lst, i, i - 1)

            draw(x, lst)

        end -= 1
        start += 1


double_bubble(y)
