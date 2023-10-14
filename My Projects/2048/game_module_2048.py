"""
Created on Wed 14 Oct 22:17 2020
Finished on Wed 28 Oct 21:30 2020
@author: Cpt.Ender

Working but no colours
                                  """
import pygame
from random import choice


class Board:
    def __init__(self, windowSize: list, grid_size: list):
        """
        A method for the initialization of a Board
        :param windowSize: dimensions of the window
        :param grid_size: dimensions of the grid
        """
        pygame.init()
        self.windowSize = windowSize
        self.grid_size = grid_size
        self.w_ = self.windowSize[0] // self.grid_size[0]
        self.h_ = self.windowSize[1] // self.grid_size[1]
        self.window_size = [self.windowSize[0] + 1, self.windowSize[1] + 1 + 60]
        pygame.display.set_caption("2048 Game")
        self.scrn = pygame.display.set_mode(self.window_size)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.running = True

        self.Grid = [[0 for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        self.availableSpots = self._updateAvailableSpots()
        self._placeANum()
        self.score = 0

        # Colors and Fonts
        self.gray = [80] * 3
        self.white = [255] * 3
        self.number_font = pygame.font.Font('freesansbold.ttf', (self.w_ + self.h_) // 4)
        self.score_font = pygame.font.Font('freesansbold.ttf', 30)

    def _placeANum(self):
        """
        Function to place a number (2 or 4) in a random available cell
        """
        num = choice([2] * 9 + [4])  # 90% chance of being a 2 and 10% chance of being a 4
        randomIndex = choice(self.availableSpots)
        self.availableSpots.pop(self.availableSpots.index(randomIndex))
        randomRowIndex = randomIndex // 4
        randomColIndex = randomIndex % 4
        self.Grid[randomRowIndex][randomColIndex] = num

    def _updateAvailableSpots(self):
        """
        Function for finding all available empty spots on the board
        :return: list of indexes of all the empty cells
        """
        emptyList = []
        for i, row in enumerate(self.Grid):
            for j, num in enumerate(row):
                if num == 0:
                    emptyList.append(i * self.grid_size[0] + j)
        return emptyList

    def _getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    return "Up"
                if event.key == pygame.K_DOWN:
                    return "Down"
                if event.key == pygame.K_RIGHT:
                    return "Right"
                if event.key == pygame.K_LEFT:
                    return "Left"
        return ''

    def _connect(self, row):
        """ Check if any number in this row can connect
            with another number in the same row """
        for i in range(len(row) - 2, -1, -1):
            number = row[i]
            if number == 0:
                continue
            if row[i + 1] == row[i]:
                row[i + 1] *= 2
                self.score += row[i + 1]
                row[i] = 0
        self._move(row)
        return row

    @staticmethod
    def _move(row):
        """ Check if any number can move in another position """
        for i in range(len(row) - 1, -1, -1):
            number = row[i]
            if number == 0:
                continue
            j = i
            while j < len(row) - 1:
                if row[j + 1] == 0:
                    row[j] = 0
                    row[j + 1] = number
                j += 1

    def _rotateMatrix(self):
        """ Rotate the Grid Matrix clockwise """
        new_mat = []
        for i in range(len(self.Grid[0])):
            new_mat.append([self.Grid[j][i] for j in range(len(self.Grid) - 1, -1, -1)])
        return new_mat

    def applyMove(self, numberOfRotations: int):
        for i in range(numberOfRotations):
            self.Grid = self._rotateMatrix()

        for i in range(len(self.Grid)):
            self._move(self.Grid[i])
            self.Grid[i] = self._connect(self.Grid[i])

        if numberOfRotations != 0:
            for i in range(4 - numberOfRotations):
                self.Grid = self._rotateMatrix()

    def logig(self):
        """ Method for the logic of the board """
        direction = self._getEvents()
        listOfDirections = ["Right", "Up", "Left", "Down"]
        gridNotChanged = True
        if direction in listOfDirections:
            temp_Grid = [row[:] for row in self.Grid]
            self.applyMove(listOfDirections.index(direction))
            for i, temp_row in enumerate(temp_Grid):
                if temp_row != self.Grid[i]:
                    gridNotChanged = False
            if not gridNotChanged:
                self.availableSpots = self._updateAvailableSpots()
                if self.availableSpots:
                    self._placeANum()

    def draw(self):
        """ A method to draw the board """

        self.scrn.fill(self.gray)  # Background Colour

        # Draw the numbers in the grid
        for i, row in enumerate(self.Grid):
            for j, num in enumerate(row):
                if num != 0:
                    number_text = self.number_font.render(str(num), True, self.white)
                    n_rect = number_text.get_rect()
                    n_rect.center = [j * self.w_ + self.w_ // 2, i * self.h_ + self.h_ // 2]
                    self.scrn.blit(number_text, n_rect)

        # Draw the Grid lines
        for i in range(self.grid_size[0] + 1):
            pygame.draw.line(self.scrn, self.white, [self.w_ * i, 0], [self.w_ * i, self.window_size[0]])
            pygame.draw.line(self.scrn, self.white, [0, self.h_ * i], [self.window_size[1], self.h_ * i])

        # Draw the score and best score counts
        score_text = self.score_font.render("Score: " + str(self.score), True, self.white)
        score_rect = score_text.get_rect()
        score_rect.center = [self.window_size[0] // 4, self.window_size[1] -
                             (self.window_size[1] - self.windowSize[1]) // 2]
        self.scrn.blit(score_text, score_rect)

        pygame.display.update()

    @staticmethod
    def quit():
        pygame.quit()
