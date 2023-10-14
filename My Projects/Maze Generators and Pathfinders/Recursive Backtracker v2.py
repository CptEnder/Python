"""
Created on Fri 02 Aug 09:46 2019
Finished on Fri 02 Aug 16:00 2019
@author: Cpt.Ender

Recursive Backtracker Algorithm v2
                                  """
import pygame, random

pygame.init()

ws = 600
hs = 600
num = 20  # number of cells per row/column
w = ws / num
h = hs / num
clock = pygame.time.Clock()
pygame.display.set_caption('Maze Generator')
scrn = pygame.display.set_mode((ws, hs))
white = (255, 255, 255)
purple = (100, 0, 100)


class Cell:
    def __init__(self, c_i, c_j):
        self.i = c_i; self.j = c_j
        self.x = c_j * w; self.y = c_i * h
        self.u = self.d = self.ri = self.le = True
        self.vis = False

    def walls(self, colour):
        if self.vis:
            pygame.draw.rect(scrn, colour, [self.x, self.y, w, h])
        if self.u:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x + w, self.y])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y], [self.x + w - 1, self.y])
        if self.ri:
            pygame.draw.line(scrn, white, [self.x + w, self.y], [self.x + w, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x + w, self.y + 1], [self.x + w, self.y + h - 1])
        if self.d:
            pygame.draw.line(scrn, white, [self.x, self.y + h], [self.x + w, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y + h], [self.x + w - 1, self.y + h])
        if self.le:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x, self.y + h])
        else:
            pygame.draw.line(scrn, colour, [self.x, self.y + 1], [self.x, self.y + h - 1])


neigh = []
cells = []
stack = []
unv_cells = num ** 2

for i in range(num):
    for j in range(num):
        cells.append(Cell(i, j))


# Assigning neighbors
def neighbors(current):
    cu_i = current.i; cu_j = current.j
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


# Starting Position
starting_pos = [0, 0]
cells[starting_pos[0]*num + starting_pos[1]].vis = True
Current_Cell = cells[starting_pos[0]*num + starting_pos[1]]
unv_cells -= 1


def redraw():
    for k in cells:
        k.walls(purple)
        if k == Current_Cell:
            k.walls([0, 0, 255])
        pygame.display.update()


run = end = True
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = end = False
    while run:
        # Conditions to break the run loop
        if unv_cells == 0:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = end = False

        print(clock.tick())
        # Redrawing the screen
        redraw()

        '''--------------------------|
         |   Recursive backtracker   |
         |--------------------------'''

        neigh = neighbors(Current_Cell)
        temp = []
        for i in neigh:
            if not i.vis:
                temp.append(i)

        if temp.__len__():
            rand_neigh = temp[random.randrange(0, temp.__len__())]
            stack.append(Current_Cell)
            # Removing the walls between the current and the selected neighbor cell
            if rand_neigh.i < Current_Cell.i and rand_neigh.j == Current_Cell.j:
                cells[Current_Cell.i*num + Current_Cell.j].u = False
                cells[rand_neigh.i*num + rand_neigh.j].d = False
            if rand_neigh.i == Current_Cell.i and rand_neigh.j > Current_Cell.j:
                cells[Current_Cell.i*num + Current_Cell.j].ri = False
                cells[rand_neigh.i*num + rand_neigh.j].le = False
            if rand_neigh.i > Current_Cell.i and rand_neigh.j == Current_Cell.j:
                cells[Current_Cell.i * num + Current_Cell.j].d = False
                cells[rand_neigh.i * num + rand_neigh.j].u = False
            if rand_neigh.i == Current_Cell.i and rand_neigh.j < Current_Cell.j:
                cells[Current_Cell.i * num + Current_Cell.j].le = False
                cells[rand_neigh.i * num + rand_neigh.j].ri = False
            Current_Cell = rand_neigh
            Current_Cell.vis = True
            unv_cells -= 1
        elif stack.__len__():
            Current_Cell = stack.pop()
        neigh.clear()

pygame.quit()