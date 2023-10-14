"""
Created on Sun 03 Jul 11:28 2022
Finished on Sun 03 Jul 12:00 2022
@author: Cpt.Ender
                                  """
import matplotlib.pyplot as plt
from random import choice
from math import sqrt

# shape = [(0, 0), (0.5, sqrt(3)/2), (1, 0), (0, 0)]
# shape = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]  # Rectangle
shape = [(0, 1), (0.25 * sqrt(10 + 2 * sqrt(5)), 0.25 * (sqrt(5) - 1)),
         (0.25 * sqrt(10 - 2 * sqrt(5)), -0.25 * (sqrt(5) + 1)),
         (-0.25 * sqrt(10 - 2 * sqrt(5)), -0.25 * (sqrt(5) + 1)),
         (-0.25 * sqrt(10 + 2 * sqrt(5)), 0.25 * (sqrt(5) - 1)), (0, 1)]  # Regular Pentagon

N = 100000
x = [0.25]
y = [0.25]

plt.plot([p[0] for p in shape], [p[1] for p in shape])
previous_k = -1  # Only when using rectangle
for i in range(1, N):
    k = choice([j for j in range(len(shape) - 1) if j != previous_k])  # random vertex
    # previous_k = k  # Only when using rectangle otherwise comment out
    x += [(shape[k][0] + x[i - 1]) / 2]
    y += [(shape[k][1] + y[i - 1]) / 2]

for i in range(1, N + 1):
    n = N // 50
    if not i % n:
        print(i / N * 100)
        plt.scatter(x[i - n:i], y[i - n:i], marker='.', s=1)
        plt.pause(0.01)
plt.show()
