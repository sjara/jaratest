import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
sys.path.append('/home/jarauser/src/jaratest/maxh')
#sys.path.append('C:/Users/mdhor/Documents/GitHub/jaratest/maxh')
import oddball_analysis_functions as odbl
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import studyparams
import time

start_time = time.time()

timeRangePlot = [-0.3, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeStimChord = [ 0.015, 0.065]
timeRangeBaseline = [-0.2, 0]
timeRangeBaselineChord = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
baselineDurationChord = timeRangeBaselineChord[1] - timeRangeBaselineChord[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]
stimDurationChord = timeRangeStimChord[1] - timeRangeStimChord[0]


"""
Choose which database to generate.
1 = database with all trials.
2 = database with only nonrunning trials.
3 = database with only running trials.

Selection only changes oddball_sequence paradigm trials.
"""
databaseType = 3


subjects = ['acid010']
#subjects = studyparams.SUBJECTS
for subject in subjects:
    dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
    dbFilename = os.path.join(dbPath,f'celldb_{subject}.h5')


    celldb = celldatabase.load_hdf(dbFilename)

    reagents = studyparams.REAGENTS


    nCells = len(celldb)

    baselineFiringPureTones = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    stimAvgFiringPureTones = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    stimMaxAvgFiringPureTones = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    stimBestFrequency = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    gaussianAmplitude = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    gaussianMean = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    gaussianSigma = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    rSquaredColumn = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    upOddSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    upStandardSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    downStandardSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    downOddSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    upOddballIndex = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    downOddballIndex = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineUpStandardFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineDownStandardFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineUpOddFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineDownOddFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}

    highOddSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    highStandardSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    lowStandardSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    lowOddSpikesAvgFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    highOddballIndex = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    lowOddballIndex = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineHighStandardFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineLowStandardFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineHighOddFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}
    baselineLowOddFiringRate = {'pre':np.empty(nCells), 'saline':np.empty(nCells), 'doi':np.empty(nCells)}


    for indRow, dbRow in celldb.iterrows():
        oneCell = ephyscore.Cell(dbRow)


        # ignore cells from session without a synclight. 
        if ((databaseType == 2) | (databaseType == 3) & (dbRow.date == studyparams.N0_LIGHT_DATE)):
            pass
        else:
            for reagent in reagents:
                sessionType = f'{reagent}PureTones'
            
                ephysData, bdata = oneCell.load(sessionType)  
                spikeTimes = ephysData['spikeTimes']
                eventOnsetTimes = ephysData['events']['stimOn']

                
                frequencies_each_trial = bdata['currentFreq']
                array_of_frequencies = np.unique(bdata['currentFreq'])
                
                # Checks to see if trial count from bdata is the same as trial count from ephys
                if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
                    print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
                    sys.exit()

                # If the ephys data is 1 more than the bdata, delete the last ephys trial.
                if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
                    eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]



                
                (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRangePlot)

                trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

                spikeCountMatBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRangeBaseline)
                spikeCountMatStim = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRangeStim)

                baselineFiringPureTones[reagent][indRow] = np.mean(spikeCountMatBase) / baselineDuration

                nTrials = len(indexLimitsEachTrial[0])
                trialsEachCondInds, nTrialsEachCond, nCond= extraplots.trials_each_cond_inds(trialsEachCond, nTrials)

                firingRates = np.empty(nCond)
                for cond in range(trialsEachCond.shape[1]):
                    nSpikesEachTrial = spikeCountMatStim[trialsEachCond[:,cond]]
                    avgSpikes = np.mean(nSpikesEachTrial)
                    spikesFiringRate = (avgSpikes / stimDuration)
                    firingRates[cond] = spikesFiringRate
                avgFiringRate = np.mean(firingRates)
                maxAvgFiringRate = firingRates.max()
                bestFreq = array_of_frequencies[np.argmax(firingRates)]


                stimAvgFiringPureTones[reagent][indRow] = avgFiringRate
                stimMaxAvgFiringPureTones[reagent][indRow] = maxAvgFiringRate
                stimBestFrequency[reagent][indRow] = bestFreq

                try:
                    possibleLogFreq = np.log2(array_of_frequencies)
                    fitParams, RSquared = extraplots.fit_tuning_curve(possibleLogFreq, firingRates)

                    gaussianAmplitude[reagent][indRow] = fitParams[0]
                    gaussianMean[reagent][indRow] = fitParams[1]
                    gaussianSigma[reagent][indRow] = fitParams[2]
                    rSquaredColumn[reagent][indRow] = RSquared
                except:
                    gaussianAmplitude[reagent][indRow] = np.nan
                    gaussianMean[reagent][indRow] = np.nan
                    gaussianSigma[reagent][indRow] = np.nan
                    rSquaredColumn[reagent][indRow] = np.nan

                

            for reagent in reagents:
                sessionType = reagent

                spikeTimesFromEventOnsetUp, trialIndexForEachSpikeUp, indexLimitsEachTrialUp, upOdd, downStandard = odbl.load_data(oneCell, f'{sessionType}FM_Up', timeRangePlot)
                spikeTimesFromEventOnsetDown, trialIndexForEachSpikeDown, indexLimitsEachTrialDown, upStandard, downOdd = odbl.load_data(oneCell, f'{sessionType}FM_Down', timeRangePlot)

                trialsBeforeUpOddDownStd = odbl.trials_before_oddball(upOdd)       
                trialsBeforeDownOddUpStd = odbl.trials_before_oddball(downOdd)

                
                ##############
                if databaseType == 1:
                    pass
                
                elif databaseType == 2:
                    #runningDBFilename = os.path.join(dbPath, f'{subject}_runningBooleanDB.h5')
                    runningArrayFilename = os.path.join(dbPath, f'{subject}_runningBooleanArrayNon.npy')
                    #runningDB = celldatabase.load_hdf(runningDBFilename)

                    runningNumpyArray = np.load(runningArrayFilename, allow_pickle=True)

                    """
                    runArrayFM_Up = runningDB.query("date == @dbRow.date & experiment == '03'")[f"{sessionType}_running_array"]
                    runArrayFM_Down = runningDB.query("date == @dbRow.date & experiment == '04'")[f"{sessionType}_running_array"]
                    """
                    sessionIndex = np.where((runningNumpyArray[0] == dbRow.date) & (runningNumpyArray[1] == reagent))[0][0]

                    nonRunArrayFM_Up = runningNumpyArray[5][sessionIndex].reshape(-1,1)
                    nonRunArrayFM_Down = runningNumpyArray[4][sessionIndex].reshape(-1,1)  


                    """
                    # to match the trial from behaviordata, pandas column needs to be squeezed out of nested array, converted to boolean, and reshaped.
                    runArrayFM_Up = np.squeeze(runArrayFM_Up).astype(bool).reshape(-1,1)
                    runArrayFM_Down = np.squeeze(runArrayFM_Down).astype(bool).reshape(-1,1)
                    """

                    upOdd = upOdd & nonRunArrayFM_Up
                    trialsBeforeUpOddDownStd = trialsBeforeUpOddDownStd & nonRunArrayFM_Up
                    trialsBeforeDownOddUpStd = trialsBeforeDownOddUpStd & nonRunArrayFM_Down
                    downOdd = downOdd & nonRunArrayFM_Down

                elif databaseType == 3:
                    runningArrayFilename = os.path.join(dbPath, f'{subject}_runningBooleanArrayRun.npy')
                    runningNumpyArray = np.load(runningArrayFilename, allow_pickle=True)

                    sessionIndex = np.where((runningNumpyArray[0] == dbRow.date) & (runningNumpyArray[1] == reagent))[0][0]

                    runArrayFM_Up = runningNumpyArray[5][sessionIndex].reshape(-1,1)
                    runArrayFM_Down = runningNumpyArray[4][sessionIndex].reshape(-1,1)

                    upOdd = upOdd & runArrayFM_Up
                    trialsBeforeUpOddDownStd = trialsBeforeUpOddDownStd & runArrayFM_Up
                    trialsBeforeDownOddUpStd = trialsBeforeDownOddUpStd & runArrayFM_Down
                    downOdd = downOdd & runArrayFM_Down
                else:
                    print('please select the databaseType.')
                    exit()
                


                 ####################
                spikeCountMatUp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetUp, indexLimitsEachTrialUp, timeRangeStim)
                spikeCountMatUpBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetUp, indexLimitsEachTrialUp, timeRangeBaseline)


                spikeCountMatDown = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetDown, indexLimitsEachTrialDown, timeRangeStim)
                spikeCountMatDownBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetDown, indexLimitsEachTrialDown, timeRangeBaseline)


                firingRates = np.empty(nCond)

                upOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatUp[upOdd])) / stimDuration
                downStandardSpikesAvgFiringRate[reagent][indRow] =  (np.mean(spikeCountMatUp[trialsBeforeUpOddDownStd])) / stimDuration
                downOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatDown[downOdd])) / stimDuration
                upStandardSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatDown[trialsBeforeDownOddUpStd])) / stimDuration
                baselineUpStandardFiringRate[reagent][indRow] = (np.mean(spikeCountMatDownBase[trialsBeforeDownOddUpStd])) / baselineDuration
                baselineDownStandardFiringRate[reagent][indRow] = (np.mean(spikeCountMatUpBase[trialsBeforeUpOddDownStd])) / baselineDuration
                baselineUpOddFiringRate[reagent][indRow] = (np.mean(spikeCountMatUpBase[upOdd])) / baselineDuration
                baselineDownOddFiringRate[reagent][indRow] = (np.mean(spikeCountMatDownBase[downOdd])) / baselineDuration


                upOddballIndex[reagent][indRow] = ((upOddSpikesAvgFiringRate[reagent][indRow] - upStandardSpikesAvgFiringRate[reagent][indRow]) / (upOddSpikesAvgFiringRate[reagent][indRow] + upStandardSpikesAvgFiringRate[reagent][indRow]))
                downOddballIndex[reagent][indRow] = ((downOddSpikesAvgFiringRate[reagent][indRow] - downStandardSpikesAvgFiringRate[reagent][indRow]) / (downOddSpikesAvgFiringRate[reagent][indRow] + downStandardSpikesAvgFiringRate[reagent][indRow]))

                # Chord Tones

                spikeTimesFromEventOnsetHigh, trialIndexForEachSpikeHigh, indexLimitsEachTrialHigh, lowStandard, highOdd = odbl.load_data(oneCell, f'{sessionType}HighFreq', timeRangePlot)
                spikeTimesFromEventOnsetLow, trialIndexForEachSpikeLow, indexLimitsEachTrialLow, lowOdd, highStandard = odbl.load_data(oneCell, f'{sessionType}LowFreq', timeRangePlot)

                trialsBeforeHighOddLowStd = odbl.trials_before_oddball(highOdd)       
                trialsBeforeLowOddHighStd = odbl.trials_before_oddball(lowOdd)

                ############
                if databaseType == 2:

                    nonRunArrayHighFreq = runningNumpyArray[2][sessionIndex].reshape(-1,1)
                    nonRunArrayLowFreq = runningNumpyArray[3][sessionIndex].reshape(-1,1)
                    

                    highOdd = highOdd & nonRunArrayHighFreq
                    trialsBeforeHighOddLowStd = trialsBeforeHighOddLowStd & nonRunArrayHighFreq
                    trialsBeforeLowOddHighStd = trialsBeforeLowOddHighStd & nonRunArrayLowFreq
                    lowOdd = lowOdd & nonRunArrayLowFreq

                elif databaseType == 3:

                    runArrayHighFreq = runningNumpyArray[2][sessionIndex].reshape(-1,1)
                    runArrayLowFreq = runningNumpyArray[3][sessionIndex].reshape(-1,1)


                    highOdd = highOdd & runArrayHighFreq
                    trialsBeforeHighOddLowStd = trialsBeforeHighOddLowStd & runArrayHighFreq
                    trialsBeforeLowOddHighStd = trialsBeforeLowOddHighStd & runArrayLowFreq
                    lowOdd = lowOdd & runArrayLowFreq
                ###########

                #trialsBeforeOddLowStd, lowOdd = odbl.compare_trial_count(trialsBeforeOddLowStd, lowOdd)
                #trialsBeforeOddHighStd, highOdd = odbl.compare_trial_count(trialsBeforeOddHighStd, highOdd)





                spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetHigh, indexLimitsEachTrialHigh, timeRangeStimChord)
                spikeCountMatHighBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetHigh, indexLimitsEachTrialHigh, timeRangeBaselineChord)


                spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetLow, indexLimitsEachTrialLow, timeRangeStimChord)
                spikeCountMatLowBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetLow, indexLimitsEachTrialLow, timeRangeBaselineChord)

                #spikeCountMatLow, spikeCountMatHigh = odbl.compare_trial_count(spikeCountMatLow, spikeCountMatHigh)
                #spikeCountMatLowBase, spikeCountMatHighBase = odbl.compare_trial_count(spikeCountMatLowBase, spikeCountMatHighBase)


                firingRates = np.empty(nCond)

                highOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatHigh[highOdd])) / stimDurationChord
                lowStandardSpikesAvgFiringRate[reagent][indRow] =  (np.mean(spikeCountMatHigh[trialsBeforeHighOddLowStd])) / stimDurationChord
                lowOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatLow[lowOdd])) / stimDurationChord
                highStandardSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatLow[trialsBeforeLowOddHighStd])) / stimDurationChord
                baselineHighStandardFiringRate[reagent][indRow] = (np.mean(spikeCountMatLowBase[trialsBeforeLowOddHighStd])) / baselineDurationChord
                baselineLowStandardFiringRate[reagent][indRow] = (np.mean(spikeCountMatHighBase[trialsBeforeHighOddLowStd])) / baselineDurationChord
                baselineHighOddFiringRate[reagent][indRow] = (np.mean(spikeCountMatHighBase[highOdd])) / baselineDurationChord
                baselineLowOddFiringRate[reagent][indRow] = (np.mean(spikeCountMatLowBase[lowOdd])) / baselineDurationChord


                highOddballIndex[reagent][indRow] = ((highOddSpikesAvgFiringRate[reagent][indRow] - highStandardSpikesAvgFiringRate[reagent][indRow]) / (highOddSpikesAvgFiringRate[reagent][indRow] + highStandardSpikesAvgFiringRate[reagent][indRow]))
                lowOddballIndex[reagent][indRow] = ((lowOddSpikesAvgFiringRate[reagent][indRow] - lowStandardSpikesAvgFiringRate[reagent][indRow]) / (lowOddSpikesAvgFiringRate[reagent][indRow] + lowStandardSpikesAvgFiringRate[reagent][indRow]))

                elapsed_time = time.time() - start_time
                minutes, seconds = divmod(elapsed_time, 60)
                print(f"Elapsed time: {int(minutes)}:{int(seconds)}")

    celldb['baselineFiringRatePureTonesSaline'] = baselineFiringPureTones['saline']
    celldb['baselineFiringRatePureTonesDOI'] = baselineFiringPureTones['doi']
    celldb['baselineFiringRatePureTonesPre'] = baselineFiringPureTones['pre']

    celldb['stimFiringRatePureTonesSaline'] = stimAvgFiringPureTones['saline']
    celldb['stimFiringRatePureTonesDOI'] = stimAvgFiringPureTones['doi']
    celldb['stimFiringRatePureTonesPre'] = stimAvgFiringPureTones['pre']

    celldb['stimMaxAvgFiringRatePureTonesSaline'] = stimMaxAvgFiringPureTones['saline']
    celldb['stimMaxAvgFiringRatePureTonesDOI'] = stimMaxAvgFiringPureTones['doi']
    celldb['stimMaxAvgFiringRatePureTonesPre'] = stimMaxAvgFiringPureTones['pre']

    celldb['stimBestFrequencyPureTonesSaline'] = stimBestFrequency['saline']
    celldb['stimBestFrequencyPureTonesDOI'] = stimBestFrequency['doi']
    celldb['stimBestFrequencyPureTonesPre'] = stimBestFrequency['pre']

    celldb['upOddSpikesAvgFiringRateSaline'] = upOddSpikesAvgFiringRate['saline']
    celldb['upOddSpikesAvgFiringRateDOI'] = upOddSpikesAvgFiringRate['doi']
    celldb['upOddSpikesAvgFiringRatePre'] = upOddSpikesAvgFiringRate['pre']

    celldb['downStandardSpikesAvgFiringRateSaline'] = downStandardSpikesAvgFiringRate['saline']
    celldb['downStandardSpikesAvgFiringRateDOI'] = downStandardSpikesAvgFiringRate['doi']
    celldb['downStandardSpikesAvgFiringRatePre'] = downStandardSpikesAvgFiringRate['pre']

    celldb['downOddSpikesAvgFiringRateSaline'] = downOddSpikesAvgFiringRate['saline']
    celldb['downOddSpikesAvgFiringRateDOI'] = downOddSpikesAvgFiringRate['doi']
    celldb['downOddSpikesAvgFiringRatePre'] = downOddSpikesAvgFiringRate['pre']

    celldb['upStandardSpikesAvgFiringRateSaline'] = upStandardSpikesAvgFiringRate['saline']
    celldb['upStandardSpikesAvgFiringRateDOI'] = upStandardSpikesAvgFiringRate['doi']
    celldb['upStandardSpikesAvgFiringRatePre'] = upStandardSpikesAvgFiringRate['pre']

    celldb['upOddballIndexSaline'] = upOddballIndex['saline']
    celldb['upOddballIndexDOI'] = upOddballIndex['doi']
    celldb['upOddballIndexPre'] = upOddballIndex['pre']

    celldb['downOddballIndexSaline'] = downOddballIndex['saline']
    celldb['downOddballIndexDOI'] = downOddballIndex['doi']
    celldb['downOddballIndexPre'] = downOddballIndex['pre']


    celldb['gaussianAmplitudeSaline'] = gaussianAmplitude['saline']
    celldb['gaussianAmplitudeDOI'] = gaussianAmplitude['doi']
    celldb['gaussianAmplitudePre'] = gaussianAmplitude['pre']

    celldb['gaussianMeanSaline'] = gaussianMean['saline']
    celldb['gaussianMeanDOI'] = gaussianMean['doi']
    celldb['gaussianMeanPre'] = gaussianMean['pre']

    celldb['gaussianSigmaSaline'] = gaussianSigma['saline']
    celldb['gaussianSigmaeDOI'] = gaussianSigma['doi']
    celldb['gaussianSigmaePre'] = gaussianSigma['pre']


    celldb['rSquaredColumnSaline'] = rSquaredColumn['saline']
    celldb['rSquaredColumnDOI'] = rSquaredColumn['doi']
    celldb['rSquaredColumnPre'] = rSquaredColumn['pre']

    celldb['baselineUpStandardFiringRateSaline'] =  baselineUpOddFiringRate['saline']
    celldb['baselineUpStandardFiringRateDOI'] =  baselineUpOddFiringRate['doi']
    celldb['baselineUpStandardFiringRatePre'] =  baselineUpOddFiringRate['pre']

    celldb['baselineDownStandardFiringRateSaline'] =  baselineDownOddFiringRate['saline']
    celldb['baselineDownStandardFiringRateDOI'] =  baselineDownOddFiringRate['doi']
    celldb['baselineDownStandardFiringRatePre'] =  baselineDownOddFiringRate['pre']

    celldb['baselineUpOddFiringRateSaline'] =  baselineUpOddFiringRate['saline']
    celldb['baselineUpOddFiringRateDOI'] =  baselineUpOddFiringRate['doi']
    celldb['baselineUpOddFiringRatePre'] =  baselineUpOddFiringRate['pre']

    celldb['baselineDownOddFiringRateSaline'] =  baselineDownOddFiringRate['saline']
    celldb['baselineDownOddFiringRateDOI'] =  baselineDownOddFiringRate['doi']
    celldb['baselineDownOddFiringRatePre'] =  baselineDownOddFiringRate['pre']


    # Chords

    celldb['highOddSpikesAvgFiringRateSaline'] = highOddSpikesAvgFiringRate['saline']
    celldb['highOddSpikesAvgFiringRateDOI'] = highOddSpikesAvgFiringRate['doi']
    celldb['highOddSpikesAvgFiringRatePre'] = highOddSpikesAvgFiringRate['pre']

    celldb['lowStandardSpikesAvgFiringRateSaline'] = lowStandardSpikesAvgFiringRate['saline']
    celldb['lowStandardSpikesAvgFiringRateDOI'] = lowStandardSpikesAvgFiringRate['doi']
    celldb['lowStandardSpikesAvgFiringRatePre'] = lowStandardSpikesAvgFiringRate['pre']

    celldb['lowOddSpikesAvgFiringRateSaline'] = lowOddSpikesAvgFiringRate['saline']
    celldb['lowOddSpikesAvgFiringRateDOI'] = lowOddSpikesAvgFiringRate['doi']
    celldb['lowOddSpikesAvgFiringRatePre'] = lowOddSpikesAvgFiringRate['pre']

    celldb['highStandardSpikesAvgFiringRateSaline'] = highStandardSpikesAvgFiringRate['saline']
    celldb['highStandardSpikesAvgFiringRateDOI'] = highStandardSpikesAvgFiringRate['doi']
    celldb['highStandardSpikesAvgFiringRatePre'] = highStandardSpikesAvgFiringRate['pre']

    celldb['highOddballIndexSaline'] = highOddballIndex['saline']
    celldb['highOddballIndexDOI'] = highOddballIndex['doi']
    celldb['highOddballIndexPre'] = highOddballIndex['pre']

    celldb['lowOddballIndexSaline'] = lowOddballIndex['saline']
    celldb['lowOddballIndexDOI'] = lowOddballIndex['doi']
    celldb['lowOddballIndexPre'] = lowOddballIndex['pre']

    celldb['baselineHighStandardFiringRateSaline'] =  baselineHighOddFiringRate['saline']
    celldb['baselineHighStandardFiringRateDOI'] =  baselineHighOddFiringRate['doi']
    celldb['baselineHighStandardFiringRatePre'] =  baselineHighOddFiringRate['pre']

    celldb['baselineLowStandardFiringRateSaline'] =  baselineLowOddFiringRate['saline']
    celldb['baselineLowStandardFiringRateDOI'] =  baselineLowOddFiringRate['doi']
    celldb['baselineLowStandardFiringRatePre'] =  baselineLowOddFiringRate['pre']

    celldb['baselineHighOddFiringRateSaline'] =  baselineHighOddFiringRate['saline']
    celldb['baselineHighOddFiringRateDOI'] =  baselineHighOddFiringRate['doi']
    celldb['baselineHighOddFiringRatePre'] =  baselineHighOddFiringRate['pre']

    celldb['baselineLowOddFiringRateSaline'] =  baselineLowOddFiringRate['saline']
    celldb['baselineLowOddFiringRateDOI'] =  baselineLowOddFiringRate['doi']
    celldb['baselineLowOddFiringRatePre'] =  baselineLowOddFiringRate['pre']


    if databaseType == 1:
        dbNewFilename = os.path.join(dbPath, f'{subject}_puretone_and_oddball_calcs_all.h5')
    
    if databaseType == 2:
        dbNewFilename = os.path.join(dbPath, f'{subject}_puretone_and_oddball_calcs_nonRunning.h5')
    
    if databaseType == 3:
        dbNewFilename = os.path.join(dbPath, f'{subject}_puretone_and_oddball_calcs_running.h5')

    celldatabase.save_hdf(celldb, dbNewFilename)
