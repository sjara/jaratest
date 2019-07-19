import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp
from jaratoolbox import settings
from scipy import stats
from scipy import signal

STUDY_NAME = '2018thstr'
SAVE=0

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU_newtagged.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_calculated_columns.h5')
# database = pd.read_hdf(dbPath, key='dataframe')
database = celldatabase.load_hdf(dbPath)

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
# database = celldatabase.load_hdf(dbPath)

### Init new database columns ###
database['summaryPulsePval'] = 1 # Whether or not the cell responds to the laser pulse
database['summaryTrainResponses'] = np.nan # How many of the pulses in the train the cell responds to.
database['summaryTrainLatency'] = np.nan
database['summaryPulseLatency'] = np.nan

#DEBUG
import ipdb

#Neurons with 4 laser pulse responses that are not tagged
# database = database.loc[[136, 1034]]

# Neurons with 5 laser pulse responses, tagged, that have longer pulse latencies
# database = database.loc[[969, 1070, 1092]]

# Tagged neurons with negative pulse latency
# database = database.loc[[370, 374, 425]]


for indIter, (indRow, dbRow) in enumerate(database.iterrows()):

    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

    try:
        pulseData, _ = cell.load('laserpulse')
    except (IndexError, ValueError):
        print "Cell has no laserpulse session, loading laser train session for pulse data"
        try:
            pulseData, _ = cell.load('lasertrain') ##FIXME!!! Loading train if we have no pulse. Bad idea??
        except (IndexError, ValueError):
            print "Cell has no laser train session or no spikes. FAIL!"
            database.loc[indRow, 'autoTagged'] = 0
            continue
    try:
        trainData, _ = cell.load('lasertrain')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        database.loc[indRow, 'autoTagged'] = 0
        continue

    #Laser pulse analysis
    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    # baseRange = [-0.2,-0.1]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseRange = [0, 0+binTime]
    alignmentRange = [baseRange[0], responseRange[1]]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,responseRange)

    try:
        zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)
    except ValueError: #All numbers identical will cause mann whitney to fail
        zStat, pVal = [0, 1]

    # ipdb.set_trace()

    database.loc[indRow, 'summaryPulsePval'] = pVal

    # if pVal<0.05 and zStat>0: #This does not work because MW still gives positive Z if response goes down
    if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
        passPulse = True
    else:
        passPulse = False

    ## LATENCY CALCULATION ##
    # timeRangeForLatency = [-0.1,0.1]
    timeRangeForLatency = [-0.05,0.1]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   timeRangeForLatency)
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        print "FAILURE IN LATENCY CODE, PULSE"
        continue
    database.loc[indRow, 'summaryPulseLatency'] = respLatency


    #Lasertrain analysis
    #There should be a significant response to all of the pulses
    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    # baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    # baseRange = [-0.05, -0.03]
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)

    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)

    zStats = np.empty(len(pulseTimes))
    pVals = np.empty(len(pulseTimes))
    respSpikeMean = np.empty(len(pulseTimes))
    for indPulse, pulse in enumerate(pulseTimes):
        responseRange = [pulse, pulse+binTime]
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,responseRange)
        respSpikeMean[indPulse] = nspkResp.ravel().mean()
        try:
            zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
        except ValueError: #All numbers identical will cause mann whitney to fail
            zStats[indPulse], pVals[indPulse] = [0, 1]

    numSignificant = sum( pVals<0.05 )
    database.loc[indRow, 'numSignificantTrainResponses'] = numSignificant

    #Save the number of significant train responses
    excited = respSpikeMean > nspkBase.ravel().mean()
    numTrainResponses = sum(pVals<0.05)
    excitedTrainResponse = (pVals<0.05) & excited
    numExcitedTrainResponse = sum(excitedTrainResponse)
    database.loc[indRow, 'summaryTrainResponses'] = numTrainResponses
    # database.loc[indRow, 'summaryTrainResponses'] = numExcitedTrainResponse

    ## Latency for laser train
    # if pVal<0.05:
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        print "FAILURE WITH LATENCY CALCULATION!!!"
        continue
    database.loc[indRow, 'summaryTrainLatency'] = respLatency

    # if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and all(zStats>0):
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        passTrain = True
    else:
        passTrain = False

    # ipdb.set_trace()
if passPulse and passTrain:
        print "PASS"
        database.loc[indRow, 'autoTagged'] = 1
    else:
        print "FAIL"
        database.loc[indRow, 'autoTagged'] = 0



# for indRow, dbRow in database.iterrows():

#     #Load the cell
#     cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

#     ############### LASER TRAIN NUM RESPONSES ###################

#     # CONDITION 2: Responds to the laser train (how many pulses have significant response?)
#     #Load the data for the laser pulse session.
#     try:
#         trainData, _ = cell.load('lasertrain')
#     except (IndexError, ValueError):
#         print "Cell has no laser train session or no spikes. FAIL!"
#         continue

#     spikeTimes = trainData['spikeTimes']
#     trainPulseOnsetTimes = trainData['events']['stimOn']
#     eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
#     # baseRange = [-0.1,-0.09]              # Baseline range (in seconds)
#     baseRange = [-0.050,-0.040]              # Baseline range (in seconds)
#     pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
#     binTime = baseRange[1]-baseRange[0]         # Time-bin size
#     # alignmentRange = [-0.5, 1]
#     alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]

#     (spikeTimesFromEventOnset,
#      trialIndexForEachSpike,
#      indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
#                                                                    eventOnsetTimes,
#                                                                    alignmentRange)

#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,baseRange)

#     zStats = np.empty(len(pulseTimes))
#     pVals = np.empty(len(pulseTimes))
#     excited = np.empty(len(pulseTimes))
#     respSpikeMean = np.empty(len(pulseTimes))
#     for indPulse, pulse in enumerate(pulseTimes):
#         responseRange = [pulse, pulse+binTime]
#         nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                             indexLimitsEachTrial,responseRange)
#         respSpikeMean[indPulse] = nspkResp.ravel().mean()
#         try:
#             zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
#         except ValueError: #All numbers identical will cause mann whitney to fail
#             zStats[indPulse], pVals[indPulse] = [0, 1]
#             # zStats[indPulse], pVals[indPulse] = [0, 1]
#             # zStats[indPulse], pVals[indPulse] = [0, 0]
#     numSignificant = sum( pVals<0.05 )
#     database.loc[indRow, 'numSignificantTrainResponses'] = numSignificant

#     excited = respSpikeMean > nspkBase.ravel().mean()

#     #Save the number of significant train responses
#     numTrainResponses = sum(pVals<0.05)
#     excitedTrainResponse = (pVals<0.05) & excited
#     numExcitedTrainResponse = sum(excitedTrainResponse)
#     database.loc[indRow, 'summaryTrainResponses'] = numTrainResponses
#     # database.loc[indRow, 'summaryTrainResponses'] = numExcitedTrainResponse

#     ## Latency for laser train
#     # if pVal<0.05:
#     timeRangeForLatency = [-0.1,0.1]
#     try:
#         (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
#                                                                 indexLimitsEachTrial,
#                                                                 timeRangeForLatency, threshold=0.5,
#                                                                 win=signal.hanning(11))
#     except:
#         print "FAILURE WITH LATENCY CALCULATION!!!"
#         continue
#     database.loc[indRow, 'summaryTrainLatency'] = respLatency



#     ############ LASER PULSE LATENCY CALCULATION ################


#     #CONDITION 1: Is there any response to the laser pulse??
#     #Load the data for the laser pulse session.
#     try:
#         pulseData, _ = cell.load('laserpulse')
#     except (IndexError, ValueError):
#         print "Cell has no laser train session or no spikes. FAIL!"
#         continue

#     spikeTimes = pulseData['spikeTimes']
#     eventOnsetTimes = pulseData['events']['stimOn']
#     baseRange = [-0.2,-0.1]              # Baseline range (in seconds)
#     binTime = baseRange[1]-baseRange[0]         # Time-bin size
#     responseRange = [0, 0+binTime]
#     alignmentRange = [-0.5, 1]
#     (spikeTimesFromEventOnset,
#      trialIndexForEachSpike,
#      indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
#                                                                    eventOnsetTimes,
#                                                                    alignmentRange)
#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,baseRange)
#     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,responseRange)
#     try:
#         zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)
#     except ValueError: #All numbers identical will cause mann whitney to fail
#         zStat, pVal = [0, 1]

#     database.loc[indRow, 'summaryPulsePval'] = pVal

#     timeRangeForLatency = [-0.1,0.1]
#     try:
#         (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
#                                                                 indexLimitsEachTrial,
#                                                                 timeRangeForLatency, threshold=0.5,
#                                                                 win=signal.hanning(11))
#     except:
#         print "FAILURE IN LATENCY CODE, PULSE"
#         continue
#     database.loc[indRow, 'summaryPulseLatency'] = respLatency


    #############################################################







##########  NBQX CELLS #############

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
databaseNBQX = celldatabase.load_hdf(dbPath)

### Init new database columns ###
databaseNBQX['summaryPulsePval'] = 1 # Whether or not the cell responds to the laser pulse
databaseNBQX['summaryTrainResponses'] = 0 # How many of the pulses in the train the cell responds to.
databaseNBQX['summaryTrainLatency'] = np.nan
databaseNBQX['summaryPulseLatency'] = np.nan
databaseNBQX['summarySurvivedNBQX'] = 0
databaseNBQX['washoutResponse'] = 0

### NBQX cell save dir ###
saveDir = '/home/nick/data/reports/nick/20180710_survivalReports'

# NBQX neuron with 5 laser responses that isn't tagged
databaseNBQX = databaseNBQX.loc[54]

for indRow, dbRow in databaseNBQX.iterrows():
    #Load the cell
    cell = ephyscore.Cell(dbRow)

    #CONDITION 1: Is there any response to the laser pulse??
    #Load the data for the laser pulse session.
    try:
        pulseData, _ = cell.load('laserpulse_pre') ##FIXME!!! Loading train if we have no pulse. Bad idea??
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        continue

    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    baseRange = [-0.2,-0.1]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseRange = [0, 0+binTime]
    alignmentRange = [-0.5, 1]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,responseRange)
    try:
        zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)
    except ValueError: #All numbers identical will cause mann whitney to fail
        zStat, pVal = [0, 1]
    databaseNBQX.loc[indRow, 'summaryPulsePval'] = pVal


    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        continue
    databaseNBQX.loc[indRow, 'summaryPulseLatency'] = respLatency

    ipdb.set_trace()


    # CONDITION 2: Responds to the laser train (how many pulses have significant response?)
    #Load the data for the laser pulse session.
    try:
        trainData, _ = cell.load('lasertrain_pre') ##FIXME!!! Loading train if we have no pulse. Bad idea??
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        continue

    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    # baseRange = [-0.1,-0.09]              # Baseline range (in seconds)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    # alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]
    alignmentRange = [-0.5, 1.0]


    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)

    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)

    zStats = np.empty(len(pulseTimes))
    pVals = np.empty(len(pulseTimes))
    excited = np.empty(len(pulseTimes))
    respSpikeMean = np.empty(len(pulseTimes))
    for indPulse, pulse in enumerate(pulseTimes):
        responseRange = [pulse, pulse+binTime]
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                           indexLimitsEachTrial,responseRange)
        respSpikeMean[indPulse] = nspkResp.ravel().mean()
        try:
            zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
        except ValueError: #All numbers identical will cause mann whitney to fail
            zStats[indPulse], pVals[indPulse] = [0, 1]
    excited = respSpikeMean > nspkBase.ravel().mean()


    ## Latency for laser train
    # if pVal<0.05:
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        continue
    databaseNBQX.loc[indRow, 'summaryTrainLatency'] = respLatency

    #Save the number of significant train responses
    numTrainResponses = sum(pVals<0.05)
    excitedTrainResponse = (pVals<0.05) & excited
    numExcitedTrainResponse = sum(excitedTrainResponse)
    # databaseNBQX.loc[indRow, 'summaryTrainResponses'] = numExcitedTrainResponse
    databaseNBQX.loc[indRow, 'summaryTrainResponses'] = numTrainResponses

    ipdb.set_trace()

    # DOES THE CELL SURVIVE THE NBQX??

    # Using laser train condition to eval NBQX effect - can still respond to each pulse after??
    # try:
    #     trainData, _ = cell.load('laserpulse_post')
    # except (IndexError, ValueError):
    #     continue

    # spikeTimes = trainData['spikeTimes']
    # trainPulseOnsetTimes = trainData['events']['stimOn']
    # eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    # baseRange = [-0.5,-0.4]              # Baseline range (in seconds)
    # alignmentRange = [-0.5, 1.0]
    # responseRange = [0, 0.1]

    # (spikeTimesFromEventOnset,
    #  trialIndexForEachSpike,
    #  indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
    #                                                                eventOnsetTimes,
    #                                                                alignmentRange)

    # nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
    #                                                     indexLimitsEachTrial,baseRange)

    # zStats = np.empty(len(pulseTimes))
    # pVals = np.empty(len(pulseTimes))
    # respSpikeMean = np.empty(len(pulseTimes))
    # for indPulse, pulse in enumerate(pulseTimes):
    #     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
    #                                                        indexLimitsEachTrial,responseRange)
    #     respSpikeMean[indPulse] = nspkResp.ravel().mean()
    #     try:
    #         zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
    #     except ValueError: #All numbers identical will cause mann whitney to fail
    #         zStats[indPulse], pVals[indPulse] = [0, 1]


    #Save the number of significant train responses
        # databaseNBQX.loc[indRow, 'summarySurvivedNBQX'] = 1


    # Using laser train condition to eval NBQX effect - can still respond to each pulse after??
    try:
        trainData, _ = cell.load('lasertrain_post')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        continue

    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.1,-0.09]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)


    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)

    zStats = np.empty(len(pulseTimes))
    pVals = np.empty(len(pulseTimes))
    respSpikeMean = np.empty(len(pulseTimes))
    for indPulse, pulse in enumerate(pulseTimes):
        responseRange = [pulse, pulse+binTime]
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                           indexLimitsEachTrial,responseRange)
        respSpikeMean[indPulse] = nspkResp.ravel().mean()
        try:
            zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
        except ValueError: #All numbers identical will cause mann whitney to fail
            zStats[indPulse], pVals[indPulse] = [0, 1]


    #Save the number of significant train responses
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        databaseNBQX.loc[indRow, 'summarySurvivedNBQX'] = 1

    # #PLOT THE NBQX REPORTS
    # nbqxCells = databaseNBQX.query('isiViolations<0.02 and spikeShapeQuality>2 and summaryPulsePval<0.05')
    # for indRow, dbRow in nbqxCells.iterrows():
    #     plot_NBQX_report(dbRow, saveDir)

if SAVE:
    celldatabase.save_hdf(database, '/tmp/database_with_pulse_responses.h5')
    celldatabase.save_hdf(databaseNBQX, '/tmp/nbqx_database_with_pulse_responses.h5')



