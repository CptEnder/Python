"""
Created on Tue 02 Jun 04:10 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
import numpy as np

# file = open("out.txt", 'r')
# contents = file.read().split()
# file.close()
# x = []
# u = []
# for i in range(len(contents)//2):
#     x.append(float(contents[2*i]))
#     u.append(float(contents[2*i+1]))
#
# plt.plot(x, u)
# plt.grid()
# plt.axis('equal')

n = 50
dt = 0.01
v = 0.001
dx = 1 / n
r = v * dt / dx ** 2
k = dt / (2 * dx)
x = np.arange(0, 1 + dx, dx)


def fwd_Euler_CDS():
    u = [i for i in np.sin(2 * np.pi * x)]
    ii = 0
    plt.figure()
    plt.grid()
    plt.title('Forward Euler - Central Differencing Scheme')

    while max(u) >= 0.05:
        u_next = u[:]
        for i in range(1, n):
            u_next[i] = r * u[i + 1] + (1 - 2 * r) * u[i] + r * u[i - 1] - k * u[i] * (u[i + 1] - u[i - 1])

        if ii % (n / 5) == 0:
            plt.plot(x, u)
            plt.pause(1 / 600)
        u = u_next[:]
        ii += 1
    print('Explicit Euler CDS ', ii)


def bwd_Euler_CDS():
    u = [i for i in np.sin(2 * np.pi * x)]
    ii = 0
    plt.figure()
    plt.grid()
    plt.title('Backward Euler - Central Differencing Scheme')
    A = np.identity(len(x)) * (1 + r)
    A[0, 1] = k / 2 * u[1] - r / 2
    A[-1, -2] = -k / 2 * u[-2] - r / 2
    B = [0 for _ in range(len(x))]
    B[0] = (1 - r) * u[0] + r / 2 * u[1]
    B[-1] = 0.5 * r * u[-2] + (1 - r) * u[-1]

    while max(u) >= 0.05:
        u[0] = 0
        u[-1] = 0
        for i in range(1, n):
            a = -k / 2 * u[i - 1] - r / 2
            c = +k / 2 * u[i + 1] - r / 2
            B[i] = 0.5 * r * u[i - 1] + (1 - r) * u[i] + r / 2 * u[i + 1]
            A[i, i - 1] = a
            A[i, i + 1] = c

        if ii % (n / 5) == 0:
            plt.plot(x, u)
            plt.pause(1 / 600)
        u = np.linalg.solve(A, B)
        ii += 1
    print('Implicit Euler CDS ', ii)


fwd_Euler_CDS()
bwd_Euler_CDS()
