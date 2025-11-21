"""
This script plots changes in freq tuning from off to on.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings,celldatabase,extraplots,ephyscore,spikesanalysis,behavioranalysis,loadneuropix
import scipy.stats as stats 
import poni_params as studyparams
import poni_utils as studyutils
import ponifig_params as figparams
import importlib
importlib.reload(figparams)
importlib.reload(studyutils)
importlib.reload(studyparams)

pd.set_option('mode.chained_assignment', None)
sessionType = 'poniSpont'
NROW = 1
NCOL = 4

subject = sys.argv[1]
sessionDate = sys.argv[2]
probeDepth = int(sys.argv[3])

SAVE_FIGURE = 1
SAVE=0
studyName = 'patternedOpto'
paradigm = 'poniSpont'
outputDir = os.path.join(settings.FIGURES_DATA_PATH,studyName,subject,sessionDate)
figFilename = f'plots_spont_PSTH' # Do not include extension
figFormat = 'jpg' # 'pdf' or 'svg'
figSize = [16, 8] # In inches

# create folders in figures directory if not already present
studyFolder = os.path.join(settings.FIGURES_DATA_PATH,studyName)
subjectFolder = os.path.join(studyFolder,subject)
sessionFolder = os.path.join(subjectFolder,sessionDate)
siteFolder = os.path.join(sessionFolder, str(probeDepth)+'um')
outFolder = os.path.join(siteFolder,paradigm)

if not os.path.exists(studyFolder):
    os.mkdir(studyFolder)                   # folder for this study (just the figures directory if no studyName)
if not os.path.exists(subjectFolder):
    os.mkdir(subjectFolder)                 # folder for this subject
if not os.path.exists(sessionFolder):
    os.mkdir(sessionFolder)                 # folder for this session
if not os.path.exists(siteFolder):
    os.mkdir(siteFolder)                    # folder for this site
if not os.path.exists(outFolder):
        os.mkdir(outFolder)                # output folder

# -- Load data --
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,f'celldb_{subject}.h5')
celldbAll = celldatabase.load_hdf(dbFilename)

celldb = celldbAll[(celldbAll.date==sessionDate) & 
                   (celldbAll.pdepth==probeDepth)]

firstCell = celldb.iloc[0].name
sessionTime = celldb.iloc[0].ephysTime[0]

XML_PATH = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject,
                            f"{sessionDate}_{sessionTime}_processed_multi",
                            "info", "settings.xml")

pmap = loadneuropix.ProbeMap(XML_PATH)


ensemble = ephyscore.CellEnsemble(celldb)
ephysData, bdata = ensemble.load(sessionType)

tileEachTrial = np.array([f"C{i}R{j}" for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
possibleTile = np.unique(tileEachTrial)

trialsEachCond = behavioranalysis.find_trials_each_type(tileEachTrial,possibleTile)

nTrials = len(tileEachTrial)
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials]# Ignore trials not in bdata 
nCell = len(celldb)
cellInds = list(range(nCell))
stimDur = ephysData['events']['stimOff'][0] - ephysData['events']['stimOn'][0]

timeRange = [-0.2, 0.5]  # In seconds

spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

binSize = 0.1
binEdges = np.arange(timeRange[0], timeRange[1], binSize)
spikeCount = ensemble.spiketimes_to_spikecounts(binEdges)  # The shape is (nCells, nTrials, nBins)
print(spikeCount.shape)
print(trialsEachCond.shape)
sortedSpikeCount = spikeCount[:,sortingInds,:]

cellsPerPage = NROW*NCOL
numcells = len(cellInds)
numpages = int(np.ceil(numcells/cellsPerPage))
numdigits = len(str(numpages))

nCond = trialsEachCond.shape[1]
dims = (6*NCOL,12*NROW)

for page in range(numpages):
    filename = f"{subject}_{sessionDate}_{probeDepth}_{paradigm}_{(page+1):02d}.png"
    
    if numpages > 1:
        figname = f"{subject} {sessionDate} {probeDepth} {paradigm} {page+1}/{numpages}"
    else:
        figname = f"{subject} {sessionDate} {probeDepth} {paradigm}"

    
    fig = plt.figure(1,figsize=dims)
    # plot cells for current page
    for count, indcell in enumerate(cellInds[page*cellsPerPage:(page+1)*cellsPerPage]):
        plt.subplot(NROW, NCOL, count+1)
        # for indcond, trialsThisCond in enumerate(trialsEachCond.T):
            # thisCond = possibleTile[indcond]
            # PSTH = spikeCount[indcell, trialsThisCond[0], :].mean(axis=0)
            # plt.subplot(NROW*nCond, NCOL, count+1+nCond-indcond)
            # plt.axis(False)
            # plt.plot(PSTH,label=thisCond,color=figparams.colors[thisCond])
            # plt.ylabel('Spike Count')
            # plt.xlabel('Time bin')

        nTrials = trialsEachCond.shape[0]
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset[indcell], 
                                                        indexLimitsEachTrial[indcell],
                                                        timeRange, trialsEachCond, 
                                                        labels=possibleTile)
        plt.setp(pRaster, ms=2)
        

        # sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike[indcell]]
        # plt.plot(spikeTimesFromEventOnset[indcell], sortedIndexForEachSpike, '.k', ms=2)
        # plt.axvline(0,color='0.75',zorder=-10)
        # plt.ylim(0,nTrials)
        # plt.yticks(np.arange(0,nTrials,24),
        #    possibleTile[condEachSortedTrial[0:nTrials:24]])
        

        plt.axvline(stimDur, color='0.75', zorder=-10)
        plt.xlabel('Time (s)')
        plt.ylabel('ScreenPosition')

        curr_loc = celldb.iloc[indcell]
        curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
        curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
        plt.title(f"Good Cell #{curr_loc.name - firstCell}\n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")

    plt.suptitle(figname)
    plt.tight_layout()

    # save and close current page/fig
    plt.savefig(os.path.join(outFolder,filename))
    plt.close(1)



    