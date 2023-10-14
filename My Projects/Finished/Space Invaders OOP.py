# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:15:05 2019

@author: plabc
"""

import pygame, math, random
pygame.init()

w_s = 1000
h_s = 600
pygame.display.set_caption("Space Invaders.py")
scrn = pygame.display.set_mode((w_s, h_s))
clock = pygame.time.Clock()

iii = [1, -1]; ii = iii[random.randint(0, 1)]
score = 0; it = 0; fps = 30
le = []
run = True


class UFO:
    def __init__(self, w, h, ii):
        self.w = w; self.h = h
        self.x = random.randint(0+2, w_s-w-2); self.y = 50
        self.v = ii*w//6

    def draw(self):
        pygame.draw.ellipse(scrn, (255, 255, 255), [self.x, self.y, self.w, self.h])


ufo = UFO(30, 20, ii)


class player:
    def __init__(self, w, h):
        self.w = w;self.h = h
        self.x = w_s/2-w;self.y = h_s-20
        self.v = ufo.w//4

    def draw(self):
        pygame.draw.rect(scrn, (0, 255, 0), (self.x, self.y, self.w, self.h))


ch = player(15, 15)


class projectile:
    def __init__(self):
        self.r = 4;self.v = 30
        self.x = round(ch.x+ch.w/2);self.y = round(ch.y-2*self.r)

    def draw(self):
        pygame.draw.circle(scrn, (0, 0, 255), (self.x, self.y), self.r)


bul = projectile()
bullets = []


class ufobullet:
    def __init__(self):
        self.r = 4; self.v = 10
        self.x = ufo.x+ufo.w//2; self.y = ufo.y+ufo.h+2*self.r

    def draw(self):
        pygame.draw.circle(scrn, (255, 0, 0), (round(self.x), round(self.y)), self.r)


ubul = ufobullet()
ubullets = []


def redrawscrn():
    ch.draw()
    ufo.draw()
    for ubul in ubullets:
        ubul.draw()
    for bul in bullets:
        bul.draw()
    
    pygame.display.update()
    scrn.fill((0, 0, 0))


while run:
    clock.tick(fps+5*score)
    keys = pygame.key.get_pressed()
    # Window-----------------------------------------
    if keys[pygame.K_ESCAPE]:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Ufo -------------------------------------------
    if math.isclose(ufo.x, 0, abs_tol=abs(ufo.v)):
        ufo.v = -ufo.v    
    elif math.isclose(ufo.x, w_s-ufo.w, abs_tol=abs(ufo.v)):
        ufo.v = -ufo.v 
    ufo.x += ufo.v
    # Player-----------------------------------------
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if math.isclose(ch.x, 0, abs_tol=2):
            ch.x = ch.x
        else:
            ch.x -= ch.v
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if math.isclose(ch.x+ch.w, w_s, abs_tol=3):
            ch.x = ch.x
        else:
            ch.x += ch.v
    # Player Bullets------------------------------------------
    for bul in bullets:
        if bul.y > 0:
            bul.y -= bul.v
        else:
            bullets.pop(bullets.index(bul))
        reqy = math.isclose(bul.y, ufo.y+ufo.h/2, abs_tol=ufo.h/2)
        reqx = math.isclose(bul.x, ufo.x+ufo.w//2, abs_tol=ufo.w/2)
        if reqy and reqx:
            bullets.pop(bullets.index(bul))
            ufo.x = random.randint(0+2, w_s-ufo.w-2)
            ufo.v = iii[random.randint(0, 1)]*ufo.v
            ubullets.clear()
            score += 1
            print(score)
    if keys[pygame.K_SPACE]:
        if len(bullets) < 2 and it % 5 == 0:
            bullets.append(projectile())
    # Ufo Bullets------------------------------------------
    it += 1
    if it % (fps//2) == 0:
        if len(ubullets) < 10:
            ubullets.append(ufobullet())
#            chx0.append(ch.x);ufox0.append(ufo.x)
#            l1 = chx0[chx0.index(ch.x)]-ufox0[ufox0.index(ufo.x)]
            l1 = ch.x - ufo.x
            le.append(l1)
            if l1 == 0:
                th = 0
            elif l1 > 0:
                th = math.atan((ch.y-ufo.y)/l1)
            else:
                th = math.atan((ch.y-ufo.y)/l1)+math.pi

    for ubul in ubullets:
        k = ubullets.index(ubul)
        reqy = math.isclose(ubul.y, ch.y+ch.h/2, abs_tol=ch.h/2)
        reqx = math.isclose(ubul.x, ch.x+ch.w//2, abs_tol=ch.w/2)
        if reqy and reqx:
            ubullets.clear(); bullets.clear()
#            chx0.clear();chy0.clear()
            print("You've lost")            
            run = False
        if abs(ubul.y - h_s/2) <= h_s//2 and abs(ubul.x-w_s//2) < w_s//2:
            ubul.y += abs(math.sin(th))*ubul.v; ubul.x += math.cos(th)*ubul.v
        else:
            ubullets.pop(k)
#            chx0.pop(k);ufox0.pop(k);le.pop(k)

    redrawscrn()
    
pygame.quit()
