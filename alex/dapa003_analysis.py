from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
reload(loadopenephys)
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import stats
import os
import pdb

subject = 'dapa003'

#Generate cell database
db = celldatabase.generate_cell_database('/home/jarauser/src/jaratest/common/inforecordings/dapa003_inforec.py')

#Calculate shape quality
allShapeQuality = np.empty(len(db))
for indCell, cell in db.iterrows():
    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']
    thisShapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    allShapeQuality[indCell] = thisShapeQuality
allShapeQuality[allShapeQuality==np.inf]=0
db['shapeQuality'] = allShapeQuality

#Select good cells
goodCells = db.query('isiViolations<0.02 and shapeQuality>2')

'''
#Cell 15
thisCell = goodCells[9:10]
tetrode = int(thisCell['tetrode'][15]) #TODO: Find out how to get the index for a dataframe
cluster = int(thisCell['cluster'][15])
behavFileName = thisCell['behavior'][15][1]
session = thisCell['ephys'][15][1]
'''

#Cell 24
thisCell = goodCells[18:19]
tetrode = int(thisCell['tetrode'][24]) #TODO: Find out how to get the index for a dataframe; cell.iloc[x]?
cluster = int(thisCell['cluster'][24])
behavFileName = thisCell['behavior'][24][1]
session = thisCell['ephys'][24][1]

###############CURRENT POSITION - NEED CELL TO ANALYZE#################

#Load ephys data
ephysBaseDir = os.path.join(settings.EPHYS_PATH, subject)
eventFilename=os.path.join(ephysBaseDir,
                           session,
                           'all_channels.events')
spikesFilename=os.path.join(ephysBaseDir,
                            session,
                            'Tetrode{}.spikes'.format(tetrode))
eventData=loadopenephys.Events(eventFilename)
spikeData = loadopenephys.DataSpikes(spikesFilename)
clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(session))
clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
spikeData.set_clusters(clustersFile)
if cluster is not None:
    spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
    spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]

# convert to seconds and millivolts
spikeData.samples = spikeData.samples.astype(float)-2**15
spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
eventData.timestamps = eventData.timestamps/eventData.samplingRate


behavFile = os.path.join(settings.BEHAVIOR_PATH,subject,behavFileName)
bdata = loadbehavior.BehaviorData(behavFile,readmode='full')


# LOAD YOUR SHIT
#eventData, spikeData = load_ephys_data(subject, session, tetrode, cluster)
eventOnsetTimes = eventData.get_event_onset_times()
spikeTimeStamps = spikeData.timestamps
tuningBData = bdata   

freqEachTrial = tuningBData['currentFreq']

timeRange = [-0.1, 1.0]

trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, np.unique(freqEachTrial))
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimeStamps, eventOnsetTimes, timeRange)

#print len(freqEachTrial), len(eventOnsetTimes)

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                               trialsEachCond=trialsEachCond)


xlabel = 'time (s)'
ylabel = 'Trial'

plt.xlabel(xlabel)
plt.ylabel(ylabel)

#plt.setp(pRaster, ms=ms)

plt.show()









'''
for indcond,trialsThisCond in enumerate(trialsEachCond):
        spikeTimesThisCond = np.empty(0,dtype='float64')
        trialIndexThisCond = np.empty(0,dtype='int')
        for indtrial,thisTrial in enumerate(trialsThisCond):
            indsThisTrial = slice(indexLimitsEachTrial[0,thisTrial],
                                  indexLimitsEachTrial[1,thisTrial])

nTrials = len(indexLimitsEachTrial[0])
(trialsEachCond2,nTrialsEachCond,nCond) = extraplots.trials_each_cond_inds(trialsEachCond,nTrials)

print len(trialsEachCond[1])

print len(trialsEachCond2[1])
'''