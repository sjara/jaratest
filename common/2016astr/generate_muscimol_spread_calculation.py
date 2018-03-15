import numpy as np
from scipy.constants import Avogadro
from matplotlib import pyplot as plt

'''
References:

Equation for concentration at a certain radius and time from a point source:
http://sites.sinauer.com/animalcommunication2e/chapter06.04.html

Constants for muscimol:
Edeline et al. Muscimol Diffusion after Intracerebral Microinjections: A Reevaluation Based on Electrophysiological and Autoradiographic Quantifications.
'''

D = 1e-5 #10**-5 cm**2/sec (from Edeline, estimate based on )
#1 cm**2/sec = 100 mm**2/sec
D_mm = 100*D

dim = 3

def concentration(rad, t, Q, D, dim):
    '''
    Calculate concentration of molecules per volume/area at a specific distance and time

    rad: distance (radius) from the point source
    t: time
    Q: number of molecules released
    D: Diffusion constant (units of area/volume per time)
    dim: dimensionality - 1 for 1D, 2 for 2D, 3 for 3D
    '''
    return (Q/((4*np.pi*D*t)**(dim/2.)))*np.exp((-1*rad**2)/(4*D*t))

Xdists = np.linspace(0, 5) #0 to 5 mm
Yconc = np.empty(len(Xdists))

# t = 10 #seconds
t = 37*60 #30 min

conc = 0.25 #ng/nl
vol = 45 #nl/hemi
mW = 114.10 #g/nol

def num_molecules(conc, vol, mW):
    weightInjected = conc*vol
    molsInjected = weightInjected/mW
    return molsInjected

#Input concentration and volume in nano-units
nanoMols = num_molecules(conc, vol, mW)
mols = nanoMols*1e-9
Q_1 = mols * Avogadro
Q_2 = mols * 4 * Avogadro

Yconc_1 = concentration(Xdists, t, Q_1, D_mm, dim)
Yconc_2 = concentration(Xdists, t, Q_2, D_mm, dim)

plt.clf()
plt.plot(Xdists, Yconc_1, 'g.-')
plt.hold(1)
plt.plot(Xdists, Yconc_2, 'r.-')
plt.xlabel('Radius from source, mm')
plt.ylabel('molecules/mm**3')
plt.axhline(y=4e11)
# plt.axhline(y=0.25e12)
plt.show()



#We injected 0.098e-9 mol/hemisphere (0.098 nmol/hemi)
# Q = 0.098e-9 * Avogadro
# for indD, dist in enumerate(Xdists):
#     Yconc[indD] = concentration(dist, t, Q, D_mm, dim)
