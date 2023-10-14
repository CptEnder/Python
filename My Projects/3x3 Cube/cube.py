"""
Created on Wed 14 Sep 13:49 2022
Finished on Wed 14 Sep 20:00 2022
@author: Cpt.Ender

3x3 Cube class that includes :
- all 6 basics moves and their inverses
- scrambler function that follows input string of moves
                                                        """
import numpy as np
from random import choice


class Cube:
    def __init__(self, startingPos=None):
        [self.UP, self.LEFT, self.FRONT, self.RIGHT, self.BACK, self.DOWN] = self.initialPos(startingPos)
        self.printCube()

    @staticmethod
    def initialPos(startingPos: list):
        if startingPos:
            return startingPos
        return [[[f'W{i + 3 * ii}' for i in range(3)] for ii in range(3)],
                [[f'O{i + 3 * ii}' for i in range(3)] for ii in range(3)],
                [[f'G{i + 3 * ii}' for i in range(3)] for ii in range(3)],
                [[f'R{i + 3 * ii}' for i in range(3)] for ii in range(3)],
                [[f'B{i + 3 * ii}' for i in range(3)] for ii in range(3)],
                [[f'Y{i + 3 * ii}' for i in range(3)] for ii in range(3)]]

    def scramble(self, moves=None):
        """
        Function to apply the moves passed as a string
        if 'moves' is None then perform a random scramble
        :param moves: string of moves separated with spaces
        """
        if moves is None:
            moves = ''
            mChoices = ['U', 'R', 'L', 'F', 'B', 'D',
                        "U'", "R'", "L'", "F'", "B'", "D'",
                        'U2', 'R2', 'L2', 'F2', 'B2', 'D2']
            previousMove = choice(mChoices)
            for i in range(30):
                nextMove = choice(mChoices)
                while nextMove[0] == previousMove[0]:
                    nextMove = choice(mChoices)
                moves += ' ' + nextMove
                previousMove = nextMove
        print(moves + '\n')
        moves = moves.upper().lstrip().split(' ')
        for m in moves:
            inverse = 0
            double = 1
            if len(m) == 2:
                if m[1].isdigit():
                    double = 2 ** ((int(m[1]) + 1) % 2)
                    if int(m[1]) % 4 == 3:
                        inverse = 1
                elif m[1] == "'" or m[1] == 'I':
                    inverse = 1
                else:
                    print(f'Incorrect format or symbol {m}')
                    return
            for i in range(double):
                if m[0] == 'U':
                    self.upMove(inverse)
                elif m[0] == 'D':
                    self.downMove(inverse)
                elif m[0] == 'F':
                    self.frontMove(inverse)
                elif m[0] == 'R':
                    self.rightMove(inverse)
                elif m[0] == 'L':
                    self.leftMove(inverse)
                elif m[0] == 'B':
                    self.backMove(inverse)
                else:
                    print(f'Incorrect format or symbol {m}')
                    return

    def upMove(self, inverse=0):
        """
        Function to apply moving the upper face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.UP = np.rot90(self.UP, 3 + inverse * (-2)).tolist()
        temp = self.FRONT[0]
        if inverse:
            self.FRONT[0] = self.LEFT[0]
            self.LEFT[0] = self.BACK[0]
            self.BACK[0] = self.RIGHT[0]
            self.RIGHT[0] = temp
        else:
            self.FRONT[0] = self.RIGHT[0]
            self.RIGHT[0] = self.BACK[0]
            self.BACK[0] = self.LEFT[0]
            self.LEFT[0] = temp
        self.printCube()

    def downMove(self, inverse=0):
        """
        Function to apply moving the down face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.DOWN = np.rot90(self.DOWN, 3 + inverse * (-2)).tolist()
        temp = self.FRONT[2]
        if not inverse:
            self.FRONT[2] = self.LEFT[2]
            self.LEFT[2] = self.BACK[2]
            self.BACK[2] = self.RIGHT[2]
            self.RIGHT[2] = temp
        else:
            self.FRONT[2] = self.RIGHT[2]
            self.RIGHT[2] = self.BACK[2]
            self.BACK[2] = self.LEFT[2]
            self.LEFT[2] = temp
        self.printCube()

    def frontMove(self, inverse=0):
        """
        Function to apply moving the front face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.FRONT = np.rot90(self.FRONT, 3 + inverse * (-2)).tolist()
        temp = self.UP[2]
        if not inverse:
            self.UP[2] = [self.LEFT[2][2], self.LEFT[1][2], self.LEFT[0][2]]
            [self.LEFT[0][2], self.LEFT[1][2], self.LEFT[2][2]] = self.DOWN[0]
            self.DOWN[0] = [self.RIGHT[2][0], self.RIGHT[1][0], self.RIGHT[0][0]]
            [self.RIGHT[2][0], self.RIGHT[1][0], self.RIGHT[0][0]] = temp[::-1]
        else:
            self.UP[2] = [self.RIGHT[0][0], self.RIGHT[1][0], self.RIGHT[2][0]]
            [self.RIGHT[0][0], self.RIGHT[1][0], self.RIGHT[2][0]] = self.DOWN[0][::-1]
            self.DOWN[0] = [self.LEFT[0][2], self.LEFT[1][2], self.LEFT[2][2]]
            [self.LEFT[0][2], self.LEFT[1][2], self.LEFT[2][2]] = temp[::-1]
        self.printCube()

    def backMove(self, inverse=0):
        """
        Function to apply moving the back face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.BACK = np.rot90(self.BACK, 3 + inverse * (-2)).tolist()
        temp = self.UP[0]
        if not inverse:
            self.UP[0] = [self.RIGHT[0][2], self.RIGHT[1][2], self.RIGHT[2][2]]
            [self.RIGHT[0][2], self.RIGHT[1][2], self.RIGHT[2][2]] = self.DOWN[2][::-1]
            self.DOWN[2] = [self.LEFT[0][0], self.LEFT[1][0], self.LEFT[2][0]]
            [self.LEFT[0][0], self.LEFT[1][0], self.LEFT[2][0]] = temp[::-1]
        else:
            self.UP[0] = [self.LEFT[2][0], self.LEFT[1][0], self.LEFT[0][0]]
            [self.LEFT[2][0], self.LEFT[1][0], self.LEFT[0][0]] = self.DOWN[2][::-1]
            self.DOWN[2] = [self.RIGHT[2][2], self.RIGHT[1][2], self.RIGHT[0][2]]
            [self.RIGHT[2][2], self.RIGHT[1][2], self.RIGHT[0][2]] = temp[::-1]
        self.printCube()

    def rightMove(self, inverse=0):
        """
        Function to apply moving the right face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.RIGHT = np.rot90(self.RIGHT, 3 + inverse * (-2)).tolist()
        temp = [self.UP[0][2], self.UP[1][2], self.UP[2][2]]
        if not inverse:
            [self.UP[0][2], self.UP[1][2], self.UP[2][2]] = [self.FRONT[0][2], self.FRONT[1][2], self.FRONT[2][2]]
            [self.FRONT[0][2], self.FRONT[1][2], self.FRONT[2][2]] = [self.DOWN[0][2], self.DOWN[1][2], self.DOWN[2][2]]
            [self.DOWN[0][2], self.DOWN[1][2], self.DOWN[2][2]] = [self.BACK[2][0], self.BACK[1][0], self.BACK[0][0]]
            [self.BACK[2][0], self.BACK[1][0], self.BACK[0][0]] = temp
        else:
            [self.UP[0][2], self.UP[1][2], self.UP[2][2]] = [self.BACK[2][0], self.BACK[1][0], self.BACK[0][0]]
            [self.BACK[2][0], self.BACK[1][0], self.BACK[0][0]] = [self.DOWN[0][2], self.DOWN[1][2], self.DOWN[2][2]]
            [self.DOWN[0][2], self.DOWN[1][2], self.DOWN[2][2]] = [self.FRONT[0][2], self.FRONT[1][2], self.FRONT[2][2]]
            [self.FRONT[0][2], self.FRONT[1][2], self.FRONT[2][2]] = temp
        self.printCube()

    def leftMove(self, inverse=0):
        """
        Function to apply moving the left face
        clockwise and anticlockwise
        :param inverse: 1 if the move is anticlockwise
        """
        self.LEFT = np.rot90(self.LEFT, 3 + inverse * (-2)).tolist()
        temp = [self.UP[0][0], self.UP[1][0], self.UP[2][0]]
        if inverse:
            [self.UP[0][0], self.UP[1][0], self.UP[2][0]] = [self.FRONT[0][0], self.FRONT[1][0], self.FRONT[2][0]]
            [self.FRONT[0][0], self.FRONT[1][0], self.FRONT[2][0]] = [self.DOWN[0][0], self.DOWN[1][0], self.DOWN[2][0]]
            [self.DOWN[0][0], self.DOWN[1][0], self.DOWN[2][0]] = [self.BACK[2][2], self.BACK[1][2], self.BACK[0][2]]
            [self.BACK[2][2], self.BACK[1][2], self.BACK[0][2]] = temp
        else:
            [self.UP[0][0], self.UP[1][0], self.UP[2][0]] = [self.BACK[2][2], self.BACK[1][2], self.BACK[0][2]]
            [self.BACK[2][2], self.BACK[1][2], self.BACK[0][2]] = [self.DOWN[0][0], self.DOWN[1][0], self.DOWN[2][0]]
            [self.DOWN[0][0], self.DOWN[1][0], self.DOWN[2][0]] = [self.FRONT[0][0], self.FRONT[1][0], self.FRONT[2][0]]
            [self.FRONT[0][0], self.FRONT[1][0], self.FRONT[2][0]] = temp
        self.printCube()

    def printCube(self):
        """
        Function to print the cube in flat format in the console
        """
        for row in self.UP:
            print(' ' * 9 + '| ' + ' '.join(row) + ' |')
        print(' ' * 11 + '_' * 8)
        for i in range(3):
            print(' '.join(self.LEFT[i] + ['|'] + self.FRONT[i] + ['|'] + self.RIGHT[i] + ['|'] + self.BACK[i]))
        print(' ' * 11 + '_' * 8)
        for row in self.DOWN:
            print(' ' * 9 + '| ' + ' '.join(row) + ' |')
        print('')


cube = Cube()
# cube.scramble()
# cube.scramble('2R M')
# cube.scramble("F' D L B2 F' R' D2 L' R' U2")
cube.scramble("L2 B2 D2 U' F2 D B2 D' R F L R2 D B2 R' F' L R2 B U2 B' U2 L' B2 L' D' L F R' D'")
# cube.leftMove()
# cube.rightMove()
# cube.backMove()
# cube.frontMove()
# cube.upMove()
# cube.downMove()
# cube.upMove(1)
# cube.backMove(1)
# cube.downMove(1)
# cube.frontMove(1)
# cube.leftMove(1)
# cube.rightMove(1)
