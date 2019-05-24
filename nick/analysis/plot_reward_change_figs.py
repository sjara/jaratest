'''
Script for plotting reward change figures for Jardon's poster
Nick Ponvert 2018-05-05
'''

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
reload(settings)
# from jaratest.lan.analysis_reward_change import new_reward_change_plotter_functions as rcfuncs
from jaratest.lan.analysis_reward_change.new_reward_change_plotter_functions import *



databaseFullPath = '/mnt/jarahubdata/figuresdata/2018rc/rc_database.h5'
key = 'reward_change'
celldb = pd.read_hdf(databaseFullPath, key=key)
evlockDir = '/tmp/evlock_rc'

cOutWindow = '0.05-0.15s'
soundWindow = '0-0.1s'

ACSoundCells = [
    {'subject':'adap071',
     'date':'2017-09-03',
     'tetrode':6,
     'cluster':2,
     'alignment':'sound',
     'freq':'low'},

    {'subject':'adap067',
     'date':'2017-10-10',
     'tetrode':2,
     'cluster':8,
     'alignment':'sound',
     'freq':'low'},

    {'subject':'gosi001',
     'date':'2017-05-01',
     'tetrode':1,
     'cluster':12,
     'alignment':'sound',
     'freq':'low'},

    {'subject':'adap067',
     'date':'2017-09-22',
     'tetrode':8,
     'cluster':4,
     'alignment':'sound',
     'freq':'low'}
    ]


ACMovementCells = [
    {'subject':'gosi004',
     'date':'2017-03-15',
     'tetrode':6,
     'cluster':7,
     'alignment':'center-out',
     'freq':'high'},

    {'subject':'adap067',
     'date':'2017-09-24',
     'tetrode':8,
     'cluster':4,
     'alignment':'center-out',
     'freq':'high'},

    {'subject':'gosi008',
     'date':'2017-03-14',
     'tetrode':7,
     'cluster':8,
     'alignment':'center-out',
     'freq':'high'},

    {'subject':'adap067',
     'date':'2017-10-15',
     'tetrode':8,
     'cluster':11,
     'alignment':'center-out',
     'freq':'high'}
    ]

AStrSoundCells = [
    {'subject':'adap012',
     'date':'2016-04-05',
     'tetrode':4,
     'cluster':6,
     'alignment':'sound',
     'freq':'high'},

    {'subject':'adap017',
     'date':'2016-04-06',
     'tetrode':4,
     'cluster':03,
     'alignment':'sound',
     'freq':'high'}
    ]

AStrMovementCells = [
    {'subject':'adap012',
     'date':'2016-03-24',
     'tetrode':4,
     'cluster':8,
     'alignment':'center-out',
     'freq':'high'},

    {'subject':'adap012',
     'date':'2016-03-23',
     'tetrode':6,
     'cluster':12,
     'alignment':'center-out',
     'freq':'high'}]

cellLists = [ACSoundCells, ACMovementCells, AStrSoundCells, AStrMovementCells]
cellListNames = ['ACSoundCells', 'ACMovementCells', 'AStrSoundCells', 'AStrMovementCells']

timeRange = [-0.3, 0.4]
timeRangeToPlot = [timeRange[0]+0.1, timeRange[1]]

fontSizeLabel = 20
fontSizeTicks = 16
axisLineWidth = 2
ticksWidth = 2
vlineWidth = 2

figSize = [5, 5.5]

#A modification of celldatabase.find_cell because I don't know the depths
def find_cell(database, subject, date, tetrode, cluster):
     cell = database.query('subject==@subject and date==@date and tetrode==@tetrode and cluster==@cluster')
     if len(cell)>1:
          raise AssertionError('This information somehow defines more than 1 cell in the database.')
     elif len(cell)==0:
          raise AssertionError('No cells fit this search criteria.')
     elif len(cell)==1:
          return cell.index[0], cell.iloc[0] #Return the index and the series: once you convert to series the index is lost



##############################

colorLeftMore = colorpalette.TangoPalette['Orange2']
colorRightMore = colorpalette.TangoPalette['SkyBlue2']

# colorDictRC = {'leftMoreLowFreq':'g',
#                'rightMoreLowFreq':'m',
#                #'sameRewardLowFreq':'y',
#                'leftMoreHighFreq':'r',
#                'rightMoreHighFreq':'b'}
#                #'sameRewardHighFreq':'darkgrey'

colorDictRC = {'leftMoreLowFreq':colorLeftMore,
               'rightMoreLowFreq':colorRightMore,
               #'sameRewardLowFreq':'y',
               'leftMoreHighFreq':colorLeftMore,
               'rightMoreHighFreq':colorRightMore}
               #'sameRewardHighFreq':'darkgrey'


colorDictMovement = {'left':'g',
                     'right':'r'}

soundChannelType = 'stim'

minBlockSize = 20 # Last blocks with valid trial number smaller than this is not plotted

def plot_reward_change_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, alignment='sound', timeRange=[-0.3,0.4], freqToPlot='low', byBlock=False, colorCondDict=colorDictRC, vlineWidth=1):
    '''
    Function to plot reward change raster.
    '''
    spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = load_intermediate_data_for_raster_psth(cellObj, evlockDir, alignment, timeRange, behavClass)
    #spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = calculate_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass) 
    if np.any(spikeTimesFromEventOnset):
        if freqToPlot == 'low' or freqToPlot=='high':
            trialsEachCond, colorEachCond, labelEachCond = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass) 

        elif freqToPlot == 'both':
            trialsEachCondList = []
            colorEachCond = []
            labelEachCond = []
            for freq in ['low','high']:
                trialsEachCondThisFreq, colorEachCondThisFreq, labelEachCondThisFreq  = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
                trialsEachCondList.append(trialsEachCondThisFreq)
                colorEachCond.extend(colorEachCondThisFreq)
                labelEachCond.extend(labelEachCondThisFreq)
            trialsEachCond = np.concatenate(trialsEachCondList, axis=1)

        # -- Plot raster -- #
        pRaster, hCond, zLine = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
        plt.axvline(x=0,linewidth=vlineWidth, color='darkgrey')
        plt.ylabel('Trials')
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
        # plt.title('{0}_{1}freq'.format(alignment,freqToPlot),fontsize=10)
    else:
       pass

    return pRaster, hCond, zLine

def plot_reward_change_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010, freqToPlot='low', byBlock=False, colorCondDict=colorDictRC, smoothWinSize=3, fontSizeLabel=12, vlineWidth=1):
    '''
    Function to plot reward change psth.
    '''
    spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = load_intermediate_data_for_raster_psth(cellObj, evlockDir, alignment, timeRange, behavClass)
    #spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = calculate_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass)
    if np.any(spikeTimesFromEventOnset):
        if freqToPlot == 'low' or freqToPlot=='high':
            trialsEachCond, colorEachCond, labelEachCond = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
        elif freqToPlot == 'both':
            trialsEachCondList = []
            colorEachCond = []
            labelEachCond = []
            for freq in ['low','high']:
                trialsEachCondThisFreq, colorEachCondThisFreq, labelEachCondThisFreq = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
                trialsEachCondList.append(trialsEachCondThisFreq)
                colorEachCond.extend(colorEachCondThisFreq)
                labelEachCond.extend(labelEachCondThisFreq)
            trialsEachCond = np.concatenate(trialsEachCondList, axis=1)

        # -- Plot PSTH -- #
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        smoothWinSize = smoothWinSize
        #plt.subplot2grid((3,1), (2, 0))
        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

        # -- Add legend -- #
        for ind,line in enumerate(pPSTH):
            plt.setp(line, label=labelEachCond[ind])
            # plt.legend(loc='upper right', fontsize=10, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

        # maxSpikes = np.max(spikeCountMat/binWidth)
        # minSpikes = np.min(spikeCountMat/binWidth)
        ax = plt.gca()
        # ax.set_yticks([minSpikes, maxSpikes])
        plt.axvline(x=0,linewidth=vlineWidth, color='darkgrey')
        plt.xlabel('Time from {0} onset (s)'.format(alignment), fontsize=fontSizeLabel)
        plt.ylabel('Firing rate\n(spk/s)', fontsize=fontSizeLabel)
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
    else:
        pass

    return pPSTH

##############################

for indCellList, cellList in enumerate(cellLists):
    outputDir = os.path.join('/mnt/jarahubdata/reports/nick/figsForPoster', cellListNames[indCellList])
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    for cellDict in cellList:

        subject = cellDict['subject']
        date = cellDict['date']
        tetrode = cellDict['tetrode']
        cluster = cellDict['cluster']

        cellInd, dbRow = find_cell(celldb, subject, date, tetrode, cluster)
        cellObj = ephyscore.Cell(dbRow)

        plt.clf()
        ax1 = plt.subplot(211)
        pRaster = plot_reward_change_raster(cellObj, evlockDir, byBlock=True, freqToPlot=cellDict['freq'], alignment=cellDict['alignment'], timeRange=timeRange, vlineWidth=vlineWidth)
        extraplots.boxoff(ax1)
        ax1.set_xlim(timeRangeToPlot)
        ax1.set_xticks([])
        ax1.spines['left'].set_visible(False)
        ax1.set_yticks([])
        ax1.set_ylabel('')
        ax2 = plt.subplot(212)

        pPsth = plot_reward_change_psth(cellObj, evlockDir, byBlock=True, freqToPlot=cellDict['freq'], alignment=cellDict['alignment'],
                                        timeRange=timeRange, fontSizeLabel=fontSizeLabel, vlineWidth=vlineWidth)
        extraplots.boxoff(ax2)
        ax2.set_xlim(timeRangeToPlot)
        ax2.set_xticks([0, timeRange[1]])
        extraplots.set_ticks_fontsize(ax2, fontSizeTicks)
        locs, labels = plt.yticks()
        # ax2.set_yticks([locs[0], locs[-1]])
        # ax2.set_yticklabels([labels[0], labels[-1]])

        ax2.xaxis.set_tick_params(width=ticksWidth)
        ax2.yaxis.set_tick_params(width=ticksWidth)

        for axis in ['bottom','left']:
            ax2.spines[axis].set_linewidth(axisLineWidth)

        plt.subplots_adjust(hspace=0)
        plt.show()

        figName = "{}_{}_TT{}c{}".format(subject, date, tetrode, cluster)
        # fullName = os.path.join(outputDir, figName)
        # plt.savefig(fullName)
        extraplots.save_figure(figName, 'svg', figSize, outputDir=outputDir)
        # print "Saved figure to {}".format(fullName)

# plot_reward_change_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
# # ax3 = plt.subplot(gs00[2, :])
