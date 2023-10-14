"""
Created on Thu 07 Nov 12:09 2019
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt

x = 16
y = 11
hg = -6 - 0.25*y
k = 0.12 + 0.005*x
Q = [i for i in range(22)]
Hap = [k*q**2 for q in Q]
Hs = [hap+hg for hap in Hap]
Hant = [30, 27, 24, 18, 13.5, 6.5]
Qant = [0, 6.6, 10.8, 15, 18, 20.4]

plt.grid()
plt.ylabel("H [m]")
plt.xlabel(r'$Q\ [m^3/s]$')
plt.title('Διάγραμμα β1')
plt.plot(Q, Hs, label='Αγωγός')
plt.plot(Qant, Hant, '--', label='Αντλία')
plt.legend()

plt.figure()
plt.grid()
plt.ylabel("H [m]")
plt.xlabel(r'$Q\ [m^3/s]$')
plt.title('Διάγραμμα β2')
plt.plot(Q, Hs, label='Αγωγός')
plt.plot(Qant, [hant*2 for hant in Hant], '--', label='Αντλία')
plt.legend()

plt.figure()
plt.grid()
plt.title('Διάγραμμα β3')
plt.ylabel("H [m]")
plt.xlabel(r'$Q\ [m^3/s]$')
plt.plot(Q, Hs, label='Αγωγός')
plt.plot([qant*2 for qant in Qant], Hant, '--', label='Αντλία')
plt.legend()
