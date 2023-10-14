"""
Created on Sat 14 Mar 18:55 2020
Finished on
@author: Cpt.Ender
                                  """
import si_maths as mth
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# import numpy as np

Nx = 10
Ny = Nx
dx = 1/(Nx-1)
dy = 1/(Ny-1)
x = mth.frange(0, 1, dx)
y = mth.frange(0, 1, dy)
grid = []
f = []
'''
Uxx + Uyy = f(x,y) = 10^3(x^2 + y^2)
Uxx(i,j) = (U(i+1,j) - 2U(i,j) + U(i-1,j))/dx**2
Uyy(i,j) = (U(i,j+1) - 2U(i,j) + U(i,j-1))/dy**2
=> U(i+1,j)+U(i,j+1)+U(i-1,j)+U(i,j-1) - 4U(i,j) = (dx*dy)**2*f(x,y)
U(borders) = 0
'''

for i in range(len(x)):
    grid.append([])
    for j in range(len(y)):
        grid[i].append([x[i], y[j]])
        f.append(-(dx*dy)**2*10**3*(x[i]**2 + y[j]**2))
        # Axes3D.plot(ax, [x[i]], [y[j]], 1, '.')

# System of equations A*u = f
# Creating f array
for i in range(len(y)):
    f[i] = f[i*len(x)] = f[i*len(x)-1] = f[-1-i] = 0
# Creating A array
A = mth.mat.zeros(len(x)*len(y), len(y)*len(x))
for i in range(len(x) + 1, len(A) - len(x)-1):
    A[i][i] = -4
    A[i][i-1] = A[i][i+1] = 1
    A[i][i+len(x)] = A[i][i-len(x)] = 1
for i in range(len(y)):
    A[i*len(x)] = [0 for ii in range(len(A))]
    A[i*len(x)-1] = [0 for ii in range(len(A))]
    A[i][i] = A[i*len(x)][i*len(x)] = A[i*len(x)-1][i*len(x)-1] = A[-1-i][-i-1] = 1

u = mth.linalg.dias(A, f, 2*len(y)+1)
# u = np.linalg.solve(A, f)
# count = 0
# for i in range(len(x)):
#     for j in range(len(y)):
#         Axes3D.scatter(ax, x[i], y[j], u[count])
#         count += 1

X = []
Y = []
U = []
for i in range(len(x)):
    X.append(x)
for j in range(len(y)):
    Y.append([y[j] for i in range(len(x))])
for k in range(len(x)):
    U.append(u[k*len(x):k*len(x)+len(x)])

X1 = mth.mat.transpose(X)
Y1 = mth.mat.transpose(Y)
U1 = mth.mat.transpose(U)
# for i in range(len(x)):
#     X1.append([x[i] for j in range(len(y))])
# for j in range(len(y)):
#     Y1.append(y)
# for k in range(len(x)):
#     U1.append(u[k*len(x):k*len(x)+5])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(y)):
    ax.plot3D(X[i], Y[i], U[i])
    ax.plot3D(X1[i], Y1[i], U1[i])
# ax.scatter(X, Y, U)
