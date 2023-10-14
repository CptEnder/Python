"""
Created on Tue 31 Mar 05:13 2020
Finished on Tue 31 Mar 06:00 2020
@author: Παύλος Λοΐζου (nm16801)
                                  """
import si_maths as mth
import matplotlib.pyplot as plt
import time

''' Txx + Tyy =0
    Txx(i,j) = (T(i+1,j) - 2T(i,j) + T(i-1,j))/dx**2
    Tyy(i,j) = (T(i,j+1) - 2T(i,j) + T(i,j-1))/dy**2
    => T(i+1,j)+T(i,j+1)+T(i-1,j)+T(i,j-1) - 4T(i,j) = 0
    Tn = 0, Te = 7                                      '''


def solve(n):
    tic = time.time()
    Nx = n
    Ny = Nx
    x = mth.linspace(0, 7, Nx)
    y = mth.linspace(0, 9, Ny)

    # System of equations A*t = f
    # Creating f array
    f = mth.matrices.zeros(len(x)*len(y), 1)
    for i in range(len(y)):
        f[i*len(x)-1] = [7]
    # Creating A array
    A = mth.matrices.I(len(x)*len(y))
    for i in range(len(x)+1, len(A)-len(x)-1):
        A[i][i] = -4
        A[i][i-1] = A[i][i+1] = 1
        A[i][i+len(x)] = A[i][i-len(x)] = 1
    for i in range(len(y)):
        A[i*len(x)] = [0*ii for ii in range(len(A))]
        A[i*len(x)-1] = [0*ii for ii in range(len(A))]
        A[i][i] = A[i*len(x)][i*len(x)] = A[i*len(x)-1][i*len(x)-1] = A[-1-i][-i-1] = 1
    for i in range(len(x)-1):
        A[i][i+len(x)] = -1
    for i in range(1, len(y)-1):
        A[i*len(x)][i*len(x) + 1] = -1

    print("Time spend creating the arrays: ", time.time() - tic)
    tic = time.time()
    t = mth.linAlg.gesgae(A, f)
    print("Time spend solving the problem: ", time.time() - tic)
    return x, y, t


def draw(x, y, t):
    T = []
    for k in range(len(x)):
        T.append(t[k*len(x): k*len(x)+len(x)])

    levels = mth.linspace(min(t), max(t), 7)
    fig, ax = plt.subplots(nrows=1)
    cMap = plt.cm.get_cmap("plasma")
    colorGraph = ax.contourf(x, y, T,  levels=levels, cmap=cMap)
    ax.contour(x, y, T, levels=levels, colors='k', linewidths=0.6, alpha=0.7)
    cbar = fig.colorbar(colorGraph)


for N in [10]:
    x_, y_, t_ = solve(N)
    draw(x_, y_, t_)
