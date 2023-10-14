"""
Created on Wed 23 Sep 10:56 2020
Finished on Sat 26 Sep 22:00 2020
@author: Cpt.Ender
                                  """
import pygame
from nonogramClass import Nonogram


class Board:
    def __init__(self, name, win_size: list, nonogramClues: list):
        """
        A method for the initialization of a Board
        Contains: screen width and height, box width and height
        """

        pygame.init()
        self.win_size = win_size
        self.grid_size = [len(nonogramClues[0]), len(nonogramClues[1])]
        self.name = name
        pygame.display.set_caption(self.name)
        self.scrn = pygame.display.set_mode(self.win_size)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.black = [0] * 3
        self.white = [200] * 3
        self.blue = [0, 0, 200]
        self.red = [150, 0, 0]
        self.green = [0, 200, 0]
        self.yellow = [0, 180, 150]

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.cluesFont = pygame.font.Font('freesansbold.ttf', 20)
        self.start_button = self.font.render('Start', True, (0, 0, 0), (0, 150, 0))
        self.start_rect = self.start_button.get_rect()
        self.start_rect.center = [self.win_size[0] // 2, self.win_size[1] - 75]
        self.start = False
        self.start_time = 0
        self.time = 0

        self.clues = nonogramClues
        self.nonogram = Nonogram(self.clues)
        self.solution = self.nonogram.solve()
        self.grid = [[0 for _ in range(self.grid_size[0])] for __ in range(self.grid_size[1])]

        self.w_ = self.win_size[0] // (self.grid_size[0] + self.nonogram.maxW - 1)
        self.h_ = self.win_size[1] // (self.grid_size[1] + self.nonogram.maxH - 1)
        self.cluesWidth = self.w_
        self.cluesHeight = self.h_
        self.game_size = [self.win_size[0] + 1 - self.cluesWidth,
                          self.win_size[0] + 1 - self.cluesHeight]

    def _mouseEventAndPosition(self, mouse_pos):
        """ Method for converting the mouse position to cell position,
        and returning the mouse button pressed"""
        # If left click is pressed and the mouse is inside the grid
        if pygame.mouse.get_pressed(3) != (0, 0, 0) and max(mouse_pos) < max(self.win_size):
            cell_pos = [(mouse_pos[0] - self.cluesWidth) // self.w_, (mouse_pos[1] - self.cluesHeight) // self.h_]
            mouse_button = None
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                # Convert mouse position to cell position
                mouse_button = 0
            elif pygame.mouse.get_pressed(3) == (0, 1, 0):
                mouse_button = 1
            elif pygame.mouse.get_pressed(3) == (0, 0, 1):
                mouse_button = 2
            return cell_pos, mouse_button
        return [], None  # return a default value

    def logig(self):
        mouse_pos = pygame.mouse.get_pos()
        cellPos, mouseB = self._mouseEventAndPosition(mouse_pos)
        # Check if the Board is filled correctly and the game has finished
        if self.grid == self.nonogram.solution:
            self.start = False
            self.start_button = self.font.render('Congrats', True, [0, 0, 0], [0, 200, 0])
            self.start_rect = self.start_button.get_rect()
            self.start_rect.center = [self.win_size[0] // 2, self.win_size[1] - 75]
        # If LMB is pressed
        if mouseB == 0:
            if -1 < cellPos[1] < self.grid_size[1] and self.start and -1 < cellPos[0] < self.grid_size[1]:
                # Turn the cell On
                self.grid[cellPos[1]][cellPos[0]] = 1
            elif self.start_rect.collidepoint(mouse_pos) and not self.start and not self.start_time:
                # Start the game
                self.start = True
                self.start_button = self.font.render('Start', True, [0, 0, 0], [150, 0, 0])
                self.start_time = pygame.time.get_ticks()
        # If RMB is pressed
        elif mouseB == 2:
            if cellPos[1] < self.grid_size[1] and self.start:
                self.grid[cellPos[1]][cellPos[0]] = 0

    def draw(self):
        """ A method to draw the board """
        self.scrn.fill(self.white)  # Background Colour

        # Draw the Vertical Clues
        for i, clues in enumerate(self.clues[0]):
            for j, clue in enumerate(clues[::-1]):
                clue_surface = self.cluesFont.render(str(clue), True, self.black)
                self.scrn.blit(clue_surface, ((i + 1.5) * self.cluesWidth,
                                              (self.nonogram.maxH - j - 1) * self.cluesHeight / self.nonogram.maxH))

        # Draw the Horizontal Clues
        for i, clues in enumerate(self.clues[1]):
            for j, clue in enumerate(clues[::-1]):
                clue_surface = self.cluesFont.render(str(clue), True, self.black)
                self.scrn.blit(clue_surface, ((self.nonogram.maxW - j - 0.5) * self.cluesWidth / self.nonogram.maxW,
                                              (i + 1.5) * self.cluesHeight))

        # Drawing the filled boxes
        for j, row in enumerate(self.grid):
            for i, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.scrn, self.black,
                                     ((self.cluesWidth + i * self.w_, self.cluesHeight + j * self.h_),
                                      (self.w_, self.h_)))

        # Drawing the Grid Lines
        # Vertical Lines
        for i in range(self.grid_size[0] + 1):
            pygame.draw.line(self.scrn, self.black, [self.cluesWidth + i * self.w_, self.cluesHeight],
                             [self.cluesWidth + i * self.w_, self.cluesHeight + self.game_size[1]])
        # Horizontal Lines
        for j in range(self.grid_size[1] + 1):
            pygame.draw.line(self.scrn, self.black, [self.cluesWidth, self.cluesHeight + j * self.h_],
                             [self.cluesWidth + self.game_size[0], self.cluesHeight + j * self.h_])

        # Drawing buttons, and info
        self.scrn.blit(self.start_button, self.start_rect)

        # Timer button
        if self.start and self.start_time:
            self.time = (pygame.time.get_ticks() - self.start_time) // 1000
        # Divide by 60 to get total minutes
        minutes = self.time // 60
        # Use modulus (remainder) to get seconds
        seconds = self.time % 60
        timer = self.font.render("{0:02}:{1:02}".format(minutes, seconds), True, [50] * 3)
        timer_rect = timer.get_rect()
        timer_rect.center = [self.start_rect.center[0], self.start_rect.center[1] + 50]
        self.scrn.blit(timer, timer_rect)

        pygame.display.update()

    def running(self):
        for event in pygame.event.get():
            evT = event.type
            if evT == pygame.QUIT or (evT == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit()
                return False
            pygame.time.wait(100)
        return True

    def quit(self):
        pygame.quit()

