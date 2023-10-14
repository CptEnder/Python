"""
Created on Mon 23 Jan 14:59 2023
Finished on Sun 05 Feb 20:00 2023
@author: Cpt.Ender

https://www.desmos.com/calculator/ejyqyu7gtt
https://www.codewars.com/kata/5886e082a836a691340000c3

A rectangle with sides equal to even integers a and b is drawn on the Cartesian plane.
Its center (the intersection point of its diagonals) coincides with the point (0, 0),
but the sides of the rectangle are not parallel to the axes;
instead, they are forming 45 degree angles with the axes.

How many points with integer coordinates are located inside the given rectangle (including on its sides)?

Example
For a = 6 and b = 4, the output should be 23

The following picture illustrates the example, and the 23 points are marked green.

rect:  mult| actual| not tilted
2x2  : 4   | 5     | 9
2x4  : 8   | 7     | 15
2x6  : 12  | 13    | 21
2x8  : 16  | 17    | 27
2x10 : 20  | 23    | 33
4x4  : 16  | 13    | 25
4x6  : 24  | 23    | 35
4x8  : 32  | 27    | 45
4x10 : 40  | 37    | 55
6x6  : 36  | 41    | 49
6x8  : 48  | 49    | 63
6x10 : 60  | 67    | 77
8x8  : 64  | 61    | 81
8x10 : 80  | 83    | 99
                                  """


# My solution
def rectangle_rotation(a, b):
    x = a // 2 ** (1 / 2)
    y = b // 2 ** (1 / 2)
    k = 0
    m = 0
    if x / 2 > a / 2 // 2 ** (1 / 2):
        k = 1
    if y / 2 > b / 2 // 2 ** (1 / 2):
        m = 1
    if k == m:
        points = (x + 1) * (y + 1) + x * y
    else:
        points = (x + 1 - m) * (y + 1 - k) + (x + m) * (y + k)
    # print(f"{a} x {b}:", k, m, x, y, points)
    return points


def rectangle_rotation2(a, b):
    a //= 2 ** 0.5
    b //= 2 ** 0.5
    points = a * b + (a + 1) * (b + 1)
    return points + points % 2 - 1


for a in range(2, 10, 2):
    for b in range(a, 10, 2):
        print(rectangle_rotation(a, b) == rectangle_rotation2(a, b))
