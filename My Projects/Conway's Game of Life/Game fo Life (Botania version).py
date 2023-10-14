"""
Created on Sun 04 May 13:00:00 2019
Finished on Wen 08 May 20:00:00 2019
@author: Cpt.Ender
"""

import pygame
from math import floor

pygame.init()

w_game = 625; h_game = 625
w_scrn = w_game
h_scrn = 680
High_Score = 0
clock = pygame.time.Clock()
pygame.display.set_caption('Game of Life')
scrn = pygame.display.set_mode((w_scrn, h_scrn))

font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 20)
start = font.render('Start', True, (0, 0, 0), (0, 150, 0))
start_rect = start.get_rect()
start_rect.center = (150+150//2, 630+45//2)
reset = font.render('Reset', True, (0, 0, 0), (200, 0, 0))
reset_rect = reset.get_rect()
reset_rect.center = (325+150//2, 630+45//2)
clear = font.render('Clear', True, (0, 0, 0), (0, 150, 150))
clear_rect = clear.get_rect()
clear_rect.center = (500+150//2, 630+45//2)


def game_start(alives, deads):
    global run, Score, High_Score
    game = True
    l_boxes = alives+[]
    d_boxes = deads+[]

    while game:
        clock.tick(2)
        redrawscrn(l_boxes)

        if len(l_boxes) == 0:
            game = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                game = False
            if e.type == pygame.KEYDOWN:
                if e.key == 27 and e.unicode == '\x1b':
                    run = False
                    game = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if reset_rect[0]+reset_rect[2] >= e.pos[0] >= reset_rect[0]\
                        and reset_rect[1]+reset_rect[3] >= e.pos[1] >= reset_rect[1]:
                    game = False
                    l_boxes.clear(); d_boxes.clear()

        l_new_boxes = []
        d_new_boxes = []

        for i in d_boxes:
            neighbors = 0
            age = 0
            for ii in l_boxes:
                if abs(i[0] - ii[0]) <= 1 and abs(i[1] - ii[1]) <= 1:
                    neighbors += 1
                    print(i, 'Neighbors: ', neighbors, ii)
                    if ii[2] > age:
                        age = ii[2]
            if neighbors == 3:
                l_new_boxes.append(i+[age])
            else:
                d_new_boxes.append(i)

        for i in l_boxes:
            neighbors = 0
            print(i)
            for ii in l_boxes:
                if i != ii:
                    if abs(i[0] - ii[0]) <= 1 and abs(i[1] - ii[1]) <= 1:
                        neighbors += 1
                        print('Neigh: ', neighbors, ii)
            if neighbors < 2 or neighbors > 3 or i[2] > 60\
                    or (abs(i[0] - 12) < 2 and abs(i[1] - 12) < 2):
                d_new_boxes.append(i[0:2])
            else:
                l_new_boxes.append(i[0:2]+[i[2]+1])
            if abs(i[0] - 12) < 2 and abs(i[1] - 12) < 2:
                Score += 1
        if Score > High_Score:
            High_Score = Score
        d_boxes = d_new_boxes + []
        l_boxes = l_new_boxes + []


def redrawscrn(tiles):
    # Paints the background of the game
    scrn.fill((130, 130, 130))
    # pygame.draw.rect(scrn, (0, 150, 0), [150, 630, 150, 45])
    # pygame.draw.rect(scrn, (200, 0, 0), [325, 630, 150, 45])
    scrn.blit(start, start_rect)
    scrn.blit(reset, reset_rect)
    scrn.blit(clear, clear_rect)
    score = font2.render('Score = ' + str(Score), True, (0, 0, 0), (0, 0, 150))
    score_rect = score.get_rect()
    score_rect.center = (150 // 2, 630 + 25 // 2)
    scrn.blit(score, score_rect)
    high_score = font2.render('High Score = ' + str(High_Score), True, (0, 0, 0), (0, 0, 150))
    high_score_rect = high_score.get_rect()
    high_score_rect.center = (150 // 2, 630 + 65 // 2)
    scrn.blit(high_score, high_score_rect)

    for i in range(26):
        if i == 11:
            pygame.draw.rect(scrn, (0, 0, 255), [i*w_game//25, i*w_game//25, 3*w_game//25, 3*w_game//25])
        if i == 12:
            pygame.draw.rect(scrn, (255, 0, 0), [i*w_game//25+2, i*w_game//25+2, w_game//25, w_game//25])
        pygame.draw.line(scrn, (0, 0, 0), (i*w_game//25, 0), (i*w_game//25, h_game), 2)
        pygame.draw.line(scrn, (0, 0, 0), (0, i*w_game//25), (w_game, i*w_game//25), 2)
    # Paints the player choices
    for i in tiles:
        pygame.draw.rect(scrn, (0, 0, 0), [i[0]*w_game//25 + 2, i[1]*w_game // 25 + 2, w_game//25, w_game//25])
    pygame.display.update()


run = True
alive = []
dead = []
while run:
    Score = 0
    paint = True; remove = False
    redrawscrn(alive)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == 27 and event.unicode == '\x1b':
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x = floor(event.pos[0] // 25)
            pos_y = floor(event.pos[1] // 25)
            dead = []
            for i in range(25):
                for j in range(25):
                    add = True
                    if i == j == 12:
                        add = False
                    for ii in range(len(alive)):
                        if alive[ii][0:2] == [j, i]:
                            add = False
                            break
                    if add:
                        dead.append([j, i])
            for i in range(len(alive)):
                if alive[i][0:2] == [pos_x, pos_y]:
                    paint = False; remove = True; index = i
            if event.button == 1:
                if pos_y < 25 and (not abs(pos_x - 12) < 2 or not abs(pos_y - 12) < 2):
                    if paint:
                        alive.append([pos_x, pos_y, 0])
                if clear_rect[0]+clear_rect[2] >= event.pos[0] >= clear_rect[0]\
                        and clear_rect[1]+clear_rect[3] >= event.pos[1] >= clear_rect[1]:
                    alive.clear()
                if start_rect[0]+start_rect[2] >= event.pos[0] >= start_rect[0]\
                        and start_rect[1]+start_rect[3] >= event.pos[1] >= start_rect[1]:
                    game_start(alive, dead)
            if event.button == 3:
                if remove and len(alive) > 0:
                    alive.pop(index)
            print(alive)

pygame.quit()
