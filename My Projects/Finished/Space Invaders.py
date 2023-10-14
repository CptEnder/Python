import pygame
import math
import random
pygame.init()

w = 1000;h = 500
pygame.display.set_caption("Space Invaders.py")
scrn = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

ufo_w = 30;ufo_h = 20
ufo_x = random.randint(0+2,w-ufo_w-2);ufo_y = 50
ufo_v = ufo_w//6

ch_h = 15;ch_w = 15
ch_x = w/2 - ch_w ;ch_y = 400
ch_v = ufo_w//4

bul_r = 4;bul_v = 30

iii = [1,-1]
ii = iii[random.randint(0,1)]
run = True
while run:
    count = False
    clock.tick(70)
    ch = pygame.draw.rect(scrn,(0,255,0),(ch_x,ch_y,ch_w,ch_h))
    keys = pygame.key.get_pressed()
    # Window-----------------------------------------
    if keys[pygame.K_ESCAPE]:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Ufo -------------------------------------------
    pygame.draw.ellipse(scrn,(255,255,255),[ufo_x,ufo_y,ufo_w,ufo_h],0)
    if math.isclose(ufo_x,0,abs_tol=ufo_v):
        ii = iii[0]
    elif math.isclose(ufo_x+ufo_w,w,abs_tol=ufo_v):
        ii = iii[1]
    ufo_x = ufo_x + ii*ufo_v    
    # Player-----------------------------------------
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if math.isclose(ch_x,0,abs_tol=2):
            ch_x = ch_x
        else:
            ch_x = ch_x - ch_v
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if math.isclose(ch_x+ch_w,w,abs_tol=3):
            ch_x = ch_x
        else:
            ch_x = ch_x + ch_v
    # Bullet------------------------------------------
    if keys[pygame.K_SPACE]:
        bul_x = math.floor(ch_x + ch_w / 2)
        bul_y = ch_y - 2*bul_r
        pygame.draw.circle(scrn,(255,0,0),(bul_x,bul_y),bul_r)
        count = True
    if count == True:
        while bul_y >=0:
            bul_y = bul_y - bul_v
            pygame.draw.circle(scrn,(255,0,0),(bul_x,bul_y),bul_r)
            pygame.display.update()
            pygame.draw.circle(scrn,(0,0,0),(bul_x,bul_y),bul_r)
            if math.isclose(bul_y,ufo_y+ufo_h/2,abs_tol=ufo_h/2): 
                if math.isclose(bul_x,ufo_x + ufo_w//2,abs_tol=ufo_w/2):
                    ufo_x = random.randint(0+2,w-ufo_w-2);ufo_y = 50
                    ii = iii[random.randint(0,1)]
    pygame.display.update()
    scrn.fill((0, 0, 0))

pygame.quit()