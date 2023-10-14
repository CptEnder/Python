"""
Created on Fri 19 Jul 22:15 2019
Finished on Thu 01 Aug 16:00 2019
@author: Cpt.Ender

Recursive Backtracker Algorithm v1
                                  """
import pygame, random

pygame.init()

ws = 600
num = 20  # number of cells per row/column
w = ws / num
pygame.display.set_caption('Maze Generator')
clock = pygame.time.Clock()
scrn = pygame.display.set_mode((ws, ws))
white = (255, 255, 255)
purple = (100, 0, 100)


class Cell:
    def __init__(self, c_i, c_j):
        self.neighbors = []
        self.i = c_i; self.j = c_j
        self.x = c_j * w; self.y = c_i * w
        self.u = self.d = self.ri = self.le = True
        self.vis = False;

    def walls(self, colour):
        if self.vis:
            pygame.draw.rect(scrn, colour, [self.x, self.y, w, w])
        if self.u:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x + w, self.y])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y], [self.x + w - 1, self.y])
        if self.ri:
            pygame.draw.line(scrn, white, [self.x + w, self.y], [self.x + w, self.y + w])
        else:
            pygame.draw.line(scrn, colour, [self.x + w, self.y + 1], [self.x + w, self.y + w - 1])
        if self.d:
            pygame.draw.line(scrn, white, [self.x, self.y + w], [self.x + w, self.y + w])
        else:
            pygame.draw.line(scrn, colour, [self.x + 1, self.y + w], [self.x + w - 1, self.y + w])
        if self.le:
            pygame.draw.line(scrn, white, [self.x, self.y], [self.x, self.y + w])
        else:
            pygame.draw.line(scrn, colour, [self.x, self.y + 1], [self.x, self.y + w - 1])

    def neigh(self, a):
        self.neighbors.append(a)


unv_cells = num ** 2
cells = []
stack = []

for i in range(num):
    for j in range(num):
        cells.append(Cell(i, j))

# Assigning neighbors
for i in range(num):
    for j in range(num):
        # Corners
        if i == 0 and j == 0:  # Upper left corner
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])
        if i == 0 and j == num - 1:  # Upper right corner
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])
        if i == num - 1 and j == 0:  # Lower left corner
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])
        if i == num - 1 and j == num - 1:  # Lower right corner
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])

        # Edges
        if i == 0 and j > 0 and j != num - 1:
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])
        if i > 0 and j == num - 1 and i != num - 1:
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])
        if i > 0 and j == 0 and i != num - 1:
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])
        if i == num - 1 and j > 0 and j != num - 1:
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])

        # Middle
        if 0 < i < num - 1 and 0 < j < num-1:
            cells[i*num + j].neigh(cells[i*num + j + 1])
            cells[i*num + j].neigh(cells[i*num + j - 1])
            cells[i*num + j].neigh(cells[(i - 1)*num + j])
            cells[i*num + j].neigh(cells[(i + 1)*num + j])

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
            end = False
    while run:
        # Conditions to break the loop
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
        temp = []
        for i in Current_Cell.neighbors:
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


pygame.quit()
