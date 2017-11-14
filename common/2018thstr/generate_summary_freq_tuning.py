import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
import pandas as pd



def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def index_all_true_after(arr):
    '''
    Find the index for a boolean array where all the inds after are True
    Args:
        arr (1-d array of bool): an array of boolean vals
    Returns:
        ind (int): The index of the first True val where all subsequent vals are also True
    '''
    for ind, _ in enumerate(arr):
        miniarr = arr[ind:]
        if np.all(miniarr):
            return ind

def calculate_tuning_curve_params(dataframe):

    #Tuning curve estimation
    #DONE: Need to make this method use the continuous curves we fit

    cfs = np.full(len(dataframe), np.nan)
    thresholds = np.full(len(dataframe), np.nan)
    lowerFreqs = np.full(len(dataframe), np.nan)
    upperFreqs = np.full(len(dataframe), np.nan)

    noTCinds = []
    runtimeErrorInds = []
    noFreqAboveThreshInds = []
    no10dbAboveInds = []


    for indCell, cell in dataframe.iterrows():
        try:
            spikeData, eventData = celldatabase.get_session_ephys(cell, 'tc')
            bdata = celldatabase.get_session_bdata(cell, 'tc')
        except IndexError: #The cell does not have a tc
            print "No tc for cell {}".format(indCell)
            noTCinds.append(indCell)
            thresholds[indCell] = None
            cfs[indCell] = None
            lowerFreqs[indCell] = None
            upperFreqs[indCell] = None
            continue

        eventOnsetTimes = eventData.get_event_onset_times()

        if spikeData.timestamps is not None:

            baseRange = [-0.2, 0]
            responseRange = [0, 0.2]
            alignmentRange = [baseRange[0], responseRange[1]]
            freqEachTrial = bdata['currentFreq']
            possibleFreq = np.unique(freqEachTrial)
            intensityEachTrial = bdata['currentIntensity']
            possibleIntensity = np.unique(intensityEachTrial)
            allBaselineCountArrays = []
            aboveBaseline = []
            popts = []

            for indinten, inten in enumerate(possibleIntensity):
                spks = np.array([])
                # inds = np.array([])
                freqs = np.array([])
                base = np.array([])
                for indfreq, freq in enumerate(possibleFreq):
                    selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
                    selectedOnsetTimes = eventOnsetTimes[selectinds]
                    (spikeTimesFromEventOnset,
                    trialIndexForEachSpike,
                    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
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

                allBaselineCountArrays.append(base)

                #DONE: Finish setting the initial param guesses and bounds for fitting in log2(freq) space
                try:
                    popt, pcov = optimize.curve_fit(gaussian, #Fit the curve for this intensity
                                                    np.log2(freqs),
                                                    spks,
                                                    p0=[1, np.log2(possibleFreq[7]), 1],
                                                    bounds=([0, np.log2(possibleFreq[0]), 0],
                                                            [inf, np.log2(possibleFreq[-1]), inf]))
                    popts.append(popt) #Save the curve paramaters
                except RuntimeError:
                    print "RUNTIME ERROR, Cell {}".format(indCell)
                    runtimeErrorInds.append(indCell)
                    thresholds[indCell] = None
                    cfs[indCell] = None
                    lowerFreqs[indCell] = None
                    upperFreqs[indCell] = None
                    break

                #Save whether the max fitted val of the curve is greater than base+1s.d.
                #This is discrete, we want to maximize on the continuous function
                # aboveBaseline.append(max(gaussian(inds, *popt)) > base.mean()+base.std())
                #DONE: This needs to be finished after I change to fitting in log(freq) space
                fm = lambda x: -gaussian(x, *popt)
                r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))
                # maxX = 2**r["x"] #The max x val is a log2(freq) value, so convert back to freq
                # aboveBaseline.append(gaussian(r["x"], *popt)>(base.mean()+base.std()))
                aboveBaseline.append(gaussian(r["x"], *popt)>(2*base.mean()))

            aboveBaseline = np.array(aboveBaseline)
            indintenFirstAbove = index_all_true_after(aboveBaseline)
            #TODO: I need to find the max for THIS curve and save that as cf
            #TODO: Need to save the intensity
            if indintenFirstAbove is None:
                #No frequencies pass the threshold
                threshold = None
                cf = None
                noFreqAboveThreshInds.append(indCell)
                continue
            else:
                threshold = possibleIntensity[indintenFirstAbove]
                #Find the max for the threshold intensity
                poptFirstAbove = popts[indintenFirstAbove]
                fm = lambda x: -gaussian(x, *poptFirstAbove)
                r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))
                cf = 2**r["x"] #The max x val is a log2(freq) value, so convert back to freq

            indinten10aboveThresh = indintenFirstAbove+2
            baselineAllIntensities = np.concatenate(allBaselineCountArrays)

            try:
                popt10Above = popts[indinten10aboveThresh]
                #TODO: using this set of popts, find the point where the curve crosses y=base.mean+base.std
                #We need to find the max using these popts as well so we know the midpoint
                fm = lambda x: -gaussian(x, *popt10Above)
                r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))

                xMax = r["x"]

                #The function to find roots for. curve minus the baseline+std
                # fr = lambda x: gaussian(x, *popt10Above) - (baselineAllIntensities.mean()+baselineAllIntensities.std())
                fr = lambda x: gaussian(x, *popt10Above) - (2*baselineAllIntensities.mean())

                #Check the inputs first. fr(a) and fr(b) need to be opposite sign for root finding to work
                #Lower root finding
                alower = np.log2(possibleFreq[0]) #The minimum x val
                blower = xMax #The x value of the function max
                if np.sign(fr(alower)) != np.sign(fr(blower)):
                    rootLower = optimize.brentq(fr, alower, blower)
                    lowerFreq = 2**rootLower
                else:
                    lowerFreq = None

                #Upper root
                aupper = xMax #The minimum x val
                bupper = np.log2(possibleFreq[-1]) #The x value of the function max
                if np.sign(fr(aupper)) != np.sign(fr(bupper)):
                    rootUpper = optimize.brentq(fr, aupper, bupper)
                    upperFreq = 2**rootUpper
                else:
                    upperFreq = None
            except IndexError:
                #We were not able to catch 10db above threshold. In this case, we can still get cf and thresh, but not uF/lF
                no10dbAboveInds.append(indCell)
                upperFreq = None
                lowerFreq = None
                continue

            #Things to save
            thresholds[indCell] = threshold
            cfs[indCell] = cf
            lowerFreqs[indCell] = lowerFreq
            upperFreqs[indCell] = upperFreq

        else:
            thresholds[indCell] = None
            cfs[indCell] = None
            lowerFreqs[indCell] = None
            upperFreqs[indCell] = None

    dataframe['threshold'] = thresholds
    dataframe['cf'] = cfs
    dataframe['lowerFreq'] = lowerFreqs
    dataframe['upperFreq'] = upperFreqs

    return noTCinds, runtimeErrorInds, noFreqAboveThreshInds, no10dbAboveInds

if __name__=="__main__":

    dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
    db = pd.read_hdf(dbPath, key='dataframe')
    noTCinds, runtimeErrorInds, noFreqAboveThreshInds, no10dbAboveInds = calculate_tuning_curve_params(db)

