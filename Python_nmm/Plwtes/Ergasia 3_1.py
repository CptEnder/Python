"""
Created on Mon 08 Jun 11:57 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
from math import pi, e

H = 2
r = 1025
W = [i / 100 for i in range(150)]
g = 9.81
K = [w ** 2 / g for w in W]
Cv1 = 1.562
Cv2 = 1.751
Cv3 = 2.112
J = 0.635
h2 = 17.32
R1 = h2 / 4
R2 = 2 * R1
h1 = 2 * h2
a = R2 / R1

M = pi * r * (R1 ** 2 * h1 + R2 ** 2 * h2)
A33 = 2 / 3 * pi * r * J * (2 * Cv1 * R2 ** 3 - 2 * Cv2 * R1 ** 3 + Cv3 * R1 ** 3)
C33 = r * g * pi * R1 ** 2
xc = [e**(-k*h1)*((e**(-k*h2)-1)*a**2+1) for k in K]
C = [C33*x for x in xc]
A = [2/3*pi*r*J*R1**3*e**(-k*h1)*((Cv1*a**3 - Cv2)*(1+e**(-k*h2))+Cv3*e**(-k*h2)) for k in K]

F30_FK = [c*H/2 for c in C]
F30_acc = [-W[i]**2*H/2*Ai for i, Ai in enumerate(A)]
F30 = [fk + F30_acc[i] for i, fk in enumerate(F30_FK)]
RAO_all = [abs(f30) / (r*g*pi*R2**2*H/2) for f30 in F30]
RAO_acc = [abs(facc) / (r*g*pi*R2**2*H/2) for facc in F30_acc]
RAO_fk = [abs(ffk) / (r*g*pi*R2**2*H/2) for ffk in F30_FK]
X30 = [F30[i] / (C33 - (M + A33) * w ** 2) for i, w in enumerate(W)]
RAO_heave = [abs(x30)/(H/2) for x30 in X30]

# F30_FK1 = [r * g * pi * H / 2 * R1 ** 2 * e ** (-k * h1) * ((e ** (-k * h2) - 1) * a + 1) for k in K]
# F30_acc1 = [-2 / 3 * pi * r * J * k * g * H / 2 * (e ** (-k * (h1 + h2)) *
#             (Cv1 * R2 ** 3 - Cv2 * R1 ** 3 + Cv3 * R1 ** 3) + e ** (-k * h1) * (Cv1 * R2 ** 3 - Cv2 * R1 ** 3))
#             for k in K]
# F301 = [fk + F30_acc[i] for i, fk in enumerate(F30_FK1)]
# RAO_all1 = [abs(f30) / (r*g*pi*R2**2*H/2) for f30 in F301]
# RAO_acc1 = [abs(facc) / (r*g*pi*R2**2*H/2) for facc in F30_acc1]
# RAO_fk1 = [abs(ffk) / (r*g*pi*R2**2*H/2) for ffk in F30_FK1]


plt.plot(W, RAO_all, label='RAO Ftotal')
plt.plot(W, RAO_acc, label='RAO Facc')
plt.plot(W, RAO_fk, label='RAO Ffk')
plt.xlabel('ω [ras/sec]')
plt.ylabel('F30/(ρπg*R2^2*H/2)')
plt.xlim(0, max(W))
plt.ylim(bottom=0)
plt.legend()
plt.grid()

plt.figure()
plt.title('RAO Heave')
plt.plot(W, RAO_heave)
plt.ylim(0, 2)
plt.xlim(0, 1)
plt.grid()
plt.xlabel('ω [ras/sec]')
plt.ylabel('X30/(H/2)')
