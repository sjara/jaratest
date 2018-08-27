'''
Create figure about the movement direction selective activity of ac and astr neurons  in the reward change task.
'''
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import figparams
reload(figparams)
import matplotlib.patches as mpatches
import scipy.stats as stats

FIGNAME = 'movement_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME
removeSideIn = True

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

colorsDict = {'left': figparams.colp['MoveLeft'],
              'right':figparams.colp['MoveRight']} 

soundColor = figparams.colp['sound']
timeRangeToPlot = [-0.2,0.4]

# -- Select example cells here -- #
#exampleMovSelAStr = 'adap005_2015-12-24_T6_c8'
exampleMovSelAStr = 'adap013_2016-03-30_T8_c5'

#exampleMovSelAC = 'gosi008_2017-03-10_T1_c10'
exampleMovSelAC = 'gosi004_2017-02-13_T7_c8'
###############################################################


PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_movement_selectivity'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

labelPosX = [0.015, 0.355, 0.65]   # Horiz position for panel labels
labelPosY = [0.92]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3)
gs.update(left=0.12, right=0.95, top=0.95, bottom=0.13, wspace=0.7, hspace=0.1)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,0], hspace=0.3)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,1], hspace=0.2)
gs02 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[:,2], hspace=0.5)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


# -- Panel A: movement selective cell in AC -- #
ax1 = plt.subplot(gs00[0:2, :])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(exampleMovSelAC)
    intDataFullPath = os.path.join(dataDir, intDataFilename)
    intData =np.load(intDataFullPath)

    trialsEachCond = intData['trialsEachCond'][:,0:2]
    numCorrectTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numCorrectTrials))
    colorEachCond = intData['colorEachCond'][0:2]
    spikeTimesFromEventOnset = intData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = intData['indexLimitsEachTrial']
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRangeToPlot,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[1.05*yLims[-1]], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[1.05*yLims[-1]], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    plt.text(0, yLims[-1]+5, 'AC', fontsize=fontSizeLabels)

    #ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.set_ylabel('Trials grouped by\nmovement direction', fontsize=fontSizeLabels)

    ax2 = plt.subplot(gs00[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,35]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks([], [])
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    #plt.text(0.2, yLims[-1]+5, 'AStr')
    #ax2.set_title('Correct trials', fontsize=fontSizeLabels)
    #plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('FR\ncorrect\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    extraplots.boxoff(plt.gca())

    trialsEachCond = intData['trialsEachCond'][:,2:]
    numErrorTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numErrorTrials))
    colorEachCond = intData['colorEachCond'][2:]
    ax = plt.subplot(gs00[3, :])
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    #ax.set_title('Error trials', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,35]
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('FR\nerror\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

    extraplots.boxoff(plt.gca())

# -- Panel B: movement selective cell in AStr -- #
ax3 = plt.subplot(gs01[0:2, :])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(exampleMovSelAStr)
    intDataFullPath = os.path.join(dataDir, intDataFilename)
    intData =np.load(intDataFullPath)

    trialsEachCond = intData['trialsEachCond'][:,:2]
    numCorrectTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numCorrectTrials))
    colorEachCond = intData['colorEachCond'][:2]
    spikeTimesFromEventOnset = intData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = intData['indexLimitsEachTrial']
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRangeToPlot,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    plt.text(0, yLims[-1]+5, 'AStr', fontsize=fontSizeLabels)

    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    plt.ylabel('Trials grouped by\nmovement direction', fontsize=fontSizeLabels)


    ax4 = plt.subplot(gs01[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,65]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks([],[])
    #plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('FR\ncorrect\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    trialsEachCond = intData['trialsEachCond'][:,2:]
    numErrorTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numErrorTrials))
    colorEachCond = intData['colorEachCond'][2:]
    ax = plt.subplot(gs01[3, :])
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,65]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('FR\nerror\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())

    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Panel C: summary distribution of movement selectivity index -- #
ax6 = plt.subplot(gs02[0,:])
ax6.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[2]:
    if removeSideIn:
        summaryFilename = 'summary_rc_movement_selectivity_rightAC_removed_sidein_trials.npz'
    else:
        summaryFilename = 'summary_rc_movement_selectivity_rightAC.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    sigModIAC = -(summary['sigModI']) # Inverting the sign of movement selectivity index
    nonsigModIAC = -(summary['nonsigModI']) # Inverting the sign of movement selectivity index
    allModIAC = -(summary['allModI'])
    
    sigModIEncodeMvAC = -(summary['sigModIEncodeMv']) # Inverting the sign of movement selectivity index
    nonsigModIEncodeMvAC = -(summary['nonsigModIEncodeMv']) # Inverting the sign of movement selectivity index
    allModIEncodeMvAC = -(summary['allModIEncodeMv'])
    
    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAC,nonsigModIAC], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIAC)/float(len(allModIAC))
    plt.text(0.5,yPosText,'AC\nn={}'.format(len(allModIAC)),ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    #plt.xlabel('Movement selectivity index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of good cells is:', len(allModIAC), '\nNumber of cells movement selective is:', len(sigModIAC)
    (Z, pVal) = stats.wilcoxon(allModIAC)
    print 'For AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAC), pVal)


    ax7 = plt.subplot(gs02[1,:])
    if removeSideIn:
        summaryFilename = 'summary_rc_movement_selectivity_rightAStr_removed_sidein_trials.npz'
    else:
        summaryFilename = 'summary_rc_movement_selectivity_rightAStr.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    sigModIAStr = -(summary['sigModI'])
    nonsigModIAStr = -(summary['nonsigModI'])
    allModIAStr = -(summary['allModI'])
    sigModIEncodeMvAStr = -(summary['sigModIEncodeMv']) # Inverting the sign of movement selectivity index
    nonsigModIEncodeMvAStr = -(summary['nonsigModIEncodeMv']) # Inverting the sign of movement selectivity index
    allModIEncodeMvAStr = -(summary['allModIEncodeMv'])

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAStr,nonsigModIAStr], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIAStr)/float(len(allModIAStr))
    plt.text(0.5,yPosText,'AStr\nn={}'.format(len(allModIAStr)),ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Movement selectivity index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of good cells is:', len(allModIAStr), '\nNumber of cells movement selective is:', len(sigModIAStr)
    (Z, pVal) = stats.wilcoxon(allModIAStr)
    print 'For AStr: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAStr), pVal)
    (Z, pValBtAreas) = stats.ranksums(allModIAC, allModIAStr)
    print 'Using wilcoxon rank sum test to compare movement selectivity indices between AC and AStr, p value is {:.3f}'.format(pValBtAreas)
    #(oddRatio, pValFisher) = stats.fisher_exact([[sum(soundRespAC)-len(sigModIAC), len(sigModIAC)],[sum(soundRespAStr)-len(sigModIAStr), len(sigModIAStr)]])
    #print 'Using Fishers exact test to compare fraction of modulated cells between AC and AStr, p value is {:.3f}'.format(pValFisher)


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()