"""

Created on Thu 08 Aug 00:08 2019
Finished on
@author: Cpt.Ender
                                  """
from Module_Maze_v1 import *

exec(open('Maze Generators and Pathfinders/Module_Maze_v1.py').read())


def next_cell(obj, arg):
    if arg == 0:
        obj = cells[(obj.i - 1)*num + obj.j]
    elif arg == 1:
        obj = cells[obj.i*num + obj.j + 1]
    elif arg == 2:
        obj = cells[(obj.i + 1)*num + obj.j]
    else:
        obj = cells[obj.i*num + obj.j - 1]
    return obj


end = False
visited = []
while not end:
    current_cell = cells[starting_pos[0] * num + starting_pos[1]]
    k = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ending_pos = [int(event.pos[1]/h), int(event.pos[0]/w)]
            for c in visited:
                redraw(c, purple)
            if 'ending_cell' in locals():
                if ending_pos == temp:
                    run = True
                else:
                    redraw(ending_cell, purple)
            ending_cell = cells[ending_pos[0]*num + ending_pos[1]]
            temp = ending_pos
            redraw(ending_cell, [0, 255, 255])

    while run:
        # pygame.time.Clock().tick(40)
        redraw(current_cell, [0, 100, 255])
        visited.append(current_cell)
        if current_cell.ar[k]:
            if k != 3:
                k += 1
            else:
                k = 0
        else:
            current_cell = next_cell(current_cell, k)
            if k != 0:
                k -= 1
            else:
                k = 3

        redraw(current_cell, blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Maze solved
        if current_cell == ending_cell:
            run = False
            print('Maze solved')

pygame.quit()