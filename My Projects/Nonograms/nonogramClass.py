"""
Created on Mon 19 Jul 20:28 2021
Finished on
@author: Cpt.Ender
                                  """
from itertools import permutations as perms


class Nonogram:
    def __init__(self, clues):
        self.clues = clues
        self.col_clues = clues[0]
        self.row_clues = clues[1]
        self.size = len(clues[0])
        self.solution = [[0 for _ in range(self.size)] for __ in range(self.size)]
        self.solutionT = []
        self.solved = False

        self.colPerms = [self.permutations(col) for col in self.col_clues]
        self.rowPerms = [self.permutations(row) for row in self.row_clues]

        self.maxW = max([len(row) for row in self.row_clues])
        self.maxH = max([len(col) for col in self.col_clues])
        self.height = self.size + (self.size + 1) + self.maxH
        self.width = self.size * 3 + (self.size + 1) + self.maxW * 2

    def transpose(self):
        """Returns the transpose of a matrix"""
        self.solutionT = []
        for i in range(len(self.solution[0])):
            self.solutionT.append([self.solution[j][i] for j in range(len(self.solution))])
        return

    def pushOver(self, ls: list):
        # Returns a list of all the permutations of the list pushed over if able
        new_ls = []
        lastOne = len(ls) - ls[::-1].index(1) - 1
        if lastOne != len(ls) - 1:
            count = self.size - lastOne - 1
            maxC = count
            while count:
                new_ls.append([])
                new_ls[-1].extend([0] * count)
                new_ls[-1].extend(ls[0:lastOne + 1])
                new_ls[-1].extend([0] * (maxC - count))
                count -= 1
        return new_ls

    def splitN2Pos(self, n_max, ln=0, n=0, index=0, ls=None, temp_ls=None):
        # Return all the combinations a number can be split in the available positions
        if ls is None:
            if not n_max:
                return [[0] * ln]
            if not n:
                n = n_max
            temp_ls = [0] * n_max
            ls = []
        if not ln:
            ln = n_max

        if n < 0:
            return
        if n == 0:
            if index <= ln:
                temp = [0] * (ln - index)
                ls.append(temp_ls[:index])
                ls[-1].extend(temp)
            return
        prev = 1 if (index == 0) else temp_ls[index - 1]

        for k in range(prev, n + 1):
            temp_ls[index] = k
            self.splitN2Pos(n_max, ln, n - k, index + 1, ls, temp_ls)
        return ls

    def permutations(self, arrangement):
        # Returns all the permutations of the arrangement
        ls = []
        n = self.size - sum(arrangement) - len(arrangement) + 1
        k = len(arrangement)
        for p in self.splitN2Pos(n, k):
            for stars in list(dict.fromkeys(list(perms(p)))):
                temp = []
                for i, starsN in enumerate(stars):
                    temp.extend([1] * arrangement[i])
                    if i != len(stars) - 1:
                        temp.extend([0] * (1 + starsN))
                    else:
                        temp.extend([0] * starsN)
                ls.append(temp)
                if not temp[-1]:
                    ls.extend(self.pushOver(temp))
        return ls

    def validate(self, rowIndex):
        # Checks if the current row is indeed in the available permutations of each column
        validation = [False] * self.size
        for i, col in enumerate(self.solutionT):
            for colPerm in self.colPerms[i]:
                if col[:rowIndex + 1] == colPerm[:rowIndex + 1]:
                    validation[i] = True
                    break
            if not validation[i]:
                return False
        return True

    def solve(self, x=0):
        if x == self.size:
            self.solved = True
            return
        row = self.rowPerms[x]
        for rowP in row:
            if self.solved:
                return tuple(tuple(row) for row in self.solution)
            self.solution[x] = rowP
            self.transpose()
            if self.validate(x):
                self.solve(x + 1)

            else:
                self.solution[x] = [0] * self.size
                self.transpose()
        return tuple(tuple(row) for row in self.solution)

    def draw(self):
        # Print the Column Clues
        for j in range(self.maxH):
            print('  ' * self.maxW + '| ' + ' | '.join(str(col[j + len(col) - self.maxH])
                                                       if j + len(col) - self.maxH >= 0
                                                       else ' ' for col in self.col_clues) + ' |')

        # Print the rows
        for i, row in enumerate(self.solution):
            print('_' * self.width)
            rowClues = '  ' * (self.maxW - len(self.row_clues[i])) + ''.join([str(n) + ' ' for n in self.row_clues[i]])
            print(rowClues + '|' + ''.join([' x |' if n else '   |' for n in row]))
        print('_' * self.width)


# clues = (
#     (
#         (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
#         (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
#         (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
#     ), (
#         (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
#         (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
#         (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
#     )
# )
#
# nono = Nonogram(clues)
# nono = Nonogram((((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,))))
# nono = Nonogram((((1, 1, 2), (1, 4), (2, 1), (1, 1, 1, 1), (1, 3, 1), (2, 1), (3, 2)),
#                  ((5, 1), (1, 2), (1, 4), (2, 1), (6,), (2, 1), (1, 2))))
#
# sol = nono.solve()
# nono.draw()
