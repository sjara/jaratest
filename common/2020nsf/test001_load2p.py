"""
Load two-photon data and separate responses by stimulus (in this case sound freq)
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import io

from jaratoolbox import settings


subject = 'imag003'

RESONANCE_FREQ = 8000 # Really 7910,  https://www.cambridgetechnology.com/sites/default/files/Datasheet%20-%20ResonantScanner_7.pdf
LINES_PER_FRAME = 512
SAMPLING_RATE = 15 # Hz

# -- Params ophys --
ophysSession = '000_007'
suite2pDir = 'suite2p/plane0/'
fluoFile = 'F.npy'
isCellFile = 'iscell.npy'
spksFile = 'spks.npy'
stimSyncFile = '{}_{}{}'.format(subject,ophysSession,'.mat')
ophysSessionDir = os.path.join(settings.TWOPHOTON_PATH,subject,ophysSession)

# -- Params behavior --
paradigm = 'am_tuning_curve'
behavSession = '20181217d'

# -- Load ophys --
ophysDataDir = os.path.join(ophysSessionDir,suite2pDir)
ftracesAll = np.load(os.path.join(ophysDataDir,fluoFile))
spksAll = np.load(os.path.join(ophysDataDir,spksFile))
iscell = np.load(os.path.join(ophysDataDir,isCellFile))
iscellBool = iscell[:,0]>0
iscellInds = np.flatnonzero(iscellBool)

ftraces = ftracesAll[iscellBool,:]
spks = spksAll[iscellBool,:]
nCells = np.sum(iscellBool)

# -- Load stim sync --
syncData = io.loadmat(os.path.join(ophysSessionDir,stimSyncFile))
idata = syncData['info'][0][0]
# TEST: for onecol in idata: print(onecol.dtype)

frameSB = idata[0].flatten()-1  # Convert to Python (start at 0)
lineSB = idata[1].flatten()-1   # Convert to Python (start at 0)
eventidSB = idata[2].flatten()
onsetFrameSB = frameSB[0::2]
onsetLineSB = lineSB[0::2]
stimOnsetFrame = onsetFrameSB+onsetLineSB/LINES_PER_FRAME
stimOnsetFrame = stimOnsetFrame[:-1] # Remove last to avoid problems of not having full data
nEvents = len(stimOnsetFrame)

# -- Calculate response each trial --
ftraceEachTrial = np.empty([nCells, nEvents])

responseWindow = [0,30] # in frames
for indEvent, stimOnset in enumerate(stimOnsetFrame):
    # FIXME: I'm rounding the stimOnset. Not sure if this is the best option
    rangeLims = int(np.round(stimOnset)) + np.array(responseWindow)
    frameRange = np.arange(rangeLims[0],rangeLims[1])
    ftraceEachTrial[:,indEvent] = np.mean(ftraces[:,frameRange],axis=1)
    '''
    # -- From Nick's code:jaratest/nick/twophoton/generate_imag003_freqTuning.py --
    for indROI in range(nROIs):
        traceThisEvent = signals[frameStart:frameEnd, indROI]
        baselineAvg = np.mean(traceThisEvent[:8])
        dff = (traceThisEvent - baselineAvg) / baselineAvg
        alignedTraces[indROI, indEvent, :] = dff
    '''

# -- Plot ophys --
PLOTCASE = 1
# Interesting cells (006): [1, 34, 207]
# Interesting cells (007): [20, 199]
cellToPlot = 20
cellInd = np.flatnonzero(iscellInds==cellToPlot)[0]
if PLOTCASE==1:
    plt.clf()
    for oneEvent in stimOnsetFrame:
        plt.axvline(oneEvent, color='0.85',lw=1)

    #plt.plot(ftraces[cellInd,:]) #color=[0.9,0.9,1]
    #plt.plot(spks[cellInd,:], color='b' )

    xVals = np.arange(len(ftraces[cellInd,:]))/SAMPLING_RATE
    plt.plot(xVals,ftraces[cellInd,:]) #color=[0.9,0.9,1]
    
    #plt.xlim(500,2000)
    #plt.xlim(0,350)
    plt.show()

if PLOTCASE==2:
    #ftraceEachTrial
    plt.clf()
    plt.hist(ftraceEachTrial[cellInd,:])
    plt.show()

if PLOTCASE==3:
    plt.clf()
    cellsToPlot = [20,199]
    cellInd0 = np.flatnonzero(iscellInds==cellsToPlot[0])[0]
    cellInd1 = np.flatnonzero(iscellInds==cellsToPlot[1])[0]
   
    plt.plot(ftraceEachTrial[cellInd0,:],ftraceEachTrial[cellInd1,:],'o')
    plt.show()
  
