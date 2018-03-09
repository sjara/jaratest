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


'''
References for this method:
Phillips and Hasenstaub 2016: https://elifesciences.org/articles/18383
General formula for MI plus a method for correcting for the bias that you get when you have smaller sample sizes.

Stack overflow post on using sklearn.mutual_info function (how to feed in the contingency table, nats instead of bits, etc.)

How to estimate the contingency table (2d joint probability distribution)
'''

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)


def calc_MI(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    1/0
    mi = metrics.mutual_info_score(None, None, contingency=c_xy)
    return mi


#I got this from this gist: https://gist.github.com/alexland/d6d64d3f634895b9dc8e
#I haven't had a chance to test it thoroughly, but it works on some examples
def xtab(cols, apply_wt=False):
    '''
    returns:
    (i) xt, NumPy array storing the xtab results, number of dimensions is equal to 
        the len(args) passed in
    (ii) unique_vals_all_cols, a tuple of 1D NumPy array for each dimension 
        in xt (for a 2D xtab, the tuple comprises the row and column headers)
    pass in:
        (i) 1 or more 1D NumPy arrays of integers
        (ii) if wts is True, then the last array in cols is an array of weights

    if return_inverse=True, then NP.unique also returns an integer index 
    (from 0, & of same len as array passed in) such that, uniq_vals[idx] gives the original array passed in
    higher dimensional cross tabulations are supported (eg, 2D & 3D)
    cross tabulation on two variables (columns):
    >>> q1 = NP.array([7, 8, 8, 8, 5, 6, 4, 6, 6, 8, 4, 6, 6, 6, 6, 8, 8, 5, 8, 6])
    >>> q2 = NP.array([6, 4, 6, 4, 8, 8, 4, 8, 7, 4, 4, 8, 8, 7, 5, 4, 8, 4, 4, 4])
    >>> uv, xt = xtab(q1, q2)
    >>> uv
    (array([4, 5, 6, 7, 8]), array([4, 5, 6, 7, 8]))
    >>> xt
    array([[2, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 2, 4],
            [0, 0, 1, 0, 0],
            [5, 0, 1, 0, 1]], dtype=uint64)
    '''
    if not all(len(col) == len(cols[0]) for col in cols[1:]):
        raise ValueError("all arguments must be same size")

    if len(cols) == 0:
        raise TypeError("xtab() requires at least one argument")

    fnx1 = lambda q: len(q.squeeze().shape)
    if not all([fnx1(col) == 1 for col in cols]):
        raise ValueError("all input arrays must be 1D")

    if apply_wt:
        cols, wt = cols[:-1], cols[-1]
    else:
        wt = 1

    uniq_vals_all_cols, idx = zip( *(np.unique(col, return_inverse=True) for col in cols) )
    shape_xt = [uniq_vals_col.size for uniq_vals_col in uniq_vals_all_cols]
    dtype_xt = 'float' if apply_wt else 'uint'
    xt = np.zeros(shape_xt, dtype=dtype_xt)
    np.add.at(xt, idx, wt)
    return uniq_vals_all_cols, xt


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

        uv, xt = xtab([spikeCountEachTrial, freqEachTrial])
        mi = metrics.mutual_info_score(None, None, contingency=xt)

        print exampleName
        print "MI (bits/trial): {}".format(mi)
        print "bits/spike: {}".format(mi/np.mean(spikeCountEachTrial))


######### Full dataset #########
if CASE==1:

    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
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


        # timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses
        timeRange = [0, 0.5] 
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

        uv, xt = xtab([spikeCountEachTrial, freqEachTrial])
        mutualInfo = metrics.mutual_info_score(None, None, contingency=xt)

        randomMIs = np.empty(500)
        for randomIter in range(500):
            randomFreqs = np.random.permutation(freqEachTrial)
            uv, xt = xtab([spikeCountEachTrial, randomFreqs])
            mutualInfoRandom = metrics.mutual_info_score(None, None, contingency=xt)
            randomMIs[randomIter] = mutualInfoRandom

        mutualInfoBC = mutualInfo - np.mean(randomMIs)
        mutualInfoBCBits = mutualInfoBC / np.log(2)
        mutualInfoPerSpike = mutualInfoBC/np.mean(spikeCountEachTrial)
        mutualInfoPerSpikeBits = mutualInfoBCBits/np.mean(spikeCountEachTrial)

        dataframe.loc[indRow, 'mutualInfoBCBits'] = mutualInfoBCBits
        dataframe.loc[indRow, 'mutualInfoPerSpikeBits'] = mutualInfoPerSpikeBits

savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dataframe.to_hdf(savePath, 'dataframe')
print "SAVED DATAFRAME to {}".format(savePath)


#Stats
goodLaser = dataframe.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
ac = goodLaser.groupby('brainArea').get_group('rightAC')
thal = goodLaser.groupby('brainArea').get_group('rightThal')

acMI = ac['mutualInfoBC'][pd.notnull(ac['mutualInfoBC'])]
thalMI = thal['mutualInfoBC'][pd.notnull(thal['mutualInfoBC'])]

acMIps = ac['mutualInfoPerSpike'][pd.notnull(ac['mutualInfoPerSpike'])]
thalMIps = thal['mutualInfoPerSpike'][pd.notnull(thal['mutualInfoPerSpike'])]

plt.clf()
plt.subplot(121)
plt.boxplot([acMI, thalMI])
ax = plt.gca()
ax.set_xticklabels(['AC->Str', 'ATh->Str'])
ax.set_ylabel('MI (nats/trial)')
st, pval = stats.ranksums(acMI, thalMI)
plt.title('p = {}'.format(pval))

plt.subplot(122)
plt.boxplot([acMIps, thalMIps])
ax = plt.gca()
ax.set_xticklabels(['AC->Str', 'ATh->Str'])
ax.set_ylabel('MI (nats/spike)')
st, pval = stats.ranksums(acMIps, thalMIps)
plt.title('p = {}'.format(pval))
plt.show()




