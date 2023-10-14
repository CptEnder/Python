"""
Created on Fri 27 Sep 22:34 2019
Finished on Sun 29 Sep 18:00 2019
@author: Cpt.Ender
                                  """
from random import sample as sample

grid = []
boxes = [[[], [], []], [[], [], []], [[], [], []]]
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# First row of the array
temp = sample(lst, 9)
grid.append(temp)
for x in temp:
    if temp.index(x).__mod__(3) == 0:
        k = temp.index(x)
    boxes[0][int(k/3)].append(x)

valid = True
l_i = 0

while grid.__len__() < 8:
    l = grid.__len__()
    # Checking for duplicate numbers in columns
    for i in range(0, l):
        for ii in range(0, 9):
            if temp[ii] == grid[i][ii]:
                valid = False
                break
    # Checking for duplicate numbers in boxes
    if valid:
        for x in temp:
            if temp.index(x).__mod__(3) == 0:
                k = temp.index(x)
            if x in boxes[l_i][int(k/3)] and l.__mod__(3) != 0:
                valid = False
                break

    if valid:
        grid.append(temp)
        if l.__mod__(3) == 0:
            l_i += 1
        for x in temp:
            if temp.index(x).__mod__(3) == 0:
                k = temp.index(x)
            boxes[l_i][int(k / 3)].append(x)
    else:
        temp = sample(lst, 9)
        valid = True


# Final row of the array
temp = []
for i in range(0, 9):
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for ii in range(0, 8):
        try:
            lst.pop(lst.index(grid[ii][i]))
        except ValueError:
            pass
    temp += lst
grid.append(temp)
for x in temp:
    if temp.index(x).__mod__(3) == 0:
        k = temp.index(x)
    boxes[2][int(k/3)].append(x)

# Printing the finished Sudoku
for i in grid:
    if grid.index(i).__mod__(3) == 0:
        print('\n', ' _________'*3)
    else:
        print('\n', end='')
    for ii in i:
        if i.index(ii).__mod__(3) == 0:
            print(' |', ii, end='')
        elif i.index(ii).__mod__(8) == 0:
            print(' ', ii, '|', end='')
        else:
            print(' ', ii, end='')
print('\n', ' _________'*3)