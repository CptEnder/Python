"""
Created on Sun 04 Aug 17:30 2019
Finished on Sun 04 Aug 18:00 2019
@author: Cpt.Ender

Recursive Backtracker Algorithm v3
                              """

import pygame, random

pygame.init()

ws = 1200
hs = 600
num = 50  # number of cells per row/column
w = ws // num
h = hs // num
pygame.display.set_caption('Maze Generator v3')
scrn = pygame.display.set_mode((ws + 1, hs + 1))
white = (200, 200, 200)
blue = (0, 0, 255)
purple = (100, 0, 100)


class Cell:
    def __init__(self, c_i, c_j):
        self.i = c_i
        self.j = c_j
        self.x = c_j * w
        self.y = c_i * h
        self.ar = [True, True, True, True]  # [up, right, down, left]
        self.vis = False

    def walls(self, colour):
        if self.vis:
            pygame.draw.rect(scrn, colour, [self.x, self.y, w, h])
        if self.ar[0]:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x + w, self.y])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y], [self.x + w - 1, self.y])
        if self.ar[1]:
            pygame.draw.line(scrn, white, [self.x + w, self.y], [self.x + w, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x + w, self.y + 1], [self.x + w, self.y + h - 1])
        if self.ar[2]:
            pygame.draw.line(scrn, white, [self.x, self.y + h], [self.x + w, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y + h], [self.x + w - 1, self.y + h])
        if self.ar[3]:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x, self.y + 1], [self.x, self.y + h - 1])


cells = []
stack = []
unv_cells = num ** 2

for i in range(num):
    for j in range(num):
        cells.append(Cell(i, j))
        # cells[i*num + j].walls(purple)  # Comment out for black starting canvas


# Assigning neighbors
def neighbors(current):
    cu_i = current.i
    cu_j = current.j
    array = []
    if cu_i == 0 and cu_j == 0:  # Upper left corner
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[(cu_i + 1)*num + cu_j])
    if cu_i == 0 and cu_j == num - 1:  # Upper right corner
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[(cu_i + 1)*num + cu_j])
    if cu_i == num - 1 and cu_j == 0:  # Lower left corner
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[(cu_i - 1)*num + cu_j])
    if cu_i == num - 1 and cu_j == num - 1:  # Lower right corner
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[(cu_i - 1)*num + cu_j])

    # Edges
    if cu_i == 0 and cu_j > 0 and cu_j != num - 1:
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[(cu_i + 1)*num + cu_j])
    if cu_i > 0 and cu_j == num - 1 and cu_i != num - 1:
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[(cu_i - 1)*num + cu_j])
        array.append(cells[(cu_i + 1)*num + cu_j])
    if cu_i > 0 and cu_j == 0 and cu_i != num - 1:
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[(cu_i - 1)*num + cu_j])
        array.append(cells[(cu_i + 1)*num + cu_j])
    if cu_i == num - 1 and cu_j > 0 and cu_j != num - 1:
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[(cu_i - 1)*num + cu_j])

    # Middle
    if 0 < cu_i < num - 1 and 0 < cu_j < num-1:
        array.append(cells[cu_i*num + cu_j + 1])
        array.append(cells[cu_i*num + cu_j - 1])
        array.append(cells[(cu_i - 1)*num + cu_j])
        array.append(cells[(cu_i + 1)*num + cu_j])
    return array


def redraw(c, x):
    c.walls(x)
    pygame.display.update()


# Starting Position
starting_pos = [0, 0]
cells[starting_pos[0]*num + starting_pos[1]].vis = True
current_cell = cells[starting_pos[0]*num + starting_pos[1]]
redraw(current_cell, purple)
unv_cells -= 1

run = True

while run:
    # clock.tick(20)  # sets the frame rate

    # Conditions to break the run loop
    if unv_cells == 0:
        run = False
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    '''--------------------------|
     |   Recursive backtracker   |
     |--------------------------'''

    neigh = neighbors(current_cell)
    temp = []
    for i in neigh:
        if not i.vis:
            temp.append(i)

    if len(temp):
        rand_neigh = temp[random.randrange(0, len(temp))]
        stack.append(current_cell)
        # Removing the walls between the current and the selected neighbor cell
        if rand_neigh.i < current_cell.i and rand_neigh.j == current_cell.j:
            cells[current_cell.i*num + current_cell.j].ar[0] = False
            cells[rand_neigh.i*num + rand_neigh.j].ar[2] = False
        if rand_neigh.i == current_cell.i and rand_neigh.j > current_cell.j:
            cells[current_cell.i*num + current_cell.j].ar[1] = False
            cells[rand_neigh.i*num + rand_neigh.j].ar[3] = False
        if rand_neigh.i > current_cell.i and rand_neigh.j == current_cell.j:
            cells[current_cell.i * num + current_cell.j].ar[2] = False
            cells[rand_neigh.i * num + rand_neigh.j].ar[0] = False
        if rand_neigh.i == current_cell.i and rand_neigh.j < current_cell.j:
            cells[current_cell.i * num + current_cell.j].ar[3] = False
            cells[rand_neigh.i * num + rand_neigh.j].ar[1] = False

        current_cell = rand_neigh
        current_cell.vis = True
        unv_cells -= 1
    elif stack.__len__():
        current_cell = stack.pop()
    neigh.clear()

    # Redrawing the screen
    if run:
        redraw(current_cell, purple)
