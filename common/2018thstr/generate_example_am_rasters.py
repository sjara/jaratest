import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import pandas as pd

FIGNAME = 'figure_am'
outputDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

#Example cells we want to show am rasters for
#AC
examples = {}
#Format: {name}_{date}_{}
examples.update({'AC1' : 'pinp017_2017-03-22_1143_4_5'})
examples.update({'AC2' : 'pinp017_2017-03-23_1281_7_2'})

#Thalamus
examples.update({'Thal1' : 'pinp015_2017-02-15_3110_7_3'})
examples.update({'Thal2' : 'pinp026_2017-11-16_3046_4_3'})

#Striatum
# examples.update({'Str1' : 'pinp029_2017-11-08_2052_2_3'})
examples.update({'Str1' : 'pinp020_2017-05-09_2702_8_2'})
examples.update({'Str2' : 'pinp020_2017-05-09_2802_7_2'})
examples.update({'Str3' : 'pinp029_2017-11-08_2052_2_3'})

exampleList = [val for key, val in examples.iteritems()]
exampleKeys = [key for key, val in examples.iteritems()]
exampleSpikeData = {}

#THE METHOD
# Calculate response range spikes for each combo
# Calculate baseline rate
# Calculate intensity threshold for cell by using response threshold
# Fit gaussian to spike data 10db above intensity threshold
# Determine upper and lower bounds of tc

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

#Only process the examples
# dataframe = db.query('cellLabel in @exampleList')

#Make labels for all the cells
db['cellLabel'] = db.apply(lambda row:'{}_{}_{}_{}_{}'.format(row['subject'], row['date'], int(row['depth']), int(row['tetrode']), int(row['cluster'])), axis=1)

examplesDB = db.query('cellLabel in @exampleList')

dataframe = examplesDB

exampleSpikeTimes = {}
exampleTrialIndexForEachSpike = {}
exampleIndexLimitsEachTrial = {}
exampleFreqEachTrial = {}

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    if dbRow['cellLabel'] in exampleList:
        cell = ephyscore.Cell(dbRow)
        try:
            ephysData, bdata = cell.load('am')
        except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
            failed=True
            print "No am for cell {}".format(indRow)

        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        freqEachTrial = bdata['currentFreq']
        alignmentRange = [-0.2, 0.7]

        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventOnsetTimes,
                                                                       alignmentRange)

        exampleInd = exampleList.index(dbRow['cellLabel'])
        exampleFreqEachTrial.update({exampleKeys[exampleInd]:freqEachTrial})
        exampleSpikeTimes.update({exampleKeys[exampleInd]:spikeTimesFromEventOnset})
        exampleTrialIndexForEachSpike.update({exampleKeys[exampleInd]:trialIndexForEachSpike})
        exampleIndexLimitsEachTrial.update({exampleKeys[exampleInd]:indexLimitsEachTrial})

exampleDataPath = os.path.join(outputDataDir, 'data_am_examples.npz')
np.savez(exampleDataPath,
         exampleIDs = exampleList,
         exampleNames = exampleKeys,
         exampleFreqEachTrial = exampleFreqEachTrial,
         exampleSpikeTimes = exampleSpikeTimes,
         exampleTrialIndexForEachSpike = exampleTrialIndexForEachSpike,
         exampleIndexLimitsEachTrial = exampleIndexLimitsEachTrial)

print 'Saved data to {}'.format(exampleDataPath)
