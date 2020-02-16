"""
Load two-photon data.
"""

import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import matplotlib
from scipy import io

from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp

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
# HighF: 78, 52, 77, 60, 113, 107, 226, 368
# LowF: 86, 145, 166, 305, 334, 391, 371
plt.clf()
ax0 = plt.gca()
RASTERIZED = False #True
cellsToPlot = [86,52]  # Best so far
#cellsToPlot = [86,2]
color0 = cp.TangoPalette['SkyBlue2']
color1 = cp.TangoPalette['ScarletRed1']
markerSize = 8
#trialsLowFreq = np.sum(trialsEachType[:,0:4], axis=1).astype(bool)
#trialsHighFreq = np.sum(trialsEachType[:,4:], axis=1).astype(bool)
trialsLowFreq = np.sum(trialsEachType[:,[2,3,4]], axis=1).astype(bool)
trialsHighFreq = np.sum(trialsEachType[:,[5,6,7]], axis=1).astype(bool)
cellInd0 = np.flatnonzero(iscellInds==cellsToPlot[0])[0]
cellInd1 = np.flatnonzero(iscellInds==cellsToPlot[1])[0]
plt.plot(ftraceEachTrial[cellInd0,trialsLowFreq],
         ftraceEachTrial[cellInd1,trialsLowFreq],
         'o', ms=markerSize, mew=3, mec=color0,mfc='none',rasterized=RASTERIZED)
plt.plot(ftraceEachTrial[cellInd0,trialsHighFreq],
         ftraceEachTrial[cellInd1,trialsHighFreq],
         'o', ms=markerSize, mew=3, mec=color1,mfc='none',rasterized=RASTERIZED)

#plt.axis('square')
#plt.xlim()
#plt.ylim()
plt.axis([4866, 6238, 4407, 7830])
ax0.set_xticklabels([])
ax0.set_yticklabels([])
ax0.tick_params('both',direction='in')
extraplots.boxoff(ax0)

fontSize = 18
plt.xlabel('Response: Neuron {}'.format(cellsToPlot[0]),fontsize=fontSize)
plt.ylabel('Response: Neuron {}'.format(cellsToPlot[1]),fontsize=fontSize)
plt.show()


# -- Classifier --
if 1:
    from sklearn import svm
    nClass0 = np.sum(trialsLowFreq)
    nClass1 = np.sum(trialsHighFreq)
    class0 = np.vstack([ftraceEachTrial[cellInd0,trialsLowFreq],
                        ftraceEachTrial[cellInd1,trialsLowFreq]]).T
    class1 = np.vstack([ftraceEachTrial[cellInd0,trialsHighFreq],
                        ftraceEachTrial[cellInd1,trialsHighFreq]]).T
    dataPoints = np.vstack([class0, class1])
    dataLabels = np.concatenate([np.zeros(nClass0),np.ones(nClass1)])
    clf = svm.SVC(kernel='linear', C=10)
    clf.fit(dataPoints, dataLabels)
    # -- Plot boundary --
    #plot_contours(ax0, clf, dataPoints, dataLabels)
    xlim = ax0.get_xlim()
    ylim = ax0.get_ylim()
    xx = np.linspace(xlim[0], xlim[1], 4)
    yy = np.linspace(ylim[0], ylim[1], 4)
    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.decision_function(xy).reshape(XX.shape)
    colorBoundary = cp.TangoPalette['Chameleon2']
    #ax0.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
    #            linestyles=['--', '-', '--'])
    hbound = ax0.contour(XX, YY, Z, colors=colorBoundary, levels=[0],
                         linestyles=['-'], zorder=-1)


SAVEFIG = 0
if SAVEFIG:
    figname = 'twocell_scatter'
    extraplots.save_figure(figname, 'svg', [3.5, 3.5], outputDir='/tmp/')
