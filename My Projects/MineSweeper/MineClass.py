"""
Created on Sun 20 Mar 19:35 2022
Finished on Wednesday 23 Mar 19:30 2022
@author: Cpt.Ender
                                  """
import pygame
from random import randint


class cell:
    def __init__(self, i, j, w, h):
        """
        Method to initialize the Cell objects
        """
        self.i = i
        self.j = j
        self.size = [w, h]
        self.pos = [self.i * w, self.j * h]
        self.value = 0
        self.neighbors = []
        self.visible = False
        self.flag = False


class Grid:
    def __init__(self, width, height, size, bombs):
        """
        Class to initialize the Grid object with Cell objects
        """
        self.width = width + 1
        self.height = height + 1
        self.gridS = size
        self.cellW = self.width // self.gridS
        self.cellH = self.height // self.gridS
        self.bombsN = bombs
        self.flagN = bombs
        self.grid = []
        self.bombIndexes = []
        self.populate()

    def populate(self):
        # Populate with default cell objects
        self.grid = [[cell(i, j, self.cellW, self.cellH) for j in range(self.gridS)] for i in range(self.gridS)]

        # Add Bombs
        self.flagN = self.bombsN
        self.bombIndexes = []
        while len(self.bombIndexes) < self.bombsN:
            index = randint(0, self.gridS ** 2 - 1)
            index = [index // self.gridS, index - index // self.gridS * self.gridS]
            if index not in self.bombIndexes:
                self.bombIndexes.append(index)
                self.grid[index[0]][index[1]].value = -1
        # print(bombIndexes)

    def findNeighbors(self, cel: cell):
        # Find all the available neighbors of the cell
        for i in range(cel.i - 1, cel.i + 2):
            for j in range(cel.j - 1, cel.j + 2):
                if (-1 < i < self.gridS and -1 < j < self.gridS) and not (i == cel.i and j == cel.j):
                    cel.neighbors.append([i, j])

        # Calculate the value of the cell based on how many bomb neighbors it has
        for neigh in cel.neighbors:
            if self.grid[neigh[0]][neigh[1]].value == -1:
                cel.value += 1

        # If the cell has 0 bomb neighbors turn its neighbors visible
        if cel.value == 0:
            self.grid[cel.i][cel.j].visible = True
            for neigh in cel.neighbors:
                if not self.grid[neigh[0]][neigh[1]].visible:
                    self.findNeighbors(self.grid[neigh[0]][neigh[1]])
                    self.grid[neigh[0]][neigh[1]].visible = True


class mineSweep(Grid):
    def __init__(self, width, height, size, bombs):
        """
        Method to initialize the game
        :param width: width of the board
        :param height: height of the board
        :param size: size of the grid
        :param bombs: how many bombs will be
        """
        super().__init__(width, height, size, bombs)
        pygame.init()
        self.gameOver = False
        self.window = [self.width, self.height]
        pygame.display.set_caption("MineSweeper.py")
        self.scrn = pygame.display.set_mode(self.window)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.events = []
        self.black = [0] * 3
        self.white = [180] * 3
        self.gray = [80] * 3
        self.red = [150, 0, 0]
        # Fonts
        self.number_font = pygame.font.Font('freesansbold.ttf', self.cellH // 3)

        print("\nHelpful keybindings:")
        print("Lft_mouse_bt : Make the Cell Visible")
        print("Rgt_mouse_bt : Flag the Cell as probable Bomb")
        print("R : reinitializes the board")

    def logig(self):
        # Mouse Position
        mousePos = pygame.mouse.get_pos()
        cellPos = [mousePos[0] * self.gridS // self.height, mousePos[1] * self.gridS // self.width]
        selectedCell = self.grid[cellPos[0]][cellPos[1]]

        if all([p1 < p2 for p1, p2 in zip(mousePos, self.window)]):
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Turn the cell visible
                    selectedCell.visible = True

                    # Find its neighbors and calculate its value
                    if selectedCell.value != -1 and not selectedCell.neighbors:
                        self.findNeighbors(selectedCell)
                        # print(selectedCell.neighbors)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    # If Right Mouse Button is pressed, mark/unmark the cell as potential bomb
                    if selectedCell.flag:
                        self.flagN += 1
                        selectedCell.flag = not selectedCell.flag
                    elif not selectedCell.flag and self.flagN > 0:
                        self.flagN -= 1
                        selectedCell.flag = not selectedCell.flag

    def running(self):
        # Check if the Game has ended
        if not self.gameOver:
            flagged = [False for n in range(self.bombsN)]
            for i, bomb in enumerate(self.bombIndexes):
                if self.grid[bomb[0]][bomb[1]].visible:
                    self.gameOver = True
                    self.draw()
                    print('BOOM')
                    break
                if self.grid[bomb[0]][bomb[1]].flag:
                    flagged[i] = True
            if all(flagged):
                self.gameOver = True
                print("Congratulations")
        # Get events
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.populate()
                    self.gameOver = False
        return True

    @staticmethod
    def quit():
        pygame.quit()

    def draw(self):
        self.scrn.fill(self.white)  # Background Colour
        # Draw cells
        for row in self.grid:
            for c in row:
                if self.gameOver:
                    c.visible = True
                if c.flag:
                    pygame.draw.rect(self.scrn, self.red, [c.pos[0], c.pos[1], c.size[0], c.size[1]])
                if c.visible:
                    pygame.draw.rect(self.scrn, self.gray, [c.pos[0], c.pos[1], c.size[0], c.size[1]])
                    if c.value == -1:
                        # Draw Bombs
                        pygame.draw.ellipse(self.scrn, self.black,
                                            [c.pos[0] + c.size[0] // 10, c.pos[1] + c.size[1] // 10,
                                             c.size[0] - c.size[0] // 5, c.size[1] - c.size[0] // 5])
                    elif c.value > 0:
                        # Draw numbers
                        number = self.number_font.render(str(c.value), True, self.black)
                        n_rect = number.get_rect()
                        n_rect.center = [c.pos[0] + c.size[0] // 2, c.pos[1] + c.size[1] // 2]
                        self.scrn.blit(number, n_rect)
                        pass
                    else:
                        # Don't draw anything for 0
                        pass

        # Draw Grid Lines
        for i in range(0, self.gridS + 2):
            pygame.draw.line(self.scrn, self.black, [i * self.cellW, 0], [i * self.cellW, self.height])
            pygame.draw.line(self.scrn, self.black, [0, i * self.cellH], [self.width, i * self.cellH])

        pygame.display.update()
