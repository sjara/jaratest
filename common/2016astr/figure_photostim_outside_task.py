'''
Create figure about photostimulation outside the task.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
import figparams
reload(figparams)

FIGNAME = 'photostim_outside_task'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_outside_task' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,5]

maxSamplesToInclude = 10
print 'Including only {0} or less samples per animal'.format(maxSamplesToInclude)

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

#labelPosX = [0.2, 0.4, 0.65]   # Horiz position for panel labels
#labelPosY = [0.9]    # Vert position for panel labels
labelPosX = [0.07, 0.36, 0.7]   # Horiz position for panel labels
labelPosY = [0.9, 0.48]    # Vert position for panel labels

STIM_DURATION = 1.5 # HARDCODED (in seconds)

laserColor = figparams.colp['blueLaser']
backStrColor = figparams.colp['backStrColor']
frontStrColor = figparams.colp['frontStrColor']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.12, right=0.95, wspace=.1, hspace=0.3)
gsC = gridspec.GridSpec(2, 3) # Another one is needed to adjust panel C
gsC.update(left=0.18, right=0.95, wspace=.1, hspace=0.3)

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
    
    yLims = np.array([-3,3])
    xbar = (stimSamples[1]-stimSamples[0]) / STIM_DURATION
    ybar = 45 * (np.pi/180)  # From degrees to radians
    stimYpos = 2.8
    lineWidth = 2.5
    
    plt.axes(ax1)
    plt.hold(True)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=lineWidth, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=lineWidth, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=6,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Left', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels)
    plt.ylim(yLims)
    extraplots.scalebar(10,-2,xbar,ybar,'1 s','45 deg',fontsize=12)
    plt.axis('off')
    
    plt.axes(ax2)
    plt.hold(True)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='frontStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=lineWidth, color=frontStrColor)
    thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='backStr'))[0]
    plt.plot(headAngleEachCond[thisCond],'-',lw=lineWidth, color=backStrColor)
    plt.plot(stimSamples,2*[stimYpos],lw=6,color=laserColor,clip_on=False)
    plt.text(np.mean(stimSamples),stimYpos+0.2, 'Right', ha='center',va='bottom', clip_on=False, fontsize=fontSizeLabels)
    plt.ylim(yLims)
    plt.axis('off')
    leg = plt.legend(['Anterior str.','Posterior str.'], loc='lower center', frameon=False,
                     labelspacing=0.2, fontsize=14)
    leg.set_frame_on(False)


# -- Panel: Summary of change in head angle --
ax3 = plt.subplot(gsC[1,1:])
ax3.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
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
    eachCond = [stimFrontLeft, stimBackLeft, stimFrontRight, stimBackRight]
    
    xPos = np.array([0, 1, 2.5, 3.5])
    colorEachCond = [frontStrColor,backStrColor,frontStrColor,backStrColor]
    markerEachCond = ['o','o','o','o']
    
    #subjectsEachCond = [np.unique(np.array(subject)[cond] for cond in eachCond)]
    #subjectsFrontStr = np.unique(np.array(subject)[stimRegion=='frontStr'])
    #subjectsBackStr = np.unique(np.array(subject)[stimRegion=='backStr'])
    meanEachCondEachSubject = [[],[],[],[]]
    plt.hold(1)
    plt.axhline(0,color='0.5',ls='--')
    for indc, sessionsThisCond in enumerate(eachCond):
        subjectsThisCond = np.unique(np.array(subject)[sessionsThisCond])
        colorThisCond = colorEachCond[indc]
        markerThisCond = markerEachCond[indc]
        for indSubject, oneSubject in enumerate(subjectsThisCond):
            sessionsThisSubject = sessionsThisCond & (subject==oneSubject)
            samples = (180/np.pi) * np.concatenate(deltaHeadAngle[sessionsThisSubject])# From radians to degrees
            samples = samples[:maxSamplesToInclude]
            xvals = np.tile(xPos[indc]+0.1*indSubject-0.2,len(samples))
            plt.plot(xvals,samples,'o',marker=markerEachSubject[indSubject],mfc='none',mec='0.75', zorder=-1,clip_on=False)
            meanVal = np.mean(samples)
            seVal = np.std(samples)/np.sqrt(len(samples))
            meanEachCondEachSubject[indc].append(meanVal)
            #[pline,pcap,pbar] = plt.errorbar(xPos[indc]+0.1*indSubject-0.2, meanVal, seVal, color=colorThisCond)
            pmark = plt.plot(xPos[indc]+0.1*indSubject-0.2, meanVal,markerThisCond,mfc=colorThisCond,mec='None')
    extraplots.boxoff(ax3)
    plt.ylabel('Change in angle (deg)')
    ax3.set_yticks(np.arange(-200,300,100))
    #plt.ylim([-200,200])
    plt.ylim(300*np.array([-1,1]))
    plt.xlim([-0.7,4.5])
    ax3.axes.get_xaxis().set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    signifYpos = 300 #220
    extraplots.significance_stars([xPos[0],xPos[1]], signifYpos, 20, starSize=8, gapFactor=0.2)
    extraplots.significance_stars([xPos[2],xPos[3]], signifYpos, 20, starSize=8, gapFactor=0.2)
    plt.text(np.mean(xPos[0:2]), -signifYpos, 'Left', ha='center', fontsize=fontSizeLabels+2)
    plt.text(np.mean(xPos[2:4]), -signifYpos, 'Right', ha='center', fontsize=fontSizeLabels+2)
    plt.show()

    
    # -- Statistics --
    (st,pval) = stats.ranksums(meanEachCondEachSubject[0],meanEachCondEachSubject[1])
    print 'Comparison LEFT front vs back: p = {0:0.3}'.format(pval)
    (st,pval) = stats.ranksums(meanEachCondEachSubject[2],meanEachCondEachSubject[3])
    print 'Comparison RIGHT front vs back: p = {0:0.3}'.format(pval)
    (st,pval) = stats.ranksums(meanEachCondEachSubject[0],meanEachCondEachSubject[3])
    print 'Comparison FRONT left vs right: p = {0:0.3}'.format(pval)
    (st,pval) = stats.ranksums(meanEachCondEachSubject[1],meanEachCondEachSubject[3])
    print 'Comparison BACK left vs right: p = {0:0.3}'.format(pval)
    
    
    '''
    for indc, oneCond in enumerate(eachCond):
        for inds in np.flatnonzero(oneCond):
            indSubject = np.flatnonzero(possibleSubjects==subject[inds])[0]
            thisMarker = markerEachSubject[indSubject]
            nSamples = len(deltaHeadAngle[inds])
            xvals = np.tile(xPos[indc]+0.1*indSubject,nSamples)
            yvals = (180/np.pi) * deltaHeadAngle[inds] # From radians to degrees
            plt.plot(xvals,yvals,'o',marker=markerEachSubject[indSubject],mfc='none',color='k')
            print '{0} - {1}'.format(subject[inds],xLabels[indc])
            print np.mean(deltaHeadAngle[inds])
    plt.axhline(0,color='0.5',ls='--')
    extraplots.boxoff(ax3)
    plt.xlim([-1,5])
    plt.ylabel('Change in head angle (deg)')
    '''

    
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
    



if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

