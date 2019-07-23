import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
import pandas as pd
import matplotlib.pyplot as plt

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
db = pd.read_hdf(dbPath, key='dataframe')

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    failed=False
    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)
        noTCinds.append(indRow)
        #NOTE: If the cell has no TC data we actually don't need to do anything because the arrays are filled with NaN by default
        # thresholds[indIter] = None
        # cfs[indIter] = None
        # lowerFreqs[indIter] = None
        # upperFreqs[indIter] = None
        continue #Move on to the next cell

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimes = ephysData['spikeTimes']

    # HARDCODED baseline and response ranges here
    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachFreq,
                                                   labels=freqLabels)
