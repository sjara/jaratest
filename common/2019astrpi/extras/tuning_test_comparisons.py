"""
1.) Load in existing database
2.) calculate the firing rate differences for tuningTest paradigm
3.) Add signficance to values and ID if there are a greater % of D1 cells tuned rather than non-D1
"""
import os
import numpy as np
import studyparams
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import database_generation_funcs as funcs

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '{}.h5'.format(studyparams.DATABASE_NAME)
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)

# FIXME: Consider what it would be better to fill empty values with instead of NaNs
db['tuningTestPVal'] = np.nan
db['tuningTestZStat'] = np.nan
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):

    sessions = dbRow['sessionType']
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

    session = 'tuningTest'
    try:
        ttEphysData, ttBehavData = oneCell.load(session)
    except IndexError:
        print('This cell does not contain a {} session'.format(session))
    except ValueError:
        print('This cell has no spikes for {} session'.format(session))
    else:
        baseRange = [-0.1, 0]

        # Extracting information from ephys and behavior data to do calculations later with
        currentFreq = ttBehavData['currentFreq']
        currentIntensity = ttBehavData['currentIntensity']
        uniqFreq = np.unique(currentFreq)
        uniqueIntensity = np.unique(currentIntensity)
        tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq, currentIntensity, uniqueIntensity)

        allIntenBase = np.array([])
        respSpikeMean = np.empty((len(uniqueIntensity), len(uniqFreq)))  # same as allIntenResp
        allIntenRespMedian = np.empty((len(uniqueIntensity), len(uniqFreq)))
        Rsquareds = np.empty((len(uniqueIntensity), len(uniqFreq)))
        ttSpikeTimes = ttEphysData['spikeTimes']
        ttEventOnsetTimes = ttEphysData['events']['soundDetectorOn']
        ttEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(ttEventOnsetTimes, minEventOnsetDiff=0.2)

        # Checking to see if the ephys data has one more trial than the behavior data and removing the last session if it does
        if len(ttEventOnsetTimes) == (len(currentFreq) + 1):
            ttEventOnsetTimes = ttEventOnsetTimes[0:-1]
            print("Correcting ephys data to be same length as behavior data")
            toCalculate = True
        elif len(ttEventOnsetTimes) == len(currentFreq):
            print("Data is already the same length")
            toCalculate = True
        else:
            print("Something is wrong with the length of these data")
            toCalculate = False

        # -------------------- Start of calculations for the tuningCurve data -------------------------
        # The latency of the cell from the onset of the stim
        if toCalculate:
            ttZStat, ttPVal = \
                funcs.sound_response_any_stimulus(ttEventOnsetTimes, ttSpikeTimes, tuningTrialsEachCond[:, :, -1],
                                                  timeRange=[0.0, 0.05], baseRange=baseRange)
            db.at[indRow, 'tuningTestPVal'] = ttPVal
            db.at[indRow, 'tuningTestZStat'] = ttZStat

celldatabase.save_hdf(db, '/var/tmp/figuresdata/2019astrpi/ttDB.h5')
