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

modulationWindows = {'side-in':['-0.2--0.1s','-0.1-0s',]} #'-0.3--0.2s'
freqLabels = ['Low','High']
movementDirections = ['Left', 'Right']

qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

plt.figure(figsize=(6,6))
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
outputDir = '/tmp/'
figFormat = 'png'

for indRegion, brainRegion in enumerate(brainRegions):
#for animal in animalList:
    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    #celldbPath = os.path.join(dataDir, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- For histogram of modulation index for sound-responsive cells, take the most responsive frequency -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    lowFreqModIndCols = []
    highFreqModIndCols = []
    lowFreqModSigCols = []
    highFreqModSigCols = []
    plt.clf()
    for alignment, modWindows in modulationWindows.items():
        for modWindow in modWindows:
            lowFreqModIndName = 'modIndLow_'+modWindow+'_'+alignment
            lowFreqModSigName = 'modSigLow_'+modWindow+'_'+alignment
            highFreqModIndName = 'modIndHigh_'+modWindow+'_'+alignment
            highFreqModSigName = 'modSigHigh_'+modWindow+'_'+alignment
            lowFreqModIndCols.append(lowFreqModIndName)
            highFreqModIndCols.append(highFreqModIndName)
            lowFreqModSigCols.append(lowFreqModSigName)
            highFreqModSigCols.append(highFreqModSigName)

        lowFreqModInds = goodQualCells[lowFreqModIndCols].values
        lowFreqModSigs = goodQualCells[lowFreqModSigCols].values < alphaLevel
        highFreqModInds = goodQualCells[highFreqModIndCols].values 
        highFreqModSigs = goodQualCells[highFreqModSigCols].values < alphaLevel
        
        for indc in range(lowFreqModInds.shape[1]):
            if indc < lowFreqModInds.shape[1]-1:
                for row in range(lowFreqModInds.shape[0]):
                    xVal = [indc, indc+1]
                    yVal = [lowFreqModInds[row, indc],lowFreqModInds[row, indc+1]]
                    plt.plot(xVal, yVal, 'o-', color='grey')

        plt.show()
