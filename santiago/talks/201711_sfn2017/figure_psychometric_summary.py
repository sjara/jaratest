# Plot psychometric average for many mice

import os
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

fontsize = 12
plt.clf()
plt.errorbar(x=range(1,9), y=np.mean(avePsycurveMoreLeft,axis=0),
             yerr=stats.sem(avePsycurveMoreLeft,axis=0), linewidth=3,linestyle='-',
             capthick=2,elinewidth=2,marker='o',ms=8,color=cp.TangoPalette['ScarletRed1'])
plt.hold(True)
plt.errorbar(x=range(1,9), y=np.mean(avePsycurveMoreRight,axis=0),
             yerr=stats.sem(avePsycurveMoreRight,axis=0), linewidth=3,linestyle='-',
             capthick=2,elinewidth=2,marker='o',ms=8,color=cp.TangoPalette['SkyBlue2'])
plt.xlabel('Frequency (kHz)',fontsize=fontsize)
plt.ylabel('Proportion of rightward choice',fontsize=fontsize)
plt.ylim((-0.1,1.1))
extraplots.set_ticks_fontsize(plt.gca(),fontsize)
plt.show()
