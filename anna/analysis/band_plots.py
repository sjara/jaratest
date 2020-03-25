import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
from scipy import stats

from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore

import band_ephys_analysis as ephysanalysis
reload(ephysanalysis)

# --- Methods for creating simple plots ---
def plot_sorted_raster(spikeTimeStamps, eventOnsetTimes, sortArray, timeRange=[-0.5, 1],xlabel='Time from sound onset (sec)',ylabel='Frequency (kHz)',ms=4,labels=None,*args,**kwargs):
    '''
    Function to accept spike timestamps, event onset times, and a sorting array and plot a
    raster plot sorted by the array passed

    Args:
        sortarray (array): An array of parameter values for each trial.
                           Output will be sorted by the possible values of the parameter.
                           Must be the same length as the event onset times array

    '''
    trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond,labels=labels, *args, **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.setp(pRaster, ms=ms)

def plot_sorted_psth(spikeTimeStamps, eventOnsetTimes, sortArray, timeRange=[-0.5,1], binsize = 50, lw=2, plotLegend=False, *args, **kwargs):
    '''
    Function to accept spike timestamps, event onset times, and a sorting array and plot a
    PSTH sorted by the sorting array

    Args:
        binsize (float) = size of bins for PSTH in ms
    '''
    binsize = binsize/1000.0
    # If a sort array is supplied, find the trials that correspond to each value of the array
    if len(sortArray) > 0:
        trialsEachCond = behavioranalysis.find_trials_each_type(
            sortArray, np.unique(sortArray))
    else:
        trialsEachCond = []
    # Align spiketimestamps to the event onset times for plotting
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, [timeRange[0]-binsize, timeRange[1]])
    binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
    pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1], trialsEachCond, *args, **kwargs)
    plt.setp(pPSTH, lw=lw)
    plt.hold(True)
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.xlim(timeRange)

    if plotLegend:
        if len(sortArray)>0:
            sortElems = np.unique(sortArray)
            for ind, pln in enumerate(pPSTH):
                pln.set_label(sortElems[ind])
            # ax = plt.gca()
            # plt.legend(mode='expand', ncol=3, loc='best')
            plt.legend(ncol=3, loc='best')

def plot_separated_rasters(gridspec, xcoords, ycoord, firstSort, secondSort, spikeTimestamps, eventOnsetTimes, timeRange=[-0.2,1.5], ylabel='bandwidth (octaves)', xlabel='Time from sound onset (sec)', titles=None, duplicate=False, colours=None, plotHeight=1):      
    firstSortLabels = ['{}'.format(first) for first in np.unique(firstSort)]
    numFirst = np.unique(firstSort)
    numSec = np.unique(secondSort)   
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort,
                                                                    numFirst,
                                                                    secondSort,
                                                                    numSec)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange) 
    if colours is None:
        colours = [np.tile(['0.25','0.6'],len(numFirst)/2+1), np.tile(['#4e9a06','#8ae234'],len(numFirst)/2+1)]
    for ind, secondArrayVal in enumerate(numSec):
        plt.subplot(gridspec[ycoord+ind*plotHeight:ycoord+ind*plotHeight+plotHeight, xcoords[0]:xcoords[1]])
        trialsThisSecondVal = trialsEachCond[:, :, ind]
        # a dumb workaround specifically for plotting harmonic sessions
        if duplicate:
            for ind2, first in enumerate(numFirst):
                if not any(trialsThisSecondVal[:,ind2]):
                    trialsThisSecondVal[:,ind2]=trialsEachCond[:,ind2,ind+1]
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        timeRange,
                                                        trialsEachCond=trialsThisSecondVal,
                                                        labels=firstSortLabels,
                                                        colorEachCond = colours[ind])
        plt.setp(pRaster, ms=4)        
        plt.ylabel(ylabel)
        if ind == len(numSec) - 1:
            plt.xlabel(xlabel)
        if titles is not None:
            plt.title(titles[ind])

def plot_tuning_curve(spikeArray, errorArray, xvals, baselineSpikeRate = None, legend = False, labels = ['50 dB SPL', '70 dB SPL'], linecolours = None, errorcolours = None, timeRange = [0,1], title=None, xlabel='Bandwidth (octaves)', ylabel='Firing rate (spk/s)'):
    xrange = range(len(xvals))
    lines = []
    plt.hold(True)
    if linecolours is None:
        linecolours = errorcolours = plt.cm.rainbow(np.linspace(0,1,spikeArray.shape[1]))
    if baselineSpikeRate is not None:
        plt.plot(xrange, baselineSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(xvals)), color = '0.75', linewidth = 2)
    for cond in range(spikeArray.shape[1]):
        l1,=plt.plot(xrange, spikeArray[:,cond].flatten(), '-o', color = linecolours[cond], linewidth = 3, mec='None')
        lines.append(l1)
        plt.fill_between(xrange, spikeArray[:,cond].flatten() - errorArray[:,cond].flatten(), 
                     spikeArray[:,cond].flatten() + errorArray[:,cond].flatten(), alpha=0.2, edgecolor = errorcolours[cond], facecolor=errorcolours[cond])
    ax = plt.gca()
    ax.set_xticks(xrange)
    ax.set_xticklabels(xvals)
    ax.set_ylim(bottom=0)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend: 
        plt.legend(lines,labels, borderaxespad=0., loc='best')
    if title:
        plt.title(title)

def plot_tuning_fitted_gaussian(spikeTimeStamps, eventOnsetTimes, tuningBData, toneInt, gaussFit, Rsquared, timeRange=[0.0,0.1], baseRange=[-0.5,-0.1]):
    freqEachTrial = tuningBData['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    
    intensityEachTrial = tuningBData['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)

    # use closest tone intensity to the one desired
    intensityInd = (np.abs(numIntensities-toneInt)).argmin()
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange)
    tuningDict = ephysanalysis.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, freqEachTrial, intensityEachTrial, timeRange, baseRange, info='plotting')
    responseArray = tuningDict['responseArray'][:,intensityInd]
    errorArray = tuningDict['errorArray'][:,intensityInd]

    plt.hold(True)
    #plot true tuning curve (mean firing rate over 100ms interval when sound was present)
    plt.plot(np.log2(numFreqs), responseArray, 'k-')
    plt.fill_between(np.log2(numFreqs), responseArray - errorArray, responseArray + errorArray, alpha=0.2, edgecolor = '0.6', facecolor='0.6')
    #plot estimated gaussian curve
    x_fine = np.linspace(np.log2(numFreqs)[0], np.log2(numFreqs)[-1], 100)
    plt.plot(x_fine, ephysanalysis.gaussian(x_fine, gaussFit[0], gaussFit[1], gaussFit[2], gaussFit[3]), 'r--')
    
    plt.xlim(np.log2(numFreqs)[0], np.log2(numFreqs)[-1])
    
    ax = plt.gca()
    ax.annotate('R^2 = {0}'.format(Rsquared), xy=(0.1, 0.9), xycoords='axes fraction')
    ax.annotate('window used: {0} to {1} ms'.format(1000*timeRange[0],1000*timeRange[1]), xy=(0.1, 0.8), xycoords='axes fraction')
    ax.set_xticks(np.log2(numFreqs))
    ax.set_xticklabels(labels)
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('Frequency tuning at {} dB'.format(numIntensities[intensityInd]))


# --- Methods for plotting reports with multiple plots ---

def plot_one_int_bandwidth_summary(cell, bandIndex, intIndex=-1):
    plt.clf()
    gs = gridspec.GridSpec(1,3)
    gs.update(left=0.15, right=0.85, top = 0.90, wspace=0.2, hspace=0.5)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    
    #load bandwidth data
    bandEphysData, bandBData = cellObj.load_by_index(bandIndex)
    bandEventOnsetTimes = ephysanalysis.get_sound_onset_times(bandEphysData, 'bandwidth')
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    timeRange = [-0.2, 1.5]
    
    #plot raster of the high amp bandwidth trials
    plt.subplot(gs[0,0])     
    colours = np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial,
                                                                    numBands,
                                                                    secondSort,
                                                                    numSec)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        timeRange) 

    trialsOneAmp = trialsEachCond[:, :, intIndex]
    firstSortLabels = ['{}'.format(band) for band in numBands]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        timeRange,
                                                        trialsEachCond=trialsOneAmp,
                                                        labels=firstSortLabels,
                                                        colorEachCond = colours)
    plt.setp(pRaster, ms=3)
    plt.ylabel('Bandwidth (octaves)')
    plt.xlabel('Time from sound onset (s)')
    #plot bandwidth tuning curves
    plt.subplot(gs[0,2])
    sustainedTimeRange = [0.2,1.0]
    tuningDict = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, secondSort, bandEachTrial, sustainedTimeRange, info='plotting')
    plot_tuning_curve(tuningDict['responseArray'][intIndex,:].reshape([7,1]), tuningDict['errorArray'][intIndex,:].reshape([7,1]), numBands, tuningDict['baselineSpikeRate'], linecolours=['#5c3566'], errorcolours=['#ad7fa8'])
    plt.title('Average sustained response (200-1000 ms)', fontsize=10)

    plt.subplot(gs[0,1])
    onsetTimeRange = [0.0, 0.05]
    tuningDict2 = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, secondSort, bandEachTrial, onsetTimeRange, info='plotting')
    plot_tuning_curve(tuningDict2['responseArray'][intIndex,:].reshape([7,1]), tuningDict2['errorArray'][intIndex,:].reshape([7,1]), numBands, tuningDict2['baselineSpikeRate'], linecolours=['#5c3566'], errorcolours=['#ad7fa8'])
    plt.title('Average onset response (0-50 ms)', fontsize=10)
    
    #save report
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            int(cell['depth']), 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate))
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = 'bandwidth_high_amp_response_{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], int(cell['depth']), tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(14, 3)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')

def plot_laser_bandwidth_summary(cell, bandIndex):
    plt.clf()
    gs = gridspec.GridSpec(2,3)
    gs.update(left=0.15, right=0.85, top = 0.90, wspace=0.2, hspace=0.3)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    
    #load bandwidth data
    bandEphysData, bandBData = cellObj.load_by_index(bandIndex)
    bandEventOnsetTimes = ephysanalysis.get_sound_onset_times(bandEphysData, 'bandwidth')
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['laserTrial']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    timeRange = [-0.5, 1.7]
    colours = [['k','0.5'], ['#c4a000','#fce94f']]
    
    #plot raster of the high amp bandwidth trials
    plt.subplot(gs[0,0])     
    rasterColours = [np.tile(colours[0],len(numBands)/2+1),np.tile(colours[1],len(numBands)/2+1)]
    titles = ['No laser', 'Laser'] 

    plot_separated_rasters(gs, [0,1], 0, bandEachTrial, secondSort, bandSpikeTimestamps, bandEventOnsetTimes, titles=titles, colours=rasterColours, timeRange=timeRange)

    plt.ylabel('Bandwidth (octaves)')
    plt.xlabel('Time from sound onset (s)')
    #plot bandwidth tuning curves
    plt.subplot(gs[0:,2])
    sustainedTimeRange = [0.2,1.0]
    tuningDict = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, sustainedTimeRange, info='plotting')
    plot_tuning_curve(tuningDict['responseArray'], tuningDict['errorArray'], numBands, tuningDict['baselineSpikeRate'], linecolours=['k','#c4a000'], errorcolours=['0.5','#fce94f'])
    plt.title('Average sustained response (200-1000 ms)', fontsize=10)

    plt.subplot(gs[0:,1])
    onsetTimeRange = [0.0, 0.05]
    tuningDict2 = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, onsetTimeRange, info='plotting')
    plot_tuning_curve(tuningDict2['responseArray'], tuningDict2['errorArray'], numBands, tuningDict2['baselineSpikeRate'], linecolours=['k','#c4a000'], errorcolours=['0.5','#fce94f'])
    plt.title('Average onset response (0-50 ms)', fontsize=10)
    
    #save report
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            int(cell['depth']), 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate))
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = 'bandwidth_laser_inactivation_{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], int(cell['depth']), tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(14, 6)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')

def plot_harmonics_summary(cell, harmIndex, bandIndex):
    plt.clf()
    gs = gridspec.GridSpec(3, 2)
    gs.update(left=0.15, right=0.85, top = 0.95, wspace=0.2, hspace=0.3)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    
    #load harmonics ephys and behaviour data
    harmEphysData, harmBData = cellObj.load('harmonics')
    harmEventOnsetTimes = ephysanalysis.get_sound_onset_times(harmEphysData, 'harmonics')
    harmSpikeTimestamps = harmEphysData['spikeTimes']
    timeRange = [-0.2, 1.5]
    
    bandEachTrial = harmBData['currentBand']
    secondSort = harmBData['harmTrialType']
    secondSortLabels = ['noise','harmonics']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    #plot rasters of the noise and harmonics trials        
    colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]
    plot_separated_rasters(gs, [0,1], 1, bandEachTrial, secondSort, harmSpikeTimestamps, harmEventOnsetTimes, titles=secondSortLabels, duplicate=True, colours=colours)
    
    #plot a response curve of the noise and harmonics trials
    plt.subplot(gs[1:, 1:])
    timeRange = [0,1.0]
    spikeArray, errorArray, baselineSpikeRate = ephysanalysis.calculate_tuning_curve_inputs(harmSpikeTimestamps, harmEventOnsetTimes, bandEachTrial, secondSort, timeRange)
    spikeArray[0,0]=spikeArray[0,1]
    errorArray[0,0]=errorArray[0,1]
    plot_tuning_curve(spikeArray, errorArray, numBands, baselineSpikeRate, legend=True, labels=['noise','harmonics'], linecolours=['#4e9a06','#5c3566'], errorcolours=['#8ae234','#ad7fa8'])
    
    #load frequency tuning data and plot frequency tuning raster
    plt.subplot(gs[0, 0])
    tuningEphysData, tuningBData = cellObj.load('tuningCurve')
    tuningEventOnsetTimes = ephysanalysis.get_sound_onset_times(tuningEphysData, 'tuningCurve')
    tuningSpikeTimestamps = tuningEphysData['spikeTimes']
    
    freqEachTrial = tuningBData['currentFreq']
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    plot_sorted_raster(tuningSpikeTimestamps, tuningEventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=labels)
    
    #load bandwidth tuning data and plot bandwidth tuning curve
    plt.subplot(gs[0,1])
    bandEphysData, bandBData = cellObj.load('bandwidth')
    bandEventOnsetTimes = ephysanalysis.get_sound_onset_times(bandEphysData, 'bandwidth')
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    timeRange = [-0.2, 1.5]
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    spikeArray, errorArray, baselineSpikeRate = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange)
    plot_tuning_curve(spikeArray[:,-1].reshape(len(numBands),1), errorArray[:,-1].reshape(len(numBands),1), numBands, baselineSpikeRate, linecolours=['k'], errorcolours=['0.5'])
    
    #save report
    charfreq = str(np.unique(harmBData['charFreq'])[0]/1000)
    modrate = str(np.unique(harmBData['modRate'])[0])
    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            cell['depth'], 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate))
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = 'harmonics_report_{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], int(cell['depth']), tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(14, 10)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
    
def plot_freq_bandwidth_tuning(cell, bandIndex=None):
    plt.clf()
    if bandIndex is None:
        print 'No bandwidth session given'
        return
    
    gs = gridspec.GridSpec(3, 2)
    gs.update(left=0.15, right=0.85, top = 0.95, wspace=0.2, hspace=0.3)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    
    #load bandwidth data
    bandEphysData, bandBData = cellObj.load('bandwidth')
    bandEventOnsetTimes = ephysanalysis.get_sound_onset_times(bandEphysData, 'bandwidth')
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    #plot rasters of the bandwidth trials        
    colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]
    plot_separated_rasters(gs, [0,1], 1, bandEachTrial, secondSort, bandSpikeTimestamps, bandEventOnsetTimes, colours=colours)
    
    #plot bandwidth tuning curve
    plt.subplot(gs[1:,1])
    timeRange = [0.0, 1.0]
    baseRange = [-1.1, -0.1]
    spikeArray, errorArray, baselineSpikeRate = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange, baseRange)
    plot_tuning_curve(spikeArray, errorArray, numBands, baselineSpikeRate, linecolours=['#4e9a06','#5c3566'], errorcolours=['#8ae234','#ad7fa8'])
    
    #load frequency tuning data and plot frequency tuning raster
    plt.subplot(gs[0, 0])
    tuningEphysData, tuningBData = cellObj.load('tuningCurve')
    tuningEventOnsetTimes = ephysanalysis.get_sound_onset_times(tuningEphysData, 'tuningCurve')
    tuningSpikeTimestamps = tuningEphysData['spikeTimes']
    
    freqEachTrial = tuningBData['currentFreq']
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    plot_sorted_raster(tuningSpikeTimestamps, tuningEventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=labels)
    
    #plot frequency tuning and fitted gaussian
    plt.subplot(gs[0,1])
    plot_tuning_fitted_gaussian(tuningSpikeTimestamps, tuningEventOnsetTimes, tuningBData, 55, cell['gaussFreqFit'], cell['tuningFitR2'], timeRange=cell['bestFreqTuningWindow'])
    plt.ylabel('Firing Rate (spk/s)')
    plt.xlabel('Frequency (kHz)')
    
    #save report
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            int(cell['depth']), 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate))
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = 'bandwidth_tuning_report_short_{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], int(cell['depth']), tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(14, 10)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
    
def plot_blind_cell_quality(cell):
    plt.clf()
    gs = gridspec.GridSpec(5, 6)
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    # -- plot laser pulse raster -- 
    laserEphysData, noBehav = cellObj.load('laserPulse')
    laserEventOnsetTimes = laserEphysData['events']['laserOn']
    laserSpikeTimestamps = laserEphysData['spikeTimes']
    timeRange = [-0.1, 0.4]
    
    plt.subplot(gs[0:2, 0:3])
    laserSpikeTimesFromEventOnset, trialIndexForEachSpike, laserIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    laserSpikeTimestamps, laserEventOnsetTimes, timeRange)
    pRaster, hcond, zline = extraplots.raster_plot(laserSpikeTimesFromEventOnset,laserIndexLimitsEachTrial,timeRange)
    plt.xlabel('Time from laser onset (sec)')
    plt.title('Laser Pulse Raster')
    
    # -- plot laser pulse psth --
    plt.subplot(gs[2:4, 0:3])
    binsize = 10/1000.0
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserSpikeTimestamps, 
                                                                                                                   laserEventOnsetTimes, 
                                                                                                                   [timeRange[0]-binsize, 
                                                                                                                    timeRange[1]])
    binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
    pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
    plt.xlim(timeRange)
    plt.xlabel('Time from laser onset (sec)')
    plt.ylabel('Firing Rate (Hz)')
    plt.title('Laser Pulse PSTH')
    
    # -- didn't record laser trains for some earlier sessions --
    if len(cellObj.get_session_inds('laserTrain')) > 0:
        # -- plot laser train raster --
        laserTrainEphysData, noBehav = cellObj.load('laserTrain')
        laserTrainEventOnsetTimes = laserTrainEphysData['events']['laserOn']
        laserTrainSpikeTimestamps = laserTrainEphysData['spikeTimes']
        laserTrainEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(laserTrainEventOnsetTimes, 0.5)
        timeRange = [-0.2, 1.0]
        
        plt.subplot(gs[0:2, 3:])
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps, 
                                                                                                                       laserTrainEventOnsetTimes, 
                                                                                                                       timeRange)
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        plt.xlabel('Time from laser onset (sec)')
        plt.title('Laser Train Raster')
        
        # -- plot laser train psth --
        plt.subplot(gs[2:4, 3:])
        binsize = 10/1000.0
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps, 
                                                                                                                   laserTrainEventOnsetTimes, 
                                                                                                                   [timeRange[0]-binsize, 
                                                                                                                    timeRange[1]])
        binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
        pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
        plt.xlim(timeRange)
        plt.xlabel('Time from laser onset (sec)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Laser Train PSTH')
        
    # -- show cluster analysis --
    #tsThisCluster, wavesThisCluster, recordingNumber = celldatabase.load_all_spikedata(cell)
    # -- Plot ISI histogram --
    plt.subplot(gs[4, 0:2])
    spikesorting.plot_isi_loghist(tsThisCluster)

    # -- Plot waveforms --
    plt.subplot(gs[4, 2:4])
    spikesorting.plot_waveforms(wavesThisCluster)

    # -- Plot events in time --
    plt.subplot(gs[4, 4:6])
    spikesorting.plot_events_in_time(tsThisCluster)
    

def plot_bandwidth_report(cell, type='normal', bandTimeRange = [0.2,1.0], bandBaseRange = [-1.0,-0.2]):
    plt.clf()
    
    bandIndex = int(cell['bestBandSession'])
    
    if bandIndex is None:
        print 'No bandwidth session given'
        return
    
    #create cell object for loading data
    cellObj = ephyscore.Cell(cell)
    
    #change dimensions of report to add laser trials if they exist
    if len(cellObj.get_session_inds('laserPulse'))>0:
        laser = True
        gs = gridspec.GridSpec(13, 6)
    else:
        laser = False
        gs = gridspec.GridSpec(9, 6)
    offset = 4*laser
    gs.update(left=0.15, right=0.85, top = 0.96, wspace=0.7, hspace=1.0)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
     
    #load bandwidth ephys and behaviour data
    bandEphysData, bandBData = cellObj.load_by_index(bandIndex)
    bandEventOnsetTimes = ephysanalysis.get_sound_onset_times(bandEphysData, 'bandwidth')
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    timeRange = [-0.2, 1.5]
    bandEachTrial = bandBData['currentBand']
    numBands = np.unique(bandEachTrial)

    #change the trial type that the bandwidth session is split by so we can use this report for Arch-inactivation experiments
    #also changes the colours to be more thematically appropriate! (in Anna's opinion)
    if type=='laser':
        secondSort = bandBData['laserTrial']
        secondSortLabels = ['no laser','laser']
        colours = ['k', '#c4a000']
        errorColours = ['0.5', '#fce94f']
        gaussFitCol = 'gaussFit'
        tuningR2Col = 'tuningFitR2'
    elif type=='normal':
        secondSort = bandBData['currentAmp']
        secondSortLabels = ['{} dB'.format(amp) for amp in np.unique(secondSort)]
        colours = ['#4e9a06','#5c3566']
        errorColours = ['#8ae234','#ad7fa8']
        gaussFitCol = 'gaussFit'
        tuningR2Col = 'tuningFitR2'
    
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    numBands = np.unique(bandEachTrial)
            
    # -- plot rasters of the bandwidth trials --     
    rasterColours = [np.tile([colours[0],errorColours[0]],len(numBands)/2+1), np.tile([colours[1],errorColours[1]],len(numBands)/2+1)]  
    plot_separated_rasters(gs, [0,3], 5+offset, bandEachTrial, secondSort, bandSpikeTimestamps, bandEventOnsetTimes, colours=rasterColours, titles=secondSortLabels, plotHeight=2)
           
    # -- plot bandwidth tuning curves --
    plt.subplot(gs[5+offset:, 3:])
    tuningDict = ephysanalysis.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, bandTimeRange, baseRange=bandBaseRange, info='plotting')
    plot_tuning_curve(tuningDict['responseArray'], tuningDict['errorArray'], numBands, tuningDict['baselineSpikeRate'], linecolours=colours, errorcolours=errorColours)

    # load tuning ephys and behaviour data
    tuningEphysData, tuningBData = cellObj.load('tuningCurve')
    tuningEventOnsetTimes = ephysanalysis.get_sound_onset_times(tuningEphysData,'tuningCurve')
    tuningSpikeTimestamps = tuningEphysData['spikeTimes']       
    
    # -- plot frequency tuning at intensity used in bandwidth trial with gaussian fit -- 
    
    # high amp bandwidth trials used to select appropriate frequency
    maxAmp = max(np.unique(bandBData['currentAmp']))
    if maxAmp < 1:
        maxAmp = 66.0 #HARDCODED dB VALUE FOR SESSIONS DONE BEFORE NOISE CALIBRATION
    
    # find tone intensity that corresponds to tone sessions in bandwidth trial
    toneInt = maxAmp - 15.0 #HARDCODED DIFFERENCE IN TONE AND NOISE AMP BASED ON OSCILLOSCOPE READINGS FROM RIG 2

    freqEachTrial = tuningBData['currentFreq']
    
    plt.subplot(gs[2+offset:4+offset, 0:3])       
    plot_tuning_fitted_gaussian(tuningSpikeTimestamps, tuningEventOnsetTimes, tuningBData, toneInt, cell[gaussFitCol], cell[tuningR2Col], timeRange=cell['tuningTimeRange'])
            
    # -- plot frequency tuning raster --
    plt.subplot(gs[0+offset:2+offset, 0:3])
    freqLabels = ["%.1f" % freq for freq in np.unique(freqEachTrial)/1000.0]
    plot_sorted_raster(tuningSpikeTimestamps, tuningEventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=freqLabels)
    plt.title('Frequency Tuning Raster')
            
    # -- plot AM PSTH --
    amEphysData, amBData = cellObj.load('AM')
    amEventOnsetTimes = ephysanalysis.get_sound_onset_times(amEphysData, 'AM')
    amSpikeTimestamps = amEphysData['spikeTimes']   
    rateEachTrial = amBData['currentFreq']
    timeRange = [-0.2, 1.5]
    colourList = ['b', 'g', 'y', 'orange', 'r']
    
    plt.subplot(gs[2+offset:4+offset, 3:])
    plot_sorted_psth(amSpikeTimestamps, amEventOnsetTimes, rateEachTrial, timeRange = [-0.2, 0.8], binsize = 25, colorEachCond = colourList)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('AM PSTH')
    
    # -- plot AM raster --
    plt.subplot(gs[0+offset:2+offset, 3:])
    rateLabels = ["%.0f" % rate for rate in np.unique(rateEachTrial)]
    plot_sorted_raster(amSpikeTimestamps, amEventOnsetTimes, rateEachTrial, timeRange=[-0.2, 0.8], labels=rateLabels, colorEachCond=colourList)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Modulation Rate (Hz)')
    plt.title('AM Raster')
    
    # -- plot laser pulse and laser train data (if available) --
    if laser:
        # -- plot laser pulse raster -- 
        laserEphysData, noBehav = cellObj.load('laserPulse')
        laserEventOnsetTimes = laserEphysData['events']['laserOn']
        laserSpikeTimestamps = laserEphysData['spikeTimes']
        timeRange = [-0.1, 0.4]
        
        plt.subplot(gs[0:2, 0:3])
        laserSpikeTimesFromEventOnset, trialIndexForEachSpike, laserIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        laserSpikeTimestamps, laserEventOnsetTimes, timeRange)
        pRaster, hcond, zline = extraplots.raster_plot(laserSpikeTimesFromEventOnset,laserIndexLimitsEachTrial,timeRange)
        plt.xlabel('Time from laser onset (sec)')
        plt.title('Laser Pulse Raster')
        
        # -- plot laser pulse psth --
        plt.subplot(gs[2:4, 0:3])
        binsize = 10/1000.0
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserSpikeTimestamps, 
                                                                                                                       laserEventOnsetTimes, 
                                                                                                                       [timeRange[0]-binsize, 
                                                                                                                        timeRange[1]])
        binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
        pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
        plt.xlim(timeRange)
        plt.xlabel('Time from laser onset (sec)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Laser Pulse PSTH')
        
        # -- didn't record laser trains for some earlier sessions --
        if len(cellObj.get_session_inds('laserTrain')) > 0:
            # -- plot laser train raster --
            laserTrainEphysData, noBehav = cellObj.load('laserTrain')
            laserTrainEventOnsetTimes = laserTrainEphysData['events']['laserOn']
            laserTrainSpikeTimestamps = laserTrainEphysData['spikeTimes']
            laserTrainEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(laserTrainEventOnsetTimes, 0.5)
            timeRange = [-0.2, 1.0]
            
            plt.subplot(gs[0:2, 3:])
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps, 
                                                                                                                           laserTrainEventOnsetTimes, 
                                                                                                                           timeRange)
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
            plt.xlabel('Time from laser onset (sec)')
            plt.title('Laser Train Raster')
            
            # -- plot laser train psth --
            plt.subplot(gs[2:4, 3:])
            binsize = 10/1000.0
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps, 
                                                                                                                       laserTrainEventOnsetTimes, 
                                                                                                                       [timeRange[0]-binsize, 
                                                                                                                        timeRange[1]])
            binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
            pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
            plt.xlim(timeRange)
            plt.xlabel('Time from laser onset (sec)')
            plt.ylabel('Firing Rate (Hz)')
            plt.title('Laser Train PSTH')
        
    # -- show cluster analysis --
    #tsThisCluster, wavesThisCluster, recordingNumber = celldatabase.load_all_spikedata(cell)
    # -- Plot ISI histogram --
    plt.subplot(gs[4+offset, 0:2])
    spikesorting.plot_isi_loghist(bandSpikeTimestamps)

    # -- Plot waveforms --
    plt.subplot(gs[4+offset, 2:4])
    spikesorting.plot_waveforms(bandEphysData['samples'])

    # -- Plot events in time --
    plt.subplot(gs[4+offset, 4:6])
    spikesorting.plot_events_in_time(bandSpikeTimestamps)
    title = '{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            cell['depth'], 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate)

    plt.suptitle(title)
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = '{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], cell['depth'], tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(20, 25)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
    
    
# --- Methods for plotting aggregate data (not single cells) ---

def plot_categorical_scatter_with_median(vals, categoryLabels, pVals=None, alphaVal=0.05, jitter=True, colours=None, xlabel=None, ylabel=None, title=None, ylim=None):
    import pdb
    numCategories = len(vals)
    plt.hold(True)
    if colours is None:
        colours = plt.cm.gist_rainbow(np.linspace(0,1,numCategories))
    for category in range(numCategories):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[category], alpha=0.5)
        if pVals is not None:
            sigInds = pVals[category]<=alphaVal #significant values will be plotted as filled circles
        else:
            sigInds = np.tile(False, len(vals[category])) #all values plotted as empty circles if no pVals passed
        xval = (category+1)*np.ones(len(vals[category]))
        if jitter:
            jitterAmt = np.random.random(len(xval))
            xval = xval + (0.3 * jitterAmt) - 0.15
        #pdb.set_trace()
        #plt.plot(xval[sigInds], vals[category][sigInds], 'o', mec=edgeColour, mew = 2, mfc=edgeColour, ms=6, alpha=0.5)
        #plt.plot(xval[~sigInds], vals[category][~sigInds], 'o', mec=edgeColour, mew = 2, mfc='None', ms=6, alpha=0.5)
        plt.plot(xval, vals[category], 'o', mec=edgeColour, mew = 2, mfc=edgeColour, ms=6, alpha=0.5)

        median = np.median(vals[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.85,category+1.15], [median,median], '-', color='k', mec=colours[category], lw=3)
        #plt.errorbar(category+1, mean, yerr = sem, color='k', lw=2)
    plt.xlim(0,numCategories+1)
    if ylim is not None:
        plt.ylim(ylim)
    ax = plt.gca()
    ax.set_xticks(range(1,numCategories+1))
    ax.set_xticklabels(categoryLabels, fontsize=16)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:
        plt.title(title)
        
def plot_paired_scatter_with_median(vals, categoryLabels, colour='k', xlabel=None, ylabel=None, title=None, ylim=None):
    numCategories = len(vals)
    plt.hold(True)
    xvals = np.arange(numCategories)+1
    yvals = np.array(vals)
    for pair in range(len(vals[0])):
        plt.plot(xvals, yvals[:,pair], 'o-', mec='None', color=colour, ms=6, alpha=0.5)
    medians = np.median(yvals, axis=1)
    #sem = stats.sem(vals[category])
    plt.plot(xvals, medians, 'o-', color=colour, mec='None', lw=3, ms=6)
    #plt.errorbar(category+1, mean, yerr = sem, color='k', lw=2)
    plt.xlim(0,numCategories+1)
    if ylim is not None:
        plt.ylim(ylim)
    ax = plt.gca()
    ax.set_xticks(range(1,numCategories+1))
    ax.set_xticklabels(categoryLabels, fontsize=16)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:
        plt.title(title)
        
def plot_histogram_comparison(vals, categoryLabels, colours=None, xlabel=None, ylabel=None, title=None, legend=True, xlim=[0,1]):
    numCategories = len(vals)
    plt.hold(True)
    if colours is None:
        colours = plt.cm.gist_rainbow(np.linspace(0,1,numCategories))
    bins = np.linspace(0, 1, 50)
    plt.hist(vals, bins, alpha=0.7, label=categoryLabels, color=colours, lw=3, normed=True, histtype='stepfilled')
    if legend:
        plt.legend(loc='best')
    plt.xlim(xlim)
    ax = plt.gca()
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:
        plt.title(title)

def plot_histogram_of_discrete_vals(vals, categoryLabels=None, colours=None, xlabel=None, ylabel=None, title=None, legend=True):
    labels = sorted(list(set(x for l in vals for x in l)))
    plotVals = range(len(labels))
    valDict = dict(zip(labels,plotVals))
    newVals = []
    for category in range(len(vals)):
        newVals.append([valDict[i] for i in vals[category]])
    if categoryLabels is None:
        categoryLabels = ['']
    plt.hist(newVals,len(labels), alpha=0.7, label=categoryLabels, color=colours, lw=3, normed=True)
    if legend:
        plt.legend(loc='best')
    ax = plt.gca()
    ax.set_xticks(plotVals)
    ax.set_xticklabels(labels)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)