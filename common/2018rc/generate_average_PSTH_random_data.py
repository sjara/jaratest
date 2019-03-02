'''
Make average PSTH for movement selectivity (as requested by reviewer).

NOTE: We find that this may be misleading because for any effect that goes in both directions,
an average will be around zero. And separating conditions (positive and negative) seems circular
since an effect will be visible even for noise.

'''

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import extraplots

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'averagePSTH_random_data' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [10,5] # In inches

np.random.seed(4)

nSamples = 100
nCells = 200
nCond = 2
colorEachCond = ['b','r']
xEachCond = np.random.random((nCells,nCond,nSamples))
timeVec = np.arange(-nSamples/2,nSamples/2)

smoothWinSize= 20;
winShape = np.ones(smoothWinSize) # Acausal
#winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Causal
winShape = winShape/np.sum(winShape)

meanSecondHalf = np.mean(xEachCond[:,:,50:],axis=2) # [nCells, nCond]
positiveCells = (np.diff(meanSecondHalf)>0).flatten()

plt.clf()
labelPosX = [0.07, 0.54]   # Horiz position for panel labels
labelPosY = [0.95, 0.48]    # Vert position for panel labels
fontSizePanel = 16

gs = gridspec.GridSpec(2, 2)
gs.update(left=0.15, right=0.95, top=0.95, bottom=0.1, wspace=0.3, hspace=0.4)

plt.subplot(gs[0,0])
plt.gca().annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
#plt.plot(np.tile(timeVec,[10,1]),xEachCond[:10,0,:],color='0.9',zorder=0)
for indc in range(nCond):
    for oneTrace in xEachCond[:5,indc,:]:
        plt.plot(timeVec,oneTrace,color=colorEachCond[indc],zorder=0,alpha=0.5)
        plt.hold(1)
    #smoothPSTH = np.convolve(np.mean(xEachCond[:,indc,:],axis=0),winShape,mode='same')
    #plt.plot(timeVec,smoothPSTH,color=colorEachCond[indc],lw=4)
plt.axvline(0,color='k')
plt.xlim([-40,40])
plt.title('Random traces (two conditions: blue & red)')
plt.xlabel('Time')
plt.ylabel('Amplitude\n(like PSTH each cell)')

plt.subplot(gs[1,0])
plt.gca().annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
meanPSTH = np.mean(xEachCond[positiveCells,:,:],axis=0)
for indc in range(nCond):
    #plt.plot(xEachCond[positiveCells,indc,:].T,color='0.9',zorder=0)
    #plt.plot(meanPSTH[indc],color=colorEachCond[indc],lw=2)
    smoothPSTH = np.convolve(meanPSTH[indc],winShape,mode='same')
    plt.plot(timeVec,smoothPSTH,color=colorEachCond[indc],lw=4)
    plt.hold(1)
plt.axvline(0,color='k')
plt.xlim([-40,40])
plt.ylim([0.4,0.6])
plt.xlabel('Time')
plt.ylabel('Smoothed average trace\n(like average PSTH)')
plt.title('For selected traces where: Red > Blue')
#plt.legend(['Blue','Red'])


# -- NOTE: I'm calculating the difference (red-blue) not the normalized index --
plt.subplot(gs[:,1])
plt.gca().annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
[nvals,bins,patches] = plt.hist(np.diff(meanSecondHalf),fc='0.75')
#plt.setp(patches,fc='0.5')
plt.xlim([-0.5,0.5])
plt.xlabel('Red-Blue (for time > 0)')
plt.ylabel('Number of "cells"')
plt.text(0.3,50,'Red > Blue\n(for time>0)',ha='center')
plt.text(-0.3,50,'Red < Blue\n(for time>0)',ha='center')
plt.show()

'''
meanPSTH = np.mean(xEachCond,axis=0)
for indc in range(nCond):
    plt.plot(xEachCond[:,indc,:].T,color='0.9',zorder=0)
    plt.plot(meanPSTH[indc],color=colorEachCond[indc],lw=2)
    plt.hold(1)
'''


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
