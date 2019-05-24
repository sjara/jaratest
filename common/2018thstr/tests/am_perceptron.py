import os
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from collections import Counter
from scipy import stats
from scipy import signal
import pandas as pd
import figparams
reload(figparams)
from sklearn import metrics
from sklearn import svm
from sklearn import linear_model
FIGNAME = 'figure_am'
STUDY_NAME = '2018thstr'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']

CASE=5

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

def spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, freqEachTrial):
    '''
    Generator func to return the spiketimes/trial indices for trials of each frequency. Also returns the index limits. This basicially just cuts up our usual eventlocked spiketimes data per frequency.
    '''
    possibleFreq = np.unique(freqEachTrial)
    for freq in possibleFreq:
        trialsThisFreq = np.flatnonzero(freqEachTrial==freq)
        spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        trialIndicesThisFreq = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        indexLimitsThisFreq = indexLimitsEachTrial[:,trialsThisFreq]
        yield (freq, spikeTimesThisFreq, trialIndicesThisFreq, indexLimitsThisFreq)

# def spiketimes_to_spikecounts(spikeTimesFromEventOnset,trialIndexForEachSpike,binEdges):
#     '''

#     I had to rework this function to work if we take a subset of trials at a time
#     (like iterating over AM rates).

#     Create a matrix with spike counts given the times of the spikes.

#     spikeTimesFromEventOnset: vector of spikes timestamps with respect
#     to the onset of the event.
#     indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial
#     binEdges: time bin edges (including the left-most and right-most).

#     Returns:
#     spikeCountMat: each rows is one trial. N columns is len(binEdges)-1
#     '''
#     possibleTrials = np.unique(trialIndexForEachSpike)
#     nTrials = len(possibleTrials)
#     spikeCountMat = np.empty((nTrials,len(binEdges)-1),dtype=int)
#     for indEnum, indTrial in enumerate(possibleTrials):
#         # indsThisTrial = slice(indexLimitsEachTrial[0,indtrial],indexLimitsEachTrial[1,indtrial])
#         indsThisTrial = np.flatnonzero(trialIndexForEachSpike==indTrial)
#         spkCountThisTrial,binsEdges = np.histogram(spikeTimesFromEventOnset[indsThisTrial],binEdges)
#         spikeCountMat[indEnum,:] = spkCountThisTrial
#     return spikeCountMat

def linear_discriminator(spikesPref, spikesNonPref):

    if len(spikesPref)==0:
        raise ValueError('SpikesPref is an empty thing')
    if len(spikesNonPref)==0:
        raise ValueError('SpikesNonPref is an empty thing')

    #Count number of times each spike number occurred for pref and nonpref
    prefSpikeCount = Counter(spikesPref)
    nonPrefSpikeCount = Counter(spikesNonPref)

    #Find possible threshold values
    minSpikes = np.min(np.concatenate([spikesPref, spikesNonPref]))
    maxSpikes = np.max(np.concatenate([spikesPref, spikesNonPref]))
    possibleThresh = np.arange(minSpikes, maxSpikes+1)

    #Init array for accuracy
    accuracy = np.empty(len(possibleThresh))

    #Try each possible threshold
    for indThresh, threshold in enumerate(possibleThresh):

        #Misclassified preferred - below the threshold
        misPref = sum([prefSpikeCount[i] for i in possibleThresh[:indThresh]])

        #Misclassified non-preferred - above the threshold
        misNonPref = sum([nonPrefSpikeCount[i] for i in possibleThresh[indThresh:]])

        #Calculate accuracy for this threshold value
        totalTrials = sum([len(spikesPref), len(spikesNonPref)])
        accuracy[indThresh] = (totalTrials - (misPref + misNonPref)) / float(totalTrials)

    #Return max accuracy and corresponding threshold
    indMaxAccuracy = np.argmax(accuracy)
    maxAccuracy = accuracy[indMaxAccuracy]
    threshold = possibleThresh[indMaxAccuracy]
    return maxAccuracy, threshold


########### Testing on examples #################
if CASE==1:

    exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
    exampleData = np.load(exampleDataPath)

    exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
    exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
    exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
    exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

    # exampleName = 'Thal1'
    exampleNames = ['Thal0', 'Thal1', 'AC0', 'AC1']
    # exampleNames = ['AC1']
    plt.clf()
    for indExample, exampleName in enumerate(exampleNames):

        spikeTimesFromEventOnset = exampleSpikeTimes[exampleName]
        trialIndexForEachSpike = exampleTrialIndexForEachSpike[exampleName]
        indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
        freqEachTrial = exampleFreqEachTrial[exampleName]

        # timeRange = [0.1, 0.5]
        timeRange = [0, 0.5]
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        spikeCountEachTrial = spikeCountMat.flatten()
        spikeCountEachTrial = spikeCountEachTrial[:-1]


        #Calculate best and worst AM rate
        possibleRates = np.unique(freqEachTrial)
        avgSpikesEachRate = np.empty(len(possibleRates))
        for indRate, thisRate in enumerate(possibleRates):
            spikesThisRate = spikeCountEachTrial[freqEachTrial==thisRate]
            avgSpikesEachRate[indRate] = np.mean(spikesThisRate.ravel())

        #Find spikes each trial for pref and nonpref frequencies
        indPref = np.argmax(avgSpikesEachRate)
        indNonPref = np.argmin(avgSpikesEachRate)
        spikesPref = spikeCountEachTrial[freqEachTrial==possibleRates[indPref]]
        spikesNonPref = spikeCountEachTrial[freqEachTrial==possibleRates[indNonPref]]

        spikes = np.concatenate([spikesPref, spikesNonPref])
        prefRate = np.concatenate([np.ones(len(spikesPref)), np.zeros(len(spikesNonPref))])


        #Reshape to column vector
        X = spikes.reshape(len(spikes), 1)
        y = prefRate

        #Shuffle and make test and train datasets
        n_sample = len(X)
        # np.random.seed(0)
        order = np.random.permutation(n_sample)
        X_shuffle = X[order]
        y_shuffle = y[order].astype(np.float)

        trainFold = 0.6

        X_train = X_shuffle[:int(trainFold * n_sample)]
        y_train = y_shuffle[:int(trainFold * n_sample)]
        X_test = X_shuffle[int(trainFold * n_sample):]
        y_test = y_shuffle[int(trainFold * n_sample):]

        classifier = svm.SVC(kernel='linear')
        # classifier = linear_model.Perceptron(n_iter=100)
        # classifier.fit(spikes, prefRate)

        # score = classifier.score(spikes, prefRate)

        # classifier.fit(X_train, y_train)
        classifier.fit(X, y)

        plt.subplot(len(exampleNames), 1, indExample+1)

        spacing = 2
        # plt.clf()
        xdata = X[:, 0]
        ydata = np.empty(len(xdata))

        uniqueX = np.unique(xdata)

        predY = classifier.predict(uniqueX.reshape(len(uniqueX), 1))

        print exampleName
        print predY

        diffY = np.diff(predY)
        xBoundary = np.flatnonzero(diffY) + 0.5

        for oneX in uniqueX:
            nVals = np.sum(xdata==oneX)
            possibleOffsets = spacing * np.arange(-nVals/2.0+0.5, nVals/2.0, 1)
            yOffset = possibleOffsets[:nVals]

            #Set these offset values
            ydata[np.flatnonzero(xdata==oneX)]=yOffset

        plt.scatter(xdata, ydata, c=y, zorder=10, cmap=plt.cm.cool,
                    edgecolor='k', s=20)
        plt.axvline(x = xBoundary, color='r')

        # score = classifier.score(X_test, y_test)
        score = classifier.score(X, y)
        maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
        plt.title("Example {}: accuracy: {:02f}\nLD accuracy: {}, threshold: {}".format(exampleName, score, maxAccuracy, threshold))

        # Circle out the test data
        # xdata = X_test[:, 0]
        # ydata = np.empty(len(xdata))

        # uniqueX = np.unique(xdata)
        # for oneX in uniqueX:
        #     nVals = np.sum(xdata==oneX)
        #     possibleOffsets = spacing * np.arange(-nVals/2.0+0.5, nVals/2.0, 1)
        #     yOffset = possibleOffsets[:nVals]

        #     #Set these offset values
        #     ydata[np.flatnonzero(xdata==oneX)]=yOffset

        # plt.scatter(xdata, ydata, s=80, facecolors='none',
        #             zorder=10, edgecolor='k')

        # uv, xt = xtab([spikeCountEachTrial, freqEachTrial])
        # mi = metrics.mutual_info_score(None, None, contingency=xt)

        # print exampleName
        # print "MI (bits/trial): {}".format(mi)
        # print "bits/spike: {}".format(mi/np.mean(spikeCountEachTrial))


elif CASE==2:
    SHUFFLE=False #Set to true to shuffle AM rates, giving an estimate of the chance level.

    dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
    dataframe = pd.read_hdf(dbPath, key='dataframe')
    # svmScore = np.empty(len(dataframe))
    for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
        if not 'am' in dbRow['sessionType']:
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print 'BREAKING, AM'
            continue
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am session for cell {}".format(indRow)
            dataframe.loc[indRow, 'svmScore'] = np.nan
            continue

        spikeTimes = ephysData['spikeTimes']

        if len(spikeTimes)<100:
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print "BREAKING, Spikenum"
            continue

        numFreq = len(np.unique(bdata['currentFreq']))

        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)

        ### --- Test to see if there is a response to the AM session --- ###
        baseRange = [-0.5, -0.1]
        responseRange = [0.1, 0.5]
        alignmentRange = [baseRange[0], responseRange[1]]
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







        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        if pVal > 0.05: #No response
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print "Breaking, no significant response"
            continue


        ### --- Calculate best and worst rate
        timeRange = [0, 0.5]
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    timeRange)

        freqEachTrial = bdata['currentFreq']

        if SHUFFLE:
            freqEachTrial = np.random.permutation(freqEachTrial)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        spikeCountEachTrial = spikeCountMat.flatten()
        if len(freqEachTrial) == len(spikeCountEachTrial)-1:
            spikeCountEachTrial = spikeCountEachTrial[:-1]

        possibleRates = np.unique(freqEachTrial)
        avgSpikesEachRate = np.empty(len(possibleRates))
        for indRate, thisRate in enumerate(possibleRates):
            spikesThisRate = spikeCountEachTrial[freqEachTrial==thisRate]
            avgSpikesEachRate[indRate] = np.mean(spikesThisRate.ravel())

        #Find spikes each trial for pref and nonpref frequencies
        indPref = np.argmax(avgSpikesEachRate)
        indNonPref = np.argmin(avgSpikesEachRate)
        spikesPref = spikeCountEachTrial[freqEachTrial==possibleRates[indPref]]
        spikesNonPref = spikeCountEachTrial[freqEachTrial==possibleRates[indNonPref]]

        # spikes = np.concatenate([spikesPref, spikesNonPref])
        # prefRate = np.concatenate([np.ones(len(spikesPref)), np.zeros(len(spikesNonPref))])



        # #Reshape to column vector
        # X = spikes.reshape(len(spikes), 1)
        # y = prefRate

        # #Shuffle and make test and train datasets
        # n_sample = len(X)
        # np.random.seed(0)
        # order = np.random.permutation(n_sample)
        # X_shuffle = X[order]
        # y_shuffle = y[order].astype(np.float)

        # trainFold = 0.6

        # X_train = X_shuffle[:int(trainFold * n_sample)]
        # y_train = y_shuffle[:int(trainFold * n_sample)]
        # X_test = X_shuffle[int(trainFold * n_sample):]
        # y_test = y_shuffle[int(trainFold * n_sample):]

        # classifier = svm.SVC(kernel='linear')
        # # classifier.fit(spikes, prefRate)

        # # score = classifier.score(spikes, prefRate)

        # classifier.fit(X_train, y_train)
        # score = classifier.score(X_test, y_test)

        maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
        dataframe.loc[indRow, 'accuracy'] = maxAccuracy
        dataframe.to_hdf('/tmp/2018thstr_with_accuracy.h5', key='dataframe')

if CASE==3:
    def jitter(arr, frac):
        jitter = (np.random.random(len(arr))-0.5)*2*frac
        jitteredArr = arr + jitter
        return jitteredArr

    def medline(yval, midline, width, color='k', linewidth=3):
        start = midline-(width/2)
        end = midline+(width/2)
        plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

    dataframe = pd.read_hdf('/tmp/2018thstr_with_accuracy.h5', key='dataframe')
    # dataframe = pd.read_hdf('/tmp/2018thstr_shuffled_with_accuracy.h5', key='dataframe')
    #Show population distributions
    colorATh = figparams.cp.TangoPalette['SkyBlue2']
    colorAC = figparams.cp.TangoPalette['ScarletRed1']
    dataMS=5

    goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
    goodShape = goodISI.query('spikeShapeQuality > 2')
    goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
    goodNSpikes = goodLaser.query('nSpikes>2000')

    ac = goodNSpikes.groupby('brainArea').get_group('rightAC')
    thal = goodNSpikes.groupby('brainArea').get_group('rightThal')

    popStatCol = 'accuracy'
    acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
    thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

    plt.clf()
    axSummary = plt.subplot(111)

    jitterFrac = 0.2
    pos = jitter(np.ones(len(thalPopStat))*0, jitterFrac)
    axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(thalPopStat), 0, 0.5)
    pos = jitter(np.ones(len(acPopStat))*1, jitterFrac)
    axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(acPopStat), 1, 0.5)
    tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
    axSummary.set_xticks(range(2))
    axSummary.set_xticklabels(tickLabels, rotation=45)
    axSummary.set_ylim([0.5, 1])
    # extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)

    zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

    # messages.append("{} p={}".format(popStatCol, pVal))

    # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

    # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')

    starHeightFactor = 0.2
    starGapFactor = 0.3
    starYfactor = 0.1
    yDataMax = max([max(acPopStat), max(thalPopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    starString = None if pVal<0.05 else 'n.s.'
    fontSizeStars = 9
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                starSize=fontSizeStars, starString=starString,
                                gapFactor=starGapFactor)
    extraplots.boxoff(axSummary)
    plt.hold(1)
    plt.show()

elif CASE==4:

    exampleColor = ['b', 'b', 'r', 'r']
    exampleStyle = ['-', '--', '-', '--']

    examples = {}
    examples.update({'AC0' : 'pinp017_2017-03-23_1604.0_TT4c2'})
    examples.update({'AC1' : 'pinp017_2017-03-23_1414.0_TT5c6'})
    examples.update({'Thal0' : 'pinp015_2017-02-15_2902.0_TT8c4'})
    examples.update({'Thal1' : 'pinp016_2017-03-16_3707.0_TT2c3'})

    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS_MODIFIED_CLU.h5'
    db = pd.read_hdf(dbPath, key='dataframe')

    # exampleNames = ['Thal0', 'Thal1', 'AC0', 'AC1']
    exampleNames = ['Thal0']
    # exampleNames = ['AC1']

    SHUFFLE = True

    plt.clf()
    for indExample, exampleName in enumerate(exampleNames):

        cellName = examples[exampleName]

        (subject, date, depth, tetrodeCluster) = cellName.split('_')
        depth = float(depth)
        tetrode = int(tetrodeCluster[2])
        cluster = int(tetrodeCluster[4:])
        indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

        cell = ephyscore.Cell(dbRow)
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am for cell {}".format(indRow)
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
        freqEachTrial = bdata['currentFreq']

        if len(eventOnsetTimes) != len(freqEachTrial):
            if len(eventOnsetTimes) == len(freqEachTrial)+1:
                eventOnsetTimes = eventOnsetTimes[:-1]
            else:
                raise ValueError("Something went wrong with the number of events")

        # spikeTimesFromEventOnset = exampleSpikeTimes[exampleName]
        # trialIndexForEachSpike = exampleTrialIndexForEachSpike[exampleName]
        # indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
        # freqEachTrial = exampleFreqEachTrial[exampleName]

        #Timerange for alignment?
        timeRange = [0.05, 0.5] #Ignoring onset responses TODO: Is this the best way to do this??

        possibleFreq = np.unique(freqEachTrial)
        accuracyEachFreq = []
        for thisFreq in possibleFreq:

            #Only use events for this frequency
            eventsThisFreq = eventOnsetTimes[freqEachTrial==thisFreq]

            (spikeTimesFromEventOnset,
             trialIndexForEachSpike,
             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                           eventsThisFreq,
                                                                           timeRange)

            # period = 1/freq

            # This is really all we need to do to bin things by phase.
            radsPerSec = thisFreq*2*np.pi
            spikeRads = (spikeTimesFromEventOnset*radsPerSec)%(2*np.pi)


            strength, phase = signal.vectorstrength(spikeTimesFromEventOnset, 1.0/thisFreq)

            phase = (phase+2*np.pi)%(2*np.pi)

            # shiftedRads = ((spikeRads - phase) + 0.25*np.pi)%2*np.pi
            shiftedRads = ((spikeRads - phase) + 2.25*np.pi)
            if any(shiftedRads<0):
                raise ValueError("Some shifted rads below 0")
            # shiftedRads = ((spikeRads - phase) + 2.25*np.pi)%(2*np.pi)
            spikeRads = shiftedRads % (2*np.pi)

            nBins=4
            binEdges = np.arange(0, 2.01*np.pi, 2*np.pi/nBins) #The 2.01 makes it actually include 2pi
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeRads,indexLimitsEachTrial,binEdges)

            spikeCountMatShuffle = np.empty(np.shape(spikeCountMat))
            for indRow in range(np.shape(spikeCountMat)[0]):
                # spikeCountMatShuffle[indRow, :] = np.random.permutation(spikeCountMat[indRow, :])
                numRolls = np.random.choice(range(np.shape(spikeCountMat)[1]))
                spikeCountMatShuffle[indRow, :] = np.roll(spikeCountMat[indRow, :], numRolls)
            if SHUFFLE:
                spikeCountMat = spikeCountMatShuffle

            binMeans = np.mean(spikeCountMat, axis=0)
            binMeansShuffle = np.mean(spikeCountMatShuffle, axis=0)

            prefInd = np.argmax(binMeans)
            nonPrefInd = np.argmin(binMeans)

            spikesPref = spikeCountMat[:, prefInd]
            spikesNonPref = spikeCountMat[:, nonPrefInd]

            maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)


            ## For plotting cycle rasters
            plt.clf()
            plt.plot(spikeRads, trialIndexForEachSpike, 'k.')
            ax = plt.gca()
            ax.set_xticks([0, np.pi/2, np.pi, np.pi*1.5, np.pi*2])
            plt.title(maxAccuracy)
            plt.show()
            # import ipdb; ipdb.set_trace()
            # print phase
            print maxAccuracy
            # print min(spikeRads)
            # plt.waitforbuttonpress()


            accuracyEachFreq.append(maxAccuracy)

        # plt.plot(accuracyEachFreq, color=exampleColor[indExample], ls=exampleStyle[indExample])
        # plt.hold(1)
    plt.show()


elif CASE==5:

    '''
    Calculate the accuracy discriminating between the preferred and non-preferred phase
    '''

    SHUFFLE = False

    dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS_MODIFIED_CLU.h5'
    # dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
    dataframe = pd.read_hdf(dbPath, key='dataframe')

    plt.clf()
    for indRow, dbRow in dataframe.iterrows():

        cell = ephyscore.Cell(dbRow)
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            # dataframe.set_value(indRow, 'phaseAccuracy', list(nanAccuracy))
            print "No am for cell {}".format(indRow)
            continue
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
        freqEachTrial = bdata['currentFreq']

        if len(eventOnsetTimes) != len(freqEachTrial):
            if len(eventOnsetTimes) == len(freqEachTrial)+1:
                eventOnsetTimes = eventOnsetTimes[:-1]
            else:
                raise ValueError("Something went wrong with the number of events")

        possibleFreq = np.unique(freqEachTrial)
        nanAccuracy = np.full(len(possibleFreq), np.nan)

        ## Test to see if there is a significant response to AM
        baseRange = [-0.5, -0.1]
        responseRange = [0.1, 0.5]
        alignmentRange = [baseRange[0], responseRange[1]]
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
        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        if pVal > 0.05: #No response
            # dataframe.set_value(indRow, 'phaseAccuracy', list(nanAccuracy))
            print "Breaking, no significant response"
            continue

        print "Calculating for cell {}".format(indRow)

        # spikeTimesFromEventOnset = exampleSpikeTimes[exampleName]
        # trialIndexForEachSpike = exampleTrialIndexForEachSpike[exampleName]
        # indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
        # freqEachTrial = exampleFreqEachTrial[exampleName]

        #Timerange for alignment?
        timeRange = [0.05, 0.5] #Ignoring onset responses TODO: Is this the best way to do this??

        possibleFreq = np.unique(freqEachTrial)
        accuracyEachFreq = []
        for thisFreq in possibleFreq:

            #Only use events for this frequency
            eventsThisFreq = eventOnsetTimes[freqEachTrial==thisFreq]

            (spikeTimesFromEventOnset,
             trialIndexForEachSpike,
             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                           eventsThisFreq,
                                                                           timeRange)

            # period = 1/freq

            # This is really all we need to do to bin things by phase.
            radsPerSec = thisFreq*2*np.pi
            spikeRads = (spikeTimesFromEventOnset*radsPerSec)%(2*np.pi)


            strength, phase = signal.vectorstrength(spikeTimesFromEventOnset, 1.0/thisFreq)
            phase = (phase+2*np.pi)%(2*np.pi)

            shiftedRads = ((spikeRads - phase) + 2.25*np.pi)
            if any(shiftedRads<0):
                raise ValueError("Some shifted rads below 0")
            # shiftedRads = ((spikeRads - phase) + 2.25*np.pi)%(2*np.pi)
            spikeRads = shiftedRads % (2*np.pi)

            nBins=4
            binEdges = np.arange(0, 2.01*np.pi, 2*np.pi/nBins) #The 2.01 makes it actually include 2pi
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeRads,indexLimitsEachTrial,binEdges)

            spikeCountMatCopy = copy.deepcopy(spikeCountMat)
            spikeCountMatShuffle = np.empty(np.shape(spikeCountMatCopy))
            for indMatRow in range(np.shape(spikeCountMatCopy)[0]):
                numRolls = np.random.choice(range(np.shape(spikeCountMatCopy)[1]))
                # numRolls = 0
                spikeCountMatShuffle[indMatRow, :] = np.roll(spikeCountMatCopy[indMatRow, :], numRolls)
            if SHUFFLE:
                spikeCountMat = spikeCountMatShuffle

            binMeans = np.mean(spikeCountMat, axis=0)
            prefInd = np.argmax(binMeans)
            nonPrefInd = np.argmin(binMeans)

            spikesPref = spikeCountMat[:, prefInd]
            spikesNonPref = spikeCountMat[:, nonPrefInd]

            maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
            print maxAccuracy

            dataframe.set_value(indRow, 'phaseAccuracy_{}Hz'.format(int(thisFreq)), maxAccuracy)
        dbPath = '/tmp/phaseCalcDatabase.h5'
        dataframe.to_hdf(dbPath, key='dataframe')
        # plt.plot(accuracyEachFreq, color=exampleColor[indExample], ls=exampleStyle[indExample])
        # plt.hold(1)


elif CASE==6:

    dbPath = '/tmp/phaseCalcDatabase.h5'
    db = pd.read_hdf(dbPath, key='dataframe')

    goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
    goodShape = goodISI.query('spikeShapeQuality > 2')
    goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
    goodNSpikes = goodLaser.query('nSpikes>2000')

    ac = goodNSpikes.groupby('brainArea').get_group('rightAC')
    thal = goodNSpikes.groupby('brainArea').get_group('rightThal')

    possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
    ratesToUse = possibleRateKeys
    keys = ['phaseAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

    acData = np.full((len(ac), len(ratesToUse)), np.nan)
    thalData = np.full((len(thal), len(ratesToUse)), np.nan)

    for externalInd, (indRow, row) in enumerate(ac.iterrows()):
        for indKey, key in enumerate(keys):
            acData[externalInd, indKey] = row[key]

    for externalInd, (indRow, row) in enumerate(thal.iterrows()):
        for indKey, key in enumerate(keys):
            thalData[externalInd, indKey] = row[key]

    acMean = np.nanmean(acData, axis=0)
    acStd = np.nanstd(acData, axis=0)
    thalMean = np.nanmean(thalData, axis=0)
    thalStd = np.nanstd(thalData, axis=0)

    plt.clf()
    colorATh = figparams.cp.TangoPalette['SkyBlue2']
    colorAC = figparams.cp.TangoPalette['ScarletRed1']
    split=0.1
    for indRate, rate in enumerate(possibleRateKeys):

        acDataThisRate = acData[:,indRate]
        acDataThisRate = acDataThisRate[~np.isnan(acDataThisRate)]

        thalDataThisRate = thalData[:,indRate]
        thalDataThisRate = thalDataThisRate[~np.isnan(thalDataThisRate)]

        [zScore, pVal] = stats.mannwhitneyu(acDataThisRate,thalDataThisRate)
        # import ipdb
        # ipdb.set_trace()
        print pVal

        starHeightFactor = 0.2
        starGapFactor = 0.5
        starYfactor = 0.05
        # yDataMax = max([max(acDataThisRate), max()])
        yDataMax = 1
        yStars = yDataMax + yDataMax*starYfactor
        yStarHeight = (yDataMax*starYfactor)*starHeightFactor

        starString = None if pVal<0.05 else 'n.s.'
        fontSizeStars = 9
        extraplots.significance_stars([indRate-split, indRate+split], yStars, yStarHeight, starMarker='*',
                                    starSize=fontSizeStars, starString=starString,
                                    gapFactor=starGapFactor)
        plt.hold(1)

        plt.plot(np.zeros(acDataThisRate.shape[0])+indRate-split, acDataThisRate, 'o', mec=colorAC, mfc='None')
        plt.plot(np.zeros(thalDataThisRate.shape[0])+indRate+split, thalDataThisRate, 'o', mec=colorATh, mfc='None')
    # for indCell in range(acData.shape[0]):
    #     plt.plot(acData[indCell, :], '-', color=colorAC)
    # for indCell in range(thalData.shape[0]):
    #     plt.plot(thalData[indCell, :], '-', color=colorATh)

    ax = plt.gca()
    ax.set_xticks(range(len(possibleRateKeys)))
    ax.set_xticklabels(possibleRateKeys)
    ax.set_xlabel('AM Rate (Hz)')
    ax.set_ylabel('Prediction accuracy')
    extraplots.boxoff(ax)

    plt.plot(acMean, '-o', color=colorAC)
    plt.plot(thalMean, '-o', color=colorATh)
    # plt.fill_between(range(len(acMean)), acMean + acStd, acMean-acStd, color='r', alpha=0.5)
    # plt.hold(1)
    # plt.plot(thalMean, 'b-')
    # plt.fill_between(range(len(thalMean)), thalMean + thalStd, thalMean-thalStd, color='b', alpha=0.5)
    plt.show()

elif CASE==7:

    plt.clf()
    ### Average all the rates together

    dbPath = '/tmp/phaseCalcDatabase.h5'
    # dbPath = '/tmp/phaseCalcDatabase_shuffled.h5'
    db = pd.read_hdf(dbPath, key='dataframe')

    # dbPath = os.path.join(dataDir, 'celldatabase_with_phase_discrimination_accuracy.h5')
    # db = pd.read_hdf(dbPath, key='dataframe')

    goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
    goodShape = goodISI.query('spikeShapeQuality > 2')
    goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
    goodNSpikes = goodLaser.query('nSpikes>2000')

    ac = goodNSpikes.groupby('brainArea').get_group('rightAC')
    thal = goodNSpikes.groupby('brainArea').get_group('rightThal')

    possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
    ratesToUse = possibleRateKeys
    keys = ['phaseAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

    acData = np.full((len(ac), len(ratesToUse)), np.nan)
    thalData = np.full((len(thal), len(ratesToUse)), np.nan)

    for externalInd, (indRow, row) in enumerate(ac.iterrows()):
        for indKey, key in enumerate(keys):
            acData[externalInd, indKey] = row[key]

    for externalInd, (indRow, row) in enumerate(thal.iterrows()):
        for indKey, key in enumerate(keys):
            thalData[externalInd, indKey] = row[key]

    acMeanPerCell = np.nanmean(acData, axis=1)
    acMeanPerCell = acMeanPerCell[~np.isnan(acMeanPerCell)]
    thalMeanPerCell = np.nanmean(thalData, axis=1)
    thalMeanPerCell = thalMeanPerCell[~np.isnan(thalMeanPerCell)]

    # plt.clf()

    dataMS = 6

    axSummary = plt.subplot(111)
    axSummary.hold(1)

    jitterFrac = 0.2
    pos = jitter(np.ones(len(thalMeanPerCell))*0, jitterFrac)
    axSummary.plot(pos, thalMeanPerCell, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(thalMeanPerCell), 0, 0.5)
    pos = jitter(np.ones(len(acMeanPerCell))*1, jitterFrac)
    axSummary.plot(pos, acMeanPerCell, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(acMeanPerCell), 1, 0.5)
    tickLabels = ['ATh:Str'.format(len(thalMeanPerCell)), 'AC:Str'.format(len(acMeanPerCell))]
    axSummary.set_xticks(range(2))
    axSummary.set_xticklabels(tickLabels)


    # plt.plot(np.zeros(len(acMeanPerCell)), acMeanPerCell, 'o', mec=colorAC, mfc='None')
    # plt.plot(np.ones(len(thalMeanPerCell)), thalMeanPerCell, 'o', mec=colorATh, mfc='None')

    zstat, pVal = stats.mannwhitneyu(thalMeanPerCell, acMeanPerCell)
    print pVal


    axSummary.set_ylabel('Prediction accuracy')
    extraplots.boxoff(axSummary)

    plt.show()

elif CASE==8:

    ### Low and high rates

    dbPath = '/tmp/phaseCalcDatabase.h5'
    db = pd.read_hdf(dbPath, key='dataframe')

    goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
    goodShape = goodISI.query('spikeShapeQuality > 2')
    goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
    goodNSpikes = goodLaser.query('nSpikes>2000')

    ac = goodNSpikes.groupby('brainArea').get_group('rightAC')
    thal = goodNSpikes.groupby('brainArea').get_group('rightThal')

    possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
    ratesToUse = possibleRateKeys
    keys = ['phaseAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

    acData = np.full((len(ac), len(ratesToUse)), np.nan)
    thalData = np.full((len(thal), len(ratesToUse)), np.nan)

    for externalInd, (indRow, row) in enumerate(ac.iterrows()):
        for indKey, key in enumerate(keys):
            acData[externalInd, indKey] = row[key]

    for externalInd, (indRow, row) in enumerate(thal.iterrows()):
        for indKey, key in enumerate(keys):
            thalData[externalInd, indKey] = row[key]

    rateSplit = 22
    indRateSplit = np.where(possibleRateKeys==rateSplit)[0][0]

    acMeanPerCellLow = np.nanmean(acData[:,:indRateSplit], axis=1)
    acMeanPerCellLow = acMeanPerCellLow[~np.isnan(acMeanPerCellLow)]
    acMeanPerCellHigh = np.nanmean(acData[:,indRateSplit:], axis=1)
    acMeanPerCellHigh = acMeanPerCellHigh[~np.isnan(acMeanPerCellHigh)]

    thalMeanPerCellLow = np.nanmean(thalData[:,:indRateSplit], axis=1)
    thalMeanPerCellLow = thalMeanPerCellLow[~np.isnan(thalMeanPerCellLow)]
    thalMeanPerCellHigh = np.nanmean(thalData[:,indRateSplit:], axis=1)
    thalMeanPerCellHigh = thalMeanPerCellHigh[~np.isnan(thalMeanPerCellHigh)]

    plt.clf()
    dataMS = 5
    axSummary = plt.subplot(111)

    jitterFrac = 0.05
    split = 0.1

    pos = jitter(np.zeros(len(thalMeanPerCellLow))-split, jitterFrac)
    axSummary.plot(pos, thalMeanPerCellLow, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(thalMeanPerCellLow), 0-split, 0.1)

    pos = jitter(np.zeros(len(acMeanPerCellLow))+split, jitterFrac)
    axSummary.plot(pos, acMeanPerCellLow, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(acMeanPerCellLow), 0+split, 0.1)

    pos = jitter(np.ones(len(thalMeanPerCellHigh))-split, jitterFrac)
    axSummary.plot(pos, thalMeanPerCellHigh, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(thalMeanPerCellHigh), 1-split, 0.1)

    pos = jitter(np.ones(len(acMeanPerCellHigh))+split, jitterFrac)
    axSummary.plot(pos, acMeanPerCellHigh, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
    medline(np.median(acMeanPerCellHigh), 1+split, 0.1)
    plt.hold(1)



    [zScore, pVal] = stats.mannwhitneyu(acMeanPerCellLow,thalMeanPerCellLow)
    print pVal
    starHeightFactor = 0.1
    starGapFactor = 0.2
    starYfactor = 0.05
    yDataMax = 1
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    starString = None if pVal<0.05 else 'n.s.'
    fontSizeStars = 9
    extraplots.significance_stars([0-split, 0+split], yStars, yStarHeight, starMarker='*',
                                starSize=fontSizeStars, starString=starString,
                                gapFactor=starGapFactor)
    plt.hold(1)


    [zScore, pVal] = stats.mannwhitneyu(acMeanPerCellHigh,thalMeanPerCellHigh)
    print pVal
    # yDataMax = max([max(acDataThisRate), max()])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    starString = None if pVal<0.05 else 'n.s.'
    fontSizeStars = 9
    extraplots.significance_stars([1-split, 1+split], yStars, yStarHeight, starMarker='*',
                                starSize=fontSizeStars, starString=starString,
                                gapFactor=starGapFactor)
    plt.hold(1)



    tickLabels = ['Rate < 22 Hz', 'Rate >= 22Hz']
    axSummary.set_xticks([0, 1])
    axSummary.set_xlim([-0.2, 1.2])
    axSummary.set_xticklabels(tickLabels, rotation=45)

    # plt.plot(np.zeros(len(acMeanPerCell)), acMeanPerCell, 'o', mec=colorAC, mfc='None')
    # plt.plot(np.ones(len(thalMeanPerCell)), thalMeanPerCell, 'o', mec=colorATh, mfc='None')

    axSummary.set_ylabel('Prediction accuracy')
    extraplots.boxoff(axSummary)

    plt.show()


elif CASE==9:

    '''
    Shuffle AM rates and perform calculation 1000 times for each cell
    '''

    SHUFFLE=False #Set to true to shuffle AM rates, giving an estimate of the chance level.

    dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
    dataframe = pd.read_hdf(dbPath, key='dataframe')
    # svmScore = np.empty(len(dataframe))
    for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
        if not 'am' in dbRow['sessionType']:
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print 'BREAKING, AM'
            continue
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am session for cell {}".format(indRow)
            dataframe.loc[indRow, 'svmScore'] = np.nan
            continue

        spikeTimes = ephysData['spikeTimes']

        if len(spikeTimes)<100:
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print "BREAKING, Spikenum"
            continue

        numFreq = len(np.unique(bdata['currentFreq']))

        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)

        ### --- Test to see if there is a response to the AM session --- ###
        baseRange = [-0.5, -0.1]
        responseRange = [0.1, 0.5]
        alignmentRange = [baseRange[0], responseRange[1]]
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


        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        if pVal > 0.05: #No response
            dataframe.loc[indRow, 'svmScore'] = np.nan
            print "Breaking, no significant response"
            continue


        ### --- Calculate best and worst rate
        timeRange = [0, 0.5]
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    timeRange)

        freqEachTrial = bdata['currentFreq']

        shuffleAccuracy = np.empty(1000)

        for indShuffle in range(1000):
            print indShuffle

            if SHUFFLE:
                freqEachTrial = np.random.permutation(freqEachTrial)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
            spikeCountEachTrial = spikeCountMat.flatten()
            if len(freqEachTrial) == len(spikeCountEachTrial)-1:
                spikeCountEachTrial = spikeCountEachTrial[:-1]

            possibleRates = np.unique(freqEachTrial)
            avgSpikesEachRate = np.empty(len(possibleRates))
            for indRate, thisRate in enumerate(possibleRates):
                spikesThisRate = spikeCountEachTrial[freqEachTrial==thisRate]
                avgSpikesEachRate[indRate] = np.mean(spikesThisRate.ravel())

            #Find spikes each trial for pref and nonpref frequencies
            indPref = np.argmax(avgSpikesEachRate)
            indNonPref = np.argmin(avgSpikesEachRate)
            spikesPref = spikeCountEachTrial[freqEachTrial==possibleRates[indPref]]
            spikesNonPref = spikeCountEachTrial[freqEachTrial==possibleRates[indNonPref]]

            maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
            shuffleAccuracy[indShuffle] = maxAccuracy

        dataframe.loc[indRow, 'accuracy'] = np.mean(shuffleAccuracy)
        dataframe.to_hdf('/tmp/2018thstr_with_phase_accuracy.h5', key='dataframe')


elif CASE==10:

    SHUFFLE = False

    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS_MODIFIED_CLU.h5'
    # dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
    dataframe = pd.read_hdf(dbPath, key='dataframe')

    plt.clf()
    for indRow, dbRow in dataframe.iterrows():

        cell = ephyscore.Cell(dbRow)
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            # dataframe.set_value(indRow, 'phaseAccuracy', list(nanAccuracy))
            print "No am for cell {}".format(indRow)
            continue
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
        freqEachTrial = bdata['currentFreq']

        if len(eventOnsetTimes) != len(freqEachTrial):
            if len(eventOnsetTimes) == len(freqEachTrial)+1:
                eventOnsetTimes = eventOnsetTimes[:-1]
            else:
                raise ValueError("Something went wrong with the number of events")

        possibleFreq = np.unique(freqEachTrial)
        nanAccuracy = np.full(len(possibleFreq), np.nan)

        ## Test to see if there is a significant response to AM
        baseRange = [-0.5, -0.1]
        responseRange = [0.1, 0.5]
        alignmentRange = [baseRange[0], responseRange[1]]
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
        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        if pVal > 0.05: #No response
            # dataframe.set_value(indRow, 'phaseAccuracy', list(nanAccuracy))
            print "Breaking, no significant response"
            continue

        print "Calculating for cell {}".format(indRow)

        # spikeTimesFromEventOnset = exampleSpikeTimes[exampleName]
        # trialIndexForEachSpike = exampleTrialIndexForEachSpike[exampleName]
        # indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
        # freqEachTrial = exampleFreqEachTrial[exampleName]

        #Timerange for alignment?
        timeRange = [0.05, 0.5] #Ignoring onset responses TODO: Is this the best way to do this??

        possibleFreq = np.unique(freqEachTrial)
        accuracyEachFreq = []
        for thisFreq in possibleFreq:

            #Only use events for this frequency
            eventsThisFreq = eventOnsetTimes[freqEachTrial==thisFreq]

            (spikeTimesFromEventOnset,
             trialIndexForEachSpike,
             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                           eventsThisFreq,
                                                                           timeRange)

            # period = 1/freq

            # This is really all we need to do to bin things by phase.
            radsPerSec = thisFreq*2*np.pi
            spikeRads = (spikeTimesFromEventOnset*radsPerSec)%(2*np.pi)


            strength, phase = signal.vectorstrength(spikeTimesFromEventOnset, 1.0/thisFreq)
            phase = (phase+2*np.pi)%(2*np.pi)

            shiftedRads = ((spikeRads - phase) + 2.25*np.pi)
            if any(shiftedRads<0):
                raise ValueError("Some shifted rads below 0")
            # shiftedRads = ((spikeRads - phase) + 2.25*np.pi)%(2*np.pi)
            spikeRads = shiftedRads % (2*np.pi)

            nBins=4
            binEdges = np.arange(0, 2.01*np.pi, 2*np.pi/nBins) #The 2.01 makes it actually include 2pi
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeRads,indexLimitsEachTrial,binEdges)

            spikeCountMatCopy = copy.deepcopy(spikeCountMat)

            shuffleAccuracy = np.empty(1000)
            for indShuffle in range(1000):

                print indShuffle
                spikeCountMatShuffle = np.empty(np.shape(spikeCountMatCopy))

                for indMatRow in range(np.shape(spikeCountMatCopy)[0]):
                    numRolls = np.random.choice(range(np.shape(spikeCountMatCopy)[1]))
                    # numRolls = 0
                    spikeCountMatShuffle[indMatRow, :] = np.roll(spikeCountMatCopy[indMatRow, :], numRolls)
                if SHUFFLE:
                    spikeCountMat = spikeCountMatShuffle

                binMeans = np.mean(spikeCountMat, axis=0)
                prefInd = np.argmax(binMeans)
                nonPrefInd = np.argmin(binMeans)

                spikesPref = spikeCountMat[:, prefInd]
                spikesNonPref = spikeCountMat[:, nonPrefInd]

                maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
                shuffleAccuracy[indShuffle] = maxAccuracy
                # print maxAccuracy

            dataframe.set_value(indRow, 'phaseAccuracy_{}Hz'.format(int(thisFreq)), np.mean(shuffleAccuracy))
        # plt.plot(accuracyEachFreq, color=exampleColor[indExample], ls=exampleStyle[indExample])
        # plt.hold(1)
