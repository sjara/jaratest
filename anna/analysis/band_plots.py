from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
import band_ephys_analysis as bandan
reload(bandan)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import stats
import os

#REMOVE LATER
from jaratest.nick.database import dataplotter

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

def plot_tuning_curve(spikeArray, errorArray, xvals, baselineSpikeRate = None, legend = False, labels = ['50 dB SPL', '70 dB SPL'], linecolours = None, errorcolours = None, timeRange = [0,1], title=None):
    xrange = range(len(xvals))
    lines = []
    if linecolours is None:
        linecolours = errorcolours = plt.cm.rainbow(np.linspace(0,1,spikeArray.shape[1]))
    if baselineSpikeRate is not None:
        plt.plot(xrange, baselineSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(xvals)), color = '0.75', linewidth = 2)
    for cond in range(spikeArray.shape[1]):
        l1,=plt.plot(xrange, spikeArray[:,cond].flatten(), '-o', color = linecolours[cond], linewidth = 3)
        lines.append(l1)
        plt.fill_between(xrange, spikeArray[:,cond].flatten() - errorArray[:,cond].flatten(), 
                     spikeArray[:,cond].flatten() + errorArray[:,cond].flatten(), alpha=0.2, edgecolor = errorcolours[cond], facecolor=errorcolours[cond])
    ax = plt.gca()
    ax.set_xticks(xrange)
    ax.set_xticklabels(xvals)
    ax.set_ylim(bottom=0)
    plt.xlabel('bandwidth (octaves)')
    plt.ylabel('Firing rate (Hz)')
    if legend: 
        plt.legend(lines,labels, borderaxespad=0., loc='best')
    if title:
        plt.title(title)

def plot_tuning_fitted_gaussian(spikeTimeStamps, eventOnsetTimes, tuningBData, toneInt, gaussFit, Rsquared):
    freqEachTrial = tuningBData['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    
    intensityEachTrial = tuningBData['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)
    if toneInt in numIntensities:
        intensityInd = np.where(numIntensities==toneInt)
    # use closest tone intensity if desired one was not presented
    else:
        intensityInd = (np.abs(numIntensities-toneInt)).argmin()
    
    spikeArray, errorArray, baselineSpikeRate = bandan.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, freqEachTrial, intensityEachTrial, [0.0,0.1], [0.0,0.7])
    tuningArray = spikeArray[:,intensityInd].flatten()
    
    #plot true tuning curve
    plt.plot(np.log2(numFreqs),tuningArray, 'k-')
    #plot estimated gaussian curve
    x_fine = np.linspace(np.log2(numFreqs)[0], np.log2(numFreqs)[-1], 100)
    plt.plot(x_fine, bandan.gaussian(x_fine, gaussFit[0], gaussFit[1], gaussFit[2], gaussFit[3]), 'r--')
    
    plt.xlim(np.log2(numFreqs)[0], np.log2(numFreqs)[-1])
    
    ax = plt.gca()
    ax.annotate('R^2 = {0}'.format(Rsquared), xy=(0.1, 0.9), xycoords='axes fraction')
    ax.set_xticks(np.log2(numFreqs))
    ax.set_xticklabels(labels)
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('Frequency tuning at {} dB'.format(toneInt))


# --- Methods for plotting reports with multiple plots ---

def plot_harmonics_summary(cell, harmIndex=None, bandIndex=None):
    if harmIndex is None:
        try:
            harmIndex = bandan.get_session_inds(cell, 'harmonics')[0]
        except IndexError:
            print 'No harmonics session'
            return
    plt.clf()
    gs = gridspec.GridSpec(3, 2)
    gs.update(left=0.15, right=0.85, top = 0.95, wspace=0.2, hspace=0.3)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #load harmonics ephys data
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][harmIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    timeRange = [-0.2, 1.5]
    
    #load harmonics behaviour data
    harmBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][harmIndex])  
    
    bandEachTrial = harmBData['currentBand']
    secondSort = harmBData['harmTrialType']
    secondSortLabels = ['noise','harmonics']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    #plot rasters of the noise and harmonics trials        
    firstSortLabels = ['{}'.format(band) for band in np.unique(bandEachTrial)]     
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           secondSort, 
                                                                           numSec) 
    colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]
    plot_separated_rasters(gs, [0,1], 1, bandEachTrial, secondSort, spikeTimeStamps, eventOnsetTimes, titles=['Noise','Harmonics'], duplicate=True, colours=colours)
    
    #plot a response curve of the noise and harmonics trials
    plt.subplot(gs[1:, 1:])
    timeRange = [0,1.0]
    spikeArray, errorArray, baselineSpikeRate = bandan.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange)
    spikeArray[0,0]=spikeArray[0,1]
    errorArray[0,0]=errorArray[0,1]
    plot_tuning_curve(spikeArray, errorArray, numBands, baselineSpikeRate, legend=True, labels=['noise','harmonics'], linecolours=['#4e9a06','#5c3566'], errorcolours=['#8ae234','#ad7fa8'])
    
    #load frequency tuning data and plot frequency tuning raster
    plt.subplot(gs[0, 0])
    tuningIndex = bandan.get_session_inds(cell, 'tuningCurve')[-1]
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][tuningIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    
    tuningBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][tuningIndex])
    freqEachTrial = tuningBData['currentFreq']
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    plot_sorted_raster(spikeTimeStamps, eventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=labels)
    
    #load bandwidth tuning data and plot bandwidth tuning curve
    plt.subplot(gs[0,1])
    if bandIndex is None:
        bandIndex = bandan.get_session_inds(cell, 'bandwidth')[0]
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][bandIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    
    bandBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][bandIndex])
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    spikeArray, errorArray, baselineSpikeRate = bandan.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange)
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
    if bandIndex is None:
        try:
            bandIndex = bandan.get_session_inds(cell, 'bandwidth')[0]
        except IndexError:
            print 'No bandwidth session'
            return
    plt.clf()
    gs = gridspec.GridSpec(3, 2)
    gs.update(left=0.15, right=0.85, top = 0.95, wspace=0.2, hspace=0.3)
    
    tetrode=int(cell['tetrode'])
    cluster=int(cell['cluster'])
    
    #load bandwidth ephys data
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][bandIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    timeRange = [-0.2, 1.5]
    
    #load bandwidth behaviour data
    bandBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][bandIndex])  
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    #plot rasters of the bandwidth trials        
    colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]
    plot_separated_rasters(gs, [0,1], 1, bandEachTrial, secondSort, spikeTimeStamps, eventOnsetTimes, colours=colours)
    
    #plot bandwidth tuning curve
    plt.subplot(gs[1:,1])
    spikeArray, errorArray, baselineSpikeRate = bandan.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange)
    plot_tuning_curve(spikeArray, errorArray, numBands, baselineSpikeRate, linecolours=['#4e9a06','#5c3566'], errorcolours=['#8ae234','#ad7fa8'])
    
    #load frequency tuning data and plot frequency tuning raster
    plt.subplot(gs[0, 0])
    tuningIndex = bandan.get_session_inds(cell, 'tuningCurve')[-1]
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][tuningIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    
    tuningBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][tuningIndex])
    freqEachTrial = tuningBData['currentFreq']
    labels = ['%.1f' % f for f in np.unique(freqEachTrial)/1000]
    plot_sorted_raster(spikeTimeStamps, eventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=labels)
    
    #plot frequency tuning heat map
    intensityEachTrial = tuningBData['currentIntensity']
    plt.subplot(gs[0,1])
    dataplotter.two_axis_heatmap(spikeTimeStamps, eventOnsetTimes, intensityEachTrial, freqEachTrial, firstSortLabels=["%.0f" % inten for inten in np.unique(intensityEachTrial)], secondSortLabels=labels, xlabel='Frequency (kHz)', ylabel='Intensity (dB SPL)',flipFirstAxis=False)
    plt.ylabel('Intensity (dB SPL)')
    plt.xlabel('Frequency (kHz)')
    
    #save report
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            cell['depth'], 
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
    

def plot_bandwidth_report(cell, bandIndex=None, type='normal'):
    if bandIndex is None:
        try:
            bandIndex = bandan.get_session_inds(cell, 'bandwidth')[0]
        except IndexError:
            print 'No bandwidth session'
            return
    #change dimensions of report to add laser trials if they exist
    if len(bandan.get_session_inds(cell, 'laserPulse'))>0:
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
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][bandIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    bandBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][bandIndex])
    
    timeRange = [-0.2, 1.5]
    bandEachTrial = bandBData['currentBand']
    numBands = np.unique(bandEachTrial)

    #change the trial type that the bandwidth session is split by so we can use this report for Arch-inactivation experiments
    #also changes the colours to be more thematically appropriate! (in Anna's opinion)
    if type=='laser':
        secondSort = bandBData['laserTrial']
        secondSortLabels = ['no laser','laser'] 
    elif type=='normal':
        secondSort = bandBData['currentAmp']
        secondSortLabels = ['{} dB'.format(amp) for amp in np.unique(secondSort)]
        colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]

    
    charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
    modrate = str(np.unique(bandBData['modRate'])[0])
    numBands = np.unique(bandEachTrial)
            
    # -- plot rasters of the bandwidth trials --       
    plot_separated_rasters(gs, [0,3], 5+offset, bandEachTrial, secondSort, spikeTimeStamps, eventOnsetTimes, colours=colours, titles=secondSortLabels, plotHeight=2)
           
    # -- plot bandwidth tuning curves --
    plt.subplot(gs[5+offset:, 3:])
    timeRange = [0.0, 1.0] if type=='normal' else [0.1, 1.1]
    spikeArray, errorArray, baselineSpikeRate = bandan.calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange)
    plot_tuning_curve(spikeArray, errorArray, numBands, baselineSpikeRate, linecolours=['#4e9a06','#5c3566'], errorcolours=['#8ae234','#ad7fa8'])

    # load tuning ephys and behaviour data
    tuningIndex = bandan.get_session_inds(cell, 'tuningCurve')[-1]
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][tuningIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    tuningBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][tuningIndex])        
    
    # -- plot frequency tuning at intensity used in bandwidth trial with gaussian fit -- 
    
    # high amp bandwidth trials used to select appropriate frequency
    maxAmp = max(np.unique(bandBData['currentAmp']))
    if maxAmp < 1:
        maxAmp = 66.0 #HARDCODED dB VALUE FOR SESSIONS DONE BEFORE NOISE CALIBRATION
    
    # find tone intensity that corresponds to tone sessions in bandwidth trial
    toneInt = maxAmp - 15.0 #HARDCODED DIFFERENCE IN TONE AND NOISE AMP BASED ON OSCILLOSCOPE READINGS FROM RIG 2

    freqEachTrial = tuningBData['currentFreq']
    
    plt.subplot(gs[2+offset:4+offset, 0:3])       
    plot_tuning_fitted_gaussian(spikeTimeStamps, eventOnsetTimes, tuningBData, toneInt, cell['gaussFit'], cell['tuningFitR2'])
            
    # -- plot frequency tuning raster --
    plt.subplot(gs[0+offset:2+offset, 0:3])
    freqLabels = ["%.1f" % freq for freq in np.unique(freqEachTrial)/1000.0]
    plot_sorted_raster(spikeTimeStamps, eventOnsetTimes, freqEachTrial, timeRange=[-0.2,0.6], labels=freqLabels)
    plt.title('Frequency Tuning Raster')
            
    # -- plot AM PSTH --
    amIndex = bandan.get_session_inds(cell, 'AM')[-1]
    eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][amIndex], tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    
    amBData = bandan.load_behaviour_data(cell['subject'], cell['behavior'][amIndex])  
    rateEachTrial = amBData['currentFreq']
    timeRange = [-0.2, 1.5]
    colourList = ['b', 'g', 'y', 'orange', 'r']
    
    plt.subplot(gs[2+offset:4+offset, 3:])
    plot_sorted_psth(spikeTimeStamps, eventOnsetTimes, rateEachTrial, timeRange = [-0.2, 0.8], binsize = 25, colorEachCond = colourList)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('AM PSTH')
    
    # -- plot AM raster --
    plt.subplot(gs[0+offset:2+offset, 3:])
    rateLabels = ["%.0f" % rate for rate in np.unique(rateEachTrial)]
    plot_sorted_raster(spikeTimeStamps, eventOnsetTimes, rateEachTrial, timeRange=[-0.2, 0.8], labels=rateLabels, colorEachCond=colourList)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Modulation Rate (Hz)')
    plt.title('AM Raster')
    
    # -- plot laser pulse and laser train data (if available) --
    if laser:
        # -- plot laser pulse raster -- 
        laserIndex = bandan.get_session_inds(cell, 'laserPulse')[-1]
        eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][laserIndex], tetrode, cluster)
        eventOnsetTimes = eventData.get_event_onset_times()
        spikeTimeStamps = spikeData.timestamps
        timeRange = [-0.1, 0.4]
        
        plt.subplot(gs[0:2, 0:3])
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)
        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
        plt.xlabel('Time from sound onset (sec)')
        plt.title('Laser Pulse Raster')
        
        # -- plot laser pulse psth --
        plt.subplot(gs[2:4, 0:3])
        binsize = 10
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       [timeRange[0]-binsize, 
                                                                                                                        timeRange[1]])
        binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
        pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
        plt.xlabel('Time from sound onset (sec)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Laser Pulse PSTH')
        
        # -- didn't record laser trains for some earlier sessions --
        laserTrainIndex = bandan.get_session_inds(cell, 'laserTrain')
        if len(laserTrainIndex) > 0:
            # -- plot laser train raster --
            laserTrainIndex = laserTrainIndex[-1]
            eventData, spikeData = bandan.load_ephys_data(cell['subject'], cell['ephys'][laserTrainIndex], tetrode, cluster)
            eventOnsetTimes = eventData.get_event_onset_times()
            spikeTimeStamps = spikeData.timestamps
            timeRange = [-0.2, 1.0]
            
            plt.subplot(gs[0:2, 3:])
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                           eventOnsetTimes, 
                                                                                                                           timeRange)
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
            plt.xlabel('Time from sound onset (sec)')
            plt.title('Laser Train Raster')
            
            # -- plot laser train psth --
            plt.subplot(gs[2:4, 3:])
            binsize = 10
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       [timeRange[0]-binsize, 
                                                                                                                        timeRange[1]])
            binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
            pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
            plt.xlabel('Time from sound onset (sec)')
            plt.ylabel('Firing Rate (Hz)')
            plt.title('Laser Train PSTH')
        
    # -- show cluster analysis --
    tsThisCluster, wavesThisCluster, recordingNumber = celldatabase.load_all_spikedata(cell)
    
    # -- Plot ISI histogram --
    plt.subplot(gs[4+offset, 0:2])
    spikesorting.plot_isi_loghist(tsThisCluster)
    plt.ylabel('c%d'%cluster,rotation=0,va='center',ha='center')
    plt.xlabel('')

    # -- Plot waveforms --
    plt.subplot(gs[4+offset, 2:4])
    spikesorting.plot_waveforms(wavesThisCluster)

    # -- Plot events in time --
    plt.subplot(gs[4+offset, 4:6])
    spikesorting.plot_events_in_time(tsThisCluster)

    plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cell['subject'], 
                                                                                            cell['date'], 
                                                                                            cell['depth'], 
                                                                                            tetrode, 
                                                                                            cluster, 
                                                                                            charfreq, 
                                                                                            modrate))
    
    fig_path = '/home/jarauser/Pictures/cell reports'
    fig_name = '{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cell['subject'], cell['date'], cell['depth'], tetrode, cluster)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(20, 25)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')