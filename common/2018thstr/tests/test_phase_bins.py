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

STUDY_NAME = '2018thstr'
FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

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


def spikes_each_period(spikeTimes, period):
    '''
    Generator function that returns the spiketimes in each period timerange
    Args:
        spikeTimes (np.array): The spiketimes, must start at 0
        period (float): length of each period (must be in same units as spikeTimes)
    '''
    start = 0
    end = period
    while start<spikeTimes[-1]:
        spikeTimesThisRange = np.flatnonzero((spikeTimes > start) & (spikeTimes < end))
        yield spikeTimes[spikeTimesThisRange]
        start = end
        end += period

def spikes_each_trial(spikeTimes, trialIndicesEachSpike):
    trialInds = np.unique(trialIndicesEachSpike)
    for trialInd in trialInds:
        spikesThisTrial = np.flatnonzero(trialIndicesEachSpike==trialInd)
        yield spikeTimes[spikesThisTrial]

# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dataframe = pd.read_hdf(dbPath, key='dataframe')

#ITERATE THROUGH ALL CELLS IN THE DATABASE
for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    if not 'am' in dbRow['sessionType']:
        dataframe.loc[indRow, 'mutualInfo'] = np.nan
        print 'BREAKING, AM'
        continue
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
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


    ############## Do for each cell ################
    miEachFreq = []

    for freq, spikeTimesThisFreq, trialIndicesThisFreq in spiketimes_each_frequency(spikeTimesFromEventOnset,
                                                                                    trialIndexForEachSpike,
                                                                                    freqEachTrial):

        #For each AM Rate (freq here):
        period = 1/freq

        binNums = []
        binRates = []
        spikesPerPeriod = []

        #For each trial this AM rate:
        for spikeTimesThisTrial in spikes_each_trial(spikeTimesThisFreq, trialIndicesThisFreq):

            ## Split out spikes in each period
            for indPeriod, spikesThisPeriod in enumerate(spikes_each_period(spikeTimesThisTrial, period)):

                ## Div up into ~6 bins
                ### Subtract indPeriod * period to get spiketimes relative to the start of the period
                spikesThisPeriod = spikesThisPeriod - period * indPeriod
                spikesPerPeriod.append(len(spikesThisPeriod))
                ### Bins to count the spikes are from 0 to period, 6 bins
                nBins = 7
                binEdges = np.linspace(0, period, nBins+1)
                ### Hist spikes into each bin
                hist, binEdges = np.histogram(spikesThisPeriod, bins=binEdges)
                ## Convert to spike rate
                binTime = binEdges[1] #The amount of time in each bin
                hist = hist/binTime
                ## Make list with period number and spike rate
                for indBin, binRate in enumerate(hist):
                    binNums.append(indBin)
                    binRates.append(binRate)

        # print binNums
        # print binRates
        ## Calc MI

        if len(binRates)==0:
            print "Why tf is this happening?? cell ind #{}".format(indRow)
            continue


        binRates = np.array(binRates)
        binNums = np.array(binNums)
        uv, xt = xtab([binRates, binNums])
        mi = metrics.mutual_info_score(None, None, contingency=xt)

        ## Do shuffling and calc random MI bunch of times
        randomMIs = np.empty(500)
        for randomIter in range(500):
            randomBinNums = np.random.permutation(binNums)
            uv, xt = xtab([binRates, randomBinNums])
            mutualInfoRandom = metrics.mutual_info_score(None, None, contingency=xt)
            randomMIs[randomIter] = mutualInfoRandom

        ## Subtract this to get Bias corrected MI for this rate.
        miCorrected = mi - np.mean(randomMIs)
        miCorrectedBits = miCorrected / np.log(2)
        miCorrectedBitsPerSpike = miCorrectedBits / np.mean(spikesPerPeriod)

        dataframe.loc[indRow, 'mutualInfoPhase_{}Hz'.format(int(freq))] = miCorrectedBits
        dataframe.loc[indRow, 'mutualInfoPerSpikePhase_{}Hz'.format(int(freq))] = miCorrectedBitsPerSpike

# savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')

savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU_phase_test.h5')
dataframe.to_hdf(savePath, 'dataframe')
print "SAVED DATAFRAME to {}".format(savePath)


goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
goodNSpikes = goodLaser.query('nSpikes>2000')
ac = goodNSpikes.groupby('brainArea').get_group('rightAC')
thal = goodNSpikes.groupby('brainArea').get_group('rightThal')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

plt.clf()
axSummary = plt.subplot(111)

possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
rateThreshold = 22
ratesToUse = possibleRateKeys[possibleRateKeys>rateThreshold]

colorAC = 'r'
colorATh = 'b'
dataMS=5

# dataframe = dataframe.query("pulsePval<0.05 and trainRatio>0.8")
# ac = dataframe.groupby('brainArea').get_group('rightAC')
# thal = dataframe.groupby('brainArea').get_group('rightThal')

keys = ['mutualInfoPhase_{}Hz'.format(rate) for rate in ratesToUse]

acData = np.full((len(ac), len(ratesToUse)), np.nan)
thalData = np.full((len(thal), len(ratesToUse)), np.nan)

for externalInd, (indRow, row) in enumerate(ac.iterrows()):
    for indKey, key in enumerate(keys):
        acData[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(thal.iterrows()):
    for indKey, key in enumerate(keys):
        thalData[externalInd, indKey] = row[key]

acData = np.nanmean(acData, axis=1)
thalData = np.nanmean(thalData, axis=1)

acData[acData<0]=0
thalData[thalData<0]=0
l
thalPopStat = thalData[~np.isnan(thalData)]
pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
medline(np.median(thalPopStat), 0, 0.5)

acPopStat = acData[~np.isnan(acData)]
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
medline(np.median(acPopStat), 1, 0.5)

plt.title('{} phase bins'.format(nBins))

plt.show()
