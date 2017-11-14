'''
Testing a plot with significance stars
'''

from jaratoolbox import extraplots
reload(extraplots)
import numpy as np
from matplotlib import pyplot as plt

plt.clf()
plt.bar([0,1],[2,3], color='0.5', align='center')
extraplots.significance_stars([0,1], 4, 0.2, starSize=10, gapFactor=0.1)

plt.xlim([-1,2])
plt.ylim([0,5])
plt.show()
