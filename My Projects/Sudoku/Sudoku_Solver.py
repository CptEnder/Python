"""
Created on Sat 15 Feb 15:54 2020
Finished on Sat 15 Feb 17:00 2020
@author: Cpt.Ender

Sudoku solver using recursion
                                  """
# array = [[4, 9, 2, 6, 8, 3, 1, 5, 7],
#          [0, 8, 7, 9, 4, 0, 0, 0, 6],
#          [0, 6, 3, 2, 7, 0, 9, 4, 8],
#          [7, 5, 4, 8, 9, 6, 0, 0, 1],
#          [9, 1, 6, 5, 3, 2, 8, 7, 4],
#          [3, 2, 8, 7, 1, 4, 6, 9, 5],
#          [6, 4, 5, 3, 2, 8, 7, 1, 9],
#          [2, 7, 1, 4, 6, 9, 5, 8, 3],
#          [8, 3, 9, 1, 5, 7, 4, 6, 2]]


# Checking whether the number 'n' can
# be put in the position (x,y) of the grid
def possible(grid, x, y, n):
    # Checking the row and column
    for i in range(9):
        if grid[i][y] == n or grid[x][i] == n:
            return False
    boxx = x//3*3
    boxy = y//3*3

    # Checking the box
    for i in range(3):
        for j in range(3):
            if grid[boxx + i][boxy+j] == n:
                return False
    return True


def solve(grid, num=0):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                for n in range(1, 10):
                    if possible(grid, x, y, n):
                        grid[x][y] = n
                        num = solve(grid, num)
                        grid[x][y] = 0
                return num
    num += 1
    # printing(grid, num)
    return num


# def solve(grid):
#     num_of_sltns = solve_(grid, 0)
#     return num_of_sltns
