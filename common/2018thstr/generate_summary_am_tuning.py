import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from collections import Counter
from scipy import stats
import pandas as pd
import figparams
reload(figparams)
from sklearn import metrics

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

def calc_MI(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = metrics.mutual_info_score(None, None, contingency=c_xy)
    return mi

CASE=1

########### Testing on examples #################
if CASE==0:

    exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
    exampleData = np.load(exampleDataPath)

    exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
    exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
    exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
    exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

    # exampleName = 'Thal1'
    exampleNames = ['Thal1', 'Thal2', 'AC1', 'AC2']
    # exampleNames = ['AC1']
    plt.clf()
    for exampleName in exampleNames:

        spikeTimesFromEventOnset = exampleSpikeTimes[exampleName]
        trialIndexForEachSpike = exampleTrialIndexForEachSpike[exampleName]
        indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
        freqEachTrial = exampleFreqEachTrial[exampleName]

        timeRange = [0.1, 0.5]
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        spikeCountEachTrial = spikeCountMat.flatten()
        spikeCountEachTrial = spikeCountEachTrial[:-1]




        plt.hold(1)
    plt.legend()
    plt.show()


######### Full dataset #########
if CASE==1:

    # dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
    dataframe = pd.read_hdf(dbPath, key='dataframe')
    for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
        if not 'am' in dbRow['sessionType']:
            dataframe.loc[indRow, 'mutualInfo'] = np.nan
            print 'BREAKING, AM'
            continue
        cell = ephyscore.Cell(dbRow)
        # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am session for cell {}".format(indRow)
            dataframe.loc[indRow, 'mutualInfo'] = np.nan
            continue

        spikeTimes = ephysData['spikeTimes']

        if len(spikeTimes)<100:
            dataframe.loc[indRow, 'mutualInfo'] = np.nan
            print "BREAKING, Spikenum"
            continue

        numFreq = len(np.unique(bdata['currentFreq']))

        allFreqVS = np.empty(numFreq)
        allFreqRal = np.empty(numFreq)
        allFreqPval = np.empty(numFreq)

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
            dataframe.loc[indRow, 'mutualInfo'] = np.nan
            print "Breaking, no significant response"
            continue


        timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    timeRange)

        freqEachTrial = bdata['currentFreq']
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        spikeCountEachTrial = spikeCountMat.flatten()
        if len(freqEachTrial) == len(spikeCountEachTrial)-1:
            spikeCountEachTrial = spikeCountEachTrial[:-1]
        nBins=50
        mi = calc_MI(spikeCountEachTrial, freqEachTrial, bins=nBins)
        mutualInfo = mi
        mutualInfoPerSpike = mi/sum(spikeCountEachTrial)
        dataframe.loc[indRow, 'mutualInfo'] = mutualInfo
        dataframe.loc[indRow, 'mutualInfoPerSpike'] = mutualInfoPerSpike
