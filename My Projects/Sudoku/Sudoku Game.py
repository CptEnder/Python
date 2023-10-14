"""
Created on Fri 05 Jun 19:43 2020
Finished on
@author: Cpt.Ender
                                  """
import pygame
from Sudoku_Generator import create as sg

pygame.init()
width = 594
height = 594
height_s = height + 50
pygame.display.set_caption("Sudoku Game.py")
scrn = pygame.display.set_mode((width, height_s))
clock = pygame.time.Clock()
frame_rate = 15
# Fonts
number_font = pygame.font.Font('freesansbold.ttf', 20)
mini_number_font = pygame.font.Font('freesansbold.ttf', 10)
font = pygame.font.Font('freesansbold.ttf', 30)
# Start button
start = font.render('Start', True, (0, 0, 0), (0, 150, 0))
start_rect = start.get_rect()
start_rect.center = [width // 2, height + 25]
start_button = False
# Colors
grey = [180, 180, 180]
white = [255, 255, 255]
blue = [0, 100, 255, 20]
black = [0, 0, 0]


class cell:
    def __init__(self, i_, j_, n_, r):
        self.i = i_
        self.j = j_
        self.x = i_ * width / 9
        self.y = j_ * height / 9
        self.n = n_
        self.shift = 0
        self.mini_n = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.rigid = r  # If it came from the original Sudoku = True
        if self.rigid:
            self.true_color = grey
        else:
            self.true_color = white
        self.color = self.true_color

    def draw(self):
        pygame.draw.rect(scrn, self.color, [int(self.x + 1), int(self.y + 1), width // 9 - 2, height // 9 - 2])
        if self.n != 10:
            number = number_font.render(str(self.n), True, black)
            n_rect = number.get_rect()
            n_rect.center = [int(self.x + width / 9 / 2), int(self.y + height / 9 / 2)]
            scrn.blit(number, n_rect)
        i_ = 0
        j_ = 0
        for k in self.mini_n.keys():
            if self.mini_n[k] != 0 and self.n == 10:
                mini_number = mini_number_font.render(str(k), True, black)
                mini_n_rect = mini_number.get_rect()
                mini_n_rect.center = [int(self.x + i_ % 3 * 15 + 7), int(self.y + j_ * 15 + 7)]
                scrn.blit(mini_number, mini_n_rect)
                i_ += 1
                if i_ % 3 == 0:
                    j_ += 1


def draw(grid, dt=0):
    scrn.fill(black)
    dx = width // 3
    dy = height // 3
    # Drawing the cells
    for i_, row_ in enumerate(grid):
        for j_, n_ in enumerate(row_):
            n_.draw()
    # Drawing the grid lines
    for i_ in range(9):
        if i_ % 3 == 0 and i_ != 0:
            pygame.draw.line(scrn, black, [i_ // 3 * dx, 0], [i_ // 3 * dx, height], 3)
            pygame.draw.line(scrn, black, [0, i_ // 3 * dy], [width, i_ // 3 * dy], 3)
    # Drawing buttons, and info
    scrn.blit(start, start_rect)
    # Timer button
    total_seconds = dt // 1000
    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
    timer = font.render("{0:02}:{1:02}".format(minutes, seconds), True, (200, 200, 200))
    timer_rect = timer.get_rect()
    timer_rect.center = [width // 3 * 2, height + 25]
    scrn.blit(timer, timer_rect)

    pygame.display.update()


def exiting(k):
    # Exiting the program
    if k[pygame.K_ESCAPE]:  # To exit press 'Esc'
        return False
    return True


def create():
    filled, sudoku = sg()
    # Creating a grid of cells
    grid = []
    for j_ in range(9):
        grid.append([])
        for i_, n in enumerate(sudoku[j_]):
            if n == 0:
                grid[j_].append(cell(i_, j_, 10, False))
            else:
                grid[j_].append(cell(i_, j_, n, True))
    return filled, sudoku, grid


def events():
    global Filled, Sudoku, Grid, start_button, start, shift
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            # Moving around with arrow keys
            if event.key == pygame.K_UP and cell_pos[0] != 0:
                cell_pos[0] -= 1
            elif event.key == pygame.K_DOWN and cell_pos[0] != 8:
                cell_pos[0] += 1
            elif event.key == pygame.K_RIGHT and cell_pos[1] != 8:
                cell_pos[1] += 1
            elif event.key == pygame.K_LEFT and cell_pos[1] != 0:
                cell_pos[1] -= 1
            # --------------------------------------------------------------- #
            elif event.key == pygame.K_n:  # Pressing 'N' creates a new Sudoku
                Filled, Sudoku, Grid = create()
                start = font.render('Start', True, [0, 0, 0], [0, 150, 0])
                start_button = False
            if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                shift += 1
            # ------------------- NumberInputs ------------------- #
            if event.key in [pygame.K_BACKSPACE, pygame.K_0, pygame.K_KP0]:
                shift += 1
                return 10
            if event.key in [pygame.K_1, pygame.K_KP1]:
                return 1
            if event.key in [pygame.K_2, pygame.K_KP2]:
                return 2
            if event.key in [pygame.K_3, pygame.K_KP3]:
                return 3
            if event.key in [pygame.K_4, pygame.K_KP4]:
                return 4
            if event.key in [pygame.K_5, pygame.K_KP5]:
                return 5
            if event.key in [pygame.K_6, pygame.K_KP6]:
                return 6
            if event.key in [pygame.K_7, pygame.K_KP7]:
                return 7
            if event.key in [pygame.K_8, pygame.K_KP8]:
                return 8
            if event.key in [pygame.K_9, pygame.K_KP9]:
                return 9


Filled, Sudoku, Grid = create()


keys = pygame.key.get_pressed()
cell_pos = [0, 0]
shift = -1
while exiting(keys):
    tik = pygame.time.get_ticks()
    clock.tick(frame_rate)
    # -------------------- Moving Around -------------------- #
    mouse_pos = pygame.mouse.get_pos()
    Grid[cell_pos[0]][cell_pos[1]].color = Grid[cell_pos[0]][cell_pos[1]].true_color
    number_input = events()
    # If left click is pressed and the mouse is inside the grid
    if pygame.mouse.get_pressed(3) != (0, 0, 0) and max(mouse_pos) < width:
        # Convert mouse position to cell position
        cell_pos = [mouse_pos[1] * 9 // width, mouse_pos[0] * 9 // height]

    # Marking the current selected cell with blue
    Grid[cell_pos[0]][cell_pos[1]].color = blue

    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed(3) == (1, 0, 0) and start_rect.collidepoint(mouse_pos) \
            and not start_button:
        # If Start button is pressed
        start_button = True
        start = font.render('Start', True, [0, 0, 0], [150, 0, 0])
        start_time = pygame.time.get_ticks()

    # If the cell is not an original, and the game has started, change its number
    if start_button and number_input and cell_pos and not Grid[cell_pos[0]][cell_pos[1]].rigid:
        num = number_input
        if shift % 2 == 0 and num != 10:
            if Grid[cell_pos[0]][cell_pos[1]].mini_n[num] == 0:
                Grid[cell_pos[0]][cell_pos[1]].mini_n[num] = 1
            else:
                Grid[cell_pos[0]][cell_pos[1]].mini_n[num] = 0
        else:
            Grid[cell_pos[0]][cell_pos[1]].n = num
            Sudoku[cell_pos[0]][cell_pos[1]] = num

    if Filled == Sudoku:
        print("Wiiiiiiiiiiiiiii")

    if start_button:
        draw(Grid, pygame.time.get_ticks() - start_time)
    else:
        draw(Grid)

    # print('fps = ', 1 / (pygame.time.get_ticks() - tik) * 1000)

pygame.quit()
