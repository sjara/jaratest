'''
Figure showing performance in signal extraction task with inactivation (of AC or specific cells).
'''

import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import pandas as pd
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'


#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)
modelDataDir = './modeldata'

modelDataFiles = ['SSNSignalExtraction-Poiss-8OctBWnoise-2.csv',
                  'SSNSignalExtraction-Poiss-1OctBWnoise-2.csv']
titleEachPanel = ['White noise background', '1 oct noise background']

# -- Columns are --
# "SNR (dB)", "% right (control)", "% right (SOM silenced)", and  "% right (PV silenced)"


#PANELS_TO_PLOT = [0,0,1]  # [Experimental, Model]

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'model_behavior' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [12,4]

fontSizeLabels = 14 #12
fontSizeTicks = 12 #10
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels


#colors = ['k', cp.TangoPalette['ScarletRed1'], cp.TangoPalette['Chameleon3']]
colors = [cp.TangoPalette['ScarletRed1'], cp.TangoPalette['Chameleon3'], 'k']
#colors = ['k', 'm', cp.TangoPalette['Chameleon3']]
#edgeColors = [cp.TangoPalette['ScarletRed1'], cp.TangoPalette['Chameleon3'], 'k']


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3)
#gs.update(top=0.9, left=0.08, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25)
gs.update(top=0.9, left=0.06, bottom=0.15, right=0.99, wspace=0.25, hspace=0.25)

#axEach = []
modelPerfEach = []
for BWcond in [0,1]:
    ax1 = plt.subplot(gs[0,BWcond])
    modelData = pd.read_csv(os.path.join(modelDataDir,modelDataFiles[BWcond]))
    modelPerf = [modelData['NoSOM(percentRight)'], modelData['NoPV(percentRight)'], modelData['Control(percentRight)']]
    modelPerfEach.append(modelPerf)
    modelSNR = modelData['SNR(dB)']
    modelSNR[0] = -4 # FIXME: HARDCODED
    pHandles = []
    for indc,thisPerf in enumerate(modelPerf):
        #thisPlot, = plt.plot(np.arange(len(modelSNR)), thisPerf, marker='o', color=colors[indc], mec='none', lw=3, ms=10, clip_on=False)
        if indc==0:
            thisPlot, = plt.plot(modelSNR, thisPerf, marker='o', color=colors[indc], mfc='w', mec=colors[indc], lw=3, mew=3, ms=10, clip_on=False)
        elif indc==10:
            thisPlot, = plt.plot(modelSNR, thisPerf, marker='s', color=colors[indc], mfc='w', mec=colors[indc], lw=3, mew=3, ms=10, clip_on=False)
        else:
            thisPlot, = plt.plot(modelSNR, thisPerf, marker='o', color=colors[indc], mec='none', lw=3, ms=10, clip_on=False)
        pHandles.append(thisPlot)
    extraplots.boxoff(ax1)
    #plt.xticks(np.arange(len(modelSNR)), modelSNR)
    #plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
    plt.ylabel('Signal detection rate (%)', fontsize=fontSizeLabels)
    plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
    #plt.xlim([-0.2, len(modelSNR)-1+0.2])
    plt.ylim((0,100))
    plt.legend(pHandles,['No SOM+','No PV+','Control'], loc='lower right', numpoints=1, markerscale=1, handlelength=1.5, frameon=False)
    #plt.title(titleEachPanel[BWcond],fontsize=fontSizeLabels)
    #origXtickLabels = ax1.get_xticklabels()
    #origXtickLabels[0]='-inf'
    origXtickLabels = ['-inf','0','5','10','15','20'] ### UGLY, but I have to submit tomorrow!
    ax1.set_xticklabels(origXtickLabels)

# -- Average error rates --
axBars = plt.subplot(gs[0,2])
indSOM, indPV, indControl = [0,1,2]
for BWcond in [0,1]:
    modelPerf = modelPerfEach[BWcond]
    errorRateControl = (modelPerf[indControl][0] + 100-np.mean(modelPerf[indControl][1:])) / 2.0
    errorRateSOM =  (modelPerf[indSOM][0] + 100-np.mean(modelPerf[indSOM][1:])) / 2.0
    errorRatePV =  (modelPerf[indPV][0] + 100-np.mean(modelPerf[indPV][1:])) / 2.0
    plt.bar(1+BWcond*1, errorRateSOM-errorRateControl, color=colors[0], ec='none', align='center')
    plt.bar(4+BWcond*1, errorRatePV-errorRateControl, color=colors[1], ec='none', align='center')

extraplots.boxoff(axBars)    
plt.ylabel('Change in error rate\n(% inactivation - % control)', fontsize=fontSizeLabels)
plt.xticks(rotation=40)
axBars.set_xticks([1,2,4,5])
axBars.set_xticklabels(['Broad','Narrow','Broad','Narrow'], fontsize=fontSizeLabels)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
