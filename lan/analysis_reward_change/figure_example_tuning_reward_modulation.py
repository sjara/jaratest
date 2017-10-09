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
FIGNAME = 'tuning_reward_change'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

soundColor = cp.TangoPalette['Butter2']
timeRange = [-0.3,0.5]
colormapTuning = matplotlib.cm.winter 

# -- Select example cells here -- #
'''
exampleModulatedSoundAstr = 'lowfreq_adap015_2016-03-18_T3_c9'
exampleModulatedSoundAc = 'lowfreq_gosi004_2017-03-03_T6_c3'
exampleModulatedSoundAc2 = 'lowfreq_gosi004_2017-03-18_T6_c10'
exampleModulatedMovementAStr = 'highfreq_adap012_2016-02-04_T3_c3'
exampleModulatedMovementAc = 'highfreq_gosi008_2017-03-14_T7_c8'
                 'lowfreq_gosi004_2017-03-03_T6_c3',  # Locked to SoundOn AC
                 'lowfreq_gosi004_2017-03-18_T6_c10', # Locked to SoundOn AC
                 'highfreq_adap012_2016-02-04_T3_c3', # Locked to CenterOut AStr
                 'highfreq_gosi008_2017-03-14_T7_c8', # Locked to CenterOut AC
'''
infoEachCell = []
infoEachCell.append({ 'soundFreq':'lowfreq', 'cellName':'adap015_2016-03-18_T3_c9',
                      'alignment':'sound', 'brainRegion':'astr' })
infoEachCell.append({ 'soundFreq':'lowfreq', 'cellName':'gosi004_2017-03-03_T6_c3',
                      'alignment':'sound', 'brainRegion':'ac' })
infoEachCell.append({ 'soundFreq':'lowfreq', 'cellName':'gosi004_2017-03-18_T6_c10',
                      'alignment':'sound', 'brainRegion':'ac' })
infoEachCell.append({ 'soundFreq':'highfreq', 'cellName':'adap012_2016-02-04_T3_c3',
                      'alignment':'center-out', 'brainRegion':'astr' })
infoEachCell.append({ 'soundFreq':'highfreq', 'cellName':'gosi008_2017-03-14_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac' })


if len(sys.argv)>1:
    cellInd = int(sys.argv[1])
    cellsToPlot = [infoEachCell[cellInd]]
else:
    cellsToPlot = infoEachCell

#print cellsToPlot
#sys.exit()
'''
# -- Here is where we can select just one cell to plot -- #
plotAll = False

if not plotAll:
    examplesDict = {'sound': {'astr': [exampleModulatedSoundAstr]}}
    #examplesDict = {'center-out': {'astr': [exampleModulatedMovementAstr]}}
else:
    examplesDict = {'sound': {'astr': [exampleModulatedSoundAstr],
                              'ac': [exampleModulatedSoundAc,
                                     exampleModulatedSoundAc2]},
                   'center-out': {'astr': [exampleModulatedMovementAStr],
                                  'ac': [exampleModulatedMovementAc]}
                   }
###########################################################
'''

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


#for alignment in examplesDict.keys():
#    for brainRegion in examplesDict[alignment].keys():
#        for indc, cell in enumerate(examplesDict[alignment][brainRegion]):

for indc, cellInfo in enumerate(cellsToPlot):
    cellName = cellInfo['cellName']
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')
    figFilename = 'example_tuning_{}'.format(cellName)
    rasterFilename = 'example_tuning_raster_{}.npz'.format(cellName) 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample = np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    colorEachFreq = [colormapTuning(x) for x in np.linspace(1.0, 0.2, len(possibleFreq))] 

    ax1 = plt.subplot(gs[0:3, :])
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachFreq,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)
    plt.setp(hcond,zorder=3)
    plt.gca().set_xticklabels('')
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) #, labelpad=labelDis)
    plt.xlim(timeRange[0],timeRange[1])
 
    ax2 = plt.subplot(gs[3, :])
    psthFilename = 'example_tuning_psth_{}.npz'.format(cellName) 
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachFreq']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    timeRange = psthExample['timeRange']
    possibleFreq = psthExample['possibleFreq']
    numFreqs = len(possibleFreq)
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,
                                 trialsEachCond=trialsEachCond,colorEachCond=colorEachFreq,
                                 linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    #yLims = [0,50]
    yLims = plt.ylim()
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    #plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRange)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())

    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
               frameon=False, labelspacing=0, borderaxespad=0)
    plt.suptitle('tuning 50dB chords\n{}'.format(cellName))
    plt.show()
    if SAVE_FIGURE:
        extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

