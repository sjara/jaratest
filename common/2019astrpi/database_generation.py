"""
Generate[1] and save[2] database with calculated stats and parameters that will be used in /
analysis. Optionally takes the arguments in the order of: script.py mouse run_parameters
"""
import os
import sys
import numpy as np
import studyparams
from scipy import stats
from scipy import signal
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import database_generation_funcs as funcs
import database_cell_locations as cellLoc


if sys.version_info[0] < 3:
    input_func = raw_input
elif sys.version_info[0] >= 3:
    input_func = input

SAVE = 1

def append_base_stats(cellDB, filename=''):
    """
    Calculate parameters to be used to filter cells in calculate_indices
    """

    # FILTERING DATAFRAME
    firstCells = cellDB.query(studyparams.FIRST_FLTRD_CELLS)  # isiViolations<0.02 and spikeShapeQuality>2

    for indIter, (indRow, dbRow) in enumerate(firstCells.iterrows()):

        dbRow = firstCells.loc[indRow]
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
            baseRange = [-0.1, 0]  # if session != 'laserpulse' else [-0.05,-0.04]
            nspkBase, nspkResp = funcs.calculate_firing_rate(noiseEphysData, baseRange, session)
            respSpikeMean = nspkResp.ravel().mean()

            # Significance calculations for the noiseburst
            try:
                zStats, pVals = stats.mannwhitneyu(nspkResp, nspkBase)
            except ValueError:  # All numbers identical will cause mann-whitney to fail, therefore p-value should be 1 as there is no difference
                zStats, pVals = [0, 1]

            # Adding noiseburst values to the dataframe
            firstCells.loc[
                indRow, '{}_pVal'.format(session)] = pVals  # changed from at to loc via recommendation from pandas
            firstCells.loc[indRow, '{}_FR'.format(session)] = respSpikeMean  # mean firing rate

        # ------------ Laserpulse calculations --------------------------------
        session = 'laserpulse'
        try:
            pulseEphysData, noBData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            baseRange = [-0.1, 0]  # if session != 'laserpulse' else [-0.05,-0.04]
            nspkBase, nspkResp = funcs.calculate_firing_rate(pulseEphysData, baseRange, session)
            respSpikeMean = nspkResp.ravel().mean()

            # Significance calculations for the laserpulse
            try:
                zStats, pVals = stats.mannwhitneyu(nspkResp, nspkBase)
            except ValueError:  # All numbers identical will cause mann-whitney to fail
                zStats, pVals = [0, 1]

            # Adding laserpulse calculations to the dataframe
            firstCells.loc[
                indRow, '{}_pVal'.format(session)] = pVals  # changed from at to loc via recommendation from pandas
            firstCells.loc[indRow, '{}_FR'.format(session)] = respSpikeMean  # mean firing rate

        # -------------- Tuning curve calculations ----------------------------
        session = 'tuningCurve'
        try:
            tuningEphysData, tuningBehavData = oneCell.load(session)
        except IndexError:
            print('This cell does not contain a {} session'.format(session))
        else:
            baseRange = [-0.1, 0] if session != 'am' else [-0.5, -0.1]

            # Extracting information from ephys and behavior data to do calculations later with
            currentFreq = tuningBehavData['currentFreq']
            currentIntensity = tuningBehavData['currentIntensity']
            # trialsEachType = behavioranalysis.find_trials_each_type(currentFreq, np.unique(currentFreq))
            uniqFreq = np.unique(currentFreq)
            uniqueIntensity = np.unique(currentIntensity)

            allIntenBase = np.array([])
            respSpikeMean = np.empty((len(uniqueIntensity), len(uniqFreq)))  # same as allIntenResp
            allIntenRespMedian = np.empty((len(uniqueIntensity), len(uniqFreq)))
            Rsquareds = np.empty((len(uniqueIntensity), len(uniqFreq)))
            spikeTimes = tuningEphysData['spikeTimes']
            eventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)

            # Checking to see if the ephys data has one more trial than the behavior data and removing the last session if it does
            if len(eventOnsetTimes) == (len(currentFreq) + 1):
                eventOnsetTimes = eventOnsetTimes[0:-1]
                print("Correcting ephys data to be same length as behavior data")
                toCalculate = True
            elif len(eventOnsetTimes) == len(currentFreq):
                print("Data is already the same length")
                toCalculate = True
            else:
                print("Something is wrong with the length of these data")
                toCalculate = False
                # Instead of generating an error I made it just not calculate statistics. I should posisbly have it log all mice
                # and sites where it failed to calculate so someone can review later

        # -------------------- Start of calculations for the tuningCurve data -------------------------
            # The latency of the cell from the onset of the stim
            if toCalculate:
                respLatency = funcs.calculate_latency(eventOnsetTimes, currentFreq, uniqFreq, currentIntensity,
                                                      uniqueIntensity, spikeTimes, indRow)
            else:
                respLatency = np.nan

            for indInten, intensity in enumerate(uniqueIntensity):
                spks = np.array([])
                freqs = np.array([])
                popts = []
                pcovs = []
                ind10AboveButNone = []
                # ------------ start of frequency specific calculations -------------
                for indFreq, freq in enumerate(uniqFreq):
                    selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == intensity)).tolist()

                    # FIXME: This function does not need to take the whole ephys
                    # data as an arguement. Needed data is already calculated outside so I just need to update the args of the functions
                    nspkBase, nspkResp = funcs.calculate_firing_rate(tuningEphysData, baseRange, session,
                                                                     selectinds=selectinds)

                    spks = np.concatenate([spks, nspkResp.ravel()])
                    freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel())) * freq])
                    respSpikeMean[indInten, indFreq] = np.mean(nspkResp)
                    allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])

                    # ------------------- Significance and fit calculations for tuning ----------------
                    Rsquared, popt = funcs.calculate_fit(uniqFreq, allIntenBase, freqs, spks)

                    Rsquareds[indInten, indFreq] = Rsquared
                    popts.append(popt)

                # ------------------------------ Intensity based calculations -------------------------
                # The reason why we are calculating bw10 here, it is to save the calculation time
                responseThreshold = funcs.calculate_response_threshold(0.2, allIntenBase, respSpikeMean)
                # [6] Find Frequency Response Area (FRA) unit: fra boolean set, yes or no, but it's originally a pair
                fra = respSpikeMean > responseThreshold
                # [6.5] get the intensity threshold
                intensityInd, freqInd = funcs.calculate_intensity_threshold_and_CF_indices(fra, respSpikeMean)
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
                        monoIndex, overallMaxSpikes = funcs.calculate_monotonicity_index(eventOnsetTimes, currentFreq,
                                                                                         currentIntensity,
                                                                                         uniqueIntensity, spikeTimes, cf
                                                                                         )
                        onsetRate, sustainedRate, baseRate = funcs.calculate_onset_to_sustained_ratio(eventOnsetTimes,
                                                                                                      spikeTimes,
                                                                                                      currentFreq,
                                                                                                      currentIntensity,
                                                                                                      cf, respLatency)
                    else:
                        monoIndex = np.nan
                        overallMaxSpikes = np.nan
                        onsetRate = np.nan
                        sustainedRate = np.nan
                        baseRate = np.nan

                    # [8] getting BW10 value, Bandwidth at 10dB above the neuron's sound intensity Threshold(SIT)
                    ind10Above = intensityInd + int(
                        10 / np.diff(uniqueIntensity)[0])  # How many inds to go above the threshold intensity ind
                    lowerFreq, upperFreq, Rsquared10AboveSIT = funcs.calculate_BW10_params(ind10Above, popts, Rsquareds,
                                                                                           responseThreshold,
                                                                                           intensityThreshold)
                    # print('lf:{},uf:{},R2:{}'.format(lowerFreq,upperFreq,Rsquared10AboveSIT))

                    if (lowerFreq is not None) and (upperFreq is not None):
                        fitMidpoint = np.sqrt(lowerFreq * upperFreq)
                        bw10 = (upperFreq - lowerFreq) / cf

                    else:
                        fitMidpoint = None
                        bw10 = None

                    # Adding tuningCurve calculations to the dataframe to be saved later
                    firstCells.at[indRow, 'thresholdFRA'] = intensityThreshold
                    firstCells.at[indRow, 'cf'] = cf
                    firstCells.at[indRow, 'lowerFreq'] = lowerFreq
                    firstCells.at[indRow, 'upperFreq'] = upperFreq
                    firstCells.at[indRow, 'rsquaredFit'] = Rsquared10AboveSIT
                    firstCells.at[indRow, 'bw10'] = bw10
                    firstCells.at[indRow, 'fit_midpoint'] = fitMidpoint
                    firstCells.at[indRow, 'latency'] = respLatency
                    firstCells.at[indRow, 'monotonicityIndex'] = monoIndex
                    firstCells.at[indRow, 'onsetRate'] = onsetRate
                    firstCells.at[indRow, 'sustainedRate'] = sustainedRate
                    firstCells.at[indRow, 'baseRate'] = baseRate

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
            amOnsetTimes = amEphysData['events']['soundDetectorOn']
            amCurrentFreq = amBehavData['currentFreq']
            amUniqFreq = np.unique(amCurrentFreq)
            amTimeRange = [-0.2, 0.7]

            if len(amCurrentFreq) != len(amOnsetTimes):
                amOnsetTimes = amOnsetTimes[:-1]
            if len(amCurrentFreq) != len(amOnsetTimes):
                print('Removing one does not align events and behavior. Skipping AM for cell')
            else:
                (amSpikeTimesFromEventOnset, amTrialIndexForEachSpike,
                 amIndexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                          amOnsetTimes,
                                                          amTimeRange)
                amBaseTime = [-0.5, -0.1]
                amOnsetTime = [0, 0.1]
                amResponseTime = [0, 0.5]

                allFreqPVal, allFreqZScore = \
                    funcs.calculate_am_significance(amSpikeTimes, amOnsetTimes, amBaseTime, amResponseTime, amCurrentFreq, amUniqFreq)


                # I am taking the lowest p-value from all the frequencies to store in the dataframe. Possibly need to add
                # way of identifying what frequency is being selected.
                # TODO: Should do some kind of post-hoc/correction on these such as
                # taking the p-value and dividing by the total number of comparisons done and using that as a threshold
                amPValue = np.min(allFreqPVal)
                firstCells.at[indRow, 'am_response_pVal'] = amPValue

                # TODO: test calculations below

                if amPValue > 0.05:  # No response
                    print("No significant AM response, no synchronization will be calculated")
                elif amPValue < 0.05:
                    amTimeRangeSync = [0.1, 0.5]  # Use this to cut out onset responses
                    (amSyncSpikeTimesFromEventOnset,
                     amSyncTrialIndexForEachSpike,
                     amSyncIndexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                                                         amOnsetTime,
                                                                                         amTimeRangeSync)

                    allFreqSyncPVal, allFreqSyncZScore, allFreqVectorStrength, allFreqRal = \
                        funcs.calculate_am_significance_synchronization(amSyncSpikeTimesFromEventOnset, amOnsetTime, amBaseTime, amOnsetTime)
                    amSyncPValue = np.min(allFreqSyncPVal)
                    firstCells.at[indRow, 'am_synchronization_pVal'] = amSyncPValue

                    if any(allFreqSyncPVal < 0.05):
                            sigPvals = np.array(allFreqSyncPVal) < 0.05
                            highestSyncInd = funcs.index_all_true_before(sigPvals)
                            firstCells.loc[indRow, 'highestSync'] = amUniqFreq[allFreqSyncPVal < 0.05].max()
                            firstCells.loc[indRow, 'highestUSync'] = amUniqFreq[highestSyncInd]
                            # print possibleFreq[pValThisCell<0.05].max()

                    else:
                        firstCells.loc[indRow, 'highestSync'] = 0

                    correctedPval = 0.05 / len(amUniqFreq)  # TODO: this can go up with where the pvalues are calculated
                    if any(allFreqSyncPVal < correctedPval):
                        firstCells.loc[indRow, 'highestSyncCorrected'] = amUniqFreq[allFreqSyncPVal < correctedPval].max()
                        highestSyncCorrected = amUniqFreq[allFreqSyncPVal < correctedPval].max()
                        freqsBelowThresh = allFreqSyncPVal < correctedPval
                        freqsBelowThresh = freqsBelowThresh.astype(int)
                        if len(significantFreqsArray) == 0:
                            significantFreqsArray = freqsBelowThresh
                        else:
                            # significantFreqsArray = np.concatenate([[significantFreqsArray], [freqsBelowThresh]])
                            significantFreqsArray = np.vstack((significantFreqsArray, freqsBelowThresh))
                    else:
                        firstCells.loc[indRow, 'highestSyncCorrected'] = 0

    firstCells['cfOnsetivityIndex'] = \
        (firstCells['onsetRate'] - firstCells['sustainedRate']) / \
        (firstCells['sustainedRate'] + firstCells['onsetRate'])
    return firstCells


def calculate_indices(db, filename=''):
    """
    Filter cells that has a good fitting then separate D1 cells(laser responsive)\
    and non-D1 cells(non laser-responsive)
    """
    pass
    # bestCells = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
    #
    # return bestCells


def calculate_cell_locations(db, filename=''):  # to be filled after complete collecting histology data
    pass


if __name__ == "__main__":
    # Cluster your data
    CLUSTER_DATA = 0  # We don't generally run this code. We kept this for documentation

    # Choosing which mice to do calculations for
    # Check for script arguements to decide what calculations are done
    dbLocation = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    if sys.argv[1:] != []:
        stat_calc = 0
        hist_calc = 0
        arguements = sys.argv[1:]
        if arguements[0] == 'all':
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            dbpath = os.path.join(dbLocation, '{}.h5'.format('direct_and_indirect_cells'))
        else:
            d1mice = [arguements[0]]
            dbpath = os.path.join(dbLocation, '{}.h5'.format(d1mice))
        print('d1mice = {}'.format(d1mice))
        # Run behavior can either be 'all', 'hist', or 'stats'
        runBehavior = arguements[1]
        print('run behavior is {}'.format(runBehavior))
        if runBehavior == 'all':
            stat_calc = 1
            hist_calc = 1
        elif runBehavior == 'hist':
            hist_calc = 1
        elif runBehavior == 'stats':
            stat_calc = 1
    else:
        # Calculates everything for all mice in studyparams
        stat_calc = 1
        hist_calc = 1
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        dbpath = os.path.join(dbLocation, '{}.h5'.format('direct_and_indirect_cells'))

    if CLUSTER_DATA:  # SPIKE SORTING
        inforecFile = os.path.join(settings.INFOREC_PATH, '{}_inforec.py'.format(d1mice))
        clusteringObj = spikesorting.ClusterInforec(inforecFile)
        clusteringObj.process_all_experiments()
        pass

    # Generate_cell_database_filters cells with the followings: isi < 0.05, spike quality > 2
    basicDB = celldatabase.generate_cell_database_from_subjects(d1mice)
    firstDB = basicDB
    d1DBFilename = os.path.join(settings.FIGURES_DATA_PATH, '{}_d1mice.h5'.format(studyparams.STUDY_NAME))
    # Create and save a database, computing first the base stats and then the indices
    if stat_calc:
        firstDB = append_base_stats(basicDB, filename=d1DBFilename)
        # bestCells = calculate_indices(firstDB, filename = d1DBFilename)
        histDB = firstDB
    if hist_calc:
        histDB = cellLoc.cell_locations(firstDB)

    if SAVE:
        # dbLocation = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
        # dbpath = os.path.join(dbLocation, '{}.h5'.format('direct_and_indirect_cells'))
        # dbpath = os.path.join(dbLocation, '{}.h5'.format('AM_additions'))

        if os.path.isdir(dbLocation):
            #celldatabase.save_hdf(histDB, dbpath)
            celldatabase.save_hdf(firstDB, dbpath)
            print("SAVED DATAFRAME to {}".format(dbpath))
        elif not os.path.isdir(dbLocation):
            answer = input_func("Save folder is not present. Would you like to make the desired directory now? (y/n) ")
            if answer.upper() in ['Y', 'YES']:
                os.mkdir(dbLocation)
                #celldatabase.save_hdf(PhotoID, dbpath)
                celldatabase.save_hdf(firstDB, dbpath)
                print("SAVED DATAFRAME to {}".format(dbpath))
                print(u"\U0001F4A9"*10)
