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
# AC
examples = {}
# Format: {name}_{date}_{}
# examples.update({'AC1' : 'pinp017_2017-03-22_1143_4_5'})
# examples.update({'AC2' : 'pinp017_2017-03-23_1281_7_2'})

examples.update({'Direct1': 'd1pi036_2019-05-29_2800.0_TT2c4'})
examples.update({'Direct2': 'd1pi036_2019-05-29_2800.0_TT6c2'})

# Thalamus
# examples.update({'Thal1' : 'pinp015_2017-02-15_3110_7_3'})
# examples.update({'Thal2' : 'pinp026_2017-11-16_3046_4_3'})

examples.update({'nDirect1': 'd1pi036_2019-05-29_2900.0_TT5c5'})
examples.update({'nDirect2': 'd1pi041_2019-08-25_3000.0_TT7c3'})
# examples.update({'Thal2' : 'pinp026_2017-11-15_3252.0_TT2c2'})
# examples.update({'Thal3' : 'pinp026_2017-11-16_3046.0_TT4c3'})


# Striatum
# examples.update({'Str1' : 'pinp029_2017-11-08_2052_2_3'})
# examples.update({'Str1' : 'pinp020_2017-05-09_2702_8_2'})
# examples.update({'Str2' : 'pinp020_2017-05-09_2802_7_2'})
# examples.update({'Str3' : 'pinp029_2017-11-08_2052_2_3'})

exampleList = [val for key, val in examples.items()]
exampleKeys = [key for key, val in examples.items()]
exampleSpikeData = {}

# THE METHOD
# Calculate response range spikes for each combo
# Calculate baseline rate
# Calculate intensity threshold for cell by using response threshold
# Fit gaussian to spike data 10db above intensity threshold
# Determine upper and lower bounds of tc

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = studyparams.DATABASE_NAME + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, '{}.h5'.format("20200602DB"))
# os.path.join(studyparams.PATH_TO_TEST,nameDB)
db = celldatabase.load_hdf(pathtoDB)

#Only process the examples
# dataframe = db.query('cellLabel in @exampleList')

#Make labels for all the cells
# db['cellLabel'] = db.apply(lambda row:'{}_{}_{}_{}_{}'.format(row['subject'], row['date'], int(row['depth']), int(row['tetrode']), int(row['cluster'])), axis=1)

# examplesDB = db.query('cellLabel in @exampleList')

# dataframe = examplesDB

exampleSpikeTimes = {}
exampleTrialIndexForEachSpike = {}
exampleIndexLimitsEachTrial = {}
exampleFreqEachTrial = {}

# for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
for exampleInd, cellName in enumerate(exampleList):

    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('am')
    except (IndexError, ValueError):  # The cell does not have a tc or the tc session has no spikes
        failed = True
        print("No am for cell {}".format(indRow))
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)

    freqEachTrial = bdata['currentFreq']
    alignmentRange = [-0.2, 0.7]
    (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                      eventOnsetTimes,
                                                                      alignmentRange)
    exampleFreqEachTrial.update({exampleKeys[exampleInd]: freqEachTrial})
    exampleSpikeTimes.update({exampleKeys[exampleInd]: spikeTimesFromEventOnset})
    exampleTrialIndexForEachSpike.update({exampleKeys[exampleInd]: trialIndexForEachSpike})
    exampleIndexLimitsEachTrial.update({exampleKeys[exampleInd]: indexLimitsEachTrial})

exampleDataPath = os.path.join(outputDataDir, 'data_am_examples.npz')
np.savez(exampleDataPath,
         exampleIDs=exampleList,
         exampleNames=exampleKeys,
         exampleFreqEachTrial=exampleFreqEachTrial,
         exampleSpikeTimes=exampleSpikeTimes,
         exampleTrialIndexForEachSpike=exampleTrialIndexForEachSpike,
         exampleIndexLimitsEachTrial=exampleIndexLimitsEachTrial)

print('Saved data to {}'.format(exampleDataPath))
