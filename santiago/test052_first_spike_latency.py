'''
Testing methods for calculating latency to first spike.

TO DO:
- Subtract baseline
- Smooth PSTH to avoid noisy peak and noisy threshold

'''

import numpy as np
import matplotlib.pyplot as plt

datafile = '/mnt/jarahubdata/figuresdata/2018thstr/latency_data.npz'

data = np.load(datafile)

#goodCells = [2,9,11,34]
cellind = 2

spikeTimes = data['data'][cellind]['spikeTimes']
trialInds = data['data'][cellind]['trialInds']

newTrialInds = np.empty(trialInds.shape, dtype=int)
uniqueTrialInds = np.unique(trialInds)
# The next thing is slow, but I don't have time to optimize
for ind,trialInd in enumerate(uniqueTrialInds):
    newTrialInds[trialInds==trialInd] = ind

# NOTE: we can't use our usual code because the data doesn't have indexLimitsEachTrial!!!
#spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,binEdges)

binEdges = np.arange(0,0.1,0.001)
nTrials = len(uniqueTrialInds)
spikeCountMat = np.empty((nTrials,len(binEdges)-1),dtype=int)
for indtrial in range(nTrials):
    indsThisTrial = (newTrialInds==indtrial) # boolean
    spkCountThisTrial,binsEdges = np.histogram(spikeTimes[indsThisTrial],binEdges)
    spikeCountMat[indtrial,:] = spkCountThisTrial

avResp = np.mean(spikeCountMat,axis=0)
maxResp = np.max(avResp)
threshold = 0.2*maxResp
respLatencyInd = np.flatnonzero(avResp>threshold)[0]
timeVec = binsEdges[1:]  # FIXME: is this the best way to define the time axis?
respLatency = timeVec[respLatencyInd]
print 'Response latency: {} sec'.format(respLatency)

plt.clf()
plt.title(cellind)
plt.subplot(2,1,1)
plt.plot(spikeTimes,newTrialInds,'.k')
plt.hold(1)
plt.axvline(respLatency,color='r')

plt.subplot(2,1,2)
#plt.imshow(spikeCountMat,cmap='gray')
plt.plot(binsEdges[1:], avResp,'.-')
plt.hold(1)
plt.axvline(respLatency,color='r')
plt.show()


'''
# -- Find interesting cells --
for cellind in goodCells:
    spikeTimes = data['data'][cellind]['spikeTimes']
    trialInds = data['data'][cellind]['trialInds']
    plt.clf()
    plt.title(cellind)
    plt.plot(spikeTimes,trialInds,'.k')
    plt.show()
    plt.waitforbuttonpress()
'''
