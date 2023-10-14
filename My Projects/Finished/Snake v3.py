"""
Created on Tue 24 Mar 10:12 2020
Finished on Fri 26 Mar 10:00 2020
@author: Cpt.Ender
                                  """
import pygame, random
pygame.init()

width = 500
height = 600  # size of window


grid_w = grid_h = width  # size of the grid
pygame.display.set_caption("Snake v.3")
win = pygame.display.set_mode((width, height))
pygame.font.init()
font1 = pygame.font.SysFont('Comic Sans Ms', 20)
font2 = pygame.font.Font('freesansbold.ttf', 40)
clock = pygame.time.Clock()
grid_num = 25
grid = [i for i in range(grid_num**2)]
fps = 20
w = grid_w/grid_num
black = [0]*3
green = [0, 255, 0]
red = [255, 0, 0]
gray = [100]*3
white = [255]*3
direction = {"Stop": 0, "Up": 1, "Down": 2, "Left": 3, "Right": 4}
snake_pos: list
fruit_pos: list
drctn: int
score: int
highscore = 0
gameover: bool
end: bool
reset_rect = [width // 2 - 150, grid_h + (height - grid_h) // 2 - 10, 54, 29]


def apple_position():
    sub_grid = grid[:]
    l = len(snake_pos)
    for i in range(l):
        index = int(snake_pos[l-i-1][0]/w + snake_pos[l-i-1][1]/w*grid_num)
        sub_grid.pop(index)
    rand_num = random.randint(0, len(sub_grid)-1)
    f_x = rand_num % grid_num * w
    f_y = rand_num // grid_num * w
    return [f_x, f_y]


def initial():
    global drctn, snake_pos, fruit_pos, score, gameover, end
    x0 = grid_num // 2*w
    y0 = grid_num // 2*w
    snake_pos = [[x0, y0]]
    fruit_pos = apple_position()
    drctn = direction["Stop"]
    score = 0
    gameover = False
    end = False


def inputCom():
    global gameover, drctn, end
    # Window-----------------------------------------------------------------
    mouse_pos = [pygame.mouse.get_pos(), 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = end = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos[1] = 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:  # To exit press 'Esc'
        gameover = end = True
    # Snake--------------------------------------------------------------------
    elif keys[pygame.K_LEFT] and drctn != direction["Right"]:
        drctn = direction["Left"]
    elif keys[pygame.K_RIGHT] and drctn != direction["Left"]:
        drctn = direction["Right"]
    elif keys[pygame.K_UP] and drctn != direction["Down"]:
        drctn = direction["Up"]
    elif keys[pygame.K_DOWN] and drctn != direction["Up"]:
        drctn = direction["Down"]
    return drctn, mouse_pos


def logic(dr: int, m_pos):
    global gameover, fruit_pos, score, highscore
    if reset_rect[0] <= m_pos[0][0] <= reset_rect[0]+reset_rect[2] and \
            reset_rect[1] <= m_pos[0][1] <= reset_rect[1]+reset_rect[3] and \
            m_pos[1] == 1:
        initial()
        return
    # Game Over
    # Collision with walls
    if snake_pos[0][0] == 0 and dr == direction["Left"] or \
            snake_pos[0][0] == grid_w - w and dr == direction["Right"] or \
            snake_pos[0][1] == 0 and dr == direction["Up"] or \
            snake_pos[0][1] == grid_h - w and dr == direction["Down"]:
        gameover = True
    # Collisions with itself
    for i in range(1, len(snake_pos)):
        if snake_pos[0] == snake_pos[i]:
            gameover = True

    if not gameover:
        temp = snake_pos[-1][:]  # temporary store the last part of the snake
        temp_list = []

        # Movement
        for i in range(len(snake_pos) - 1):
            temp_list.append(snake_pos[i][:])
        if dr == 1:
            snake_pos[0][1] -= w
        if dr == 2:
            snake_pos[0][1] += w
        if dr == 3:
            snake_pos[0][0] -= w
        if dr == 4:
            snake_pos[0][0] += w
        for i in range(1, len(snake_pos)):
            snake_pos[i] = temp_list[i-1][:]

        # Eating the apple
        if snake_pos[0] == fruit_pos:
            snake_pos.append(temp)
            fruit_pos = apple_position()
            score += 1
            if score > highscore:
                highscore = score


def draw():
    # Drawing the apple
    pygame.draw.rect(win, red, [fruit_pos[0], fruit_pos[1], w, w])

    # Drawing the snake
    for x, y in snake_pos:
        pygame.draw.rect(win, green, [x, y, w, w])

    # Drawing the grid
    for i in range(grid_num+1):
        pygame.draw.line(win, gray, [0, i*w], [grid_w, i*w])
        pygame.draw.line(win, gray, [i * w, 0], [i * w, grid_h])

    # Display Game Over
    if gameover:
        win.fill(black)
        gameover_text = font2.render("Game Over", True,  white, black)
        win.blit(gameover_text, [width//2-gameover_text.get_size()[0]//2,
                                 width//2-gameover_text.get_size()[0]//2])
    # Display scores
    score_text = font1.render("Score = "+str(score), True, green, gray)
    highscore_text = font1.render("Highscore = "+str(highscore), True, green, gray)
    win.blit(score_text, [width//2 + 50, grid_h+(height-grid_h)//2-30])
    win.blit(highscore_text, [width//2 + 50, grid_h+(height-grid_h)//2+10])

    # Reset button
    reset_text = font1.render("Reset", True, red, gray)
    win.blit(reset_text, [width//2 - 150, grid_h+(height-grid_h)//2-20])

    # Update screen
    pygame.display.update()
    win.fill(black)


def main():
    global drctn
    initial()
    while not end:
        clock.tick(fps)
        draw()
        drctn, mouse_position = inputCom()
        logic(drctn, mouse_position)


if __name__ == "__main__":
    # execute only if run as a script
    main()
    pygame.quit()