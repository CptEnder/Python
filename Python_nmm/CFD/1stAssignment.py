"""
Created on Sun 29 Mar 16:15 2020
Finished on Mon 30 Mar 04:00 2020
@author: Παύλος Λοΐζου (nm16801)

v1: N*N grids
                                  """
import numpy as np
import matplotlib.pyplot as plt
import time

''' Txx + Tyy =0
    Txx(i,j) = (T(i+1,j) - 2T(i,j) + T(i-1,j))/dx**2
    Tyy(i,j) = (T(i,j+1) - 2T(i,j) + T(i,j-1))/dy**2
    => T(i+1,j)+T(i,j+1)+T(i-1,j)+T(i,j-1) - 4T(i,j) = 0
    Tn = 0, Te = 7                                       '''


def solve(n: int):
    global Tn, Te
    tic = time.time()
    x_ = np.linspace(0, 7, n)
    y_ = np.linspace(0, 9, n)

    # System of equations A*t = f
    # Creating f array
    f = [[0] for _ in range(n * n)]
    for i in range(n):
        f[i * n - 1] = [Te]
    f[-1] = [(Tn + Te)/2]
    f[-n:-1] = [[Tn] for _ in range(n-1)]
    # dt = (f[-1][0] - Tn)/(nx-1)
    # f[-nx:-1] = [[i] for i in np.linspace(Tn, f[-1][0] - dt, nx-1)]
    # Creating A array
    A = np.eye(n * n)
    for i in range(n + 1, len(A) - n - 1):
        A[i, i] = -4
        A[i, i - 1] = A[i, i + 1] = 1
        A[i, i + n] = A[i, i - n] = 1
    for i in range(n):
        A[i * n] = [0 for _ in range(len(A))]
        A[i * n - 1] = [0 for _ in range(len(A))]
        A[i, i] = A[i * n, i * n] = A[i * n - 1, i * n - 1] = A[-1 - i, -i - 1] = 1
    for i in range(n - 1):
        A[i, i + n] = -1
    for i in range(1, n - 1):
        A[i * n, i * n + 1] = -1

    print("Time spend creating the arrays: ", time.time() - tic)
    tic = time.time()
    t_ = np.linalg.solve(A, f)
    print("Time spend solving the problem: ", time.time() - tic)

    T = np.zeros([n, n])
    for k in range(n):
        T[k] = np.take(t_, [i for i in range(k * n, k * n + n)])
    return x_, y_, T


def draw(x_, y_, t_):
    global Tn, Te
    plt.figure()
    c_map = plt.cm.get_cmap("plasma")
    levels = np.linspace(t_.min(), t_.max(), x_.size)
    plt.contourf(x_, y_, t_, levels=levels, cmap=c_map)
    m = plt.cm.ScalarMappable(cmap=c_map)
    m.set_clim(Tn, Te)
    plt.colorbar(m, boundaries=np.linspace(Tn, Te, 8))
    plt.contour(x_, y_, t_, colors='k', linewidths=0.6, alpha=0.8)
    plt.title("N = "+str(x_.size))


T_list = []
error_lst = []
N = 8
Tn = 0
Te = 7
for it in range(3):
    x, y, t = solve(N)
    T_list.append(t)
    error_lst.append([])
    draw(x, y, t)
    N = 2*N - 1

# Reference Temperature map
x, y, reference_T = solve(N)
T_list.append(reference_T)
draw(x, y, reference_T)

''' Calculating the error '''
# Subtracting all available temperature maps from the reference one

ln = len(error_lst)
for it in range(len(reference_T)):
    for ii in range(1, ln+1):
        if it % (2**ii) == 0:
            for it2 in range(len(reference_T)):
                if it2 % (2**ii) == 0:
                    error = reference_T[it][it2] - T_list[ln-ii][int(it/(2**ii))][int(it2/(2**ii))]
                    error_lst[ii-1].append(abs(error))

# Calculating the average error for each temperature map
errors = [[], []]
plt.figure()
for it, e in enumerate(error_lst):
    errors[0].append(sum(e)/len(e))
    errors[1].append(len(e)**0.5)

plt.plot(errors[1], errors[0], '.-')
plt.ylim(bottom=0)
plt.title("Mean error diagram. Reference N = "+str(N))
plt.xlabel("N")
plt.ylabel("Mean error")
plt.grid()
plt.show()
