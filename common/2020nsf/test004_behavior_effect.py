"""
Plot summary of behavior effect in humans when comparing
active+active vs active+passive, etc
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import extraplots

np.random.seed(3)

dataFilename = './data_human_behavior.txt'

dframe = pd.read_csv(dataFilename, sep='\t')

dataBySchedule = dframe.groupby('Schedule')
#schedLabels = {'Act':'AA', 'AP':'AP', 'Pass':'PP', 'SA':'A_'}
schedMapping = {'Act':0, 'AP':1, 'Pass':2, 'SA':3}
schedSorted = ['AA', 'AP', 'PP', 'Ax'] # Because dicts don't always return keys sorted (pre Py3)
nSched = len(schedMapping)
#featureToPlot = 'Difference'
#featureToPlot = 'Day1pre'
featureToPlot = 'Day2post'

plt.clf()
ax0 = plt.gca()

for schedName, schedData in dataBySchedule:
    #print(schedData)
    #print(schedName)
    nSamplesThisSched = len(schedData)
    xvals = np.tile(schedMapping[schedName],nSamplesThisSched) + 0.1*np.random.rand(nSamplesThisSched)
    plt.plot(xvals, schedData[featureToPlot], 'o', mfc='none')

plt.ylabel(featureToPlot)
ax0.set_xticks(np.arange(nSched))
ax0.set_xticklabels(schedSorted)
if featureToPlot == 'Difference':
    plt.ylim([-20,50])
else:
    plt.ylim([50,100]) 
plt.show()
    
SAVEFIG = 0
if SAVEFIG:
    figname = 'behavior_effect_{}'.format(featureToPlot)
    extraplots.save_figure(figname, 'png', [5, 3.5], facecolor='w', outputDir='/tmp/')

