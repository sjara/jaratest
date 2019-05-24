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
from sklearn import metrics
from matplotlib import pyplot as plt
import figparams

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
import pandas as pd

FIGNAME = 'figure_frequency_tuning'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

numIntensities = 12

allMI = np.empty((len(db), numIntensities))
allMIperSpike = np.empty((len(db), numIntensities))
allCellInds = np.empty(len(db))

for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    print "Cell {} out of {}".format(indIter, len(db))
    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimes = ephysData['spikeTimes']

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    freqEachTrial = bdata['currentFreq']

    #If there is one more event onset than frequency saved
    if len(freqEachTrial) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:-1]

    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)
    for indinten, inten in enumerate(possibleIntensity):
        selectinds = np.flatnonzero(intensityEachTrial==inten)
        selectedOnsetTimes = eventOnsetTimes[selectinds]
        selectedFreqEachTrial = freqEachTrial[selectinds]
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    selectedOnsetTimes,
                                                                    alignmentRange)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)
        spikeCountEachTrial = spikeCountMat.flatten()

        uv, xt = xtab([spikeCountEachTrial, selectedFreqEachTrial])
        mutualInfo = metrics.mutual_info_score(None, None, contingency=xt)

        randomMIs = np.empty(500)
        for randomIter in range(500):
            randomFreqs = np.random.permutation(selectedFreqEachTrial)
            uv, xt = xtab([spikeCountEachTrial, randomFreqs])
            mutualInfoRandom = metrics.mutual_info_score(None, None, contingency=xt)
            randomMIs[randomIter] = mutualInfoRandom

        mutualInfoBC = mutualInfo - np.mean(randomMIs)
        mutualInfoBCBits = mutualInfoBC / np.log(2)
        allMI[indIter, indinten] = mutualInfoBCBits

        # mutualInfoPerSpike = mutualInfoBC/np.mean(spikeCountEachTrial)
        mutualInfoPerSpikeBits = mutualInfoBCBits/np.mean(spikeCountEachTrial)
        allMIperSpike[indIter, indinten] = mutualInfoPerSpikeBits

        allCellInds[indIter] = indRow


laserCells = db.query('taggedCond==0')
laserThal = laserCells.groupby('brainArea').get_group('rightThal')
laserAC = laserCells.groupby('brainArea').get_group('rightAC')

laserThalInds = np.flatnonzero(np.in1d(allCellInds, laserThal.index.values))
laserACInds = np.flatnonzero(np.in1d(allCellInds, laserAC.index.values))

laserThalMI = allMI[laserThalInds, :]
laserACMI = allMI[laserACInds, :]

laserThalMIperSpike = allMIperSpike[laserThalInds, :]
laserACMIperSpike = allMIperSpike[laserACInds, :]


    # plt.clf()
    # plt.plot(allIntenMI)
    # plt.show()
    # plt.waitforbuttonpress()
