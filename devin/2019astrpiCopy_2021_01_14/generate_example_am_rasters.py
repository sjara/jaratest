"""
Using hand-picked cells, this script will find the cells' ephys data and save
what is needed to plot a raster plot in the figure_am.py file
"""
import os
import numpy as np
import pandas as pd
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import studyparams

STRIATUM_ONLY = True
FIGNAME = 'figure_am'
outputDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)

# Example cells we want to show am rasters for
examples = {}
examples.update({'Direct1': 'd1pi042_2019-09-11_3200.0_TT3c4'})
examples.update({'nDirect1': 'd1pi042_2019-09-11_3100.0_TT3c4'})

exampleList = [val for key, val in examples.items()]
exampleKeys = [key for key, val in examples.items()]
exampleSpikeData = {}

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = studyparams.DATABASE_NAME + '_original.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)

exampleSpikeTimes = {}
exampleTrialIndexForEachSpike = {}
exampleIndexLimitsEachTrial = {}
exampleFreqEachTrial = {}

for exampleInd, cellName in enumerate(exampleList):

    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('am')
    except (IndexError, ValueError):
        failed = True
        print("No am for cell {}".format(indRow))
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)

    freqEachTrial = bdata['currentFreq']
    alignmentRange = [-0.2, 0.7]  # Time chosen to include spikes visually for pre- and post-response period

    # Finding spike times that are relative to the event onset for the raster plot
    (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                      eventOnsetTimes,
                                                                      alignmentRange)
    # Saving all the data into a dictionary which will become the npz file
    exampleFreqEachTrial.update({exampleKeys[exampleInd]: freqEachTrial})
    exampleSpikeTimes.update({exampleKeys[exampleInd]: spikeTimesFromEventOnset})
    exampleTrialIndexForEachSpike.update({exampleKeys[exampleInd]: trialIndexForEachSpike})
    exampleIndexLimitsEachTrial.update({exampleKeys[exampleInd]: indexLimitsEachTrial})

# Filtering DB for AM cells
db = db.query(studyparams.FIRST_FLTRD_CELLS)
zDB = db.query(studyparams.LABELLED_Z)
zDB2 = db[db['z_coord'].isnull()]
zDBt = pd.concat([zDB, zDB2], axis=0, ignore_index=True, sort=False)
if STRIATUM_ONLY:
    db = zDBt.query(studyparams.BRAIN_REGION_QUERY_STRIATUM_ONLY)
elif not STRIATUM_ONLY:
    db = zDBt

D1 = db.query(studyparams.D1_CELLS)
nD1 = db.query(studyparams.nD1_CELLS)
D1 = D1.query(studyparams.AM_FILTER)
nD1 = nD1.query(studyparams.AM_FILTER)

# Check if example cells are in plotting database
for exampleInd, cellName in enumerate(exampleList):

    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    try:
        indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
    except AssertionError:
        print("Cell {} not in db".format(cellName))

plotting_data = {}

popStatCol = 'highestSyncCorrected'
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1PopStat[nD1PopStat > 0]
D1PopStat = D1PopStat[D1PopStat > 0]
nD1PopStat = np.log(nD1PopStat)
D1PopStat = np.log(D1PopStat)
plotting_data.update({"D1_highestSyncCorrected": D1PopStat, "nD1_highestSyncCorrected": nD1PopStat})

popStatCol = 'highestSyncCorrected'
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
nD1PopStat = nD1PopStat[pd.notnull(nD1PopStat)]
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
D1PopStat = D1PopStat[pd.notnull(D1PopStat)]
nD1SyncN = len(nD1PopStat[nD1PopStat > 0])
nD1NonSyncN = len(nD1PopStat[nD1PopStat == 0])
nD1SyncFrac = nD1SyncN / float(nD1SyncN + nD1NonSyncN)
nD1NonSyncFrac = nD1NonSyncN / float(nD1SyncN + nD1NonSyncN)
D1SyncN = len(D1PopStat[D1PopStat > 0])
D1NonSyncN = len(D1PopStat[D1PopStat == 0])
D1SyncFrac = D1SyncN / float(D1SyncN + D1NonSyncN)
D1NonSyncFrac = D1NonSyncN / float(D1SyncN + D1NonSyncN)
plotting_data.update({"D1_pieSync": D1SyncFrac, "nD1_pieSync": nD1SyncFrac,
                      "D1_pieNonSync": D1NonSyncFrac, "nD1_pieNonSync": nD1NonSyncFrac})
plotting_data.update({"D1_pieSyncN": D1SyncN, "nD1_pieSyncN": nD1SyncN,
                      "D1_pieNonSyncN": D1NonSyncN, "nD1_pieNonSyncN": nD1NonSyncN})

popStatCol = 'rateDiscrimAccuracy'
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
plotting_data.update({"D1_rateDiscrimAccuracy": D1PopStat, "nD1_rateDiscrimAccuracy": nD1PopStat})

possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
ratesToUse = possibleRateKeys
keys = ['phaseDiscrimAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

nD1Data = np.full((len(nD1), len(ratesToUse)), np.nan)
D1Data = np.full((len(D1), len(ratesToUse)), np.nan)

for externalInd, (indRow, row) in enumerate(nD1.iterrows()):
    for indKey, key in enumerate(keys):
        nD1Data[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(D1.iterrows()):
    for indKey, key in enumerate(keys):
        D1Data[externalInd, indKey] = row[key]

nD1MeanPerCell = np.nanmean(nD1Data, axis=1)
nD1MeanPerCell = nD1MeanPerCell[~np.isnan(nD1MeanPerCell)]
D1MeanPerCell = np.nanmean(D1Data, axis=1)
D1MeanPerCell = D1MeanPerCell[~np.isnan(D1MeanPerCell)]
plotting_data.update({"D1_phaseDiscrimAccuracy": D1MeanPerCell,
                      "nD1_phaseDiscrimAccuracy": nD1MeanPerCell})


ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

nD1PopStat = np.log(nD1PopStat)
D1PopStat = np.log(D1PopStat)

# Set path/filename for data output
exampleDataPath = os.path.join(outputDataDir, 'data_am_examples.npz')

# Saving the dictionary as an npz
np.savez(exampleDataPath,
         exampleIDs=exampleList,
         exampleNames=exampleKeys,
         exampleFreqEachTrial=exampleFreqEachTrial,
         exampleSpikeTimes=exampleSpikeTimes,
         exampleTrialIndexForEachSpike=exampleTrialIndexForEachSpike,
         exampleIndexLimitsEachTrial=exampleIndexLimitsEachTrial,
         **plotting_data)

print('Saved data to {}'.format(exampleDataPath))
