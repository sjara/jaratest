"""
Exercise to plot: https://matplotlib.org/stable/_images/sphx_glr_simple_plot_001.png
"""

import numpy as np
import matplotlib.pyplot as plt

print("Plot 1")
print()
x = np.linspace(0.0,2.0) #Thinking about plt.xlim(inferior limit, superior limit). Applied to both axis. Same results?
y = np.sin(x * np.pi * 2) + 1
plt.title('About as simple as it gets, folks')
plt.xlabel('time')
plt.ylabel('Voltage mV')
plt.grid(b=True)
plt.plot(x,y)
