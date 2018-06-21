import os, sys
import argparse
import pdb
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import ephyscore
reload(loadopenephys)
from jaratoolbox import settings

parser = argparse.ArgumentParser(description='Generate reports for dapa mice electrophysiology')
parser.add_argument('subject', metavar='subject', help='dapa mouse to analyze')
parser.add_argument('--analyze_all', action='store_true', help='analyze all cells')
parser.add_argument('--cell', type = int, default=None, help='specific cell to analyze')
parser.add_argument('--gaussian', action='store_true', help='test Gaussian function')

args = parser.parse_args()
#Added to ephyscore
'''
def load_all_spikedata(cell):
    
    Load the spike data for all recorded sessions into a set of arrays.
    Args:
        dbRow (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
    Returns:
        timestamps (np.array): The timestamps for all spikes across all sessions
        samples (np.array): The samples for all spikes across all sessions
        recordingNumber (np.array): The index of the session where the spike was recorded
    
    samples=np.array([])
    timestamps=np.array([])
    recordingNumber=np.array([])
    #for ind, sessionType in enumerate(cell.dbRow['sessionType']):
    for ind in range(0, len(cell.dbRow['sessionType'])):
        ephysData = cell.load_ephys_by_index(ind)
        bdata = cell.load_behavior_by_index(ind)
        numSpikes = len(ephysData['spikeTimes'])
        sessionVector = np.zeros(numSpikes)+ind
        if len(samples)==0:
            samples = ephysData['samples']
            timestamps = ephysData['spikeTimes']
            recordingNumber = sessionVector
        else:
            samples = np.concatenate([samples, ephysData['samples']])
            # Check to see if next session ts[0] is lower than self.timestamps[-1]
            # If so, add self.timestamps[-1] to all new timestamps before concat
            if not len(ephysData['spikeTimes'])==0:
                #print(timestamps)
                #print(sessionType, timestamps[-1], ephysData['spikeTimes'][0])
                if ephysData['spikeTimes'][0]<timestamps[-1]:
                    ephysData['spikeTimes'] = ephysData['spikeTimes'] + timestamps[-1]
                timestamps = np.concatenate([timestamps, ephysData['spikeTimes']])
                recordingNumber = np.concatenate([recordingNumber, sessionVector])
    return timestamps, samples, recordingNumber
'''

####################################################################################

#Plot raster for noise bursts
def noise_raster(ephysData, gs):
    plt.subplot(gs[0, 1])

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.3, 0.6]
    baseTimeRange = [-0.15, -0.05]

    trialsEachCond = []

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    baseSpikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    base_avg = np.mean(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])
    base_sem = stats.sem(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond)

    title = "Noise Bursts (Base FR: {} +/- {} spikes/s)".format(round(base_avg, 2), round(base_sem, 2)) 
    #title = "Noise Bursts (Base FR: {} spikes/s)".format(round(base_avg, 2)) 
    #title = "Noise Bursts"
    xlabel = 'Time from sound onset (s)'
    ylabel = 'Trial'

    plt.title(title, fontsize = 'medium')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    '''
    print("Saving Noise Bursts for Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    '''

####################################################################################

#Plot raster for normal tuning curves
def tuning_raster(bdata, ephysData, gs):
    plt.subplot(gs[1, 1])

    freqEachTrial = bdata['currentFreq']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [-0.3, 0.6]
    baseTimeRange = [-0.15, -0.05]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)
    #print len(freqEachTrial), len(eventOnsetTimes)

    baseSpikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    base_avg = np.mean(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])
    base_sem = stats.sem(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])
    #    for freqInd, freq in enumerate(possiblefreqs):
    #        freq_spikecounts = spikeMat[trialsEachCond[:,freqInd]==True]
    #        freq_avg = np.mean(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
    #        freq_avgs.append(freq_avg)
    '''
    try:
        base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, baseIndexLimitsEachTrial)
    except:
        behavBaseIndexLimitsEachTrial = baseIndexLimitsEachTrial[0:2,:-1]
        base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavBaseIndexLimitsEachTrial)
    
    base_avg = np.mean(base_avgs)
    base_frs = np.divide(base_avg, baseTimeRange[1] - baseTimeRange[0])
    #print(base_avg)
    '''

    title = "Tuning Curve (Base FR: {} +/- {} spikes/s)".format(round(base_avg, 2), round(base_sem, 2)) 
    #title = "Tuning Curve (Base FR: {} spikes/s)".format(round(base_avg, 2)) 

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=freqLabels)


    xlabel = 'Time from sound onset (s)'
    ylabel = 'Frequency (kHz)'

    plt.title(title, fontsize = 'medium')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    '''
    print("Saving Tuning Curve for Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    '''

####################################################################################

#Plot tuning curve
def tuning_curve(bdata, ephysData, gs):
    plt.subplot(gs[2, 1])

    freqEachTrial = bdata['currentFreq']
    intEachTrial = bdata['currentIntensity']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [-0.3, 0.6]
    soundTimeRange = [0.0, 0.1]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]
    possibleInts = np.unique(intEachTrial)

    intTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, intEachTrial, possibleInts)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)
    for intInd, inten in enumerate(possibleInts):
        line = '-'
        if intInd == 0 and len(possibleInts) > 1:
            line = '--'
        curveName = str(inten) + ' dB'
        trialsEachCond = intTrialsEachCond[:,:,intInd]
        spikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, soundTimeRange)
        freq_avgs = np.empty(len(possiblefreqs))
        freq_sems = np.empty(len(possiblefreqs))
        for freqInd, freq in enumerate(possiblefreqs):
            freq_spikecounts = spikeMat[trialsEachCond[:,freqInd]==True]
            freq_avg = np.mean(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
            freq_avgs[freqInd] = freq_avg
            freq_sem = stats.sem(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
            freq_sems[freqInd] = freq_sem
        #print(spikeMat)
        #print(freq_avgs)
        '''
        try:
            freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)
        except:
            behavIndexLimitsEachTrial = indexLimitsEachTrial[0:2,:-1]
            freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavIndexLimitsEachTrial)
        
        freq_frs = np.divide(freq_avgs, timeRange[1]-timeRange[0])
        '''

        xpoints = [x for x in range(0, len(possiblefreqs))]
        xpointticks = [x for x in range(1, len(possiblefreqs), 2)]
        freqticks = [freqLabels[x] for x in range(1, len(freqLabels), 2)]
        #plt.semilogx(possiblefreqs, freq_avgs, linestyle = line, color = 'black', label = curveName)
        #plt.plot(log(possiblefreqs), freq_avgs, linestyle = line, color = 'black', label = curveName, xlabels = possiblefreqs)
        #plt.plot(xpoints, freq_avgs, linestyle = line, color = 'black', marker = 'o', label = curveName)
        #plt.errorbar(xpoints, freq_avgs, yerr = freq_stds, linestyle = line, color = 'black', marker = 'o', label = curveName)
        plt.plot(xpoints, freq_avgs, linestyle = line, color = 'black', marker = 'o', label = curveName)
        #plt.fill_between(xpoints, freq_avgs - freq_sems, freq_avgs + freq_sems, alpha = 0.1, color = 'black')
        plt.xticks(xpointticks, freqticks)
        plt.hold(True)

    xlabel = 'Frequency (kHz)'
    ylabel = 'Firing rate (spikes/s)'
    title = 'Tuning curve (time range: {})'.format(soundTimeRange)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize = 'medium')
    plt.legend(fontsize = 'x-small', loc = 'upper right', frameon=False, framealpha=100, markerscale=0.5)
    plt.hold(False)

####################################################################################

#Plot raster for laser tuning curves
def laser_tuning_raster(cell, gs):

    laserSessionInds = cell.get_session_inds('laserTuningCurve')
    for count, sessionInd in enumerate(laserSessionInds):

        bdata = cell.load_behavior_by_index(sessionInd)
        ephysData = cell.load_ephys_by_index(sessionInd)

        freqEachTrial = bdata['currentFreq']
        laserEachTrial = bdata['laserOn']
        intEachTrial = bdata['currentIntensity']
        
        eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimeStamps = ephysData['spikeTimes']

        timeRange = [-0.3, 0.6]
        baseTimeRange = [-0.15, -0.05]
        
        possiblefreqs = np.unique(freqEachTrial)
        freqLabels = [round(x/1000, 1) for x in possiblefreqs]
        possiblelaser = np.unique(laserEachTrial)
        possibleInts = np.unique(intEachTrial)

        laserOnsetTimes = ephysData['events']['laserOn']
        laserOffsetTimes = ephysData['events']['laserOff']
        laserDuration = laserOffsetTimes - laserOnsetTimes
        meanLaser = round(laserDuration.mean(), 2)
        #print(meanLaser)
        laserEventOnsetTimes = eventOnsetTimes[laserEachTrial == True]
        if len(laserOnsetTimes) > len(laserEventOnsetTimes):
            laserStartTimes = laserOnsetTimes[:-1] - laserEventOnsetTimes
        elif len(laserEventOnsetTimes) > len(laserOnsetTimes):
            laserStartTimes = laserOnsetTimes - laserEventOnsetTimes[:-1]
        else:
            laserStartTimes = laserOnsetTimes - laserEventOnsetTimes
        laserStart = round(laserStartTimes.mean(), 2)
        #print(laserStart)
        #trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)

        laserTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, laserEachTrial, possiblelaser)
        intTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, intEachTrial, possibleInts)
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)
        #plt.figure()
        
        baseSpikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
                
        for intInd, inten in enumerate(possibleInts):
            for indLaser in possiblelaser:
                #plt.subplot(2, 1, indLaser)
                ax = plt.subplot(gs[indLaser, intInd + (count * 2) + 1])
                if indLaser == 0:
                    title = "No Laser " + str(inten) + " dB"
                else:
                    title = "Laser " + str(inten) + " dB"
                trialsEachCond = laserTrialsEachCond[:,:,indLaser] & intTrialsEachCond[:,:,intInd]
                '''
                try:
                    base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, baseIndexLimitsEachTrial)
                except:
                    behavBaseIndexLimitsEachTrial = baseIndexLimitsEachTrial[0:2,:-1]
                    base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavBaseIndexLimitsEachTrial)

                base_avg = np.mean(base_avgs)
                base_frs = np.divide(base_avg, baseTimeRange[1] - baseTimeRange[0])
                '''
                trialsThisIntLaser = np.all([bdata['laserOn']==indLaser, bdata['currentIntensity']==inten], axis=0)
                baseSpikeMatThisCond = baseSpikeMat[trialsThisIntLaser==True]

                base_avg = np.mean(baseSpikeMatThisCond) / (baseTimeRange[1] - baseTimeRange[0])
                base_sem = stats.sem(baseSpikeMatThisCond) / (baseTimeRange[1] - baseTimeRange[0])

                title += " (Base FR: {} +/- {} spikes/s)".format(round(base_avg, 2), round(base_sem, 2))
                #title += " (Base FR: {} spikes/s)".format(round(base_avg, 2)) 
                pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                           trialsEachCond=trialsEachCond, labels=freqLabels)

                if indLaser == 1:
                    laserbar = patches.Rectangle((laserStart, sum(sum(trialsEachCond)) + 2), meanLaser, 5, color="b", clip_on=False)
                    #laserbar = patches.Rectangle((-0.05, 10), 2.0, 5, color="b")
                    ax.add_patch(laserbar)

                xlabel = 'Time from sound onset (s)'
                ylabel = 'Frequency (kHz)'

                plt.title(title, fontsize = 'medium')
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
        '''
        #plt.setp(pRaster, ms=ms)
        print("Saving Laser Tuning Curve for Cell " + str(indRow))
        figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
        plt.savefig(figname)
        
        plt.clf()
        #plt.show()
        '''

####################################################################################

#Plot laser tuning curve
def laser_tuning_curve(cell, gs):
    #plt.subplot(gs[3, 1])
    laserSessionInds = cell.get_session_inds('laserTuningCurve')
    for count, sessionInd in enumerate(laserSessionInds):

        bdata = cell.load_behavior_by_index(sessionInd)
        ephysData = cell.load_ephys_by_index(sessionInd)

        freqEachTrial = bdata['currentFreq']
        laserEachTrial = bdata['laserOn']
        intEachTrial = bdata['currentIntensity']
        
        eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimeStamps = ephysData['spikeTimes']

        timeRange = [-0.3, 0.6]
        soundTimeRange = [0.0, 0.1]

        possiblefreqs = np.unique(freqEachTrial)
        freqLabels = [round(x/1000, 1) for x in possiblefreqs]
        possiblelaser = np.unique(laserEachTrial)
        possibleInts = np.unique(intEachTrial)

        laserTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, laserEachTrial, possiblelaser)
        intTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, intEachTrial, possibleInts)
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

        for intInd, inten in enumerate(possibleInts):
            plt.subplot(gs[2,intInd+(count * 2)+1])
            line = '-'
            #if intInd == 0:
            #    line = '--'
            for indLaser in possiblelaser:
                color = 'black'
                if indLaser == 1:
                    color = 'blue'

                laser = 'No Laser'
                if indLaser == 1:
                    laser = 'Laser'
                curveName = laser + str(inten) + ' dB'

                trialsEachCond = laserTrialsEachCond[:,:,indLaser] & intTrialsEachCond[:,:,intInd]
                spikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, soundTimeRange)
                freq_avgs = np.empty(len(possiblefreqs))
                freq_sems = np.empty(len(possiblefreqs))
                for freqInd, freq in enumerate(possiblefreqs):
                    freq_spikecounts = spikeMat[trialsEachCond[:,freqInd]==True]
                    freq_avg = np.mean(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
                    freq_avgs[freqInd] = freq_avg
                    freq_sem = stats.sem(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
                    freq_sems[freqInd] = freq_sem
                '''
                try:
                    freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)
                    base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, baseIndexLimitsEachTrial)
                except:
                    behavIndexLimitsEachTrial = indexLimitsEachTrial[0:2,:-1]
                    freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavIndexLimitsEachTrial)
                
                freq_frs = np.divide(freq_avgs, timeRange[1]-timeRange[0])
                #print(freq_avgs, freq_frs) 
                '''
                xpoints = [x for x in range(0, len(possiblefreqs))]
                xpointticks = [x for x in range(1, len(possiblefreqs), 2)]
                freqticks = [freqLabels[x] for x in range(1, len(freqLabels), 2)]
                #plt.semilogx(possiblefreqs, freq_avgs, linestyle = line, color = color, label = curveName)
                #plt.plot(xvalues, freq_avgs, linestyle = line, color = 'black', label = curveName, xlabels = possiblefreqs)
                #plt.plot(xpoints, freq_avgs, linestyle = line, color = color, marker = 'o', label = laser)
                #plt.errorbar(xpoints, freq_avgs, yerr = freq_stds, linestyle = line, color = color, marker = 'o', label = laser)
                plt.plot(xpoints, freq_avgs, linestyle = line, color = color, marker = 'o', label = laser)
                #plt.fill_between(xpoints, freq_avgs - freq_sems, freq_avgs + freq_sems, alpha = 0.1, color = color)
                plt.xticks(xpointticks, freqticks)
                plt.hold(True)
                
            xlabel = 'Frequency (kHz)'
            ylabel = 'Firing rate (spikes/s)'
            title = str(inten) + ' dB Tuning curve (time range: {})'.format(soundTimeRange)

            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title, fontsize = 'medium')
            plt.legend(fontsize = 'x-small', loc = 'upper right', frameon=False, framealpha=100, markerscale=0.5)
        plt.hold(False)

####################################################################################

#Plot raster for am sessions
def am_raster(bdata, ephysData, gs):
    plt.subplot(gs[1, 1])

    freqEachTrial = bdata['currentFreq']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [-0.3, 0.6]
    baseTimeRange = [-0.15, -0.05]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)
    #print len(freqEachTrial), len(eventOnsetTimes)

    baseSpikeMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    base_avg = np.mean(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])
    base_sem = stats.sem(baseSpikeMat) / (baseTimeRange[1] - baseTimeRange[0])
    #    for freqInd, freq in enumerate(possiblefreqs):
    #        freq_spikecounts = spikeMat[trialsEachCond[:,freqInd]==True]
    #        freq_avg = np.mean(freq_spikecounts) / (soundTimeRange[1] - soundTimeRange[0])
    #        freq_avgs.append(freq_avg)
    '''
    try:
        base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, baseIndexLimitsEachTrial)
    except:
        behavBaseIndexLimitsEachTrial = baseIndexLimitsEachTrial[0:2,:-1]
        base_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavBaseIndexLimitsEachTrial)
    
    base_avg = np.mean(base_avgs)
    base_frs = np.divide(base_avg, baseTimeRange[1] - baseTimeRange[0])
    #print(base_avg)
    '''

    title = "Tuning Curve (Base FR: {} +/- {} spikes/s)".format(round(base_avg, 2), round(base_sem, 2)) 
    #title = "Tuning Curve (Base FR: {} spikes/s)".format(round(base_avg, 2)) 

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=freqLabels)


    xlabel = 'Time from sound onset (s)'
    ylabel = 'Frequency (kHz)'

    plt.title(title, fontsize = 'medium')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    '''
    print("Saving Tuning Curve for Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    '''

####################################################################################

def gaussian(x, a, x0, sigma, y0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + y0

####################################################################################

def plot_gaussian(cell, gs):
    laserTuningSessionInds = cell.get_session_inds('laserTuningCurve')

    if len(laserTuningSessionInds) != 0:
        for sessionInd in laserTuningSessionInds:
            bdata = cell.load_behavior_by_index(sessionInd)
            ephysData = cell.load_ephys_by_index(sessionInd)
    else:
        return

    freqEachTrial = bdata['currentFreq']
    laserEachTrial = bdata['laserOn']
    intEachTrial = bdata['currentIntensity']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [-0.3, 0.6]
    baseTimeRange = [0.0, 0.1]
    alignmentRange = [baseTimeRange[0], timeRange[1]]   

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]
    possiblelaser = np.unique(laserEachTrial)
    possibleInts = np.unique(intEachTrial)

    #Init list to hold the optimized parameters for the gaussian for each intensity and laser
    popts = []
    Rsquareds = []

    #Init arrays to hold the baseline and response spike counts per condition
    allLaserIntenBase = np.array([])
    allLaserIntenResp = np.empty((len(possiblelaser), len(possibleInts), len(possiblefreqs)))
    allLaserIntenRespMedian = np.empty((len(possiblelaser), len(possibleInts), len(possiblefreqs)))

    for indlaser, laser in enumerate(possiblelaser):
        for indinten, inten in enumerate(possibleInts):
            spks = np.array([])
            freqs = np.array([])
            base = np.array([])
            for indfreq, freq in enumerate(possiblefreqs):
                selectinds = np.flatnonzero((freqEachTrial==freq)&(intEachTrial==inten)&(laserEachTrial==laser))
                selectedOnsetTimes = eventOnsetTimes[selectinds]
                (spikeTimesFromEventOnset,
                trialIndexForEachSpike,
                indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps,
                                                                            selectedOnsetTimes,
                                                                            alignmentRange)
                nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    baseTimeRange)
                nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    timeRange)
                base = np.concatenate([base, nspkBase.ravel()])
                spks = np.concatenate([spks, nspkResp.ravel()])
                # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
                freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])
                allLaserIntenBase = np.concatenate([allLaserIntenBase, nspkBase.ravel()])
                allLaserIntenResp[indlaser, indinten, indfreq] = np.mean(nspkResp)
                allLaserIntenRespMedian[indlaser, indinten, indfreq] = np.median(nspkResp)

            try:
                popt, pcov = optimize.curve_fit(gaussian, #Fit the curve for this intensity
                                                np.log2(freqs),
                                                spks,
                                                p0=[1, np.log2(possiblefreqs[7]), 1, allLaserIntenBase.mean()],
                                                #bounds=([0, np.log2(possiblefreqs[0]), 0, 0],
                                                #        [inf, np.log2(possiblefreqs[-1]), inf, inf])
                                                )
                popts.append(popt) #Save the curve paramaters

                ## Calculate the R**2 value for the fit
                fittedSpks = gaussian(np.log2(freqs), *popt)
                residuals = spks - fittedSpks
                SSresidual = np.sum(residuals**2)
                SStotal = np.sum((spks-np.mean(spks))**2)
                Rsquared = 1-(SSresidual/SStotal)
                Rsquareds.append(Rsquared)

            except RuntimeError:
                '''
                failed=True
                print "RUNTIME ERROR, Cell {}".format(indIter)
                runtimeErrorInds.append(indIter)
                thresholds[indIter] = None
                cfs[indIter] = None
                lowerFreqs[indIter] = None
                upperFreqs[indIter] = None
                '''
                print "RUNTIME ERROR, Cell {}".format(indIter)
                popts.append([np.nan, np.nan, np.nan, np.nan])
                Rsquareds.append(np.nan)
                continue
            
            #plt.figure()
            #print(gaussian(popt[1], *popt))
            #plt.plot(np.log2(freqs), gaussian(np.log2(freqs), *popt))
            #plt.show()



    print(popts)
    print(Rsquareds)


####################################################################################

def cluster_stats(cell, gs):

    (timestamps,
    samples,
    recordingNumber) = cell.load_all_spikedata()

    #ISI loghist
    plt.subplot(gs[0, 0])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            # raise AttributeError
            print("problem with isi vals")

    #Waveforms
    plt.subplot(gs[1, 0])
    if len(samples)>0:
        spikesorting.plot_waveforms(samples)

    #Events in time
    plt.subplot(gs[2, 0])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print("problem with isi vals")

####################################################################################

def generate_report(indRow, dbRow):
    #Create a cell object using the database row
    print(indRow)
    cell = ephyscore.Cell(dbRow)

    #Find the inds for the noiseburst sessions
    noiseSessionInds = cell.get_session_inds('noisebursts')

    #Find the inds for the laser tuning curve sessions
    laserTuningSessionInds = cell.get_session_inds('laserTuningCurve')

    #Go through the tuning curve sessions and plot the rasters
    if len(laserTuningSessionInds) <= 1:
        return

    plt.figure(figsize = (18, 10), frameon = False)

    gs = gridspec.GridSpec(3, 5)
    gs.update(hspace=0.4)
    gs.update(wspace=0.3)

    if args.gaussian:
        plot_gaussian(cell, gs)
               
    #Plot cluster stats for all sessions
    #try:
    cluster_stats(cell, gs)
    #except:
        #print('spikes error')

    try:
        laser_tuning_raster(cell, gs)
        laser_tuning_curve(cell, gs)
    except:
        print("no laser tuning curve")
    

    print("Saving Cell {} ({} {} depth {} T{} C{})".format(indRow, subject, dbRow['date'], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster']))
    figTitle = '{} {} depth {} T{} C{}'.format(subject, dbRow['date'], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    #figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.figtext(0.5,0.95,figTitle,ha='center',fontweight='bold',fontsize=14)
    figname = finaldir + '{}_depth{}_T{}_C{}.png'.format(dbRow['date'], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.close()

    '''
    #Go through the noiseburst sessions and plot the rasters
    if len(noiseSessionInds) != 0:
        for sessionInd in noiseSessionInds:
            try:
                ephysData = cell.load_ephys_by_index(sessionInd)
                noise_raster(ephysData, gs)
            except:
                print("no noiseburst")

    #Find the inds for the tuning curve sessions
    tuningSessionInds = cell.get_session_inds('tuningCurve')

    #Go through the tuning curve sessions and plot the rasters
    if len(tuningSessionInds) != 0:
        for sessionInd in tuningSessionInds:
            try:
                bdata = cell.load_behavior_by_index(sessionInd)
                ephysData = cell.load_ephys_by_index(sessionInd)
                tuning_raster(bdata, ephysData, gs)
                tuning_curve(bdata, ephysData, gs)
            except:
                print("no tuning curve")
    '''

####################################################################################

subject = args.subject
#subject = dapa011
dbpath = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
db = pd.read_hdf(dbpath, key='database')

finaldir = '/home/jarauser/data/reports_alex/{}/tc_control_test/'.format(subject)

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')
goodCells = goodCells.reset_index(drop=True)

if args.cell:
    dbRow = goodCells.loc[args.cell]
    generate_report(args.cell, dbRow)
    sys.exit()

if not args.analyze_all:
    current = os.listdir(finaldir)
    date_list = []
    for cell in current:
        date = cell.split('_')[0]
        if date not in date_list:
            date_list.append(date)
    #print(len(goodCells))
    newCells = goodCells
    for ind, cell in goodCells.iterrows():
        if cell['date'] in date_list:
            newCells = newCells.drop([ind])
    #print(len(newCells))
    goodCells = newCells

for indRow, dbRow in goodCells.iterrows():
    generate_report(indRow, dbRow)
    

    '''
    try:
        sessionInds = cell.get_session_inds('laserTuningCurve')
        print(sessionInds)
    except:
        continue
    if len(sessionInds) == 0:
        continue
    for sessionInd in sessionInds:
        #Get the bdata for this session
        try:
            bdata = cell.load_behavior_by_index(sessionInd)
        except:
            continue

        #Look at something in the bdata
        if bdata['numTones'][0]==16:
            indToUse=sessionInd
            break #We keep this bdata and use this sessionInd

    #get the spikeData for this ind (we might already have the bdata because we just loaded it)
    try:
        ephysData = cell.load_ephys_by_index(indToUse)
    except:
        continue
    '''

sys.exit()
