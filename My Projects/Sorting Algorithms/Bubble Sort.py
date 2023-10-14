"""
Created on Fri 18 Sep 10:37 2020
Finished on Fri 18 Sep 12:00 2020
@author: Cpt.Ender

Visualization of the Bubble Sorting Algorithm
                                                """

import random
from Draw_module import draw

x = [i for i in range(1, 20)]
y = x[:]
random.shuffle(y)


def swap(lst: list, index: int):
    temp = lst[index]
    lst[index] = lst[index + 1]
    lst[index + 1] = temp


def bubble_sort(lst: list):
    n = len(lst)
    while n > 0:
        for i in range(n - 1):
            if lst[i] > lst[i + 1]:
                swap(lst, i)
            draw(x, lst)
        n -= 1


bubble_sort(y)
