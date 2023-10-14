"""
Created on Sat 02 Jul 17:07 2022
Finished on Sun 03 Jul 11:00 2022
@author: Cpt.Ender
                                  """
from matplotlib import pyplot as plt


def translate(arr: list, l: int, angle=1):
    temp = [arr[0][:], arr[1][:]]
    for i in range(len(arr[0])):
        if angle:
            temp[0][i] += l / 2
            temp[1][i] += l
        else:
            temp[0][i] += l
            temp[1][i] += 0
    return temp


def copy(points: list, l: int):
    temp = []
    for p in points:
        temp += [[__[:] for __ in p[:]]]
    for tria in temp:
        trans1 = translate(tria, l, 1)
        trans2 = translate(tria, l, 0)
        points += [trans1] + [trans2]


def sierpinskiTriangle(nStart: int, n: int = None, points=None, l=1):
    if points is None:
        points = [[[0, l / 2, l, 0], [0, l, 0, 0]]]
    if n is None:
        n = nStart
    if n <= 1:
        return points
    else:
        copy(points, l)
        sierpinskiTriangle(nStart, n - 1, points, l * 2)

    return points


if __name__ == '__main__':
    Triangles = sierpinskiTriangle(6)
    for triangle in Triangles:
        plt.plot(triangle[0], triangle[1])
