import pandas as pd
from scipy import signal
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from jaratoolbox import settings
import figparams
from matplotlib import pyplot as plt
import os

STUDY_NAME = '2018thstr'

def angle_population_vector(angles):
    '''
        Compute the complex population mean vector from a set of angles
        Mean over Axis 0
    '''
    return np.mean(np.exp(1j*angles), axis=0)

def angle_population_R(angles=None, angle_population_vec=None, weights=None):
    '''
        Compute R, the length of the angle population complex vector.
        Used to compute Standard deviation and diverse tests.
        If weights is provided, computes a weighted population mean vector instead.
    '''
    if angle_population_vec is None:
        if weights is None:
            angle_population_vec = angle_population_vector(angles)
        else:
            angle_population_vec = angle_population_vector_weighted(angles, weights)
    return np.abs(angle_population_vec)

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
    R = N*angle_population_R(angles)
    # Compute Rayleight's z
    zVal = R**2. / N
    # Compute pvalue (Zar, Eq 27.4)
    pVal = np.exp(np.sqrt(1. + 4*N + 4*(N**2. - R**2)) - 1. - 2.*N)
    return zVal, pVal

# timeRange = [0, 0.5]
# spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
#     spikeTimestamps, eventOnsetTimes, timeRange)
# freqEachTrial = behavData['currentFreq']
# squeezedinds=np.array([list(np.unique(selectinds)).index(x) for x in selectinds])

def AM_vector_strength(spikeTimesFromEventOnset, behavData, ignoreBefore=0.03):
    '''
    Compute the vector strength

    '''
    currentFreq = behavData['currentFreq']
    possibleFreq = np.unique(currentFreq)
    vs_array=np.array([])
    ral_array=np.array([])
    pval_array = np.array([])
    for freq in possibleFreq:
        select = np.flatnonzero(currentFreq==freq)
        selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
        selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
        squeezedinds=np.array([list(np.unique(selectinds)).index(x) for x in selectinds])
        spikesAfterFirstCycle = selectspikes[selectspikes>ignoreBefore]
        indsAfterFirstCycle = selectinds[selectspikes>ignoreBefore]

        strength, phase = signal.vectorstrength(spikesAfterFirstCycle, 1.0/freq)
        vs_array=np.concatenate((vs_array, np.array([strength])))

        #Compute the pval for the vector strength
        radsPerSec=freq*2*np.pi
        spikeRads = (spikesAfterFirstCycle*radsPerSec)%(2*np.pi)
        ral_test = rayleigh_test(spikeRads)
        pval = np.array([ral_test['pvalue']])
        ral =np.array([2*len(spikesAfterFirstCycle)*(strength**2)])
        pval_array = np.concatenate((pval_array, pval))
        ral_array = np.concatenate((ral_array, ral))
    return vs_array, pval_array, ral_array

#TODO: not needed after example testing
def find_cell(dataframe, subject, date, depth, tetrode, cluster):
    cell = dataframe.query("subject==@subject and date==@date and depth==@depth and tetrode==@tetrode and cluster==@cluster")
    return cell

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
if CASE==0:
    cell = {'subject':'pinp015',
            'date':'2017-02-15',
            'depth':2902,
            'tetrode':8,
            'cluster':6}
    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
    db = pd.read_hdf(dbPath, key='dataframe')
    #TODO: Define these
    # eventID =
    # eventChannel =
    cell = find_cell(db, cell['subject'], cell['date'], cell['depth'], cell['tetrode'], cell['cluster']).iloc[0]
    spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times(eventID=1, eventChannel=5)
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)
    bdata = celldatabase.get_session_bdata(cell, 'am')
    timeRange = [-0.2, 0.7]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeData.timestamps, eventOnsetTimes, timeRange)
    freqEachTrial = bdata['currentFreq']
    plt.figure()
    for spiketimes, trialInds in spiketimes_each_frequency(spikeTimesFromEventOnset,
                                                           trialIndexForEachSpike,
                                                           freqEachTrial):
        plt.clf()
        plt.plot(spiketimes, trialInds, '.')
        plt.show()
        plt.waitforbuttonpress()

if CASE==1:
    # dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
    dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
    db = pd.read_hdf(dbPath, key='dataframe')

    #FOR TESTING
    # db = db[:5]

    numFreq = 11
    allFreqVS = np.empty((len(db), numFreq))
    allFreqRal = np.empty((len(db), numFreq))
    allFreqPval = np.empty((len(db), numFreq))

    for indCell, cell in db.iterrows():
        if not 'am' in cell['sessiontype']:
            db.loc[indCell, 'highestSync'] = np.nan
            print 'BREAKING, AM'
            continue
        spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
        if spikeData.timestamps is None:
            db.loc[indCell, 'highestSync'] = np.nan
            print "BREAKING, no spike data"
            continue
        if len(spikeData.timestamps)<100:
            db.loc[indCell, 'highestSync'] = np.nan
            print "BREAKING, Spikenum"
            continue
        eventOnsetTimes = eventData.get_event_onset_times(eventID=1, eventChannel=5)
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)
        bdata = celldatabase.get_session_bdata(cell, 'am')
        timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses

        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
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

            allFreqVS[indCell, indFreq] = strength
            allFreqRal[indCell, indFreq] = ral
            allFreqPval[indCell, indFreq] = pVal

            # # pValArr = np.concatenate((pValArr, np.array([pVal])))
            # allFreqPval.append(pVal)

            # # ralArr = np.concatenate((ralArr, np.array([ral])))
            # allFreqRal.append(ral)

        pValThisCell = allFreqPval[indCell, :]
        possibleFreq = np.unique(freqEachTrial)
        if any(pValThisCell<0.05):
            db.loc[indCell, 'highestSync'] = possibleFreq[pValThisCell<0.05].max()
            print possibleFreq[pValThisCell<0.05].max()
        else:
            db.loc[indCell, 'highestSync'] = 0
            print 'ZERO'
    if SAVE:
        savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
        db.to_hdf(savePath, 'dataframe')
        print "SAVED DATAFRAME to {}".format(savePath)


