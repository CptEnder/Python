"""
Created on Sun 26 Jul 17:28 2020
Finished on Thu 30 Jul 14:00 2020
@author: Cpt.Ender

Notes: Add noise function for the values of
       points instead of using the random lib
                                                """
import pygame
from random import random as rand

pygame.init()
width = 600
height = 600
pygame.display.set_caption("Marching Squares.py")
scrn = pygame.display.set_mode((width + 1, height + 1))
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
black = [0] * 3
white = [255] * 3
gray = [80] * 3
purple = (100, 0, 100)
fill_colour = (0, 120, 0)  # filling colour
rez = 21  # number of points in each row an column
sqr_w = width // (rez - 1)  # width of each square


class point:
    def __init__(self, i_, j_):
        self.i = j_
        self.j = i_
        self.x = i_ * sqr_w
        self.y = j_ * sqr_w
        self.value = round(rand())  # Change to noise function

    def draw(self):
        # r = 5  # radius
        if self.value == 0:
            pygame.draw.polygon(scrn, fill_colour, [[self.x, self.y + sqr_w // 2],
                                                    [self.x + sqr_w // 2, self.y],
                                                    [self.x, self.y - sqr_w // 2],
                                                    [self.x - sqr_w // 2, self.y],
                                                    [self.x, self.y + sqr_w // 2]], 0)
            # pygame.draw.circle(scrn, black, [self.x, self.y], r)
        else:
            # pygame.draw.circle(scrn, white, [self.x, self.y], r)
            pass


class square:
    def __init__(self, p1: point, p2: point, p3: point, p4: point):
        self.c1 = p1  # coordinates of upper left corner
        self.c2 = p2  # coordinates of upper right corner
        self.c3 = p3  # coordinates of lower right corner
        self.c4 = p4  # coordinates of lower left corner
        self.corner_list = [self.c1, self.c2, self.c3, self.c4]
        self.a = [(p1.x + p2.x) // 2, p1.y]  # midpoint between c1 and c2
        self.b = [p2.x, (p2.y + p3.y) // 2]  # midpoint between c2 and c3
        self.c = [(p3.x + p4.x) // 2, p3.y]  # midpoint between c3 and c4
        self.d = [p4.x, (p1.y + p4.y) // 2]  # midpoint between c1 and c4
        self.values = [c.value for c in self.corner_list]  # The 4 values of the corners
        # Values of the midpoints (average between the two corners)
        self.a_v = (p1.value + p2.value) / 2
        self.b_v = (p2.value + p3.value) / 2
        self.c_v = (p3.value + p4.value) / 2
        self.d_v = (p4.value + p1.value) / 2
        self.mid_values = [self.a_v, self.b_v, self.c_v, self.d_v]
        self.mid_list = [self.a, self.b, self.c, self.d]

    def draw(self):
        # Filling the space between midpoints with colour
        temp = self.values[:]
        temp.sort()
        if temp[2] == 0:  # if 3 or more corners are 0 (black)
            pygame.draw.polygon(scrn, fill_colour, [self.a, self.b,
                                                    self.c, self.d, self.a])

        # Drawing the connections and filling the space between midpoints with value of 0.5
        if self.mid_values.count(0.5) == 2:
            # finding the positions of the midpoints with value 0.5
            [i_1, i_2] = duplicates(self.mid_values, 0.5)
            point_1 = self.mid_list[i_1]
            point_2 = self.mid_list[i_2]
            if self.mid_values.count(0) == 1:
                # finding the position of the midpoint with value 1
                [i_0] = duplicates(self.mid_values, 0)
                point_0 = self.mid_list[i_0]
                pygame.draw.polygon(scrn, fill_colour, [point_0, point_1, point_2, point_0])
            pygame.draw.line(scrn, purple, point_1, point_2)
        elif self.mid_values.count(0.5) == 4:
            # pygame.draw.polygon(scrn, fill_colour, [self.a, self.b,
            #                                         self.c, self.d, self.a])

            # If the upper left corner value is 0
            if self.values[0] == 0:
                pygame.draw.aaline(scrn, purple, self.a, self.d)
                pygame.draw.aaline(scrn, purple, self.b, self.c)
            else:
                pygame.draw.aaline(scrn, purple, self.a, self.b)
                pygame.draw.aaline(scrn, purple, self.c, self.d)


def duplicates(lst, item):
    return [i_ for i_, x in enumerate(lst) if x == item]


def running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def draw(points, squares):
    scrn.fill(gray)  # Background Colour
    # Grid lines
    for i in range(rez + 1):
        pygame.draw.line(scrn, white, [i * sqr_w, 0], [i * sqr_w, height])
        pygame.draw.line(scrn, white, [0, i * sqr_w], [width, i * sqr_w])
    for p in points:
        p.draw()
    for sq in squares:
        sq.draw()
    pygame.display.update()


def init():
    squares = []  # A list of all the squares
    points = []  # A list of all the points
    for i in range(rez):
        for j in range(rez):
            points.append(point(j, i))

    for i in range(rez - 1):
        for j in range(rez - 1):
            squares.append(square(points[i * rez + j], points[i * rez + j + 1],
                                  points[i * rez + j + 1 + rez], points[i * rez + j + rez]))
    return points, squares


if __name__ == '__main__':
    Points, Squares = init()
    while running():
        draw(Points, Squares)
        if pygame.key.get_pressed()[pygame.K_r]:
            Points, Squares = init()
            pygame.time.wait(300)
    pygame.quit()
