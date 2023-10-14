"""
Created on Sun 01 May 17:00:00 2019
Finished on
@author: Cpt.Ender
"""

import pygame

pygame.init()

ws = 640
hs = 640
boxes = 16
pygame.display.set_caption('Game of Life')
scrn = pygame.display.set_mode((ws, hs))


def redrawscrn(w):
    scrn.fill((130, 130, 130))
    for i in range(1, w):
        pygame.draw.line(scrn, (0, 0, 0), (i*ws/w, 0), (i*ws/w, hs), 1)
        pygame.draw.line(scrn, (0, 0, 0), (0, i*ws/w), (ws, i*ws/w), 1)
    pygame.display.update()


run = True
while run:
    redrawscrn(boxes)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == 27 and event.unicode == '\x1b':
                run = False
                break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if boxes > 5:
                    boxes -= 1
            elif event.button == 5:
                boxes += 1
            print(boxes)

pygame.quit()
