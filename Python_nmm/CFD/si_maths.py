"""
Created on Wed 04 Mar 20:56 2020
Finished on
@author: Cpt.Ender

Current features :  - Matrix sub module
                    - Module for solving linear equations
                    - some constants

                                        """


import matrices as mat
import linAlg as linalg

pi = 3.141592653589793
e = 2.718281828459045

def frange(start: float, stop: float, step: float = 1):
    lst = []
    count = 0
    x = len(str(step).split('.')[1])

    if start < stop:
        while round(start + count * step,x) < round(stop + step,x):
            lst.append(round(start + count * step, x))
            count += 1
    else:
        while start + count * step > stop - step:
            lst.append(round(start + count * step, x))
            count -= 1

    return lst

def linspace(start: float,end: float, num: int):
    num = int(num)
    dx = (end-start)/(num-1)
    lst = frange(start, end, abs(dx))
    return lst
