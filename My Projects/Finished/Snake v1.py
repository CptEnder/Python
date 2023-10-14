# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:53:27 2019

@author: plabc
"""
import pygame, random

pygame.init()

w_s = 500;
h_s = 500;
pygame.display.set_caption("Snake")
win = pygame.display.set_mode((w_s, h_s))
clock = pygame.time.Clock()


class s_part():
    def __init__(self, x, y):
        self.w = w_s // 50;
        self.h = h_s // 50
        self.x = [x];
        self.y = [y]
        self.vx = 0;
        self.vy = 0
        self.colour = (0, 0, 255)

    def draw(self, win, it1):
        pygame.draw.rect(win, self.colour, (self.x[it1], self.y[it1], self.w, self.h))


part = s_part(w_s // 2 - w_s // 100, h_s // 2 - h_s // 100)
snake = [part]

r = 4


class apple():
    def __init__(self, x, y):
        self.x = x;
        self.y = y
        self.r = r

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.r)


ap = apple(random.randint(r, w_s // 2 - r) * 2, random.randint(r, h_s // 2 - r) * 2)


def redrawscrn(it):
    ap.draw(win)
    for part in snake:
        k = snake.index(part)
        part.draw(win, it[k])
    pygame.display.update()
    win.fill((0, 0, 0))


run = True
v = part.w // 2;
fps = 20
it = [0];
it1 = 0;
color = [(0, 0, 255)]
while run:
    clock.tick(fps)
    keys = pygame.key.get_pressed()

    # Window-------------------------------------------------------------------
    if keys[pygame.K_ESCAPE]:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Snake--------------------------------------------------------------------
    if keys[pygame.K_LEFT]:
        snake[0].vx = -v;
        snake[0].vy = 0;
        ix = 1;
        iy = 0
    elif keys[pygame.K_RIGHT]:
        snake[0].vx = v;
        snake[0].vy = 0;
        ix = -1;
        iy = 0
    elif keys[pygame.K_UP]:
        snake[0].vx = 0;
        snake[0].vy = -v;
        ix = 0;
        iy = 1
    elif keys[pygame.K_DOWN]:
        snake[0].vx = 0;
        snake[0].vy = v
        ix = 0;
        iy = -1

    for part in snake:
        k = snake.index(part)
        if k == 0:
            snake[k].x.append(snake[k].x[it[k]] + part.vx)
            snake[k].y.append(snake[k].y[it[k]] + part.vy)
        else:

            snake[k].x.append(snake[k - 1].x[it[k - 1] - 2])
            snake[k].y.append(snake[k - 1].y[it[k - 1] - 2])

    # Collision with apple-----------------------------------------------------
    reqy1 = ap.y - snake[0].y[it[0]];
    reqy2 = snake[0].y[it[0]] + part.h - ap.y
    reqx1 = ap.x - snake[0].x[it[0]];
    reqx2 = snake[0].x[it[0]] + part.w - ap.x
    if reqy1 <= part.h and reqy2 <= part.h:
        if reqx1 <= part.w and reqx2 <= part.w:
            ap = apple(random.randint(ap.r, w_s // 2 - ap.r) * 2, random.randint(ap.r, h_s // 2 - ap.r) * 2)
            snake.append(s_part(snake[it1].x[it[it1] - 2],
                                snake[it1].y[it[it1] - 2]))
            it1 += 1
            it.append(0)
            #            print(it[it1-1])
            snake[it1].colour = (255, 255, 255)

    # Collision with wall------------------------------------------------------  
    if snake[0].x[it[0]] < 0 or snake[0].x[it[0]] + part.w > w_s:
        run = False
    elif snake[0].y[it[0]] < 0 or snake[0].y[it[0]] + part.h > h_s:
        run = False

    redrawscrn(it)
    it[:] = [i + 1 for i in it]
pygame.quit()
