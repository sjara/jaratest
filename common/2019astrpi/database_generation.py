"""
Generate and save database of parameters and stats for each recorded cell.

Run as:
python3 database_generation.py RUNMODE SUBJECT

where RUNMODE can be:
- concat: grab all mouse names in studyparams.py, load all dataframes, and
          concatenate all the dataframes together to make the full database.
- basic: generate only the minimum dataframe from the inforecs, no other
        other information is added.
- locations: generate only the minimum dataframe from the inforecs and find
          the anatomical location of each cell.
- stats: generate a dataframe and append base stats to it for each session type.
          It does not estimate anatomical locations.
- all: calculate both "stats" and "locations"

and SUBJECT can be either a singular mouse or the word 'all',
which will use the mouse list in studyparams.py
"""

import os
import sys
import numpy as np
import pandas as pd
import studyparams
from scipy import stats
from scipy import signal
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratoolbox import histologyanalysis
import database_generation_funcs as funcs


SAVE = 1


def append_base_stats(cellDB, filename=''):
    """
    Calculate parameters to be used to filter cells in calculate_indices
    """

    # FILTERING DATAFRAME
    firstCells = cellDB.query(studyparams.FIRST_FLTRD_CELLS)  # isiViolations < 0.02 and spikeShapeQuality > 2.5

    for indIter, (indRow, dbRow) in enumerate(firstCells.iterrows()):

        sessions = dbRow['sessionType']
        oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

        print("Now processing ", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster'],
              indRow)
        print("Sessions tested in this cell are(is) ", sessions)

        # -------------- Noiseburst data calculations -------------------------
        session = 'noiseburst'
        try:
            noiseEphysData, noBData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            baseRange = [-0.1, 0]  # Time range for baseline firing calculations
            noiseEventOnsetTimes = noiseEphysData['events']['soundDetectorOn']
            noiseSpikeTimes = noiseEphysData['spikeTimes']
            nspkBaseNoise, nspkRespNoise = funcs.calculate_firing_rate(noiseEventOnsetTimes, noiseSpikeTimes, baseRange)

            # Significance calculations for the noiseburst
            try:
                zStats, pVals = stats.mannwhitneyu(nspkRespNoise, nspkBaseNoise, alternative='two-sided')
            except ValueError:  # All numbers identical will cause mann-whitney to fail, therefore p-value should be 1 as there is no difference
                zStats, pVals = [0, 1]

            # Adding noiseburst values to the dataframe
            cellDB.at[indRow, '{}_pVal'.format(session)] = pVals  # p-value from Mann-Whitney U test
            cellDB.at[indRow, '{}_ZStat'.format(session)] = zStats  # U-statistic from Mann-Whitney U test
            # If we want to save the spikes themselves, we must convert the 'nspkBase' variables to a pandas series to
            # store it in the DF. We must then use Series.to_list() after to use the data normally again. Instead I just
            # saved the mean of spikes below as it was good enough for what I needed
            cellDB.at[indRow, '{}_baselineFR'.format(session)] = np.mean(nspkBaseNoise) # mean firing rate (formally called noiseburst_FR)
            cellDB.at[indRow, '{}_responseFR'.format(session)] = np.mean(nspkRespNoise)  # mean response firing rate

        # ------------ Laserpulse calculations --------------------------------
        session = 'laserpulse'
        try:
            pulseEphysData, noBData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            baseRange = [-0.1, 0]  # Originally this used [-0.05, -0.04]
            laserEventOnsetTimes = pulseEphysData['events']['laserOn']
            laserSpikeTimes = pulseEphysData['spikeTimes']
            nspkBaseLaser, nspkRespLaser = funcs.calculate_firing_rate(laserEventOnsetTimes, laserSpikeTimes, baseRange)
            respSpikeMeanLaser = np.mean(nspkRespLaser)
            baseSpikeMeanLaser = np.mean(nspkBaseLaser)
            changeFiring = respSpikeMeanLaser - baseSpikeMeanLaser  # Used to ID if cell inc or dec FR from laser

            # Significance calculations for the laserpulse
            try:
                zStats, pVals = stats.mannwhitneyu(nspkRespLaser, nspkBaseLaser, alternative='two-sided')
            except ValueError:  # All numbers identical will cause mann-whitney to fail
                zStats, pVals = [0, 1]

            # Adding laserpulse calculations to the dataframe
            cellDB.at[indRow, '{}_pVal'.format(session)] = pVals  # p-value from Mann-Whitney U test
            cellDB.at[indRow, '{}_ZStat'.format(session)] = zStats  # U-statistic from Mann-Whitney U test
            cellDB.at[indRow, '{}_dFR'.format(session)] = changeFiring  # Difference between base and response firing rate
            cellDB.at[indRow, '{}_baselineFR'.format(session)] = baseSpikeMeanLaser  # Mean of baseline firing rate
            cellDB.at[indRow, '{}_responseFR'.format(session)] = respSpikeMeanLaser  # Mean of response firing rate

        # -------------- Tuning curve calculations ----------------------------
        session = 'tuningCurve'
        try:
            tuningEphysData, tuningBehavData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            baseRange = [-0.1, 0]  # Time used for baseline spike counts.

            # Extracting information from ephys and behavior data to do calculations later with
            currentFreq = tuningBehavData['currentFreq']  # The frequency for each individual trial
            currentIntensity = tuningBehavData['currentIntensity']  # The intensity for each individual trial
            uniqFreq = np.unique(currentFreq)  # List of frequencies used for presentations, no repeats
            uniqueIntensity = np.unique(currentIntensity)  # List of intensities used for presentatiosn, no repeats
            tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq,
                                                                                 currentIntensity, uniqueIntensity)
            # Output of above is [trial:frequency:intensity]

            allIntenBase = np.array([])  # A list to collect the baseline spikes across all intensities
            respSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))  # same as allIntenBase, but for response
            Rsquareds = []  # Collection of rsquared values
            popts = []  # Collection of optimal fit parameters for the Gaussians
            tuningSpikeTimes = tuningEphysData['spikeTimes']
            tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
            tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes,
                                                                            minEventOnsetDiff=0.2)
            # The above line is used to remove small errors in the sound detector reporting events, especially in AM

            # Checking to see if the ephys data has one more trial than the behavior data and removing the last session if it does
            if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
                tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
                print("Correcting ephys data to be same length as behavior data")
                toCalculate = True
            elif len(tuningEventOnsetTimes) == len(currentFreq):
                print("Data is already the same length")
                toCalculate = True
            else:
                print("Something is wrong with the length of these data")
                toCalculate = False
                #TODO: Instead of generating an error I made it just not calculate statistics. I should posisbly have it
                #  log all mice and sites where it failed to calculate so someone can review later

        # -------------------- Start of calculations for the tuningCurve data -------------------------
            # The latency of the cell from the onset of the stim
            if toCalculate:
                tuningZStat, tuningPVal = \
                    funcs.sound_response_any_stimulus(tuningEventOnsetTimes, tuningSpikeTimes,
                                                      tuningTrialsEachCond[:, :, -1], timeRange=[0.0, 0.05],
                                                      baseRange=[-0.05, 0])  # All trials at all frequencies at the highest intensity
                try:
                    respLatency = funcs.calculate_latency(tuningEventOnsetTimes, currentFreq, uniqFreq, currentIntensity,
                                                          uniqueIntensity, tuningSpikeTimes)
                except IndexError:
                    print("Index error for cell {}".format(indRow))  # If there are no spikes in the timeRangeForLatency
                    respLatency = np.nan

                if tuningPVal > 0.05/len(uniqFreq):
                    toCalculate = False  # Excludes doing calculations/fitting a Gaussian for non-responsive cells
                tuningTimeRange = [-0.1, 0.1]  # Includes baseline and response range
                (tuningSpikeTimesFromEventOnset, tuningTrialIndexForEachSpike,
                 tuningIndexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(tuningSpikeTimes,
                                                          tuningEventOnsetTimes,
                                                          tuningTimeRange)
            else:
                respLatency = np.nan
                tuningPVal = np.nan
                tuningZStat = np.nan

            highestFR = 0
            highestOnsetFR = 0
            highestSustainedFR = 0
            for indInten, intensity in enumerate(uniqueIntensity):
                spks = np.array([])  # Collection of all response spikes
                freqs = np.array([])  # Collection of all frequencies matched with the spikes above
                # ------------ start of frequency specific calculations -------------
                for indFreq, freq in enumerate(uniqFreq):
                    # Finding the indices for the spikes that have a set frequency and intensity from the above loops
                    selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == intensity))

                    # Firing rate calculation over whole base/response period at a specific frequency and intensity
                    nspkBaseTuning, nspkRespTuning = funcs.calculate_firing_rate(tuningEventOnsetTimes,
                                                                                 tuningSpikeTimes, baseRange,
                                                                                 selectinds=selectinds)
                    if respLatency > 0:
                        # Firing rate just for base/onset
                        nspkBaseTuningOnset, nspkRespTuningOnset = funcs.calculate_firing_rate(tuningEventOnsetTimes,
                                                                                               tuningSpikeTimes,
                                                                                               [-(respLatency + 0.05), -respLatency],
                                                                                               selectinds=selectinds)
                        # Firing rate just for base/sustained
                        nspkBaseTuningSustained, nspkRespTuningSustained = funcs.calculate_firing_rate(tuningEventOnsetTimes,
                                                                                                       tuningSpikeTimes,
                                                                                                       [-(respLatency + 0.1), -(respLatency + 0.05)],
                                                                                                       selectinds=selectinds)
                    spks = np.concatenate([spks, nspkRespTuning.ravel()])
                    freqs = np.concatenate([freqs, np.ones(len(nspkRespTuning.ravel())) * freq])
                    respSpikeMeanTuning[indInten, indFreq] = np.mean(nspkRespTuning)
                    allIntenBase = np.concatenate([allIntenBase, nspkBaseTuning.ravel()])

                    if intensity == uniqueIntensity[-1]:
                        meanRespFRTuning = np.mean(nspkRespTuning)
                        if meanRespFRTuning > highestFR:
                            highestFR = meanRespFRTuning

                            # Storing the highest response spikes as well as the frequency to save in the database later
                            bestFreqMaxInt = freq
                            baseSpksTuning = nspkBaseTuning
                            respSpksTuning = nspkRespTuning
                        if respLatency > 0:
                            meanOnsetFRTuning = np.mean(nspkRespTuningOnset)
                            meanSustainedFRTuning = np.mean(nspkRespTuningSustained)
                            if meanOnsetFRTuning > highestOnsetFR:
                                highestOnsetFR = meanOnsetFRTuning

                                # Storing the highest response spikes as well as the frequency to save in the database later
                                bestFreqOnsetMaxInt = freq
                                baseOnsetSpksTuning = nspkBaseTuningOnset
                                respOnsetSpksTuning = nspkRespTuningOnset
                            if meanSustainedFRTuning > highestSustainedFR:
                                highestSustainedFR = meanSustainedFRTuning

                                # Storing the highest response spikes as well as the frequency to save in the database later
                                bestFreqSustainedMaxInt = freq
                                baseSustainedSpksTuning = nspkBaseTuningSustained
                                respSustainedSpksTuning = nspkRespTuningSustained

                    # ------------------- Significance and fit calculations for tuning ----------------
                # TODO: Do we really need to calculate this for each frequency at each intensity?
                Rsquared, popt = funcs.calculate_fit(uniqFreq, allIntenBase, freqs, spks)

                Rsquareds.append(Rsquared)
                popts.append(popt)

            # ------------------------------ Intensity based calculations -------------------------
            responseThreshold = funcs.calculate_response_threshold(0.2, allIntenBase, respSpikeMeanTuning)
            # [6] Find Frequency Response Area (FRA) unit: fra boolean set, yes or no, but it's originally a pair
            fra = respSpikeMeanTuning > responseThreshold
            # [6.5] get the intensity threshold
            intensityInd, freqInd = funcs.calculate_intensity_threshold_and_CF_indices(fra, respSpikeMeanTuning)
            if intensityInd is None:  # None of the intensities had anything
                bw10 = None
                lowerFreq = None
                upperFreq = None
                cf = None
                intensityThreshold = None
                fit_midpoint = None
            else:
                intensityThreshold = uniqueIntensity[intensityInd]
                cf = uniqFreq[freqInd]

                if toCalculate:
                    monoIndex, overallMaxSpikes = funcs.calculate_monotonicity_index(tuningEventOnsetTimes, currentFreq,
                                                                                     currentIntensity,
                                                                                     uniqueIntensity, tuningSpikeTimes,
                                                                                     cf)
                    onsetRate, sustainedRate, baseRate = funcs.calculate_onset_to_sustained_ratio(tuningEventOnsetTimes,
                                                                                                  tuningSpikeTimes,
                                                                                                  currentFreq,
                                                                                                  currentIntensity,
                                                                                                  uniqueIntensity,
                                                                                                  cf, respLatency)
                else:
                    monoIndex = np.nan
                    overallMaxSpikes = np.nan
                    onsetRate = np.nan
                    sustainedRate = np.nan
                    baseRate = np.nan

                # [8] getting BW10 value, Bandwidth at 10dB above the neuron's sound intensity threshold(SIT)
                ind10Above = intensityInd + int(
                    10 / np.diff(uniqueIntensity)[0])  # How many inds to go above the threshold intensity ind
                lowerFreq, upperFreq, Rsquared10AboveSIT = funcs.calculate_BW10_params(ind10Above, popts, Rsquareds,
                                                                                       responseThreshold,
                                                                                       intensityThreshold)

                if (lowerFreq is not None) and (upperFreq is not None):
                    fitMidpoint = np.sqrt(lowerFreq * upperFreq)
                    bw10 = (upperFreq - lowerFreq) / cf

                else:
                    fitMidpoint = None
                    bw10 = None

                # Adding tuningCurve calculations to the dataframe to be saved later
                cellDB.at[indRow, 'thresholdFRA'] = intensityThreshold  # Threshold intensity for the FRA
                cellDB.at[indRow, 'cf'] = cf  # Characteristic frequency of the cell
                cellDB.at[indRow, 'lowerFreq'] = lowerFreq  # Lower frequency bound of the Gaussian
                cellDB.at[indRow, 'upperFreq'] = upperFreq  # Upper frequency bound of the Gaussian
                cellDB.at[indRow, 'rsquaredFit'] = Rsquared10AboveSIT  # The fit of the Gaussian to the actual FR 10 dB above SIT
                cellDB.at[indRow, 'bw10'] = bw10  # The bandwidth 10 dB above the neuron's SIT
                cellDB.at[indRow, 'fit_midpoint'] = fitMidpoint  # Midpoint of the Gaussian
                cellDB.at[indRow, 'latency'] = respLatency  # How long the cell takes to have an onset response after presentation
                cellDB.at[indRow, 'monotonicityIndex'] = monoIndex  # How linearly the cell increases FR with intensity
                cellDB.at[indRow, 'tuningOnsetRate'] = onsetRate  # The FR of the onset of the cell response (first 50 ms)
                cellDB.at[indRow, 'tuningSustainedRate'] = sustainedRate  # The FR of the sustained cell response (last 50 ms)
                cellDB.at[indRow, 'tuningBaseRate'] = baseRate  # Baseline FR of the cell (-100 ms to 0 ms)
                cellDB.at[indRow, 'tuning_pVal'] = tuningPVal  # p-value from Mann-Whitney U test of Onset spikes
                cellDB.at[indRow, 'tuning_ZStat'] = tuningZStat  # U-statistic from Mann-Whitney U test of Onset spikes
                cellDB.at[indRow, 'tuningBaseFRBestFreqMaxInt'] = np.mean(baseSpksTuning)  # Highest baseline FR at max intensity
                cellDB.at[indRow, 'tuningRespFRBestFreqMaxInt'] = np.mean(respSpksTuning)  # Highest response FR at max intensity
                cellDB.at[indRow, 'tuningBestFreqMaxInt'] = bestFreqMaxInt  # The frequency used for the two above variables
                if respLatency > 0:
                    cellDB.at[indRow, 'tuningBaseOnsetFRBestFreqMaxInt'] = np.mean(baseOnsetSpksTuning)  # Highest baseline FR at max intensity for Onset period [-0.05 s, 0.0 s]
                    cellDB.at[indRow, 'tuningRespOnsetFRBestFreqMaxInt'] = np.mean(respOnsetSpksTuning)  # Highest response FR at max intensity for Onset period [0.0 s, 0.05 s]
                    cellDB.at[indRow, 'tuningBestOnsetFreqMaxInt'] = bestFreqOnsetMaxInt  # The frequency used for the two above variables
                    cellDB.at[indRow, 'tuningBaseSustainedFRBestFreqMaxInt'] = np.mean(baseSustainedSpksTuning)  # Highest baseline FR at max intensity for Sustained period [-0.1 s, 0.05 s]
                    cellDB.at[indRow, 'tuningRespSustainedFRBestFreqMaxInt'] = np.mean(respSustainedSpksTuning)  # Highest response FR at max intensity for Sustained period [0.05 s, 0.1 s]
                    cellDB.at[indRow, 'tuningBestSustainedFreqMaxInt'] = bestFreqSustainedMaxInt  # The frequency used for the two above variables
                # Onset-to-sustained ratio is calculated right before the database is returned since it is calculated
                # purely from columns in the database, so look near line 461

        # -------------------- am calculations ---------------------------
        session = 'am'
        try:
            amEphysData, amBehavData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            significantFreqsArray = np.array([])

            # General variables for am calculations/plotting from ephys and behavior data
            amSpikeTimes = amEphysData['spikeTimes']
            amEventOnsetTimes = amEphysData['events']['soundDetectorOn']
            amEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(amEventOnsetTimes, minEventOnsetDiff=0.2)
            amCurrentRate = amBehavData['currentFreq']
            amUniqRate = np.unique(amCurrentRate)
            amTimeRange = [-0.2, 0.7]
            amTrialsEachCond = behavioranalysis.find_trials_each_type(amCurrentRate, amUniqRate)

            if len(amCurrentRate) != len(amEventOnsetTimes):
                amEventOnsetTimes = amEventOnsetTimes[:-1]
            if len(amCurrentRate) != len(amEventOnsetTimes):
                print('Removing one does not align events and behavior. Skipping AM for cell')
            else:
                (amSpikeTimesFromEventOnset, amTrialIndexForEachSpike,
                 amIndexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                          amEventOnsetTimes,
                                                          amTimeRange)
                amBaseTime = [-0.6, -0.1]
                amOnsetTime = [0, 0.1]
                amResponseTime = [0, 0.5]

                amBaseTimeOnset = [-0.1, 0]
                amBaseTimeSustained = [-0.5, -0.1]
                # Initializing lowest possible firing rate to compare to later
                amSusFR = 0
                amOnsetFR = 0

                #TODO: Maybe make this into a funciton in funcs file?
                for rate in amUniqRate:
                    AMSelectInds = np.flatnonzero(amCurrentRate == rate)  # Selecting rate indices that match the specific rate

                    # Calculating FR using the indexes of the specific rate from above
                    nspkBaseOnset, nspkRespOnset = funcs.calculate_firing_rate(amEventOnsetTimes,
                                                                               amSpikeTimes,
                                                                               amBaseTimeOnset,
                                                                               selectinds=AMSelectInds)
                    nspkBaseSustained, nspkRespSustained = funcs.calculate_firing_rate(amEventOnsetTimes,
                                                                                       amSpikeTimes,
                                                                                       amBaseTimeSustained,
                                                                                       selectinds=AMSelectInds)
                    # Comapring the current FR to previous highest FR so that ultimately we save the rate with highest FR
                    if np.mean(nspkRespOnset) > amOnsetFR:
                        amOnsetFR = np.mean(nspkRespOnset)
                        amRespOnsetSpikes = nspkRespOnset
                        amBaseOnsetSpikes = nspkBaseOnset
                        amRateBestOnset = rate
                    if np.mean(nspkRespSustained) > amSusFR:
                        amSusFR = np.mean(nspkRespSustained)
                        amRespSustainedSpikes = nspkRespSustained
                        amBaseSustainedSpikes = nspkBaseSustained
                        amRateBestSustained = rate
                cellDB.at[indRow, 'AMBaseFROnset'] = np.mean(amBaseOnsetSpikes)  # Mean baseline FR matched for the onset period (-100 ms to 0 ms)
                cellDB.at[indRow, 'AMRespFROnset'] = np.mean(amRespOnsetSpikes)  # Mean response FR for the onset period (0 ms to 100 ms)
                cellDB.at[indRow, 'AMBestRateOnset'] = amRateBestOnset  # Rate that gave the highest onset response
                cellDB.at[indRow, 'AMBaseFRSustained'] = np.mean(amBaseSustainedSpikes)  # Mean baseline FR paired with sustained period (-500 ms to -100 ms)
                cellDB.at[indRow, 'AMRespFRSustained'] = np.mean(amRespSustainedSpikes)  # Mean response FR for sustained period (100 ms to 500 ms)
                cellDB.at[indRow, 'AMBestRateSustained'] = amRateBestSustained  # Rate that gave the highest sustained response

                #TODO: Should do some kind of post-hoc/correction on these such as
                # taking the p-value and dividing by the total number of comparisons done and using that as a threshold
                zStat, amPValue = \
                    funcs.sound_response_any_stimulus(amEventOnsetTimes, amSpikeTimes, amTrialsEachCond, amResponseTime,
                                                      amBaseTime)
                cellDB.at[indRow, 'am_response_pVal'] = amPValue  # p-value from Mann-Whitney U test
                cellDB.at[indRow, 'am_response_ZStat'] = zStat  # U-statistic from Mann-Whitney U test

                # TODO: test calculations below
                #TODO: Should do some kind of post-hoc/correction on the alpha such as
                # taking the alpha and dividing by the total number of comparisons done (11) and using that as a threshold
                correctedPval = 0.05 / len(amUniqRate)  # Correcting for comparison of multiple p-values

                # Decide whether to make the next calculations based on 0.05 or on corrected value
                if amPValue > correctedPval:  # No response
                    print("No significant AM response, no synchronization will be calculated")
                elif amPValue < correctedPval:
                    amTimeRangeSync = [0.1, 0.5]  # Use this to cut out onset responses
                    (amSyncSpikeTimesFromEventOnset,
                     amSyncTrialIndexForEachSpike,
                     amSyncIndexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                                                         amEventOnsetTimes,
                                                                                         amTimeRangeSync)

                    allFreqSyncPVal, allFreqSyncZScore, allFreqVectorStrength, allFreqRal = \
                        funcs.calculate_am_significance_synchronization(amSyncSpikeTimesFromEventOnset,
                                                                        amSyncTrialIndexForEachSpike, amCurrentRate,
                                                                        amUniqRate)
                    amSyncPValue = np.min(allFreqSyncPVal)
                    amSyncZStat = np.max(allFreqSyncZScore)
                    cellDB.at[indRow, 'am_synchronization_pVal'] = amSyncPValue  # p-value from Rayleigh's test for periodicity
                    cellDB.at[indRow, 'am_synchronization_ZStat'] = amSyncZStat  # Statistic from Rayleigh's test for periodicity

                    phaseDiscrimAccuracyDict = funcs.calculate_phase_discrim_accuracy(amSpikeTimes, amEventOnsetTimes,
                                                                                      amCurrentRate, amUniqRate)

                    for rate in amUniqRate:
                        cellDB.at[indRow, 'phaseDiscrimAccuracy_{}Hz'.format(int(rate))] = \
                            phaseDiscrimAccuracyDict[int(rate)]

                    rateDiscrimAccuracy = funcs.calculate_rate_discrimination_accuracy(amSpikeTimes, amEventOnsetTimes,
                                                                                       amBaseTime, amResponseTime,
                                                                                       amCurrentRate)
                    cellDB.at[indRow, 'rateDiscrimAccuracy'] = rateDiscrimAccuracy
                    if any(allFreqSyncPVal < 0.05):
                            sigPvals = np.array(allFreqSyncPVal) < 0.05
                            highestSyncInd = funcs.index_all_true_before(sigPvals)
                            cellDB.at[indRow, 'highestSync'] = amUniqRate[allFreqSyncPVal < 0.05].max()
                            cellDB.at[indRow, 'highestUSync'] = amUniqRate[highestSyncInd]

                    else:
                        cellDB.at[indRow, 'highestSync'] = 0

                    if any(allFreqSyncPVal < correctedPval):
                        cellDB.at[indRow, 'highestSyncCorrected'] = amUniqRate[allFreqSyncPVal < correctedPval].max()  # Storing the highest rate that should synchronization from the Rayleigh test
                        freqsBelowThresh = allFreqSyncPVal < correctedPval
                        freqsBelowThresh = freqsBelowThresh.astype(int)
                        if len(significantFreqsArray) == 0:
                            significantFreqsArray = freqsBelowThresh  #TODO Should we save all the frequencies that showed synchronization?
                        else:
                            significantFreqsArray = np.vstack((significantFreqsArray, freqsBelowThresh))
                    else:
                        cellDB.at[indRow, 'highestSyncCorrected'] = 0

    # Calculating the onset-to-sustained ratio from the relevant columns
    cellDB['cfOnsetivityIndex'] = \
        (cellDB['tuningOnsetRate'] - cellDB['tuningSustainedRate']) / \
        (cellDB['tuningSustainedRate'] + cellDB['tuningOnsetRate'])

    return cellDB


def calculate_indices(db, filename=''):
    """
    Filter cells that has a good fitting then separate D1 cells(laser responsive)\
    and non-D1 cells(non laser-responsive)
    """
    pass
    # bestCells = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
    #
    # return bestCells


def calculate_cell_locations(db, filename=''):
    # We do not have this function in this file as it relies on the allensdk
    # module which must be installed in a virtual environment
    # The function is located in database_cell_locations.py
    pass


def merge_dataframes(listOfMice, firstMouse, dataframe_location='/var/tmp/figuresdata/2019astrpi/'):
    """
    Takes two dataframes and concatenates them so we can process one mouse at a time
    instead of having to regenerate an entire database when we add on a new mouse
    Args:
        listOfMice (list): List of mouse names as strings
        firstMouse (string): Name of first mouse to load the dataframe for. All
        mice in listOfMice will be appened to the end of this frame in order

    Returns:
        new_df (pandas.DataFrame): Two given dataframes appended through index value

    """
    df = celldatabase.load_hdf(os.path.join(dataframe_location, "{}.h5".format(firstMouse)))
    for mouse in listOfMice:
        try:
            appendedFrame = celldatabase.load_hdf(mouse)
        except OSError:
            print("Mouse {} does not have an h5 file")
        else:
            df = pd.concat([df, appendedFrame], axis=0, ignore_index=True, sort=False)

    return df


if __name__ == "__main__":
    # Cluster your data
    CLUSTER_DATA = 0  # We don't generally run this code. We kept this for documentation

    # Choosing which mice to do calculations for
    # Check for script arguements to decide what calculations are done
    dbLocation = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    if sys.argv[1:] != []:
        # Defaulting all calculations to false
        basic_generation = 0
        calc_stats = 0
        calc_locations = 0
        concat_mice = 0
        arguments = sys.argv[1:]
        if arguments[0] == "concat":
            concat_mice = 1
        else:
            if arguments[1] == 'all':
                d1mice = studyparams.ASTR_D1_CHR2_MICE
                dbpath = os.path.join(dbLocation, '{}.h5'.format(studyparams.DATABASE_NAME))
            elif isinstance(arguments[1], str):
                d1mice = arguments[1]
                dbpath = os.path.join(dbLocation, '{}.h5'.format(d1mice))

                #FIXME: Storing the string as a list since the database generation tries to loop through the mice. A
                # single mouse string would instead cause it to loop through letters. A list of one fixes this
                d1mice = [d1mice]
            else:
                # If no mice are specified, default to using all mice in the studyparams
                d1mice = studyparams.ASTR_D1_CHR2_MICE
                dbpath = os.path.join(dbLocation, '{}.h5'.format(studyparams.DATABASE_NAME))
            print('d1mice = {}'.format(d1mice))  # Printing mice so user can see what is being used
            # Run behavior can either be 'all', 'hist', or 'stats' if not concatenating
            runBehavior = arguments[0]
            print('Run behavior is {}'.format(runBehavior))  # Printing behavior so user is aware
            if runBehavior == 'all':
                # Generates dataframe from inforec, calculates in-depth statistics, and then finds locations from tracks
                basic_generation = 1
                calc_stats = 1
                calc_locations = 1
            elif runBehavior == 'locations':
                # Generates a dataframe from inforec and then finds locations from the tracks files
                basic_generation = 1
                calc_locations = 1
            elif runBehavior == 'stats':
                # Generates a dataframe from the inforec and then calculates in-depth statistics
                basic_generation = 1
                calc_stats = 1
            elif runBehavior == 'basic':
                # Just generates a dataframe from the inforecs. Good for checking if you have all needed files available
                # to your system (besides tracks/histology files)
                basic_generation = 1

    else:
        # Calculates everything and finds locations for all mice in studyparams if no system arguements are provided
        calc_stats = 1
        calc_locations = 1
        basic_generation = 1
        concat_mice = 0
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        dbpath = os.path.join(dbLocation, '{}.h5'.format(studyparams.DATABASE_NAME))

    if CLUSTER_DATA:  # SPIKE SORTING
        # TODO: Need to loop through d1mice as it is a list
        #FIXME: Add an error for if a list of mice is going to be given to the cluster inforec function
        inforecFile = os.path.join(settings.INFOREC_PATH, '{}_inforec.py'.format(d1mice))
        clusteringObj = spikesorting.ClusterInforec(inforecFile)
        clusteringObj.process_all_experiments()
        pass

    # Generate_cell_database filters cells with the following: isi < 0.05, spike quality > 2
    if concat_mice:
        # Fetches individual mice dataframes and merges into one dataframe
        first_mouse, *list_of_mice = studyparams.ASTR_D1_CHR2_MICE
        histDB = merge_dataframes(list_of_mice, first_mouse)
        dbpath = os.path.join(dbLocation, '{}.h5'.format(studyparams.DATABASE_NAME))
    if basic_generation:
        basicDB = celldatabase.generate_cell_database_from_subjects(d1mice)

        '''
        These renaming variables below are to account for if only some calculations are done. Otherwise the save
        function would have to do four different if-elif clauses to test for what dataframe to save. Instead I just
        have each variable get overwritten as more advanced calculations are done.
        '''
        firstDB = basicDB
        histDB = basicDB
        d1DBFilename = os.path.join(settings.FIGURES_DATA_PATH, '{}_d1mice.h5'.format(studyparams.STUDY_NAME))
    # Create and save a database, computing first the base stats and then the indices
    if calc_stats:
        firstDB = append_base_stats(basicDB, filename=d1DBFilename)
        # bestCells = calculate_indices(firstDB, filename = d1DBFilename)
        histDB = firstDB
        celldatabase.save_hdf(histDB, os.path.join(dbLocation, '{}.h5'.format('temp_rescue_db')))
    if calc_locations:
        histDB = histologyanalysis.cell_locations(firstDB, brainAreaDict=studyparams.BRAIN_AREA_DICT)

    if SAVE:
        if os.path.isdir(dbLocation):
            celldatabase.save_hdf(histDB, dbpath)
            print("SAVED DATAFRAME to {}".format(dbpath))
            print(u"\U0001F4A9" * 10)
        elif not os.path.isdir(dbLocation):
            answer = input("Save folder is not present. Would you like to make the desired directory now? (y/n) ")
            if answer.upper() in ['Y', 'YES']:
                os.mkdir(dbLocation)
                celldatabase.save_hdf(histDB, dbpath)
                print("SAVED DATAFRAME to {}".format(dbpath))
                print(u"\U0001F4A9"*10)
