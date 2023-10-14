"""
Created on Sat 23 May 11:34 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
import numpy as np

v = 1 * 10 ** (-3)
dx = 0.05
dt = dx
x = np.arange(0, 1 + dx, dx)
D = v / dx ** 2


def fwd_Euler_cds():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    plt.figure()
    plt.grid()
    plt.title('Forward Euler - Central Differencing Scheme')

    while max(u) >= 0.05:
        u_next = u[:]
        for i in range(1, len(x) - 1):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]

            aW = D
            aE = D
            aP = aW + aE
            aW2 = 0.25*dx
            aE2 = 0.25*dx

            f = -aP * uP + aW * uW + aE * uE + aW2*uW**2 - aE2*uE**2
            u_next[i] = uP + f * dt

        if ii % (1 / dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)

        u = u_next[:]
        ii += 1
    print('Forward Euler - CDS ', ii)


def fwd_Euler_lus():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    plt.figure()
    plt.grid()
    plt.title("Forward Euler - Linear Upwind Scheme")

    # for ii in range(8000):
    while max(u) >= 0.05:
        u_next = u[:]
        for i in range(2, len(x) - 2):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]
            uWW = u[i - 2]
            uEE = u[i + 2]

            if uP > 0:
                aEE = - v/(2*dx)
                aE = 2*v/dx
                aE2 = -1/dx
                aP2 = 1/dx
                aP = aEE - aE
                f = -aP * uP + aE * uE + aEE*uEE + aE2*uE**2 + aP2 * uP**2
            else:
                aW = -2*v/dx
                aWW = + v/(2*dx)
                aP = aWW - aW
                aP2 = -1/dx
                aW2 = +1/dx
                f = -aP * uP + aW * uW + aWW*uWW + aP2*uP**2 + aW2*uW**2

            u_next[i] = uP + f * dt

        if ii % (1 / dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)
        u = u_next[:]
        ii += 1
    print('Forward Euler - LUS ', ii)


fwd_Euler_cds()
# fwd_Euler_lus()
