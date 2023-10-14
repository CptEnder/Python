"""
Created on Sat 23 May 11:34 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
import numpy as np

r = 3
v = 1 * 10 ** (-r)
dx = 0.02
dt = 0.01
x = np.arange(0, 1 + dx, dx)
D = v / dx**2
T = 100


# ----------------------------------- #
#            Forward Euler            #
# ----------------------------------- #
def fwd_Euler_cds():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    plt.figure()
    plt.grid()
    plt.title(f'Forward Euler - Central Differencing Scheme \n (v={v})')

    while max(max(u), abs(min(u))) >= 0.05 and ii*dt < T:
        u_next = u[:]
        for i in range(1, len(x) - 1):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]

            Fe = (uP + uE) / 2
            Fw = (uP + uW) / 2

            aW = D + Fw / 2
            aE = D - Fe / 2
            aP = aW + aE + Fe - Fw

            f = -aP * uP + aW * uW + aE * uE
            u_next[i] = uP + f * dt

        if ii % (10 / dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)

        u = u_next[:]
        ii += 1
    print('Forward Euler - CDS ', ii)
    return u


def fwd_Euler_lus():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    plt.figure()
    plt.grid()
    plt.title(f"Forward Euler - Linear Upwind Scheme\n (v={v})")

    while max(max(u), abs(min(u))) >= 0.05 and ii*dt < T:
        u_next = u[:]
        for i in range(1, len(x) - 1):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]

            if uP > 0:
                Fw = uW
                Fe = uP
            else:
                Fw = uP
                Fe = uE

            aE = D + max(-Fe, 0)
            aW = D + max(Fw, 0)
            aP = aW + aE + Fe - Fw

            f = -aP * uP + aW * uW + aE * uE
            u_next[i] = uP + f * dt

        if ii % (5 / dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)
        u = u_next[:]
        ii += 1
    print('Forward Euler - LUS ', ii)
    return u


# ----------------------------------- #
#           Adams-Bashforth           #
# ----------------------------------- #
def Adam_cds():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    B = [[0] * int(1 / dx + 1)]
    plt.figure()
    plt.grid()
    plt.title(f'Adams-Bashforth Central Differencing Scheme\n (v={v})')

    while max(max(u), abs(min(u))) >= 0.05 and ii*dt < T:
        u_next = u[:]
        B.append([])
        for i in range(1, len(x) - 1):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]

            Fe = (uP + uE) / 2
            Fw = (uP + uW) / 2

            aW = D + Fw / 2
            aE = D - Fe / 2
            aP = aW + aE + Fe - Fw

            f = -aP * uP + aW * uW + aE * uE
            B[ii + 1].append(f)

            u_next[i] = uP + dt / 2 * (3 * f - B[ii][i - 1])

        if ii % (5 / dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)
        u = u_next[:]
        ii += 1
    print('Adams-Bashforth CDS ', ii)
    return u


# ---------------------------------- #
#           Backward Euler           #
# ---------------------------------- #
def bwd_Euler_cds():
    u = [i for i in np.sin(2 * np.pi * x)]
    u[-1] = u[0] = 0
    ii = 0
    plt.figure()
    plt.grid()
    plt.title(f'Backward Euler - Central Differencing Scheme\n (v={v})')
    A = np.identity(len(x))

    while max(max(u), abs(min(u))) >= 0.05 and ii*dt < T:
        for i in range(1, len(x)-1):
            uP = u[i]
            uW = u[i - 1]
            uE = u[i + 1]

            Fe = (uP + uE) / 2
            Fw = (uP + uW) / 2

            aE = D - Fe / 2
            aW = D + Fw / 2
            aP = aW + aE

            A[i, i] = aP*dt + 1
            A[i, i + 1] = -aE * dt
            A[i, i - 1] = -aW * dt

        if ii % (5/dt) == 0:
            plt.plot(x, u)
            plt.pause(1 / 60)
        u = np.linalg.solve(A, u)
        ii += 1
    print('Implicit Euler CDS ', ii)
    return u


def bwd_Euler_cds1():
    u = [[i for i in np.sin(2 * np.pi * x)], []]
    u[0][-1] = u[0][0] = 0
    u[1] = u[0][:]
    u_imp = [0 for _ in range(len(u[0]))]
    ii = 0
    plt.figure()
    plt.grid()
    plt.title(f"Backward Euler - Central Differencing Scheme\n (v={v})")

    while max(max(u[-1]), abs(min(u[-1]))) >= 0.05 and ii*dt < T:
        u_next = u[-1][:]
        for i in range(1, len(u[0]) - 1):
            uP = u_next[i]
            uE = u_next[i + 1]
            uW = u_next[i - 1]
            Fe = (uE + uP) / 2
            Fw = (uW + uP) / 2
            aW = D + Fw / 2
            aE = D - Fe / 2
            aP = aE + aW + Fe - Fw
            f = -aP * uP + aW * uW + aE * uE
            u_next[i] = uP + dt * f
        u[1] = u_next[:]

        for i in range(1, len(u[0])-1):
            uiP = u[-1][i]
            uiE = u[-1][i + 1]
            uiW = u[-1][i - 1]
            Fie = (uiE + uiP) / 2
            Fiw = (uiW + uiP) / 2
            aiW = D + Fiw / 2
            aiE = D - Fie / 2
            aiP = aiE + aiW + Fie - Fiw
            fi = -aiP * uiP + aiW * uiW + aiE * uiE
            u_imp[i] = u[-2][i] + dt * fi

        if ii % (5/dt) == 0:
            plt.plot(x[::10], u[-1][::10], 'b.')
            plt.plot(x, u_imp)
            plt.pause(1/60)
        u[0] = u_next[:]
        ii += 1
    print('Backwards Euler - CDS', ii)
    return u[-1]


def bwd_Euler_lus():
    u = [[i for i in np.sin(2 * np.pi * x)], []]
    u[0][-1] = u[0][0] = 0
    u[1] = u[0][:]
    u_imp = [0 for _ in range(len(u[0]))]
    ii = 0
    plt.figure()
    plt.grid()
    plt.title(f"Backward Euler - Linear Upwind Scheme\n (v={v})")

    while max(max(u[-1]), abs(min(u[-1]))) >= 0.05 and ii*dt < T:
        u_next = u[-1][:]
        for i in range(1, len(x) - 1):
            uP = u_next[i]
            uE = u_next[i + 1]
            uW = u_next[i - 1]

            if uP > 0:
                Fw = uW
                Fe = uP
            else:
                Fw = uP
                Fe = uE

            aE = D + max(-Fe, 0)
            aW = D + max(Fw, 0)
            aP = aW + aE + Fe - Fw
            f = -aP * uP + aW * uW + aE * uE
            u_next[i] = uP + f * dt
        u[1] = u_next[:]

        for i in range(1, len(u[0])-1):
            uiP = u[-1][i]
            uiE = u[-1][i + 1]
            uiW = u[-1][i - 1]

            if uiP > 0:
                Fiw = uiW
                Fie = uiP
            else:
                Fiw = uiP
                Fie = uiE

            aiE = D + max(-Fie, 0)
            aiW = D + max(Fiw, 0)
            aiP = aiW + aiE + Fie - Fiw
            fi = -aiP * uiP + aiW * uiW + aiE * uiE
            u_imp[i] = u[-2][i] + dt * fi

        if ii % (5/dt) == 0:
            plt.plot(x[::10], u[-1][::10], 'b.')
            plt.plot(x, u_imp)
            plt.pause(1 / 60)
        # print(np.array(u[1]) - np.array(u_imp))
        u[0] = u_next[:]
        # u[1] = u_imp[:]
        ii += 1
    print('Backwards Euler - LUS', ii)
    return u[-1]


# ufc = fwd_Euler_cds()
# ufu = fwd_Euler_lus()
# ufa = Adam_cds()
ubc = bwd_Euler_cds()
ubc1 = bwd_Euler_cds1()
# ubu = bwd_Euler_lus()
