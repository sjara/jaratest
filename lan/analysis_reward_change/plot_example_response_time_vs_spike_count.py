import os, sys
import matplotlib
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import scipy.stats as stats
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratest.lan.analysis_reward_change import plot_reward_change_behavior as behavPlot
reload(behavPlot)
import scipy.stats as stats

STUDY_NAME = '2017rc'
FIGNAME = 'reward_modulation_movement_selective_cells'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

colorDict = {'leftMoreLowFreq':cp.TangoPalette['SkyBlue2'],
             'rightMoreLowFreq':cp.TangoPalette['Orange2'],
             'sameRewardLowFreq':'y',
             'leftMoreHighFreq':'r',
             'rightMoreHighFreq':'b',
             'sameRewardHighFreq':'darkgrey'}

soundColor = cp.TangoPalette['Butter2']
timeRange = [-0.3,0.5]

# -- Select example cells here -- #
infoEachCell = []
infoEachCell.append({ 'cellName':'gosi001_2017-05-06_T3_c5',
                      'alignment':'center-out', 'brainRegion':'ac',
                      'behavSession':'20170506a'})
infoEachCell.append({ 'cellName':'gosi004_2017-02-13_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac',
                      'behavSession': '20170213a'})
infoEachCell.append({ 'cellName':'gosi008_2017-03-14_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac', 
                      'behavSession': '20170314a'})


if len(sys.argv)>1:
    cellInd = int(sys.argv[1])
    cellsToPlot = [infoEachCell[cellInd]]
else:
    cellsToPlot = infoEachCell


SAVE_FIGURE = 1
outputDir = '/tmp/'
soundFreqsToPlot = ['lowfreq','highfreq']
movementTimeRange = [0.05,0.25]

figFormat = 'svg' # 'pdf' or 'svg'
figSize = [5,15]

fontSizeLabels = 12 #figparams.fontSizeLabels
fontSizeTicks = 12 #figparams.fontSizeTicks
fontSizePanel = 16 #figparams.fontSizePanel

gs = gridspec.GridSpec(3, 1)
gs.update(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0.2, hspace=0.4)

for indc, cellInfo in enumerate(cellsToPlot):
    alignment = cellInfo['alignment']
    brainRegion = cellInfo['brainRegion']
    cellName = cellInfo['cellName']
    animal = cellName.split('_')[0]
    date = cellName.split('_')[1]
    
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')
    figFilename = 'rt_fr_{}_{}'.format(alignment, cellName)

    for inds, soundFreq in enumerate(soundFreqsToPlot):
        rasterFilename = 'example_rc_{}aligned_raster_{}_{}.npz'.format(alignment, soundFreq, cellName) 
        rasterFullPath = os.path.join(dataDir, rasterFilename)
        rasterExample = np.load(rasterFullPath)
        
        spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
        indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
        trialsEachCond = rasterExample['trialsEachCond']
        labelEachCond = rasterExample['condLabels']
        spikeCountEachTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,movementTimeRange).flatten()

        behavSumFilename = 'behavior_times_{}_{}_{}.npz'.format(soundFreq, animal, date)
        behavSumFullPath = os.path.join(dataDir,behavSumFilename)
        behavSum = np.load(behavSumFullPath)
        leftMoreTrialsOneFreq = behavSum['leftMoreTrials']
        rightMoreTrialsOneFreq = behavSum['rightMoreTrials']
        responseTimes = behavSum['responseTimes']

        #plt.subplot(3,1,inds+1)
        ax = plt.subplot(gs[inds, :])
        jitter = 1 * (np.random.rand(len(spikeCountEachTrial[leftMoreTrialsOneFreq]))-0.5) 
        plt.scatter(responseTimes[leftMoreTrialsOneFreq], spikeCountEachTrial[leftMoreTrialsOneFreq]+jitter, edgecolor='blue', facecolor='None', label='left_more_reward')
        jitter = 1 * (np.random.rand(len(spikeCountEachTrial[rightMoreTrialsOneFreq]))-0.5)
        plt.scatter(responseTimes[rightMoreTrialsOneFreq], spikeCountEachTrial[rightMoreTrialsOneFreq] + jitter, edgecolor='grey', facecolor='None', label='right_more_reward')
        rThisFreq, pValThisFreq = stats.pearsonr(responseTimes[leftMoreTrialsOneFreq|rightMoreTrialsOneFreq], spikeCountEachTrial[leftMoreTrialsOneFreq|rightMoreTrialsOneFreq])
        print 'For {}, correlation r: {:.3f}, p: {:.3f}'.format(soundFreq, rThisFreq, pValThisFreq)
        plt.xlim([0.15,0.8])
        plt.xlabel('Response time (sec)')
        plt.ylabel('Spike count 0.05-0.25s after Cout')
        plt.legend()
        plt.title(soundFreq)

    #plt.subplot(313)
    ax = plt.subplot(gs[2, :])
    behavPlot.plot_ave_psycurve_reward_change(animal, [cellInfo['behavSession']])
        
    plt.show()
    if SAVE_FIGURE:
        extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
