"""
Created on Wed 23 Sep 10:56 2020
Finished on Sat 26 Sep 22:00 2020
@author: Cpt.Ender
                                  """
import pygame


class Board:
    def __init__(self, name, win_size: list, grid_size: list):
        """
        A method for the initialization of a Board
        Contains: screen width and height, box width and height
                  a list of obstacles, a start and a finish node
        """
        pygame.init()
        self.window_size = win_size
        self.grid_size = grid_size
        self.w_ = self.window_size[0] // self.grid_size[0]
        self.h_ = self.window_size[1] // self.grid_size[1]
        self.game_size = [self.window_size[0] + 1, self.window_size[1] + 1]
        self.name = name
        pygame.display.set_caption(self.name)
        self.scrn = pygame.display.set_mode(self.game_size)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.black = [0] * 3
        self.white = [200] * 3
        self.blue = [0, 0, 200]
        self.red = [150, 0, 0]
        self.green = [0, 200, 0]
        self.yellow = [0, 180, 150]
        # self._init()
        print("\nHelpful keybindings:")
        print("Lft_mouse_bt : Create an Obstacle at mouse position")
        print("Rgt_mouse_bt : Remove Obstacle at mouse position")
        print("Mddle_mouse_button : Remove and Replace start or finish tiles.\n"
              "                     To remove it the mouse must be above the occupied tile")
        print("Spacebar: Starts the searching algorithm")
        print("C : reinitializes the board")

    # def _init(self):
        self.obstacles = []  # Obstacle list
        self.Grid = self.makeGrid()
        self.start_node = self.Grid[0][0]  # Starting position
        self.end_node = self.Grid[self.grid_size[1] - 1][self.grid_size[0] - 1]  # Finishing position
        self.movingStartNode = False
        self.movingEndNode = False
        self.Alg_running = False
        self.checkedList = []
        self.path = []

    def _mouseEventAndPosition(self):
        """ Method for converting the mouse position  to cell position,
        and returning the mouse button pressed"""
        mouse_pos = pygame.mouse.get_pos()
        # If left click is pressed and the mouse is inside the grid
        if pygame.mouse.get_pressed() != (0, 0, 0) and max(mouse_pos) < max(self.window_size):
            cell_pos = [mouse_pos[0] * 1 // self.w_, mouse_pos[1] * 1 // self.h_]
            mouse_button = None
            if pygame.mouse.get_pressed() == (1, 0, 0):
                # Convert mouse position to cell position
                mouse_button = 0
            elif pygame.mouse.get_pressed() == (0, 1, 0):
                mouse_button = 1
            elif pygame.mouse.get_pressed() == (0, 0, 1):
                mouse_button = 2
            return cell_pos, mouse_button
        return [], None  # return a default value

    def makeGrid(self):
        """ A method to fill the Grid array with Node objects """
        grid = [[Node(x, y) for x in range(self.grid_size[0])]
                for y in range(self.grid_size[1])]
        return grid

    def _updateNodes(self):
        """ Check and update every node's attributes """
        for row in self.Grid:
            for node in row:
                if node.pos in self.obstacles:
                    node.traversable = False
                else:
                    node.traversable = True
                node.neighbors = self._get_neighbors(node)
                node.h_cost = get_Distance(node, self.end_node)
                node.update_f_Cost()
        self.start_node.g_cost = 0

    def _get_neighbors(self, node):
        """ Add neighbors (no diagonals) to the given node """
        neighbors = []

        for [x, y] in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
            checkX = node.x + x
            checkY = node.y + y

            if 0 <= checkX < self.grid_size[0] and 0 <= checkY < self.grid_size[1]:
                neighbors.append(self.Grid[checkY][checkX])
        return neighbors

    def Retrace_Path(self):
        """ Makes a path from the end to the start, by retracing
        the parents of each node and then reversing that list """
        current_node = self.end_node

        while current_node != self.start_node:
            self.path.append(current_node)
            current_node = current_node.parent
        self.path.reverse()

    def quit(self):
        pygame.quit()

    def _updateState(self):
        self._updateNodes()  # Updates the neighbors list and the values of the costs  for each node
        self.path = []  # Emptying the path list
        self.checkedList = []

    def logig(self):
        """ Method for the logic of the board. Making and removing obstacles,
        moving the start and ending """
        selected_cell, mouse_button = self._mouseEventAndPosition()

        if selected_cell and not self.Alg_running:
            if mouse_button == 0 and selected_cell not in self.obstacles:
                # Add an obstacle
                self.obstacles.append(selected_cell)
            elif mouse_button == 2 and selected_cell in self.obstacles:
                # Remove an Obstacle
                self.obstacles.pop(self.obstacles.index(selected_cell))
            elif mouse_button == 1 and selected_cell == self.start_node.pos and not self.movingEndNode:
                # Remove Starting Node
                self.movingStartNode = True
            elif mouse_button == 1 and self.movingStartNode:
                # Place Starting Node
                self.start_node = self.Grid[selected_cell[1]][selected_cell[0]]
                self.movingStartNode = False
                pygame.time.wait(100)
            elif mouse_button == 1 and selected_cell == self.end_node.pos and not self.movingStartNode:
                # Remove Finish Node
                self.movingEndNode = True
            elif mouse_button == 1 and self.movingEndNode:
                # Place Finish Node
                self.end_node = self.Grid[selected_cell[1]][selected_cell[0]]
                self.movingEndNode = False
                pygame.time.wait(100)
            pygame.time.wait(100)
        for i, cell in enumerate(self.obstacles):
            if cell == self.start_node.pos or cell == self.end_node.pos:
                self.obstacles.pop(i)

    def draw(self):
        """ A method to draw the board, the obstacles, the path,
         and the beginning and ending on the screen """

        self.scrn.fill(self.white)  # Background Colour

        for node in self.checkedList:
            pygame.draw.rect(self.scrn, self.yellow, [[node.x * self.w_, node.y * self.h_],
                                                      [self.w_, self.h_]])

        # Drawing the Path
        for node in self.path:
            pygame.draw.rect(self.scrn, self.green, [[node.x * self.w_, node.y * self.h_],
                                                     [self.w_, self.h_]])

        # Drawing the Obstacles
        for obs in self.obstacles:
            pygame.draw.rect(self.scrn, self.black, [[obs[0] * self.w_, obs[1] * self.h_], [self.w_, self.h_]])
        # Drawing the Start
        if not self.movingStartNode:
            pygame.draw.rect(self.scrn, self.blue, [[self.start_node.x * self.w_, self.start_node.y * self.h_],
                                                    [self.w_, self.h_]])
        # Drawing the End
        if not self.movingEndNode:
            pygame.draw.rect(self.scrn, self.red, [[self.end_node.x * self.w_, self.end_node.y * self.h_],
                                                   [self.w_, self.h_]])

        # Drawing the Grid Lines
        for i in range(self.grid_size[0] + 1):
            pygame.draw.line(self.scrn, self.black, [i * self.w_, 0], [i * self.w_, self.window_size[1]])
        for j in range(self.grid_size[1] + 1):
            pygame.draw.line(self.scrn, self.black, [0, j * self.h_], [self.window_size[0], j * self.h_])

        pygame.display.update()

    def running(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_c:
                    self.__init__(self.name, self.window_size, self.grid_size)
                if event.key == pygame.K_SPACE:
                    if not self.end_node.pos or not self.start_node.pos:
                        print('Missing Start or End')
                    else:
                        self.Alg_running = not self.Alg_running
                    self._updateState()
                    pygame.time.wait(100)
        return True


class Node:
    def __init__(self, x, y):
        """ A class to create Node objects """
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.g_cost = float('inf')  # Distance from start
        self.h_cost = 0  # Distance from end
        self.f_cost = 0  # Sum of G cost and H cost
        self.traversable = True  # Is it an obstacle or not
        self.parent = None  # What was the previous node
        self.neighbors = []

    def update_f_Cost(self):
        self.f_cost = self.g_cost + self.h_cost


def get_Distance(node1: Node, node2: Node):
    """ The manhattan distance between two nodes"""
    distance = abs(node1.x - node2.x) + abs(node1.y - node2.y)
    return distance
