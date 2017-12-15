'''
Testing methods for calculating latency to first spike.

TO DO:
- Subtract baseline
- Smooth PSTH to avoid noisy peak and noisy threshold

'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

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
#winShape = [0.25,0.5,1,0.5,0.25]; winShape = winShape/np.sum(winShape)
winShape = scipy.signal.hanning(7); winShape = winShape/np.sum(winShape)
smoothPSTH = np.convolve(avResp,winShape,mode='same')
avBaseline = np.mean(smoothPSTH[:10])

maxResp = np.max(smoothPSTH)
threshold = avBaseline + 0.5*(maxResp-avBaseline)
respLatencyInd = np.flatnonzero(smoothPSTH>threshold)[0]
timeVec = binsEdges[1:]  # FIXME: is this the best way to define the time axis?
#respLatency = timeVec[respLatencyInd]
yFraction = (threshold-smoothPSTH[respLatencyInd-1])/(smoothPSTH[respLatencyInd]-smoothPSTH[respLatencyInd-1])
respLatency = timeVec[respLatencyInd-1] + yFraction*(timeVec[respLatencyInd]-timeVec[respLatencyInd-1])

print 'Response latency: {} sec'.format(respLatency)

plt.clf()
plt.title(cellind)
plt.subplot(2,1,1)
plt.plot(spikeTimes,newTrialInds,'.k')
plt.hold(1)
plt.axvline(respLatency,color='r')

plt.subplot(2,1,2)
#plt.imshow(spikeCountMat,cmap='gray')
plt.plot(binsEdges[1:], avResp,'.-k')
plt.hold(1)
plt.axvline(respLatency,color='r')
plt.axhline(threshold,ls='--',color='0.75')
plt.axhline(avBaseline,ls=':',color='0.75')
plt.axhline(maxResp,ls=':',color='0.75')
plt.plot(binsEdges[1:],smoothPSTH,'ro-',mec='none',lw=3)
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
