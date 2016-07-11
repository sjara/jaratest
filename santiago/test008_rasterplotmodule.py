'''
Testing raster_plot from extraplots
'''


from jaratoolbox import spikesanalysis
reload(spikesanalysis)
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import extraplots
reload(extraplots)
from pylab import *

if 0:
    timeStamps = np.cumsum(np.random.random(120))
    eventOnsetTimes = np.arange(10,60,10)
    timeRange = [-4,6]
    trialsEachCond=[[0,2],[1,3,4]]
else:
    nFactor = 60
    timeStamps = np.cumsum(np.random.random(20*nFactor))
    eventOnsetTimes = np.arange(10,10*nFactor,10)
    timeRange = [-10,20]
    trialsEachCond=[range(0,nFactor-1,2),range(1,nFactor-1,2)]
    
nTrials = len(eventOnsetTimes)

# plot(timestamps,ones(len(timestamps)),'.'); show()

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(timeStamps,eventOnsetTimes,timeRange)


clf()
ax1=subplot(3,1,1)
plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.'); show()
ylim([-1,nTrials])

# -- Plot sorted raster --
ax2=subplot(3,1,2,sharex=ax1)

colorEachCond=None
fillWidth=None
labels = ['one','two']

extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                       trialsEachCond=trialsEachCond,
                       colorEachCond=colorEachCond,fillWidth=fillWidth,labels=labels)
show()

timeVec = np.arange(timeRange[0],timeRange[-1]+2,2) # Bin edges (including right-most)
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
#spikeCountMat = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

ax3=subplot(3,1,3,sharex=ax1)
bar(timeVec[:-1],mean(spikeCountMat,axis=0),width=timeVec[1]-timeVec[0], facecolor='0.5',lw=2)
show()

'''
timeVec = np.arange(timeRange[0],timeRange[-1]+2,2.0) # Bin edges (including right-most)

nTrials = indexLimitsEachTrial.shape[1]
spikeCountMat = np.empty((nTrials,len(timeVec)-1),dtype=int)
for indtrial in range(nTrials):
    indsThisTrial = slice(indexLimitsEachTrial[0,indtrial],indexLimitsEachTrial[1,indtrial])
    spkCountThisTrial,binsEdges = np.histogram(spikeTimesFromEventOnset[indsThisTrial],timeVec)
    spikeCountMat[indtrial,:] = spkCountThisTrial
'''

'''
nTrials = indexLimitsEachTrial.shape[1]
deltaTime = timeVec[1]-timeVec[0]
spikeRasterMat = np.zeros((nTrials,len(timeVec)),dtype=bool)
for indtrial in range(nTrials):
    indsThisTrial = slice(indexLimitsEachTrial[0,indtrial],indexLimitsEachTrial[1,indtrial])
    sampleIndexOfSpike = np.around( (spikeTimesFromEventOnset[indsThisTrial]-timeVec[0]) / deltaTime ).astype(int)
    #if indtrial==1: 1/0 ### DEBUG
    spikeRasterMat[indtrial,sampleIndexOfSpike]=True
'''

'''
'''
