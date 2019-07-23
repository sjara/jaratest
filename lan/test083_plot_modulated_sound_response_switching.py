'''
For good cells (nonduplicates) in the striatum recorded in switching 2afc task: plot suond response in 2afc task for modulated cells (modSig<0.05, modDir>1).

Lan Guo 20170310
'''

import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib
import figparams
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import pandas as pd
from matplotlib import pyplot as plt
import pdb

FIGNAME = 'sound_modulation_switching'
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
timeRange = [-0.3,0.4]
minBlockSize = 20
binWidth = 0.010
qualityList = [1,6]
ISIcutoff = 0.02
maxZThreshold = 3
figSize = [12,8]
fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

colorsDict = {'lowBlock':figparams.colp['MidFreqL'], 
              'highBlock':figparams.colp['MidFreqR']} 

outputDir = os.path.join('/home/languo/tmp', FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

plt.figure(figsize=figSize) 
gs = gridspec.GridSpec(2,2)
gs.update(left=0.1, right=0.9, wspace=0.55, hspace=0.6)
gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,0], hspace=0.2)
#gs01 = gridspec.GridSpecFromSubplotSpec(4, 3, subplot_spec=gs[:,1], hspace=0.2)

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))

# -- Load psycurve cell database and select cells to plot -- #
switchingFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

goodcells_switching = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellInStr =  (allcells_switching.cellInStr==1)
keepAfterDupTest = allcells_switching.keep_after_dup_test
cellSelector = goodcells_switching & cellInStr & keepAfterDupTest  #Boolean array
#goodCells = allcells_switching[cellSelector]
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold
allcellsResponsive = allcells_switching[cellSelector & responsiveMidFreqs] # good cells IN STR sound responsive to middle frequency
sigMod = np.array((allcellsResponsive.modSig<=0.05) & (allcellsResponsive.modDir>=1), dtype=bool) 
cellsToPlot = allcellsResponsive[sigMod]

for ind, cell in cellsToPlot.iterrows(): 
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')
    
    # -- Select a cell from allcells file -- #
    cellParams = {'firstParam':str(cell['animalName']),
                  'behavSession':str(cell['behavSession']),
                  'tetrode':int(cell['tetrode']),
                  'cluster':int(cell['cluster'])} 

    figname = '{}_{}_T{}_c{}_switching_mod_soundres.png'.format(cell['animalName'],cell['behavSession'],cell['tetrode'],cell['cluster'])
    fullFigname = os.path.join(outputDir, figname)
    #pdb.set_trace()
    #if os.path.exists(fullFigname): #Don't plot if already exists
        #print 'This cell has been plotted'
        #continue

    print 'Plotting figure for cell', ind
    mouseName = cellParams['firstParam']
    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(**cellParams)
    oneCell = allcells.cellDB[cellIndex]


    ######################## 2afc task ##################################
    ## Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,oneCell.animalName,behavFileName)
    bdata = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')


    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, oneCell.animalName, oneCell.ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!


    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    spikeTimestamps = spikeData.timestamps

    # -- Check to see if ephys has skipped trials, if so remove trials from behav data -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimeEphys = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    # -- Select trials to plot from behavior file -- #
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)

    # -- Select trials of middle frequency to plot, determine whether to plot by block -- #
    middleFreq = possibleFreq[numFreqs/2] #selects middle frequency, using int division resulting in int property. MAY FAIL IN THE FUTURE
    #pdb.set_trace()
    oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency
    correctOneFreq = oneFreq  & correct 

    # -- Plot sound response to mid freq by block -- #
    bdata.find_trials_each_block()
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
    correctBlockSizes = sum(correctTrialsEachBlock)
    if (correctBlockSizes[-1] < minBlockSize): #A check to see if last block is too small to plot
        correctTrialsEachBlock = correctTrialsEachBlock[:,:-1]

    trialsEachCond = correctTrialsEachBlock
    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachCond = 5*[colorsDict['lowBlock'],colorsDict['highBlock']] #assume there are not more than 5 blocks
    elif bdata['currentBlock'][0]==bdata.labels['currentBlock']['high_boundary']:
        colorEachCond = 5*[colorsDict['highBlock'],colorsDict['lowBlock']]

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimeEphys,timeRange)

    # -- Plot 2afc raster -- #
    ax3 = plt.subplot(gs00[0:2,:])

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond,
                                                   colorEachCond)

    plt.setp(pRaster, ms=msRaster)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)

    plt.title('modInd:{};\n modSig:{}; maxZ:{}'.format(cell['modIndex'],cell['modSig'],cell['maxZSoundMid']), fontsize=fontSizeLabels-2)


    # -- Plot tuning PSTH -- #
    ax4 = plt.subplot(gs00[2,:])   
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond,colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    left_line = mlines.Line2D([], [], color='g', label='left choice')
    right_line = mlines.Line2D([], [], color='r', label='right choice')
    plt.legend(handles=[left_line, right_line], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)



    # -- Plot waveform -- #
    ax7 = plt.subplot(gs[0,1])
    wavesThisCluster = spikeData.samples
    spikesorting.plot_waveforms(wavesThisCluster)

    # -- Plot ISI -- #
    ax8 = plt.subplot(gs[1,1])
    spikesorting.plot_isi_loghist(spikeTimestamps)


    print 'Saving figure'

    plt.savefig(fullFigname)

    #except:
        #continue

