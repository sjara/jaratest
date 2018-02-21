'''
Create figure about the activity of astr neurons during sound being modulated by choice in the psychometric curve task.
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
timeRangeToPlot = [-0.3,0.5]

# -- Select example cells here -- #
exampleModulatedAStr = 'lowfreq_adap017_2016-04-24_T6_c11'
exampleModulatedAC = 'lowfreq_gosi004_2017-03-19_T6_c4'

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_reward_modulation_sound'
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
gs02 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[:,2], hspace=0.4)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1


# -- Panel A: reward modulated cell during sound in AStr -- #
ax1 = plt.subplot(gs00[0:3, :])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
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
    ax1.set_yticklabels([])
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
    yLims = [0,30]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRangeToPlot)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

# -- Panel B: reward modulated cell during sound in AC -- #
ax3 = plt.subplot(gs01[0:3, :])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
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
    plt.ylabel('Trials grouped by\nreward expectation', fontsize=fontSizeLabels)


    ax4 = plt.subplot(gs01[3, :])
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
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Panel C: summary distribution of reward modulation index during sound -- #
ax6 = plt.subplot(gs02[0,:])
ax6.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
maxZThreshold = 3
alphaLevel = 0.05
modWindow = '0-0.1s'
if PANELS[2]:
    dbKey = 'reward_change'
    dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
    celldbPath = os.path.join(dbFolder, 'rc_database.h5')
    celldb = pd.read_hdf(celldbPath, key=dbKey)
    
    brainArea = 'rightAStr'
    goodQualCells = celldb.query("keepAfterDupTest==True and brainArea=='{}'".format(brainArea))

    soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x)) >=  maxZThreshold) #The bigger of the sound Z score is over threshold
    moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[0]) > abs(x[1]))
    moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[1]) > abs(x[0]))
    goodLowFreqRespCells = goodQualCells[moreRespLowFreq]
    goodHighFreqRespCells = goodQualCells[moreRespHighFreq]

    lowFreqModIndName = 'modIndLow_'+modWindow+'_'+'sound'
    lowFreqModSigName = 'modSigLow_'+modWindow+'_'+'sound'
    lowFreqModDirName = 'modDirLow_'+modWindow+'_'+'sound'
    highFreqModIndName = 'modIndHigh_'+modWindow+'_'+'sound'
    highFreqModSigName = 'modSigHigh_'+modWindow+'_'+'sound'
    highFreqModDirName = 'modDirHigh_'+modWindow+'_'+'sound'
            
    goodLowFreqRespModInd = (-1) * goodLowFreqRespCells[lowFreqModIndName]
    goodLowFreqRespModSig = goodLowFreqRespCells[lowFreqModSigName]
    goodLowFreqRespModDir = goodLowFreqRespCells[lowFreqModDirName]
    goodHighFreqRespModInd = goodHighFreqRespCells[highFreqModIndName]
    goodHighFreqRespModSig = goodHighFreqRespCells[highFreqModSigName]
    goodHighFreqRespModDir = goodHighFreqRespCells[highFreqModDirName]
    
    sigModulatedLow = (goodLowFreqRespModSig < alphaLevel) & (goodLowFreqRespModDir > 0)
    sigModulatedHigh = (goodHighFreqRespModSig < alphaLevel) & (goodHighFreqRespModDir > 0)
    sigModI = np.concatenate((goodLowFreqRespModInd[sigModulatedLow].values,
                                      goodHighFreqRespModInd[sigModulatedHigh].values))
    nonsigModI = np.concatenate((goodLowFreqRespModInd[~sigModulatedLow].values,
                                      goodHighFreqRespModInd[~sigModulatedHigh].values))

    allModI = np.concatenate((goodLowFreqRespModInd.values, goodHighFreqRespModInd.values))
    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)

    yPosText = 0.95*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'AStr',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Modulation index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of sound responsive good cells is:', sum(soundResp), '\nNumber of cells significantly modulated is:', len(sigModI)
    (Z, pVal) = stats.wilcoxon(allModI)
    print 'For {}: Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(brainArea, pVal)

    ax7 = plt.subplot(gs02[1,:])
    brainArea = 'rightAC'
    goodQualCells = celldb.query("keepAfterDupTest==True and brainArea=='{}'".format(brainArea))

    soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x)) >=  maxZThreshold) #The bigger of the sound Z score is over threshold
    moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[0]) > abs(x[1]))
    moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[1]) > abs(x[0]))
    goodLowFreqRespCells = goodQualCells[moreRespLowFreq]
    goodHighFreqRespCells = goodQualCells[moreRespHighFreq]

    lowFreqModIndName = 'modIndLow_'+modWindow+'_'+'sound'
    lowFreqModSigName = 'modSigLow_'+modWindow+'_'+'sound'
    lowFreqModDirName = 'modDirLow_'+modWindow+'_'+'sound'
    highFreqModIndName = 'modIndHigh_'+modWindow+'_'+'sound'
    highFreqModSigName = 'modSigHigh_'+modWindow+'_'+'sound'
    highFreqModDirName = 'modDirHigh_'+modWindow+'_'+'sound'
            
    goodLowFreqRespModInd = (-1) * goodLowFreqRespCells[lowFreqModIndName]
    goodLowFreqRespModSig = goodLowFreqRespCells[lowFreqModSigName]
    goodLowFreqRespModDir = goodLowFreqRespCells[lowFreqModDirName]
    goodHighFreqRespModInd = goodHighFreqRespCells[highFreqModIndName]
    goodHighFreqRespModSig = goodHighFreqRespCells[highFreqModSigName]
    goodHighFreqRespModDir = goodHighFreqRespCells[highFreqModDirName]
    
    sigModulatedLow = (goodLowFreqRespModSig < alphaLevel) & (goodLowFreqRespModDir > 0)
    sigModulatedHigh = (goodHighFreqRespModSig < alphaLevel) & (goodHighFreqRespModDir > 0)
    sigModI = np.concatenate((goodLowFreqRespModInd[sigModulatedLow].values,
                                      goodHighFreqRespModInd[sigModulatedHigh].values))
    nonsigModI = np.concatenate((goodLowFreqRespModInd[~sigModulatedLow].values,
                                      goodHighFreqRespModInd[~sigModulatedHigh].values))

    allModI = np.concatenate((goodLowFreqRespModInd.values, goodHighFreqRespModInd.values))
    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)

    yPosText = 0.95*plt.ylim()[1]
    #plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    #plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'AC',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Modulation index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())

    # -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
    print 'Total number of sound responsive good cells is:', sum(soundResp), '\nNumber of cells significantly modulated is:', len(sigModI)
    (Z, pVal) = stats.wilcoxon(allModI)
    print 'For {}: Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(brainArea, pVal)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
