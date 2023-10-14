"""
Created on Wed 28 Jul 16:29 2021
Finished on
@author: Cpt.Ender
                                  """
from itertools import permutations as perms


def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def combinations(n, k):
    comb = factorial(n + k - 1) / (factorial(k - 1) * factorial(n))
    return comb


def splitN2Pos(n_max, ln=0, n=0, index=0, ls=None, temp_ls=None):
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
        splitN2Pos(n_max, ln, n - k, index + 1, ls, temp_ls)
    return ls


def pushOver(ls: list):
    new_ls = []
    lastOne = len(ls) - ls[::-1].index(1) - 1
    if lastOne != len(ls) - 1:
        count = len(ls) - lastOne - 1
        maxC = count
        while count:
            new_ls.append([])
            new_ls[-1].extend([0] * count)
            new_ls[-1].extend(ls[0:lastOne + 1])
            new_ls[-1].extend([0] * (maxC - count))
            count -= 1

    return new_ls


def permutations(arrangement, ln):
    ls = []
    n = ln - sum(arrangement) - len(arrangement) + 1
    k = len(arrangement)
    numOfCombinations = combinations(n, k)
    for p in splitN2Pos(n, k):
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
                ls.extend(pushOver(temp))
    return ls


def generateCombis(currentPlace, numberOfPlaces, currentString, number):
    global combis
    if currentPlace > numberOfPlaces:
        return
    if number == 0:
        combis += currentString + str('0' * (numberOfPlaces - currentPlace))
        return

    for i in range(number+1):
        generateCombis(currentPlace + 1, numberOfPlaces, currentString + str(i), number - i)


combis = ''
nOfPlaces = 7
n = 7
generateCombis(0, nOfPlaces, '', n)
combis = list(dict.fromkeys([''.join(sorted(combis[i:i+n])) for i in range(0, len(combis), n)]))
# arr = splitN2Pos(7, 7)
# arr = permutations((2, 1, 2, 2), 11)
