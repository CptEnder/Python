"""
Created on Sun 12 Jan 22:21 2020
Finished on Wed 16 Jan 00:30 2020
@author: Cpt.Ender
                                  """
import pygame, time, math
from random import randint as rand

pygame.init()
width = 600
height = 600
pygame.display.set_caption("2D Ray Casting")
scrn = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
white = (150, 150, 150, 1)


class obstacles:
    def __init__(self, s_pos, length, f):
        self.point1 = s_pos
        self.length = length
        self.sinf = math.sin(math.radians(f))
        self.cosf = math.cos(math.radians(f))
        self.point2 = (s_pos[0] + self.cosf*length, s_pos[1] + self.sinf*length)

    def draw(self):
        pygame.draw.aaline(scrn, (0, 0, 255), self.point1, self.point2)


def random_walls(n):
    if walls.__len__() > 4:
        del walls[4:]
    for i in range(n):
        walls.append(obstacles((rand(30, 470), rand(30, 470)), rand(100, 200), rand(0, 360)))


def cross_product(p1, p2):
    return p1[0]*p2[1] - p1[1]*p2[0]


def get_intersect_point(a, b, c, d):
    r = [b[0] - a[0], b[1] - a[1]]
    s = [d[0] - c[0], d[1] - c[1]]

    rxs = cross_product(r, s)
    temp1 = [c[0] - a[0], c[1] - a[1]]
    if rxs != 0:  # if the lines are not parallel
        t = cross_product(temp1, s)/rxs
        u = cross_product(temp1, r)/rxs

        if 0 <= t <= 1 and 0 <= u <= 1:  # if there is an intersecting point
            x = a[0] + t*r[0]
            y = a[1] + t*r[1]
            return x, y


def redraw(pos):
    scrn.fill((0, 0, 0))
    if Show_area:  # draw the area
        pygame.draw.polygon(scrn, (100, 100, 0, 50), polygon_point_lst, 0)
        pygame.draw.circle(scrn, white, pos, 5, 0)
    else:  # draw individual rays
        for r in rays:
            pygame.draw.line(scrn, white, r[0], r[1])
        pygame.draw.circle(scrn, (150, 150, 0), pos, 5, 0)
    for wall in walls:
        wall.draw()
    pygame.display.update()


# Initial conditions
th_s = 0
th_e = 180  # actual th_end*2
step = int((th_e-th_s)/th_e)

walls = [obstacles((0, 0), width, 0), obstacles((0, 0), height, 90),
         obstacles((width-1, 0), height, 90), obstacles((0, height-1), width, 0)]  # screen edges
random_walls(5)  # adding random walls

Show_area = False
run = True

while run:
    ts = time.time()
    # Exiting the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:  # To exit press 'Esc'
        break
    elif keys[pygame.K_a]:  # To rotate clockwise press 'A'
        time.sleep(0.05)
        th_s += 9
        th_e += 9
    elif keys[pygame.K_d]:  # To rotate counter clockwise press 'D'
        time.sleep(0.05)
        th_s -= 9
        th_e -= 9
    elif keys[pygame.K_SPACE]:  # To change between area or ray mode press 'Space_Bar'
        time.sleep(0.1)
        if Show_area:
            Show_area = False
        else:
            Show_area = True
    elif keys[pygame.K_r]:  # To recreate random walls press 'R'
        time.sleep(0.1)
        random_walls(5)
    elif keys[pygame.K_w]:  # To add 10 more degrees press 'W'
        if abs(th_e - th_s) < 720:
            th_e += step
    elif keys[pygame.K_s]:  # To remove 10 more degrees press 'S'
        if abs(th_e - th_s) > 10:
            th_e -= step
    rays = []
    polygon_point_lst = []
    current_pos = pygame.mouse.get_pos()
    for th in range(th_s, th_e+1, step):
        sinth = math.sin(math.radians(th/2))
        costh = math.cos(math.radians(th/2))
        max_pos = [current_pos[0] + costh*width**2, current_pos[1] + sinth*height**2]
        end_pos_lst = []
        max_dis = math.sqrt((current_pos[0]-max_pos[0])**2 + (current_pos[1] - max_pos[1])**2)

        for w in walls:
            end_pos = None
            point = get_intersect_point(current_pos, max_pos, w.point1, w.point2)
            if point:  # if an intersecting point exist, add it to a list
                end_pos_lst.append(point)

        # From the list of intersecting points, choose the one with the smallest distance
        for p in end_pos_lst:
            dis = math.sqrt((current_pos[0]-p[0])**2 + (current_pos[1] - p[1])**2)
            if dis < max_dis:
                max_dis = dis
                end_pos = p

        if end_pos_lst:
            rays.append([current_pos, end_pos])
            polygon_point_lst.append(end_pos)

    polygon_point_lst.append(current_pos)
    redraw(current_pos)
    if time.time() - ts > 0:
        print('fps = ', 1//(time.time() - ts))

pygame.quit()
