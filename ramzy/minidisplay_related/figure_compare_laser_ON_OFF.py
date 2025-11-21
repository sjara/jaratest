"""
Compare responses during laserON and not-laserON trials.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
import scipy.stats as stats 
import poni_params as studyparams
import poni_utils as studyutils
import ponifig_params as figparams
import importlib
importlib.reload(figparams)
importlib.reload(studyutils)
importlib.reload(studyparams)

subject = sys.argv[1]
sessionDate = sys.argv[2]
probeDepth = int(sys.argv[3])

SAVE_FIGURE = 0
outputDir = os.path.join(settings.FIGURES_DATA_PATH,subject,sessionDate)
figFilename = 'plots_overall_firing' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7, 5] # In inches

if len(sys.argv)==5:
    trialSubset = sys.argv[4]
    trialSubset = sys.argv[1]
else:
    trialSubset = ''
if trialSubset not in ['', 'laserON', 'laserOFF']:
    raise ValueError("trialSubset must be '', 'laserON', or 'laserOFF'")

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.36, 0.7]   # Horiz position for panel labels
labelPosY = [0.95, 0.71]    # Vert position for panel labels


# -- Load data --
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning.h5')
condLabels = ['off','on']
celldbAll_full = celldatabase.load_hdf(dbFilename)
# celldbs = [celldatabase.load_hdf(dbFileNameOFF),
#            celldatabase.load_hdf(dbFileNameON)]

celldbAll = celldbAll_full[(celldbAll_full['sessionType'].apply(lambda x: 'Freq' in x))]

# -- Process data --
metrics = ['ToneBaselineFiringRate', 'ToneFiringRateBestFreq', 'ToneAvgEvokedFiringRate']
responsive = studyutils.find_tone_responsive_cells(celldbAll, frThreshold=5, allreagents=False)
steady = studyutils.find_steady_cells(celldbAll, metrics,maxChangeFactor=1.2)

print(np.nonzero(responsive))
print(np.nonzero(steady))
# -- Plot results --
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

# -- Main gridspec --
gsMain = gridspec.GridSpec(1,len(metrics))
gsMain.update(left=0.07, right=0.98, top=0.92, bottom=0.08, wspace=0.4, hspace=0.3)
axs = []

pColor = '0.5'

condLabels = studyparams.REAGENTS

for indm, metric in enumerate(metrics):
    thisMetricFiringAll = np.empty((len(celldbAll), len(condLabels)))
    #baselineFiring = np.empty((len(celldbAll), len(condLabels)))
    #evokedFiring = np.empty((len(celldbAll), len(condLabels)))
    for indr, reagent in enumerate(studyparams.REAGENTS):
        thisMetricFiringAll[:, indr] = celldbAll[reagent + metric]

        #thisMetricFiring = thisMetricFiring[responsive & steady, :] 
        thisMetricFiring = thisMetricFiringAll[responsive, :]  # Control
        # thisMetricFiring = thisMetricFiringAll

        axs.append(plt.subplot(gsMain[0, indm]))
        plt.axhline(0, ls='--', color='0.5', lw=1)
        plt.plot([0, 1], thisMetricFiring.T, '-', color='0.75')
        plt.plot([0, 1], thisMetricFiring.T, 'o', mec=pColor, color=pColor)
        
        medianFR = np.nanmedian(thisMetricFiring[:,indr])
        print(f'{reagent} {metric} median: {medianFR}')
        plt.plot(indr, medianFR, '_', ms=40, color='0.25')
        plt.xlim([-0.5, 1.5])
        plt.ylabel(f'{metric} (spk/s)', fontsize=fontSizeLabels)
        plt.xticks([0, 1], condLabels, fontsize=fontSizeTicks)
        if indr%2:
            wstat1, pVal1 = stats.wilcoxon(thisMetricFiring[:,0], thisMetricFiring[:,1])
        #wstat2, pVal2 = stats.wilcoxon(thisMetricFiring[:,1], thisMetricFiring[:,2])
            plt.text(0.5, 0.95, f'p = {pVal1:0.3f}', transform=axs[-1].transAxes, ha='center',
                 fontsize=fontSizeLabels)
        #plt.text(0.66, 0.95, f'p = {pVal2:0.3f}', transform=axs[-1].transAxes, ha='center',
        #         fontsize=fontSizeLabels)
        #plt.title(f'{cstim} (N={nCellsThisStim})', fontsize=fontSizeLabels)
        plt.title(f'{reagent}  (N = {len(thisMetricFiring)})', fontsize=fontSizeLabels)

plt.show()

sys.exit()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
