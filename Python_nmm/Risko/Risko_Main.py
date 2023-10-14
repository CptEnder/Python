"""
Created on Mon 30 Nov 12:15 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)

ship 1 - DWT 73 000
                                  """
import risko_module as rm
import matplotlib.pyplot as plt
import numpy as np

""" Ship Characteristics [m]"""
L = 219.7
B = 32.26
D = 20.8
ds = 14.5  # Loadline depth
db = 0.3 * D  # Waterline
Z1 = 2  # Double bottom height
ps = 1.025  # sea water density t/m^3
dh = 2  # double hull
B_cargo = B - 2 * dh

"""" total volume of cargo oil, in m^3 at 98% tank filling """
C = 86178.2

""" Deadweight in tons """
DWT = 73632.5

pn = DWT / C  # Cargo density t/m^3

""" Creating the Tanks """
fr = 0.85  # frame length
StartingPosition = 13 * 0.7 + 39 * 0.8
# Tank_i = [xa, xf, zl, zu, yp, ys, tankBreadth, V]

""" Initial OM """
print("------------")
print(" Initial OM \n")

Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D, B - dh, B / 2, B / 2 - dh,
          6582 + 1414.2 + 319.2 / 2]
Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D, B / 2, dh, B / 2 - dh,
          6554.6 + 1409.9 + 319.2 / 2]

Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B - dh, B / 2, B / 2 - dh, 7093]
Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B / 2, dh, B / 2 - dh, 7103.9]

Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B - dh, B / 2, B / 2 - dh, 7127.4]
Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B / 2, dh, B / 2 - dh, 7084.9]

Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B - dh, B / 2, B / 2 - dh, 7133.2]
Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B / 2, dh, B / 2 - dh, 7108.5]

Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B - dh, B / 2, B / 2 - dh, 7127.3]
Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B / 2, dh, B / 2 - dh, 7107.6]

Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B - dh, B / 2, B / 2 - dh, 5651]
Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B / 2, dh, B / 2 - dh, 5637.9]

TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
            Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

OM = rm.regulation23([L, B, D, Z1, ds, ps, pn, C], TankList)

# Conditions for acceptable values of OM related to Cargo Oil volume and DWT
if DWT >= 5000:
    if C <= 200000:
        if OM >= 0.015:
            print("The Annex I regulation 23 is not satisfied")
        else:
            print("The Annex I regulation 23 is satisfied")
    elif 200000 < C < 400000:
        if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
            print("The Annex I regulation 23 is not satisfied")
        else:
            print("The Annex I regulation 23 is satisfied")
    elif C >= 400000:
        if OM >= 0.012:
            print("The Annex I regulation 23 is not satisfied")
        else:
            print("The Annex I regulation 23 is satisfied")

""" Variation of the number of Longitudinal Compartments """
print("------------------------------------------------------")
print(""" Variation of the number of Longitudinal Compartments""")
OMList = []
startingNumOfTanks = 6
endingNumbOfTanks = 12
x_axis = range(startingNumOfTanks, endingNumbOfTanks)
for j in x_axis:
    N = 2 * j
    print("\n", str(N // 2) + "x2")

    TankList = []
    for i in range(N // 2):
        vima = (249 - 52) * fr / N * 2
        tank_iP = [StartingPosition + i * vima, StartingPosition + (i + 1) * vima, Z1, D, B - dh, B / 2, B / 2 - dh,
                   C / N * 0.98]
        tank_iS = [StartingPosition + i * vima, StartingPosition + (i + 1) * vima, Z1, D, B / 2, dh, B / 2 - dh,
                   C / N * 0.98]
        TankList.append(tank_iP)
        TankList.append(tank_iS)

    OM = rm.regulation23([L, B, D, Z1, ds, ps, pn, C], TankList)
    OMList.append(OM)

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT >= 5000:
        if C <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
                print("The Annex I regulation 23 is not satisfied")
        elif C >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, constrained_layout=True)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the Number of longitudinal compartments")

ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2.plot(x_axis, [DWT] * len(x_axis), '.-')
ax2.grid()
ax2.set_ylim(top=DWT * 1.005, bottom=DWT * 0.99)
ax2.set_ylabel("Deadweight [tons]")

""" Variation of Double Hull while keeping the same DWT """
print("-----------------------------------------------------")
print(""" Variation of Double Hull while keeping the same DWT""")
OMList = []
B_list = []
B_temp = B
maxDH = dh + 1
x_axis = np.linspace(dh, maxDH, 6)
for j in range(len(x_axis)):
    B_list.append(B_temp)
    dh_temp = x_axis[j]

    Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D,
              B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp, 6582 + 1414.2 + 319.2 / 2]
    Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D,
              B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 6554.6 + 1409.9 + 319.2 / 2]

    Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp, 7093]
    Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7103.9]

    Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7127.4]
    Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7084.9]

    Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7133.2]
    Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7108.5]

    Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7127.3]
    Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7107.6]

    Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp, 5651]
    Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 5637.9]

    TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
                Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

    print(f"\nBreadth: {round(B_temp, 3)} m, Double Hull: {round(dh_temp, 3)} m")
    OM = rm.regulation23([L, B_temp, D, Z1, ds, ps, pn, C], TankList)
    OMList.append(OM)
    B_temp += 2 * (x_axis[1] - x_axis[0])

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT >= 5000:
        if C <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
                print("The Annex I regulation 23 is not satisfied")
        elif C >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the length of Double Hull")

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(x_axis, [DWT] * len(x_axis), '.-')
ax2.grid()
ax2.set_ylim(top=DWT * 1.005, bottom=DWT * 0.99)
ax2.set_ylabel("Deadweight [tons]")

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x_axis, B_list, '.-')
ax3.grid()
ax3.set_ylabel("Breadth [m]")

""" Variation of Double Bottom while keeping the same DWT """
print("-------------------------------------------------------")
print(""" Variation of Double Bottom while keeping the same DWT""")
OMList = []
D_list = []
D_temp = D
T_temp = ds
maxDB = Z1 + 1
x_axis = np.linspace(Z1, maxDB, 6)
for z1 in x_axis:
    D_list.append(D_temp)

    Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, z1, D_temp, B - dh, B / 2, B / 2 - dh,
              6582 + 1414.2 + 319.2 / 2]
    Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, z1, D_temp, B / 2, dh, B / 2 - dh,
              6554.6 + 1409.9 + 319.2 / 2]

    Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1, D_temp, B - dh, B / 2, B / 2 - dh, 7093]
    Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1, D_temp, B / 2, dh, B / 2 - dh, 7103.9]

    Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1, D_temp, B - dh, B / 2, B / 2 - dh, 7127.4]
    Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1, D_temp, B / 2, dh, B / 2 - dh, 7084.9]

    Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1, D_temp, B - dh, B / 2, B / 2 - dh, 7133.2]
    Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1, D_temp, B / 2, dh, B / 2 - dh, 7108.5]

    Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1, D_temp, B - dh, B / 2, B / 2 - dh, 7127.3]
    Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1, D_temp, B / 2, dh, B / 2 - dh, 7107.6]

    Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1, D_temp, B - dh, B / 2, B / 2 - dh, 5651]
    Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1, D_temp, B / 2, dh, B / 2 - dh, 5637.9]

    TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
                Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

    print(f"\nDepth: {round(D_temp, 3)} m, Double Bottom: {round(z1, 3)} m")
    OM = rm.regulation23([L, B, D_temp, z1, T_temp, ps, pn, C], TankList)
    OMList.append(OM)
    D_temp += (x_axis[1] - x_axis[0])
    T_temp += (x_axis[1] - x_axis[0])

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT >= 5000:
        if C <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
                print("The Annex I regulation 23 is not satisfied")
        elif C >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the length of Double Bottom")

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(x_axis, [DWT] * len(x_axis), '.-')
ax2.grid()
ax2.set_ylim(top=DWT * 1.005, bottom=DWT * 0.99)
ax2.set_ylabel("Deadweight [tons]")

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x_axis, D_list, '.-')
ax3.grid()
ax3.set_ylabel("Depth [m]")

""" Variation of Double Hull and Double Bottom while keeping the same DWT """
print("-----------------------------------------------------------------------")
print(""" Variation of Double Hull and Double Bottom while keeping the same DWT""")
OMList = []

B_list = []
B_temp = B

D_list = []
D_temp = D
T_temp = ds

x_axis = np.linspace(0, 1, 6)
for j in range(len(x_axis)):
    B_list.append(B_temp)
    dh_temp = dh + x_axis[j]

    D_list.append(D_temp)
    z1 = Z1 + x_axis[j]

    Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, z1, D_temp,
              B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp, 6582 + 1414.2 + 319.2 / 2]
    Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, z1, D_temp,
              B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 6554.6 + 1409.9 + 319.2 / 2]

    Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1, D_temp, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7093]
    Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1, D_temp, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7103.9]

    Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1, D_temp, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7127.4]
    Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1, D_temp, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7084.9]

    Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1, D_temp, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7133.2]
    Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1, D_temp, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7108.5]

    Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1, D_temp, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              7127.3]
    Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1, D_temp, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 7107.6]

    Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1, D_temp, B_temp - dh_temp, B_temp / 2, B_temp / 2 - dh_temp,
              5651]
    Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1, D_temp, B_temp / 2, dh_temp, B_temp / 2 - dh_temp, 5637.9]

    TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
                Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

    print(f"\nBreadth: {round(B_temp, 3)} m, Double Hull: {round(dh_temp, 3)} m")
    print(f"Depth: {round(D_temp, 3)} m, Double Bottom: {round(z1, 3)} m")

    OM = rm.regulation23([L, B_temp, D_temp, z1, T_temp, ps, pn, C], TankList)
    OMList.append(OM)
    B_temp += 2 * (x_axis[1] - x_axis[0])
    D_temp += (x_axis[1] - x_axis[0])
    T_temp += (x_axis[1] - x_axis[0])

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT >= 5000:
        if C <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
                print("The Annex I regulation 23 is not satisfied")
        elif C >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 2)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the length of Double Hull and Double Bottom")

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2 = fig.add_subplot(gs[2, :])
ax2.plot(x_axis, [DWT] * len(x_axis), '.-')
ax2.grid()
ax2.set_ylim(top=DWT * 1.005, bottom=DWT * 0.99)
ax2.set_ylabel("Deadweight [tons]")

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x_axis, B_list, '.-')
ax3.grid()
ax3.set_ylabel("Breadth [m]")

ax4 = fig.add_subplot(gs[1, 0])
ax4.plot(x_axis, D_list, '.-')
ax4.grid()
ax4.set_ylabel("Depth [m]")

""" Variation of Double Hull while keeping the same ship dimensions """
print("-----------------------------------------------------------------")
print(""" Variation of Double Hull while keeping the same ship dimensions""")
OMList = []

DWT_List = []

x_axis = np.linspace(0, 0.5, 5) + dh
for j in range(len(x_axis)):
    dh_temp = x_axis[j]
    C_temp = C

    Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D,
              B - dh_temp, B / 2, B / 2 - dh_temp, 6582 + 1414.2 + 319.2 / 2]
    Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, Z1, D,
              B / 2, dh_temp, B / 2 - dh_temp, 6554.6 + 1409.9 + 319.2 / 2]

    Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B - dh_temp, B / 2, B / 2 - dh_temp, 7093]
    Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, Z1, D, B / 2, dh_temp, B / 2 - dh_temp, 7103.9]

    Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B - dh_temp, B / 2, B / 2 - dh_temp, 7127.4]
    Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, Z1, D, B / 2, dh_temp, B / 2 - dh_temp, 7084.9]

    Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B - dh_temp, B / 2, B / 2 - dh_temp, 7133.2]
    Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, Z1, D, B / 2, dh_temp, B / 2 - dh_temp, 7108.5]

    Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B - dh_temp, B / 2, B / 2 - dh_temp, 7127.3]
    Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, Z1, D, B / 2, dh_temp, B / 2 - dh_temp, 7107.6]

    Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B - dh_temp, B / 2, B / 2 - dh_temp, 5651]
    Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, Z1, D, B / 2, dh_temp, B / 2 - dh_temp, 5637.9]

    TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
                Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

    # Decrease of tankVolume and C by Dx * Dy * Dz
    for tank in TankList:
        # Tank Volume -= Dx * Dy * Dz
        tank[-1] -= (tank[1] - tank[0]) * (x_axis[j] - x_axis[0]) * (tank[3] - tank[2])
        C_temp -= (tank[1] - tank[0]) * (x_axis[j] - x_axis[0]) * (tank[3] - tank[2])

    print(f"\nBreadth: {round(B, 3)} m, Double Hull: {round(dh_temp, 3)} m")
    DWT_List.append(C_temp * pn)
    OM = rm.regulation23([L, B, D, Z1, ds, ps, pn, C_temp], TankList)
    OMList.append(OM)

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT_List[j] >= 5000:
        if C_temp <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C_temp < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C_temp):
                print("The Annex I regulation 23 is not satisfied")
        elif C_temp >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the length of Double Hull")

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(x_axis, DWT_List, '.-')
ax2.grid()
ax2.set_ylabel("Deadweight [tons]")

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x_axis, [B] * len(x_axis), '.-')
ax3.grid()
ax3.set_ylim(top=B * 1.005, bottom=B * 0.99)
ax3.set_ylabel("Breadth [m]")

""" Variation of Double Bottom while keeping the same ship dimensions """
print("-------------------------------------------------------------------")
print(""" Variation of Double Bottom while keeping the same ship dimensions""")
OMList = []

DWT_List = []

x_axis = np.linspace(0, 1, 5) + Z1
for j in range(len(x_axis)):
    z1_temp = x_axis[j]
    C_temp = C

    Tank6P = [StartingPosition, (90 - 52) * fr + StartingPosition, z1_temp, D,
              B - dh, B / 2, B / 2 - dh, 6582 + 1414.2 + 319.2 / 2]
    Tank6S = [StartingPosition, (90 - 52) * fr + StartingPosition, z1_temp, D,
              B / 2, dh, B / 2 - dh, 6554.6 + 1409.9 + 319.2 / 2]

    Tank5P = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1_temp, D, B - dh, B / 2, B / 2 - dh, 7093]
    Tank5S = [Tank6P[1], Tank6P[1] + (122 - 90) * fr, z1_temp, D, B / 2, dh, B / 2 - dh, 7103.9]

    Tank4P = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1_temp, D, B - dh, B / 2, B / 2 - dh, 7127.4]
    Tank4S = [Tank5P[1], Tank5P[1] + (154 - 122) * fr, z1_temp, D, B / 2, dh, B / 2 - dh, 7084.9]

    Tank3P = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1_temp, D, B - dh, B / 2, B / 2 - dh, 7133.2]
    Tank3S = [Tank4P[1], Tank4P[1] + (186 - 154) * fr, z1_temp, D, B / 2, dh, B / 2 - dh, 7108.5]

    Tank2P = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1_temp, D, B - dh, B / 2, B / 2 - dh, 7127.3]
    Tank2S = [Tank3P[1], Tank3P[1] + (218 - 186) * fr, z1_temp, D, B / 2, dh, B / 2 - dh, 7107.6]

    Tank1P = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1_temp, D, B - dh, B / 2, B / 2 - dh, 5651]
    Tank1S = [Tank2P[1], Tank2P[1] + (249 - 218) * fr, z1_temp, D, B / 2, dh, B / 2 - dh, 5637.9]

    TankList = [Tank1P, Tank1S, Tank2P, Tank2S, Tank3P, Tank3S,
                Tank4P, Tank4S, Tank5P, Tank5S, Tank6P, Tank6S]

    # Decrease of tankVolume and C by Dx * Dy * Dz
    for tank in TankList:
        # Tank Volume -= Dx * Dy * Dz
        tank[-1] -= (tank[1] - tank[0]) * (tank[4] - tank[5]) * (x_axis[j] - x_axis[0])
        C_temp -= (tank[1] - tank[0]) * (tank[4] - tank[5]) * (x_axis[j] - x_axis[0])

    print(f"\nDepth: {round(D, 3)} m, Double Hull: {round(z1_temp, 3)} m")
    DWT_List.append(C_temp * pn)
    OM = rm.regulation23([L, B, D, z1_temp, ds, ps, pn, C_temp], TankList)
    OMList.append(OM)

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT_List[j] >= 5000:
        if C_temp <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C_temp < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C_temp):
                print("The Annex I regulation 23 is not satisfied")
        elif C_temp >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the length of Double Bottom")

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_ylabel("Mean Oil Outflow")

ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(x_axis, DWT_List, '.-')
ax2.grid()
ax2.set_ylabel("Deadweight [tons]")

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x_axis, [D] * len(x_axis), '.-')
ax3.grid()
ax3.set_ylim(top=D * 1.005, bottom=D * 0.99)
ax3.set_ylabel("Depth [m]")

""" Variation of the breadth of Transverse Compartments """
print("-----------------------------------------------------")
print(""" Variation of the breadth of Transverse Compartments""")

OMList = []
N = 6 * 3
n = 6
print(str(n) + "x3")
x_axis = list(np.linspace(B_cargo / 2, B_cargo / 3, 6))  # the breadth of the Center Compartment

for b_center in x_axis:

    b_side = (B_cargo - b_center) / 2  # the breadth of the Site Compartments
    TankList = []
    vima = (249 - 52) * fr / n

    for i in range(n):
        tank_iP = [StartingPosition + i * vima, StartingPosition + (i + 1) * vima, Z1, D,
                   B - dh, B - dh - b_side, b_side, C / N * 0.98]
        tank_iC = [StartingPosition + i * vima, StartingPosition + (i + 1) * vima, Z1, D,
                   B - dh - b_side, dh + b_side + b_center, b_center, C / N * 0.98]
        tank_iS = [StartingPosition + i * vima, StartingPosition + (i + 1) * vima, Z1, D,
                   dh + b_side + b_center, dh, b_side, C / N * 0.98]
        TankList.append(tank_iP)
        TankList.append(tank_iC)
        TankList.append(tank_iS)

    print("\nBreadth of the Center Compartment: ", round(b_center, 3), "m")
    print("Breadth of the Side Compartment: ", round(b_side, 3), "m")
    OM = rm.regulation23([L, B, D, Z1, ds, ps, pn, C], TankList)
    OMList.append(OM)

    # Conditions for acceptable values of OM related to Cargo Oil volume and DWT
    if DWT >= 5000:
        if C <= 200000:
            if OM >= 0.015:
                print("The Annex I regulation 23 is not satisfied")
        elif 200000 < C < 400000:
            if OM >= 0.012 + (0.003 / 200000) * (400000 - C):
                print("The Annex I regulation 23 is not satisfied")
        elif C >= 400000:
            if OM >= 0.012:
                print("The Annex I regulation 23 is not satisfied")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, constrained_layout=True)
fig.set_size_inches(10, 6)
fig.suptitle("OM change as a function of the breadth of Center Compartment")

ax1.plot(x_axis, OMList, '.-')
ax1.plot([x_axis[0], x_axis[-1]], [OMList[0], OMList[-1]], 'r--')
ax1.grid()
ax1.set_xlim(x_axis[0] * 1.01, x_axis[-1] * 0.99)
ax1.set_ylabel("Mean Oil Outflow")

ax2.plot(x_axis, [DWT] * len(x_axis), '.-')
ax2.grid()
ax2.set_ylim(top=DWT * 1.005, bottom=DWT * 0.99)
ax2.set_ylabel("Deadweight [tons]")
