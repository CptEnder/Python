# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:04:31 2019

@author: plabc
"""

# helpful website https://www.pygame.org/docs/

import pygame
pygame.init()
clock = pygame.time.Clock()

w = 500
h = 500
pygame.display.set_caption("First Game")
scrn = pygame.display.set_mode((w,h))

ch_x = 20;ch_y = 20
ch_h = 15;ch_w = 15
v = 5
run = True
while run:
    clock.tick(70)
    pygame.draw.rect(scrn,(0,255,0),(ch_x,ch_y,ch_w,ch_h))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ch_x = ch_x - v
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ch_x = ch_x + v
    if keys[pygame.K_UP] or keys[pygame.K_w]:
            ch_y = ch_y - v
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ch_y = ch_y + v
    pygame.display.update()
    scrn.fill((0, 0, 0))

pygame.quit()