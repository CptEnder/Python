"""
Created on Wed 20 Jan 21:28 2021
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt

file = open("R-3DampedOscPulse.txt")
lines = file.readlines()
Time = []
X1 = []
X2 = []
X3 = []
X4 = []
X5 = []
X6 = []

for i, line_ in enumerate(lines):
    if i % 2:
        line = line_.split('    ')
        count = line.count('')
        for ii in range(count):
            line.remove('')
        Time.append(float(line[0]))
        X1.append(float(line[1]))
        X2.append(float(line[2]))
        X3.append(float(line[3]))
        X4.append(float(line[4]))
        X5.append(float(line[5]))
        X6.append(float(line[6][:-1]))
        print(line)
file.close()

# Erwtima 4.1
vima = 150/15000
endTime = int(10.02//vima)
plt.grid()
plt.plot(Time[:endTime], X2[:endTime])

plt.figure()
plt.grid()
plt.plot(Time[:endTime], X4[:endTime])

plt.figure()
plt.grid()
plt.plot(Time[:endTime], X6[:endTime])
