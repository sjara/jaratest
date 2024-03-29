'''
Create raster plot and psth of astr neurons in the reward-change task.
'''
import os, sys
import matplotlib
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import scipy.stats as stats
from jaratoolbox import extraplots
from jaratoolbox import settings
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp

STUDY_NAME = '2017rc'
FIGNAME = 'reward_modulation_movement_selective_cells'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

colorDict = {'leftMoreLowFreq':cp.TangoPalette['SkyBlue2'],
             'rightMoreLowFreq':cp.TangoPalette['Orange2'],
             'sameRewardLowFreq':'y',
             'leftMoreHighFreq':cp.TangoPalette['Orange2'],
             'rightMoreHighFreq':cp.TangoPalette['SkyBlue2'],
             'sameRewardHighFreq':'darkgrey'}

soundColor = cp.TangoPalette['Butter2']
timeRange = [-0.3,0.5]

# -- Select example cells here -- #
infoEachCell = []
infoEachCell.append({ 'cellName':'gosi001_2017-05-06_T3_c5',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi004_2017-02-13_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi004_2017-03-15_T6_c7',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi004_2017-03-18_T3_c4',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi004_2017-04-06_T7_c5',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi008_2017-03-14_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac' })


if len(sys.argv)>1:
    cellInd = int(sys.argv[1])
    cellsToPlot = [infoEachCell[cellInd]]
else:
    cellsToPlot = infoEachCell


SAVE_FIGURE = 1
outputDir = '/tmp/'

figFormat = 'svg' # 'pdf' or 'svg'
figSize = [5,5]

fontSizeLabels = 12 #figparams.fontSizeLabels
fontSizeTicks = 12 #figparams.fontSizeTicks
fontSizePanel = 16 #figparams.fontSizePanel
#labelDis = 0.1

#labelPosX = [0.015, 0.355, 0.68]   # Horiz position for panel labels
#labelPosY = [0.92]    # Vert position for panel labels

gs = gridspec.GridSpec(4, 1)
gs.update(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0.4, hspace=0.15)

#timeRangeSound = [-0.2, 0.4]
msRaster = 4
smoothWinSizePsth = 3
lwPsth = 3
downsampleFactorPsth = 1
#soundFreqsToPlot = ['lowfreq','highfreq']
soundFreqsToPlot = ['highfreq']

#for alignment in examplesDict.keys():
#    for brainRegion in examplesDict[alignment].keys():
#        for indc, cell in enumerate(examplesDict[alignment][brainRegion]):

for indc, cellInfo in enumerate(cellsToPlot):
    alignment = cellInfo['alignment']
    brainRegion = cellInfo['brainRegion']
    cellName = cellInfo['cellName']
    for soundFreq in soundFreqsToPlot:
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')
        figFilename = 'example_rc_{}_{}_{}_{}'.format(alignment, brainRegion, soundFreq, cellName)
        rasterFilename = 'example_rc_{}aligned_raster_{}_{}.npz'.format(alignment, soundFreq, cellName) 
        rasterFullPath = os.path.join(dataDir, rasterFilename)
        rasterExample = np.load(rasterFullPath)

        trialsEachCond = rasterExample['trialsEachCond']
        #colorEachCond = rasterExample['colorEachCond']
        colorEachCond = [colorDict['leftMoreHighFreq'],colorDict['rightMoreHighFreq'],colorDict['leftMoreHighFreq']]
        ####### WARNING!: hardcoded #######

        spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
        indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
        #timeRange = rasterExample['timeRange']
        ax1 = plt.subplot(gs[0:3, :])
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                       indexLimitsEachTrial,
                                                       timeRange=timeRange,
                                                       trialsEachCond=trialsEachCond,
                                                       colorEachCond=colorEachCond,
                                                       fillWidth=None,labels=None)

        plt.setp(pRaster, ms=msRaster)
        #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
        #ax2.axes.xaxis.set_ticklabels([])
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        #plt.ylabel('Trials',fontsize=fontSizeLabels,labelpad=labelDis)
        plt.ylabel('Trials\nby reward size', fontsize=fontSizeLabels)
        #plt.xlim(timeRangeSound[0],timeRangeSound[1])

        ax2 = plt.subplot(gs[3, :])
        psthFilename = 'example_rc_{}aligned_psth_{}_{}.npz'.format(alignment, soundFreq, cellName) 
        psthFullPath = os.path.join(dataDir, psthFilename)
        psthExample =np.load(psthFullPath)

        condLabels = psthExample['condLabels']
        trialsEachCond = psthExample['trialsEachCond']
        #colorEachCond = psthExample['colorEachCond']
        spikeCountMat = psthExample['spikeCountMat']
        timeVec = psthExample['timeVec']
        binWidth = psthExample['binWidth']
        #timeRange = psthExample['timeRange']

        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,
                                     trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,
                                     linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        #yLims = [0,50]
        yLims = plt.ylim()
        plt.yticks(yLims)
        plt.xlim(timeRange)
        plt.xticks(np.arange(-0.2,0.6,0.2))
        #plt.xlabel('Time from {} (s)'.format(alignment),fontsize=fontSizeLabels)
        plt.xlabel('Time from center exit (s)'.format(alignment),fontsize=fontSizeLabels)
        plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
        extraplots.boxoff(plt.gca())

        legLabels = ['LESS reward','MORE reward'] # Or use stored condLabels
        plt.legend(legLabels, loc='upper left', fontsize=fontSizeTicks, handlelength=1.5,
                   frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)
        #plt.suptitle('{}\n{}'.format(figFilename,cellName))
        plt.show()
        if SAVE_FIGURE:
            extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

