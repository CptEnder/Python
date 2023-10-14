"""
@author: Cpt.Ender
                                  """
import matplotlib.pyplot as plt
import si_maths as mth
import numpy as np
import time

n = 20
dx = 1/(n-1)
x = mth.frange(0, 1, dx)
f = [-(3*i + i**2)*mth.e**i for i in x]

a = mth.mat.I(n)
for i in range(1, n-1):
    a[i][i-1] = 1
    a[i][i] = -2
    a[i][i+1] = 1
f[0] = f[-1] = 0

# Solving u = a^-1*f*dx^2
tic = time.time()
u = np.linalg.solve(a, f)
u = [float(i)*dx**2 for i in u]
print("Time for numpy's solution:", time.time() - tic)
tic = time.time()
u1 = mth.linalg.dias(a, f, 3)
u1 = [i*dx**2 for i in u1]
print("Time for my solution:", time.time() - tic)
# print(mth.mat.sub(u, u1))

plt.plot(x, u, x, u1)
plt.grid()
plt.show()
