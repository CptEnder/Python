"""
Created on Sat 05 Oct 09:45 2019
Finished on Sun 06 Oct 00:52 2019
@author: Cpt.Ender
Currently not working
                                  """
from random import sample as sample

grid_r = [[], [], [], [], [], [], [], [], []]
grid_c = [[], [], [], [], [], [], [], [], []]
boxes = [[[], [], []], [[], [], []], [[], [], []]]

while grid_r[8].__len__() < 8:
    for x in grid_r:
        if x.__len__() < 9:
            n = grid_r.index(x)
            break
    row_done = column_done = False
    print(n)
# Creating rows:
    while not row_done:
        check1 = True
        # 1st - Creating temporary row
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for col in grid_c[0:n]:
            lst.pop(lst.index(col[n]))
        temp_r = sample(lst, 9-n)
        # 2nd - Checking for duplicate numbers in boxes
        for y in temp_r:
            for x in boxes[int(n/3)][int((temp_r.index(y)+n)/3)]:
                if y == x:
                    check1 = False
                    break
        # 3rd - Checking for duplicate numbers in columns
        # if check1:
        for y in temp_r:
            for x in grid_c[temp_r.index(y)+n]:
                if y == x:
                    check1 = False
                    break
        # 4th - Appending the temporary row to the grid
        if check1:
            grid_r[n] += temp_r
            for i in range(n, 9):
                grid_c[i].append(temp_r[i-n])
            for y in grid_r[n][n:9]:
                boxes[int(n/3)][int(grid_r[n].index(y)/3)].append(y)
            row_done = True

# Creating columns
    while not column_done:
        check2 = True
        # 1st - Creating temporary column
        lst_c = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in grid_r[0:n+1]:
            lst_c.pop(lst_c.index(row[n]))
        temp_c = sample(lst_c, 9-n-1)
        # 2nd - Checking for duplicate numbers in boxes
        for y in temp_c:
            for x in boxes[int((temp_c.index(y)+n+1)/3)][int(n/3)]:
                if y == x:
                    check2 = False
                    break
        # 3rd - Checking for duplicate numbers in rows
        # if check2:
        for y in temp_c:
            for x in grid_r[temp_c.index(y)+n+1]:
                if y == x:
                    check2 = False
                    break
        # 4th - Appending the temporary column to the grid
        if check2:
            grid_c[n] += temp_c
            for i in range(n, 8):
                grid_r[i+1].append(temp_c[i-n])
            for y in grid_c[n][n+1:9]:
                boxes[int(grid_c[n].index(y)/3)][int(n/3)].append(y)
            column_done = True