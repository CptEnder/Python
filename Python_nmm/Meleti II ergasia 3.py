"""
Created on Sat 16 May 20:52 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import math as mth

r = 0.03
i = 0.01
k1 = r + 1
k2 = i + 1
RBR = 0
C = [1000, 100, 15]
V = [31, 43, 38, 49, 46, 67, 48, 31, 44, 50,
     43, 49, 32, 68, 49, 53, 52, 50, 35, 35,
     38, 38, 59, 57, 47]

for t in range(1, 26):
    pc = (1 + mth.log(t) - mth.log(t+1))*10**-4
    Cost = 0
    Value = 0
    for T in range(3):
        Cost += C[T]*r/(k1**(T+1)*mth.log(k1))
    for s in range(1, t+1):
        Value += V[s-1]*i/(k2**s*mth.log(k2))
    RBR += pc*Cost/Value
