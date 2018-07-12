''' THIS IS TO TEST analysis of effects of laser inactivation of PV/SOM cells on firing rate during noise bursts'''
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from jaratoolbox import celldatabase
reload(celldatabase)
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

from jaratest.anna.analysis import band_plots

import pdb


import subjects_info

CASE = 2

dbFilename = os.path.join(settings.DATABASE_PATH,'inactivation_cells.h5')
db = celldatabase.load_hdf(dbFilename)

bestCells = db[db['sustainedSuppressionIndexLaser'].notnull()]
noPV = bestCells.loc[bestCells['subject'].isin(subjects_info.PV_ARCHT_MICE)]
noSOM = bestCells.loc[bestCells['subject'].isin(subjects_info.SOM_ARCHT_MICE)]

cells = [noPV, noSOM]

if CASE == 0:
    PSTHs = []
    laserPSTHs = []
    
    PSTHs2 = []
    laserPSTHs2 = []
    
    for ind, cellsThisType in enumerate(cells):
        thisCellTypePSTHs = None
        thisCellTypeLaserPSTHs = None
        thisCellTypePSTHs2 = None
        thisCellTypeLaserPSTHs2 = None
        for indCell in range(len(cellsThisType)):
            cell = cellsThisType.iloc[indCell]
            cellObj = ephyscore.Cell(cell)
            noiseEphysData, noBehav = cellObj.load('noisebursts')
            laserNoiseEphysData, noBehav = cellObj.load('lasernoisebursts')
            
            noiseEventOnsetTimes = noiseEphysData['events']['soundDetectorOn']
            laserEventOnsetTimes = laserNoiseEphysData['events']['soundDetectorOn']
            
            noiseSpikeTimestamps = noiseEphysData['spikeTimes']
            laserSpikeTimestamps = laserNoiseEphysData['spikeTimes']
            
            noiseTimeRange = [-0.3, 0.5]
            binsize = 50 #in milliseconds
            noiseSpikeTimesFromEventOnset, trialIndexForEachSpike, noiseIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                            noiseSpikeTimestamps, 
                                                                                                            noiseEventOnsetTimes,
                                                                                                            [noiseTimeRange[0]-binsize, noiseTimeRange[1]+2*(binsize/1000.0)])
            laserSpikeTimesFromEventOnset, trialIndexForEachSpike, laserIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                            laserSpikeTimestamps, 
                                                                                                            laserEventOnsetTimes,
                                                                                                            [noiseTimeRange[0]-binsize, noiseTimeRange[1]+2*(binsize/1000.0)])
            
            binEdges = np.around(np.arange(noiseTimeRange[0]-(binsize/1000.0), noiseTimeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
            
            if thisCellTypePSTHs is None:
                thisCellTypePSTHs = []
                thisCellTypeLaserPSTHs = []
                thisCellTypePSTHs2 = []
                thisCellTypeLaserPSTHs2 = []
            noiseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(noiseSpikeTimesFromEventOnset, noiseIndexLimitsEachTrial, binEdges)
            laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(laserSpikeTimesFromEventOnset, laserIndexLimitsEachTrial, binEdges)
            
            thisNoisePSTH = np.mean(noiseSpikeCountMat,axis=0)
            thisLaserPSTH = np.mean(laserSpikeCountMat,axis=0)
    
            if (thisNoisePSTH[0]!=0) and (thisLaserPSTH[0]!=0):
                thisNoisePSTH1 = thisNoisePSTH/thisNoisePSTH[0] #normalise so baseline is 1
                thisLaserPSTH1 = thisLaserPSTH/thisLaserPSTH[0]
                
                thisCellTypePSTHs.append(thisNoisePSTH1)
                thisCellTypeLaserPSTHs.append(thisLaserPSTH1)
                
            if (thisNoisePSTH[5]!=0) and (thisLaserPSTH[5]!=0):    
                thisNoisePSTH2 = thisNoisePSTH/thisNoisePSTH[5] #normalise so baseline with laser is 1
                thisLaserPSTH2 = thisLaserPSTH/thisLaserPSTH[5]
                
                thisCellTypePSTHs2.append(thisNoisePSTH2)
                thisCellTypeLaserPSTHs2.append(thisLaserPSTH2)
            
            #pdb.set_trace()
        PSTHs.append(thisCellTypePSTHs)
        laserPSTHs.append(thisCellTypeLaserPSTHs)
        PSTHs2.append(thisCellTypePSTHs2)
        laserPSTHs2.append(thisCellTypeLaserPSTHs2)
    
    
    
    #plot all this garbage
    for ind in range(2):
        plt.figure()
        for ind2 in range(len(PSTHs[ind])):
            plt.plot(binEdges[:-1], PSTHs[ind][ind2], 'k-', alpha=0.2)
            plt.plot(binEdges[:-1], laserPSTHs[ind][ind2], 'y-', alpha=0.2)
            
        meanPSTH = np.mean(PSTHs[ind], axis=0)
        meanLaserPSTH = np.mean(laserPSTHs[ind], axis=0)
        
        plt.plot(binEdges[:-1], meanPSTH, 'k-', lw=5)
        plt.plot(binEdges[:-1], meanLaserPSTH, 'y-', lw=5)
        plt.xlabel('Time from sound onset')
        plt.ylabel('Normalised spike rate')
        if ind==0:
            plt.title('no PV, normal baseline')
        else:
            plt.title('no SOM, normal baseline')
    
    for ind in range(2):
        plt.figure()
        for ind2 in range(len(PSTHs2[ind])):
            plt.plot(binEdges[:-1], PSTHs2[ind][ind2], 'k-', alpha=0.2)
            plt.plot(binEdges[:-1], laserPSTHs2[ind][ind2], 'y-', alpha=0.2)
            
        meanPSTH2 = np.mean(PSTHs2[ind], axis=0)
        meanLaserPSTH2 = np.mean(laserPSTHs2[ind], axis=0)
        
        plt.plot(binEdges[:-1], meanPSTH2, 'k-', lw=5)
        plt.plot(binEdges[:-1], meanLaserPSTH2, 'y-', lw=5)
        plt.xlabel('Time from sound onset')
        plt.ylabel('Normalised spike rate')
        if ind==0:
            plt.title('no PV, laser baseline')
        else:
            plt.title('no SOM, laser baseline')        
    
    plt.show()
    
elif CASE == 1:
    bandPSTHs = []
    
    for ind, cellsThisType in enumerate(cells):
        thisCellTypeAllPSTHs = None
        
        thisCellTypeAllPSTHs2 = None
        
        for indCell in range(len(cellsThisType)):
            cell = cellsThisType.iloc[indCell]
            cellObj = ephyscore.Cell(cell)
            bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandSession']))
            bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
            bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            
            bandTimeRange = [-0.5, 1.5]
            binsize = 50 #in milliseconds
            
            bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                            bandSpikeTimestamps, 
                                                                                                            bandEventOnsetTimes,
                                                                                                            [bandTimeRange[0]-binsize, bandTimeRange[1]+2*(binsize/1000.0)])
            
            numBands = np.unique(bandBData['currentBand'])
            numLas = np.unique(bandBData['laserTrial'])
            trialsEachCond = behavioranalysis.find_trials_each_combination(bandBData['currentBand'], 
                                                                       numBands, 
                                                                       bandBData['laserTrial'], 
                                                                       numLas)

            binEdges = np.around(np.arange(bandTimeRange[0]-(binsize/1000.0), bandTimeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
            
            if thisCellTypeAllPSTHs is None:
                thisCellTypeAllPSTHs = np.zeros((len(cellsThisType),len(numLas),len(numBands),len(binEdges)-1))
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, binEdges)
            for las in range(len(numLas)):
                trialsThisLaser = trialsEachCond[:,:,las]
                for band in range(len(numBands)):
                    trialsThisBand = trialsThisLaser[:,band]
                    thisBandSpikeCounts = spikeCountMat[trialsThisBand]
                    thisPSTH = np.mean(thisBandSpikeCounts,axis=0)
                    thisCellTypeAllPSTHs[indCell,las,band,:] = thisPSTH

        bandPSTHs.append(thisCellTypeAllPSTHs)
        
elif CASE == 2:
    PSTHs = []
    PSTHs2 = []
    onsetProps = []
    
    for ind, cellsThisType in enumerate(cells):
        thisCellTypeAllPSTHs = None
        thisCellTypeAllPSTHs2 = None
        thisCellTypeOnsetProps = None
        
        for indCell in range(len(cellsThisType)):
            cell = cellsThisType.iloc[indCell]
            cellObj = ephyscore.Cell(cell)
            bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandSession']))
            bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
            bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            
            bandTimeRange = [-0.5, 1.5]
            binsize = 50 #in milliseconds
            
            bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                            bandSpikeTimestamps, 
                                                                                                            bandEventOnsetTimes,
                                                                                                            [bandTimeRange[0]-binsize, bandTimeRange[1]+2*(binsize/1000.0)])
            
            numLas = np.unique(bandBData['laserTrial'])
            trialsEachLas = behavioranalysis.find_trials_each_type(bandBData['laserTrial'],numLas)

            binEdges = np.around(np.arange(bandTimeRange[0]-(binsize/1000.0), bandTimeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
            
            baselineRange = [-0.55, -0.15]
            baselineDuration = baselineRange[1]-baselineRange[0]
            baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                         bandIndexLimitsEachTrial, baselineRange)
            baselineMean = np.mean(baselineSpikeCountMat)/baselineDuration
            
            
            if thisCellTypeAllPSTHs is None:
                thisCellTypeAllPSTHs = np.zeros((len(cellsThisType),len(numLas),len(binEdges)-1))
                thisCellTypeAllPSTHs2 = np.zeros_like(thisCellTypeAllPSTHs)
                thisCellTypeOnsetProps = np.zeros((len(cellsThisType), len(numLas)))
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, binEdges)
            for las in range(len(numLas)):
                trialsThisLaser = trialsEachLas[:,las]
                thisLaserSpikeCounts = spikeCountMat[trialsThisLaser]
                thisPSTH = np.mean(thisLaserSpikeCounts,axis=0)
                thisPSTH1 = thisPSTH/baselineMean #normalise so baseline is 1
                thisPSTH2 = thisPSTH/thisPSTH[np.where(binEdges==0)[0][0]] #normalise so onset is 1
                thisCellTypeAllPSTHs[indCell,las,:] = thisPSTH1
                thisCellTypeAllPSTHs2[indCell,las,:] = thisPSTH2
                
                onsetTimeRange = [0.0,0.05]
                fullTimeRange = [0.0,1.0]
                onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, onsetTimeRange)
                thisLasOnsetCounts = onsetSpikeCountMat[trialsThisLaser]
                fullSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, fullTimeRange)
                thisLasFullCountMat = fullSpikeCountMat[trialsThisLaser]
                propOnset = 1.0*sum(thisLasOnsetCounts)/sum(thisLasFullCountMat)
                thisCellTypeOnsetProps[indCell, las] = propOnset

        PSTHs.append(thisCellTypeAllPSTHs)
        PSTHs2.append(thisCellTypeAllPSTHs2)
        onsetProps.append(thisCellTypeOnsetProps)
        
    #plot all this garbage
    colours = ['k-', 'y-']
    for ind in range(2):
        plt.figure()
        for ind2 in range(PSTHs[ind].shape[1]):
            for ind3 in range(PSTHs[ind].shape[0]):
                plt.plot(binEdges[:-1], PSTHs[ind][ind3,ind2,:], colours[ind2], alpha=0.2)
            
            meanPSTH = np.median(PSTHs[ind][:,ind2,:], axis=0)    
            plt.plot(binEdges[:-1], meanPSTH, colours[ind2], lw=5)

        plt.xlabel('Time from sound onset')
        plt.ylabel('Normalised spike rate')
        if ind==0:
            plt.title('no PV, normal baseline')
        else:
            plt.title('no SOM, normal baseline')
            
        colours = ['k-', 'y-']
        
    for ind in range(2):
        plt.figure()
        for ind2 in range(PSTHs2[ind].shape[1]):
            for ind3 in range(PSTHs2[ind].shape[0]):
                plt.plot(binEdges[:-1], PSTHs2[ind][ind3,ind2,:], colours[ind2], alpha=0.2)
            
            meanPSTH = np.median(PSTHs2[ind][:,ind2,:], axis=0)    
            plt.plot(binEdges[:-1], meanPSTH, colours[ind2], lw=5)

        plt.xlabel('Time from sound onset')
        plt.ylabel('Normalised spike rate')
        if ind==0:
            plt.title('no PV, normal onset')
        else:
            plt.title('no SOM, normal onset')
            
    for ind in range(2):
        plt.figure()
        thisOnsets = onsetProps[ind]
        thisOnsetsNoLaser = thisOnsets[:,0]
        thisOnsetsLaser = thisOnsets[:,1]
        pairOnsets = [thisOnsetsNoLaser, thisOnsetsLaser]
        band_plots.plot_paired_scatter_with_median(pairOnsets, ['no laser', 'laser'])
        plt.ylabel('Proportion of spikes at onset')
        if ind==0:
            plt.title('no PV')
        else:
            plt.title('no SOM')
        print stats.wilcoxon(thisOnsetsNoLaser, thisOnsetsLaser)
        
    
    plt.show()
