import pandas as pd
from scipy import signal
from scipy import stats
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import ephyscore
import figparams
from matplotlib import pyplot as plt
import os

STUDY_NAME = '2018thstr'

# def angle_population_vector(angles):
#     '''
#         Compute the complex population mean vector from a set of angles
#         Mean over Axis 0
#     '''
#     return np.mean(np.exp(1j*angles), axis=0)

# def angle_population_R(angles=None, angle_population_vec=None, weights=None):
#     '''
#         Compute R, the length of the angle population complex vector.
#         Used to compute Standard deviation and diverse tests.
#         If weights is provided, computes a weighted population mean vector instead.
#     '''
#     if angle_population_vec is None:
#         if weights is None:
#             angle_population_vec = angle_population_vector(angles)
#         else:
#             angle_population_vec = angle_population_vector_weighted(angles, weights)
#     return np.abs(angle_population_vec)

def index_all_true_before(arr):
    '''
    Find the index for a boolean array where all the inds after are True
    Args:
        arr (1-d array of bool): an array of boolean vals
    Returns:
        ind (int): The index of the first True val where all subsequent vals are also True
    '''
    if any(~arr):
        indLastTrue = np.min(np.where(~arr))-1
    else:
        indLastTrue = len(arr)-1
    return indLastTrue

def angle_population_vector_zar(angles):
    '''
    Copied directly from Biostatistical analysis, Zar, 3rd ed, pg 598 (Mike W has this book)
    Computes the length of the mean vector for a population of angles
    '''
    X = np.mean(np.cos(angles))
    Y = np.mean(np.sin(angles))
    r = np.sqrt(X**2 + Y**2)
    return r

def rayleigh_test(angles):
    '''
        Performs Rayleigh Test for non-uniformity of circular data.
        Compares against Null hypothesis of uniform distribution around circle
        Assume one mode and data sampled from Von Mises.
        Use other tests for different assumptions.
        Maths from [Biostatistical Analysis, Zar].
    '''
    if angles.ndim > 1:
        angles = angles.flatten()
    N = angles.size
    # Compute Rayleigh's R
    R = N*angle_population_vector_zar(angles)
    # Compute Rayleight's z
    zVal = R**2. / N
    # Compute pvalue (Zar, Eq 27.4)
    pVal = np.exp(np.sqrt(1. + 4*N + 4*(N**2. - R**2)) - 1. - 2.*N)
    return zVal, pVal

def spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, freqEachTrial):
    '''
    Generator func to return the spiketimes/trial indices for trials of each frequency
    '''
    possibleFreq = np.unique(freqEachTrial)
    for freq in possibleFreq:
        trialsThisFreq = np.flatnonzero(freqEachTrial==freq)
        spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        trialIndicesThisFreq = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        yield (freq, spikeTimesThisFreq, trialIndicesThisFreq)

CASE=1
SAVE=True

significantFreqsArray = np.array([])


# if CASE==0:
#     cell = {'subject':'pinp015',
#             'date':'2017-02-15',
#             'depth':2902,
#             'tetrode':8,
#             'cluster':6}
#     dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
#     db = pd.read_hdf(dbPath, key='dataframe')
#     #TODO: Define these
#     # eventID =
#     # eventChannel =
#     cell = find_cell(db, cell['subject'], cell['date'], cell['depth'], cell['tetrode'], cell['cluster']).iloc[0]
#     spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
#     eventOnsetTimes = eventData.get_event_onset_times(eventID=1, eventChannel=5)
#     eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)
#     bdata = celldatabase.get_session_bdata(cell, 'am')
#     timeRange = [-0.2, 0.7]
#     spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
#         spikeData.timestamps, eventOnsetTimes, timeRange)
#     freqEachTrial = bdata['currentFreq']
#     plt.figure()
#     for spiketimes, trialInds in spiketimes_each_frequency(spikeTimesFromEventOnset,
#                                                            trialIndexForEachSpike,
#                                                            freqEachTrial):
#         plt.clf()
#         plt.plot(spiketimes, trialInds, '.')
#         plt.show()
#         plt.waitforbuttonpress()

if CASE==1:
    # dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
    # dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
    # dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
    dbPath = '/tmp/celldatabase_new_20180830.h5'
    dataframe = pd.read_hdf(dbPath, key='dataframe')


    for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
        if not 'am' in dbRow['sessionType']:
            dataframe.loc[indRow, 'highestSync'] = np.nan
            print 'BREAKING, AM'
            continue
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am session for cell {}".format(indRow)
            dataframe.loc[indRow, 'highestSync'] = np.nan
            continue

        spikeTimes = ephysData['spikeTimes']

        if len(spikeTimes)<100:
            dataframe.loc[indRow, 'highestSync'] = np.nan
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
            dataframe.loc[indRow, 'highestSync'] = np.nan
            print "Breaking, no significant response"
            continue
        ### ------------------------------------------------------------ ###

        ### --- Calculate vector strength and significance --- ###
        timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    timeRange)
        freqEachTrial = bdata['currentFreq']
        for indFreq, (freq, spiketimes, trialInds) in enumerate(spiketimes_each_frequency(spikeTimesFromEventOnset,
                                                                                        trialIndexForEachSpike,
                                                                                        freqEachTrial)):
            strength, phase = signal.vectorstrength(spiketimes, 1.0/freq)
            # vsArr = np.concatenate((vsArr, np.array([strength])))

            #TODO: Check the math here
            radsPerSec=freq*2*np.pi
            spikeRads = (spiketimes*radsPerSec)%(2*np.pi)
            ral = np.array([2*len(spiketimes)*(strength**2)])

            #NOTE: I checked the math in this function using the text referenced (Mike W. has a copy if needed)
            zVal, pVal = rayleigh_test(spikeRads)

            allFreqVS[indFreq] = strength
            allFreqRal[indFreq] = ral
            allFreqPval[indFreq] = pVal

            # # pValArr = np.concatenate((pValArr, np.array([pVal])))
            # allFreqPval.append(pVal)

            # # ralArr = np.concatenate((ralArr, np.array([ral])))
            # allFreqRal.append(ral)

        possibleFreq = np.unique(freqEachTrial)
        if any(allFreqPval<0.05):
            sigPvals = np.array(allFreqPval)<0.05
            highestSyncInd = index_all_true_before(sigPvals)
            dataframe.loc[indRow, 'highestSync'] = possibleFreq[allFreqPval<0.05].max()
            dataframe.loc[indRow, 'highestUSync'] = possibleFreq[highestSyncInd]
            # print possibleFreq[pValThisCell<0.05].max()
        else:
            dataframe.loc[indRow, 'highestSync'] = 0
            # print 'ZERO'
        correctedPval = 0.05/len(possibleFreq)
        if any(allFreqPval<correctedPval):
            dataframe.loc[indRow, 'highestSyncCorrected'] = possibleFreq[allFreqPval<correctedPval].max()
            freqsBelowThresh = allFreqPval<correctedPval
            freqsBelowThresh = freqsBelowThresh.astype(int)
            if len(significantFreqsArray)==0:
                significantFreqsArray = freqsBelowThresh
            else:
                # significantFreqsArray = np.concatenate([[significantFreqsArray], [freqsBelowThresh]])
                significantFreqsArray = np.vstack((significantFreqsArray, freqsBelowThresh))
        else:
            dataframe.loc[indRow, 'highestSyncCorrected'] = 0

    if SAVE:
        # savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
        dataframe.to_hdf(dbPath, 'dataframe')
        print "SAVED DATAFRAME to {}".format(dbPath)

        # saveDataArrayPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'significantFreqsArray.npy')
        # np.save(saveDataArrayPath, significantFreqsArray)
