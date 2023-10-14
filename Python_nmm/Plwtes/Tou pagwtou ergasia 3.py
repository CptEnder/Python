"""
Created on Tue 09 Jun 14:05 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import numpy as np
from matplotlib import pyplot as plt

'''erwtima a'''
T = 10  # s
w = np.pi * 2 / T
'''erwtima b'''
w = np.arange(0, 4, 0.1)
L = 37.5
d = 22 - 7 / 2
r = 5
pikn = 1025
g = 9.81
H = 2
A = H / 2
zm = d / 2
zt = -(22 - 7)
B = 50
# zm=zg gia evresi RAO sto simeio G kentrou varous tis kataskevis
zg = -10
zm = zg
# kimatarithmos k
k = (w ** 2) / g
# diatomes horizontal(h) kai vertical(v) merwn kataskevis
Ah = 15 * 7
Av = np.pi * (r ** 2)
print('Ah: ', Ah, 'Av: ', Av)
# an ogkos
V = 2 * (2 * Av * (d - 7 / 2) + 100 * Ah)
# maza
m = V * pikn
print('Mass m: ', m, 'kg')
# prostheti maza
a33 = 1.75 * pikn * V
print('Aditional mass: ', a33, 'kg')
# isalos epifaneia
Awl = 2 * (15 * 100 + 2 * np.pi * r ** 2)
print('Awl: ', Awl, 'sqr m')
# dinami F3 sto deksi melos
F3 = pikn * g * (H / 2) * np.exp(k * zm) * np.cos(k * B / 2) * Awl * (np.exp(k * (zt - zm)) - 2.75 * k * (V / Awl))
F3 = abs(F3)
print('F3 = ', F3, 'N')
# apokrisi x30
x30 = F3 / (-w ** 2 * (pikn * V + a33) + pikn * g * Awl)
x30 = abs(x30)
# print('x30: ',x30, 'm')
RAO_heave = x30 / A
RAO_F3 = F3 / (pikn * g * Awl * A)
plt.grid()
plt.plot(w, RAO_heave, 'b-')
plt.plot(w, RAO_F3, 'r-')
plt.xlabel('ω')
plt.ylabel('RAO')
