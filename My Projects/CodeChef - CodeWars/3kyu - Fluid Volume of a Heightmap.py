"""
Created on Fri 17 Feb 11:58 2023
Finished on
@author: Cpt.Ender

https://www.codewars.com/kata/5b98dfa088d44a8b000001c1/train/python
Given a height map as a 2D array of integers, return the volume of liquid that it could contain. For example:

heightmap:
  8 8 8 8 6 6 6 6
  8 0 0 8 6 0 0 6
  8 0 0 8 6 0 0 6
  8 8 8 8 6 6 6 0

filled:
  8 8 8 8 6 6 6 6
  8 8 8 8 6 6 6 6
  8 8 8 8 6 6 6 6
  8 8 8 8 6 6 6 0

result: 4*8 + 4*6 = 56
For this heightmap, you would return 56: were you to pour water over it until
it couldn't contain any more, it would look like the second heightmap, taking on 56 units of water in the process.

Water pours off the edges of the heightmap, even when they are negative.
It doesn't flow through diagonal cracks (note the lower-right corner of the example).
Heightmaps in the test cases will come in many different sizes, and some will be quite large,
but they will always be rectangular. Heights may be negative.

Performances requirements:
Think about the efficiency of your solution:

50 big random tests and maps around 100x100

def _():
        pretty_test([[0]], 0)
        pretty_test([[22]], 0)
        pretty_test([[2, 1, 2],
                     [1, 0, 1],
                     [2, 1, 2]], 1)
        pretty_test([[1, 1, 1],
                     [1, 8, 1],
                     [1, 1, 1]], 0)
        pretty_test([[9, 9, 9, 9],
                     [9, 0, 0, 9],
                     [9, 0, 0, 9],
                     [9, 9, 9, 9]], 36)
        pretty_test([[9, 9, 9, 9, 9],
                     [9, 0, 1, 2, 9],
                     [9, 7, 8, 3, 9],
                     [9, 6, 5, 4, 9],
                     [9, 9, 9, 9, 9]], 45)
        pretty_test([[8, 8, 8, 8, 6, 6, 6, 6],
                     [8, 0, 0, 8, 6, 0, 0, 6],
                     [8, 0, 0, 8, 6, 0, 0, 6],
                     [8, 8, 8, 8, 6, 6, 6, 0]], 56)
        pretty_test([[ 0, 10,  0, 20,  0],
                     [20,  0, 30,  0, 40],
                     [ 0, 40,  0, 50,  0],
                     [50,  0, 60,  0, 70],
                     [ 0, 60,  0, 70,  0]], 150)
        pretty_test([[3, 3, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3],
                     [3, 0, 0, 0, 3],
                     [3, 0, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3]], 0)
        pretty_test([[3, 3, 3, 3, 3],
                     [3, 2, 2, 2, 3],
                     [3, 3, 3, 2, 3],
                     [3, 1, 1, 1, 3],
                     [3, 1, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3]], 0)
        f=lambda:[[3, 3, 3, 3, 3],
                  [3, 0, 0, 0, 3],
                  [3, 3, 3, 0, 3],
                  [3, 0, 0, 0, 3],
                  [3, 0, 3, 3, 3],
                  [3, 0, 0, 0, 3],
                  [3, 3, 3, 1, 3]]
        pretty_test(f(), 11)
        pretty_test(f()[::-1], 11)
        pretty_test([ r[::-1] for r in f()], 11)
        pretty_test([ r[::-1] for r in reversed(f())], 11)

    @test.it("Tests with negative heights")
    def _():
        pretty_test([[-1]], 0)
        pretty_test([[3, 3, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3],
                     [3, 0, -2, 0, 3],
                     [3, 0, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 1, -3]], 13)
        pretty_test([[8192, 8192, 8192, 8192],
                     [8192,-8192,-8192, 8192],
                     [8192,-8192,-8192, 8192],
                     [8192, 8192, 8192, 8192]], 65536)
                                                              """


def volume(heightmap):
    a = len(heightmap)
    b = len(heightmap[0])
    if max(a, b) <= 3 and min(a, b) < 3:
        return 0

    for i in range(1, len(heightmap) - 1):
        for j in range(1, len(heightmap[1]) - 1):
            value = heightmap[i][j]
            if all(value <= neigh for neigh in [heightmap[i - 1][j], heightmap[i + 1][j],
                                                heightmap[i][j - 1], heightmap[i][j + 1]]):
                print(value)
    return 1


print(volume([[1, 2], [2, 1], [1, 3]]))
print(volume([[3, 3, 3, 3, 3],
              [3, 2, 2, 2, 3],
              [3, 3, 3, 2, 3],
              [3, 1, 1, 1, 3],
              [3, 1, 3, 3, 3],
              [3, 0, 0, 0, 3],
              [3, 3, 3, 0, 3]]))

print(volume([[3, 3, 3, 3, 3],
              [3, 0, 0, 0, 3],
              [3, 3, 3, 0, 3],
              [3, 0, -2, 0, 3],
              [3, 0, 3, 3, 3],
              [3, 0, 0, 0, 3],
              [3, 3, 3, 1, -3]]))
print(volume([[9, 9, 9, 9],
              [9, 0, 0, 9],
              [9, 0, 0, 9],
              [9, 9, 9, 9]]))
print(volume([[0, 10, 0, 20, 0],
              [20, 0, 30, 0, 40],
              [0, 40, 0, 50, 0],
              [50, 0, 60, 0, 70],
              [0, 60, 0, 70, 0]]))
