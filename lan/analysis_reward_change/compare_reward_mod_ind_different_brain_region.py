'''
This script plots modulation index histogram in different windows:
0-0.1 sec after sound-onset or 0.05-0.25 sec after center-out.
To use in IPython console: 'run plot_reward_mod_ind_histogram_diff_window.py sound' or 'run plot_reward_mod_ind_histogram_diff_window.py center-out'
'''
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
#animalList = ['adap005', 'adap012', 'adap013', 'adap015', 'adap017'] #['gosi001','gosi004','gosi008','gosi010','adap067','adap071']

modulationWindows = {'sound':'0-0.1s',
                     'center-out': '0.05-0.25s'}
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

modIndGroups = []
sigModIndGroups = []
allFractions = []

if len(sys.argv) == 1:
    print 'Please provide which alignment you want to compare modulation index with: sound or center-out'
elif len( sys.argv) == 2:
    alignment = sys.argv[1]

for indRegion, brainRegion in enumerate(brainRegions):
#for animal in animalList:
    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    #celldbPath = os.path.join(dataDir, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- For histogram of modulation index for sound-responsive cells, take the most responsive frequency -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))

    soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x)) >=  maxZThreshold) #The bigger of the sound Z score is over threshold
    moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[0]) > abs(x[1]))
    moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[1]) > abs(x[0]))
    goodLowFreqRespCells = goodQualCells[moreRespLowFreq]
    goodHighFreqRespCells = goodQualCells[moreRespHighFreq]

    # -- For histogram of modulation index for movement-selective cells, take the preferred movement direction -- #
    movementSelective = goodQualCells.movementModS < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells.movementModI < 0)
    moreRespMoveRight = movementSelective & (goodQualCells.movementModI > 0)
    goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
    goodRightMovementSelCells = goodQualCells[moreRespMoveRight]
 
    if alignment == 'sound':
        modWindow = modulationWindows['sound']
        lowFreqModIndName = 'modIndLow_'+modWindow+'_'+'sound'
        lowFreqModSigName = 'modSigLow_'+modWindow+'_'+'sound'
        highFreqModIndName = 'modIndHigh_'+modWindow+'_'+'sound'
        highFreqModSigName = 'modSigHigh_'+modWindow+'_'+'sound'

        goodLowFreqRespModInd = (-1) * goodLowFreqRespCells[lowFreqModIndName]
        goodLowFreqRespModSig = goodLowFreqRespCells[lowFreqModSigName]
        goodHighFreqRespModInd = goodHighFreqRespCells[highFreqModIndName]
        goodHighFreqRespModSig = goodHighFreqRespCells[highFreqModSigName]
        sigModulatedLow = goodLowFreqRespModSig < alphaLevel
        sigModulatedHigh = goodHighFreqRespModSig < alphaLevel
        sigModI = np.concatenate((goodLowFreqRespModInd[sigModulatedLow].values,
                                  goodHighFreqRespModInd[sigModulatedHigh].values))
        nonsigModI = np.concatenate((goodLowFreqRespModInd[~sigModulatedLow].values,
                                  goodHighFreqRespModInd[~sigModulatedHigh].values))

        
    # -- reward modulation during movement only for movement-selective cells -- #
    elif alignment == 'center-out':
        modWindow = modulationWindows['center-out']
        leftModIndName = 'modIndLow_'+modWindow+'_'+'center-out'
        leftModSigName = 'modSigLow_'+modWindow+'_'+'center-out'
        rightModIndName = 'modIndHigh_'+modWindow+'_'+'center-out'
        rightModSigName = 'modSigHigh_'+modWindow+'_'+'center-out'

        goodMovementSelCells = goodQualCells[movementSelective]
        sigModEitherDirection = (goodMovementSelCells[leftModSigName] < alphaLevel) | (goodMovementSelCells[rightModSigName] < alphaLevel)  
        #print 'Out of {} movement-selective cells, {} were modulated by reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection))
        goodLeftMovementSelModInd = (-1) * goodLeftMovementSelCells[leftModIndName]
        goodLeftMovementSelModSig = goodLeftMovementSelCells[leftModSigName]
        goodRightMovementSelModInd = goodRightMovementSelCells[rightModIndName]
        goodRightMovementSelModSig = goodRightMovementSelCells[rightModSigName]
        sigModulatedLeft = goodLeftMovementSelModSig < alphaLevel
        sigModulatedRight = goodRightMovementSelModSig < alphaLevel
        sigModI = np.concatenate((goodLeftMovementSelModInd[sigModulatedLeft].values,
                                  goodRightMovementSelModInd[sigModulatedRight].values))
        nonsigModI = np.concatenate((goodLeftMovementSelModInd[~sigModulatedLeft].values,
                                     goodRightMovementSelModInd[~sigModulatedRight].values))

    fractionMod = [len(sigModI), len(nonsigModI)] #This is a list containing the number of sig modulated cells and the number of non-modulated cells
    allFractions.append(fractionMod)
    allModI = np.concatenate((sigModI, nonsigModI))
    Z, pVal = stats.wilcoxon(allModI)
    print '{} population mod ind mean: {:.2E}, compared to zero p value: {:.3E}'.format(brainRegion, np.mean(allModI), pVal)
    modIndGroups.append(allModI)
    sigModIndGroups.append(sigModI)


# -- Stats -- #
T, pVal = stats.ranksums(*modIndGroups)
print 'For {} window aligned to {}, comparing all modulation indices from AC vs AStr using rank sum test, p = {:.3E}'.format(modWindow, alignment, pVal)

T, pVal = stats.ranksums(*sigModIndGroups)
print 'For {} window aligned to {}, comparing all significant modulation indices from AC vs AStr using rank sum test, p = {:.3E}'.format(modWindow, alignment, pVal)

oddsratio, pValue = stats.fisher_exact(allFractions)
print 'Using Fisher exact test to compare fraction of modulated cells for the two regions, p = {:.3E}'.format(pValue)

