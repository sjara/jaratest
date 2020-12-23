# -*- coding: utf-8 -*-
"""
This script calculates statistics for a single cell  

Created on Fri Sep 18 14:19:55 2020
@author: Devin Henderling
"""

import os
import numpy as np
import pandas as pd
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import database_generation_funcs as funcs

outputDirectory = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                               '{}_one_cell.h5'.format(studyparams.DATABASE_NAME))
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                        '{}_basic.h5'.format(studyparams.DATABASE_NAME))

# ========================== Basic Database Creation ==========================

# Loads basic database for testing
basicDB = celldatabase.load_hdf(pathtoDB)  

# More strictly selects for SSQ and ISIviolations (specfied in studyparams.py)
db = basicDB.query(studyparams.FIRST_FLTRD_CELLS)

hasAM = db['sessionType'].apply(lambda s: 'am' in s)
hasLP = db['sessionType'].apply(lambda s: 'laserpulse' in s)
hasLT = db['sessionType'].apply(lambda s: 'lasertrain' in s)
hasNB = db['sessionType'].apply(lambda s: 'noiseburst' in s)
hasTC = db['sessionType'].apply(lambda s: 'tuningCurve' in s)
hasTT = db['sessionType'].apply(lambda s: 'tuningTest' in s)

# db = db[hasLP]
# db = db[hasTC]
# ========================== Laserpulse ==========================

examples = {}
# examples.update({'D1': 'd1pi046_2020-02-15_2800.0_TT2c2'})
examples.update({'D1': 'd1pi041_2019-08-25_3200.0_TT5c3'})
# examples.update({'nD1': 'd1pi049_2020-03-13_3200.0_TT7c3'})

exampleCell = [val for key, val in examples.items()]
exampleKeys = [key for key, val in examples.items()]

# ===========================Create and save figures=============================
for ind, cellInfo in enumerate(exampleCell):

    (subject, date, depth, tetrodeCluster) = cellInfo.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, exampleCell = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)    
    oneCell = ephyscore.Cell(exampleCell, useModifiedClusters=False)
      
    # Progress message 
    print("Processing cell {} \n {}, {}, depth = {} tetrode {}, cluster {}".format(indRow, 
          exampleCell['subject'], exampleCell['date'], exampleCell['depth'], exampleCell['tetrode'], exampleCell['cluster']))
    
    # Checks for a laserpulse session
    session = 'laserpulse'
    try:
        pulseEphysData, noBData = oneCell.load(session)
    except IndexError:
        print('This cell does not contain a {} session'.format(session))
    else:
        baseRange = [-0.1, 0] # Time used for baseline spike counts.
        
        # Creates arrays of times stimulus presented
        laserEventOnsetTimes = pulseEphysData['events']['laserOn']
        laserSpikeTimes = pulseEphysData['spikeTimes']
        
        # Calculates firing rate during baseline and response periods 
        nspkBaseLaser, nspkRespLaser = funcs.calculate_firing_rate(laserEventOnsetTimes, 
                                                                   laserSpikeTimes, baseRange)
        
        # Calculates mean firing rate for baseline and response periods 
        nspkRespLaserMean = np.mean(nspkRespLaser)
        nspkBaseLaserMean = np.mean(nspkBaseLaser)
        
        # Calculates change in firing rate during laserpulse
        spikeCountChange = nspkRespLaserMean - nspkBaseLaserMean
            
        # Significance calculations for the laserpulse
        try:
            zStats, pVals = stats.mannwhitneyu(nspkRespLaser, nspkBaseLaser, 
                                               alternative='two-sided')
        except ValueError:  # All numbers identical will cause mann-whitney to fail
            print("laserpulse mann-whitney fail for {}".format(oneCell))
            zStats, pVals = [0, 1]
        
        # Adds laserpulse information to database
        exampleCell['laserpulse_pVal'] = pVals  # p-value from Mann-Whitney U test
        exampleCell['laserpulse_ZStat'] = zStats  # U-statistic from Mann-Whitney U test
        # Difference between base and response firing rate
        exampleCell['laserpulse_SpikeCountChange'] = spikeCountChange
        exampleCell['laserpulse_baselineSpikeCount'] = nspkBaseLaserMean  # Mean of baseline FR
        exampleCell['laserpulse_responseSpikeCount'] = nspkRespLaserMean  # Mean of response FR
    
    # ========================== Tuning Curve ==========================
        
    # Checks for a tuning curve session
    session = 'tuningCurve'
    try:
        tuningEphysData, tuningBehavData = oneCell.load(session)
    except IndexError:
        print('This cell does not contain a {} session'.format(session))
    else:            
        baseRange = [-0.1, 0]  # Time used for baseline spike counts.
    
        currentFreq = tuningBehavData['currentFreq']  # The frequency for each trial
        currentIntensity = tuningBehavData['currentIntensity'] # The intensity for each trial
        
        uniqFreq = np.unique(currentFreq)  # List of unqiue frequencies presented
        uniqueIntensity = np.unique(currentIntensity)  # List of unique intensities presented   
        
        # Creates a boolean 3D array of size [nTrials,nValues1,nValues2]. True for each combination.
        tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq,
                                                                             currentIntensity, 
                                                                             uniqueIntensity)
        
        # A list to collect the baseline spikes across all intensities
        allIntenBase = np.array([])
        
        # A list to collect the response spikes across all intensities
        respSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))
        
        # A list to collect the baseline spikes across all intensities
        baseSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))
    
        Rsquareds = []  # Collection of rsquared values
        popts = []  # Collection of optimal fit parameters for the Gaussians
        
        # Creates array of tuning curve spike times
        tuningSpikeTimes = tuningEphysData['spikeTimes']
        
        # Creates array of tuning curve stimulus event times
        tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
        
        # Exclude events that happen too soon after a preceeding event
        tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes,
                                                                        minEventOnsetDiff=0.2)
        
        # Removing last session of ephys data if it has one more trial than the behavior data
        if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
            tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
            print("Correcting ephys data to be same length as behavior data")
            calculate = True
        elif len(tuningEventOnsetTimes) == len(currentFreq):
            print("Data is already the same length")
            calculate = True
        else:
            print("Something is wrong with the length of these data")
            calculate = False
        
    # ========================== Latency ==========================
    
        if calculate:
            tuningZStat, tuningPVal = \
                        funcs.sound_response_any_stimulus(tuningEventOnsetTimes, tuningSpikeTimes,
                                                          tuningTrialsEachCond[:, :, -1], 
                                                          timeRange=[0.0, 0.05],
                                                          baseRange=[-0.05, 0])  
                        # All trials at all frequencies at the highest intensity
            try:
                respLatency = funcs.calculate_latency(tuningEventOnsetTimes, currentFreq, uniqFreq, 
                                                      currentIntensity, uniqueIntensity, tuningSpikeTimes)
            except IndexError:
                 # If there are no spikes in the timeRangeForLatency
                print("Index error for cell {}".format(indRow)) 
                respLatency = np.nan
        else:
            respLatency = np.nan
        # if respLatency <= 0:
        #     respLatency = np.nan
            
        # How long the cell takes to have an response after presentation
        exampleCell['latency'] = respLatency
    
        # ========================== BW10  and Onset to Sustained Ratio ==========================
    
        for indInten, intensity in enumerate(uniqueIntensity):
            spks = np.array([])  # Collection of all response spikes
            freqs = np.array([])  # Collection of all frequencies matched with the spikes above
            
            for indFreq, freq in enumerate(uniqFreq):
                # Finding the indices for the spikes that have a set frequency and intensity from the above loops
                selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == intensity))
    
                # Firing rate calculation over whole base/response period at a specific frequency and intensity
                nspkBaseTuning, nspkRespTuning = funcs.calculate_firing_rate(tuningEventOnsetTimes,
                                                                             tuningSpikeTimes, baseRange,
                                                                             selectinds=selectinds)
                
                spks = np.concatenate([spks, nspkRespTuning.ravel()])
                freqs = np.concatenate([freqs, np.ones(len(nspkRespTuning.ravel())) * freq])
                respSpikeMeanTuning[indInten, indFreq] = np.mean(nspkRespTuning)
                baseSpikeMeanTuning[indInten, indFreq] = np.mean(nspkBaseTuning)
                allIntenBase = np.concatenate([allIntenBase, nspkBaseTuning.ravel()])
                
            Rsquared, popt = funcs.calculate_fit(uniqFreq, allIntenBase, freqs, spks)
            Rsquareds.append(Rsquared)
            popts.append(popt)

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
            monoIndex = np.nan
            overallMaxSpikes = np.nan
            onsetRate = np.nan
            sustainedRate = np.nan
            baseRate = np.nan
        else:
            intensityThreshold = uniqueIntensity[intensityInd]
            cf = uniqFreq[freqInd]
                    
            if calculate:
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
                
            ind10Above = intensityInd + int(
                10 / np.diff(uniqueIntensity)[0])  # How many inds to go above the threshold intensity ind
            lowerFreq, upperFreq, Rsquared10AboveSIT = funcs.calculate_BW10_params(ind10Above, popts, Rsquareds,
                                                                                   responseThreshold,
                                                                                   intensityThreshold)
            # Checking that neither bound of BW10 is none
            if (lowerFreq is not None) and (upperFreq is not None):
                bw10 = (upperFreq - lowerFreq) / cf
            else:
                bw10 = None
            
            # Mean of tuning response rate across all instensity/frequency combinations
            respTuningMean = np.mean(respSpikeMeanTuning[respSpikeMeanTuning > 0])
            
            # Mean of tuning base rate across all instensity/frequency combinations
            baseTuningMean = np.mean(baseSpikeMeanTuning)
            
            # Index for ratio between response and base firing rates
            try:
                respBaseTuningRatio = (respTuningMean - baseTuningMean) / (respTuningMean + baseTuningMean)
            except ZeroDivisionError:
                respBaseTuningRatio = 0 
            exampleCell['tuningBaseRateCount'] = baseSpikeMeanTuning  # The FR of the cell response (0 to 100 ms)
            exampleCell['tuningResponseRate'] = respTuningMean  # The FR of the cell response (0 to 100 ms) 
            exampleCell['tuningBaseRate'] = baseTuningMean  # The FR of the cell baseline (-100 to 0 ms) 
            exampleCell['tuningResponseRatio'] = respBaseTuningRatio  # Index for ratio between response and base firing rates (between 0 and 1)     
            exampleCell['bw10'] = bw10  # The bandwidth 10 dB above the neuron's SIT
            exampleCell['tuning_pVal'] = tuningPVal  # p-value from Mann-Whitney U test of Onset spikes
            exampleCell['tuning_ZStat'] = tuningZStat  # U-statistic from Mann-Whitney U test of Onset spikes
            exampleCell['thresholdFRA'] = intensityThreshold  # Threshold intensity for the FRA
            exampleCell['cf'] = cf  # Characteristic frequency of the cell
            exampleCell['tuningOnsetRate'] = onsetRate  # The FR of the onset of the cell response (first 50 ms)
            exampleCell['tuningSustainedRate'] = sustainedRate  # The FR of the sustained cell response (last 50 ms)    
            exampleCell['rsquaredFit'] = Rsquared10AboveSIT  # The fit of the Gaussian to the actual FR 10 dB above SIT
            exampleCell['lowerFreq'] = lowerFreq  # Lower frequency bound of the Gaussian
            exampleCell['upperFreq'] = upperFreq  # Upper frequency bound of the Gaussian
            exampleCell['rsquaredFit'] = Rsquared10AboveSIT  # The fit of the Gaussian to the actual FR 10 dB above SITdb.at[indRow, 'tuning_pVal'] = tuningPVal  # p-value from Mann-Whitney U test of Onset spikes
            try:
                exampleCell['cfOnsetivityIndex'] = \
                    (exampleCell['tuningOnsetRate'] - exampleCell['tuningSustainedRate']) / \
                        (exampleCell['tuningSustainedRate'] + exampleCell['tuningOnsetRate'])
            except ZeroDivisionError:
                exampleCell['cfOnsetivityIndex'] = np.nan
                
############################################ Matt's Code Beginning 
        

    # # ========================== AM ==========================
    # try:
    #     amEphysData, amBehavData = oneCell.load('am')
    # except IndexError:
    #     print('This cell does not contain a {} session'.format('am'))
    # else:
    #     # General variables for am calculations/plotting from ephys and behavior data
    #     amSpikeTimes = amEphysData['spikeTimes']
    #     amEventOnsetTimes = amEphysData['events']['soundDetectorOn']
    #     amEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(amEventOnsetTimes, minEventOnsetDiff=0.2)
    #     amCurrentRate = amBehavData['currentFreq']
    #     amUniqRate = np.unique(amCurrentRate)
    #     amTimeRange = [-0.2, 0.7]
    #     amTrialsEachCond = behavioranalysis.find_trials_each_type(amCurrentRate, amUniqRate)

    #     if len(amCurrentRate) != len(amEventOnsetTimes):
    #         amEventOnsetTimes = amEventOnsetTimes[:-1]
    #     if len(amCurrentRate) != len(amEventOnsetTimes):
    #         print('Removing one does not align events and behavior. Skipping AM for cell')
    #     else:
    #         (amSpikeTimesFromEventOnset, amTrialIndexForEachSpike,
    #           amIndexLimitsEachTrial) = \
    #             spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
    #                                                   amEventOnsetTimes,
    #                                                   amTimeRange)
    #         amBaseTime = [-0.6, -0.1]
    #         amOnsetTime = [0, 0.1]
    #         amResponseTime = [0, 0.5]

    #         amBaseTimeOnset = [-0.1, 0]
    #         amBaseTimeSustained = [-0.5, -0.1]
    #         # Initializing lowest possible firing rate to compare to later
    #         amSusFR = 0
    #         amOnsetFR = 0

    #         for rate in amUniqRate:
    #             AMSelectInds = np.flatnonzero(amCurrentRate == rate)  # Selecting rate indices that match the specific rate

    #             # Calculating FR using the indexes of the specific rate from above
    #             nspkBaseOnset, nspkRespOnset = funcs.calculate_firing_rate(amEventOnsetTimes,
    #                                                                         amSpikeTimes,
    #                                                                         amBaseTimeOnset,
    #                                                                         selectinds=AMSelectInds)
    #             nspkBaseSustained, nspkRespSustained = funcs.calculate_firing_rate(amEventOnsetTimes,
    #                                                                                 amSpikeTimes,
    #                                                                                 amBaseTimeSustained,
    #                                                                                 selectinds=AMSelectInds)
    #             # Comapring the current FR to previous highest FR so that ultimately we save the rate with highest FR
    #             if np.mean(nspkRespOnset) > amOnsetFR:
    #                 amOnsetFR = np.mean(nspkRespOnset)
    #                 amRespOnsetSpikes = nspkRespOnset
    #                 amBaseOnsetSpikes = nspkBaseOnset
    #                 amRateBestOnset = rate
    #             if np.mean(nspkRespSustained) > amSusFR:
    #                 amSusFR = np.mean(nspkRespSustained)
    #                 amRespSustainedSpikes = nspkRespSustained
    #                 amBaseSustainedSpikes = nspkBaseSustained
    #                 amRateBestSustained = rate
    #         db.at[indRow, 'AMBaseFROnset'] = np.mean(amBaseOnsetSpikes)  # Mean baseline FR matched for the onset period (-100 ms to 0 ms)
    #         db.at[indRow, 'AMRespFROnset'] = np.mean(amRespOnsetSpikes)  # Mean response FR for the onset period (0 ms to 100 ms)
    #         db.at[indRow, 'AMBestRateOnset'] = amRateBestOnset  # Rate that gave the highest onset response
    #         db.at[indRow, 'AMBaseFRSustained'] = np.mean(amBaseSustainedSpikes)  # Mean baseline FR paired with sustained period (-500 ms to -100 ms)
    #         db.at[indRow, 'AMRespFRSustained'] = np.mean(amRespSustainedSpikes)  # Mean response FR for sustained period (100 ms to 500 ms)
    #         db.at[indRow, 'AMBestRateSustained'] = amRateBestSustained  # Rate that gave the highest sustained response

    #         zStat, amPValue = \
    #             funcs.sound_response_any_stimulus(amEventOnsetTimes, amSpikeTimes, amTrialsEachCond, amResponseTime,
    #                                               amBaseTime)
    #         db.at[indRow, 'am_response_pVal'] = amPValue  # p-value from Mann-Whitney U test
    #         db.at[indRow, 'am_response_ZStat'] = zStat  # U-statistic from Mann-Whitney U test

    #         correctedPval = 0.05 / len(amUniqRate)  # Correcting for comparison of multiple p-values

    #         # Decide whether to make the next calculations based on 0.05 or on corrected value
    #         if amPValue > correctedPval:  # No response
    #             print("No significant AM response, no synchronization will be calculated")
    #         elif amPValue < correctedPval:
    #             amTimeRangeSync = [0.1, 0.5]  # Use this to cut out onset responses
    #             (amSyncSpikeTimesFromEventOnset,
    #               amSyncTrialIndexForEachSpike,
    #               amSyncIndexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
    #                                                                                   amEventOnsetTimes,
    #                                                                                   amTimeRangeSync)

    #             allFreqSyncPVal, allFreqSyncZScore, allFreqVectorStrength, allFreqRal = \
    #                 funcs.calculate_am_significance_synchronization(amSyncSpikeTimesFromEventOnset,
    #                                                                 amSyncTrialIndexForEachSpike, amCurrentRate,
    #                                                                 amUniqRate)
    #             amSyncPValue = np.min(allFreqSyncPVal)
    #             amSyncZStat = np.max(allFreqSyncZScore)
    #             db.at[indRow, 'am_synchronization_pVal'] = amSyncPValue  # p-value from Rayleigh's test for periodicity
    #             db.at[indRow, 'am_synchronization_ZStat'] = amSyncZStat  # Statistic from Rayleigh's test for periodicity

    #             phaseDiscrimAccuracyDict = funcs.calculate_phase_discrim_accuracy(amSpikeTimes, amEventOnsetTimes,
    #                                                                               amCurrentRate, amUniqRate)

    #             for rate in amUniqRate:
    #                 db.at[indRow, 'phaseDiscrimAccuracy_{}Hz'.format(int(rate))] = \
    #                     phaseDiscrimAccuracyDict[int(rate)]

    #             rateDiscrimAccuracy = funcs.calculate_rate_discrimination_accuracy(amSpikeTimes, amEventOnsetTimes,
    #                                                                                 amBaseTime, amResponseTime,
    #                                                                                 amCurrentRate)
    #             db.at[indRow, 'rateDiscrimAccuracy'] = rateDiscrimAccuracy
    #             if any(allFreqSyncPVal < 0.05):
    #                 sigPvals = np.array(allFreqSyncPVal) < 0.05
    #                 highestSyncInd = funcs.index_all_true_before(sigPvals)
    #                 db.at[indRow, 'highestSync'] = amUniqRate[allFreqSyncPVal < 0.05].max()
    #                 db.at[indRow, 'highestUSync'] = amUniqRate[highestSyncInd]
    #             else:
    #                 db.at[indRow, 'highestSync'] = 0

    #             if any(allFreqSyncPVal < correctedPval):
    #                 db.at[indRow, 'highestSyncCorrected'] = amUniqRate[allFreqSyncPVal < correctedPval].max()  # Storing the highest rate that should synchronization from the Rayleigh test
    #                 freqsBelowThresh = allFreqSyncPVal < correctedPval
    #                 freqsBelowThresh = freqsBelowThresh.astype(int)
    #             else:
    #                 db.at[indRow, 'highestSyncCorrected'] = 0

############################### Matts code end
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("SAVED DATAFRAME to {}".format(outputDirectory))
print(u"\U0001F4A9" * 10)