import numpy as np
from matplotlib import pyplot as plt

# _________________________centre scheme__________________________________
# _________________________explicit forward_______________________________
xL = 1
dx = 0.05
dt = 0.05
N = int(xL / dx + 1)
N = 26
dx = 1/(N-1)
u = np.zeros((N, 1))
v = 1 * 10 ** (-3)

x = 0
for i in range(1, N - 1, 1):
    x = x + dx
    u[i][0] = np.sin(2 * np.pi * x)

x = np.linspace(0, xL, N)
u = np.sin(2*np.pi*x)
u[0] = 0
u[-1] = 0
plt.grid()
plt.plot(x, u, 'k-')

for t in np.arange(0, 200, dt):

    for i in range(1, N - 1, 1):
        up = u[i]
        ue = u[i + 1]
        uw = u[i - 1]

        Fe = (ue + up) / 2
        Fw = (uw + up) / 2
        D = v / dx

        ap = (D + Fw / 2) + (D - Fe / 2) + (Fe - Fw)
        aw = (D + Fw / 2)
        ae = (D - Fe / 2)

        u[i] = u[i] + (-ap * up + aw * uw + ae * ue) * dt
    if t % 2 == 0:
        plt.plot(x, u)
        # plt.plot(x,u,'r.')
        plt.pause(1 / 60)
