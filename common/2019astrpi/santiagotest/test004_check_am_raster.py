"""
Check cells that show not synchronized response to AM, but have response to white noise.
"""

import os
import sys
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

sys.path.append('..')
import studyparams
import database_generation_funcs as funcs


'''
dbPath = '/data/figuresdata/2019astrpi/testdb041.h5'
subject = 'd1pi041'
date = '2019-08-25'
depth = 2700
tetrode = 4
cluster = 1
dbPath = '/data/figuresdata/2019astrpi/test{}.h5'.format(subject)
basicDB = celldatabase.load_hdf(dbPath)
'''
CASE = 0
if CASE==0:
    cellToUse = ('d1pi042','2019-09-11',3400,4,5)
elif CASE==1:
    pass

subject, date, depth, tetrode, cluster = cellToUse
dbPath = '/data/figuresdata/2019astrpi/test{}.h5'.format(subject)
basicDB = celldatabase.load_hdf(dbPath)
 
(indRow, dbRow) = celldatabase.find_cell(basicDB, subject, date, depth, tetrode, cluster)
oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

session = 'am'
amEphysData, amBehavData = oneCell.load(session)

amSpikeTimes = amEphysData['spikeTimes']
amEventOnsetTimesOrig = amEphysData['events']['soundDetectorOn']
amEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(amEventOnsetTimesOrig, 0.2)
amCurrentFreq = amBehavData['currentFreq']
amUniqFreq = np.unique(amCurrentFreq)
amTimeRange = [-0.2, 0.7]
amTrialsEachCond = behavioranalysis.find_trials_each_type(amCurrentFreq, amUniqFreq)

print('N events behav: {}', len(amCurrentFreq))
print('N events ephys: {}', len(amEventOnsetTimes))

bdata = amBehavData

behavStimOnEventsBool = bdata.events['nextState']==bdata.stateMatrix['statesNames']['output1On']
behavStimOnTime = bdata.events['eventTime'][behavStimOnEventsBool]

(amSpikeTimesFromEventOnset, amTrialIndexForEachSpike, amIndexLimitsEachTrial) = \
                           spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                                 amEventOnsetTimes,
                                                                 amTimeRange)

binEdges = np.arange(*amTimeRange, 0.005)
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(amSpikeTimesFromEventOnset,
                                                         amIndexLimitsEachTrial,binEdges)
sumSpikes = np.sum(spikeCountMat,axis=0)

plt.clf()
#ax0 = plt.subplot(2,1,1)
#plt.plot(amSpikeTimesFromEventOnset,amTrialIndexForEachSpike,'.')
extraplots.raster_plot(amSpikeTimesFromEventOnset, amIndexLimitsEachTrial,
                       amTimeRange, amTrialsEachCond)
plt.xlabel('Time (s)')
plt.ylabel('AM rate')
plt.title(str(oneCell))

#ax1 = plt.subplot(2,1,2, sharex=ax0)
#plt.step(binEdges[:-1],sumSpikes, where='post')
plt.show()


# -- Save figure --
if 1:
    figfilename = 'am_raster_{}'.format(oneCell).replace(' ','_')
    extraplots.save_figure(figfilename, 'png', [8,8], outputDir='/tmp/', facecolor='w')


