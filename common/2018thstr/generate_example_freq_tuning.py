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

FIGNAME = 'figure_frequency_tuning'

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
db = pd.read_hdf(dbPath, key='dataframe')

examples = {}
# examples.update({'AC1' : 'pinp016_2017-03-09_1904_6_6'})
# examples.update({'AC2' : 'pinp017_2017-03-22_1143_6_5'})
examples.update({'AC0':'pinp016_2017-03-09_1904.0_TT6c6'})

#Thalamus
# 'pinp015_2017-02-15_3110_7_3'
# 'pinp016_2017-03-16_3800_3_6'

examples.update({'Thal0' : 'pinp026_2017-11-16_3256.0_TT6c3'})
examples.update({'Thal1' : 'pinp017_2017-03-28_3074.0_TT2c4'})
examples.update({'Thal2' : 'pinp026_2017-11-16_3046.0_TT4c2'})

exampleList = [val for key, val in examples.iteritems()]
exampleKeys = [key for key, val in examples.iteritems()]

exampleSpikeData = {}

for exampleInd, cellName in enumerate(exampleList):

    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

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
            base = np.concatenate([base, nspkBase.ravel()])
            spks = np.concatenate([spks, nspkResp.ravel()])
            # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
            freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])
            allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])
            allIntenResp[indinten, indfreq] = np.mean(nspkResp)

    ### ----- Save the example cells out to an NPZ ---- ###
    exampleSpikeData.update({exampleKeys[exampleInd]:allIntenResp})

exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
np.savez(exampleDataPath, **exampleSpikeData)
