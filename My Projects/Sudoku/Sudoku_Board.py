"""
Created on Fri 03 Mar 15:47 2023
Finished on Mon 06 Mar 19:00 2023
@author: Cpt.Ender
                                  """

import pygame
from Sudoku_Generator import create as sg


class Board:
    def __init__(self, name, winS: list):
        """
        A method for the initialization of a Board
        Contains: screen width and height, box width and height
        """
        pygame.init()
        self.windowS = winS
        self.dx = self.windowS[0] // 3
        self.dy = self.windowS[1] // 3
        self.dxx = self.windowS[0] // 9
        self.dyy = self.windowS[1] // 9
        self.dxxx = self.windowS[0] // 27
        self.dyyy = self.windowS[1] // 27
        self.gameS = [self.windowS[0] + 1, self.windowS[1] + 51]
        self.name = name
        pygame.display.set_caption(self.name + ".py")
        self.scrn = pygame.display.set_mode(self.gameS)
        pygame.mouse.set_visible(True)
        self.mouse_pos = pygame.mouse.get_pos()
        self.clock = pygame.time.Clock()
        self.frame_rate = 50
        self.clock.tick(self.frame_rate)
        self.start_time = 0
        self.total_seconds = '00:00'

        self.grid = []
        self.gridStorage = []
        self.filled = []
        self.sudoku = [[1, 2]]
        self.cell_pos = [0, 0]
        self.currentN = [0, False]
        self.numberCounts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.mini_numberFlag = 0  # Mini Number Flag
        self.undoFlag = False  # Undo Flag
        self.completed = False  # Sudoku Completed Flag

        # Colors
        self.gray = [200, 200, 200]
        self.white = [255, 255, 255]
        self.blue = pygame.Color(3, 138, 255, 130)
        self.black = [0, 0, 0]
        self.yellow = pygame.Color(255, 255, 159, 80)  # [255, 255, 159, 0]

        # Fonts
        self.number_font = pygame.font.Font('freesansbold.ttf', 30)
        self.mini_number_font = pygame.font.Font('freesansbold.ttf', 12)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        # Start button
        self.start = self.number_font.render('Start', True, (0, 0, 0), (0, 150, 0))
        self.start_rect = self.start.get_rect()
        self.start_rect.center = [self.windowS[0] // 2, self.windowS[1] + 25]
        self.start_button = False
        # Mini Numbers Flag Indicator
        self.notesN = self.number_font.render('Notes OFF', True, (0, 0, 0), (150, 0, 0))
        self.miniF_rect = self.notesN.get_rect()
        self.miniF_rect.midleft = [3 * self.windowS[0] // 4, self.windowS[1] + 25]

        # Difficulty Options
        self.difficulty = ['easy', 38]
        self.diffRects = []
        easy = self.number_font.render('EASY', True, self.black)
        medium = self.number_font.render('MEDIUM', True, self.black)
        hard = self.number_font.render('HARD', True, self.black)
        for i, option in enumerate([easy, medium, hard]):
            option_rect = option.get_rect()
            rect = pygame.Rect(self.windowS[0] // 2, self.windowS[0] // 2 + i * self.number_font.get_height() * 2,
                               option_rect.width + 10, option_rect.height + 10)
            rect.center = [self.windowS[0] // 2, self.windowS[0] // 2 + i * self.number_font.get_height() * 2]
            option_rect.center = [self.windowS[0] // 2,
                                  self.windowS[0] // 2 + i * self.number_font.get_height() * 2]
            self.diffRects.append([rect, option, option_rect, self.gray])
        self.diffRects[0][3] = self.blue

    def _create(self, diff):
        """ Method for creating a new sudoku """
        self.filled, self.sudoku = sg(diff)
        for col in self.sudoku:
            for n in col:
                self.numberCounts[n] += 1
        print(f"\n{81 - self.numberCounts[0]} Clues")
        # Creating a grid of cells
        for j in range(9):
            self.grid.append([])
            for i, n in enumerate(self.sudoku[j]):
                if n == 0:
                    self.grid[j].append([0, False, [0] * 9])
                else:
                    self.grid[j].append([n, True, [0] * 9])
        return

    def logig(self):
        """ Method for the logic of the board """
        if self.filled != self.sudoku:
            # Set the cell position to the current mouse position if LMB is pressed inside the grid
            self.mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and max(self.mouse_pos) < self.windowS[0]:
                self.cell_pos = [self.mouse_pos[0] * 9 // self.windowS[0], self.mouse_pos[1] * 9 // self.windowS[1]]

            if not self.start_button:
                # Start the Game if the LMB is pressed inside the start_button rectangle
                self.start_time = pygame.time.get_ticks()
                if pygame.mouse.get_pressed(3) == (1, 0, 0):
                    if self.start_rect.collidepoint(self.mouse_pos):
                        # If Start button is pressed
                        self.start_button = True
                        self.start = self.number_font.render('Start', True, [0, 0, 0], [150, 0, 0])
                        self._create(self.difficulty[1])
                    for i, rect in enumerate(self.diffRects):
                        # If a difficulty option button is pressed
                        if rect[0].collidepoint(self.mouse_pos):
                            self.difficulty = [['easy', 38], ['medium', 30], ['hard', 25]][i]
                            rect[3] = self.blue
                            for j in range(len(self.diffRects)):
                                if j != i:
                                    self.diffRects[j][3] = self.gray
            else:
                # If the current cell can be changed and there is a number pressed
                if not self.grid[self.cell_pos[0]][self.cell_pos[1]][1] and self.currentN[1]:
                    # If it's not a note number and the current cell number is not the current number pressed
                    if not self.mini_numberFlag % 2 and \
                            self.grid[self.cell_pos[0]][self.cell_pos[1]][0] != self.currentN[0]:
                        # Adding a copy off the current grind in the grid storage
                        self.gridStorage.append([[[row[0], row[1], row[2].copy()] for row in col] for col in self.grid])

                        # Changing the current number of the cell
                        self.sudoku[self.cell_pos[0]][self.cell_pos[1]] = self.currentN[0]
                        self.numberCounts[self.grid[self.cell_pos[0]][self.cell_pos[1]][0]] -= 1
                        self.numberCounts[self.currentN[0]] += 1
                        self.grid[self.cell_pos[0]][self.cell_pos[1]] = [self.currentN[0], False,
                                                                         [0] * 9]

                        # Remove mini numbers from row,column and box that are the same as current number
                        for i, col in enumerate(self.grid):
                            for j, cell in enumerate(col):
                                if i == self.cell_pos[0] or j == self.cell_pos[1] or \
                                        (i // 3 == self.cell_pos[0] // 3 and j // 3 == self.cell_pos[1] // 3):
                                    cell[2][self.currentN[0] - 1] = 0
                    elif self.mini_numberFlag % 2 and self.currentN[0]:
                        # Adding a copy off the current grind in the grid storage
                        self.gridStorage.append([[[row[0], row[1], row[2].copy()] for row in col] for col in self.grid])

                        self.grid[self.cell_pos[0]][self.cell_pos[1]][2][self.currentN[0] - 1] += 1

        elif self.filled == self.sudoku and not self.completed:
            self.completed = True
            self.save()

    def draw(self):
        """ A method to draw the board on the screen """
        self.scrn.fill(self.white)

        # Drawing the cells
        if self.start_button:
            selectedN = self.grid[self.cell_pos[0]][self.cell_pos[1]][0]
            for i, col in enumerate(self.grid):
                for j, n in enumerate(col):
                    # Draw background for Immutable Cells
                    if n[1]:
                        pygame.draw.rect(self.scrn, self.gray, [i * self.dxx, j * self.dyy, self.dxx, self.dyy])

                    # Draw background for Cells within the same row, column and box of selected cell
                    if i == self.cell_pos[0] or j == self.cell_pos[1] or \
                            (i // 3 == self.cell_pos[0] // 3 and j // 3 == self.cell_pos[1] // 3):
                        rec = pygame.Surface([self.dxx, self.dyy])
                        rec.set_alpha(self.yellow.a)
                        rec.fill(self.yellow)
                        self.scrn.blit(rec, [i * self.dxx, j * self.dyy])

                    # Draw background for Cells with the same Number as the current cell
                    if selectedN and (n[0] == selectedN or n[2][selectedN - 1] % 2):
                        rec = pygame.Surface([self.dxx, self.dyy])
                        rec.set_alpha(self.blue.a)
                        rec.fill(self.blue)
                        self.scrn.blit(rec, [i * self.dxx, j * self.dyy])

                    # Draw the numbers on the screen
                    if n[0]:
                        number = self.number_font.render(str(n[0]), True, self.black)
                        n_rect = number.get_rect()
                        n_rect.center = [int(i * self.dxx + self.dxx / 2), int(j * self.dyy + self.dyy / 2)]
                        self.scrn.blit(number, n_rect)
                    else:
                        for k in range(9):
                            if n[2][k] % 2:
                                mini_number = self.mini_number_font.render(str(k + 1), True, self.black)
                                mini_n_rect = mini_number.get_rect()
                                mini_n_rect.midleft = [int(i * self.dxx + k % 3 * self.dxxx + self.dxxx / 2),
                                                       int(j * self.dyy + k // 3 * self.dyyy + self.dyyy / 2)]
                                self.scrn.blit(mini_number, mini_n_rect)

            # Draw Current Cell perimeter
            pygame.draw.rect(self.scrn, self.black,
                             [self.cell_pos[0] * self.dxx + 1, self.cell_pos[1] * self.dyy + 1,
                              self.dxx - 1, self.dyy - 1], 2)

            # Draw the grid lines
            for i in range(10):
                pygame.draw.line(self.scrn, self.black, [i * self.dxx, 0], [i * self.dxx, self.windowS[0]], 1)
                pygame.draw.line(self.scrn, self.black, [0, i * self.dyy], [self.windowS[1], i * self.dyy], 1)
                if i % 3 == 0:
                    pygame.draw.line(self.scrn, self.black, [i // 3 * self.dx, 0], [i // 3 * self.dx, self.windowS[1]],
                                     3)
                    pygame.draw.line(self.scrn, self.black, [0, i // 3 * self.dy], [self.windowS[0], i // 3 * self.dy],
                                     3)

        else:
            # Draw the Useful Tips and Info
            for i, text in enumerate(["Useful Tips and Keys:",
                                      "You can move around with arrow keys or mouse pressing",
                                      "You can undo a move with LCTRL + Z",
                                      "You can toggle note numbers by pressing SPACE ",
                                      "You can press C to reset the Game with new board",
                                      "You can press BACKSPACE or 0 to delete a number from a cell"]):
                tips = self.font.render(text, True, self.black)
                tips_rect = tips.get_rect()
                tips_rect.topleft = [0, i * self.number_font.get_height() + 50]
                self.scrn.blit(tips, tips_rect)

            # Draw the difficulty options
            for rect, option, option_rect, color in self.diffRects:
                pygame.draw.rect(self.scrn, color, rect)
                pygame.draw.rect(self.scrn, self.black, rect, 1)
                self.scrn.blit(option, option_rect)

        # Draw buttons, and info
        self.scrn.blit(self.start, self.start_rect)
        self.scrn.blit(self.notesN, self.miniF_rect)
        for i in range(1, 10):
            w = 30
            rect = pygame.Rect(w * i, self.windowS[1] + 25, w, w)
            rect.center = [w * (i - 1) + w / 2, self.windowS[1] + 25]
            number = self.number_font.render(str(i), False, self.black)
            noteN = self.mini_number_font.render(str(self.numberCounts[i]), True, [80, 80, 110])
            number_rect = number.get_rect()
            number_rect.midtop = rect.midtop
            noteN_rect = noteN.get_rect()
            noteN_rect.bottomright = rect.bottomright
            pygame.draw.rect(self.scrn, self.gray, rect)
            pygame.draw.rect(self.scrn, self.black, rect, 1)
            self.scrn.blit(number, number_rect)
            self.scrn.blit(noteN, noteN_rect)

        # Timer button
        if not self.completed:
            self.total_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
            # Divide by 60 to get total minutes
            minutes = self.total_seconds // 60
            # Use modulus (remainder) to get seconds
            seconds = self.total_seconds % 60
            self.total_seconds = "{0:02}:{1:02}".format(minutes, seconds)
        timer = self.number_font.render(self.total_seconds, True, (200, 200, 200))
        timer_rect = timer.get_rect()
        timer_rect.center = [self.windowS[0] // 3 * 2, self.windowS[1] + 25]
        self.scrn.blit(timer, timer_rect)

        if self.completed:
            rec = pygame.Surface(self.windowS)
            rec.set_alpha(200)
            rec.fill([0, 150, 0])
            text1 = self.number_font.render("Completion Time of " + self.difficulty[0].upper() + " Mode :", True,
                                            self.black)
            text2 = self.number_font.render(str(self.total_seconds) + " Congratulations!!", True, self.black)
            text_rect1 = text1.get_rect()
            text_rect1.center = [self.windowS[0] // 2, self.windowS[0] // 2]
            text_rect2 = text2.get_rect()
            text_rect2.center = [self.windowS[0] // 2, self.windowS[0] // 2 + self.number_font.get_height() * 1.5]
            self.scrn.blit(rec, [0, 0])
            self.scrn.blit(text1, text_rect1)
            self.scrn.blit(text2, text_rect2)

        pygame.display.update()

    def events(self):
        self.currentN = [0, False]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                self.undoFlag = False
            if event.type == pygame.KEYDOWN:
                # Moving around with arrow keys
                if event.key == pygame.K_UP and self.cell_pos[1] != 0:
                    self.cell_pos[1] -= 1
                elif event.key == pygame.K_DOWN and self.cell_pos[1] != 8:
                    self.cell_pos[1] += 1
                elif event.key == pygame.K_RIGHT and self.cell_pos[0] != 8:
                    self.cell_pos[0] += 1
                elif event.key == pygame.K_LEFT and self.cell_pos[0] != 0:
                    self.cell_pos[0] -= 1
                elif event.key == pygame.K_ESCAPE:
                    self._quit()
                elif event.key == pygame.K_c:
                    # Resetting the game
                    self.__init__(self.name, self.windowS)
                    # self.completed = True
                elif event.key in range(48, 58) or event.key in [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
                                                                 pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7,
                                                                 pygame.K_KP8, pygame.K_KP9]:
                    # Changing the current number [0->9]
                    self.currentN = [int(event.unicode), True]
                elif event.key == pygame.K_BACKSPACE:
                    # Deleting the current cell number
                    self.currentN = [0, True]
                elif event.key == pygame.K_SPACE:
                    # Toggling between normal numbers and note numbers
                    self.mini_numberFlag += 1
                    if self.mini_numberFlag % 2:
                        self.notesN = self.number_font.render('Notes ON', True, (0, 0, 0), (0, 150, 0))
                    else:
                        self.notesN = self.number_font.render('Notes OFF', True, (0, 0, 0), (150, 0, 0))
                elif event.key == pygame.K_LCTRL:
                    self.undoFlag = True
                elif event.key == pygame.K_z and self.undoFlag and self.gridStorage:
                    self.grid = [[[row[0], row[1], row[2].copy()] for row in col] for col in self.gridStorage[-1]]
                    self.gridStorage.pop()
                    self.numberCounts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
                    for col in self.grid:
                        for n in col:
                            self.numberCounts[n[0]] += 1
        return True

    def save(self):
        """ Method for saving the highestScores for each difficulty"""
        try:
            with open('Sudoku/' + self.name + '.txt') as file:
                data = file.readlines()

            if self.difficulty[0] not in ' '.join(data):
                # If there is no record for the current difficulty
                data.append(f"{self.difficulty[0]} {self.total_seconds}\n")
                print(data)
            else:
                # If there is record for the current difficulty check if the time has been beaten
                for i, line in enumerate(data):
                    temp = line.split(' ')[1].split(':')
                    tempT = self.total_seconds.split(':')
                    if self.difficulty[0] in line:
                        if int(tempT[0]) < int(temp[0]) or \
                                (int(tempT[0]) == int(temp[0]) and int(tempT[1]) <= int(temp[1])):
                            data[i] = self.difficulty[0] + ' ' + self.total_seconds

            with open('Sudoku/' + self.name + '.txt', 'w') as file:
                file.writelines(data)
        except FileNotFoundError:
            with open('Sudoku/' + self.name + '.txt', 'w') as file:
                file.write(f"{self.difficulty[0]} {self.total_seconds}\n")
        return

    @staticmethod
    def _quit():
        pygame.quit()
