"""
Created on Wed 06 Nov 18:54 2019
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import matplotlib.pyplot as plt
from numpy import arange

# Input data
Pname = 1000
Psur = 3500
Pon = Pname + Psur
Non = 116
ns = 0.99
Ship_type = "Tanker"

# Erwtima 1
P_clean = Pon/1.25
Nclean = Non/1.031
Pmcr = Pon/ns
Nmcr = Non/ns
Pclean = P_clean/ns
MCR = [Nmcr, Pmcr]
CLEAN = [Nclean, Pclean]

# Engines field rating diagram
W5X40_B = [[146, 146, 104, 104, 146], [5675, 4550, 3250, 4050, 5675], 'W5X40-B']
W6X40_B = [[146, 146, 104, 104, 146], [6810, 5460, 3900, 4860, 6810], 'W6X40-B']
W7X35_B = [[167, 167, 118, 118, 167], [6090, 4865, 3430, 4305, 6090], 'W7X35-B']
engines = [W5X40_B, W6X40_B, W7X35_B]

plt.grid()
plt.ylabel("Engine Power [kW]")
plt.xlabel("Engine Speed [RPM]")
for e in engines:
    plt.plot(e[0], e[1], '-', label=e[2])
plt.plot(CLEAN[0], CLEAN[1], '+', label='Clean Hull and Calm Weather O.p.')
plt.plot(MCR[0], MCR[1], 'x', label='Fouled Hull O.p.')
plt.legend(loc='best')

# Epilogi tou Wartsila 5X40-B two-stroke engine
# https://www.wingd.com/en/engines/engine-types/diesel/x40-b/

# Erwtima 3
P_em = 100 + 0.55 * Pmcr**0.7  # Mesi ilektriki isxis
Pem = 1.35*P_em  # Proafksimeni kata 35% Pem
Num_gen = 4  # 3 + 1 for emergencies
Pgen = 455  # Wartsila 455W5L16 (1000 rpm, 50Hz)
Pel = Pgen*0.95
Pel_ol = Pel*3
Bhp_mcr = Pmcr*1.34102


# Erwtima 4
plt.figure()
plt.grid()
plt.ylabel("Engine Power [kW]")
plt.xlabel("Engine Speed [RPM]")
plt.plot(W5X40_B[0], W5X40_B[1], '-', label=W5X40_B[2])
plt.plot(CLEAN[0], CLEAN[1], '+', label='Clean Hull and Calm Weather O.p.')
plt.plot(MCR[0], MCR[1], 'x', label='Fouled Hull O.p.')
plt.legend(loc='best')

# Erwtima 5
Ccl = Pclean / Nclean**3  # Clean Hull & Calm Weather
Cmcr = Pmcr / Nmcr**3  # Fouled Hull
Cmcr_max = 1.2*Cmcr  # Fouled Hull & Heavy Weather

n = arange(0, 125, 0.05)
pcl = [[Ccl*i**3 for i in n], 'Clean Hull & Calm Weather']
pmcr = [[Cmcr*i**3 for i in n], 'Fouled Hull']
pmcr_max = [[Cmcr_max*i**3 for i in n], 'Fouled Hull & Heavy Weather']
n2 = arange(0,  0.96*Nmcr, 0.05)
p5 = []
for i in n2:
    if i < 0.4*Nmcr:
        c2 = 0
        c1 = 0.5
    elif 0.4 <= i < 0.6*Nmcr:
        c2 = 0.5
        c1 = 0.3
    else:
        c2 = 1.111
        c1 = -0.067
    p5.append(Pmcr*(c2*(i/Nmcr)**2+c1*i/Nmcr))

# Evresi simeiou tomis
for i in range(n2.__len__()):
    if pmcr_max[0][i] - p5[i] <= 0.05:
        Olp = [n2[i], p5[i]]

plt.figure()
plt.grid()
plt.ylabel("Power [kW]")
plt.xlabel("Speed [RPM]")
plt.plot(n, pcl[0], '-', label=pcl[1])
plt.plot(n, pmcr[0], '-', label=pmcr[1])
plt.plot(n, pmcr_max[0], '-', label=pmcr_max[1])
plt.plot(n2, p5, 'k-', label='Load Diagram')
plt.plot([1.04*Nmcr, 1.04*Nmcr, Nmcr, n2[n2.__len__()-1]], [0, Pmcr, Pmcr, p5[p5.__len__()-1]], 'k-')
plt.plot(Olp[0], Olp[1], 'r*', label='Fouled Hull & Heavy weather Overloading limit')
plt.plot(Nmcr, Pmcr, 'm*', label='Fouled Hull O.p.')
plt.plot(Nclean, Pclean, 'y*', label='Clean Hull & Calm Weather O.p.')

plt.legend(loc='best')

# Erwtima 6
z = 5
A = 0.771
b = 0.058
c = d = 1
na = 0.06*Nmcr + 14
pe = 21  # bar
s = 177  # Piston Stroke (cm)
D = 40  # Bore (cm)
Vh = 3.141592*D**2/4*s
v = A*(s/D)**(1/3)*(z+b*pe*na+0.9)*Vh*c*d/10**6  # m^3
V_ = 1.7*v*(30 - 9)  # m^3/h

# Erwtima 7
Hu = 39550  # thermiki ikanotita RMG -35
Hdes = 42700  # thermiki ikanotita kafsimou kataskevasti
BSFC_des = 176.9/1000  # kg/kWh
BSFC = BSFC_des*Hdes/Hu
mb_des = BSFC_des*Pmcr/3600
mb = BSFC*Pmcr/3600  # paroxi mazas kafsimou [kg/s]
Qfuel = mb*Hu  # Thermiki isxis kafsimou [kW]
mk_des = 33.4*1000/3600
mk = mk_des + (mb - mb_des)  # paroxi mazas kafsaeriou [kg/s]
R = (mk - mb)/mb
cp = (1.075+1.025)/2
Qex = mk*cp*(279 - 45)  # Thermiki isxis kafsaeriou [kW]

n_engine = Pmcr/Qfuel  # vathmos apodosis tis mixanis
a = Qex/Qfuel
k = 3070/Qfuel
r = 60/Qfuel
PA = (n_engine + a + k + r - 1)*100

Qboiler = mk*1.0625*(274-180)
nb = Qboiler/Qex

# Erwtima 9
Jeng = 10900
Jax = 53.97
Jp = 3.141592*3**4*0.025*8730/32
k1 = 14.13 * 10**6
k2 = 65.96 * 10**6

a = Jeng*Jax*Jp
b = k2*Jeng*Jax - k1*Jax*Jp - k1*Jeng*Jp - k2*Jeng*Jp
c = k1**2*Jp + k1*k2*(Jp+Jax+Jeng) + k2**2*Jp

W1 = (-b+(b**2-4*a*c)**0.5)/(2*a)
W2 = (-b-(b**2-4*a*c)**0.5)/(2*a)
w1 = W1**0.5
w2 = W2**0.5

# Erwtima 12
Build_cost = 400  # $/kW
Repairs_cost = 0.004  # $/kWh
Fuel_cost = 530  # $/t (RMG-35)
Cyl_oil_cost = 4400  # $/t
Oil_cost = 5180  # $/t

Days_per_year_sea = 300
Days_per_year_port = 50
Days_per_year_repairs = 15

Engine_daily_fuel_cons = 20.8353  # t/day
Engine_daily_cyl_oil_cons = 0.065  # t/day
Engine_daily_oil_cons = 0.014  # t/day

Gen_daily_fuel_cons = 61.39363  # t/day
Gen_daily_oil_cons = 0.1963  # t/day

Starting_cost = Build_cost*Pmcr
Repairs_cost_per_year = Repairs_cost*Pmcr*24*Days_per_year_repairs
Fuel_cost_per_year = Fuel_cost*(Engine_daily_fuel_cons*Days_per_year_sea +
                                Gen_daily_fuel_cons*(Days_per_year_port + Days_per_year_sea))
Oil_cost_per_year = (Oil_cost*(Engine_daily_oil_cons*Days_per_year_sea +
                               Gen_daily_oil_cons*(Days_per_year_port + Days_per_year_sea)) +
                     Cyl_oil_cost*Engine_daily_cyl_oil_cons*Days_per_year_sea)
