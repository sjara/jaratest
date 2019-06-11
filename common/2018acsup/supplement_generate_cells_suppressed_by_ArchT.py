'''This is to plot sound responses of cells to 0.25 bandwidth sounds with and without laser.'''

import os
import numpy as np
from scipy import stats

from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import settings

import studyparams
import figparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'inactivation_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_cells_inactivated_by_archt'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

BAND_USED = 1 #look at responses for 0.25 octaves

# responses of example cells
cellList = [{'subject' : 'band062',
            'date' : '2018-05-25',
            'depth' : 1450,
            'tetrode' : 5,
            'cluster' : 5}, #suppressed cell in PV-ArchT mouse
            
            {'subject' : 'band073',
            'date' : '2018-09-14',
            'depth' : 1300,
            'tetrode' : 4,
            'cluster' : 4} #suppressed cell in SOM-ArchT mouse
            ]

cellTypes = ['PV', 'SOM']

for indCell, oneCell in enumerate(cellList):
    # -- find the cell we want based on dictionary --
    cellInd, dbRow = celldatabase.find_cell(db, **oneCell)
    cell = ephyscore.Cell(dbRow)
    
    bandEphysData, bandBData = cell.load_by_index(int(dbRow['bestBandSession']))
    bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
    bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    bandEachTrial = bandBData['currentBand']
    numBands = np.unique(bandEachTrial)
    LaserEachTrial = bandBData['laserTrial']
    numLaser = np.unique(LaserEachTrial)
        
    bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                               numBands, 
                                                                               LaserEachTrial, 
                                                                               numLaser)
    
    bandTimeRange = [-0.5, 1.5]
    binsize = 50 #in milliseconds
    
    bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                    bandSpikeTimestamps, 
                                                                                                    bandEventOnsetTimes,
                                                                                                    [bandTimeRange[0]-binsize, bandTimeRange[1]])
    
    binEdges = np.around(np.arange(bandTimeRange[0]-(binsize/1000.0), bandTimeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, binEdges)
    
    # find trials of bandwidth we want
    trialsThisBand = bandTrialsEachCond[:,BAND_USED,:]
    
    controlSpikeCounts = spikeCountMat[trialsThisBand[:,0]]
    laserSpikeCounts = spikeCountMat[trialsThisBand[:,1]]
    
    controlPSTH = np.mean(controlSpikeCounts,axis=0)/(binsize/1000.0)
    laserPSTH = np.mean(laserSpikeCounts, axis=0)/(binsize/1000.0)
    
    ### Save bandwidth data ###    
    outputFile = 'example_{}_inactivated_sound_response_{}_{}_{}um_T{}_c{}.npz'.format(cellTypes[indCell],dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])

    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath,
             bandwidth=BAND_USED,
             possibleLasers=numLaser,
             spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
             indexLimitsEachTrial=bandIndexLimitsEachTrial,
             trialsEachCond=trialsThisBand,
             rasterTimeRange=bandTimeRange,
             PSTHbins = binEdges[1:-2], controlPSTH = controlPSTH[1:-1], laserPSTH = laserPSTH[1:-1])
    print outputFile + " saved"


# responses for all sound responsive cells

singleUnits = db.query(studyparams.SINGLE_UNITS_INACTIVATION)
goodCells = singleUnits.query('spikeShapeQuality>{} and controlSession==0'.format(studyparams.SPIKE_QUALITY_THRESHOLD))
bestCells = goodCells.query('onsetSoundResponsePVal<{} or sustainedSoundResponsePVal<{} or soundResponsePVal<{}'.format(studyparams.SOUND_RESPONSE_PVAL))
bestCells = bestCells.query('bestBandSession>0')

noPVCells = bestCells.loc[bestCells['subject'].isin(studyparams.PV_ARCHT_MICE)]
noSOMCells = bestCells.loc[bestCells['subject'].isin(studyparams.SOM_ARCHT_MICE)]

cellTypes = [noPVCells, noSOMCells]

soundResponses = [[np.zeros(len(noPVCells)), np.zeros(len(noPVCells))], [np.zeros(len(noSOMCells)), np.zeros(len(noSOMCells))]]
laserOnsetResponses = [[np.zeros(len(noPVCells)), np.zeros(len(noPVCells))], [np.zeros(len(noSOMCells)), np.zeros(len(noSOMCells))]]

soundpVals = [np.zeros(len(noPVCells)), np.zeros(len(noSOMCells))]
laserOnsetpVals = [np.zeros(len(noPVCells)), np.zeros(len(noSOMCells))]

for indType, cells in enumerate(cellTypes):
    for indCell, (dbIndex, dbRow) in enumerate(cells.iterrows()):
    
        cell = ephyscore.Cell(dbRow)
        
        # --- loads spike and event data for bandwidth ephys sessions ---
        bandEphysData, bandBData = cell.load_by_index(int(dbRow['bestBandSession'])) #make them ints in the first place
        bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
        bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        # -- Define sorting parameters for behaviour --
        bandEachTrial = bandBData['currentBand']
        numBands = np.unique(bandEachTrial)
        
        LaserEachTrial = bandBData['laserTrial']
        numLaser = np.unique(LaserEachTrial)
            
        bandTimeRange = [-0.5, 1.5]
        bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                               numBands, 
                                                                               LaserEachTrial, 
                                                                               numLaser)
        bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                            bandSpikeTimestamps, 
                                                                                                            bandEventOnsetTimes,
                                                                                                            bandTimeRange)
        
        sustainedTimeRange = [0.2, 1.0]
        sustainedDuration = sustainedTimeRange[1]-sustainedTimeRange[0]
        
        sustainedSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, sustainedTimeRange)
        
        laserOnsetTimeRange = [-0.1,-0.05]
        laserOnsetDuration = laserOnsetTimeRange[1]-laserOnsetTimeRange[0]
        
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, laserOnsetTimeRange)
        
        trialsThisBand = bandTrialsEachCond[:,BAND_USED,:] #looking at 0.25 octave trials
        # Average firing rate for laser and non-laser trials and SEMev
        
        soundCounts = []
        laserCounts = []
        
        for laser in range(len(numLaser)):
            trialsThisLaser = trialsThisBand[:,laser]
            if sustainedSpikeCountMat.shape[0] != len(trialsThisLaser): #if number of events greater than behaviour trials because last trial didn't get saved
                sustainedSpikeCountMat = sustainedSpikeCountMat[:-1,:]
                laserSpikeCountMat = laserSpikeCountMat[:-1,:]
            if any(trialsThisLaser):
                thisLaserSustainedCounts = sustainedSpikeCountMat[trialsThisLaser].flatten()
                soundCounts.append(thisLaserSustainedCounts)
                
                thisLaserLaserCounts = laserSpikeCountMat[trialsThisLaser].flatten()
                laserCounts.append(thisLaserLaserCounts)
                
                soundResponses[indType][laser][indCell] = np.mean(thisLaserSustainedCounts)/sustainedDuration
                laserOnsetResponses[indType][laser][indCell] = np.mean(thisLaserLaserCounts)/laserOnsetDuration
                
        soundpVal = stats.ranksums(soundCounts[0], soundCounts[1])[1]
        soundpVals[indType][indCell] = soundpVal
        
        laserpVal = stats.ranksums(laserCounts[0], laserCounts[1])[1]
        laserOnsetpVals[indType][indCell] = laserpVal
                
# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'low_bandwidth_responses_during_inactivation.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVcontrolResponses = soundResponses[0][0], PVlaserResponses = soundResponses[0][1],
         SOMcontrolResponses = soundResponses[1][0], SOMlaserResponses = soundResponses[1][1],
         PVpVals = soundpVals[0], SOMpVals = soundpVals[1],
         PVcontrolLaserOnset = laserOnsetResponses[0][0], PVlaserOnset = laserOnsetResponses[0][1],
         SOMcontrolLaserOnset = laserOnsetResponses[1][0], SOMlaserOnset = laserOnsetResponses[1][1],
         PVlaserOnsetpVals = laserOnsetpVals[0], SOMlaserOnsetpVals = laserOnsetpVals[1],)
print outputFile + " saved"