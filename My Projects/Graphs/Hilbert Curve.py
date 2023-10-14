"""
Created on Wed 10 Mar 22:51 2021
Finished on Thu 11 Mar 18:00 2021
@author: Cpt.Ender

Visualization of the Hilbert space-filling curve
                                                 """
import pygame

pygame.init()
width_s = 750
height_s = 750
pygame.display.set_caption("Hilbert Curve.py")
scrn = pygame.display.set_mode((width_s, height_s))
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
fps = 30
black = [0] * 3
white = [255] * 3
color = white  # Drawing Color
colorMode = True


def setup(order_: int):
    global colorMode
    if order <= 0:
        print("Order must be an integer greater than 0")
        return
    scrn.fill(black)  # Background Colour

    N = 2 ** order_
    total = N ** 2  # Total number of points
    length = width_s / N

    Curve.clear()
    for i in range(total):
        Curve.append(hilbertCurve(i, order_))
        for j in range(len(Curve[i])):
            Curve[i][j] *= length
            Curve[i][j] += length / 2
    colorMode = True
    print(f'Hilbert Curve of order {order_} Completed')


def hilbertCurve(index: int, order_: int):
    # 1st Order Curve - Starting Curve
    points = [[0, 0], [0, 1], [1, 1], [1, 0]]

    i = index & 3  # Bitwise 'AND' so that i loops from 0 to 3
    point = points[i]

    for j in range(1, order_):
        index = index >> 2  # Bitwise shift to the right by 2
        i = index & 3
        len_ = 2 ** j
        if i == 0:
            temp = point[0]
            point[0] = point[1]
            point[1] = temp
        elif i == 1:
            point[1] += len_
        elif i == 2:
            point[0] += len_
            point[1] += len_
        elif i == 3:
            temp = len_ - 1 - point[0]
            point[0] = len_ - 1 - point[1]
            point[1] = temp
            point[0] += len_

    return point


def running():
    global fps, step, order
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_UP:
                fps += 2
            elif event.key == pygame.K_DOWN and fps > 0:
                fps -= 2
            elif event.key == pygame.K_RIGHT:
                order += 1
            elif event.key == pygame.K_LEFT and order > 1:
                order -= 1
            print(fps, clock.get_fps())
            print(order)
    return True


def draw():
    global counter, color, temp_order, colorMode
    for i in range(counter - step, counter):
        if colorMode:
            h = 360 * i / len(Curve)
            color = pygame.Color(2)
            color.hsva = (h, 100, 100, 100)
        else:
            color = black
        pygame.draw.line(scrn, color, Curve[i], Curve[i + 1])
    pygame.display.update()
    counter += step
    if counter >= len(Curve):
        counter = step
        pygame.time.wait(1000)
        colorMode = not colorMode
        if order != temp_order:
            setup(order)
        temp_order = order
        # scrn.fill(black)  # Background Colour


if __name__ == '__main__':
    print("Up and Down arrow keys controls the frame rate")
    print("Left and Right arrow keys controls the Curves order")
    Curve = []
    order = 5
    temp_order = order
    step = 2 ** 2 - 1  # Drawing Step
    counter = step

    setup(order)
    while running():
        clock.tick(fps)
        draw()
    pygame.quit()
