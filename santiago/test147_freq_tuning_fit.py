"""
Fit a Gaussian to a tuning curve.
"""

import numpy as np
from jaratoolbox import extraplots
import matplotlib.pyplot as plt


# -- Made-up data --
possibleFreq = [2000, 4000, 8000, 16000, 32000, 64000]
averageFiringRate = [2.3, 5.6, 10.1, 14.2, 8.9, 6]

possibleLogFreq = np.log2(possibleFreq)
nFreq = len(possibleLogFreq)

(fitParams, Rsquared) = extraplots.fit_tuning_curve(possibleLogFreq, averageFiringRate)

sigma = fitParams[2]
fullWidthHalfMax = extraplots.gaussian_full_width_half_max(sigma)

(pdots, pfit) = extraplots.plot_tuning_curve(possibleFreq, averageFiringRate, fitParams, xscale='log')
plt.show()

'''
plt.clf()
xvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
yvals = extraplots.gaussian(xvals, *fitParams)
plt.plot(possibleLogFreq, averageFiringRate, 'o')
plt.plot(xvals, yvals, '-', lw=3)
plt.title(f'R^2 = {Rsquared:0.4f} ,  Bandwidth = {fullWidthHalfMax:0.2f} oct')
plt.ylabel('Firing rate (Hz)')
plt.xlabel('Frequency (kHz)')
xTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
plt.xticks(possibleLogFreq, xTickLabels)
plt.show()
'''
