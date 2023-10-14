"""
Created on Wed 20 May 13:14 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import math as mth

w = 0.5
d = [160, 80]
H = 12
c = 1/2
dn = [0.6666666666, 0.3555555555, 0.1608465608,
      0.0632098765, 0.0217540484, 0.0065407983]
R = [1.4, 0.5]

for h in d:
    s = 0
    y = w**2*h/9.81
    for i in range(1, 7):
        s += dn[i-1]*y**i

    kh = (y**2 + y/(1+s))**0.5
    k = kh/h

    for r in R:
        D = (H*(mth.sinh(2*kh)-2*kh)/(4*mth.pi*r*(mth.cosh(2*kh)-1)))
        print(D, kh)
