'''
Create figure about the activity of astr neurons during movement being modulated by reward expectation in the reward change task.
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

FIGNAME = 'reward_modulation_movement'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

colorsDict = {'colorLMore':figparams.colp['MoreRewardL'], 
              'colorRMore':figparams.colp['MoreRewardR']} 

soundColor = figparams.colp['sound']
timeRangeToPlot = [-0.2,0.5]
removeSideIn = True
modWindow = '0-0.3s'
controlForSound = True

# -- Select example cells here -- #
#exampleModulatedAStr = 
exampleModulatedAStr = 'highfreq_adap012_2016-02-04_T3_c3'
exampleModulatedAC = 'highfreq_gosi008_2017-03-14_T7_c8'
exampleNonModulatedAStr = 'highfreq_adap017_2016-04-06_T7_c12'
exampleNonModulatedAC = 'highfreq_gosi004_2017-03-07_T7_c10'
###############################################################

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_reward_modulation_movement'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [5,10]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1

labelPosX = [0.015, 0.5]   # Horiz position for panel labels
labelPosY = [0.97, 0.58, 0.2]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(5, 2)
gs.update(left=0.15, right=0.96, top=0.98, bottom=0.06, wspace=0.55, hspace=0.5)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[0:2,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[0:2,1], hspace=0.15)
#gs02 = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[4,:], hspace=0.5)
gs03 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[2:4,0], hspace=0.15)
gs04 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[2:4,1], hspace=0.15)

msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


# -- Panel A: reward modulated cell during center-out in AStr -- #
ax1 = plt.subplot(gs00[0:3, :])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    intDataFilename = 'example_rc_center-outaligned_{}.npz'.format(exampleModulatedAC)
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

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    plt.text(0, yLims[-1]+5, 'AC')
    
    #ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)

    ax2 = plt.subplot(gs00[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,35]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

# -- Panel B: reward modulated cell during center-out in AC -- #
ax3 = plt.subplot(gs01[0:3, :])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_center-outaligned_{}.npz'.format(exampleModulatedAStr)
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

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    plt.text(0, yLims[-1]+5, 'AStr')

    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax4 = plt.subplot(gs01[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,23]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    #plt.legend(condLabels[0:2], loc='best', fontsize=fontSizeTicks, handlelength=0.2,
    #       frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Panel C: summary distribution of reward modulation index during movement -- #
if PANELS[2]:
    ax6 = plt.subplot(gs[4,0])
    ax6.annotate('E', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    if removeSideIn:
        summaryFilename = 'summary_reward_modulation_movement_rightAC_{}_win_removed_sidein_trials.npz'.format(modWindow)
    else:
        summaryFilename = 'summary_reward_modulation_movement_rightAC_{}_win.npz'.format(modWindow)
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    movementSelAC = summary['movementSelective']
    encodeMv = summary['encodeMv']
    encodeSd = summary['encodeSd']
    sigModIAC = summary['sigModI']
    nonsigModIAC = summary['nonsigModI']
    allModIAC = summary['allModI']
    sigModIEncodeMvAC = summary['sigModIEncodeMv'] 
    nonsigModIEncodeMvAC = summary['nonsigModIEncodeMv'] 
    allModIEncodeMvAC = summary['allModIEncodeMv']
    sigModIEncodeSdAC = summary['sigModIEncodeSd'] 
    nonsigModIEncodeSdAC = summary['nonsigModIEncodeSd'] 
    allModIEncodeSdAC = summary['allModIEncodeSd']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIEncodeMvAC,nonsigModIEncodeMvAC], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIEncodeMvAC)/float(len(allModIEncodeMvAC))
    plt.text(0.5,yPosText,'AC\nn={}\n{:.2f}% modulated'.format(len(allModIEncodeMvAC), percentSelective),ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Reward modulation index\n(movement period)', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Sound encoding 'movement-selective' cells -- #
    percentSelective = 100*len(sigModIEncodeSdAC)/float(len(allModIEncodeSdAC))
    print('AC movement-selective cells that encode sound\nn={}\n{:.2f}% modulated'.format(len(allModIEncodeSdAC), percentSelective))

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of movement selective good cells is:', sum(movementSelAC&encodeMv), '\nNumber of cells significantly modulated is:', len(sigModIEncodeMvAC)
    (Z, pVal) = stats.wilcoxon(allModIEncodeMvAC)
    print 'For AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIEncodeMvAC), pVal)
    (Z, pVal) = stats.wilcoxon(sigModIEncodeMvAC)
    print 'For significantly modulated cells in AStr: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution to zero yielded a p value of {:.3f}'.format(np.mean(sigModIEncodeMvAC), pVal)
    

    ax7 = plt.subplot(gs[4,1])
    ax7.annotate('F', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    if removeSideIn:
        summaryFilename = 'summary_reward_modulation_movement_rightAStr_{}_win_removed_sidein_trials.npz'.format(modWindow)
    else:
        summaryFilename = 'summary_reward_modulation_movement_rightAStr_{}_win.npz'.format(modWindow)
    
    summaryFullPath = os.path.join(dataDir, summaryFilename)
    summary = np.load(summaryFullPath)
    movementSelAStr = summary['movementSelective']
    sigModIAStr = summary['sigModI']
    nonsigModIAStr = summary['nonsigModI']
    allModIAStr = summary['allModI']
    encodeMv = summary['encodeMv']
    encodeSd = summary['encodeSd']
    
    sigModIEncodeMvAStr = summary['sigModIEncodeMv'] 
    nonsigModIEncodeMvAStr = summary['nonsigModIEncodeMv'] 
    allModIEncodeMvAStr = summary['allModIEncodeMv']
    sigModIEncodeSdAStr = summary['sigModIEncodeSd'] 
    nonsigModIEncodeSdAStr = summary['nonsigModIEncodeSd'] 
    allModIEncodeSdAStr = summary['allModIEncodeSd']

    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModIEncodeMvAStr,nonsigModIEncodeMvAStr], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
    yPosText = 0.7*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    percentSelective = 100*len(sigModIEncodeMvAStr)/float(len(allModIEncodeMvAStr))
    plt.text(0.5,yPosText,'AStr\nn={}\n{:.2f}% modulated'.format(len(allModIEncodeMvAStr), percentSelective),ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Reward modulation index\n(movement period)', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Sound encoding 'movement-selective' cells -- #
    percentSelective = 100*len(sigModIEncodeSdAStr)/float(len(allModIEncodeSdAStr))
    print('AStr movement-selective cells that encode sound\nn={}\n{:.2f}% modulated'.format(len(allModIEncodeSdAStr), percentSelective))

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of movement selective good cells is:', sum(movementSelAStr&encodeMv), '\nNumber of cells significantly modulated is:', len(sigModIEncodeMvAStr)
    (Z, pVal) = stats.wilcoxon(allModIEncodeMvAStr)
    print 'For AStr: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(np.mean(allModIEncodeMvAStr), pVal)
    (Z, pVal) = stats.wilcoxon(sigModIEncodeMvAStr)
    print 'For significantly modulated cells in AC: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution to zero yielded a p value of {:.3f}'.format(np.mean(sigModIEncodeMvAStr), pVal)
    
    (Z, pValBtAreas) = stats.ranksums(allModIEncodeMvAC, allModIEncodeMvAStr)
    print 'Using wilcoxon rank sum test to compare modulation indices between AC and AStr, p value is {:.3f}'.format(pValBtAreas)
    #(oddRatio, pValFisher) = stats.fisher_exact([[sum(movementRespAC)-len(sigModIAC), len(sigModIAC)],[sum(movementRespAStr)-len(sigModIAStr), len(sigModIAStr)]])
    #print 'Using Fishers exact test to compare fraction of modulated cells between AC and AStr, p value is {:.3f}'.format(pValFisher)

# -- Cells that are not modulated by reward -- #
ax8 = plt.subplot(gs03[0:3, :])
ax8.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_center-outaligned_{}.npz'.format(exampleNonModulatedAC)
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

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    #plt.text(0.2, yLims[-1]+5, 'AC')

    ax8.set_yticklabels([])
    ax8.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax9 = plt.subplot(gs03[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,15]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    #plt.legend(condLabels[0:2], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           #frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

ax10 = plt.subplot(gs04[0:3, :])
ax10.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    intDataFilename = 'example_rc_center-outaligned_{}.npz'.format(exampleNonModulatedAStr)
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

    soundTimesFromEventOnset = intData['soundTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(soundTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[yLims[-1]*0.04])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    #plt.text(0.2, yLims[-1]+5, 'AStr')

    ax10.set_yticklabels([])
    ax10.set_xticklabels([])
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax11 = plt.subplot(gs04[3, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,60]
    #soundBarHeight = 0.1*yLims[-1]
    #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    #plt.legend(condLabels[0:2], loc='best', fontsize=fontSizeTicks, handlelength=0.2,
    #       frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
