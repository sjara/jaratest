import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.anna import bandwidths_analysis_v2 as bandan
from jaratest.anna import behaviour_test as bt
reload(bt)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
import matplotlib.gridspec as gridspec
import matplotlib
import string
import pdb

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

PRINT_FIGURE = 0
outputDir = '/tmp/'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

FIG = 3

if FIG == 1:
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv')
    cell = db.loc[154]
    ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
    behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
    sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]
    bandIndex = sessType.index('bandwidth')
    
    loader = dataloader.DataLoader(cell['subject'])
    
    plt.clf()
    
    gs = gridspec.GridSpec(1,2)
    gs.update(left=0.15, right=0.85, wspace=0.2, hspace=0.3)
    
    eventData = loader.get_session_events(ephysDirs[bandIndex])
    spikeData = loader.get_session_spikes(ephysDirs[bandIndex], int(cell['tetrode']), cluster=int(cell['cluster']))
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimestamps = spikeData.timestamps
    bdata = loader.get_session_behavior(behavDirs[bandIndex])
    bandEachTrial = bdata['currentBand']
    ampEachTrial = bdata['currentAmp']
    spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandan.bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)
    
    
    ax1 = plt.subplot(gs[0, 0])
    trialsThisSecondVal = trialsEachCond[:, :, 1]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                    indexLimitsEachTrial,
                                                    timeRange = [-0.2, 1.5],
                                                    trialsEachCond=trialsThisSecondVal,
                                                    labels=firstSortLabels)
    plt.setp(pRaster, ms=4)
    extraplots.boxoff(plt.gca())
    plt.xlabel('Time from stimulus onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    #ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    
    ax2 = plt.subplot(gs[0,1])
    spikeArray, errorArray, baseSpikeRate = bandan.band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
    xrange = range(len(np.unique(bandEachTrial)))
    plt.plot(xrange, spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')    
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
    plt.ylabel('Average number of spikes during stimulus', fontsize=fontSizeLabels)
    ax = plt.gca()
    ax.set_xticklabels(np.unique(bandEachTrial))
    #ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    
    
    plt.show()
    
    figFormat = 'pdf' #'svg' 
    figFilename = 'testfig' # Do not include extension
    if PRINT_FIGURE:
        extraplots.save_figure(figFilename, figFormat, [8,6], outputDir)
elif FIG == 2:
    plt.clf()
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
    PV_CELL = 210
    SOM_CELL = 304
    cells = [PV_CELL, SOM_CELL]
    
    gs = gridspec.GridSpec(2,2)
    gs.update(left=0.15, right=0.85, wspace=0.3, hspace=0.3)
    
    labelPosX = [0.18, 0.47, 0.67]  # Horiz position for panel labels
    labelPosY = [0.92]    # Vert position for panel labels
    
    for indCell, cell in enumerate(cells):
        cell = db.loc[cell]
        cellInfo = bandan.get_cell_info(cell)
        
        loader = dataloader.DataLoader(cell['subject'])
        
        
        #plt.subplot(gs[indCell,0])
        #tsThisCluster, wavesThisCluster = bandan.load_cluster_waveforms(cellInfo)
        #spikesorting.plot_waveforms(wavesThisCluster)
        
        plt.subplot(gs[indCell,0])
        eventData = loader.get_session_events(cellInfo['ephysDirs'][cellInfo['laserIndex'][-1]])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][cellInfo['laserIndex'][-1]], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.1, 0.4]
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimestamps, eventOnsetTimes, timeRange)
        pRaster, hcond, zline = extraplots.raster_plot(
            spikeTimesFromEventOnset,
            indexLimitsEachTrial,
            timeRange)
        plt.setp(pRaster, ms=4)
        plt.xlabel('Time from laser onset (sec)')
        plt.axvspan(0, 0.1, alpha=0.2, color='blue')
        
        plt.subplot(gs[indCell, 1])
        bandIndex = cellInfo['bandIndex'][0]
        eventData = loader.get_session_events(cellInfo['ephysDirs'][bandIndex])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][bandIndex], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.2, 1.5]
        bandBData = loader.get_session_behavior(cellInfo['behavDirs'][bandIndex])  
        bandEachTrial = bandBData['currentBand']
        ampEachTrial = bandBData['currentAmp']
        numAmps = len(np.unique(ampEachTrial))
        spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandan.bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)
        spikeArray, errorArray, baseSpikeRate = bandan.band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
        xrange = range(len(np.unique(bandEachTrial)))
        if numAmps > 1:
            plt.plot(xrange, spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
            plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                             spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
        else:
            plt.plot(xrange, spikeArray, '-o', color = '#5c3566', linewidth = 3)
            plt.fill_between(xrange, spikeArray.flatten() - errorArray.flatten(), 
                             spikeArray.flatten() + errorArray.flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.xlabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
        ax = plt.gca()
        ax.set_xticklabels(np.unique(bandEachTrial))
        plt.ylabel('Average spike rate (Hz)', fontsize=fontSizeLabels)
    plt.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    plt.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    plt.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    plt.annotate('PV', xy=(0.12,0.71), xycoords='figure fraction', fontsize=20, fontweight='bold')
    plt.annotate('SOM', xy=(0.12,0.265), xycoords='figure fraction', fontsize=20, fontweight='bold')
    plt.show()
elif FIG == 3:
    from statsmodels.stats.proportion import proportion_confint
    gs = gridspec.GridSpec(1,2)
    gs.update(left=0.15, right=0.85, wspace=0.4, hspace=0.4)
    labelPosX = [0.08, 0.48]
    labelPosY = [0.92, 0.46]
    
    animal = 'band008'
    sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a', '20161206a', '20161207a']
    plt.subplot(gs[0,0])
    validPerSNR, rightPerSNR, possibleSNRs = bt.band_SNR_psychometric(animal, sessions[::2])
    bt.plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs)
    validPerSNR, rightPerSNR, possibleSNRs = bt.band_SNR_psychometric(animal, sessions[1::2])
    bt.plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour='r')
    plt.ylabel('% rightward choice')
    plt.xlabel('Signal to noise ratio (dB)')
    
    animals = ['band006','band008','band010']
    plt.subplot(gs[0,1])
    for animal in animals:
        salValid, salCorrect = bt.behav_stats(animal, sessions[::2])
        musValid, musCorrect = bt.behav_stats(animal, sessions[1::2])
        salAccuracy = 100.0*salCorrect/salValid
        musAccuracy = 100.0*musCorrect/musValid
        plt.plot([1,2],[salAccuracy,musAccuracy], '-o', color='k', lw=3, ms=10)
        salCI = np.array(proportion_confint(salCorrect, salValid, method = 'wilson'))
        musCI = np.array(proportion_confint(musCorrect, musValid, method = 'wilson'))
        upper = [(100.0*salCI[1]-salAccuracy),(100.0*musCI[1]-musAccuracy)]
        lower = [(salAccuracy-100.0*salCI[0]), (musAccuracy-100.0*musCI[0])]
        plt.errorbar([1,2], [salAccuracy, musAccuracy], yerr = [lower, upper],color='k')
    plt.xlim([0.5,2.5])
    plt.ylim([50,100])
    ax = plt.gca()
    ax.set_xticks([1,2])
    ax.set_xticklabels(['saline', 'muscimol'],fontsize=12)
    plt.ylabel('Accuracy (%)',fontsize=16)
        
    '''animal = 'band017'
    sessions = ['20170228a','20170226a','20170224a','20170222a']
    plt.subplot(gs[1,0])
    validPerSNR, rightPerSNR, possibleSNRs = bt.band_SNR_laser_psychometric(animal, sessions)
    colours = ['k','b']
    for las in range(len(validPerSNR)):
        bt.plot_psychometric(validPerSNR[las,:], rightPerSNR[las,:], possibleSNRs, colour = colours[las])
    plt.ylabel('% rightward choice')
    plt.xlabel('Signal to noise ratio (dB)')
       
    animals = ['band017', 'band020']
    plt.subplot(gs[1,1])
    for animal in animals:
        valid, correct = bt.behav_laser_stats(animal, sessions[::2])
        conAccuracy = 100.0*correct[0]/valid[0]
        lasAccuracy = 100.0*correct[1]/valid[1]
        plt.plot([1,2],[conAccuracy,lasAccuracy], '-o', color='k', lw=2)
        conCI = np.array(proportion_confint(correct[0], valid[0], method = 'wilson'))
        lasCI = np.array(proportion_confint(correct[1], valid[1], method = 'wilson'))
        upper = [(100.0*conCI[1]-conAccuracy),(100.0*lasCI[1]-lasAccuracy)]
        lower = [(conAccuracy-100.0*conCI[0]), (lasAccuracy-100.0*lasCI[0])]
        plt.errorbar([1,2], [conAccuracy, lasAccuracy], yerr = [lower, upper],color='k')
    plt.xlim([0.5,2.5])
    plt.ylim([50,100])
    ax = plt.gca()
    ax.set_xticks([1,2])
    ax.set_xticklabels(['no laser', 'laser'])
    plt.ylabel('Accuracy (%)')'''
    
    plt.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    plt.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    #plt.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    #plt.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
elif FIG == 4:
    plt.clf()
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/good_cells_stats.csv')
    CELL_1 = 19
    CELL_2 = 210
    CELL_3 = 296
    cells = [CELL_1, CELL_2, CELL_3]
    
    gs = gridspec.GridSpec(1,3)
    gs.update(left=0.15, right=0.85, wspace=0.15, hspace=0.3)
    
    for indCell, cell in enumerate(cells):
        cell = db.loc[cell]
        cellInfo = bandan.get_cell_info(cell)
        
        loader = dataloader.DataLoader(cell['subject'])
        
        
        plt.subplot(gs[0,indCell])
        bandIndex = cellInfo['bandIndex'][0]
        eventData = loader.get_session_events(cellInfo['ephysDirs'][bandIndex])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][bandIndex], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.2, 1.5]
        bandBData = loader.get_session_behavior(cellInfo['behavDirs'][bandIndex])  
        bandEachTrial = bandBData['currentBand']
        ampEachTrial = bandBData['currentAmp']
        numAmps = len(np.unique(ampEachTrial))
        spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandan.bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)
        spikeArray, errorArray, baseSpikeRate = bandan.band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
        xrange = range(len(np.unique(bandEachTrial)))
        if numAmps > 1:
            plt.plot(xrange, spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
            plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                             spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
        else:
            plt.plot(xrange, spikeArray, '-o', color = '#5c3566', linewidth = 3)
            plt.fill_between(xrange, spikeArray.flatten() - errorArray.flatten(), 
                             spikeArray.flatten() + errorArray.flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
        extraplots.set_ticks_fontsize(plt.gca(),14)
        plt.xlabel('Bandwidth (octaves)', fontsize=20)
        ax = plt.gca()
        ax.set_xticklabels(np.unique(bandEachTrial))
        if indCell==0:
            plt.ylabel('Average spike rate (Hz)', fontsize=20)
    plt.show()