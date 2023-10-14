"""
Created on Fri 07 Aug 10:46 2020
Finished on Fri 07 Aug 16:00 2020
@author: Cpt.Ender
                                  """
import pygame
from random import choices

pygame.init()
width_s = 1200
height_s = 600
pygame.display.set_caption("Cellular Automata Method.py")
scrn = pygame.display.set_mode((width_s + 1, height_s + 1))
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
black = [0] * 3
white = [255] * 3
gray = [80] * 3
rez = 50  # number of rectangles in a row/column
rect_w = width_s // rez  # width of each rectangle
rect_h = height_s // rez  # height of each rectangle
wall_prob = 0.4  # probability of a cell being a wall


class rect:
    def __init__(self, i, j, width, height):
        self.w = width
        self.h = height
        self.i = i
        self.j = j
        self.n = self.j * rez + self.i
        self.c1 = [self.i * width, self.j * height]  # coordinates of upper left corner
        self.c2 = [self.c1[0] + width, self.c1[1]]  # coordinates of upper right corner
        self.c3 = [self.c1[0] + width, self.c1[1] + height]  # coordinates of lower right corner
        self.c4 = [self.c1[0], self.c1[1] + height]  # coordinates of lower left corner
        self.corner_list = [self.c1, self.c2, self.c3, self.c4]
        self.neighbors = []  # the neighbor rectangles
        self.value = None  # 0 = wall, 1 = empty space

    def draw(self):
        if self.value == 1:
            pygame.draw.rect(scrn, white, [self.c1, [self.w, self.h]])


def running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def draw(rects):
    scrn.fill(black)  # Background Colour
    for rct in rects:
        rct.draw()
    for i in range(rez + 1):
        pygame.draw.line(scrn, gray, [i * rect_w, 0], [i * rect_w, height_s])
        pygame.draw.line(scrn, gray, [0, i * rect_h], [width_s, i * rect_h])
    pygame.display.update()


def init():
    rects = []  # A list of all the squares
    for j in range(rez):
        for i in range(rez):
            if not rez - 1 > i > 0 or not rez - 1 > j > 0:
                # If it's a border make it a wall
                value_list[i + j * rez] = 0
            rects.append(rect(i, j, rect_w, rect_h))
            rects[i + j * rez].value = value_list[i + j * rez]

    # Appending neighbors
    for i in range(1, rez - 1):
        for j in range(1, rez - 1):
            up_left = (i - 1) * rez + j - 1
            up = (i - 1) * rez + j
            up_right = (i - 1) * rez + j + 1
            left = i * rez + j - 1
            right = i * rez + j + 1
            down_left = (i + 1) * rez + j - 1
            down = (i + 1) * rez + j
            down_right = (i + 1) * rez + j + 1

            rects[i * rez + j].neighbors += [up_left, up, up_right, left, right,
                                             down_left, down, down_right]

    return rects


def change(rects):
    temp_v_lst = value_list
    for rct in rects:
        number_of_walls = 0
        for n in rects[rct.n].neighbors:
            if rects[n].value == 0:
                number_of_walls += 1
        if number_of_walls > 4:
            # If there are more than 4 nearby walls change to wall
            temp_v_lst[rct.n] = 0
        elif number_of_walls < 4:
            temp_v_lst[rct.n] = 1
    return temp_v_lst


if __name__ == '__main__':
    value_list = choices([0, 1], [wall_prob, 1 - wall_prob], k=rez ** 2)
    original_v_list = value_list[:]
    Rects = init()
    iterations = 0
    while running():
        # if pygame.key.get_pressed()[pygame.K_SPACE]:
        if iterations < 6:
            value_list = change(Rects)
            Rects = init()
            pygame.time.wait(300)
        if pygame.key.get_pressed()[pygame.K_LCTRL]:
            value_list = original_v_list[:]
            Rects = init()
            pygame.time.wait(300)
            iterations = 0
        elif pygame.key.get_pressed()[pygame.K_r]:
            value_list = choices([0, 1], [wall_prob, 1 - wall_prob], k=rez ** 2)
            original_v_list = value_list[:]
            Rects = init()
            pygame.time.wait(300)
            iterations = 0
        iterations += 1
        draw(Rects)
    pygame.quit()
