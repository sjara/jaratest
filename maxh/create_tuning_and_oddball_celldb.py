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

timeRangePlot = [-0.3, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeBaseline = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]


subject = 'acid006'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')

celldb = celldatabase.generate_cell_database(inforecFile)
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

reagents = ('saline', 'doi')


nCells = len(celldb)

baselineFiringPureTones = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
stimAvgFiringPureTones = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
stimMaxFiringPureTones = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
stimBestFrequency = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
gaussianAmplitude = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
gaussianMean = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
gaussianSigma = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
rSquaredColumn = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
upOddSpikesAvgFiringRate = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
downStandardSpikesAvgFiringRate = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
downOddSpikesAvgFiringRate = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
upStandardSpikesAvgFiringRate = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
upOddballIndex = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}
downOddballIndex = {'saline':np.empty(nCells), 'doi':np.empty(nCells)}


for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)

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
        maxFiringRate = firingRates.max()
        bestFreq = array_of_frequencies[np.argmax(firingRates)]


        stimAvgFiringPureTones[reagent][indRow] = avgFiringRate
        stimMaxFiringPureTones[reagent][indRow] = maxAvgFiringRate
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
        spikeTimesFromEventOnsetUp, trialIndexForEachSpikeUp, indexLimitsEachTrialUp, upOdd, downStandard = odbl.main_function(oneCell, f'{sessionType}FM_Up', timeRangePlot)
        spikeTimesFromEventOnsetDown, trialIndexForEachSpikeDown, indexLimitsEachTrialDown, upStandard, downOdd = odbl.main_function(oneCell, f'{sessionType}FM_Down', timeRangePlot)

        trialsBeforeOddDownStd = odbl.trials_before_oddball(upOdd)       
        trialsBeforeOddUpStd = odbl.trials_before_oddball(downOdd)

        spikeCountMatUp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetUp, indexLimitsEachTrialUp, timeRangeStim)
        spikeCountMatDown = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetDown, indexLimitsEachTrialDown, timeRangeStim)

        firingRates = np.empty(nCond)

        upOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatUp[upOdd])) / stimDuration
        downStandardSpikesAvgFiringRate[reagent][indRow] =  (np.mean(spikeCountMatUp[trialsBeforeOddDownStd])) / stimDuration
        downOddSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatDown[downOdd])) / stimDuration
        upStandardSpikesAvgFiringRate[reagent][indRow] = (np.mean(spikeCountMatDown[trialsBeforeOddUpStd])) / stimDuration

        upOddballIndex[reagent][indRow] = ((upOddSpikesAvgFiringRate[reagent][indRow] - upStandardSpikesAvgFiringRate[reagent][indRow]) / (upOddSpikesAvgFiringRate[reagent][indRow] + upStandardSpikesAvgFiringRate[reagent][indRow]))
        downOddballIndex[reagent][indRow] = ((downOddSpikesAvgFiringRate[reagent][indRow] - downStandardSpikesAvgFiringRate[reagent][indRow]) / (downOddSpikesAvgFiringRate[reagent][indRow] + downStandardSpikesAvgFiringRate[reagent][indRow]))




celldb['baselineFiringRatePureTonesSaline'] = baselineFiringPureTones['saline']
celldb['baselineFiringRatePureTonesDOI'] = baselineFiringPureTones['doi']

celldb['stimFiringRatePureTonesSaline'] = stimAvgFiringPureTones['saline']
celldb['stimFiringRatePureTonesDOI'] = stimAvgFiringPureTones['doi']

celldb['stimMaxFiringRatePureTonesSaline'] = stimMaxFiringPureTones['saline']
celldb['stimMaxFiringRatePureTonesDOI'] = stimMaxFiringPureTones['doi']

celldb['stimBestFrequencyPureTonesSaline'] = stimBestFrequency['saline']
celldb['stimBestFrequencyPureTonesDOI'] = stimBestFrequency['doi']

celldb['upOddSpikesAvgFiringRateSaline'] = upOddSpikesAvgFiringRate['saline']
celldb['upOddSpikesAvgFiringRateDOI'] = upOddSpikesAvgFiringRate['doi']

celldb['downStandardSpikesAvgFiringRateSaline'] = downStandardSpikesAvgFiringRate['saline']
celldb['downStandardSpikesAvgFiringRateDOI'] = downStandardSpikesAvgFiringRate['doi']

celldb['downOddSpikesAvgFiringRateSaline'] = downOddSpikesAvgFiringRate['saline']
celldb['downOddSpikesAvgFiringRateDOI'] = downOddSpikesAvgFiringRate['doi']

celldb['upStandardSpikesAvgFiringRateSaline'] = upStandardSpikesAvgFiringRate['saline']
celldb['upStandardSpikesAvgFiringRateDOI'] = upStandardSpikesAvgFiringRate['doi']

celldb['upOddballIndexSaline'] = upOddballIndex['saline']
celldb['upOddballIndexDOI'] = upOddballIndex['doi']

celldb['downOddballIndexSaline'] = downOddballIndex['saline']
celldb['downOddballIndexDOI'] = downOddballIndex['doi']

celldb['gaussianAmplitudeSaline'] = gaussianAmplitude['saline']
celldb['gaussianAmplitudeDOI'] = gaussianAmplitude['doi']

celldb['gaussianMeanSaline'] = gaussianMean['saline']
celldb['gaussianMeanDOI'] = gaussianMean['doi']

celldb['gaussianSigmaSaline'] = gaussianSigma['saline']
celldb['gaussianSigmaeDOI'] = gaussianSigma['doi']

celldb['rSquaredColumnSaline'] = rSquaredColumn['saline']
celldb['rSquaredColumnDOI'] = rSquaredColumn['doi']

filename = 'C:/Users/mdhor/Documents/updatedAcid006.h5'
celldatabase.save_hdf(celldb, filename)
