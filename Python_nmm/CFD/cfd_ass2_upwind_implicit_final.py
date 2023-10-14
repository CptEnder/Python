import numpy as np
from matplotlib import pyplot as plt

# _________________________upwind scheme__________________________________
# _________________________implicit (Euler Backwards)_______________________________
xL = 1
dx = 0.01
dt = 0.1 * dx
N = int(xL / dx + 1)
v = 1 * 10 ** (-3)
T = 2

uimp = np.zeros(N)
x = np.linspace(0, xL, N)
u = np.sin(2 * np.pi * x)
plt.grid()
plt.plot(x, u, 'k-')

# oi dio parakatw grammes mpikan gia na mporei i python na anagnwrisei
# tin lista-array kai na kanei append kathe lista me u gia explicit
arxeio = [[i for i in np.sin(2 * np.pi * x)]]
un = arxeio[0][:]

# afto to loop ipologizei tis times u(n) me explicit methodo
# meta tha mpoun stin implicit methodo
for t in np.arange(0, T, dt):

    for i in range(1, N - 1, 1):
        # ta ue kai uw einai oi komvoi anatolika kai ditika tou up antistoixa
        up = u[i]
        ue = u[i + 1]
        uw = u[i - 1]

        if up >= 0:
            # deiktis 1 = sinriakes ston komvo p
            ue1 = up
            uw1 = uw

            Fe = ue1
            Fw = uw1
            D = v / dx

            ap = (D + Fw) + D + (Fe - Fw)
            aw = (D + Fw)
            ae = D

            un[i] = u[i] - (ap * up - aw * uw - ae * ue) * (dt / dx)
            u[i] = un[i]

        # dimiourgw mia lista-arxeio pou periexei oles tis times twn u gia explicit
        # arxeio.append(un[:])

        if up < 0:
            ue1 = ue
            uw1 = up

            Fe = ue1
            Fw = uw1
            D = v / dx

            aw = D + max(Fw, 0)
            ae = D + max(0, -Fe)
            ap = aw + ae + (Fe - Fw)

            un[i] = u[i] - (ap * up - aw * uw - ae * ue) * (dt / dx)
            u[i] = un[i]

    # dimiourgw mia lista-arxeio pou periexei oles tis times twn u gia explicit
    arxeio.append(un[:])

d = 1
for t in np.arange(0, T, dt):
    u = arxeio[d][:]
    upre = arxeio[d - 1][:]
    for i in range(1, N - 1, 1):
        up = u[i]
        ue = u[i + 1]
        uw = u[i - 1]

        if up >= 0:
            ue1 = up
            uw1 = uw

            Fe = ue1
            Fw = uw1
            D = v / dx

            ap = (D + Fw) + D + (Fe - Fw)
            aw = (D + Fw)
            ae = D

            uimp[i] = upre[i] - (ap * up - aw * uw - ae * ue) * (dt / dx)

        if up < 0:
            ue1 = ue
            uw1 = up

            Fe = ue1
            Fw = uw1
            D = v / dx

            aw = D + max(Fw, 0)
            ae = D + max(0, -Fe)
            ap = aw + ae + (Fe - Fw)

            uimp[i] = upre[i] - (ap * up - aw * uw - ae * ue) * (dt / dx)

    d = d + 1

    # plottarisma se frames
# plt.grid()
plt.plot(x, uimp, 'c-')
# plt.plot(x,uimp,'r.')
plt.xlabel('x')
plt.ylabel('u')
plt.title('Upwind Scheme - Backwards Euler')
# plt.pause(1 / 2000)
