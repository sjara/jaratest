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

PANELS = [1,1] # Which panels to plot

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'plots_photostim_outside_task' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

#labelPosX = [0.2, 0.4, 0.65]   # Horiz position for panel labels
#labelPosY = [0.9]    # Vert position for panel labels
labelPosX = [0.07, 0.38, 0.7]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

STIM_DURATION = 1.5 # HARDCODED (in seconds)


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.12, right=0.95, wspace=.1, hspace=0.5)


# -- Panel: example of change in head angle --
ax1 = plt.subplot(gs[0, 1])
ax2 = plt.subplot(gs[0, 2])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
#ax2.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
#             fontsize=fontSizePanel, fontweight='bold')
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
    ybar = 45 * (np.pi/180)  # From degrees to radians
    stimYpos = 2.8
    
    plt.axes(ax1)
    plt.hold(True)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=8,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Left', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels+2)
    plt.ylim(yLims)
    extraplots.scalebar(10,-2,xbar,ybar,'1 s','45 deg',fontsize=12)
    plt.axis('off')
    
    plt.axes(ax2)
    plt.hold(True)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=3, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=8,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Right', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels+2)
    plt.ylim(yLims)
    plt.axis('off')
    leg = plt.legend(['Anterior striatum','Posterior striatum'], loc='lower center', frameon=False, labelspacing=0.2)
    leg.set_frame_on(False)


# -- Panel: Summary of change in head angle --
ax3 = plt.subplot(gs[1,0:])
ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    summaryFilename = 'head_angle_summary.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    haFile = np.load(summaryFullPath)

    subject = haFile['subject']
    session = haFile['session']
    deltaHeadAngle = haFile['deltaAngleEachTrial']
    stimSide = haFile['stimSide']
    stimRegion = haFile['stimRegion']

    possibleSubjects = np.unique(subject)
    markerEachSubject = ['o','o','o','o','o','o','o']

    stimFrontLeft = (stimSide=='left') & (stimRegion=='frontStr')
    stimFrontRight = (stimSide=='right') & (stimRegion=='frontStr')
    stimBackLeft = (stimSide=='left') & (stimRegion=='backStr')
    stimBackRight = (stimSide=='right') & (stimRegion=='backStr')
    eachCond = [stimFrontLeft, stimFrontRight, stimBackLeft, stimBackRight]
    
    xPos = [0,1,3,4]
    xLabels = ['FL','FR', 'BL','BR']
    
    plt.hold(1)
    for indc, oneCond in enumerate(eachCond):
        for inds in np.flatnonzero(oneCond):
            indSubject = np.flatnonzero(possibleSubjects==subject[inds])[0]
            thisMarker = markerEachSubject[indSubject]
            nSamples = len(deltaHeadAngle[inds])
            xvals = np.tile(xPos[indc]+0.2*indSubject,nSamples)
            yvals = (180/np.pi) * deltaHeadAngle[inds] # From radians to degrees
            plt.plot(xvals,yvals,'o',marker=markerEachSubject[indSubject],mfc='none',color='k')
            print '{0} - {1}'.format(subject[inds],xLabels[indc])
            print np.mean(deltaHeadAngle[inds])
            
    plt.axhline(0,color='0.5',ls='--')
    extraplots.boxoff(ax3)
    plt.xlim([-1,5])
    plt.ylabel('Change in head angle (deg)')
    
    #leftDeltaHeadAngle = allDeltaHeadAngle[stimSide=='left']
    #rightDeltaHeadAngle = allDeltaHeadAngle[stimSide=='right']

    
    #import pandas as pd
    #pd.set_option('display.width', 1000)
    #haData=pd.DataFrame(dict(haFile))
    #haData.pivot_table(values='deltaAngleEachTrial', index=['subject','stimSide'], columns='stimRegion')

    '''
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
    '''
    

plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

