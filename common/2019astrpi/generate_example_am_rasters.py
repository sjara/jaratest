"""
Using hand-picked cells, this script will find the cells' ephys data and save
what is needed to plot a raster plot in the figure_am.py file
"""
import os
import numpy as np
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import studyparams

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
nameDB = studyparams.DATABASE_NAME + '.h5'
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

# Set path/filename for data output
exampleDataPath = os.path.join(outputDataDir, 'data_am_examples.npz')

# Saving the dictionary as an npz
np.savez(exampleDataPath,
         exampleIDs=exampleList,
         exampleNames=exampleKeys,
         exampleFreqEachTrial=exampleFreqEachTrial,
         exampleSpikeTimes=exampleSpikeTimes,
         exampleTrialIndexForEachSpike=exampleTrialIndexForEachSpike,
         exampleIndexLimitsEachTrial=exampleIndexLimitsEachTrial)

print('Saved data to {}'.format(exampleDataPath))
