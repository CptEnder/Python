"""
Created on Thu 23 Apr 23:15 2020
Finished on Fri 24 Apr 01:00 2020
@author: Παύλος Λοΐζου (nm16801)

v2: M*N grids
                                  """
import numpy as np
import matplotlib.pyplot as plt
import time

""" Txx + Tyy =0
    Txx(i,j) = (T(i+1,j) - 2T(i,j) + T(i-1,j))/dx**2
    Tyy(i,j) = (T(i,j+1) - 2T(i,j) + T(i,j-1))/dy**2
    => (T(i+1,j)+T(i-1,j))*dy**2 + (T(i,j+1)+T(i,j-1))**dx**2
    - (2*dx**2+2*dy**2)*T(i,j) = 0
    Tn = 0, Te = 7                                       """


def solve(nx: int, ny: int):
    global Tn, Te
    tic = time.time()
    x_ = np.linspace(0, 7, nx)
    y_ = np.linspace(0, 9, ny)
    dx2 = ((max(x_) - min(x_)) / (nx - 1)) ** 2
    dy2 = ((max(y_) - min(y_)) / (ny - 1)) ** 2

    """  -- System of equations A*t = f --  """
    # Creating f array
    f = [[0] for _ in range(nx * ny)]
    for i in range(ny):
        f[i * nx - 1] = [Te]
    # f[-1] = [(Tn + Te) / 2]
    # f[-nx:-1] = [[Tn] for _ in range(nx - 1)]
    dt = (f[-1][0] - Tn)/(nx-1)
    f[-nx:-1] = [[i] for i in np.linspace(Tn, f[-1][0] - dt, nx-1)]

    # Creating A array
    A = np.eye(nx * ny)
    for i in range(nx + 1, len(A) - nx - 1):
        A[i, i] = -2 * dx2 - 2 * dy2
        A[i, i - 1] = A[i, i + 1] = 1 * dy2
        A[i, i + nx] = A[i, i - nx] = 1 * dx2
    for i in range(1, ny):
        A[i * nx] = [0 for _ in range(len(A))]
        A[i * nx - 1] = [0 for _ in range(len(A))]
        A[i * nx, i * nx] = A[i * nx - 1, i * nx - 1] = 1
    for i in range(nx - 1):
        A[i, i + nx] = -1
    for i in range(1, ny - 1):
        A[i * nx, i * nx + 1] = -1

    print("Time spend creating the arrays: ", time.time() - tic)
    tic = time.time()
    t_ = np.linalg.solve(A, f)
    print("Time spend solving the problem: ", time.time() - tic)

    T = np.zeros([ny, nx])
    for k in range(ny):
        T[k] = np.take(t_, [i for i in range(k * nx, k * nx + nx)])
    return x_, y_, T


def draw(x_, y_, t_):
    global Tn, Te
    plt.figure()
    c_map = plt.cm.get_cmap("plasma")
    levels = np.linspace(Tn, Te, (Te - Tn) * 2 ** (it + 1) + 1)
    plt.contourf(x_, y_, t_, levels=levels, cmap=c_map)
    m = plt.cm.ScalarMappable(cmap=c_map)
    m.set_clim(Tn, Te)
    bound = np.linspace(Tn, Te, Te - Tn + 1)
    plt.colorbar(m, boundaries=bound)
    plt.contour(x_, y_, t_, levels=bound, colors='k', linewidths=0.6, alpha=0.8)
    plt.title("Grid : (" + str(x_.size) + "*" + str(y_.size) + ")")


T_list = []
error_lst = []
errors = [[], [], []]

"""   -- INPUTS --   """
Nx = 4   # Number of nodes on X axis
Ny = 5   # Number of nodes on Y axis
Tn = 0   # Temperature of the North side
Te = 7   # Temperature of the East side

for it in range(5):
    x, y, t = solve(Nx, Ny)
    T_list.append(t)
    error_lst.append([])
    errors[0].append(Nx * Ny)
    errors[2].append([Nx, Ny])
    draw(x, y, t)
    Nx = 2 * Nx - 1
    Ny = 2 * Ny - 1

# Reference Temperature map
it += 1
x, y, reference_T = solve(Nx, Ny)
T_list.append(reference_T)
draw(x, y, reference_T)

""" -- Calculating the error -- """
# Subtracting all available temperature maps from the reference one

ln = len(error_lst)
for it in range(reference_T.shape[0]):
    for ii in range(1, ln + 1):
        if it % (2 ** ii) == 0:
            for it2 in range(reference_T.shape[1]):
                if it2 % (2 ** ii) == 0:
                    error = reference_T[it][it2] - T_list[ln - ii][int(it / (2 ** ii))][int(it2 / (2 ** ii))]
                    error_lst[ii - 1].append(abs(error))

# Calculating the average error for each temperature map

for it, e in enumerate(error_lst):
    errors[1].append(sum(e) / len(e))

errors[1].reverse()

plt.figure()
plt.plot(errors[0], errors[1], '.-')
for _ in range(len(errors[0])):
    plt.annotate("(" + str(errors[2][_][0]) + "*" + str(errors[2][_][1]) + ")", xy=(errors[0][_], errors[1][_]))
plt.ylim(bottom=0)
plt.title("Mean error diagram. Reference Grid : (" + str(Nx) + "*" + str(Ny) + ")")
plt.xlabel("Nx * Ny")
plt.ylabel("Mean error")
plt.grid()
plt.show()
