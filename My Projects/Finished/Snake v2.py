# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:53:27 2019

@author: plabc
"""
import pygame,random
pygame.init()

w_s = 500;h_s = 500
pygame.display.set_caption("Snake v.2")
win = pygame.display.set_mode((w_s,h_s))
clock = pygame.time.Clock()

class s_part():
    def __init__(self,x,y,vx,vy):
        self.w = w_s//50;self.h = h_s//50
        self.x =[x];self.y = [y]
        self.vx = 0;self.vy= 0
    def draw(self,win,it1):
        pygame.draw.rect(win,(0,0,255),(self.x[it1],self.y[it1],self.w,self.h))

snake = s_part(w_s//2,h_s//2,0,0)

r=5;d=2*r
class apple():
    def __init__(self,x,y):
        self.x = x;self.y = y
        self.r = r
    def draw(self,win):
        pygame.draw.circle(win,(255,0,0),(self.x,self.y),self.r)
apx=random.randint(r,w_s//d-r)*d-r;apy=random.randint(r,h_s//d-r)*d-r
ap = apple(apx,apy)

def redrawscrn(it):
    ap.draw(win)
    k=0
    while k <= len(it):
        if k ==0 :
            snake.draw(win,it[k])
        else:
            snake.draw(win,it[k-1])
        k +=1
    pygame.display.update()
    win.fill((0,0,0))    

run = True
v = snake.w;fps = 15
it = [0];it1 = 0;
while run: 
    clock.tick(fps)   
    apx=random.randint(r,w_s//d-r)*d-r;apy=random.randint(r,h_s//d-r)*d-r
    keys = pygame.key.get_pressed()
    
    # Window-------------------------------------------------------------------
    if keys[pygame.K_ESCAPE]:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # Snake--------------------------------------------------------------------
    if keys[pygame.K_LEFT] and snake.vx != v:
        snake.vx = -v;snake.vy=0;
        ix = 1;iy = 0
    elif keys[pygame.K_RIGHT] and snake.vx != -v:
        snake.vx = v;snake.vy=0;
        ix = -1;iy = 0
    elif keys[pygame.K_UP] and snake.vy != v:
        snake.vx = 0;snake.vy= -v;
        ix = 0;iy = 1 
    elif keys[pygame.K_DOWN] and snake.vy != -v:
        snake.vx = 0;snake.vy = v
        ix = 0;iy = -1
        
    snake.x.append(snake.x[it[0]]+snake.vx)
    snake.y.append(snake.y[it[0]]+snake.vy)
            
    # Collision with apple-----------------------------------------------------
    reqy1 = ap.y-snake.y[it[0]];reqy2 = snake.y[it[0]]+snake.h-ap.y
    reqx1 = ap.x-snake.x[it[0]];reqx2 = snake.x[it[0]]+snake.w-ap.x
    if reqy1 <= r and reqy2 <= r:
        if reqx1 <= r and reqx2 <= r:
            ap = apple(apx,apy)
            for i in it :
                reqy1 = ap.y-snake.y[i];reqy2 = snake.y[i]+snake.h-ap.y
                reqx1 = ap.x-snake.x[i];reqx2 = snake.x[i]+snake.w-ap.x
                while reqy1 <= r and reqy2 <= r and reqx1 <=r and reqx2<=r:
                        apx=random.randint(r,w_s//d-r)*d-r
                        apy=random.randint(r,h_s//d-r)*d-r
                        ap = apple(apx,apy)
                        reqy1 = ap.y-snake.y[i];reqy2 = snake.y[i]+snake.h-ap.y
                        reqx1 = ap.x-snake.x[i];reqx2 = snake.x[i]+snake.w-ap.x

            it1 +=1
            it.append(it[it1-1]-1)
    if keys[pygame.K_x]:
#        ap = apple(apx,apy)
#        print(ap.x,ap.y)
        it1 +=1
        it.append(it[it1-1]-1)

    # Collision with wall------------------------------------------------------ 
    if snake.x[it[0]] < v or snake.x[it[0]] + 3*v//2 > w_s:
        run = False
    elif snake.y[it[0]] < v or snake.y[it[0]] + 3*v//2 > h_s:
        run = False
        
    # Collision with it self---------------------------------------------------
    if it1>3:
        k = 7
        while k < len(it)+3:
            xa = snake.x[it[0]]<snake.x[it[k-3]];xb = snake.x[it[0]]+snake.w>snake.x[it[k-3]]
            ya = snake.y[it[0]]<snake.y[it[k-3]];yb = snake.y[it[0]]+snake.h>snake.y[it[k-3]]
            xa1 = snake.x[it[0]]-snake.x[it[k-3]];ya1 = snake.y[it[0]]-snake.y[it[k-3]];
            if [xa,xb,ya,yb] == [True,True,True,True] :
                run = False
            elif [xa,xb,ya,yb] == [False,False,True,True]:
                run = False  
            elif [xa,xb,ya,yb] == [True,True,False,False]:
                run = False
            elif [xa,xb,ya,yb] == [False,False,False,False]:
                run = False
            elif [xa1,ya1] == [0,0]:
                run = False
            k+=1
            
    redrawscrn(it)
    it[:]=[i+1 for i in it ]
pygame.quit()    