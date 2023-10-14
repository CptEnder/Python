"""
Created on Tue 26 Nov 11:30 2019
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
from math import pi

a = 2.7
w = 107.2
sy = [1470, 1730, 500]
smax = [i/1.5 for i in sy]
Kic = [1500, 2900, 1040]
Ki = []
amax = []
smax_y = []
smax_p = []
Y = 1.12 - 0.23 * (a / w) + 10.56 * (a / w) ** 2 - 21.74 * (a / w) ** 3 + 30.42 * (a / w) ** 4

for i in range(0, 3):
    Ki.append(Y*smax[i]*(pi*a)**0.5)

for i in range(0, 3):
    amax.append(1/pi*(Kic[i]/(Y*smax[i]))**2)  # smax i sy ?

for i in range(0, 3):
    smax_y.append(Kic[i]/Y/(pi*a)**0.5)
    smax_p.append(sy[i] * (w - a) / w)

