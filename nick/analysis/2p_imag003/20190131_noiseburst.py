import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt

dataDir = '/home/nick/data/2pdata/imag003/'
# dataDir = '/media/nick/My Passport/data/2pdata/imag003/'

'''
Objective: Do any neurons display frequency tuning?

From the Wiki page for imag003:

000_006: New field of view, new ROIs. 2x magnification. Collecting 4000 trials while presenting noise bursts. 100msec bursts. 2 sec, -/+0.2sec ISI. Behavior suffix 'c'

000_007: Same field of view, same ROIs. 2x mag. Collecting 3200 frames, 10 trials each of 8 frequencies at 70dB uncalibrated. This recording location is at -548um. During this recording I had the purple screen again in the realtime area. Not sure what is going on there. Behavior suffix 'd'.

Both of theses sessions have already been aligned and had signals extracted
using the scanbox matlab code, so they are easy to work with.
'''

#First, evaluate whether noisebursts give us anything
session = '000_006'
Fn = 'imag003_{}_rigid.signals.mat'.format(session)

#Read the file with the extracted signals
sigMat = os.path.join(dataDir, Fn)
sigData = io.loadmat(sigMat)

#Get number of frames and extracted ROIs
signals = sigData['sig']
nFrames, nROIs = np.shape(signals)

#Read the events file
rtMat = os.path.join(dataDir, 'imag003_{}_realtime.mat'.format(session))
rtData = io.loadmat(rtMat)

#Get onset frame numbers
ttl = rtData['ttl_log']
ttl = ttl.ravel().astype(int) #uint8 making things strange for diff

#This gets the leading edge frame of each event.
#Sometimes events span multiple frames, so this is necessary.
onsets = np.flatnonzero(np.diff((ttl==2).astype(int))==1)+1

#Drop the last event because too close to the end
onsets = onsets[:-1]
nEvents = len(onsets)

#How many samples before and after onset to average
samplesBefore = 10
samplesAfter = 30
nSamples = samplesBefore + samplesAfter

#Initialize array to hold stim-locked traces
alignedTraces = np.empty([nROIs, nEvents, nSamples])

for indEvent, onsetFrame in enumerate(onsets):
    frameStart = onsetFrame-samplesBefore
    frameEnd = onsetFrame+samplesAfter
    for indROI in range(nROIs):
        traceThisEvent = signals[frameStart:frameEnd, indROI]
        # baselineSubtractedTrace = traceThisEvent - traceThisEvent[0]
        # alignedTraces[indROI, indEvent, :] = baselineSubtractedTrace

        baselineAvg = np.mean(traceThisEvent[:8])
        dff = (traceThisEvent - baselineAvg) / baselineAvg
        alignedTraces[indROI, indEvent, :] = dff

#Average over events
averageResponse = np.mean(alignedTraces, axis=1)

plt.clf()

#### Plot ROI responses ####
ax = plt.subplot(111)
cax = ax.imshow(averageResponse)
cbar = plt.colorbar(cax, ax=ax)
ax.set_xticks([10, 30])
ax.set_xticklabels(['0', '20'])
ax.set_xlabel('Frames since sound onset')
ax.set_ylabel('ROI')
cbar.ax.set_ylabel('df/f')

#### Plot the ROIs ####
FnROI = 'imag003_{}_rigid.segment.mat'.format(session)

#Read the file with the ROI masks
roiMat = os.path.join(dataDir, FnROI)
roiData = io.loadmat(roiMat)
roiImg = roiData['mask']

# plt.subplot(121)
# plt.imshow(roiImg>0, cmap='gray')

plt.show()
# plt.tight_layout()




'''

#Load the behavior data
behavFn = loadbehavior.path_to_behavior_data('imag002', 'am_tuning_curve', '20181201b')
bdata = loadbehavior.BehaviorData(behavFn)

currentFreq = bdata['currentFreq']

if len(onsets) != len(currentFreq):
    currentFreq = currentFreq[:len(onsets)] #Events will stop sooner than behavior.

possibleFreq = np.unique(currentFreq)
maxEachFreq = np.empty(len(possibleFreq))
minEachFreq = np.empty(len(possibleFreq))
axEachFreq = []
for indFreq, thisFreq in enumerate(possibleFreq):
    ax = plt.subplot(4, 3, indFreq+1)
    axEachFreq.append(ax)
    onsetsThisFreq = onsets[np.flatnonzero(currentFreq==thisFreq)]
    averagesThisFreq = np.empty((len(onsetsThisFreq), np.shape(im0.asarray())[0], np.shape(im0.asarray())[1]))

    #Load just the tiff frames we need for each onset
    for indOnset, thisOnset in enumerate(onsetsThisFreq):
        framesThisOnset = range(thisOnset-samplesBefore, thisOnset+samplesAfter)
        #Using the with construct here auto-closes the TiffFile instances when done.
        with tifffile.TiffFile(fullFile, pages=framesThisOnset) as im:
            avgImageThisOnset = np.mean(im.asarray(), axis=0)
        averagesThisFreq[indOnset, :, :] = avgImageThisOnset

    avgAllOnsetsThisFreq = np.mean(averagesThisFreq, axis=0)
    maxEachFreq[indFreq] = np.max(avgAllOnsetsThisFreq.ravel())
    minEachFreq[indFreq] = np.min(avgAllOnsetsThisFreq.ravel())

    ax.imshow(avgAllOnsetsThisFreq)
    ax.set_title('{} Hz'.format(int(thisFreq)))

for ax in axEachFreq:
    ax.get_images()[0].set_clim(np.min(minEachFreq), np.max(maxEachFreq))
plt.tight_layout()
plt.show()

'''
