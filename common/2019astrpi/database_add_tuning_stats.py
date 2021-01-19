# -*- coding: utf-8 -*-
"""
This script loads the cell database produced by database_select_reliable_cells.py calculates 
laserpulse statistics for D1 vs. nD1 determination, and calculates statistics used for tuning curve 
sound response comparison. This database is filtered according to the parameters listed in 
database_select_reliable_cells.py.

This script calculates statistics used for:
1. D1 vs. nD1 selection
4. Response latency comparison
5. BW10 comparison
5. Onset to sustained ratio comparison

Created on Jan 17, 2021
Author: Devin Henderling
"""
import os
import numpy as np
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import database_generation_funcs as funcs

# ========================== Run Mode ==========================

TEST = 1 # Set to 1 to generate database for one animal for faster testing

if TEST:
    d1mice = studyparams.SINGLE_MOUSE 
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'astrpi_{}_tuning.h5'.format(d1mice[0]))
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'astrpi_{}_cells.h5'.format(d1mice[0]))
else:
    d1mice = studyparams.ASTR_D1_CHR2_MICE
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'astrpi_all_cells_tuning.h5')
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'astrpi_all_cells.h5')
     
# Loads cell database
db = celldatabase.load_hdf(inputDirectory)  

# Iterates through each cell in the database       
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
    
    # Progress message 
    print("Processing cell {} \n {}, {}, depth = {} tetrode {}, cluster {}".format(indRow, 
          dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    
    # ========================== Laserpulse Statistics Calculation ==========================
    
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
        nspkBaseLaser, nspkRespLaser = funcs.calculate_spike_count(laserEventOnsetTimes, 
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
        db.at[indRow, 'laserpulsePval'] = pVals  # p-value from Mann-Whitney U test
        db.at[indRow, 'laserpulseZstat'] = zStats  # U-statistic from Mann-Whitney U test
        # Difference between base and response firing rate
        db.at[indRow, 'laserpulseSpikeCountChange'] = spikeCountChange
        db.at[indRow, 'laserpulseBaselineSpikeCount'] = nspkBaseLaserMean  # Mean of baseline FR
        db.at[indRow, 'laserpulseResponseSpikeCount'] = nspkRespLaserMean  # Mean of response FR

    # ========================== Tuning Curve Statistics Calculation ==========================
    
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
        
        # A list to collect the onset response spikes across all intensities
        onsetRespSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))
        
        # A list to collect the onset-mirrored baseline spikes across all intensities
        onsetbaseSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))
        
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
    
        if calculate:
            tuningZStat, tuningPVal = \
                        funcs.sound_response_any_stimulus(tuningEventOnsetTimes, tuningSpikeTimes,
                                                          tuningTrialsEachCond[:, :, -1], 
                                                          timeRange=[0.0, 0.05],
                                                          baseRange=[-0.05, 0])  
                        # All trials at all frequencies at the highest intensity
                        
            # ========================== Latency ==========================
                        
            try:
                respLatency = funcs.calculate_latency(tuningEventOnsetTimes, currentFreq, uniqFreq, 
                                                      currentIntensity, uniqueIntensity, tuningSpikeTimes)
            except IndexError:
                 # If there are no spikes in the timeRangeForLatency
                print("No spikes during the period for latency: cell {}".format(indRow)) 
                respLatency = np.nan
        else:
            respLatency = np.nan
            
        # How long the cell takes to have an response after presentation
        db.at[indRow, 'latency'] = respLatency
    
        # ========================== BW10 and Onset to Sustained Ratio ==========================
    
        for indInten, intensity in enumerate(uniqueIntensity):
            spks = np.array([])  # Collection of all response spikes
            freqs = np.array([])  # Collection of all frequencies matched with the spikes above
            onsetspks = np.array([])  # Collection of all onset response spikes
            onsetfreqs = np.array([])  # Collection of all frequencies matched with the onset spikes above
            
            for indFreq, freq in enumerate(uniqFreq):
                # Finding the indices for the spikes that have a set frequency and intensity from the above loops
                selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == intensity))
    
                # Firing rate calculation over whole base/response period at a specific frequency and intensity
                nspkBaseTuning, nspkRespTuning = funcs.calculate_spike_count(tuningEventOnsetTimes,
                                                                             tuningSpikeTimes, baseRange,
                                                                             selectinds=selectinds)
                
                spks = np.concatenate([spks, nspkRespTuning.ravel()])
                freqs = np.concatenate([freqs, np.ones(len(nspkRespTuning.ravel())) * freq])
                respSpikeMeanTuning[indInten, indFreq] = np.mean(nspkRespTuning)
                baseSpikeMeanTuning[indInten, indFreq] = np.mean(nspkBaseTuning)
                allIntenBase = np.concatenate([allIntenBase, nspkBaseTuning.ravel()])
                
                # Calculations for response to baseline ratio for onset period (0 to 50ms)
                onsetBaseRange = [-0.05, 0]  # Time used for onset response and baseline spike counts.
                onsetnspkBaseTuning, onsetnspkRespTuning = funcs.calculate_spike_count(tuningEventOnsetTimes,
                                                                                         tuningSpikeTimes, onsetBaseRange,
                                                                                         selectinds=selectinds)
                onsetspks = np.concatenate([onsetspks, nspkRespTuning.ravel()])
                onsetfreqs = np.concatenate([onsetfreqs, np.ones(len(nspkRespTuning.ravel())) * freq])
                onsetRespSpikeMeanTuning[indInten, indFreq] = np.mean(onsetnspkRespTuning)
            
            Rsquared, popt = funcs.calculate_fit(uniqFreq, allIntenBase, freqs, spks)
            Rsquareds.append(Rsquared)
            popts.append(popt)

        responseThreshold = funcs.calculate_response_threshold(0.2, allIntenBase, respSpikeMeanTuning)
        # [6] Find Frequency Response Area (FRA) unit: fra boolean set, yes or no, but it's originally a pair
        fra = respSpikeMeanTuning > responseThreshold
        # [6.5] get the intensity threshold
        intensityInd, freqInd = funcs.calculate_intensity_threshold_and_CF_indices(fra, respSpikeMeanTuning)
    
        # Further calculations for onset reponse to baseline ratio
        respTuningMean = np.mean(onsetRespSpikeMeanTuning[fra])
        # Mean of tuning base rate across all instensity/frequency combinations
        baseTuningMean = np.mean(baseSpikeMeanTuning)
        
        # Index for ratio between response and base firing rates
        try:
            respBaseTuningRatio = (respTuningMean - baseTuningMean) / (respTuningMean + baseTuningMean)
        except ZeroDivisionError:
            respBaseTuningRatio = 0 
        
        db.at[indRow,'tuningResponseRate'] = respTuningMean  # The FR of the cell onset response (0 to 50 ms) 
        db.at[indRow,'tuningBaseRate'] = baseTuningMean  # The FR of the cell baseline (-100 to -50 ms) 
        db.at[indRow,'tuningResponseRatio'] = respBaseTuningRatio  # Index for ratio between response and base firing rates (between 0 and 1)
    
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
            
            # ========================== Threshold ==========================
            
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
            
            # ========================== BW10 ==========================
                
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
                
          
            db.at[indRow, 'bw10'] = bw10  # The bandwidth 10 dB above the neuron's SIT
            db.at[indRow, 'tuningPval'] = tuningPVal  # p-value from Mann-Whitney U test of Onset spikes
            db.at[indRow, 'tuningZstat'] = tuningZStat  # U-statistic from Mann-Whitney U test of Onset spikes
            db.at[indRow, 'thresholdFRA'] = intensityThreshold  # Threshold intensity for the FRA
            db.at[indRow, 'cf'] = cf  # Characteristic frequency of the cell
            db.at[indRow, 'tuningOnsetRate'] = onsetRate  # The FR of the onset of the cell response (first 50 ms)
            db.at[indRow, 'tuningSustainedRate'] = sustainedRate  # The FR of the sustained cell response (last 50 ms)    
            db.at[indRow, 'rSquaredFit'] = Rsquared10AboveSIT  # The fit of the Gaussian to the actual FR 10 dB above SIT
            db.at[indRow, 'lowerFreq'] = lowerFreq  # Lower frequency bound of the Gaussian
            db.at[indRow, 'upperFreq'] = upperFreq  # Upper frequency bound of the Gaussian
            
            # ========================== Onset to Sustained Ratio ==========================
            
            try:
                db.at[indRow, 'cfOnsetivityIndex'] = \
                    (db.at[indRow, 'tuningOnsetRate'] - db.at[indRow, 'tuningSustainedRate']) / \
                    (db.at[indRow, 'tuningSustainedRate'] + db.at[indRow, 'tuningOnsetRate'])
            except ZeroDivisionError:
                db.at[indRow, 'cfOnsetivityIndex'] = np.nan
     
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("SAVED DATAFRAME to {}".format(outputDirectory))