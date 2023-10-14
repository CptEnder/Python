"""
Created on Wed 06 May 19:25 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import numpy as np
import matplotlib.pyplot as plt

v = 1 * 10**(-3)
N = 51
dx = 1/(N-1)
dt = 0.01
x = np.linspace(0, 1, N)


# Central Differencing Scheme O(Dx**2)
def fwd_e_cds():
    plt.figure()
    plt.grid()
    plt.title('Forward Euler - Central Differencing Scheme')
    i = 0
    u = [i for i in np.sin(2 * np.pi * x)]
    u[0] = 0
    u[-1] = 0
    u_next = u[:]
    while 150 > max(max(u), abs(min(u))) > 0.05:
        D = v / dx
        for ii in range(1, N - 1):
            uP = u[ii]
            uE = u[ii + 1]
            uW = u[ii - 1]
            Fe = (uE + uP) / 2
            Fw = (uW + uP) / 2
            aW = D + Fw / 2
            aE = D - Fe / 2
            aP = aE + aW + Fe - Fw
            f = - aP * uP + aW * uW + aE * uE
            u_next[ii] = uP + f * dt
        u = u_next[:]
        if i % (5/dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 100)
        i += 1

    print('Forward Euler - CDS ', i)
    return u


def bwd_e_cds():
    plt.figure()
    plt.grid()
    plt.title('Backward Euler - Central Differencing Scheme')
    i = 0
    u = [[i for i in np.sin(2 * np.pi * x)]]
    u_next = u[0][:]
    uimp = [0 for _ in range(N)]
    while 15 > max(max(u[-1]), abs(min(u[-1]))) > 0.05:
    # for i in range(500):
        D = v / dx
        for ii in range(1, N - 1):
            uP = u_next[ii]
            uE = u_next[ii + 1]
            uW = u_next[ii - 1]
            Fe = (uE + uP) / 2
            Fw = (uW + uP) / 2
            aW = D + Fw / 2
            aE = D - Fe / 2
            aP = aE + aW + Fe - Fw
            f = -aP * uP + aW * uW + aE * uE
            u_next[ii] = uP + dt * f
        u.append(u_next[:])

        for ii in range(1, N-1):
            uiP = u[-1][ii]
            uiE = u[-1][ii + 1]
            uiW = u[-1][ii - 1]
            Fie = (uiE + uiP) / 2
            Fiw = (uiW + uiP) / 2
            aiW = D + Fiw / 2
            aiE = D - Fie / 2
            aiP = aiE + aiW + Fie - Fiw
            fi = -aiP * uiP + aiW * uiW + aiE * uiE
            uimp[ii] = u[-2][ii] + dt * fi

        if i % 1000 == 0:
            plt.plot(x, u[-1], 'b')
            plt.plot(x, uimp, 'r.')
            plt.pause(1/60)

        i += 1
    print(i)
    return u


uc = fwd_e_cds()
ub = bwd_e_cds()
