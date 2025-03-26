"""
Show raster plots of neurons in response to natural sounds.

 Feat015 2024-03-20 2413um
 feat015 2024-03-20 2413
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import loadneuropix
from jaratoolbox import extraplots
from importlib import reload
reload(celldatabase)
reload(loadneuropix)


SAVE_FIGS = 1
outputDir = '/data/reports/arch013'

SESSIONID = 0
if SESSIONID == 0:
    subject = 'arch013'
    sessionDate = '2024-10-23'
    probeDepth = 3780
if SESSIONID == 0:
    subject = 'arch013'
    sessionDate = '2024-10-23'
    probeDepth = 4500
if SESSIONID == 99:
    subject = 'test143'
    sessionDate = '2024-07-19'
    probeDepth = 2280

    
if 1:
    inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
    #inforecFile = inforecFile.replace('.py','.test.py')
    celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True)


# -- Load the data --
celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth)]

ensemble = ephyscore.CellEnsemble(celldbSubset)

CASE = 1
caseStr = ['AM', 'NatCateg']
if CASE==0:
    ephysData, bdata = ensemble.load('optoTuningAM')
    currentStim = bdata['currentFreq']
    timeRange = [-0.5, 1]  # In seconds
elif CASE==1:
    ephysData, bdata = ensemble.load('optoNaturalCategories')
    currentStim = bdata['soundID']
    #timeRange = [-6, 10]  # In seconds
    timeRange = [-2, 6]  # In seconds
elif CASE==2:
    ephysData, bdata = ensemble.load('pureTones')
    currentStim = bdata['currentFreq']
    timeRange = [-0.5, 1]  # In seconds
sessionLabel = caseStr[CASE]

#nTrials = len(bdata['timeTrialStart'])
nTrials = len(currentStim)
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata 

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

possibleStim = np.unique(currentStim)
#possibleStim = np.arange(4)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it

condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

# -- Plot rasters --
nCells = len(celldbSubset)
nRows = 4
nCols = 7
nPages = int(np.ceil(nCells/(nRows*nCols)))
fig = plt.gcf()
figSize = [25, 12.8]
fig.set_size_inches(figSize)
for indpage in range(nPages):
    plt.clf()
    someCells = np.arange(0, nRows*nCols) + indpage*nRows*nCols
    for count, indcell in enumerate(someCells):
        if indcell >= len(celldbSubset):
            break
        sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
        plt.subplot(nRows, nCols, count+1)
        plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
        plt.xlabel('Time (s)')
        plt.ylabel(f'[{indcell}] Sorted trials')
        #recSiteName = studyutils.simplify_site_name(celldbSubset.iloc[indcell].recordingSiteName)
        #plt.title(f'{recSiteName}')
    plt.suptitle(f'{subject} {sessionDate} {probeDepth}um {sessionLabel} ({indpage+1}/{nPages})',
                 fontweight='bold')
    plt.tight_layout()
    plt.show()
    #plt.waitforbuttonpress()

    if SAVE_FIGS:
        figFilename = f'{subject}_{sessionLabel}_{sessionDate}_{probeDepth}um_{indpage+1:02d}'
        extraplots.save_figure(figFilename, 'png', figSize, outputDir=outputDir, facecolor='w')

        
if 0:
    # -- Plot subset --
    #someCells = [21, 61, 10, 237, 88, 248, 5, 266] # AM
    #someCells = [77, 123, 114, 155, 146, 190, 177, 222, 212, 271] # Natural sounds
    someCells = [222, 212, 123, 271, 146, 177]
    plt.clf()
    for count, indcell in enumerate(someCells):
        sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
        #plt.subplot(2, 4, count+1)
        plt.subplot(2, 3, count+1)
        plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
        plt.xlabel('Time (s)')
        plt.ylabel(f'[{indcell}] Sorted trials')
    plt.suptitle(f'{subject} {sessionDate} {probeDepth}um ({caseStr[CASE]})')
    plt.tight_layout()
    plt.show()
    extraplots.save_figure(f'{subject}_{sessionDate}_{probeDepth}um_rasters_{caseStr[CASE]}_new', 'png',
                           [14, 7], facecolor='w', outputDir='/tmp/')
