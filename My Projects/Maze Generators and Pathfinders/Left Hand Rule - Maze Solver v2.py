"""
Created on Thu 30 Jul 17:08 2020
Finished on Thu 30 Jul 18:53 2020
@author: Cpt.Ender
                                  """
import pygame
from Module_Maze_v2 import amaze

pygame.init()
width = 1200
height = 600
pygame.display.set_caption("Left Hand Rule - Maze Solver v2.py")
scrn = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
black = [0] * 3
white = [255] * 3
num = 15  # number of cells per row/column
frameR = 15


def running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def next_cell(cells, obj, arg):
    if arg == 0:
        obj = cells[(obj.i - 1) * num + obj.j]
    elif arg == 1:
        obj = cells[obj.i * num + obj.j + 1]
    elif arg == 2:
        obj = cells[(obj.i + 1) * num + obj.j]
    else:
        obj = cells[obj.i * num + obj.j - 1]
    return obj


def cell_update(cell, colour):
    # A function to update a specific's cell colour
    pygame.draw.rect(scrn, colour, [cell.x, cell.y, w, h])
    if cell.ar[0]:
        pygame.draw.line(scrn, white, [cell.x, cell.y], [cell.x + w, cell.y])
    else:
        pygame.draw.line(scrn, colour, [cell.x + 1, cell.y], [cell.x + w - 1, cell.y])
    if cell.ar[1]:
        pygame.draw.line(scrn, white, [cell.x + w, cell.y], [cell.x + w, cell.y + h])
    else:
        pygame.draw.line(scrn, colour, [cell.x + w, cell.y + 1], [cell.x + w, cell.y + h - 1])
    if cell.ar[2]:
        pygame.draw.line(scrn, white, [cell.x, cell.y + h], [cell.x + w, cell.y + h])
    else:
        pygame.draw.line(scrn, colour, [cell.x + 1, cell.y + h], [cell.x + w - 1, cell.y + h])
    if cell.ar[3]:
        pygame.draw.line(scrn, white, [cell.x, cell.y], [cell.x, cell.y + h])
    else:
        pygame.draw.line(scrn, colour, [cell.x, cell.y + 1], [cell.x, cell.y + h - 1])
    pygame.display.update()


def draw(cells, c_list):
    scrn.fill(black)  # Background Colour
    for index in c_list:
        cell = cells[index]
        cell_update(cell, cell.colour)


if __name__ == '__main__':
    w = width // num
    h = height // num
    maze_solving = False
    starting_pos = [0, 0]
    visited = []

    maze, list_of_creation = amaze(width, height, num, starting_pos)
    temp = maze[0]
    draw(maze, list_of_creation)
    while running():
        if pygame.key.get_pressed()[pygame.K_r]:
            maze, list_of_creation = amaze(width, height, num, starting_pos)
            draw(maze, list_of_creation)
            pygame.time.wait(500)
        if pygame.mouse.get_pressed() != (0, 0, 0):
            ending_pos = [pygame.mouse.get_pos()[1] // h, pygame.mouse.get_pos()[0] // w]
            ending_cell = maze[ending_pos[0] * num + ending_pos[1]]
            for cell_vis in visited:
                cell_update(cell_vis, cell_vis.colour)
            if ending_cell == temp:
                maze_solving = True
            else:
                cell_update(ending_cell, [0, 255, 255])
                cell_update(temp, temp.colour)
            temp = ending_cell
            visited = []
            pygame.time.wait(200)

        '''Solving the maze '''
        current_cell = maze[starting_pos[0] * num + starting_pos[1]]
        k = 0
        while maze_solving:
            clock.tick(frameR)
            cell_update(current_cell, [0, 100, 255])
            visited.append(current_cell)
            if current_cell.ar[k]:
                if k != 3:
                    k += 1
                else:
                    k = 0
            else:
                current_cell = next_cell(maze, current_cell, k)
                if k != 0:
                    k -= 1
                else:
                    k = 3

            cell_update(current_cell, [0, 0, 255])
            # Maze solved
            if current_cell == ending_cell or not running():
                maze_solving = False
                print('Maze solved')
    pygame.quit()
