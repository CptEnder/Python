# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 14:23:14 2019
Updated to version 2 on Wen Apr 03 17:00:00 2019
@author: Cpt.Ender

Tips:
1) Make sure you have positions0.txt in your directory
2) The position file format:(never forget the spaces)
    -Black positions
    -[num, num, 'r'] (the order doesnt matter)
    - ...
    -White positions
    -[num, num, 'r']
    -....
    -z xpos ypos rect (en_passant variables)(example :0 400.0 80 p)
    -1 1 1 1 (castles variables)(determening if the rooks or the king for each color has been moved)
                                (1 = not moved, 0 = moved)
                                (first argument = left black rook, second = right black rook
                                third = left white rook, forth = right white rook. If the king has moved
                                the two arguments of the same color(as the king) = 0)
"""

import pygame, math
pi = math.pi
pygame.init()

ws = 640; hs = 640
w = ws/8; h = hs/8
pygame.display.set_caption('Chess')
scrn = pygame.display.set_mode((ws, hs))
white = (255, 255, 255); black = (0, 0, 0); bckw = (80, 80, 80); bckb = (40, 40, 40)


class pawn:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)
        pygame.draw.lines(win, self.color1, False, [[self.x+23, self.y+59], [self.x+35, self.y+23],
                                                 [self.x+45, self.y+23], [self.x+57, self.y+59]], 3)
        pygame.draw.arc(win, self.color1, (self.x+32, self.y+8, 16, 16), -pi/3, 4*pi/3, 3)


class rook:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)
        pygame.draw.rect(win, self.color1, (self.x+25, self.y+30, 30, 30), 3)
        pygame.draw.polygon(win, self.color1, ([self.x+15, self.y+30], [self.x+15, self.y+8],
                                             [self.x+24, self.y+8], [self.x+25, self.y+16],
                                             [self.x+34, self.y+16], [self.x+35, self.y+8],
                                             [self.x+44, self.y+8], [self.x+45, self.y+16],
                                             [self.x+54, self.y+16], [self.x+55, self.y+8],
                                             [self.x+64, self.y+8], [self.x+64, self.y+30]), 3)


class knight:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)
        pygame.draw.line(win, self.color1, [self.x+24, self.y+59], [self.x+24, self.y+50], 3)
        pygame.draw.arc(win, self.color1, (self.x+13, self.y+34, 24, 16), 1.5*pi, 0, 3)
        pygame.draw.line(win, self.color1, [self.x+36, self.y+42], [self.x+36, self.y+25], 3)
        pygame.draw.arc(win, self.color1, (self.x+29, self.y+25, 14, 18), pi/2, pi, 3)
        pygame.draw.lines(win, self.color1, False, ([self.x+29, self.y+29], [self.x+29, self.y+38],
                                                [self.x+19, self.y+38], [self.x+19, self.y+10],
                                                [self.x+14, self.y+8], [self.x+39, self.y+8]), 3)
        pygame.draw.arc(win, self.color1, (self.x+12, self.y+8, 45, 45), 0, pi/2, 3)
        pygame.draw.line(win, self.color1, [self.x+56, self.y+31], [self.x+56, self.y+59], 3)
        pygame.draw.circle(win, self.color1, [int(self.x+26), int(self.y+20)], 3, 3)


class bishop:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)


class queen:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)


class king:
    def __init__(self, x, y, color1, color2):
        self.x = x; self.y = y
        self.w = 50; self.h = 16
        self.color1 = color1; self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color1, (self.x+15, self.y+59, self.w, self.h), 3)


def pieces():
    global wpieces, bpieces, run, whites, blacks
    wpieces= []; wpcount=wrcount=wkncount=wbcount=wqcount=wkcount=0
    bpieces= []; bpcount=brcount=bkncount=bbcount=bqcount=bkcount=0
    for i in range(len(whpos)):
        if whpos[i][2] == 'p':  # counts white pawns
            wpcount +=1
            wpawn = pawn(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wpawn)
        elif whpos[i][2] == 'r':  # counts white rooks
            wrcount +=1
            wrook = rook(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wrook)
        elif whpos[i][2] == 'kn':  # counts white knights
            wkncount +=1
            wknight = knight(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wknight)
        elif whpos[i][2] == 'b':  # counts white bishops
            wbcount +=1
            wbishop = bishop(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wbishop)
        elif whpos[i][2] == 'q':  # counts white queens
            wqcount +=1
            wqueen = queen(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wqueen)
        elif whpos[i][2] == 'k':  # counts white kings
            wkcount +=1
            wking = king(whpos[i][0], whpos[i][1], white, bckw)
            wpieces.append(wking)
    for i in range(len(blpos)):
        if blpos[i][2] == 'p':  # counts white pawns
            bpcount +=1
            bpawn = pawn(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(bpawn)
        elif blpos[i][2] == 'r':  # counts black rooks
            brcount +=1
            brook = rook(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(brook)
        elif blpos[i][2] == 'kn':  # counts black knights
            bkncount +=1
            bknight = knight(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(bknight)
        elif blpos[i][2] == 'b':  # counts black bishops
            bbcount +=1
            bbishop = bishop(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(bbishop)
        elif blpos[i][2] == 'q':  # counts black queens
            bqcount +=1
            bqueen = queen(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(bqueen)
        elif blpos[i][2] == 'k':  # counts black kings
            bkcount +=1
            bking = king(blpos[i][0], blpos[i][1], black, bckb)
            bpieces.append(bking)
    whites = [wpcount, wrcount, wkncount, wbcount, wqcount, wkcount]
    blacks = [bpcount, brcount, bkncount, bbcount, bqcount, bkcount]
    if wkcount == 0 or bkcount == 0:
        print ('The End')
        run = False


def choices(rectx, recty, k):
    global undo, whpos, blpos, x, z, epx, epy, ep, en_passant, bcastle1, bcastle2, wcastle1, wcastle2
    loop = True; castles_a = True; castles_b = True
    if k%2 == 0:  # whites
        i = 1; a = blpos; b = whpos; line = 6*w
        castles1 = wcastle1; castles2 = wcastle2
    else:  # blacks
        i = -1; a = whpos; b = blpos; line = w
        castles1 = bcastle1; castles2 = bcastle2
# Choices for Pawns ------------------------------------------------------
    if rect == 'p':
        f = ff = True
        for xx in a:
            for xxx in b:
                # Checks if there is something infront of the pawn
                if xxx[0]-rectx[0] == 0 and xxx[1]-recty[0] == -i*w \
                    or xx[0]-rectx[0] == 0 and xx[1]-recty[0] == -i*w:
                        f = ff = False
                # Checks if the pawn is on the starting line and nothing infront of
                #  it for 2 squares
                if (xxx[0]-rectx[0] == 0 and xxx[1]-recty[0] == -i*2*w
                    or xx[0]-rectx[0] == 0 and xx[1]-recty[0] == -i*2*w) \
                        or recty[0] != line:
                            ff = False
            # Checks diagonally(right) for enemy
            if xx[0]+w == rectx[0] and xx[1]+i*w == recty[0]:
                rectx.append(xx[0]);recty.append(xx[1])
            # Checks diagonally(left) for enemy
            if xx[0]-w == rectx[0] and xx[1]+i*w == recty[0]:
                rectx.append(xx[0]); recty.append(xx[1])
        # En passant
        if k > 2 and k - z == 1 and abs(epy - recty[0]) == 0 \
            and abs(epx - rectx[0]) == w and ep == 'p':
                rectx.append(epx); recty.append(epy-i*w)
                en_passant = True
        else:
            en_passant = False; z = 0
        if f:
            rectx.append(rectx[0]); recty.append(recty[0]-i*w)
        if ff:
            rectx.append(rectx[0]); recty.append(recty[0]-i*2*w)
# Choices for Rooks ----------------------------------------------------------
    if rect == 'r':
        rpos = [[], [], [], []]
        f = [True, True, True, True]
        for j in range(8):  # adding all the possible positions to a list
            rpos[0].append([rectx[0] - (j+1) * w, recty[0]])
            rpos[1].append([rectx[0] + (j+1) * w, recty[0]])
            rpos[2].append([rectx[0], recty[0] + (j+1) * w])
            rpos[3].append([rectx[0], recty[0] - (j+1) * w])
            for jj in range(4):
                for xx in b:
                    # checking for collisions with the same color/position outside of the screen
                    if xx[0] == rpos[jj][j][0] and xx[1] == rpos[jj][j][1]\
                        or rpos[jj][j][0] < 0 or rpos[jj][j][0] >= ws \
                            or rpos[jj][j][1] < 0 or rpos[jj][j][1] >= hs:
                                f[jj] = False
                                break
                for xx in a:  # not allowing you to capture a piece that's behind something else
                    if j >= 1 and xx[0] == rpos[jj][j-1][0] and xx[1] == rpos[jj][j-1][1]:
                        f[jj] = False
                if f[jj]:
                    rectx.append(rpos[jj][j][0]); recty.append(rpos[jj][j][1])
# Choices for Knights
    if rect == 'kn':
        knpos = [[rectx[0] - w, recty[0] - 2 * w], [rectx[0] - 2 * w, recty[0] - w],
                 [rectx[0] - w, recty[0] + 2 * w], [rectx[0] - 2 * w, recty[0] + w],
                 [rectx[0] + w, recty[0] - 2 * w], [rectx[0] + 2 * w, recty[0] - w],
                 [rectx[0] + w, recty[0] + 2 * w], [rectx[0] + 2 * w, recty[0] + w]]
        for xxx in knpos:
            f = True
            for xx in b:  # checking for collisions with the same color
                if xx[0] - xxx[0] == 0 and xx[1] - xxx[1] == 0\
                    or xxx[0] < 0 or xxx[0] >= ws or xxx[1] < 0 or xxx[1] >= hs:
                        f = False
                        break
            if f:
                rectx.append(xxx[0]); recty.append(xxx[1])
# Choices for Bishops
    if rect == 'b':
        bpos = [[], [], [], []]
        f = [True, True, True, True]
        for j in range(8):  # adding all the possible positions to a list
            bpos[0].append([rectx[0] - (j+1) * w, recty[0] - (j+1) * w])
            bpos[1].append([rectx[0] + (j+1) * w, recty[0] + (j+1) * w])
            bpos[2].append([rectx[0] - (j+1) * w, recty[0] + (j+1) * w])
            bpos[3].append([rectx[0] + (j+1) * w, recty[0] - (j+1) * w])
            for jj in range(4):
                for xx in b:
                    # checking for collisions with the same color/position outside of the screen
                    if xx[0] == bpos[jj][j][0] and xx[1] == bpos[jj][j][1]\
                        or bpos[jj][j][0] < 0 or bpos[jj][j][0] >= ws \
                            or bpos[jj][j][1] < 0 or bpos[jj][j][1] >= hs:
                                f[jj] = False
                                break
                for xx in a:  # not allowing you to capture a piece that's behind something else
                    if j >= 1 and xx[0] == bpos[jj][j-1][0] and xx[1] == bpos[jj][j-1][1]:
                        f[jj] = False
                if f[jj]:
                    rectx.append(bpos[jj][j][0]); recty.append(bpos[jj][j][1])
# Choices for Queens
    if rect == 'q':
        qpos = [[], [], [], [], [], [], [], []]
        f = [True, True, True, True, True, True, True, True]
        for j in range(8):  # adding all the possible positions to a list
            qpos[0].append([rectx[0] - (j + 1) * w, recty[0]])
            qpos[1].append([rectx[0] + (j + 1) * w, recty[0]])
            qpos[2].append([rectx[0], recty[0] + (j + 1) * w])
            qpos[3].append([rectx[0], recty[0] - (j + 1) * w])
            qpos[4].append([rectx[0] - (j+1) * w, recty[0] - (j+1) * w])
            qpos[5].append([rectx[0] + (j+1) * w, recty[0] + (j+1) * w])
            qpos[6].append([rectx[0] - (j+1) * w, recty[0] + (j+1) * w])
            qpos[7].append([rectx[0] + (j+1) * w, recty[0] - (j+1) * w])
            for jj in range(8):
                for xx in b:
                    # checking for collisions with the same color/position outside of the screen
                    if xx[0] == qpos[jj][j][0] and xx[1] == qpos[jj][j][1]\
                        or qpos[jj][j][0] < 0 or qpos[jj][j][0] >= ws \
                            or qpos[jj][j][1] < 0 or qpos[jj][j][1] >= hs:
                                f[jj] = False
                                break
                for xx in a:  # not allowing you to capture a piece that's behind something else
                    if j >= 1 and xx[0] == qpos[jj][j-1][0] and xx[1] == qpos[jj][j-1][1]:
                        f[jj] = False
                if f[jj]:
                    rectx.append(qpos[jj][j][0]); recty.append(qpos[jj][j][1])
# Choices for Kings
    if rect == 'k':
        kpos = [[rectx[0], recty[0]-w], [rectx[0], recty[0]+w],
                [rectx[0]-w, recty[0]-w], [rectx[0]-w, recty[0]+w],
                [rectx[0]+w, recty[0]-w], [rectx[0]+w, recty[0]+w],
                [rectx[0]-w, recty[0]], [rectx[0]+w, recty[0]]]
        for xxx in kpos:
            f = True
            for xx in b:
                for j in a:
                    if j[2] == 'k':
                        if abs(j[0] - xxx[0]) == w and abs(j[1] - xxx[1]) == w \
                            or abs(j[0] - xxx[0]) == w and abs(j[1] - xxx[1]) == 0 \
                                or abs(j[0] - xxx[0]) == 0 and abs(j[1] - xxx[1]) == w:
                                    f = False
                                    break
                    if xx[0] == xxx[0] and xx[1] == xxx[1] \
                        or xxx[0] < 0 or xxx[0] >= ws or xxx[1] < 0 or xxx[1] >= hs:
                            f = False
                            break
                    if castles1 == 1 :
                        for cc in b:
                            if cc[0:2] == [rectx[0] + 2*w, recty[0]] \
                                or cc[0:2] == [rectx[0] + w, recty[0]]:
                                    castles_a = False
                        for vv in a:
                            if vv[0:2] == [rectx[0] + 2*w, recty[0]] \
                                or vv[0:2] == [rectx[0] + w, recty[0]]:
                                    castles_a = False
                    if castles2 == 1 :
                        for cc in b:
                            if cc[0:2] == [rectx[0] - 3*w, recty[0]] \
                                or cc[0:2] == [rectx[0] - 2*w, recty[0]] \
                                    or cc[0:2] == [rectx[0] - w, recty[0]]:
                                        castles_b = False
                        for vv in a:
                            if vv[0:2] == [rectx[0] - 3 * w, recty[0]] \
                                or vv[0:2] == [rectx[0] - 2 * w, recty[0]] \
                                    or vv[0:2] == [rectx[0] - w, recty[0]]:
                                        castles_b = False
            if f:
                rectx.append(xxx[0]); recty.append(xxx[1])
        if castles_a and castles1 == 1:
            rectx.append(rectx[0]+2*w); recty.append(recty[0])
        if castles_b and castles2 == 1:
            rectx.append(rectx[0]-2*w); recty.append(recty[0])
# Choice between moving your selected piece or undoing your 1st selection------
    while loop:
        pygame.event.clear()
        redrawscrn(rectx, recty)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1, len(rectx)):
                    # Checks if you left click on a available tile
                    if e.button == 1 and e.pos[1] < recty[i]+w and e.pos[0]<rectx[i]+w \
                        and e.pos[0]>rectx[i] and e.pos[1]>recty[i]:
                            z = k  # en passant checking variable
                            epx = rectx[i]; epy= recty[i]; ep = rect
                            if k%2 == 0:
                                if rect == 'k':
                                    wcastle2 = wcastle1 = 0
                                elif whpos[x] == [0.0, 560.0, 'r']:
                                    wcastle1 = 0
                                elif whpos[x] == [560.0, 560.0, 'r']:
                                    wcastle2 = 0
                                if rectx[i] == 480.0 and rect == 'k' and castles_a:
                                    for ii in range(1, 4):
                                        if whpos[x+ii][2] == 'r':
                                            whpos[x+ii][0] = 400.0
                                if rectx[i] == 160.0 and rect == 'k' and castles_b:
                                    whpos[0][0] = 240.0
                                whpos[x][0]=rectx[i]; whpos[x][1]=recty[i]
                            else:
                                if rect == 'k':
                                    bcastle2 = bcastle1 = 0
                                elif blpos[x] == [0.0, 0.0, 'r']:
                                    bcastle1 = 0
                                elif blpos[x] == [560.0, 0.0, 'r']:
                                    bcastle2 = 0
                                if rectx[i] == 480.0 and rect == 'k' and castles_a:
                                    for ii in range(1, 4):
                                        if blpos[x+ii][2] == 'r':
                                            blpos[x+ii][0] = 400.0
                                if rectx[i] == 160.0 and rect == 'k' and castles_b:
                                    blpos[0][0] = 240.0
                                blpos[x][0] = rectx[i]; blpos[x][1] = recty[i]
                            rectx.clear(); recty.clear()
                            undo = loop = False
                            break
                if e.button == 3:
                    rectx.clear(); recty.clear()
                    undo = True; loop = False
                    redrawscrn(rectx, recty)
    # Promotion of a pawn to a Queen
    if rect == 'p' and b[x][1] == 0 and k%2 == 0:
        whpos[x][2] = 'q'
    elif rect == 'p' and b[x][1] == hs-w and k%2 != 0:
        blpos[x][2] = 'q'
# Capturing -------------------------------------------------------------------
    for x1 in range(len(a)):
        if k%2 == 0:
            if whpos[x][0:2] == blpos[x1][0:2]:
                print('white captures')
                blpos.pop(x1)
                break
            elif whpos[x][2] == 'p' and en_passant \
                and whpos[x][1] - blpos[x1][1] == -w and whpos[x][0] - blpos[x1][0] == 0:
                    print('white captures')
                    blpos.pop(x1)
                    break
        elif k%2 != 0:
            if blpos[x][0:2] == whpos[x1][0:2]:
                print('black captures')
                whpos.pop(x1)
                break
            elif blpos[x][2] == 'p' and en_passant \
                and blpos[x][1] - whpos[x1][1] == w and whpos[x1][0] - blpos[x][0] == 0:
                    print('black captures')
                    whpos.pop(x1)
                    break


def redrawscrn(rectx, recty):
    # Chessboard --------------------------------------------------------------
    scrn.fill(bckb)
    for i in range(8):
        for ii in range(8):
            if (i%2 == 0 and ii%2 == 0) or (i%2 != 0 and ii%2 != 0):
                pygame.draw.rect(scrn, bckw, (i*w, ii*w, w, h))
    # Available moving positions ----------------------------------------------
    for i in range(len(rectx)):  # Choices
        pygame.draw.rect(scrn, [120, 120, 120], [rectx[i], recty[i], w, w], 0)
        pygame.draw.rect(scrn, [30, 0, 255], [rectx[i], recty[i], w, w], 2)
    # Chess pieces -------------------------------------------------------------
    for x in range(len(wpieces)):  # White pieces
        wpieces[x].draw(scrn)
    for x in range(len(bpieces)):  # Black pieces
        bpieces[x].draw(scrn)
    pygame.display.update()


'''
|----------------------------------------------------------------------------|
|                     ~  The Game Loop  ~                                    |
|----------------------------------------------------------------------------|
                                                                            '''
run = True; k = 0; opening = True
while opening:
    try :
        try:
            filename = 'positions'
            file = open(filename + str(k) + ".txt", 'r')
        except IOError:
            filename = "Chess\positions"
            file = open(filename + str(k) + '.txt', 'r')
        k += 1
    except IOError:
        print('Loading file : '+file.name)
        opening = False
        k -= 1

while run:
    blpos = []; whpos = []
    rectx = []; recty = []
    file = open(filename + str(k) + '.txt', 'r')
    lines = file.readlines()
    # Reading from a file and assining those values to the positions of blacks and whites
    for l in range(len(lines)):
        split = lines[l].split() # because it's a string i have to split it in order to get the 3 parts
        if lines[l] == 'Black positions\n':
            bl = True
        elif lines[l] == 'White positions\n':
            bl = False; index = l
        if bl and l > 0:  # appends the positions of blacks to a list
            corx = split[0]; cory = split[1]; corid = split[2]
            blpos.append([float(corx[1:len(corx)-1]), float(cory[0:len(cory)-1]), corid[1:len(corid)-2]])
        elif not bl and index < l < len(lines) - 2:  # appends the positions of whites to a list
            corx = split[0]; cory = split[1]; corid = split[2]
            whpos.append([float(corx[1:len(corx)-1]), float(cory[0:len(cory)-1]), corid[1:len(corid)-2]])
        elif l == len(lines)-2:  # appends all the variables needed for 'en passant'
            z = int(split[0]); epx = float(split[1]); epy = float(split[2]); ep = split[3]
        elif l == len(lines)-1:  # appends all the variables needed for 'castles'
            bcastle1 = int(split[0]); bcastle2 = int(split[1])
            wcastle1 = int(split[2]); wcastle2 = int(split[3])
            print(bcastle1, bcastle2, wcastle1, wcastle2)
    pieces()
    print('whites : ', whites)
    print('blacks : ', blacks)
    redrawscrn(rectx, recty)
    wait = True; filewrite = True
    while wait:
        undo = False
# Window-----------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                wait = False
# 1st Selection ---------------------------------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if you clicked inside the hitbox of a chesspiece (of the correct color of course)
                for x in range(len(whpos)):
                    if k%2 == 0 and event.pos[0]-whpos[x][0] < w and event.pos[1]-whpos[x][1] < w \
                        and event.pos[0]-whpos[x][0] > 0 and event.pos[1]-whpos[x][1] > 0:
                            rectx.append(whpos[x][0]); recty.append(whpos[x][1]); rect = whpos[x][2]
                            choices(rectx, recty, k)
                            if not undo:
                                wait = False
                            break
                for x in range(len(blpos)):
                    if k%2 != 0 and event.pos[0]-blpos[x][0] < w and event.pos[1]-blpos[x][1] < w \
                        and event.pos[0]-blpos[x][0] > 0 and event.pos[1]-blpos[x][1] > 0:
                            rectx.append(blpos[x][0]); recty.append(blpos[x][1]); rect = blpos[x][2]
                            choices(rectx, recty, k)
                            if not undo:
                                wait = False
                            break
            if event.type == pygame.KEYDOWN:
                print(event)
                # if you press Esc the program ends
                if event.key == 27 and event.unicode == '\x1b' :
                    wait = False
                    run = False
                # if you press the Spacebar you essentially waste a turn
                if event.key == 32:
                    wait = False
                # if you press LCtrl you move to a previous position (like Ctrl + Z)
                if k >= 1 and event.key == 306:
                    wait = False
                    filewrite = False
                    k -= 2
    pieces()
    k += 1
    if filewrite and run:  # writing to a file the current positions
        file = open(filename+str(k)+".txt", "w+")
        print('Saving to file : '+file.name)
        file.write('Black positions\n')
        for j in range(len(blpos)):
            file.write(str(blpos[j])+'\n')
        file.write('White positions\n')
        for j in range(len(whpos)):
            file.write(str(whpos[j])+'\n')
        file.write(str(z)+' '+str(epx)+' '+str(epy)+' '+ep+'\n')
        file.write(str(bcastle1)+' '+str(bcastle2)+' '+str(wcastle1)+' '+str(wcastle2))

pygame.quit()
