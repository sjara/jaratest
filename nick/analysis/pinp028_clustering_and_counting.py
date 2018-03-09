import sys
import numpy as np
from scipy import stats
from jaratoolbox import spikesorting
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
reload(ephyscore)
reload(celldatabase)

inforec = '/home/nick/src/jaratest/common/inforecordings/pinp028_inforec.py'

# ci = spikesorting.ClusterInforec(inforec)
# ci.process_all_experiments(recluster=False)

db = celldatabase.generate_cell_database(inforec)

noiseZscore = np.empty(len(db))
noisePval = np.empty(len(db))
baseRange = [-0.2,0]
responseRange = [0, 0.2]
for indCell, dbRow in db.iterrows():

    cell = ephyscore.Cell(dbRow)

    if 'noiseburst' in cell.dbRow['sessionType']:
        sessiontype = 'noiseburst'
    elif 'rlf' in cell.dbRow['sessionType']:
        sessiontype = 'rlf'
    elif 'am' in cell.dbRow['sessionType']:
        sessiontype = 'am'

    ephysData, bdata = cell.load(sessiontype)

    spikeTimes = ephysData['spikeTimes']
    events = ephysData['events']

    if spikeTimes is not None:
        eventOnsetTimes = events['stimOn']
        alignmentRange = [baseRange[0], responseRange[1]]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventOnsetTimes,
                                                                       alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)
        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
    else:
        zScore=0
        pVal=0
    noiseZscore[indCell] = zScore
    noisePval[indCell] = pVal
db['noiseZscore'] = noiseZscore
db['noisePval'] = noisePval

result = db.query('spikeShapeQuality > 2 and noisePval < 0.05')
