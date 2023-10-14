"""
Created on Sat 07 Nov 11:19 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
import numpy as np

# L = input()
L = 219.7
# B = input()
B = 32.26
# D = input()
D = 20.8
# ds = input()
ds = 14.5  # Loadline depth
db = 0.3 * D  # Waterline
Z1 = 2  # Double bottom height
ps = 1.025  # sea water density t/m^3
dh = B / 2 - 14.13  # Double Hull


def linearInterpolation(_xm: float, Xaxis: list, Yaxis: list):
    for _i, _x in enumerate(Xaxis):
        if _x <= _xm <= Xaxis[_i + 1]:
            _x1 = _x
            _x2 = Xaxis[_i + 1]
            _f1 = Yaxis[_i]
            _f2 = Yaxis[_i + 1]
            _fm = _f1 + (_f2 - _f1) * (_xm - _x1) / (_x2 - _x1)
            break
    return _fm


def trapezoidIntegration(b1, b2, h):
    return (b1 + b2) * h / 2


"""" total volume of cargo oil, in m^3 at 98% tank filling """
# C = input()
C = 86178.2

# n =input()
n = 6  # Number of tanks

""" Deadweight in tons """
# DWT = input()
DWT = 73632.5

pn = DWT / C  # Cargo density

""" Permeability and tank filling coefficients """
d1 = 0.99
d2 = 0.98

""" Cargo Oil Tanks positions from aft and volume @ 98% """
fr = 0.85  # frame length
StartingPosition = 13 * 0.7 + 39 * 0.8
# Tank_i = [xa, xf, zl, zu, V]
Tank6 = [StartingPosition, (90 - 52) * fr + StartingPosition, 2, 20.8, 2199.2 * 2]
Tank5 = [Tank6[1], Tank6[1] + (122 - 90) * fr, 2, 20.8, 1861.6 * 2]
Tank4 = [Tank5[1], Tank5[1] + (154 - 122) * fr, 2, 20.8, 1862 * 2]
Tank3 = [Tank4[1], Tank4[1] + (186 - 154) * fr, 2, 20.8, 1862 * 2]
Tank2 = [Tank3[1], Tank3[1] + (218 - 186) * fr, 2, 20.8, 1854 * 2]
Tank1 = [Tank2[1], Tank2[1] + (249 - 218) * fr, 2, 20.8, 2003 * 2]

TankS = [Tank1, Tank2, Tank3, Tank4, Tank5, Tank6]

""" Probability density functions for side damage """

pdf_LoLo = [[0, 1], [1, 1]]  # Longitudinal Location
pdf_LoEx = [[0, 0.1, 0.2, 0.3], [11.95, 3.5, 0.35, 0.35]]  # Longitudinal Extent
pdf_TrPe = [[0, 0.05, 0.1, 0.3], [24.96, 5, 0.56, 0.56]]  # Traverse Penetration
pdf_VeEx = [[0, 0.3, 1], [3.83, 0.5, 0.5]]  # Vertical Extent
pdf_VeLo = [[0, 0.25, 0.5, 1], [0, 0.25, 1.5, 1.5]]  # Vertical Location

""" Probability density functions for bottom damage """

pdf_LoLoB = [[0, 0.5, 1], [0.2, 0.6, 2.6]]  # Longitudinal Location
pdf_LoExB = [[0, 0.3, 0.8], [4.5, 0.5, 0.5]]  # Longitudinal Extent
pdf_VePeB = [[0, 0.1, 0.3], [14.5, 1.1, 1.1]]  # Vertical Penetration
pdf_TrExB = [[0, 0.3, 0.9, 1], [4, 0.4, 0.4, 1.6]]  # Traverse Extent
pdf_TrLoB = [[0, 1], [1, 1]]  # Traverse Location

# for lst in [pdf_LoLo, pdf_LoEx, pdf_TrPe, pdf_VeEx, pdf_VeLo]:
#     plt.figure()
#     plt.grid()
#     plt.plot(lst[0], lst[1])

""" Regulation 24 - Annex I application """
minLoEx = min(L ** (2 / 3) / 3, 14.5)  # Longitudinal Extent
minTrEx = min(B / 5, 11.5)  # Traverse Extent
minVeEx = 0.5  # Vertical Extent

minLoExB = [min(L / 10, 5), L / 10]  # Longitudinal Extent bottom damage
minTrExB = max(min(B / 6, 10), 5)  # Traverse Extent bottom damage
minVeExtB = min(B / 15, 6)  # Vertical Extent bottom damage

""" Calculating probabilities for side damage """
step = 0.05
probabilitiesTable = []
for x in np.arange(pdf_LoLo[0][0], pdf_LoLo[0][-1], step):
    f_LoLo1 = linearInterpolation(x, pdf_LoLo[0], pdf_LoLo[1])
    f_LoLo2 = linearInterpolation(x + step, pdf_LoLo[0], pdf_LoLo[1])
    px = trapezoidIntegration(f_LoLo1, f_LoLo2, step)
    for l in np.arange(pdf_LoEx[0][0], pdf_LoEx[0][-1], step):
        f_LoEx1 = linearInterpolation(l, pdf_LoEx[0], pdf_LoEx[1])
        f_LoEx2 = linearInterpolation(l + step, pdf_LoEx[0], pdf_LoEx[1])
        py = trapezoidIntegration(f_LoEx1, f_LoEx2, step)
        for t in np.arange(pdf_TrPe[0][0], pdf_TrPe[0][-1], step):
            f_TrPe1 = linearInterpolation(t, pdf_TrPe[0], pdf_TrPe[1])
            f_TrPe2 = linearInterpolation(t + step, pdf_TrPe[0], pdf_TrPe[1])
            pz = trapezoidIntegration(f_TrPe1, f_TrPe2, step)
            probabilitiesTable.append(px * py * pz)

""" Calculating probabilities for bottom damage """

probabilitiesTableB = []
for x in np.arange(pdf_LoLoB[0][0], pdf_LoLoB[0][-1], step):
    f_LoLo1B = linearInterpolation(x, pdf_LoLoB[0], pdf_LoLoB[1])
    f_LoLo2B = linearInterpolation(x + step, pdf_LoLoB[0], pdf_LoLoB[1])
    pxB = trapezoidIntegration(f_LoLo1B, f_LoLo2B, step)
    for l in np.arange(pdf_LoExB[0][0], pdf_LoExB[0][-1], step):
        f_LoEx1B = linearInterpolation(l, pdf_LoExB[0], pdf_LoExB[1])
        f_LoEx2B = linearInterpolation(l + step, pdf_LoExB[0], pdf_LoExB[1])
        pyB = trapezoidIntegration(f_LoEx1B, f_LoEx2B, step)
        for t in np.arange(pdf_VePeB[0][0], pdf_VePeB[0][-1], step):
            f_VePe1B = linearInterpolation(t, pdf_VePeB[0], pdf_VePeB[1])
            f_VePe2B = linearInterpolation(t + step, pdf_VePeB[0], pdf_VePeB[1])
            pzB = trapezoidIntegration(f_VePe1B, f_VePe2B, step)
            probabilitiesTableB.append(pxB * pyB * pzB)

""" Calculating probability of damage for each Tank alone"""
step = 0.01
oneTankProbabilities = []
for tank in TankS:
    tankX_aft = tank[0] / L
    tankX_fwd = tank[1] / L
    # print((tankX_fwd - tankX_aft) * L)

    probabilitiesTable = []
    for x in np.arange(tankX_aft, tankX_fwd, step):
        f_LoLo1 = linearInterpolation(x, pdf_LoLo[0], pdf_LoLo[1])
        f_LoLo2 = linearInterpolation(x + step, pdf_LoLo[0], pdf_LoLo[1])
        px = trapezoidIntegration(f_LoLo1, f_LoLo2, step)
        for l in np.arange(pdf_LoEx[0][0], pdf_LoEx[0][-1], step):
            f_LoEx1 = linearInterpolation(l, pdf_LoEx[0], pdf_LoEx[1])
            f_LoEx2 = linearInterpolation(l + step, pdf_LoEx[0], pdf_LoEx[1])
            py = trapezoidIntegration(f_LoEx1, f_LoEx2, step)
            for t in np.arange(pdf_TrPe[0][0], pdf_TrPe[0][-1], step):
                f_TrPe1 = linearInterpolation(t, pdf_TrPe[0], pdf_TrPe[1])
                f_TrPe2 = linearInterpolation(t + step, pdf_TrPe[0], pdf_TrPe[1])
                pz = trapezoidIntegration(f_TrPe1, f_TrPe2, step)
                if t < dh / B:
                    pz = 0
                probabilitiesTable.append(px * py * pz)

    oneTankProbabilities.append(sum(probabilitiesTable))
print(oneTankProbabilities)

oneTankProbabilitiesB = []
for tank in TankS:
    tankX_aft = tank[0] / L
    tankX_fwd = tank[1] / L

    probabilitiesTableB = []
    for x in np.arange(tankX_aft, tankX_fwd, step):
        f_LoLo1B = linearInterpolation(x, pdf_LoLoB[0], pdf_LoLoB[1])
        f_LoLo2B = linearInterpolation(x + step, pdf_LoLoB[0], pdf_LoLoB[1])
        pxB = trapezoidIntegration(f_LoLo1B, f_LoLo2B, step)
        for l in np.arange(pdf_LoExB[0][0], pdf_LoExB[0][-1], step):
            f_LoEx1B = linearInterpolation(l, pdf_LoExB[0], pdf_LoExB[1])
            f_LoEx2B = linearInterpolation(l + step, pdf_LoExB[0], pdf_LoExB[1])
            pyB = trapezoidIntegration(f_LoEx1B, f_LoEx2B, step)
            for t in np.arange(pdf_VePeB[0][0], pdf_VePeB[0][-1], step):
                f_VePe1B = linearInterpolation(t, pdf_VePeB[0], pdf_VePeB[1])
                f_VePe2B = linearInterpolation(t + step, pdf_VePeB[0], pdf_VePeB[1])
                pzB = trapezoidIntegration(f_VePe1B, f_VePe2B, step)
                if t < Z1 / D:
                    pzB = 0
                probabilitiesTableB.append(pxB * pyB * pzB)

    oneTankProbabilitiesB.append(sum(probabilitiesTableB))
print(oneTankProbabilitiesB)
