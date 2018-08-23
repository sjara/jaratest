'''
Create figure about the activity of astr neurons during sound being modulated by reward expectation in the reward change task.
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

FIGNAME = 'reward_modulation_sound'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

colorsDict = {'colorLMore':figparams.colp['MoreRewardL'], 
              'colorRMore':figparams.colp['MoreRewardR']} 

soundColor = figparams.colp['sound']
timeRangeToPlot = [-0.2,0.3]

# -- Select example cells here -- #
#exampleModulatedAStr = 'lowfreq_adap017_2016-04-24_T6_c11'
exampleModulatedAStr = 'highfreq_adap012_2016-04-05_T4_c6'
exampleModulatedAC = 'lowfreq_gosi004_2017-03-19_T6_c4'
exampleNonModulatedAStr = 'highfreq_adap017_2016-04-06_T4_c3'
exampleNonModulatedAC = 'lowfreq_gosi004_2017-03-15_T6_c4'
###############################################################


PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_reward_modulation_sound'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,10]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1

labelPosX = [0.015, 0.5]   # Horiz position for panel labels
labelPosY = [0.97, 0.6, 0.2]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#gs = gridspec.GridSpec(2, 3)
gs = gridspec.GridSpec(5, 2)
gs.update(left=0.13, right=0.93, top=0.98, bottom=0.06, wspace=0.5, hspace=0.6)

gs00 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[0:2,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[0:2,1], hspace=0.15)
#gs02 = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[4,:], hspace=0.5)
gs03 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[2:4,0], hspace=0.15)
gs04 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[2:4,1], hspace=0.15)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


# -- Panel A: reward modulated cell during sound in AStr -- #
ax1 = plt.subplot(gs00[0:2, :])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    intDataFilename = 'example_rc_soundaligned_{}.npz'.format(exampleModulatedAC)
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

    
    movementTimesFromEventOnset = intData['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    plt.text(-0.1, yLims[-1]+5, 'AC')
    #ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)

    ax2 = plt.subplot(gs00[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,
        timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,35]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    #plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
    #       frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

# -- Panel B: reward modulated cell during sound in AC -- #
ax3 = plt.subplot(gs01[0:2, :])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_soundaligned_{}.npz'.format(exampleModulatedAStr)
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

    movementTimesFromEventOnset = intData['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    plt.text(-0.1, yLims[-1]+5, 'AStr')

    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax4 = plt.subplot(gs01[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,35]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Panel C: summary distribution of reward modulation index during sound -- #
if PANELS[2]:
    ax6 = plt.subplot(gs[4,0])
    ax6.annotate('E', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

    summaryFilename = 'summary_reward_modulation_sound_rightAC.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    soundRespAC = summary['soundResponsive']
    sigModIAC = summary['sigModI']
    nonsigModIAC = summary['nonsigModI']
    allModIAC = summary['allModI']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAC,nonsigModIAC], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIAC)/float(len(allModIAC))
    plt.text(0.5,yPosText,'AC\nn={}'.format(len(allModIAC)),ha='center',fontsize=fontSizeLabels)
  
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Reward modulation index\n(sound period)', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of sound responsive good cells is:', sum(soundRespAC), '\nNumber of cells significantly modulated is:', len(sigModIAC)
    (Z, pVal) = stats.wilcoxon(allModIAC)
    print 'For AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAC), pVal)
    (Z, pVal) = stats.wilcoxon(sigModIAC)
    print 'For significantly modulated cells in AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution to zero yielded a p value of {:.3f}'.format(np.mean(sigModIAC), pVal)
    
    #ax7 = plt.subplot(gs02[:,1])
    ax7 = plt.subplot(gs[4,1])
    ax7.annotate('F', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

    summaryFilename = 'summary_reward_modulation_sound_rightAStr.npz'
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    soundRespAStr = summary['soundResponsive']
    sigModIAStr = summary['sigModI']
    nonsigModIAStr = summary['nonsigModI']
    allModIAStr = summary['allModI']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIAStr,nonsigModIAStr], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIAStr)/float(len(allModIAStr))
    plt.text(0.5,yPosText,'AStr\nn={}'.format(len(allModIAStr)),ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Reward modulation index\n(sound period)', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of sound responsive good cells is:', sum(soundRespAStr), '\nNumber of cells significantly modulated is:', len(sigModIAStr)
    (Z, pVal) = stats.wilcoxon(allModIAStr)
    print 'For AStr: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIAStr), pVal)
    (Z, pVal) = stats.wilcoxon(sigModIAStr)
    print 'For significantly modulated cells in AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution to zero yielded a p value of {:.3f}'.format(np.mean(sigModIAC), pVal)
    
    (Z, pValBtAreas) = stats.ranksums(allModIAC, allModIAStr)
    print 'Using wilcoxon rank sum test to compare modulation indices between AC and AStr, p value is {:.3f}'.format(pValBtAreas)
    #(oddRatio, pValFisher) = stats.fisher_exact([[sum(soundRespAC)-len(sigModIAC), len(sigModIAC)],[sum(soundRespAStr)-len(sigModIAStr), len(sigModIAStr)]])
    #print 'Using Fishers exact test to compare fraction of modulated cells between AC and AStr, p value is {:.3f}'.format(pValFisher)

# -- Cells that are not modulated by reward -- #
ax8 = plt.subplot(gs03[0:2, :])
ax8.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_soundaligned_{}.npz'.format(exampleNonModulatedAC)
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

    movementTimesFromEventOnset = intData['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    #plt.text(-0.1, yLims[-1]+5, 'AC')

    ax8.set_yticklabels([])
    ax8.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax9 = plt.subplot(gs03[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,60]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    #plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
    #       frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

ax10 = plt.subplot(gs04[0:2, :])
ax10.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_soundaligned_{}.npz'.format(exampleNonModulatedAStr)
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

    movementTimesFromEventOnset = intData['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]*1.05], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    #plt.text(-0.1, yLims[-1]+5, 'AStr')

    ax10.set_yticklabels([])
    ax10.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax11 = plt.subplot(gs04[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,85]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
