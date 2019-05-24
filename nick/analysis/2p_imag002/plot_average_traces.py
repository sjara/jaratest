from scipy import io
import numpy as np
from jaratoolbox import loadbehavior
from matplotlib import pyplot as plt
import os

dataDir = '/home/nick/data/imag002_20181201/'
behavDir = '/home/nick/data/behavior/imag002'
session = '000_003' #NoiseBurst session
# session = '000_002' #AM session (I think), 3000 frames, 10 trials x 11 conditions
# behavSuffix = 'b'

rtMat = os.path.join(dataDir, 'imag002_20181201_{}_realtime.mat'.format(session))
# behavPath = os.path.join(behavDir, 'imag002_am_tuning_curve_20181201{}.h5'.format(behavSuffix))

rtData = io.loadmat(rtMat)

activityMat = rtData['rtdata']
ttl = rtData['ttl_log']
ttl = ttl.ravel().astype(int) #uint8 making things strange for diff
onsets = np.flatnonzero(np.diff(ttl.astype(int))==2)+1 #Should catch the leading edges
onsets = onsets[:-1] #Remove the last one because we didn't get onset+30

#Number of samples from event onset to plot
samplesBefore = 10
samplesAfter = 15
traceLen = samplesBefore + samplesAfter
nROIs = np.shape(activityMat)[1]

#Shape nTraces, nTrials, nROIs
traceArray = np.empty((traceLen, len(onsets), nROIs))

for indROI in range(nROIs):
    for indOnset, onsetFrame in enumerate(onsets):
        thisTrace = activityMat[onsetFrame-samplesBefore:onsetFrame+samplesAfter, indROI]
        thisTrace = thisTrace - thisTrace[0] #subtract starting point
        traceArray[:, indOnset, indROI] = thisTrace

averageResponse = np.mean(traceArray, axis=1) #average over trials

plt.clf()
for indROI in range(nROIs):
    plt.plot(averageResponse[:,indROI])

plt.show()


