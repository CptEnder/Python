"""
Created on Tue 09 Jun 13:17 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
from math import pi, e, cos

g = 9.81
r = 1025
W = [i / 1000 for i in range(1000)]
K = [w ** 2 / g for w in W]
H = 2
h1 = 15
R1 = 5
h2 = 7
b2 = 15
l2 = 100
Cm = 0.68
B = 50
zm = -10
zt = -15
Cv = Cm

Awl = 4*pi*R1**2
Vp = 2*b2*h2*l2
a33p = r*Cm*Vp
c33 = r*g*Awl
m = r*(8*pi*R1**2*h1+2*b2*h2*l2)
a33 = 2*Cv*pi*(b2/2)**2*l2*r
F30 = [r*g*H/2*e**(k*zm)*cos(k*B/2)*Awl*(e**(-k*(zt-zm))-(1+Cm)*k*Vp/Awl) for k in K]
X30 = [F30[i]/(-w**2*(m+a33)+c33) for i, w in enumerate(W)]

RAO_F30 = [abs(f30)/(r*g*H/2*Awl) for f30 in F30]
RAO_X30 = [abs(x30)*2/H for x30 in X30]

plt.plot(W, RAO_F30, label='RA0 Ftotal')
plt.plot(W, RAO_X30, label='RAO Heave')
plt.ylim(0, 2)
plt.xlim(0, max(W))
plt.grid()
plt.xlabel('ω [ras/sec]')
plt.legend(loc='upper center')
