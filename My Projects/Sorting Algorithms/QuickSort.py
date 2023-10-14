"""
Created on Sat 19 Sep 20:41 2020
Finished on
@author: Cpt.Ender

Visualization of the QuickSort Algorithm
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


def partition(array: list, start, end):
    pivot_value = array[end]
    pivot_index = start
    for i in range(start, end):
        if array[i] < pivot_value:
            swap(array, i, pivot_index)
            pivot_index += 1
    swap(array, pivot_index, end)
    return pivot_index


def quicksort(array: list, start: int, end: int):
    draw(x, y)
    if start >= end:
        return

    index = partition(array, start, end)
    quicksort(array, start, index - 1)
    quicksort(array, index + 1, end)


quicksort(y, 0, len(y) - 1)
