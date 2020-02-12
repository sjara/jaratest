"""
Load two-photon data.
"""

import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy import io

from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

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
# Interesting cells (006): [1, 34, 207]
# Interesting cells (007): [20, 199]
# HighF: 78, 52, 77, 60, 113, 107, 226, 368
# LowF: 86, 145, 166, 305, 334, 391, 371
cellsToPlot = np.arange(20)
#cellsToPlot = [20, 199, 78, 52, 77, 60, 113, 107, 226, 368, 86, 145, 166, 305, 334, 391, 37]
cellsToPlot = [0,2,4,7,8,9,6,10,11,12,23,14,16,17,18,19,21,20]
rangeToPlot = np.arange(000,2000)
plt.clf()
ax0 = plt.gca()
fontSize = 18
RASTERIZED = 1#False #True

for indc,cellToPlot in enumerate(cellsToPlot):
    cellInd = np.flatnonzero(iscellInds==cellToPlot)[0]
    normedTrace = ftraces[cellInd,rangeToPlot]
    normedTrace = normedTrace-min(normedTrace)
    normedTrace = 0.2 * normedTrace/np.std(normedTrace)
    yOffset = len(cellsToPlot) - np.tile(indc,len(normedTrace))
    xVals = np.arange(len(rangeToPlot))/SAMPLING_RATE
    plt.plot(xVals, yOffset+normedTrace, rasterized=RASTERIZED)
ax0.set_xticks([0,20])
ax0.set_xticklabels([])
ax0.set_yticks([])
plt.xlabel('Time',fontsize=fontSize)
plt.ylabel('Neuron #',fontsize=fontSize)
plt.box(False)
plt.show()

print('Number of segmented cells: {}'.format(np.sum(iscellBool)))

SAVEFIG = 0
if SAVEFIG:
    figname = 'fluo_traces'
    extraplots.save_figure(figname, 'svg', [3.5, 3.5], outputDir='/tmp/')
