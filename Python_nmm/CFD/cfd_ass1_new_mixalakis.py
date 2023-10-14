import numpy as np
import matplotlib.pyplot as plt
import time

Nx = 15
Ny = 15
N = Nx * Ny

yt1 = 1.5  # yt1: y-coordinate of the 1st vortex
yt2 = -1.5  # yt2: y-coordinate of the 2nd vortex
xt1 = 0  # xt1: x-coordinate of the 1st vortex
xt2 = 0  # xt2: x-coordinate of the 2nd vortex

x = np.linspace(-5, 5, Nx)
y = np.linspace(-5, 5, Ny)

vA = 1.5 * 10 ** (-5)  # Viscosity

Grid = []
for i in range(Nx):
    Grid.append([])
    for ii in range(Ny):
        Grid[i].append([x[i], y[ii]])

boundaryPoints = []
insidePoints = []
for i in range(Nx):
    for ii in range(Ny):
        if i == 0 or i == Nx - 1 or ii == 0 or ii == Ny - 1:
            boundaryPoints.append(Grid[i][ii])
        else:
            insidePoints.append(Grid[i][ii])

# Creating the A matrix
A = np.diag(np.full(N, 1))

for i in range(N):
    if i % Nx == 0 and i not in [N - Nx, 0]:
        for ii in range(i + 1, i + Nx - 1):
            A[ii][ii] = -4
            A[ii][ii + 1] = 1
            A[ii][ii - 1] = 1
            A[ii][ii + Nx] = 1
            A[ii][ii - Nx] = 1

dx = abs(x[-1] - x[0]) / (Nx - 1)
dy = abs(y[-1] - y[0]) / (Ny - 1)


def distance(xt, yt, xn, yn):  # (xt,yt): turbine center, (xn,yn): node center
    dist = np.sqrt((xn - xt) ** 2 + (yn - yt) ** 2)  # r = sqrt( (x-xo)**2  + (y-yo)**2 )
    return dist


# Creating the b matrix
def calculatingB(w_values_):
    b = np.ones(N)

    yb = []
    for point in boundaryPoints:
        sum_ = 0
        for i_, in_point in enumerate(insidePoints):
            index = (i_ // (Nx - 2) + 1) * Nx + (i_ % (Nx - 2) + 1)
            sum_ += -(dx * dy / (2 * np.pi) * w_values_[index]) * \
                np.log(distance(point[0], point[1], in_point[0], in_point[1]))
        yb.append(sum_)

    # North and South boundaries
    b[0:Nx] = yb[0:Nx]
    b[-Nx:-1] = yb[-Nx:-1]
    b[-1] = yb[-1]

    # East and West boundaries
    counter = 0
    for i_ in range(N):
        if i_ % Nx == 0 and i_ not in [N - Nx, 0]:

            for ii_ in range(i_ + 1, i_ + Nx - 1):
                b[ii_] = -dx ** 2 * w_values_[ii_]

            # boundary conditions
            b[i_] = yb[Nx + counter * 2]
            b[i_ + Nx - 1] = yb[Nx + counter * 2 + 1]
            counter += 1

    return b


# Starting W values
w_values = []
Psi = []

for y_ in y:
    for x_ in x:
        r1 = distance(xt1, yt1, x_, y_)  # r1: distance between node(i,j) and center of turbine 1
        r2 = distance(xt2, yt2, x_, y_)  # r2: distance between node(i,j) and center of turbine 2

        w1 = (2 - r1 ** 2) * np.exp((1 - r1 ** 2) / 2)  # ω1: turbulence equation for turbine number 1 (+)
        w2 = -(2 - r2 ** 2) * np.exp((1 - r2 ** 2) / 2)  # ω2: turbulence equation for turbine number 2 (-)
        w = w1 + w2  # The Principle of Superimposition applies so we add algebraically the two equations

        psi1 = np.exp((1-r1**2)/2)
        psi2 = -np.exp((1-r2**2)/2)
        psi = psi1+psi2
        Psi.append(psi)

        w_values.append(w)

Psi = np.array(Psi)

# Loop for time steps
dt = 0.1

B = calculatingB(w_values)
X = np.linalg.solve(A, B)

# print(np.mean(abs(X)-abs(Psi)))
# Psi = np.reshape(Psi, newshape=(Nx, Ny))
# plt.contourf(x, y, Psi)
# plt.colorbar()


W_values = np.reshape(w_values, newshape=(Nx, Ny))  # we reshape array w_values from [1xNx*Ny] into [Nx*Ny]
X = np.reshape(X, newshape=(Nx, Ny))


# Calculating the velocity
U = []
for i in range(Nx):
    for ii in range(Ny):
        if 0 < i < Nx - 1 and 0 < ii < Ny - 1:
            u = (X[i][ii + 1] - X[i][ii - 1]) / (2 * dy)
            v = -(X[i + 1][ii] - X[i - 1][ii]) / (2 * dx)

            if u != 0:
                tanf = v/u
            else:
                tanf = v/1*10**(-6)
            f = np.arctan(tanf)
            if -np.pi/2 <= f < np.pi/2:
                sign = +1
            else:
                sign = -1

            U.append(sign*np.sqrt(u ** 2 + v ** 2))

U = np.reshape(U, newshape=(Nx-2, Ny-2))
x1 = x[1:-1]
y1 = y[1:-1]
plt.figure()
# plt.contourf(x, y, X)
plt.contourf(x1, y1, U)
plt.colorbar()
plt.show()


for t in np.arange(0, 15, dt):

    B = calculatingB(w_values)
    X = np.linalg.solve(A, B)

    W_values = np.reshape(w_values, newshape=(Nx, Ny))  # we reshape array w_values from [1xNx*Ny] into [Nx*Ny]
    X = np.reshape(X, newshape=(Nx, Ny))

    if (t * 10) % 2 == 0:
        # plt.contourf(x, y, X)
        plt.contourf(x1, y1, U)
        plt.show()
        plt.pause(1 / 600)

    # Calculate new W values
    w_next = []
    for i in range(Nx):
        w_next.append(np.zeros(Ny))
        for ii in range(Ny):
            if 0 < i < Nx - 1 and 0 < ii < Ny - 1:
                u = (X[i][ii + 1] - X[i][ii - 1]) / (2 * dy)
                v = -(X[i + 1][ii] - X[i - 1][ii]) / (2 * dx)

                tanf = u/v
                f = np.arctan(tanf)
                if -np.pi/2 <= f < np.pi/2:
                    sign = +1
                else:
                    sign = -1

                U[i-1][ii-1] = sign*np.sqrt(u**2+v**2)

                temp = u * (W_values[i + 1][ii] - W_values[i - 1][ii]) / (2 * dx) + \
                       v * (W_values[i][ii + 1] - W_values[i][ii - 1]) / (2 * dy)
                temp2 = -vA / dx ** 2 * (W_values[i][ii + 1] + W_values[i][ii - 1] +
                                         W_values[i + 1][ii] + W_values[i - 1][ii] - 4 * W_values[i][ii])
                w_next[i][ii] = W_values[i][ii] - dt * (temp + temp2)

    w_values = np.reshape(w_next, newshape=N)
