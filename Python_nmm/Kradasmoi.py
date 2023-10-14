"""
Created on Wed 20 Jan 20:15 2021
Finished on
@author: Παύλος Λοΐζου (nm16801)

Runge-Kutta 4th Order Method to
Solve Differential Equation
                                  """
import matplotlib.pyplot as plt
from math import cos, pi

ND = 10

# System's Dimensions (NxN)
N = 6
# Natural Period of the oscillator Me
T = 1
we = 2 * pi
W = 5 / 2 * we
# [A,B] time interval
A = 0
B = 150 * T
# Number of Step
M = 15000
# Step Size
H = (B - A) // M
# Initial time value
X = A
# Initial Vector (Dimension N)
Y = [0] * N


def f(x, y):
    V[0] = y[1]
    V[1] = -0.04 * pi * y[1] + 0.02 * pi * y[3] - 25 * pi ** 2 * y[0] + 10 * pi ** 2 * y[2]
    V[2] = y[3]
    if 3 * T - T / 10 <= x <= 3 * T + T / 10:
        V[3] = 0.08 * pi * y[1] - 0.12 * pi * y[3] + 0.04 * pi * y[5] + 0.4 * pi ** 2 * y[0] - 4.4 * pi ** 2 \
               * y[2] + 4 * pi ** 2 * y[4] + 2 * cos(W * x) + 5
    else:
        V[3] = 0.08 * pi * y[1] - 0.12 * pi * y[3] + 0.04 * pi * y[5] + 0.4 * pi ** 2 * y[0] - 4.4 * pi ** 2 \
               * y[2] + 4 * pi ** 2 * y[4] + 2 * cos(W * x)
    V[4] = y[5]
    V[5] = 0.004 * pi * y[3] - 0.006 * pi * y[5] + 0.4 * pi ** 2 * y[2] - 40.4 * pi ** 2 * y[4]


def rungeKutta():
    global X
    """
    INPUT:
    F: VECTOR FUNCTION SUBROUTINE
    X: INITIAL VARIABLE VALUE
    Y: INITIAL VECTOR(N)
    ND: MAXIMUM DIMENSION OF ARRAYS
    N: DIMENSION OF ARRAYS
    H: STEP SIZE

    OUTPUT:
    X = X + H
    Y: Approximate solution vector at x (N)  """
    Z1 = [0] * N
    YZ = [0] * N
    for i_ in range(N):
        Z1[i_] = H * V[i_]
        YZ[i_] = Y[i_] + Z1[i_] // 2
    XH = X + H / 2
    f(XH, YZ)

    Z2 = [0] * N
    for i_ in range(N):
        Z2[i_] = H * V[i_]
        YZ[i_] = Y[i_] + Z2[i_] // 2
    f(XH, YZ)

    Z3 = [0] * N
    for i_ in range(N):
        Z3[i_] = H * V[i_]
        YZ[i_] = Y[i_] + Z3[i_]
    X += H
    f(X, YZ)

    Z4 = [0] * N
    for i_ in range(N):
        Z4[i_] = H * V[i_]
        Y[i_] += (Z1[i_] + 2 * Z2[i_] + 2 * Z3[i_] + Z4[i_]) / 6

    return


R = [[num for num in Y]]
R[0].insert(0, X)
V = [0] * N

for i in range(1, M):
    rungeKutta()
    R.append([])
    R[i] = [num for num in Y]
    R[i].insert(0, X)
