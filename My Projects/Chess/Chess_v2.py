"""
v1 : Created on Sun 10 Mar 14:23:14 2019
v2 : Updated from v1 on Wen 03 Apr 17:00:00 2019
Finished(?) on Tue 09 Apr  21:12:00 2019
@author: Cpt.Ender

Chess rules that have been implemented :
    -Castles
    -En passant
    -Check
    -Checkmate
    -Stalemate
    -Impossibility of a checkmate due to insufficient pieces
Other implementations:
    -Saving to a file
    -Loading from a file
    -Undo ('press LCtrl')

Tips:
1) Make sure you have positions0.txt in your directory
2) The position file format:(never forget the spaces)
    -Black positions
    -[x, y, 'r'] (the order doesnt matter)
    - ...
    -White positions
    -[x, y, 'r']
    -....
    -z xpos ypos rect (en_passant variables)(example :0 400.0 80 p)
    -1 1 1 1 (castles variables)(determining if the rooks or the king for each color has been moved)
                                (1 = not moved, 0 = moved)
                                (first argument = left black rook, second = right black rook
                                third = left white rook, forth = right white rook. If the king has moved
                                the two arguments of the same color(as the king) = 0)
"""

import pygame, math

pi = math.pi
pygame.init()

ws = 640
hs = 640
w = ws // 8
h = hs // 8
pygame.display.set_caption('Chess')
scrn = pygame.display.set_mode((ws, hs))
white = (230, 230, 230)
black = (0, 0, 0)
bckw = (80, 80, 80)
bckb = (40, 40, 40)


class pawn:
    def __init__(self, x_, y_, color):
        self.x = int(x_)
        self.y = int(y_)
        self.w = 40
        self.h = 10
        self.color = color
        # self.image = image

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y])
        pygame.draw.rect(win, self.color, (self.x + 20, self.y + 65, self.w, self.h), 3)
        pygame.draw.lines(win, self.color, False, [[self.x + 25, self.y + 65], [self.x + 35, self.y + 30],
                                                   [self.x + 45, self.y + 30], [self.x + 55, self.y + 65]], 3)
        pygame.draw.arc(win, self.color, (self.x + 32, self.y + 15, 16, 16), -pi / 3, 4 * pi / 3, 3)


class rook:
    def __init__(self, x_, y_, color):
        self.x = int(x_)
        self.y = int(y_)
        self.w = 50
        self.h = 16
        self.color = color
        # self.image = image

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y])
        pygame.draw.rect(win, self.color, (self.x + 15, self.y + 59, self.w, self.h), 3)
        pygame.draw.rect(win, self.color, (self.x + 25, self.y + 30, 30, 30), 3)
        pygame.draw.polygon(win, self.color, ([self.x + 15, self.y + 30], [self.x + 15, self.y + 8],
                                              [self.x + 24, self.y + 8], [self.x + 25, self.y + 16],
                                              [self.x + 34, self.y + 16], [self.x + 35, self.y + 8],
                                              [self.x + 44, self.y + 8], [self.x + 45, self.y + 16],
                                              [self.x + 54, self.y + 16], [self.x + 55, self.y + 8],
                                              [self.x + 65, self.y + 8], [self.x + 65, self.y + 30]), 3)


class knight:
    def __init__(self, x_, y_, color):
        self.x = int(x_)
        self.y = int(y_)
        self.w = 50
        self.h = 10
        self.color = color
        # self.image = image

    def draw(self, win):
        # win.blit(self.image,[self.x,self.y])
        pygame.draw.rect(win, self.color, (self.x + 15, self.y + 65, self.w, self.h), 3)
        pygame.draw.line(win, self.color, [self.x + 24, self.y + 65], [self.x + 24, self.y + 50], 3)
        pygame.draw.arc(win, self.color, (self.x + 13, self.y + 34, 24, 16), 1.5 * pi, 0, 3)
        pygame.draw.line(win, self.color, [self.x + 36, self.y + 42], [self.x + 36, self.y + 25], 3)
        pygame.draw.arc(win, self.color, (self.x + 29, self.y + 25, 14, 18), pi / 2, pi, 3)
        pygame.draw.lines(win, self.color, False, ([self.x + 29, self.y + 29], [self.x + 29, self.y + 38],
                                                   [self.x + 19, self.y + 38], [self.x + 19, self.y + 10],
                                                   [self.x + 14, self.y + 8], [self.x + 39, self.y + 8]), 3)
        pygame.draw.arc(win, self.color, (self.x + 12, self.y + 8, 45, 45), 0, pi / 2, 3)
        pygame.draw.line(win, self.color, [self.x + 56, self.y + 31], [self.x + 56, self.y + 65], 3)
        pygame.draw.circle(win, self.color, [int(self.x + 26), int(self.y + 20)], 3, 3)


class bishop:
    def __init__(self, x_, y_, color):
        self.x = int(x_)
        self.y = int(y_)
        self.w = 40
        self.h = 10
        self.color = color
        # self.image = image

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y])
        pygame.draw.rect(win, self.color, (self.x + 20, self.y + 65, self.w, self.h), 3)
        pygame.draw.polygon(win, self.color, [[self.x + 28, self.y + 65], [self.x + 32, self.y + 35],
                                              [self.x + 47, self.y + 35], [self.x + 51, self.y + 65]], 3)
        pygame.draw.polygon(win, self.color, [[self.x + 32, self.y + 35], [self.x + 28, self.y + 25],
                                              [self.x + 39, self.y + 14], [self.x + 51, self.y + 25],
                                              [self.x + 47, self.y + 35]], 3)
        pygame.draw.line(win, self.color, [self.x + 42, self.y + 29], [self.x + 47, self.y + 22], 2)
        pygame.draw.arc(win, self.color, (self.x + 36, self.y + 8, 8, 8), -pi / 3, 4 * pi / 3, 2)


class queen:
    def __init__(self, x_, y_, color, color2):
        self.x = int(x_)
        self.y = int(y_)
        self.w = 50
        self.h = 16
        self.color = color
        self.color2 = color2
        # self.image = image

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y])
        pygame.draw.rect(win, self.color, (self.x + 15, self.y + 59, self.w, self.h), 3)
        pygame.draw.lines(win, self.color, False, ([self.x + 15, self.y + 59], [self.x + 10, self.y + 25],
                                                   [self.x + 25, self.y + 44], [self.x + 40, self.y + 25],
                                                   [self.x + 54, self.y + 44], [self.x + 68, self.y + 25],
                                                   [self.x + 65, self.y + 59]), 3)
        pygame.draw.circle(win, self.color2, [int(self.x + 25), int(self.y + 67)], 3, 3)
        pygame.draw.circle(win, self.color2, [int(self.x + 40), int(self.y + 67)], 3, 3)
        pygame.draw.circle(win, self.color2, [int(self.x + 55), int(self.y + 67)], 3, 3)
        pygame.draw.circle(win, self.color, [int(self.x + 9), int(self.y + 23)], 5, 0)
        pygame.draw.circle(win, self.color, [int(self.x + 40), int(self.y + 23)], 5, 0)
        pygame.draw.circle(win, self.color, [int(self.x + 70), int(self.y + 23)], 5, 0)


class king:
    def __init__(self, x_, y_, color):
        self.x = int(x_)
        self.y = int(y_)
        self.color = color
        # self.image = image

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y])
        pygame.draw.polygon(win, self.color, ([self.x + 35, self.y + 55], [self.x + 37, self.y + 42],
                                              [self.x + 25, self.y + 45], [self.x + 25, self.y + 35],
                                              [self.x + 37, self.y + 37], [self.x + 35, self.y + 25],
                                              [self.x + 45, self.y + 25], [self.x + 42, self.y + 37],
                                              [self.x + 55, self.y + 35], [self.x + 55, self.y + 45],
                                              [self.x + 42, self.y + 42], [self.x + 45, self.y + 55]), 0)
        pygame.draw.arc(win, self.color, (self.x + 8, self.y - 40, 60, 116), pi + 0.01, 8 * pi / 5, 3)
        pygame.draw.arc(win, self.color, (self.x + 13, self.y - 40, 60, 116), -3 * pi / 5, 0, 3)
        pygame.draw.arc(win, self.color, [self.x + 8, self.y + 8, 64, 22], 0, pi + 0.01, 3)


def pieces():
    global wpieces, bpieces, run, whites, blacks
    global wrcastle, wlcastle, brcastle, blcastle
    wpieces = []
    wpcount = wrcount = wkncount = wbcount = wqcount = wkcount = 0
    bpieces = []
    bpcount = brcount = bkncount = bbcount = bqcount = bkcount = 0
    wlbishop = wrbishop = wrrook = wlrook = 0
    blbishop = brbishop = brrook = blrook = 0
    for i in range(len(whpos)):
        if whpos[i][2] == 'p':  # counts white pawns
            wpcount += 1
            wpawn = pawn(whpos[i][0], whpos[i][1], white)
            wpieces.append(wpawn)
        elif whpos[i][2] == 'r':  # counts white rooks
            wrcount += 1
            if wkcount == 0:
                wlrook = 1
            else:
                wrrook = 1
            wrook = rook(whpos[i][0], whpos[i][1], white)
            wpieces.append(wrook)
        elif whpos[i][2] == 'kn':  # counts white knights
            wkncount += 1
            wknight = knight(whpos[i][0], whpos[i][1], white)
            wpieces.append(wknight)
        elif whpos[i][2] == 'b':  # counts white bishops
            wbcount += 1
            if wkcount == 0:
                wlbishop = 1
            else:
                wrbishop = 1
            wbishop = bishop(whpos[i][0], whpos[i][1], white)
            wpieces.append(wbishop)
        elif whpos[i][2] == 'q':  # counts white queens
            wqcount += 1
            wqueen = queen(whpos[i][0], whpos[i][1], white, (0, 255, 0))
            wpieces.append(wqueen)
        elif whpos[i][2] == 'k':  # counts white kings
            wkcount += 1
            wking = king(whpos[i][0], whpos[i][1], white)
            wpieces.append(wking)
    for i in range(len(blpos)):
        if blpos[i][2] == 'p':  # counts white pawns
            bpcount += 1
            bpawn = pawn(blpos[i][0], blpos[i][1], black)
            # bpawn = pawn(blpos[i][0], blpos[i][1], goblin)
            bpieces.append(bpawn)
        elif blpos[i][2] == 'r':  # counts black rooks
            brcount += 1
            if bkcount == 0:
                blrook = 1
            else:
                brrook = 1
            # brook = rook(blpos[i][0], blpos[i][1], pylon)
            brook = rook(blpos[i][0], blpos[i][1], black)
            bpieces.append(brook)
        elif blpos[i][2] == 'kn':  # counts black knights
            bkncount += 1
            bknight = knight(blpos[i][0], blpos[i][1], black)
            # bknight = knight(blpos[i][0], blpos[i][1],dragon)
            bpieces.append(bknight)
        elif blpos[i][2] == 'b':  # counts black bishops
            bbcount += 1
            if bkcount == 0:
                blbishop = 1
            else:
                brbishop = 1
            # bbishop = bishop(blpos[i][0], blpos[i][1], skeleton)
            bbishop = bishop(blpos[i][0], blpos[i][1], black)
            bpieces.append(bbishop)
        elif blpos[i][2] == 'q':  # counts black queens
            bqcount += 1
            # bqueen = queen(blpos[i][0], blpos[i][1], medusa)
            bqueen = queen(blpos[i][0], blpos[i][1], black, (255, 0, 0))
            bpieces.append(bqueen)
        elif blpos[i][2] == 'k':  # counts black kings
            bkcount += 1
            # bking = king(blpos[i][0], blpos[i][1], beholder)
            bking = king(blpos[i][0], blpos[i][1], black)
            bpieces.append(bking)
    if brrook == 0:
        brcastle = 0
    elif blrook == 0:
        blcastle = 0
    elif wrrook == 0:
        wrcastle = 0
    elif wlrook == 0:
        wlcastle = 0
    whites = [wpcount, wrcount, wkncount, wbcount, wqcount, wkcount]
    blacks = [bpcount, brcount, bkncount, bbcount, bqcount, bkcount]
    if blacks == whites == [0, 0, 0, 0, 0, 1] \
            or (blacks == [0, 0, 0, 1, 0, 1] and whites == [0, 0, 0, 0, 0, 1]) \
            or (blacks == [0, 0, 0, 0, 0, 1] and whites == [0, 0, 0, 1, 0, 1]) \
            or (blacks == [0, 0, 1, 0, 0, 1] and whites == [0, 0, 0, 0, 0, 1]) \
            or (blacks == [0, 0, 0, 0, 0, 1] and whites == [0, 0, 1, 0, 0, 1]) \
            or (blacks == whites == [0, 0, 0, 1, 0, 1] and blbishop == wlbishop == 1
                and brbishop == wrbishop == 0) \
            or (blacks == whites == [0, 0, 0, 1, 0, 1] and blbishop == wlbishop == 0
                and brbishop == wrbishop == 1):
        print("Impossibility of a checkmate. It's a draw")
        run = False


def choices(posx, posy, obj, k, loop, checks):
    global undo, whpos, blpos, x, z, epx, epy, ep, en_passant
    global blcastle, brcastle, wlcastle, wrcastle
    castles_L = True
    castles_R = True
    Checks = checks
    if k % 2 == 0:  # whites
        i = 1
        a = blpos
        b = whpos
        line = 6 * w
        Lcastles = wlcastle
        Rcastles = wrcastle
    else:  # blacks
        i = -1
        a = whpos
        b = blpos
        line = w
        Lcastles = blcastle
        Rcastles = brcastle
    if obj == 'p':
        choice_a, cover = p(posx, posy, i, a, b, line, z, epx, epy, ep, Checks)
    elif obj == 'r':
        choice_a, cover = r(posx, posy, a, b, Checks)
    elif obj == 'kn':
        choice_a, cover = kn(posx, posy, b, Checks)
    elif obj == 'b':
        choice_a, cover = bi(posx, posy, a, b, Checks)
    elif obj == 'q':
        choice_a, cover = q(posx, posy, a, b, Checks)
    elif obj == 'k':
        cover = []
        choice_a, Checks = ki(posx, posy, a, b, k, castles_L, castles_R, Lcastles, Rcastles, Checks)
    # Choice between moving your selected piece or undoing your 1st selection------
    while loop:
        pygame.event.clear()
        redrawscrn(posx, posy)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                for j in range(1, len(posx)):
                    # Checks if you left click on a available tile
                    if e.button == 1 and e.pos[1] < posy[j] + w and e.pos[0] < posx[j] + w \
                            and e.pos[0] > posx[j] and e.pos[1] > posy[j]:
                        z = k  # en passant checking variable
                        epx = posx[j]
                        epy = posy[j]
                        ep = obj
                        if k % 2 == 0:
                            if posx[j] == 480.0 and obj == 'k' and castles_R and wrcastle == 1:
                                for ii in range(1, 4):
                                    if whpos[x + ii][2] == 'r':
                                        whpos[x + ii][0] = 400.0
                            if posx[j] == 160.0 and obj == 'k' and castles_L and wlcastle == 1:
                                whpos[0][0] = 240.0
                            if obj == 'k':
                                wrcastle = wlcastle = 0
                            elif whpos[x] == [0.0, 560.0, 'r']:
                                wlcastle = 0
                            elif whpos[x] == [560.0, 560.0, 'r']:
                                wrcastle = 0
                            whpos[x][0] = rectx[j]
                            whpos[x][1] = recty[j]
                        else:
                            if posx[j] == 480.0 and obj == 'k' and castles_R and brcastle == 1:
                                for ii in range(1, 4):
                                    if blpos[x + ii][2] == 'r':
                                        blpos[x + ii][0] = 400.0
                            if posx[j] == 160.0 and obj == 'k' and castles_L and blcastle == 1:
                                blpos[0][0] = 240.0
                            if obj == 'k':
                                brcastle = blcastle = 0
                            elif blpos[x] == [0.0, 0.0, 'r']:
                                blcastle = 0
                            elif blpos[x] == [560.0, 0.0, 'r']:
                                brcastle = 0
                            blpos[x][0] = rectx[j]
                            blpos[x][1] = recty[j]
                        posx.clear()
                        posy.clear()
                        undo = loop = False
                        break
                if e.button == 3:
                    posx.clear()
                    posy.clear()
                    undo = True
                    loop = False
                    redrawscrn(posx, posy)
        # Promotion of a pawn to a Queen
        if obj == 'p' and b[x][1] == 0 and k % 2 == 0:
            whpos[x][2] = 'q'
        elif obj == 'p' and b[x][1] == hs - w and k % 2 != 0:
            blpos[x][2] = 'q'
        # Capturing
        for x1 in range(len(a)):
            if k % 2 == 0:
                if whpos[x][0:2] == blpos[x1][0:2]:
                    print('white captures')
                    blpos.pop(x1)
                    break
                elif whpos[x][2] == 'p' and en_passant \
                        and whpos[x][1] - blpos[x1][1] == -w and whpos[x][0] - blpos[x1][0] == 0:
                    print('white captures')
                    blpos.pop(x1)
                    break
            elif k % 2 != 0:
                if blpos[x][0:2] == whpos[x1][0:2]:
                    print('black captures')
                    whpos.pop(x1)
                    break
                elif blpos[x][2] == 'p' and en_passant \
                        and blpos[x][1] - whpos[x1][1] == w and whpos[x1][0] - blpos[x][0] == 0:
                    print('black captures')
                    whpos.pop(x1)
                    break
    return choice_a, cover, Checks


# Choices for Pawns
def p(rectx_, recty_, i, enemy, me, line, z, epx, epy, ep, checks):
    global en_passant
    pawn_choices = []
    pawn_covers = []
    f = ff = True
    for xx in enemy:
        for xxx in me:
            # Checks if there is something infront of the pawn
            if xxx[0] - rectx_[0] == 0 and xxx[1] - recty_[0] == -i * w \
                    or xx[0] - rectx_[0] == 0 and xx[1] - recty_[0] == -i * w:
                f = ff = False
            # Checks if the pawn is on the starting line and nothing infront of
            #  it for 2 squares
            if (xxx[0] - rectx_[0] == 0 and xxx[1] - recty_[0] == -i * 2 * w
                or xx[0] - rectx_[0] == 0 and xx[1] - recty_[0] == -i * 2 * w) \
                    or recty_[0] != line:
                ff = False
        # Checks diagonally(right) for enemy
        if xx[0] + w == rectx_[0] and xx[1] + i * w == recty_[0]:
            rectx_.append(xx[0])
            recty_.append(xx[1])
        # Checks diagonally(left) for enemy
        if xx[0] - w == rectx_[0] and xx[1] + i * w == recty_[0]:
            rectx_.append(xx[0])
            recty_.append(xx[1])
    for xxx in me:
        # Checks diagonally(right) for same color piece
        if xxx[0] + w == rectx_[0] and xxx[1] + i * w == recty_[0]:
            pawn_covers.append(xxx[0])
            pawn_covers.append(xxx[1])
            break
        # Checks diagonally(left) for same color piece
        if xxx[0] - w == rectx_[0] and xxx[1] + i * w == recty_[0]:
            pawn_covers.append(xxx[0])
            pawn_covers.append(xxx[1])
            break
    # En passant
    if k > 2 and k - z == 1 and epy == recty_[0] == line - i * 3 * w \
            and abs(epx - rectx_[0]) == w and ep == 'p':
        rectx_.append(epx)
        recty_.append(epy - i * w)
        en_passant = True
    else:
        en_passant = False
        z = 0
    if f:
        rectx_.append(rectx_[0])
        recty_.append(recty_[0] - i * w)
    if ff:
        rectx_.append(rectx_[0])
        recty_.append(recty_[0] - i * 2 * w)
    if checks == 1:
        j = 1
        while j < len(recty_):
            c = []
            for i in range(0, len(checkline), 2):
                c.append(True)
                if checkline[i] != rectx_[j] or checkline[i + 1] != recty_[j]:
                    c[i // 2] = False
            if all(ci == False for ci in c):
                rectx_.pop(j)
                recty_.pop(j)
            else:
                j += 1
    # How many available moving positions are there
    if len(rectx_) >= 1:
        for i in range(len(recty_)):
            pawn_choices.append(rectx_[i])
            pawn_choices.append(recty_[i])
        pawn_choices.append('p')
    pawn_covers.append('p')
    return pawn_choices, pawn_covers


# Choices for Rooks
def r(rectx_, recty_, enemy, me, checks):
    rook_choices = []
    rook_covers = []
    rpos = [[], [], [], []]
    f = [True, True, True, True]
    ff = [0, 0, 0, 0]
    for j in range(8):  # adding all the possible positions to a list
        rpos[0].append([rectx_[0] - (j + 1) * w, recty_[0]])
        rpos[1].append([rectx_[0] + (j + 1) * w, recty_[0]])
        rpos[2].append([rectx_[0], recty_[0] + (j + 1) * w])
        rpos[3].append([rectx_[0], recty_[0] - (j + 1) * w])
        for jj in range(4):
            for xxx in me:
                # checking for collisions with the same color/position outside of the screen
                if xxx[0] == rpos[jj][j][0] and xxx[1] == rpos[jj][j][1] \
                        or rpos[jj][j][0] < 0 or rpos[jj][j][0] >= ws \
                        or rpos[jj][j][1] < 0 or rpos[jj][j][1] >= hs:
                    f[jj] = False
                    break
            for xx in enemy:  # not allowing you to capture a piece that's behind something else
                if j >= 1 and xx[0] == rpos[jj][j - 1][0] and xx[1] == rpos[jj][j - 1][1]:
                    f[jj] = False
            if f[jj]:
                rectx_.append(rpos[jj][j][0])
                recty_.append(rpos[jj][j][1])
    # Checks what same color pieces the rook protects
    for i in range(len(recty_)):
        cover = True
        for j in enemy:
            if rectx_[i] - j[0] == 0 and recty_[i] - j[1] == 0:
                cover = False
        for ii in me:
            if ii[0:2] != [rectx_[0], recty_[0]] and cover:
                if ii[0] - w == rectx_[i] and ii[1] == recty_[0] \
                        or ii[0] + w == rectx_[i] and ii[1] == recty_[0] \
                        or ii[0] == rectx_[0] and ii[1] + w == recty_[i] \
                        or ii[0] == rectx_[0] and ii[1] - w == recty_[i]:
                    rook_covers.append(ii[0])
                    rook_covers.append(ii[1])
    if checks == 1:
        j = 1
        while j < len(recty_):
            c = []
            for i in range(0, len(checkline), 2):
                c.append(True)
                if checkline[i] != rectx_[j] or checkline[i + 1] != recty_[j]:
                    c[i // 2] = False
            if all(ci == False for ci in c):
                rectx_.pop(j)
                recty_.pop(j)
            else:
                j += 1
    # How many avalaible moving positions are there
    if len(rectx_) >= 1:
        for i in range(len(recty_)):
            rook_choices.append(rectx_[i])
            rook_choices.append(recty_[i])
        rook_choices.append('r')
    rook_covers.append('r')
    return rook_choices, rook_covers


# Choices for Knights
def kn(rectx_, recty_, me, checks):
    knight_choices = []
    knight_covers = []
    knpos = [[rectx_[0] - w, recty_[0] - 2 * w], [rectx_[0] - 2 * w, recty_[0] - w],
             [rectx_[0] - w, recty_[0] + 2 * w], [rectx_[0] - 2 * w, recty_[0] + w],
             [rectx_[0] + w, recty_[0] - 2 * w], [rectx_[0] + 2 * w, recty_[0] - w],
             [rectx_[0] + w, recty_[0] + 2 * w], [rectx_[0] + 2 * w, recty_[0] + w]]
    for xxx in knpos:
        f = True
        for xx in me:  # checking for collisions with the same color
            if xx[0] - xxx[0] == 0 and xx[1] - xxx[1] == 0:
                knight_covers.append(xx[0])
                knight_covers.append(xx[1])
                f = False
                break
            if xxx[0] < 0 or xxx[0] >= ws or xxx[1] < 0 or xxx[1] >= hs:
                f = False
                break
        if f:
            rectx_.append(xxx[0])
            recty_.append(xxx[1])
    if checks == 1:
        j = 1
        while j < len(recty_):
            c = []
            for i in range(0, len(checkline), 2):
                c.append(True)
                if checkline[i] != rectx_[j] or checkline[i + 1] != recty_[j]:
                    c[i // 2] = False
            if all(ci == False for ci in c):
                rectx_.pop(j)
                recty_.pop(j)
            else:
                j += 1
    # How many available moving positions are there
    if len(rectx_) >= 1:
        for i in range(len(recty_)):
            knight_choices.append(rectx_[i])
            knight_choices.append(recty_[i])
        knight_choices.append('kn')
    knight_covers.append('kn')
    return knight_choices, knight_covers


# Choices for Bishops
def bi(rectx_, recty_, enemy, me, checks):
    bishop_choices = []
    bishop_covers = []
    bpos = [[], [], [], []]
    f = [True, True, True, True]
    for j in range(8):  # adding all the possible positions to a list
        bpos[0].append([rectx_[0] - (j + 1) * w, recty_[0] - (j + 1) * w])
        bpos[1].append([rectx_[0] + (j + 1) * w, recty_[0] + (j + 1) * w])
        bpos[2].append([rectx_[0] - (j + 1) * w, recty_[0] + (j + 1) * w])
        bpos[3].append([rectx_[0] + (j + 1) * w, recty_[0] - (j + 1) * w])
        for jj in range(4):
            for xx in me:
                # checking for collisions with the same color/position outside of the screen
                if xx[0] == bpos[jj][j][0] and xx[1] == bpos[jj][j][1] \
                        or bpos[jj][j][0] < 0 or bpos[jj][j][0] >= ws \
                        or bpos[jj][j][1] < 0 or bpos[jj][j][1] >= hs:
                    f[jj] = False
                    break
            for xx in enemy:  # not allowing you to capture a piece that's behind something else
                if j >= 1 and xx[0] == bpos[jj][j - 1][0] and xx[1] == bpos[jj][j - 1][1]:
                    f[jj] = False
            if f[jj]:
                rectx_.append(bpos[jj][j][0])
                recty_.append(bpos[jj][j][1])
    # Checks what same color pieces the bishop protects
    for i in range(len(recty_)):
        cover = True
        for j in enemy:
            if rectx_[i] - j[0] == 0 and recty_[i] - j[1] == 0:
                cover = False
        for ii in me:
            dx = ii[0] - rectx_[0]
            dy = ii[1] - recty_[0]
            if ii[0:2] != [rectx_[0], recty_[0]] and cover:
                if abs(dx) == abs(dy):
                    if ii[1] - recty_[i] == w and ii[0] - rectx_[i] == w \
                            or recty_[i] - ii[1] == w and rectx_[i] - ii[0] == w \
                            or ii[1] - recty_[i] == w and rectx_[i] - ii[0] == w \
                            or recty_[i] - ii[1] == w and ii[0] - rectx_[i] == w:
                        bishop_covers.append(ii[0])
                        bishop_covers.append(ii[1])
    if checks == 1:
        j = 1
        while j < len(recty_):
            c = []
            for i in range(0, len(checkline), 2):
                c.append(True)
                if checkline[i] != rectx_[j] or checkline[i + 1] != recty_[j]:
                    c[i // 2] = False
            if all(ci == False for ci in c):
                rectx_.pop(j)
                recty_.pop(j)
            else:
                j += 1
    # How many avalaible moving positions are there
    if len(rectx_) >= 1:
        for i in range(len(recty_)):
            bishop_choices.append(rectx_[i])
            bishop_choices.append(recty_[i])
        bishop_choices.append('b')
    bishop_covers.append('b')
    return bishop_choices, bishop_covers


# Choices for Queens
def q(rectx_, recty_, enemy, me, checks):
    queen_choices = []
    queen_covers = []
    qpos = [[], [], [], [], [], [], [], []]
    f = [True, True, True, True, True, True, True, True]
    c = [True, True, True, True, True, True, True, True]
    for j in range(8):  # adding all the possible positions to a list
        qpos[0].append([rectx_[0] - (j + 1) * w, recty_[0]])
        qpos[1].append([rectx_[0] + (j + 1) * w, recty_[0]])
        qpos[2].append([rectx_[0], recty_[0] + (j + 1) * w])
        qpos[3].append([rectx_[0], recty_[0] - (j + 1) * w])
        qpos[4].append([rectx_[0] - (j + 1) * w, recty_[0] - (j + 1) * w])
        qpos[5].append([rectx_[0] + (j + 1) * w, recty_[0] + (j + 1) * w])
        qpos[6].append([rectx_[0] - (j + 1) * w, recty_[0] + (j + 1) * w])
        qpos[7].append([rectx_[0] + (j + 1) * w, recty_[0] - (j + 1) * w])
        for jj in range(8):
            for xx in me:
                # checking for collisions with the same color/position outside of the screen
                if xx[0] == qpos[jj][j][0] and xx[1] == qpos[jj][j][1] \
                        or qpos[jj][j][0] < 0 or qpos[jj][j][0] >= ws \
                        or qpos[jj][j][1] < 0 or qpos[jj][j][1] >= hs:
                    f[jj] = False
                    break
            for xx in enemy:  # not allowing you to capture a piece that's behind something else
                if j >= 1 and xx[0] == qpos[jj][j - 1][0] and xx[1] == qpos[jj][j - 1][1]:
                    f[jj] = False
            if f[jj]:
                rectx_.append(qpos[jj][j][0])
                recty_.append(qpos[jj][j][1])
    # Checks what same color pieces the queen protects
    for i in range(len(recty_)):
        cover = True
        for j in enemy:
            if rectx_[i] - j[0] == 0 and recty_[i] - j[1] == 0:
                cover = False
                break
        for ii in me:
            dx = ii[0] - rectx_[0]
            dy = ii[1] - recty_[0]
            if ii[0:2] != [rectx_[0], recty_[0]] and cover:
                if rectx_[i] == rectx_[0]:
                    if ii[1] - recty_[i] == w and dx == 0 \
                            or recty_[i] - ii[1] == w and dx == 0:
                        queen_covers.append(ii[0])
                        queen_covers.append(ii[1])
                if recty_[i] == recty_[0]:
                    if ii[0] - rectx_[i] == w and dy == 0 \
                            or rectx_[i] - ii[0] == w and dy == 0:
                        queen_covers.append(ii[0])
                        queen_covers.append(ii[1])
                if abs(dx) == abs(dy):
                    if ii[1] - recty_[i] == w and ii[0] - rectx_[i] == w \
                            or recty_[i] - ii[1] == w and rectx_[i] - ii[0] == w \
                            or ii[1] - recty_[i] == w and rectx_[i] - ii[0] == w \
                            or recty_[i] - ii[1] == w and ii[0] - rectx_[i] == w:
                        queen_covers.append(ii[0])
                        queen_covers.append(ii[1])
    if checks == 1:
        j = 1
        while j < len(recty_):
            c = []
            for i in range(0, len(checkline), 2):
                c.append(True)
                if checkline[i] != rectx_[j] or checkline[i + 1] != recty_[j]:
                    c[i // 2] = False
            if all(ci == False for ci in c):
                rectx_.pop(j)
                recty_.pop(j)
            else:
                j += 1
    # How many avalaible moving positions are there
    if len(rectx_) >= 1:
        for i in range(len(recty_)):
            queen_choices.append(rectx_[i])
            queen_choices.append(recty_[i])
        queen_choices.append('q')
    queen_covers.append('q')
    return queen_choices, queen_covers


# Choices for Kings
def ki(rectx_, recty_, a, b, k, castles_L, castles_R, Lcastles, Rcastles, Checka):
    global enemy_choices, checkline, enemy_covers
    if k % 2 == 0:
        l = -1
    else:
        l = 1
    enemy_choices = []
    enemy_covers = []
    Checks = Checka
    kpos = [[rectx_[0], recty_[0] - w], [rectx_[0], recty_[0] + w],
            [rectx_[0] - w, recty_[0] - w], [rectx_[0] - w, recty_[0] + w],
            [rectx_[0] + w, recty_[0] - w], [rectx_[0] + w, recty_[0] + w],
            [rectx_[0] - w, recty_[0]], [rectx_[0] + w, recty_[0]]]
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
        if f:
            rectx_.append(xxx[0])
            recty_.append(xxx[1])

    # checks if there is anything between the king and the right rook
    # if the king and the rook havenot been moved yet
    if Rcastles == 1:
        for cc in b:
            if cc[0:2] == [rectx_[0] + 2 * w, recty_[0]] \
                    or cc[0:2] == [rectx_[0] + w, recty_[0]]:
                castles_R = False
        for vv in a:
            if vv[0:2] == [rectx_[0] + 2 * w, recty_[0]] \
                    or vv[0:2] == [rectx_[0] + w, recty_[0]]:
                castles_R = False
    # checks if there is anything between the king and the left rook
    # if the king and the rook havenot been moved yet
    if Lcastles == 1:
        for cc in b:
            if cc[0:2] == [rectx_[0] - 3 * w, recty_[0]] \
                    or cc[0:2] == [rectx_[0] - 2 * w, recty_[0]] \
                    or cc[0:2] == [rectx_[0] - w, recty_[0]]:
                castles_L = False
        for vv in a:
            if vv[0:2] == [rectx_[0] - 3 * w, recty_[0]] \
                    or vv[0:2] == [rectx_[0] - 2 * w, recty_[0]] \
                    or vv[0:2] == [rectx_[0] - w, recty_[0]]:
                castles_L = False
    # If the king and the left rook havenot been moved yet and there is nothing between them
    # then the king can castle with the left rook
    if castles_L and Lcastles == 1:
        rectx_.append(rectx_[0] - 2 * w)
        recty_.append(recty_[0])
    # If the king and the right rook have not been moved yet and there is nothing between them
    # then the king can castle with the right rook
    if castles_R and Rcastles == 1:
        rectx_.append(rectx_[0] + 2 * w)
        recty_.append(recty_[0])
    # Finds all the available positions of the enemy
    for i in a:
        if i[2] != 'k':
            if len(choices([i[0]], [i[1]], i[2], k + 1, False, 0)[0]) != 0:
                enemy_choices.append(choices([i[0]], [i[1]], i[2], k + 1, False, 0)[0])
                enemy_covers.append(choices([i[0]], [i[1]], i[2], k + 1, False, 0)[1])
    # Checks if any of the enemy's available choices coincide with the king's available choices
    for i in enemy_choices:
        for ii in range(2, len(i) - 2):
            if ii % 2 == 0 and i[len(i) - 1] != 'p':
                j = 1
                while j < len(recty_):
                    # print(i,i[ii],i[ii+1],rectx_[j],recty_[j])
                    if rectx_[j] == i[ii] and recty_[j] == i[ii + 1]:
                        rectx_.pop(j)
                        recty_.pop(j)
                    else:
                        j += 1
                if rectx_[0] == i[ii] and recty_[0] == i[ii + 1]:
                    Checks = 1
        if i[len(i) - 1] == 'p':
            j = 1
            while j < len(recty_):
                if rectx_[j] == i[0] - w and recty_[j] == i[1] - l * w:
                    rectx_.pop(j)
                    recty_.pop(j)
                elif rectx_[j] == i[0] + w and recty_[j] == i[1] - l * w:
                    rectx_.pop(j)
                    recty_.pop(j)
                j += 1
            if rectx_[0] == i[0] - w and recty_[0] == i[1] - l * w \
                    or rectx_[0] == i[0] + w and recty_[0] == i[1] - l * w:
                Checks = 1
    checkline = []
    # All the tiles that the king cannot move to , because of existing check
    if Checks == 1:
        for i in enemy_choices:
            Check1 = 0
            for ii in range(len(i) - 1):
                if ii % 2 == 0:
                    if rectx_[0] == i[ii] and recty_[0] == i[ii + 1]:
                        Check1 = 1
            if Check1 == 1:
                dx = rectx_[0] - i[0]
                dy = recty_[0] - i[1]
                checkline.append(i[0])
                checkline.append(i[1])
                if dy == 0:
                    for d in range(1, abs(int(dx / 80)) + 1):
                        checkline.append(i[0] + d * dx / abs(dx) * w)
                        checkline.append(i[1])
                elif dx == 0:
                    for d in range(1, abs(int(dy / 80)) + 1):
                        checkline.append(i[0])
                        checkline.append(i[1] + d * dy / abs(dy) * w)
                elif i[len(i) - 1] != 'kn':
                    for d in range(1, abs(int(dy / 80)) + 1):
                        checkline.append(i[0] + d * dx / abs(dx) * w)
                        checkline.append(i[1] + d * dy / abs(dy) * w)

    # Checks if any of the king's available choices coincide with the Check line
    for i in range(0, len(checkline), 2):
        dx = checkline[i] - rectx_[0]
        dy = checkline[i + 1] - recty_[0]
        j = 1
        while j < len(recty_):
            if dx == 0 and dy != 0:
                if rectx_[j] == rectx_[0] and abs(recty_[j] - checkline[i + 1]) == 2 * w:
                    rectx_.pop(j)
                    recty_.pop(j)
            elif dx != 0 and dy == 0:
                if recty_[j] == recty_[0] and abs(rectx_[j] - checkline[i]) == 2 * w:
                    rectx_.pop(j)
                    recty_.pop(j)
            elif abs(dx) == abs(dy):
                if abs(checkline[i] - rectx_[j]) == abs(checkline[i + 1] - recty_[j]) == 2 * w \
                        and (dx == dy > 0 or dx == dy < 0 or dx > 0 > dy or dy > 0 > dx):
                    rectx_.pop(j)
                    recty_.pop(j)
            elif rectx_[j] == checkline[i] and recty_[j] == checkline[i + 1]:
                rectx_.pop(j)
                recty_.pop(j)
            j += 1
    # Checks if any of the king's available choices coincide with the enemy's cover tiles
    for i in enemy_covers:
        if len(i) != 1:
            for ii in range(0, len(i), 2):
                j = 1
                while j < len(recty_):
                    if rectx_[j] == i[ii] and recty_[j] == i[ii + 1]:
                        rectx_.pop(j)
                        recty_.pop(j)
                    j += 1
    # How many avalaible moving positions are there
    king_choices = []
    if len(rectx_) >= 1:
        for i in range(0, len(recty_)):
            king_choices.append(rectx_[i])
            king_choices.append(recty_[i])
        king_choices.append('k')
    return king_choices, Checks


def redrawscrn(rectx_, recty_):
    # Chessboard --------------------------------------------------------------
    scrn.fill(bckb)
    for i in range(8):
        for ii in range(8):
            if (i % 2 == 0 and ii % 2 == 0) or (i % 2 != 0 and ii % 2 != 0):
                pygame.draw.rect(scrn, bckw, (i * w, ii * w, w, h))
    # Available moving positions ----------------------------------------------
    for i in range(len(rectx_)):  # Choices
        pygame.draw.rect(scrn, [120, 120, 120], [int(rectx_[i]), int(recty_[i]), w, w], 0)
        if i == 0:
            pygame.draw.rect(scrn, [255, 255, 0], [int(rectx_[i]) + 1, int(recty_[i]) + 1, w - 2, w - 2], 2)
        else:
            pygame.draw.rect(scrn, [30, 0, 255], [int(rectx_[i]), int(recty_[i]), w, w], 2)
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
run = True
k = 0
opening = True
endgame = False
while opening:
    try:
        filename = 'positions'
        file = open(filename + str(k) + ".txt", 'r')
    except IOError:
        filename = "Chess//positions"
        file = open(filename + str(k) + '.txt', 'r')
    k += 1
    try:
        file = open(filename + str(k) + '.txt', 'r')
    except IOError:
        print('Loading file : ' + file.name)
        opening = False
        k -= 1

while run:
    blpos = []
    whpos = []
    rectx = []
    recty = []
    file = open(filename + str(k) + '.txt', 'r')
    print('Loading file : ' + file.name)
    lines = file.readlines()
    # Reading from a file and assining those values to the positions of blacks and whites
    for l in range(len(lines)):
        split = lines[l].split()  # because it's a string i have to split it in order to get the 3 parts
        if lines[l] == 'Black positions\n':
            bl = True
        elif lines[l] == 'White positions\n':
            bl = False
            index = l
        if bl and l > 0:  # appends the positions of blacks to a list
            corx = split[0]
            cory = split[1]
            corid = split[2]
            blpos.append([float(corx[1:len(corx) - 1]), float(cory[0:len(cory) - 1]), corid[1:len(corid) - 2]])
        elif not bl and index < l < len(lines) - 2:  # appends the positions of whites to a list
            corx = split[0]
            cory = split[1]
            corid = split[2]
            whpos.append([float(corx[1:len(corx) - 1]), float(cory[0:len(cory) - 1]), corid[1:len(corid) - 2]])
        elif l == len(lines) - 2:  # appends all the variables needed for 'en passant'
            z = int(split[0])
            epx = float(split[1])
            epy = float(split[2])
            ep = split[3]
        elif l == len(lines) - 1:  # appends all the variables needed for 'castles'
            blcastle = int(split[0])
            brcastle = int(split[1])
            wlcastle = int(split[2])
            wrcastle = int(split[3])
    pieces()
    print('whites : ', whites)
    print('blacks : ', blacks)
    redrawscrn(rectx, recty)
    wait = True
    filewrite = True
    my_choices = []
    Check = 0
    if k % 2 == 0:
        thepositions = whpos
        winner = 'Blacks have won'
    else:
        thepositions = blpos
        winner = 'White have won'
    for i in thepositions:
        my_choices.append(choices([i[0]], [i[1]], i[2], k, False, Check)[0])
        Check = choices([i[0]], [i[1]], i[2], k, False, Check)[2]
    if Check == 1:
        print('Check. Your King is under attack')
        my_choices = []
        for i in thepositions:
            my_choices.append(choices([i[0]], [i[1]], i[2], k, False, Check)[0])
    if all(len(m) == 3 for m in my_choices) and Check == 0:
        print("No available moving positions. It's a Stalemate Draw")
        run = wait = False
    elif all(len(m) == 3 for m in my_choices) and Check == 1:
        print("Checkmate 'mate'. " + winner)
        run = wait = False
    while wait:
        undo = False
        # Window-----------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = wait = False
                endgame = True
            # 1st Selection ---------------------------------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if you clicked inside the hitbox of a chesspiece (of the correct color of course)
                for x in range(len(whpos)):
                    if k % 2 == 0 and event.pos[0] - whpos[x][0] < w and event.pos[1] - whpos[x][1] < w \
                            and event.pos[0] - whpos[x][0] > 0 and event.pos[1] - whpos[x][1] > 0:
                        rectx.append(whpos[x][0])
                        recty.append(whpos[x][1])
                        rect = whpos[x][2]
                        choices(rectx, recty, rect, k, True, Check)
                        if not undo:
                            wait = False
                        break
                for x in range(len(blpos)):
                    if k % 2 != 0 and event.pos[0] - blpos[x][0] < w and event.pos[1] - blpos[x][1] < w \
                            and event.pos[0] - blpos[x][0] > 0 and event.pos[1] - blpos[x][1] > 0:
                        rectx.append(blpos[x][0])
                        recty.append(blpos[x][1])
                        rect = blpos[x][2]
                        choices(rectx, recty, rect, k, True, Check)
                        if not undo:
                            wait = False
                        break
            if event.type == pygame.KEYDOWN:
                # print(event)
                # if you press Esc the program ends
                if event.key == 27 and event.unicode == '\x1b':
                    wait = run = False
                    endgame = True
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
        file = open(filename + str(k) + ".txt", "w+")
        print('Saving to file : ' + file.name)
        file.write('Black positions\n')
        for j in range(len(blpos)):
            file.write(str(blpos[j]) + '\n')
        file.write('White positions\n')
        for j in range(len(whpos)):
            file.write(str(whpos[j]) + '\n')
        file.write(str(z) + ' ' + str(epx) + ' ' + str(epy) + ' ' + ep + '\n')
        file.write(str(blcastle) + ' ' + str(brcastle) + ' ' + str(wlcastle) + ' ' + str(wrcastle) + '\n')

while not endgame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True
        if event.type == pygame.KEYDOWN:
            if event.key == 27 and event.unicode == '\x1b':
                endgame = True

pygame.quit()
