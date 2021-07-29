"""
Exercise to plot: https://matplotlib.org/stable/_images/sphx_glr_subplot_001.png
"""

import numpy as np
import matplotlib.pyplot as plt

print("Plot 2")
x = np.linspace(0.0, 5.0) # fixes sample rate. Former line used x = np.arange(0, 5, 0.005)
y = np.sin(x * np.pi * 2) * np.exp(-x)
w = np.linspace(0.0, 2.0)
z = np.cos(w * np.pi * 2)/2
fig, (gr1, gr2) = plt.subplots(2, sharey =True)
gr1.plot(x, y, '-o', markersize = 5)
gr1.set(title = 'A tale of 2 subplots', ylabel = 'Damped oscillation')
gr2.plot(w, z, '-o', markersize = 2.5)
gr2.set(xlabel = 'time (s)', ylabel ='Undamped')
plt.show(gr1, gr2)
