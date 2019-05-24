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
exampleMovSelAStr = ['adap005_2015-12-24_T6_c8',
                     'adap013_2016-03-30_T8_c5',
                     'adap012_2016-03-29_T4_c11',
                     'adap017_2016-04-21_T1_c7']

exampleMovSelAC = ['gosi004_2017-02-25_T1_c8',
                   'gosi004_2017-02-13_T7_c8',
                   'gosi008_2017-03-10_T1_c10',
                   'gosi004_2017-03-07_T7_c10']
###############################################################
numRws = max(len(exampleMovSelAC), len(exampleMovSelAStr))

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_movement_selectivity_examples'
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,12]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

labelPosX = [0.012, 0.53]   # Horiz position for panel labels
labelPosY = [0.95, 0.3]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gsMain = gridspec.GridSpec(numRws, 2)
gsMain.update(left=0.1, right=0.97, top=0.97, bottom=0.06, wspace=0.5, hspace=0.5)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


for ind, example in enumerate(exampleMovSelAC):
    gs = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gsMain[ind,0], hspace=0.3)

    ax1 = plt.subplot(gs[0:2, :])

    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(example)
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
    #extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1, clip_on=True)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='red')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[1.05*yLims[-1]], widths=[yLims[-1]*0.04])
    plt.autoscale(enable=True, axis='y', tight=True)
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1, clip_on=True)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='red')
    #plt.text(0, yLims[-1]+5, 'AC', fontsize=fontSizeLabels)

    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.set_ylabel('Trials grouped by\nchoice direction', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca(), keep='none')

    ax2 = plt.subplot(gs[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    # yLims = [0,35]
    # #soundBarHeight = 0.1*yLims[-1]
    # #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    # plt.ylim(yLims)
    # plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks([], [])
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    #plt.text(0.2, yLims[-1]+5, 'AStr')
    #ax2.set_title('Correct trials', fontsize=fontSizeLabels)
    #plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    # plt.text(-0.1, 0.85*yLims[-1], 'AC', fontweight='normal', ha='center', fontsize=fontSizeTicks)
    # plt.text(-0.1, 0.6*yLims[-1], 'correct\ntrials', fontweight='normal', ha='center', va='center', fontsize=fontSizeTicks-2)
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.1,
        frameon=False, handletextpad=0.5, labelspacing=0, borderaxespad=0)

    trialsEachCond = intData['trialsEachCond'][:,2:]
    numErrorTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numErrorTrials))
    colorEachCond = intData['colorEachCond'][2:]
    
    ax = plt.subplot(gs[3, :])
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    #ax.set_title('Error trials', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    # yLims = [0,35]
    # plt.ylim(yLims)
    # plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    
    # plt.text(-0.1, 0.85*yLims[-1], 'AC', fontweight='normal', ha='center', fontsize=fontSizeTicks)
    # plt.text(-0.1, 0.6*yLims[-1], 'error\ntrials', fontweight='normal', ha='center', va='center', fontsize=fontSizeTicks-2)
    # plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.1,
    #       frameon=False, handletextpad=0.5, labelspacing=0, borderaxespad=0)

    extraplots.boxoff(plt.gca())

for ind, example in enumerate(exampleMovSelAStr):
    gs = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gsMain[ind,1], hspace=0.3)

    ax1 = plt.subplot(gs[0:2, :])

    intDataFilename = 'example_rc_movement_sel_{}.npz'.format(example)
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
    #extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1, clip_on=True)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='red')

    sideInTimesFromEventOnset = intData['sideInTimesFromEventOnset']
    plt.hold('on')
    bplot = plt.boxplot(sideInTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[1.05*yLims[-1]], widths=[yLims[-1]*0.04])
    plt.autoscale(enable=True, axis='y', tight=True)
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1, clip_on=True)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='red')
    #plt.text(0, yLims[-1]+5, 'AC', fontsize=fontSizeLabels)

    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.set_ylabel('Trials grouped by\nchoice direction', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca(), keep='none')

    ax2 = plt.subplot(gs[2, :])
    condLabels = intData['condLabels']
    spikeCountMat = intData['spikeCountMat']
    timeVec = intData['timeVec']
    binWidth = intData['binWidth']
    
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    # yLims = [0,35]
    # #soundBarHeight = 0.1*yLims[-1]
    # #plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    # plt.ylim(yLims)
    # plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks([], [])
    #plt.xticks(np.arange(-0.2,0.6,0.2))
    #plt.text(0.2, yLims[-1]+5, 'AStr')
    #ax2.set_title('Correct trials', fontsize=fontSizeLabels)
    #plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    # plt.text(-0.1, 0.85*yLims[-1], 'AStr', fontweight='normal', ha='center', fontsize=fontSizeTicks)
    # plt.text(-0.1, 0.6*yLims[-1], 'correct\ntrials', fontweight='normal', ha='center', va='center', fontsize=fontSizeTicks-2)
    # plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.1,
    #       frameon=False, handletextpad=0.5, labelspacing=0, borderaxespad=0)

    trialsEachCond = intData['trialsEachCond'][:,2:]
    numErrorTrials = trialsEachCond.sum()
    print('Number of correct trials: {}'.format(numErrorTrials))
    colorEachCond = intData['colorEachCond'][2:]
    
    ax = plt.subplot(gs[3, :])
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec,
        trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,
        linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    #ax.set_title('Error trials', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    # yLims = [0,35]
    # plt.ylim(yLims)
    # plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels,labelpad=labelDis)
    
    # plt.text(-0.1, 0.85*yLims[-1], 'AStr', fontweight='normal', ha='center', fontsize=fontSizeTicks)
    # plt.text(-0.1, 0.6*yLims[-1], 'error\ntrials', fontweight='normal', ha='center', va='center', fontsize=fontSizeTicks-2)
    # plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.1,
    #       frameon=False, handletextpad=0.5, labelspacing=0, borderaxespad=0)

    extraplots.boxoff(plt.gca())


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
