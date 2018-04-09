import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import pandas as pd
from matplotlib import pyplot as plt

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# soundResponsive = db.query('isiViolations<0.02 and spikeShapeQuality>2 and noisePval<0.05')
thal = db.groupby('brainArea').get_group('rightThal')
dataframe = thal[thal['taggedCond']==0]

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    failed=False
    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)
        noTCinds.append(indRow)
        #NOTE: If the cell has no TC data we actually don't need to do anything
        #because the arrays are filled with NaN by default
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

    #Init list to hold the optimized parameters for the gaussian for each intensity
    popts = []
    Rsquareds = []

    #Init arrays to hold the baseline and response spike counts per condition
    allIntenBase = np.array([])
    allIntenResp = np.empty((len(possibleIntensity), len(possibleFreq)))
    allIntenRespMedian = np.empty((len(possibleIntensity), len(possibleFreq)))
    allIntenPval = np.empty((len(possibleIntensity), len(possibleFreq)))

    for indinten, inten in enumerate(possibleIntensity):
        spks = np.array([])
        freqs = np.array([])
        base = np.array([])
        for indfreq, freq in enumerate(possibleFreq):
            selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
            selectedOnsetTimes = eventOnsetTimes[selectinds]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                        selectedOnsetTimes,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)

            base = nspkBase.ravel()
            resp = nspkResp.ravel()

            zScore, pVal = stats.ranksums(base, resp)

            allIntenPval[indinten, indfreq] = pVal

            # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
            freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])
            allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])
            allIntenResp[indinten, indfreq] = np.mean(nspkResp)
            allIntenRespMedian[indinten, indfreq] = np.median(nspkResp)

    alpha = 0.05/(len(possibleIntensity)*len(possibleFreq))
    #plt.clf()
    #plt.imshow(allIntenPval<alpha, interpolation='none', cmap='Reds')
    #plt.show()
    print sum(allIntenPval<alpha)

