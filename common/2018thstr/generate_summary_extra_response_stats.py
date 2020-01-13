import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from matplotlib import pyplot as plt
import os
import pandas as pd

dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'
database = celldatabase.load_hdf(dbPath)

goodISI = database.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
goodNSpikes = goodLaser.query('nSpikes>2000')

# db = goodNSpikes
# Calculate for all cells so we can save the complete database
db = database

CASE = 3

if CASE == 0:
    #Compute onsetivity using noiseburst session

    # db['normPSTH'] = np.
    for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        try:
            ephysData, bdata = cell.load('noiseburst')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            print "No noiseburst for cell {}".format(indRow)
        eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimes = ephysData['spikeTimes']
        cellLatency = dbRow['latency']
        if not cellLatency > 0:
            print "Negative latency!! Skipping"
            continue
        baseRange = [-0.1, -0.05]
        # responseRange = [0, 0.05, 0.1]
        responseRange = [cellLatency, cellLatency + 0.05, 0.1+cellLatency]
        # if dbRow['brainArea']=='rightAC':
        #     # responseRange = [0.02, 0.07, 0.12]
        #     responseRange = [0.02, 0.07, 0.1]
        # elif dbRow['brainArea']=='rightThal':
        #     # responseRange = [0.005, 0.015, 0.105]
        #     responseRange = [0.005, 0.015, 0.1]

        alignmentRange = [baseRange[0], responseRange[-1]]
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        avgResponse = nspkResp.mean(axis=0)
        onsetSpikes = avgResponse[0]
        sustainedSpikes = avgResponse[1]
        onsetRate = onsetSpikes / (responseRange[1] - responseRange[0])
        sustainedRate = sustainedSpikes / (responseRange[2] - responseRange[1])

        baseSpikes = nspkBase.mean()
        baseRate = baseSpikes / (baseRange[1] - baseRange[0])

        onsetBaseSubtracted = onsetRate - baseRate
        sustainedBaseSubtracted = sustainedRate - baseRate

        # baseSub = avgResponse - avgBase
        # normResponse = baseSub / baseSub[0]
        db.loc[indRow, 'onsetRateNoise'] = onsetRate
        db.loc[indRow, 'sustainedRateNoise'] = sustainedRate
        db.loc[indRow, 'baselineRateNoise'] = baseRate

    celldatabase.save_hdf(db, '/tmp/database_with_normResponse.h5')

elif CASE == 1:

    PLOT = 0
    SAVE = 1
    #Compute onsetivity using CF trials with top 5 intensities.
    for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        try:
            ephysData, bdata = cell.load('tc')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            print "No TC for cell {}".format(indRow)

        eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimes = ephysData['spikeTimes']
        freqEachTrial = bdata['currentFreq']
        if len(eventOnsetTimes) != len(freqEachTrial):
            eventOnsetTimes = eventOnsetTimes[:-1]
            if len(eventOnsetTimes) != len(freqEachTrial):
                print "BAD number of trials! Skipping"
                continue

        #Get the trials for the CF
        possibleFreq = np.unique(freqEachTrial)
        intensityEachTrial = bdata['currentIntensity']
        cfTrials = freqEachTrial==dbRow['cf']
        eventsThisFreq = eventOnsetTimes[cfTrials]
        intenThisFreq = intensityEachTrial[cfTrials]

        #Get only the trials with the CF and the top 5 intensities
        possibleIntensity = np.unique(intenThisFreq)
        if len(possibleIntensity) > 4:
            intenToUse = possibleIntensity[-5:]
        else:
            intenToUse = possibleIntensity

        #Boolean of which trials from this frequency were high intensity
        highIntenTrials = np.in1d(intenThisFreq, intenToUse)

        #Filter the events this frequency to just take the ones from high intensity
        eventsThisFreqHighIntensity = eventsThisFreq[highIntenTrials]

        cellLatency = dbRow['latency']
        if not cellLatency > 0:
            print "Negative latency!! Skipping"
            continue

        baseRange = [-0.1, -0.05]
        # responseRange = [0, 0.05, 0.1]
        responseRange = [cellLatency, cellLatency + 0.05, 0.1+cellLatency]
        # if dbRow['brainArea']=='rightAC':
        #     # responseRange = [0.02, 0.07, 0.12]
        #     responseRange = [0.02, 0.07, 0.1]
        # elif dbRow['brainArea']=='rightThal':
        #     # responseRange = [0.005, 0.015, 0.105]
        #     responseRange = [0.005, 0.015, 0.1]

        alignmentRange = [baseRange[0], responseRange[-1]]

        #Align spikes just to the selected event onset times
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventsThisFreqHighIntensity,
                                                                       alignmentRange)

        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)

        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        avgResponse = nspkResp.mean(axis=0)
        onsetSpikes = avgResponse[0]
        sustainedSpikes = avgResponse[1]
        onsetRate = onsetSpikes / (responseRange[1] - responseRange[0])
        sustainedRate = sustainedSpikes / (responseRange[2] - responseRange[1])

        baseSpikes = nspkBase.mean()
        baseRate = baseSpikes / (baseRange[1] - baseRange[0])

        onsetBaseSubtracted = onsetRate - baseRate
        sustainedBaseSubtracted = sustainedRate - baseRate

        # baseSub = avgResponse - avgBase
        # normResponse = baseSub / baseSub[0]
        db.loc[indRow, 'onsetRateCF'] = onsetRate
        db.loc[indRow, 'sustainedRateCF'] = sustainedRate
        db.loc[indRow, 'baselineRateCF'] = baseRate

        #Plot sanity check
        if PLOT:
            saveDir = '/home/nick/Desktop/cf_onsetivity_plots'
            title = '{}_{}_{}_T{}c{}.png'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], int(dbRow['tetrode']), int(dbRow['cluster']))
            plt.clf()
            ax = plt.subplot(111)
            ax.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
            ax.axvline(x = 0, color = '0.5')
            ax.axvline(x = responseRange[0], color = 'r')
            ax.axvline(x = responseRange[1], color = 'r')
            ax.axvline(x = responseRange[2], color = 'r')
            ax.set_xlabel('Time from sound onset (s)')
            ax.set_xlim(alignmentRange)
            plt.tight_layout()

            plt.savefig(os.path.join(saveDir, title))

    if SAVE:
        # celldatabase.save_hdf(db, '/tmp/database_with_cf_onsetivity.h5')
        celldatabase.save_hdf(db, dbPath)


elif CASE == 2:

    plt.clf()
    # ax0 = plt.subplot(121)
    ax0 = plt.subplot(111)
    # ax1 = plt.subplot(122)

    mono = []
    maxSpikes = []

    goodFit = db.query('rsquaredFit > 0.04')
    goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
    goodFitToUse = goodFit.query('fitMidPoint<32000')
    goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')

    ## -- Monotonicity with respect to level -- ##
    for indIter, (indRow, dbRow) in enumerate(goodFitToUseNSpikes.iterrows()):
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
            # print spikesThisInten
            try:
                meanSpikesThisInten = np.mean(spikesThisInten)
                maxSpikesThisInten = np.max(spikesThisInten)
            except ValueError:
                meanSpikesThisInten = 0
                maxSpikesThisInten = 0

            meanSpikesAllInten[indInten] = meanSpikesThisInten
            maxSpikesAllInten[indInten] = maxSpikesThisInten

        overallMaxSpikes = np.max(maxSpikesAllInten)
        maxSpikes.append(overallMaxSpikes)
        #TODO: Save this value out

        if len(meanSpikesAllInten)>10:
            # ax0.plot(meanSpikesAllInten, 'k-', alpha=0.3)
            ax0.plot(meanSpikesAllInten/max(meanSpikesAllInten).astype(float), 'k-', alpha=0.3)
        # else:
        #     ax1.plot(meanSpikesAllInten, 'k-', alpha=0.3)

    ax0.set_xticks(range(len(possibleIntensity)))
    ax0.set_xticklabels(possibleIntensity)
    ax0.set_xlabel('Intensity (dB SPL)')
    ax0.set_ylabel('Average spikes fired during stimulus')

    plt.show()



# Max rate from tone-evoked
elif CASE == 3:

    plt.clf()
    # ax0 = plt.subplot(121)
    ax0 = plt.subplot(111)
    # ax1 = plt.subplot(122)

    mono = []
    maxSpikes = []

    goodFit = db.query('rsquaredFit > 0.04')
    goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
    goodFitToUse = goodFit.query('fitMidPoint<32000')
    goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')

    ## -- Max rate (tone-evoked) -- ##
    for indIter, (indRow, dbRow) in enumerate(goodFitToUseNSpikes.iterrows()):
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

        cellLatency = dbRow['latency']
        if not cellLatency > 0:
            print "Negative latency!! Skipping"
            continue
        baseRange = [-0.1, -0.05]
        # responseRange = [0, 0.05, 0.1]
        responseRange = [cellLatency, cellLatency + 0.1]

        # baseRange = [-0.1, 0]
        # responseRange = [0, 0.1]
        alignmentRange = [baseRange[0], responseRange[1]]

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
                allIntenRespMedian[indinten, indfreq] = np.median(nspkResp)

        maxSpikes = np.max(allIntenResp.ravel())
        baseSpikes = np.mean(allIntenBase.ravel())
        timeRangeResp = responseRange[1]-responseRange[0]
        timeRangeBase = baseRange[1] - baseRange[0]
        maxFr = maxSpikes/timeRangeResp
        baseFr = baseSpikes/timeRangeBase

        db.loc[indRow, 'maxFR'] = maxFr
        db.loc[indRow, 'baseFR'] = baseFr
