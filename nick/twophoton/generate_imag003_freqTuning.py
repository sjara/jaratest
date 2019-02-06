import os
import numpy as np
from scipy import io
from jaratoolbox import loadbehavior
from matplotlib import pyplot as plt
from skimage.external import tifffile

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
session = '000_007'
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
onsets = np.flatnonzero(np.diff((ttl==2).astype(int))==1)+1 #leading edges
onsets = onsets[:-1] #NOTE: Drop the last event because too close to the end
nEvents = len(onsets)

#How many samples before and after onset to average
samplesBefore = 10
samplesAfter = 30
nSamples = samplesBefore + samplesAfter

#Load the behavior data
behavFn = loadbehavior.path_to_behavior_data('imag003', 'am_tuning_curve', '20181217d')
bdata = loadbehavior.BehaviorData(behavFn)

currentFreq = bdata['currentFreq']
if len(onsets) != len(currentFreq):
    currentFreq = currentFreq[:len(onsets)] #Events will stop sooner than behavior.
possibleFreq = np.unique(currentFreq)

#Initialize array to hold stim-locked traces
alignedTraces = np.empty([nROIs, nEvents, nSamples])

for indEvent, onsetFrame in enumerate(onsets):
    frameStart = onsetFrame-samplesBefore
    frameEnd = onsetFrame+samplesAfter
    for indROI in range(nROIs):
        traceThisEvent = signals[frameStart:frameEnd, indROI]
        baselineAvg = np.mean(traceThisEvent[:8])
        dff = (traceThisEvent - baselineAvg) / baselineAvg
        alignedTraces[indROI, indEvent, :] = dff

#The idea is: iterate through each cell. For each cell, iterate through
#frequencies and collapse into an array of size (nPossibleFreq, nSamples).
#Save this array in an intermediate data location.
intermediateDataDir = '/home/nick/data/2pdata/tmp'

#Array to save preffered freqs
preferredFreqEachROI = np.empty(nROIs)

#Iterate over ROIs to save out average response per frequency
for indROI in range(nROIs):

    #Init an array to hold the average response per frequency
    averagePerFreqThisROI = np.empty([len(possibleFreq), nSamples])

    #For each frequency, average over the trials where it was presented.
    for indFreq, thisFreq in enumerate(possibleFreq):
        trialsThisFreq = np.flatnonzero(currentFreq==thisFreq)
        responsesThisFreq = alignedTraces[indROI, trialsThisFreq, :]
        assert np.shape(responsesThisFreq) == (len(trialsThisFreq), nSamples)
        averageThisFreq = np.mean(responsesThisFreq, axis=0)
        averagePerFreqThisROI[indFreq, :] = averageThisFreq

        #Save out the frequency with the max response for plotting
        maxEachFreq = np.max(averagePerFreqThisROI, axis=1)
        bestFreq = np.argmax(maxEachFreq)
        preferredFreqEachROI[indROI] = bestFreq

        #Save the average response per frequency for this ROI
        fName = os.path.join(intermediateDataDir, 'imag003_ROI_{}.npy'.format(indROI))
        np.save(fName, averagePerFreqThisROI)

FnROI = 'imag003_{}_rigid.segment.mat'.format(session)

#Read the file with the ROI masks
roiMat = os.path.join(dataDir, FnROI)
roiData = io.loadmat(roiMat)
roiImg = roiData['mask']

for indROI, preferredFreq in enumerate(preferredFreqEachROI):
    roiImg[roiImg==indROI+1] = preferredFreq

plt.clf()
ax = plt.subplot(111)
cax = ax.imshow(roiImg)
cbar = plt.colorbar(cax, ax=ax)
freqLabels = ['{:.1f}'.format(freq/1000) for freq in possibleFreq]
cbar.ax.set_yticklabels(freqLabels)
cbar.ax.set_ylabel('Preferred frequency (kHz)')
plt.show()

