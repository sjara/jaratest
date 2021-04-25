# -*- coding: utf-8 -*-
"""
This script takes an existing database and calculates statistics using data from AM sessions. These 
statistics are used for amplitude modulated sound response comparison. 

This script calculates statistics used for:
1. Highest Rate Sustained Comparison
2. Highest Synchronization Comparison
2. Percent Synchronization Comparison
3. Rate Descrimination Accuracy Comparison
4. Phase Descrimination Accuracy Comparison

When run without arguments, this script will use all animals and store in a default database. This 
script can also be run using arguments to specify a specfic basic database that has been generated. 
The two arguments are "SUBJECT" and "TAG".

Run as (if not using tag)
`database_add_am_stats.py` or `database_add_am_stats.py SUBJECT`

Run as (if using tag)
`database_add_am_stats.py SUBJECT TAG`

The file `studyparams.py` contains a list of animals as well as statistical parameters for the 
database calculations. Database scripts use functions from the moddule 
`database_generation_funcs.py`. 
"""
import os
import sys
import numpy as np
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import database_generation_funcs as funcs

# ========================== Run Mode ==========================

TAG = 0 # Automatically set to 1 if tag given

# Determining animals used and file name by arguments given
if __name__ == '__main__':
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if len(arguments) == 2:
                tag = arguments[1]
                TAG = 1
        if arguments[0].upper() in 'ALL':
            subjects = 'all'
        elif arguments[0].upper() == 'TEST':
            subjects = studyparams.SINGLE_MOUSE[0]
        elif isinstance(arguments[0], str):
            subjects = arguments[0]
            if subjects not in studyparams.ASTR_D1_CHR2_MICE:
                sys.exit('\n SUBJECT ERROR, DATAFRAME COULD NOT BE LOADED')
    else:
        subjects = 'all'
        print('No arguments given, default database with all animals will be used')
else:
    subjects = 'all'
    print("database_add_am_stats.py being ran as module, default database with all animals will be used")

if TAG == 1:
    directory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells_{}.h5'.format(subjects, tag))
else:
    directory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells.h5'.format(subjects)) 
    
dir = os.path.dirname(directory)

# Checks if file path exists
if os.path.isdir(dir):
    print('Directory Exists')
else:
    sys.exit('\n DIRECTORY ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(directory)) 
 
# ========================== Amplitude Modulated Statistics Calculation ==========================
    
db = celldatabase.load_hdf(directory) # Loads cell database 

# Iterates through each cell in the database       
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
    
    # Progress message 
    print("Processing cell {} \n {}, {}, depth = {} tetrode {}, cluster {}".format(indRow, 
          dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
              
    session = 'am'
    try:
        amEphysData, amBehavData = oneCell.load(session)
    except IndexError:
        print('This cell does not contain a {} session'.format(session))
    else: 
        # General variables for am calculations/plotting from ephys and behavior data
        amSpikeTimes = amEphysData['spikeTimes']
        amEventOnsetTimes = amEphysData['events']['soundDetectorOn']
        amEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(amEventOnsetTimes, 
                                                                    minEventOnsetDiff=0.2)
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
    
            for rate in amUniqRate:
                AMSelectInds = np.flatnonzero(amCurrentRate == rate)  # Selecting rate indices that match the specific rate
    
                # Calculating FR using the indexes of the specific rate from above
                nspkBaseOnset, nspkRespOnset = funcs.calculate_spike_count(amEventOnsetTimes,
                                                                            amSpikeTimes,
                                                                            amBaseTimeOnset,
                                                                            selectinds=AMSelectInds)
                nspkBaseSustained, nspkRespSustained = funcs.calculate_spike_count(amEventOnsetTimes,
                                                                                    amSpikeTimes,
                                                                                    amBaseTimeSustained,
                                                                                    selectinds=AMSelectInds)
                # Comapring the current FR to previous highest FR so that ultimately we save the rate with highest FR
                if np.mean(nspkRespOnset) > amOnsetFR or amOnsetFR == 0:
                    amOnsetFR = np.mean(nspkRespOnset)
                    amRespOnsetSpikes = nspkRespOnset
                    amBaseOnsetSpikes = nspkBaseOnset
                    amRateBestOnset = rate
                if np.mean(nspkRespSustained) > amSusFR or amSusFR == 0:
                    amSusFR = np.mean(nspkRespSustained)
                    amRespSustainedSpikes = nspkRespSustained
                    amBaseSustainedSpikes = nspkBaseSustained
                    amRateBestSustained = rate
                    
            # db.at[indRow, 'AMBaseFROnset'] = np.mean(amBaseOnsetSpikes)  # Mean baseline FR matched for the onset period (-100 ms to 0 ms)
            # db.at[indRow, 'AMRespFROnset'] = np.mean(amRespOnsetSpikes)  # Mean response FR for the onset period (0 ms to 100 ms)
            # db.at[indRow, 'AMHigestRateOnset'] = amRateBestOnset  # Rate that gave the highest onset response
            # db.at[indRow, 'AMBaseFRSustained'] = np.mean(amBaseSustainedSpikes)  # Mean baseline FR paired with sustained period (-500 ms to -100 ms)
            # db.at[indRow, 'AMRespFRSustained'] = np.mean(amRespSustainedSpikes)  # Mean response FR for sustained period (100 ms to 500 ms)
            db.at[indRow, 'AMBestRateSustained'] = amRateBestSustained  # Rate that gave the highest sustained response
    
            zStat, pVal = \
                funcs.sound_response_any_stimulus(amEventOnsetTimes, amSpikeTimes, amTrialsEachCond, amResponseTime,
                                                  amBaseTime)
            db.at[indRow, 'AMPval'] = pVal  # p-value from Mann-Whitney U test
            db.at[indRow, 'AMZstat'] = zStat  # U-statistic from Mann-Whitney U test
    
            correctedPval = 0.05 / len(amUniqRate)  # Correcting for comparison of multiple p-values
    
            # Decide whether to make the next calculations based on 0.05 or on corrected value
            if pVal > correctedPval:  # No response
                print("No significant AM response, no synchronization will be calculated")
            elif pVal < correctedPval:
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
                    
                allFreqSyncPVal, allFreqSyncZScore, allFreqVectorStrength, allFreqRal = \
                    funcs.calculate_am_significance_synchronization(amSyncSpikeTimesFromEventOnset,
                                                                    amSyncTrialIndexForEachSpike, amCurrentRate,
                                                                    amUniqRate)
                amSyncPValue = np.min(allFreqSyncPVal)
                amSyncZStat = np.max(allFreqSyncZScore)
                db.at[indRow, 'AMsynchronizationPval'] = amSyncPValue  # p-value from Rayleigh's test for periodicity
                db.at[indRow, 'AMsynchronizationZstat'] = amSyncZStat  # Statistic from Rayleigh's test for periodicity
    
                # ========================== Phase Descrimination Accuracy ==========================
                
                phaseDiscrimAccuracyDict = funcs.calculate_phase_discrim_accuracy(amSpikeTimes, amEventOnsetTimes,
                                                                                  amCurrentRate, amUniqRate)

                for rate in amUniqRate:
                    db.at[indRow, 'phaseDiscrimAccuracy{}Hz'.format(int(rate))] = \
                        phaseDiscrimAccuracyDict[int(rate)]
    
                # ========================== Rate Descrimination Accuracy ==========================
                        
                rateDiscrimAccuracy = funcs.calculate_rate_discrimination_accuracy(amSpikeTimes, amEventOnsetTimes,
                                                                                    amBaseTime, amResponseTime,
                                                                                    amCurrentRate)
                
                db.at[indRow, 'rateDiscrimAccuracy'] = rateDiscrimAccuracy
                
                # ========================== Highest Synchronization  ==========================

                if any(allFreqSyncPVal < 0.05):
                    sigPvals = np.array(allFreqSyncPVal) < 0.05
                    highestSyncInd = funcs.index_all_true_before(sigPvals)
                    db.at[indRow, 'highestSync'] = amUniqRate[allFreqSyncPVal < 0.05].max()
                    db.at[indRow, 'highestUSync'] = amUniqRate[highestSyncInd]
                else:
                    db.at[indRow, 'highestSync'] = 0
    
                if any(allFreqSyncPVal < correctedPval):
                    db.at[indRow, 'highestSyncCorrected'] = amUniqRate[allFreqSyncPVal < correctedPval].max()  # Storing the highest rate that should synchronization from the Rayleigh test
                    freqsBelowThresh = allFreqSyncPVal < correctedPval
                    freqsBelowThresh = freqsBelowThresh.astype(int)
                else:
                    db.at[indRow, 'highestSyncCorrected'] = 0

# ========================== Saving ==========================

celldatabase.save_hdf(db, directory)
print("SAVED DATAFRAME to {}".format(directory))