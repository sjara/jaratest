"""
Load two-photon data.
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import io

from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots


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
    
# -- Load behavior --
behavFilename = loadbehavior.path_to_behavior_data(subject, paradigm, behavSession)
bdata = loadbehavior.BehaviorData(behavFilename)
currentFreq = bdata['currentFreq']
if nEvents != len(currentFreq):
    currentFreq = currentFreq[:nEvents] #Events will stop sooner than behavior.
possibleFreq = np.unique(currentFreq)
nFreq = len(possibleFreq)
trialsEachType = behavioranalysis.find_trials_each_type(currentFreq,possibleFreq)

# -- Calculate response each freq --
respEachFreqMean = np.empty([nCells,nFreq])
respEachFreqStDev = np.empty([nCells,nFreq])
nTrialsEachFreq = np.sum(trialsEachType,axis=0)
for indf,oneFreq in enumerate(possibleFreq):
    trialsThisFreq = trialsEachType[:,indf]
    respEachFreqMean[:,indf] = np.mean(ftraceEachTrial[:,trialsThisFreq],axis=1)
    respEachFreqStDev[:,indf] = np.std(ftraceEachTrial[:,trialsThisFreq],axis=1)
respEachFreqSEM = respEachFreqStDev/np.sqrt(nTrialsEachFreq)


# -- Plot ophys --
PLOTCASE = 3
# Interesting cells (006): [1, 34, 207]
# Interesting cells (007): [20, 199]
cellToPlot = 20
cellInd = np.flatnonzero(iscellInds==cellToPlot)[0]
if PLOTCASE==4:
    plt.clf()
    for oneEvent in stimOnsetFrame:
        plt.axvline(oneEvent, color='0.85',lw=1)

    plt.plot(ftraces[cellInd,:]) #color=[0.9,0.9,1]
    #plt.plot(spks[cellInd,:], color='b' )
    #plt.xlim(500,2000)
    #plt.xlim(0,350)
    plt.show()

if PLOTCASE==2:
    #ftraceEachTrial
    plt.clf()
    plt.hist(ftraceEachTrial[cellInd,:])
    plt.show()

if PLOTCASE==3:
    # HighF: 78, 52, 77, 60, 113, 107, 226, 368
    # LowF: 86, 145, 166, 305, 334, 391, 371
    plt.clf()
    #cellsToPlot = [20,199]
    #cellsToPlot = [86,107]
    cellsToPlot = [86,52]  # Best so far
    cellsToPlot = [86,2]  
    #trialsLowFreq = np.sum(trialsEachType[:,0:4], axis=1).astype(bool)
    #trialsHighFreq = np.sum(trialsEachType[:,4:], axis=1).astype(bool)
    trialsLowFreq = np.sum(trialsEachType[:,[2,3,4]], axis=1).astype(bool)
    trialsHighFreq = np.sum(trialsEachType[:,[5,6,7]], axis=1).astype(bool)
    cellInd0 = np.flatnonzero(iscellInds==cellsToPlot[0])[0]
    cellInd1 = np.flatnonzero(iscellInds==cellsToPlot[1])[0]
    plt.plot(ftraceEachTrial[cellInd0,trialsLowFreq],
             ftraceEachTrial[cellInd1,trialsLowFreq],'o',mfc='r',mec='none')
    plt.plot(ftraceEachTrial[cellInd0,trialsHighFreq],
             ftraceEachTrial[cellInd1,trialsHighFreq],'o',mfc='b',mec='none')
    plt.show()
  
if PLOTCASE==4:
    freqInds = np.arange(nFreq)
    pColor = '#1f77b4' #[0.4, 0.4, 0.7]
    plt.clf()
    for cellInd in range(400):
        plt.cla()
        plt.plot(freqInds,respEachFreqMean[cellInd,:],'o-',color=pColor)    
        plt.errorbar(freqInds,respEachFreqMean[cellInd,:],respEachFreqSEM[cellInd,:],color=pColor)
        plt.title(cellInd)
        plt.waitforbuttonpress()
        plt.show()
        
if PLOTCASE==5:
    freqInds = np.arange(nFreq)
    pColor = '#1f77b4' #[0.4, 0.4, 0.7]
    pageShape = [5,8]
    nPerPage = pageShape[0]*pageShape[1]
    SAVEFIG = 0
    for indpage in range(10):
        plt.clf()        
        for indc in range(nPerPage):
            plt.subplot(pageShape[0],pageShape[1],indc+1)
            cellInd = nPerPage*indpage + indc
            plt.plot(freqInds,respEachFreqMean[cellInd,:],'o-',color=pColor)    
            plt.errorbar(freqInds,respEachFreqMean[cellInd,:],
                         respEachFreqSEM[cellInd,:],color=pColor)
            plt.axis('off')
            plt.title(cellInd)
        plt.show()
        if SAVEFIG:
            figname = 'page{}'.format(indpage)
            extraplots.save_figure(figname, 'png', [20,12],
                                   outputDir='/tmp/tuning/', facecolor='w')
        #plt.waitforbuttonpress()

