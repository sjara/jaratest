'''
Create figure about photostimulation outside the task.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
import figparams
reload(figparams)

FIGNAME = 'photostim_outside_task'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,0] # Which panels to plot

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'plots_photostim_outside_task' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.5]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

STIM_DURATION = 1.5 # HARDCODED (in seconds)


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2)
gs.update(left=0.05, right=0.95, wspace=.1, hspace=0.5)


# -- Panel: example of change in head angle --
ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[0, 1])
if PANELS[0]:
    exampleFilename = 'example_photostim_outside_task.npz'
    exampleFullPath = os.path.join(dataDir,exampleFilename)
    exampledata = np.load(exampleFullPath)

    stimSideEachCond = exampledata['stimSideEachCond']
    stimRegionEachCond = exampledata['stimRegionEachCond']
    headAngleEachCond = exampledata['headAngleEachCond']
    stimSamples = exampledata['stimSamples']
    
    laserColor = figparams.colp['blueLaser']
    backStrColor = figparams.cp.TangoPalette['Chameleon3']
    frontStrColor = figparams.cp.TangoPalette['ScarletRed1']
    yLims = np.array([-3,3])
    xbar = (stimSamples[1]-stimSamples[0]) / STIM_DURATION
    ybar = 45 * (np.pi/180)  # From radians to degrees
    stimYpos = 2.8
    
    plt.axes(ax1)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=8,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Left', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels)
    plt.ylim(yLims)
    extraplots.scalebar(10,-2,xbar,ybar,'1 s','45 deg',fontsize=12)
    ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')
    plt.axis('off')
    
    plt.axes(ax2)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=8,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Right', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels)
    plt.ylim(yLims)
    ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')
    plt.axis('off')
    leg = plt.legend(['Front striatum','Back striatum'], loc='lower center', frameon=False, labelspacing=0.2)
    leg.set_frame_on(False)

    '''
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
    plt.plot(trialLimsL,2*[stimYpos],lw=8,color=laserColor)
    plt.plot(trialLimsR,2*[stimYpos],lw=8,color=laserColor)
    plt.hold(0)
    extraplots.boxoff(plt.gca())
    plt.xlim(xLims)
    plt.ylim(yLims)

    plt.xlabel('Time (video frames)', fontsize=fontSizeLabels)
    plt.ylabel('Head angle (radians)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    '''


# -- Panel: Summary of change in head angle --
ax3 = plt.subplot(gs[1,:-1])
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
    ax3.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

    

plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

