import os
import numpy as np
from scipy import io
from jaratoolbox import loadbehavior
from matplotlib import pyplot as plt
from skimage.external import tifffile

dataDir = '/home/nick/data/imag002_20181201/'
session = '000_002'
Fn = 'imag002_20181201_{}.tif'.format(session)

#Read in data file (nFrames, m, n)
fullFile = os.path.join(dataDir, Fn)
im0 = tifffile.TiffFile(fullFile, pages=[0])
# im = tifffile.imread(fullFile)

#Read the events file
rtMat = os.path.join(dataDir, 'imag002_20181201_{}_realtime.mat'.format(session))
rtData = io.loadmat(rtMat)

#Get onset frame numbers
ttl = rtData['ttl_log']
ttl = ttl.ravel().astype(int) #uint8 making things strange for diff
onsets = np.flatnonzero(np.diff(ttl.astype(int))==2)+1 #Should catch the leading edges

#How many samples before and after onset to average
samplesBefore = 0
samplesAfter = 20
traceLen = samplesBefore + samplesAfter

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

