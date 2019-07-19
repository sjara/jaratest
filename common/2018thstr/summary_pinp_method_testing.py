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
db = celldatabase.load_hdf(dbPath)

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_NBQX.h5')
# database = celldatabase.load_hdf(dbPath)

### Init new database columns ###
# database['summaryPulsePval'] = 1 # Whether or not the cell responds to the laser pulse
# database['summaryTrainResponses'] = np.nan # How many of the pulses in the train the cell responds to.
# database['summaryTrainLatency'] = np.nan
# database['summaryPulseLatency'] = np.nan

lasercells = db.query('modifiedISI<0.02 or isiViolations<0.02')
goodcells = lasercells.query('spikeShapeQuality>2 and autoTagged==1 and pulsePval<0.05')

PLOT = True

database = goodcells

for indRow, dbRow in database.iterrows():

    cell = ephyscore.Cell(dbRow, useModifiedClusters=False)

    try:
        trainData, _ = cell.load('lasertrain')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        # dataframe.loc[indRow, 'autoTagged'] = 0
        continue

    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
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
    pVals = np.ones(len(pulseTimes))
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

    if PLOT:
        plt.clf()
        plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=4)
        plt.title('Cell {}, Num sig = {}'.format(indRow, numSignificant))
        for pulse in pulseTimes:
            plt.axvline(x=pulse, color='r')
            plt.axvline(x=pulse+binTime, color='r')
        plt.waitforbuttonpress()

    database.loc[indRow, 'numSignificantTrainResponses'] = numSignificant

    excited = respSpikeMean > nspkBase.ravel().mean()
    numTrainResponses = sum(pVals<0.05)
    excitedTrainResponse = (pVals<0.05) & excited
    numExcitedTrainResponse = sum(excitedTrainResponse)
    database.loc[indRow, 'summaryTrainResponses'] = numTrainResponses

print goodcells['summaryTrainResponses']
