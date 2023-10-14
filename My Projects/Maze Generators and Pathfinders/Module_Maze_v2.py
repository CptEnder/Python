"""
Created on Thu 30 Jul 17:08 2020
Finished on Thu 30 Jul 18:53 2020
@author: Cpt.Ender

Recursive Backtracker Algorithm v3
A module for creating mazes
                                    """
import random


class Cell:
    def __init__(self, c_i, c_j, width, height):
        self.i = c_i
        self.j = c_j
        self.x = c_j * width
        self.y = c_i * height
        self.ar = [True, True, True, True]  # [up, right, down, left]
        self.vis = False
        self.colour = (100, 0, 100)


# Assigning neighbors
def neighbors(current, cells, num):
    cu_i = current.i
    cu_j = current.j
    array = []
    if cu_i == 0 and cu_j == 0:  # Upper left corner
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[(cu_i + 1) * num + cu_j])
    if cu_i == 0 and cu_j == num - 1:  # Upper right corner
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[(cu_i + 1) * num + cu_j])
    if cu_i == num - 1 and cu_j == 0:  # Lower left corner
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[(cu_i - 1) * num + cu_j])
    if cu_i == num - 1 and cu_j == num - 1:  # Lower right corner
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[(cu_i - 1) * num + cu_j])

    # Edges
    if cu_i == 0 and cu_j > 0 and cu_j != num - 1:
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[(cu_i + 1) * num + cu_j])
    if cu_i > 0 and cu_j == num - 1 and cu_i != num - 1:
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[(cu_i - 1) * num + cu_j])
        array.append(cells[(cu_i + 1) * num + cu_j])
    if cu_i > 0 and cu_j == 0 and cu_i != num - 1:
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[(cu_i - 1) * num + cu_j])
        array.append(cells[(cu_i + 1) * num + cu_j])
    if cu_i == num - 1 and cu_j > 0 and cu_j != num - 1:
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[(cu_i - 1) * num + cu_j])

    # Middle
    if 0 < cu_i < num - 1 and 0 < cu_j < num - 1:
        array.append(cells[cu_i * num + cu_j + 1])
        array.append(cells[cu_i * num + cu_j - 1])
        array.append(cells[(cu_i - 1) * num + cu_j])
        array.append(cells[(cu_i + 1) * num + cu_j])
    return array


def amaze(screen_w: int, screen_h: int, num_cells: int, start):
    w = screen_w // num_cells
    h = screen_h // num_cells

    cells = []
    stack = []

    for i in range(num_cells):
        for j in range(num_cells):
            cells.append(Cell(i, j, w, h))
    starting_pos = start
    cells[starting_pos[0] * num_cells + starting_pos[1]].vis = True
    current_cell = cells[starting_pos[0] * num_cells + starting_pos[1]]
    unv_cells = num_cells ** 2 - 1

    # A list of the order the cells are being visited
    list_of_creation = [cells.index(current_cell)]
    while unv_cells > 0:
        '''--------------------------|
         |   Recursive backtracker   |
         |--------------------------'''

        neigh = neighbors(current_cell, cells, num_cells)
        temp = []
        for i in neigh:
            if not i.vis:
                temp.append(i)

        if len(temp):
            rand_neigh = temp[random.randrange(0, len(temp))]
            stack.append(current_cell)
            # Removing the walls between the current and the selected neighbor cell
            if rand_neigh.i < current_cell.i and rand_neigh.j == current_cell.j:
                cells[current_cell.i * num_cells + current_cell.j].ar[0] = False
                cells[rand_neigh.i * num_cells + rand_neigh.j].ar[2] = False
            if rand_neigh.i == current_cell.i and rand_neigh.j > current_cell.j:
                cells[current_cell.i * num_cells + current_cell.j].ar[1] = False
                cells[rand_neigh.i * num_cells + rand_neigh.j].ar[3] = False
            if rand_neigh.i > current_cell.i and rand_neigh.j == current_cell.j:
                cells[current_cell.i * num_cells + current_cell.j].ar[2] = False
                cells[rand_neigh.i * num_cells + rand_neigh.j].ar[0] = False
            if rand_neigh.i == current_cell.i and rand_neigh.j < current_cell.j:
                cells[current_cell.i * num_cells + current_cell.j].ar[3] = False
                cells[rand_neigh.i * num_cells + rand_neigh.j].ar[1] = False

            current_cell = rand_neigh
            current_cell.vis = True
            unv_cells -= 1
            list_of_creation.append(cells.index(current_cell))
        elif len(stack):
            current_cell = stack.pop()
        neigh.clear()
    return cells, list_of_creation