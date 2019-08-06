import numpy as np
from numpy import inf
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
import pandas as pd
import figparams #TODO: Remove this once we move plotting code to a figure file
import matplotlib.pyplot as plt
from scipy import stats
from scipy import optimize
import ipdb

dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'
database = celldatabase.load_hdf(dbPath)

goodISI = database.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
goodNSpikes = goodLaser.query('nSpikes>2000')

db = goodNSpikes

# plt.clf()
# ax0 = plt.subplot(121)
# ax0 = plt.subplot(111)
# ax1 = plt.subplot(122)

mono = []
maxSpikes = []

goodFit = db.query('rsquaredFit > 0.04')
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')
goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')

## Functions for fitting method
def split_gaussian(l, a, mu, sigLow, sigHigh, cLow, cHigh):
    '''
    a: amplitude
    mu: best level
    sigLow: low sound level variance
    sigHigh: high sound level variance
    cLow: low sound level offset
    cHigh: high sound level offset
    '''
    if l<=mu:
        return a * np.exp(-1*((l-mu)**2/(2*sigLow**2))) + cLow
    elif l>mu:
        return a * np.exp(-1*((l-mu)**2/(2*sigHigh**2))) + cHigh
    # To fit: optimize.curve_fit(split_gaussian, levels, spks, p0, bounds)

## -- Monotonicity with respect to level -- ##

dbToUse = goodFitToUseNSpikes.iloc[:3]
for indIter, (indRow, dbRow) in enumerate(dbToUse.iterrows()):
    print indRow
    failed=False
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimes = ephysData['spikeTimes']
    freqEachTrial = bdata['currentFreq']
    if len(eventOnsetTimes) != len(freqEachTrial):
        eventOnsetTimes = eventOnsetTimes[:-1]
        if len(eventOnsetTimes) != len(freqEachTrial):
            raise ValueError("The trials still don't line up")

    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    cfTrials = freqEachTrial==dbRow['cf']
    eventsThisFreq = eventOnsetTimes[cfTrials]
    intenThisFreq = intensityEachTrial[cfTrials]

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventsThisFreq,
                                                                alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    nspkBase = nspkBase.ravel()
    nspkResp = nspkResp.ravel()
    ipdb.set_trace()

    #TODO: Make sure that intenThisFreq and nspkResp are in the correct shape for the fxn

    #TODO: Figure out reasonable starting points and bounds
    #p0 = [a      mu     sigLow     sigHigh     cLow     cHigh]
    possibleInten = np.unique(intenThisFreq)

    p0=[1, , 1, possibleInten[-1], 0, 0, 0, 0],
    bounds=([0, possibleInten[0], 0, 0, 0, 0],
            [inf, possibleInten[-1], inf, inf, inf, inf])

    popt, pcov = optimize.curve_fit(split_gaussian, intenThisFreq, nspkResp, p0, bounds)

    ipdb.set_trace()


## FOR PLOTTING
#     if len(meanSpikesAllInten)>10:
#         # ax0.plot(meanSpikesAllInten, 'k-', alpha=0.3)
#         ax0.plot(meanSpikesAllInten/max(meanSpikesAllInten).astype(float), 'k-', alpha=0.3)
#     # else:
#     #     ax1.plot(meanSpikesAllInten, 'k-', alpha=0.3)

# ax0.set_xticks(range(len(possibleIntensity)))
# ax0.set_xticklabels(possibleIntensity)
# ax0.set_xlabel('Intensity (dB SPL)')
# ax0.set_ylabel('Average spikes fired during stimulus')

plt.show()

# ## -- Monotonicity with respect to level -- ##
# for indIter, (indRow, dbRow) in enumerate(goodFitToUseNSpikes.iterrows()):
#     print indRow
#     failed=False
#     cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
#     try:
#         ephysData, bdata = cell.load('tc')
#     except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
#         failed=True
#         print "No tc for cell {}".format(indRow)

#     eventOnsetTimes = ephysData['events']['stimOn']
#     spikeTimes = ephysData['spikeTimes']
#     freqEachTrial = bdata['currentFreq']
#     if len(eventOnsetTimes) != len(freqEachTrial):
#         eventOnsetTimes = eventOnsetTimes[:-1]
#         if len(eventOnsetTimes) != len(freqEachTrial):
#             raise ValueError("The trials still don't line up")

#     possibleFreq = np.unique(freqEachTrial)
#     intensityEachTrial = bdata['currentIntensity']
#     possibleIntensity = np.unique(intensityEachTrial)

#     cfTrials = freqEachTrial==dbRow['cf']
#     eventsThisFreq = eventOnsetTimes[cfTrials]
#     intenThisFreq = intensityEachTrial[cfTrials]

#     baseRange = [-0.1, 0]
#     responseRange = [0, 0.1]
#     alignmentRange = [baseRange[0], responseRange[1]]

#     meanSpikesAllInten = np.empty(len(possibleIntensity))
#     maxSpikesAllInten = np.empty(len(possibleIntensity))

#     for indInten, inten in enumerate(possibleIntensity):
#         # print inten
#         trialsThisIntensity = intenThisFreq==inten
#         eventsThisCombo = eventsThisFreq[trialsThisIntensity]

#         (spikeTimesFromEventOnset,
#         trialIndexForEachSpike,
#         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
#                                                                     eventsThisCombo,
#                                                                     alignmentRange)
#         nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                             indexLimitsEachTrial,
#                                                             baseRange)
#         nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                             indexLimitsEachTrial,
#                                                             responseRange)

#         spikesThisInten = nspkResp[:,0]
#         # print spikesThisInten
#         try:
#             meanSpikesThisInten = np.mean(spikesThisInten)
#             maxSpikesThisInten = np.max(spikesThisInten)
#         except ValueError:
#             meanSpikesThisInten = 0
#             maxSpikesThisInten = 0

#         meanSpikesAllInten[indInten] = meanSpikesThisInten
#         maxSpikesAllInten[indInten] = maxSpikesThisInten

#     overallMaxSpikes = np.max(maxSpikesAllInten)
#     maxSpikes.append(overallMaxSpikes)
