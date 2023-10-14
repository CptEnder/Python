"""
Created on Tue 05 May 11:25 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)

Explicit - Forward Euler
                                  """
import numpy as np
import matplotlib.pyplot as plt

v = 1 * 10**(-4)
# v = 0
N = 21
dt = 0.05
dx = 1/(N-1)
x = np.linspace(0, 1, N)

# ----------------------------------- #
#            Forward Euler            #
# ----------------------------------- #


# Linear Upwind Scheme O(Dx)
def fwd_e_lus():
    plt.figure()
    plt.grid()
    plt.title("Forward Euler - LUS Scheme")
    i = 0
    u = [i for i in np.sin(2 * np.pi * x)]
    u[0] = 0
    u[-1] = 0
    while 15 > max(max(u), abs(min(u))) > 0.05:
        D = v/dx
        # u_next = [0, 0]
        for ii in range(1, len(x)-1):
            uP = u[ii]
            uE = u[ii+1]
            uW = u[ii-1]
            if uP > 0:
                Fw = uW
                Fe = uP
            else:
                Fw = uP
                Fe = uE
            aE = D + max(-Fe, 0)
            aW = D + max(Fw, 0)
            aP = aE + aW + Fe - Fw
            f = -aP*uP + aW*uW + aE*uE
            u[ii] = uP + dt*f
        #     u_next.insert(ii, f)
        # u = u_next
        if i % (5*1/dt) == 0:
            plt.plot(x, u)
            plt.pause(1/60)
        i += 1
    print('Forward Euler - LUS ', i)
    return u


# Central Differencing Scheme O(Dx**2)
def func(u):
    D = v/dx
    f = [0]
    for ii in range(1, N-1):
        uP = u[ii]
        uE = u[ii+1]
        uW = u[ii-1]
        Fe = (uE + uP) / 2
        Fw = (uW + uP) / 2
        aW = D + Fw/2
        aE = D - Fe/2
        aP = aE + aW + Fe - Fw
        f.append(- aP*uP + aW*uW + aE*uE)
        u[ii] = uP + f[ii]*dt/dx
    return u, f


def fwd_e_cds(n_dt: int = 0):
    plt.figure()
    plt.grid()
    plt.title('Forward Euler - Central Differencing Scheme')
    i = 0
    u = [i for i in np.sin(2 * np.pi * x)]
    u[0] = 0
    u[-1] = 0
    if n_dt == 0:
        while 150 > max(max(u), abs(min(u))) > 0.05:
            u, _ = func(u)
            if i % (5) == 0:
                plt.plot(x, u)
                plt.pause(1 / 100)
            i += 1
    else:
        for i in range(0, n_dt):
            u, _ = func(u)
            plt.plot(x, u)
            plt.pause(1 / 60)
    print('Forward Euler - CDS ', i)
    return u


# Quadratic Upstream Interpolation for Convective Kinematics O(Dx**3)
def fwd_e_quick():
    plt.figure()
    plt.grid()
    plt.title("Forward Euler - QUICK Scheme")
    i = 0
    u = np.sin(2 * np.pi * x)
    u[0] = 0
    u[-1] = 0
    while 10 > max(max(u), abs(min(u))) > 0.05:
        D = v/dx
        u[1] = u[2]/2
        u[-2] = u[-3]/2
        # u_next = [0, u[1], u[-2], 0]
        for ii in range(2, len(x)-2):
            uP = u[ii]
            uE = u[ii+1]
            uW = u[ii-1]
            uWW = u[ii-2]
            uEE = u[ii+2]
            if uP > 0:
                Fe = 6/8*uP + 3/8*uE - 1/8*uW
                Fw = 6/8*uW + 3/8*uP - 1/8*uWW
                k = 1
            else:
                Fe = 6/8*uE + 3/8*uP - 1/8*uEE
                Fw = 6/8*uP + 3/8*uW - 1/8*uE
                k = 0
            aW = D + 6/8*k*Fw + 1/8*k*Fe + 3/8*(1-k)*Fw
            aE = D - 3/8*k*Fe - 6/8*(1-k)*Fe - 1/8*(1-k)*Fw
            aWW = -1/8*k*Fw
            aEE = 1/8*(1-k)*Fe
            aP = aE + aW + aWW + aEE + Fe - Fw
            f = aP*uP - aW*uW - aE*uE - aWW*uWW - aEE*uEE
            u[ii] = uP - dt*f
        #     u_next.insert(ii, f)
        # u.append(u_next)
        if i % (2/dt) == 0:
            plt.plot(x, u)
            plt.pause(1/60)
        i += 1
    print('Forward Euler - QUICK ', i)
    return u

# ----------------------------------- #
#           Adams-Bashforth           #
# ----------------------------------- #


# Linear Upwind Scheme O(Dx)
def as_ba_lus():
    plt.figure()
    plt.grid()
    plt.title("Adams-Bashforth LUS Scheme")
    i = 1
    u = [np.sin(2 * np.pi * x)]
    u[0][0] = 0
    u[0][-1] = 0
    u1, f_previous = func(u[0])
    u.append(u1)
    while 10 > max(max(u[-1]), abs(min(u[-1]))) > 0.05:
        D = v/dx
        # u_next = [0, 0]
        u[0] = u[-1][:]
        for ii in range(1, len(x)-1):
            uP = u[-1][ii]
            uE = u[-1][ii + 1]
            uW = u[-1][ii - 1]
            if uP > 0:
                Fw = uW
                Fe = uP
            else:
                Fw = uP
                Fe = uE
            aE = D + max(-Fe, 0)
            aW = D + max(Fw, 0)
            aP = aE + aW + Fe - Fw
            f = - aP*uP + aW*uW + aE*uE
            u[-1][ii] = uP + (3 * f - f_previous[ii]) * dt / 2
            f_previous[ii] = f
        #     u_next.insert(ii, f)
        # u = u_next
        if i % 80 == 0:
            plt.plot(x, u[-1])
            plt.pause(1/60)
        i += 1
    print('Adams-Bashforth LUS ', i)
    return u


# Central Differencing Scheme O(Dx**2)
def as_ba_cds():
    plt.figure()
    plt.grid()
    plt.title('Adams-Bashforth Central Differencing Scheme')
    i = 1
    u = [np.sin(2 * np.pi * x)]
    u[0][0] = 0
    u[0][-1] = 0
    u1, f_previous = func(u[0])
    u.append(u1)
    while 15 > max(max(u[-1]), abs(min(u[-1]))) > 0.05:
        D = v/dx
        u[0] = u[-1][:]
        for ii in range(1, N-1):
            uP = u[-1][ii]
            uE = u[-1][ii+1]
            uW = u[-1][ii-1]
            Fe = (uE + uP) / 2
            Fw = (uW + uP) / 2
            aW = D + Fw/2
            aE = D - Fe/2
            aP = aE + aW + Fe - Fw
            f = - aP*uP + aW*uW + aE*uE
            u[-1][ii] = uP + (3*f - f_previous[ii])*dt/2
            f_previous[ii] = f
        if i % 80 == 0:
            plt.plot(x, u[-1])
            plt.pause(1/60)
        i += 1
    print('Adams-Bashforth CDS ', i)
    return u


# ---------------------------------- #
#           Backward Euler           #
# ---------------------------------- #
def bwd_e_cds():
    plt.figure()
    plt.grid()
    plt.title('Backward Euler - Central Differencing Scheme')
    i = 0
    u = [[i for i in np.sin(2 * np.pi * x)]]
    u_next = u[0][:]
    uimp = [0 for _ in range(N)]
    while 15 > max(max(u[-1]), abs(min(u[-1]))) > 0.05:
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

        if i % 100 == 0:
            # plt.plot(x, u[-1], 'b')
            plt.plot(x, uimp)
            plt.pause(1/60)

        i += 1
    print('Backwards Euler - CDS', i)
    return u


# Ufl = fwd_e_lus()
# Ufc = fwd_e_cds()
# Ufq = fwd_e_quick()
# Uac = as_ba_cds()
# Ual = as_ba_lus()
ubc = bwd_e_cds()
