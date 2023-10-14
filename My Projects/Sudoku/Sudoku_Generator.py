"""
Created on Sat 15 Feb 23:28 2020
Finished on Thu 21 Feb 00:10 2020
@author: Cpt.Ender

Sudoku Generator v3
                                  """
from random import sample
from Sudoku_Solver import solve

lst = range(1, 10)


# Printing the grid to the screen
def printing(grid):
    # print("Solution N %s" % N)
    for row in grid:
        if grid.index(row).__mod__(3) == 0:
            print('\n', ' _________' * 3)
        else:
            print('\n', end='')
        for ii in range(9):
            if ii.__mod__(3) == 0:
                print(' |', row[ii], end='')
            elif ii.__mod__(8) == 0:
                print(' ', row[ii], '|', end='')
            else:
                print(' ', row[ii], end='')
    print('\n', ' _________' * 3)


# Checking if it's possible to put the number
# 'n' in the position (x,y) of the grid
def possible(grid, x, y, n):
    # Checking the row and column
    for i in range(9):
        if grid[i][y] == n or grid[x][i] == n:
            return False
    boxx = x // 3 * 3
    boxy = y // 3 * 3

    # Checking the box
    for i in range(3):
        for j in range(3):
            if grid[boxx + i][boxy + j] == n:
                return False
    return True


# Fill the empty array
def fill_grid(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                temp = sample(lst, 9)
                for n in temp:
                    if possible(grid, x, y, n):
                        grid[x][y] = n
                        fill_grid(grid)
                        if grid[8][8] == 0:
                            grid[x][y] = 0
                return
    return


# Removing numbers from the grid and checking
# the number of solutions (must be only one solution)
def sudokufication(grid, positions_list):
    # num_of_sltns = 1
    # while num_of_sltns < 2:
    #     x = sample(lst, 1)[0] - 1
    #     y = sample(lst, 1)[0] - 1
    #     n_temp = grid[x][y]  # Store temporary the number in the current position
    #     grid[x][y] = 0
    #     num_of_sltns = solve(grid)
    # # If there are 2 solutions to the Sudoku, then put
    # # the last removed number back to its place
    # grid[x][y] = n_temp
    sudoku = [[]] * 9
    for i, line in enumerate(grid):
        sudoku[i] = grid[i][:]
    for n in positions_list:
        x, y = divmod(n, 9)
        n_temp = sudoku[x][y]  # Store temporary the number in the current position
        sudoku[x][y] = 0
        num_of_sltns = solve(sudoku)
        if num_of_sltns >= 2:
            sudoku[x][y] = n_temp
    return sudoku


def create(n=25):
    grid = []
    for x in range(9):
        grid.append([])
        for y in range(9):
            grid[x].append(0)
    fill_grid(grid)
    availableGridPos = sample(range(0, 81), 81 - n)
    sudoku = sudokufication(grid, availableGridPos)
    # printing(grid)
    return grid, sudoku


Filled, Sudoku = create()
