"""
Created on Tue 26 Nov 12:03 2019
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
from math import pi

C = 1.095*10**-9
m = 3
R = 0.6
a = 0.001
Kmin = 3
Kic = 78
smin = Kmin/(1.12*(pi*a)**0.5)
smax = smin/R
Kmax = Kmin/R
Dkth = Kmax - Kmin
da_dn = C*(Dkth*10**2)**m

Kmin_f = Kic*R
Dkf = Kic-Kmin_f
a_f = 1 / pi * (Kic / 1.12 / smax) ** 2

