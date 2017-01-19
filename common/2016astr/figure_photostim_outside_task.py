'''
Create figure about photostimulation outside the task.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import settings
from jaratoolbox import extraplots
import figparams
reload(figparams)

FIGNAME = 'photostim_outside_task'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,0] # Which panels to plot

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'testfig' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.65]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)


# -- Panel: example of change in head angle --
ax1 = plt.subplot(gs[0, :])
if PANELS[0]:
    exampleFilename = 'example_head_angle_dmstr.npz'
    exampleFullPath = os.path.join(dataDir,exampleFilename)
    dmstr = np.load(exampleFullPath)

    headAngle = dmstr['headAngle']
    stimBool = dmstr['stimBool']
    firstFrameEachTrial = dmstr['firstFrameEachTrial']
    lastFrameEachTrial = dmstr['lastFrameEachTrial']

    trialToPlotL = 4
    trialToPlotR = 3
    stimYpos = 2.5
    xLims = [920,1250]
    yLims = [-3.5,3]
    plt.hold(1)
    plt.plot(headAngle,'-',lw=2,color='k')
    trialLimsL = [firstFrameEachTrial[0][trialToPlotL],lastFrameEachTrial[0][trialToPlotL]]
    trialLimsR = [firstFrameEachTrial[1][trialToPlotR],lastFrameEachTrial[1][trialToPlotR]]
    laserColor = figparams.colp['blueLaser']
    plt.plot(trialLimsL,2*[stimYpos],lw=8,color=laserColor)
    plt.plot(trialLimsR,2*[stimYpos],lw=8,color=laserColor)
    plt.hold(0)
    extraplots.boxoff(plt.gca())
    plt.xlim(xLims)
    plt.ylim(yLims)

    plt.xlabel('Time (video frames)', fontsize=fontSizeLabels)
    plt.ylabel('Head angle (radians)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')

# -- Panel: Summary of change in head angle --
ax2 = plt.subplot(gs[1,:-1])
if PANELS[1]:
    summaryFilename = 'head_angle_summary.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    haFile = np.load(summaryFullPath)
    stimSides = haFile['stimSides']
    allDeltaHeadAngle = haFile['deltaAngleEachTrialEachSession']
    leftDeltaHeadAngle = allDeltaHeadAngle[stimSides=='left']
    rightDeltaHeadAngle = allDeltaHeadAngle[stimSides=='right']

    plt.hold(1)
    for ind,dha in enumerate(leftDeltaHeadAngle):
        nTrials = len(dha)
        plt.plot(np.tile(ind,nTrials),dha,'o',mfc='None')
    for ind,dha in enumerate(rightDeltaHeadAngle):
        nTrials = len(dha)
        offset = len(leftDeltaHeadAngle)+2
        plt.plot(np.tile(ind+offset,nTrials),dha,'o',mfc='None')
    plt.hold(0)

    extraplots.boxoff(plt.gca())
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Session', fontsize=fontSizeLabels)
    plt.ylabel('Change in head angle (rad)', fontsize=fontSizeLabels)
    ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

    

plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

