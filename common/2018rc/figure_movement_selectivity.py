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

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

colorsDict = {'left': figparams.colp['MoveLeft'],
              'right':figparams.colp['MoveRight']} 

soundColor = figparams.colp['sound']
timeRangeToPlot = [-0.3,0.5]

# -- Select example cells here -- #
exampleMovSelAStr = 'adap005_2015-12-24_T6_c8'
#exampleMovSelAStr = 'adap012_2016-03-09_T3_c2'

exampleMovSelAC = 'gosi008_2017-03-10_T1_c10'
#exampleMovSelAC = 'gosi008_2017-03-07_T1_c4'
###############################################################


PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_movement_selectivity'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [10,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1

labelPosX = [0.015, 0.355, 0.68]   # Horiz position for panel labels
labelPosY = [0.92]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3)
gs.update(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.4, hspace=0.1)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,1], hspace=0.15)
gs02 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[:,2], hspace=0.5)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


# -- Panel A: movement selective cell in AStr -- #
ax1 = plt.subplot(gs00[0:3, :])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(exampleMovSelAStr)
    intDataFullPath = os.path.join(dataDir, intDataFilename)
    intData =np.load(intDataFullPath)

    trialsEachCond = intData['trialsEachCond']
    colorEachCond = intData['colorEachCond']
    spikeTimesFromEventOnset = intData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = intData['indexLimitsEachTrial']
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRangeToPlot,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)

    '''
    movementTimesFromEventOnset = rasterExample['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[5])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    '''
    #ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    plt.ylabel('Trials grouped by\nmovement direction', fontsize=fontSizeLabels)

    ax2 = plt.subplot(gs00[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,6]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

# -- Panel B: movement selective cell in AC -- #
ax3 = plt.subplot(gs01[0:3, :])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(exampleMovSelAC)
    intDataFullPath = os.path.join(dataDir, intDataFilename)
    intData =np.load(intDataFullPath)

    trialsEachCond = intData['trialsEachCond']
    colorEachCond = intData['colorEachCond']
    spikeTimesFromEventOnset = intData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = intData['indexLimitsEachTrial']
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRangeToPlot,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)

    '''
    movementTimesFromEventOnset = rasterExample['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[5])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    '''
    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    plt.ylabel('Trials grouped by\nmovement direction', fontsize=fontSizeLabels)


    ax4 = plt.subplot(gs01[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,20]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Panel C: summary distribution of movement selectivity index -- #
ax6 = plt.subplot(gs02[0,:])
ax6.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[2]:
    summaryFilename = 'summary_rc_movement_selectivity_rightAStr.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    sigModIAStr = summary['sigModI']
    nonsigModIAStr = summary['nonsigModI']
    allModIAStr = summary['allModI']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAStr,nonsigModIAStr], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.9*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'AStr',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Movement selectivity index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of good cells is:', len(allModIAStr), '\nNumber of cells movement selective is:', len(sigModIAStr)
    (Z, pVal) = stats.wilcoxon(allModIAStr)
    print 'For AStr: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAStr), pVal)


    ax7 = plt.subplot(gs02[1,:])
    summaryFilename = 'summary_rc_movement_selectivity_rightAC.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    sigModIAC = summary['sigModI']
    nonsigModIAC = summary['nonsigModI']
    allModIAC = summary['allModI']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAC,nonsigModIAC], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.9*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'AC',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Movement selectivity index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of good cells is:', len(allModIAC), '\nNumber of cells movement selective is:', len(sigModIAC)
    (Z, pVal) = stats.wilcoxon(allModIAC)
    print 'For AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAC), pVal)
    (Z, pValBtAreas) = stats.ranksums(allModIAC, allModIAStr)
    print 'Using wilcoxon rank sum test to compare movement selectivity indices between AC and AStr, p value is {:.3f}'.format(pValBtAreas)
    #(oddRatio, pValFisher) = stats.fisher_exact([[sum(soundRespAC)-len(sigModIAC), len(sigModIAC)],[sum(soundRespAStr)-len(sigModIAStr), len(sigModIAStr)]])
    #print 'Using Fishers exact test to compare fraction of modulated cells between AC and AStr, p value is {:.3f}'.format(pValFisher)
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
