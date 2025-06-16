"""
Script for creating raster plot report of multiple cells from a recording session
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import re
from jaratoolbox import settings, celldatabase, loadneuropix, \
    ephyscore, extraplots, spikesanalysis, behavioranalysis

NROW = 3
NCOL = 4


studyName = 'patternedOpto'
subject,sessionDate,probeDepth,paradigm = sys.argv[1:5]
cellsToPlot = sys.argv[5] if len(sys.argv) > 5 else ''
stim = 'currentFreq'

# get data
dbPath = os.path.join(settings.DATABASE_PATH, studyName, f'celldb_{subject}.h5')

if os.path.exists(dbPath):
    celldb = celldatabase.load_hdf(dbPath)

    if not celldb['date'].isin([sessionDate]).any() :
        celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH,
                                                              f"{subject}_inforec.py"))
        
        celldatabase.save_hdf(celldb, dbPath)
        
else:
    celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH,
                                                              f"{subject}_inforec.py"))
    celldatabase.save_hdf(celldb, dbPath)


celldb = celldb.rename(columns={'info' : 'extra'})
celldb['soundLoc'] = [i[1] for i in celldb.extra]


# subset data
celldbSubset = celldb[(celldb.date==sessionDate) \
                      & (celldb.pdepth==probeDepth) \
                        & (celldb.cluster_label=='good')]

if len(celldbSubset) == 0:
    raise Exception(f"error, no cells matching {sessionDate}, {probeDepth}um")

if cellsToPlot:
    cellInds = [int(i) for i in cellsToPlot.split(',')]
else:
    cellInds = list(range(len(celldbSubset)))

firstCell = celldbSubset.iloc[0].name
sessionTimes = {}
for ind,type in enumerate(celldbSubset.iloc[0].sessionType):
    sessionTimes[type] = celldbSubset.iloc[0].ephysTime[ind]


ensemble = ephyscore.CellEnsemble(celldbSubset)


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



# get eventLocked spikes

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = {},{},{}
possibleStim,trialsEachComb,rasterTimeRange,stimDur = {},{},{},{}

ephysData,bdata = ensemble.load(paradigm)
laserEachTrial = bdata['laserTrial']
laserOnInds = np.nonzero(laserEachTrial)
laserOffInds = np.nonzero(1-laserEachTrial)

XML_PATH = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject,
                        f"{sessionDate}_{sessionTimes[paradigm]}_processed_multi",
                        "info", "settings.xml")

pmap = loadneuropix.ProbeMap(XML_PATH)
nTrials = len(bdata[stim])
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata 

stimDur[paradigm] = ephysData['events']['stimOff'][0] - ephysData['events']['stimOn'][0]

rasterTimeRange[paradigm] = (min(-0.2,-0.5*stimDur[paradigm]),
                max(0.6,1.5*stimDur[paradigm]))  # In seconds

spikeTimesFromEventOnsetAll[paradigm], trialIndexForEachSpikeAll[paradigm], indexLimitsEachTrialAll[paradigm] = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, rasterTimeRange[paradigm])

# get trials
currentStim = bdata[stim]
possibleStim[paradigm] = np.unique(currentStim)
currentLaser = bdata['laserTrial']
possibleLaser = np.unique(currentLaser)
trialsEachComb[paradigm] = behavioranalysis.find_trials_each_combination(currentStim, possibleStim[paradigm],
                                                                         currentLaser,possibleLaser)


for count, indcell in enumerate(cellInds):
    spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond = \
        spikeTimesFromEventOnsetAll[paradigm][indcell], indexLimitsEachTrialAll[paradigm][indcell], trialsEachCond[paradigm]
    
    







