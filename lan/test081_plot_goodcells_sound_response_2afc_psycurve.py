'''
Generate and store intermediate data for plot showing frequency-selectivity of astr sound-responsive neurons (using 2afc data). Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.

Lan Guo 20170302
'''

### To DO 

# In the filename of the npz should include tetrode and cluster e.g. T6_c2
# save the script name that generates the npz in the npz file, in the field called 'script' (using os.path.realpath(__file__)
# Save the manually set params such as timeRange in npz file

import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib
import figparams
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib import pyplot as plt
import pdb

FIGNAME = 'sound_freq_selectivity_psycurve'
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
timeRange = [-0.3,0.4]
binWidth = 0.010
qualityList = [1,6]
ISIcutoff = 0.02

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

colormapTuning = matplotlib.cm.winter 

outputDir = os.path.join('/home/languo/tmp', FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

gs = gridspec.GridSpec(1,2)
gs.update(left=0.15, right=0.85, wspace=0.5, hspace=0.2)
gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,0], hspace=0.2)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,1], hspace=0.2)
# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))

# -- Load psycurve cell database and select cells to plot -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

goodcells_psychometric = (allcells_psychometric.cellQuality.isin(qualityList)) & (allcells_psychometric.ISI <= ISIcutoff)
cellInStr =  (allcells_psychometric.cellInStr==1)
keepAfterDupTest = allcells_psychometric.keep_after_dup_test
cellSelector = goodcells_psychometric & cellInStr & keepAfterDupTest  #Boolean array
cellsToPlot = allcells_psychometric[cellSelector]

for ind, cell in cellsToPlot.iterrows(): 
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')
    
    # -- Select a cell from allcells file -- #
    cellParams = {'firstParam':str(cell['animalName']),
                  'behavSession':str(cell['behavSession']),
                  'tetrode':int(cell['tetrode']),
                  'cluster':int(cell['cluster'])} 

    figname = '{}_{}_T{}_c{}_tuning_2afc_soundres'.format(cell['animalName'],cell['behavSession'],cell['tetrode'],cell['cluster'])
    fullFigname = os.path.join(outputDir, figname)
    pdb.set_trace()
    if os.path.exists(fullFigname): #Don't plot if already exists
        print 'This cell has been plotted'
        continue

    try: #This is a hack, when some files cannot be open or anything goes wrong, just skip this cell
        print 'Plotting figure for cell', ind
        mouseName = cellParams['firstParam']
        allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)
        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(**cellParams)
        oneCell = allcells.cellDB[cellIndex]

        #################### tuning curve task ###########################
        ## Get behavior data associated with 2afc session ###
        behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'tuning_curve',oneCell.behavSession)
        behavFile = os.path.join(BEHAVIOR_PATH,oneCell.animalName,behavFileName)
        bdata = loadbehavior.BehaviorData(behavFile,readmode='full')

        ### Get events data ###
        fullEventFilename=os.path.join(EPHYS_PATH, oneCell.animalName, oneCell.tuningSession, 'all_channels.events')
        eventData = loadopenephys.Events(fullEventFilename)
        ##### Get event onset times #####
        eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
        eventOnsetTimes = eventData.timestamps
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

        ### GEt spike data of just this cluster ###
        spikeFilename = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.tuningSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
        spikeData = loadopenephys.DataSpikes(spikeFilename)
        spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
        clustersDir = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.tuningSession)+'_kk'
        clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
        clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
        spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
        spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
        spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
        # FIXME: This assumes the gain is the same for all channels and records
        spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
        #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
        spikeTimestamps = spikeData.timestamps

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)
        trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)
        # -- Plot tuning raster -- #
        ax1 = plt.subplot(gs00[0:2,:])
        labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                       indexLimitsEachTrial,
                                                       timeRange,
                                                       trialsEachCond=trialsEachFreq,
                                                       labels=labels)

        plt.setp(pRaster, ms=msRaster)
        plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.title('Tuning curve', fontsize=fontSizeLabels)

        # -- Plot tuning PSTH -- #
        ax2 = plt.subplot(gs00[2,:])
        freqScaleFactor = 3 #factor to reduce number of frequencies plotted by
        possibleFreq = possibleFreq[1::freqScaleFactor] #select just a subset of frequencies to plot
        numFreqs = len(possibleFreq)
        trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        cm_subsection = np.linspace(0.0, 1.0, numFreqs)
        colorEachCond = [colormapTuning(x) for x in cm_subsection] 
        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachFreq,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

        for ind,line in enumerate(pPSTH):
            plt.setp(line, label=labels[ind])
        plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)


        ######################## 2afc task ##################################
        ## Get behavior data associated with 2afc session ###
        behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
        behavFile = os.path.join(BEHAVIOR_PATH,oneCell.animalName,behavFileName)
        bdata = loadbehavior.BehaviorData(behavFile,readmode='full')


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

        # -- Calculate and store intermediate data for tuning raster -- #
        freqEachTrial = bdata['targetFrequency']
        possibleFreq = np.unique(freqEachTrial)

        trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
        labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

        # -- Plot 2afc raster -- #
        ax3 = plt.subplot(gs01[0:2,:])
        labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                       indexLimitsEachTrial,
                                                       timeRange,
                                                       trialsEachCond=trialsEachFreq,
                                                       labels=labels)

        plt.setp(pRaster, ms=msRaster)
        plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.title('Psycurve 2afc', fontsize=fontSizeLabels)

        # -- Plot tuning PSTH -- #
        ax4 = plt.subplot(gs01[2,:])
        freqScaleFactor = 1 #factor to reduce number of frequencies plotted by
        possibleFreq = possibleFreq[1::freqScaleFactor] #select just a subset of frequencies to plot
        numFreqs = len(possibleFreq)
        trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        cm_subsection = np.linspace(0.0, 1.0, numFreqs)
        colorEachCond = [colormapTuning(x) for x in cm_subsection] 
        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachFreq,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

        for ind,line in enumerate(pPSTH):
            plt.setp(line, label=labels[ind])
        plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
        plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)

        print 'Saving figure'

        plt.savefig(fullFigname)
    
    except:
        pass
