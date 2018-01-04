import sys
import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as stats

STUDY_NAME = '2017rc'
brainRegions = ['astr', 'ac']

modulationWindows = {'side-in':['-0.3--0.2s','-0.2--0.1s','-0.1-0s']} 
freqLabels = ['Low','High']
movementDirections = ['Left', 'Right']

qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

plt.figure(figsize=(6,6))
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
dataDir = settings.DATABASE_PATH
outputDir = '/tmp/'
figFormat = 'png'

for indRegion, brainRegion in enumerate(brainRegions):
    plt.clf()
#for animal in animalList:
    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    #celldbPath = os.path.join(dataDir, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- For mod index in different windows aligned to side-in for movement-selective cells, take the preferred direction -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    movementSel = goodQualCells.movementModS < alphaLevel
    leftPreferred = (goodQualCells.movementModI < 0) & movementSel
    rightPreferred = (goodQualCells.movementModI > 0) & movementSel
    leftPreferredCells = goodQualCells[leftPreferred]
    rightPreferredCells = goodQualCells[rightPreferred]

    
    for alignment, modWindows in modulationWindows.items():
        allModInds = np.empty([sum(movementSel), len(modWindows)])
        for indW,modWindow in enumerate(modWindows):
            lowFreqModIndName = 'modIndLow_{}_{}'.format(modWindow, alignment)
            highFreqModIndName = 'modIndHigh_{}_{}'.format(modWindow, alignment)
            thisWinModInd = np.r_[np.abs(leftPreferredCells[lowFreqModIndName]), np.abs(rightPreferredCells[highFreqModIndName])]
            allModInds[:,indW] = thisWinModInd

        for indc in range(allModInds.shape[1]):
            if indc < allModInds.shape[1]-1:
                for row in range(allModInds.shape[0]):
                    xVal = [indc, indc+1]
                    yVal = [allModInds[row, indc],allModInds[row, indc+1]]
                    plt.plot(xVal, yVal, 'o-', color='grey')
        plt.xlim([-0.5, 2.5])
        plt.xticks([0,1,2], modWindows)
        figTitle = '{}_{}_preferred_movement_direction'.format(brainRegion, alignment)
        plt.title(figTitle)
        figFullPath = os.path.join(outputDir, figTitle)
        plt.savefig(figFullPath,format=figFormat)

        plt.show()
