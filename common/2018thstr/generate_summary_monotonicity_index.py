import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
import pandas as pd
import figparams #TODO: Remove this once we move plotting code to a figure file
import matplotlib.pyplot as plt
from scipy import stats

PLOT=1
SAVE = 1


dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'
database = celldatabase.load_hdf(dbPath)

# goodISI = database.query('isiViolations<0.02 or modifiedISI<0.02')
# goodShape = goodISI.query('spikeShapeQuality > 2')
# goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
# goodNSpikes = goodLaser.query('nSpikes>2000')

# db = goodNSpikes

plt.clf()
# ax0 = plt.subplot(121)
ax0 = plt.subplot(111)
# ax1 = plt.subplot(122)

mono = []
maxSpikes = []

# goodFit = db.query('rsquaredFit > 0.04')
# goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
# goodFitToUse = goodFit.query('fitMidPoint<32000')
# goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')

# dbToUse = goodFitToUseNSpikes
#Calculate for every cell
dbToUse = database

## -- Monotonicity with respect to level -- ##
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
            continue

    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    cfTrials = freqEachTrial==dbRow['cf']
    eventsThisFreq = eventOnsetTimes[cfTrials]
    intenThisFreq = intensityEachTrial[cfTrials]

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    meanSpikesAllInten = np.empty(len(possibleIntensity))
    maxSpikesAllInten = np.empty(len(possibleIntensity))
    baseSpikesAllInten = np.empty(len(possibleIntensity))
    for indInten, inten in enumerate(possibleIntensity):
        # print inten
        trialsThisIntensity = intenThisFreq==inten
        eventsThisCombo = eventsThisFreq[trialsThisIntensity]

        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventsThisCombo,
                                                                    alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        spikesThisInten = nspkResp[:,0]
        baselineThisInten = nspkBase[:,0]
        # print spikesThisInten
        try:
            meanSpikesThisInten = np.mean(spikesThisInten)
            meanBaselineSpikesThisInten = np.mean(baselineThisInten)
            maxSpikesThisInten = np.max(spikesThisInten)
        except ValueError:
            meanSpikesThisInten = 0
            maxSpikesThisInten = 0

        meanSpikesAllInten[indInten] = meanSpikesThisInten
        maxSpikesAllInten[indInten] = maxSpikesThisInten
        baseSpikesAllInten[indInten] = meanBaselineSpikesThisInten

    baseline = np.mean(baseSpikesAllInten)
    monoIndex = (meanSpikesAllInten[-1] - baseline) / (np.max(meanSpikesAllInten)-baseline)

    dbToUse.loc[indRow, 'monotonicityIndex'] = monoIndex

    overallMaxSpikes = np.max(maxSpikesAllInten)
    maxSpikes.append(overallMaxSpikes)

if SAVE:
    celldatabase.save_hdf(database, dbPath)

if PLOT:

    def jitter(arr, frac):
        jitter = (np.random.random(len(arr))-0.5)*2*frac
        jitteredArr = arr + jitter
        return jitteredArr

    plt.clf()
    ax = plt.subplot(111)
    colorATh = 'b'
    colorAC = 'r'

    ac = dbToUse.groupby('brainArea').get_group('rightAC')
    thal = dbToUse.groupby('brainArea').get_group('rightThal')

    popStatCol = 'monotonicityIndex'
    acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
    thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

    pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    ax.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None')
    # medline(axBW, np.median(thalPopStat), 0, 0.5)
    pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    ax.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None')
    ax.set_ylabel('Monotonicity index')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['ATh:Str', 'AC:Str'])

    zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)
    print pVal
    # medline(axBW, np.median(acPopStat), 1, 0.5)



    #TODO: Save this value out

    # if len(meanSpikesAllInten)>10:
    #     # ax0.plot(meanSpikesAllInten, 'k-', alpha=0.3)
    #     ax0.plot(meanSpikesAllInten/max(meanSpikesAllInten).astype(float), 'k-', alpha=0.3)
    # else:
    #     ax1.plot(meanSpikesAllInten, 'k-', alpha=0.3)

# ax0.set_xticks(range(len(possibleIntensity)))
# ax0.set_xticklabels(possibleIntensity)
# ax0.set_xlabel('Intensity (dB SPL)')
# ax0.set_ylabel('Average spikes fired during stimulus')

# plt.show()
