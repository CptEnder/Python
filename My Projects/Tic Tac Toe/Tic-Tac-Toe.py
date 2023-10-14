"""
Created on Wed 16 Sep 12:09 2020
Finished on Thu 17 Sep 12:00 2020
@author: Cpt.Ender
                                  """
import pygame
from MiniMax_algorithm import next_move, winning


class Game:
    def __init__(self, players: list):
        """
        A method for the initialization of the game
        Contains: screen width and height, box width and height
                  a list of boxes filled and yet to be filled,
                  the board array and who's playing
        """
        pygame.init()
        self.width_s = 600
        self.height_s = 600
        self.w_ = self.width_s // 3
        self.h_ = self.height_s // 3
        pygame.display.set_caption("Tic-Tac-Toe.py")
        self.scrn = pygame.display.set_mode((self.width_s + 1, self.height_s + 1))
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.black = [0] * 3
        self.white = [200] * 3
        self.available_boxes = [[j, i] for i in range(3) for j in range(3)]  # All boxes ara available at the beginning
        self.filled_boxes = []  # nothing is filled yet
        self.X_boxes = []
        self.O_boxes = []
        self.board = [['_' for _ in range(3)] for _ in range(3)]
        self.Game_State = True  # State of the game
        self.players = players  # Who are the players
        self.current_player = self.players[0]

    def _board(self):
        """ A method to create the board array """
        for pos in self.available_boxes:
            self.board[pos[0]][pos[1]] = '_'
        for x in self.X_boxes:
            self.board[(x - 1) // 3][(x - 1) % 3] = 'x'
        for o in self.O_boxes:
            self.board[(o - 1) // 3][(o - 1) % 3] = 'o'

    def _pieces(self):
        self.X_boxes = []
        self.O_boxes = []
        for i, pos in enumerate(self.filled_boxes):
            if i % 2 == 0:  # If it's an even number then it means it's an X
                if pos[0] * 1 + pos[1] * 3 + 1 not in self.X_boxes:
                    self.X_boxes.append(pos[0] * 1 + pos[1] * 3 + 1)
            else:  # If it's an odd number then it means it's an O
                if pos[0] * 1 + pos[1] * 3 + 1 not in self.O_boxes:
                    self.O_boxes.append(pos[0] * 1 + pos[1] * 3 + 1)

    def logig(self, selected_pos: list):
        """
        Method for the logic of the game. Applying the selected move,
        if possible, and checking if the game ended.
        """
        # Check if the box that was selected is the available_boxes list
        if selected_pos in self.available_boxes:
            index = self.available_boxes.index(selected_pos)
            self.available_boxes.pop(index)
            self.filled_boxes.append(selected_pos)
            # Switch players
            self.current_player = self.players[self.players.index(self.current_player) ^ 1]

        self._pieces()
        self._board()

        # Check if the game ended
        winner = winning(self.board)
        if winner and winner != 'Tie':
            print('The winner is ' + winner)
            self.Game_State = False
        elif winner and winner == 'Tie':
            print("It's a Tie")
            self.Game_State = False

    def draw(self):
        """ A method to draw the board and all the pieces on the screen """
        self.scrn.fill(self.white)  # Background Colour
        # Drawing the Board
        for i in range(1, 3):
            x = i * self.w_
            y = i * self.h_
            pygame.draw.line(self.scrn, self.black, [x, 0], [x, self.height_s], 3)
            pygame.draw.line(self.scrn, self.black, [0, y], [self.width_s, y], 3)

        # Drawing the pieces
        for j, row in enumerate(self.board):
            for i, piece in enumerate(row):
                pos = [i * self.w_ + self.w_ // 2, j * self.w_ + self.w_ // 2]
                if piece == 'x':
                    pygame.draw.line(self.scrn, self.black, [pos[0] - self.w_ // 3, pos[1] - self.h_ // 3],
                                     [pos[0] + self.w_ // 3, pos[1] + self.h_ // 3], 4)
                    pygame.draw.line(self.scrn, self.black, [pos[0] + self.w_ // 3, pos[1] - self.h_ // 3],
                                     [pos[0] - self.w_ // 3, pos[1] + self.h_ // 3], 4)
                elif piece == 'o':
                    pygame.draw.circle(self.scrn, self.black, pos, 2 * self.w_ // 5, 2)

        pygame.display.update()


def running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.KEYDOWN:  # Undo previous move
                if event.key == pygame.K_LCTRL and game.filled_boxes:
                    game.available_boxes.append(game.filled_boxes.pop())
                    if 'AI' in Players:
                        game.available_boxes.append(game.filled_boxes.pop())
                    game.Game_State = True
                if event.key == pygame.K_r:  # Restarts the Game
                    game.__init__(game.players)
                if event.key == pygame.K_SPACE:  # Switch Players
                    game.__init__([game.players[1], game.players[0]])

    return True


def mouse_position():
    mouse_pos = pygame.mouse.get_pos()
    # If left click is pressed and the mouse is inside the grid
    if pygame.mouse.get_pressed() != (0, 0, 0) and max(mouse_pos) < game.width_s:
        # Convert mouse position to cell position
        cell_pos = [mouse_pos[0] * 3 // game.width_s, mouse_pos[1] * 3 // game.height_s]
        return cell_pos
    return [-1, -1]  # return a default value


if __name__ == '__main__':
    Players = ['AI', 'Human']
    game = Game(Players)

    while running():
        game.clock.tick(15)
        if game.Game_State:
            if game.current_player == 'Human':
                game.logig(mouse_position())
            elif game.current_player == 'AI':
                AI_pos = next_move(game.board)  # AI's selection
                game.logig([AI_pos[1], AI_pos[0]])
        game.draw()

    pygame.quit()
