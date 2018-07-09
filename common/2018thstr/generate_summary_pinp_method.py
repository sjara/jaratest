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

# inforecPath = '/home/nick/src/jaratest/common/inforecordings/pinp031_inforec.py'
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
# database = celldatabase.load_hdf(dbPath)

# failExamples = [
#     {'subject':'pinp031',
#      'date':'2018-06-26',
#      'depth':1901,
#      'tetrode':1,
#      'cluster':4
#     },

#     {'subject':'pinp031',
#      'date':'2018-06-26',
#      'depth':1901,
#      'tetrode':2,
#      'cluster':4
#     },

#     {'subject':'pinp031',
#      'date':'2018-06-26',
#      'depth':1901,
#      'tetrode':6,
#      'cluster':6
#     }
# ]

# thisExample = failExamples[2]
# indRow, dbRow = celldatabase.find_cell(database, **thisExample)
# cell = ephyscore.Cell(dbRow)

# ####################################################
# for indIter, (indRow, dbRow) in enumerate(database.iterrows()):

#     cell = ephyscore.Cell(dbRow)

#     try:
#         pulseData, _ = cell.load('laserpulse_pre')
#     except (IndexError, ValueError):
#         print "Cell has no laserpulse session, loading laser train session for pulse data"
#         try:
#             pulseData, _ = cell.load('lasertrain_pre') ##FIXME!!! Loading train if we have no pulse. Bad idea??
#         except (IndexError, ValueError):
#             print "Cell has no laser train session or no spikes. FAIL!"
#             database.loc[indRow, 'autoTagged'] = 0
#             continue
#     try:
#         trainData, _ = cell.load('lasertrain_pre')
#     except (IndexError, ValueError):
#         print "Cell has no laser train session or no spikes. FAIL!"
#         database.loc[indRow, 'autoTagged'] = 0
#         continue

#     #Laser pulse analysis
#     spikeTimes = pulseData['spikeTimes']
#     eventOnsetTimes = pulseData['events']['stimOn']
#     baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
#     binTime = baseRange[1]-baseRange[0]         # Time-bin size
#     responseRange = [0, 0+binTime]
#     alignmentRange = [baseRange[0], responseRange[1]]
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

#     # if pVal<0.05 and zStat>0: #This does not work because MW still gives positive Z if response goes down
#     if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
#         passPulse = True
#     else:
#         passPulse = False


#     #Lasertrain analysis
#     #There should be a significant response to all of the pulses
#     spikeTimes = trainData['spikeTimes']
#     trainPulseOnsetTimes = trainData['events']['stimOn']
#     eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
#     baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
#     pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
#     baseRange = [-0.05, -0.03]
#     binTime = baseRange[1]-baseRange[0]         # Time-bin size
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
#     respSpikeMean = np.empty(len(pulseTimes))
#     for indPulse, pulse in enumerate(pulseTimes):
#         responseRange = [pulse, pulse+binTime]
#         nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                            indexLimitsEachTrial,responseRange)
#         respSpikeMean[indPulse] = nspkResp.ravel().mean()
#         try:
#             zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
#         except ValueError: #All numbers identical will cause mann whitney to fail
#             zStats[indPulse], pVals[indPulse] = [0, 1]

#     # if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and all(zStats>0):
#     if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
#         passTrain = True
#     else:
#         passTrain = False

#     if passPulse and passTrain:
#         print "PASS"
#         database.loc[indRow, 'autoTagged'] = 1
#     else:
#         print "FAIL"
#         database.loc[indRow, 'autoTagged'] = 0

##################################################


# sessiontype = 'lasertrain_pre'

# ephysData, bdata = cell.load(sessiontype)
# eventOnsetTimes = ephysData['events']['stimOn']
# timeRange = [-0.05, 0.1]

# (spikeTimesFromEventOnset,
# trialIndexForEachSpike,
# indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
#                                                                 eventOnsetTimes,
#                                                                 timeRange)
# plt.clf()

# axRaster = plt.subplot(111)

# axRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
# axRaster.axvline(x=0.01)

# plt.show()

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
database = pd.read_hdf(dbPath, key='dataframe')

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
# database = celldatabase.load_hdf(dbPath)

for indRow, dbRow in database.iterrows():

    cell = ephyscore.Cell(dbRow)
    try:
        pulseData, _ = cell.load('lasertrain') ##FIXME!!! Loading train if we have no pulse. Bad idea??
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        database.loc[indRow, 'trainPval'] = 1
        continue

    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
    baseRange = [-0.05,-0.04]              # Baseline range (in seconds)
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

    database.loc[indRow, 'trainPval'] = pVal
    database.loc[indRow, 'trainZstat'] = zStat


    ## Latency for laser train
    # if pVal<0.05:
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        respLatency = np.nan

    database.loc[indRow, 'trainLatency'] = respLatency


    ## reliability?
    ## % of times that you get a spike after 2nd laser pulse (w/in 10 msec of pulse onset)
    pulseTwoRange = [0.80, 0.81]
    nspkPulseTwo = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,pulseTwoRange)
    reliability = sum(nspkPulseTwo>0)/float(len(nspkPulseTwo))
    database.loc[indRow, 'trainReliability'] = reliability

plt.clf()
fig = plt.gcf()
# ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(111)
ax.hold(1)
# lasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1')
nonlasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0 and pulsePval<0.05')
lasercells = database.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1 and pulsePval<0.05')

laserlatencies = lasercells['trainLatency'].values
nonlaserlatencies = nonlasercells['trainLatency'].values

laserreliability = lasercells['trainReliability'].values
nonlaserreliability = nonlasercells['trainReliability'].values

laserpulseZ = lasercells['pulseZscore'].values
nonlaserpulseZ = nonlasercells['pulseZscore'].values

laserNum = lasercells['numSignificantTrainResponses'].values
nonlaserNum = nonlasercells['numSignificantTrainResponses'].values

# plt.plot(nonlaserlatencies, nonlaserNum, nonlaserpulseZ, 'k.')
# plt.plot(nonlaserlatencies, nonlaserNum, nonlaserreliability, 'k.')
plt.plot(nonlaserlatencies, nonlaserNum, 'k.')
ax.set_xlabel('latency')
ax.set_xlim([0, 0.1])
ax.set_ylabel('num significant train responses')
# ax.set_zlabel('pulse Z score')
# plt.plot(laserlatencies, laserNum, laserpulseZ, 'b.')
# plt.plot(laserlatencies, laserNum, laserreliability, 'b.')
plt.plot(laserlatencies, laserNum, 'b.')
ax.axvline(x=0.01, color='r')
plt.show()



# Now for the NBQX data we need these metrics plus a way to know if it passes after the treatment or not.

inforecPath = '/home/nick/src/jaratest/common/inforecordings/pinp031_inforec.py'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
database = celldatabase.load_hdf(dbPath)


# ####################################################
for indIter, (indRow, dbRow) in enumerate(database.iterrows()):

    cell = ephyscore.Cell(dbRow)

    try:
        pulseData, _ = cell.load('laserpulse_post')
    except (IndexError, ValueError):
        print "Cell has no laserpulse session, loading laser train session for pulse data"
        try:
            pulseData, _ = cell.load('lasertrain_post') ##FIXME!!! Loading train if we have no pulse. Bad idea??
        except (IndexError, ValueError):
            print "Cell has no laser train session or no spikes. FAIL!"
            database.loc[indRow, 'postTagged'] = 0
            continue
    try:
        trainData, _ = cell.load('lasertrain_post')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        database.loc[indRow, 'postTagged'] = 0
        continue

    #Laser pulse analysis
    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
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

    # if pVal<0.05 and zStat>0: #This does not work because MW still gives positive Z if response goes down
    if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
        passPulse = True
    else:
        passPulse = False


    #Lasertrain analysis
    #There should be a significant response to all of the pulses
    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    baseRange = [-0.05, -0.03]
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


    ## Latency for laser train
    # if pVal<0.05:
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except:
        respLatency = np.nan

    database.loc[indRow, 'trainLatency'] = respLatency


    # if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and all(zStats>0):
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        passTrain = True
    else:
        passTrain = False

    if passPulse and passTrain:
        print "PASS"
        database.loc[indRow, 'postTagged'] = 1
    else:
        print "FAIL"
        database.loc[indRow, 'postTagged'] = 0

##################################################

