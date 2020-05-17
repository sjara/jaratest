# Plot psychometric average for many mice

import os, sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp

STUDY_NAME = '2017rc'
FIGNAME = 'behavior_change'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

outputFile = 'psychometric_summary_9_mice.npz'
outputFullPath = os.path.join(dataDir,outputFile)

psycurvesData = np.load(outputFullPath)

avePsycurveMoreLeft = psycurvesData['avePsycurveMoreLeft']
avePsycurveMoreRight = psycurvesData['avePsycurveMoreRight']
possibleValues = psycurvesData['possibleFreqs']/1000.0

plt.clf()
fig = plt.gcf()
fig.set_facecolor('w')
gs = gridspec.GridSpec(1,1)
gs.update(top=0.95, bottom=0.15, left=0.16, right=0.98)
ax1 = plt.subplot(gs[0])
fontsize = 16

#plt.hold('on')
(p1,c1,b1) = plt.errorbar(x=possibleValues, y=100*np.mean(avePsycurveMoreRight,axis=0),
             yerr=100*stats.sem(avePsycurveMoreRight,axis=0), linewidth=2,linestyle='-',
             capthick=2,elinewidth=2,marker='o',ms=8,color=cp.TangoPalette['Orange2'])
(p2,c2,b2) = plt.errorbar(x=possibleValues, y=100*np.mean(avePsycurveMoreLeft,axis=0),
             yerr=100*stats.sem(avePsycurveMoreLeft,axis=0), linewidth=2,linestyle='-',
             capthick=2,elinewidth=2,marker='o',ms=8,color=cp.TangoPalette['SkyBlue2'])
plt.xlabel('Frequency (kHz)',fontsize=fontsize)
plt.ylabel('Reported HIGH freq (%)',fontsize=fontsize)
plt.axhline(y=50, color = '0.5',ls='--')
allPline = [p1,p2]

plt.ylim([0,100])
plt.xlim([possibleValues[0]/1.2,possibleValues[-1]*1.2])

xTicks = [6,11,20]
ax1.set_xscale('log')
ax1.set_xticks([], minor=True)
#sys.exit()
ax1.set_xticks(xTicks)
from matplotlib.ticker import ScalarFormatter
ax1.xaxis.set_major_formatter(ScalarFormatter())


blockLegendsHARDCODED = ['More reward HIGH','More reward LOW']
plt.legend(allPline, blockLegendsHARDCODED, loc='upper left',frameon=False, handlelength=2,
           handletextpad=0.3, fontsize=fontsize-3)
extraplots.boxoff(ax1)
extraplots.set_ticks_fontsize(plt.gca(),fontsize)

plt.show()

outputDir='/tmp/'
filename = 'behavior_summary_9_mice'
fileFormat = 'svg' 
figSize = (5,4)
extraplots.save_figure(filename, fileFormat, figSize, outputDir)
