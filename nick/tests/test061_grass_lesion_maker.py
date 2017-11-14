import numpy as np
from matplotlib import pyplot as plt

setting = np.array([5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 93])
Vpk = np.array([0.24, 1.6, 3.2, 4.4, 5.6, 7.2, 9.0, 11.2, 15.8, 22.0, 22.0])

R = 1000.0

Ipk = Vpk/R

ma_pk = Ipk*1000.0

plt.clf()
plt.plot(setting, ma_pk, '-o')
plt.show()

plt.ylabel('Peak Current (ma)')
plt.xlabel('Setting')
