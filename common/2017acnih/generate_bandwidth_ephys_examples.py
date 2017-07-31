'''
Generate the intermediate ephys and behaviour data to plot rasters
and tuning curves for bandwidth ephys sessions.

Calling this script without parameters will generate data for all
cells in cellParamsList below.

To generate data for only a few cells, you can specify what cells to save:
run generate_bandwidth_ephys_examples 0 2 3
'''

import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from scipy import stats

photoFigName = 'photoidentified_cells_bandwidth_tuning'
SOMFigName = 'SOM_inactivation_bandwidth_tuning'

photoDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', photoFigName)
SOMDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', SOMFigName)


# -- Ephys and behaviour file names for example cells -- #
cellParamsList = [{'animal':'band004',
                   'date': '2016-09-09',
                   'laserEphysSession': '2016-09-09_13-36-54',
                   'bandwidthEphysSession': '2016-09-09_13-40-30',
                   'bandwidthBehavSession':'band004_bandwidth_am_20160909f.h5',
                   'tetrode':6,
                   'cluster':4}, #example PV cell
                  
                  {'animal':'band015',
                   'date': '2016-11-12',
                   'laserEphysSession': '2016-11-12_12-19-00',
                   'bandwidthEphysSession': '2016-11-12_12-23-23',
                   'bandwidthBehavSession':'band015_bandwidth_am_20161112f.h5',
                   'tetrode':8,
                   'cluster':4}, #example SOM cell         
                  
                  {'animal':'band015',
                   'date': '2016-11-12',
                   'laserEphysSession': '2016-11-12_13-53-27',
                   'bandwidthEphysSession': '2016-11-12_13-58-43',
                   'bandwidthBehavSession':'band015_bandwidth_am_20161112l.h5',
                   'tetrode':7,
                   'cluster':4}, #bad example SOM cell (not tuned to center frequency)         
                  
                  {'animal':'band016',
                   'date': '2016-12-11',
                   'laserEphysSession': '2016-12-11_15-02-44',
                   'bandwidthEphysSession': '2016-12-11_15-07-28',
                   'bandwidthBehavSession':'band016_bandwidth_am_20161211f.h5',
                   'tetrode':6,
                   'cluster':6}, #example excitatory cell (non-SOM cell in SOM animal)
                  
                  {'animal':'band002',
                   'date': '2016-08-11',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2016-08-11_10-14-24',
                   'bandwidthBehavSession':'band002_bandwidth_am_20160811d.h5',
                   'tetrode':4,
                   'cluster':5}, #example excitatory cell (from wt animal)
                  
                  {'animal':'band002',
                   'date': '2016-08-12',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2016-08-12_12-27-34',
                   'bandwidthBehavSession':'band002_bandwidth_am_20160812k.h5',
                   'tetrode':6,
                   'cluster':4}, #example excitatory cell (from wt animal)
                  
                  {'animal':'band003',
                   'date': '2016-08-18',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2016-08-18_14-48-21',
                   'bandwidthBehavSession':'band003_bandwidth_am_20160818o.h5',
                   'tetrode':6,
                   'cluster':6},
                  
                  {'animal':'band025',
                   'date': '2017-04-20',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2017-04-20_15-16-29',
                   'bandwidthBehavSession':'band025_bandwidth_am_20170420k.h5',
                   'tetrode':6,
                   'cluster':6}, #example cell showing different contextual modulation with laser on (SOM-Arch)
                  
                  {'animal':'band025',
                   'date': '2017-04-19',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2017-04-19_14-38-17',
                   'bandwidthBehavSession':'band025_bandwidth_am_20170419g.h5',
                   'tetrode':8,
                   'cluster':2}, #example cell showing same context mod, difference in gain with laser on (SOM-Arch) 

                   {'animal':'band025',
                   'date': '2017-04-19',
                   'laserEphysSession': None,
                   'bandwidthEphysSession': '2017-04-19_14-38-17',
                   'bandwidthBehavSession':'band025_bandwidth_am_20170419g.h5',
                   'tetrode':4,
                   'cluster':3}] #example cell suppressed by laser

# -- Define which cells to process --
args = sys.argv[1:]
if len(args):
    cellsToGenerate = [int(x) for x in args]
else:
    cellsToGenerate = range(len(cellParamsList))
print cellsToGenerate


for indCell in cellsToGenerate:
    
    cell = cellParamsList[indCell]
    # --- loads spike and event data for bandwidth ephys sessions ---
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, cell['animal'])
    bandEphysSession = cell['bandwidthEphysSession']
    tetrode=int(cell['tetrode'])
    eventFilename=os.path.join(ephysBaseDir,
                               bandEphysSession,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                bandEphysSession,
                                'Tetrode{}.spikes'.format(tetrode))
    bandEventData=loadopenephys.Events(eventFilename)
    bandSpikeData = loadopenephys.DataSpikes(spikesFilename)
    clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(bandEphysSession))
    clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
    bandSpikeData.set_clusters(clustersFile)
    bandSpikeData.samples=bandSpikeData.samples[bandSpikeData.clusters==cell['cluster']]
    bandSpikeData.timestamps=bandSpikeData.timestamps[bandSpikeData.clusters==cell['cluster']]
    
    # convert to seconds and millivolts
    bandSpikeData.samples = bandSpikeData.samples.astype(float)-2**15
    bandSpikeData.samples = (1000.0/bandSpikeData.gain[0,0]) * bandSpikeData.samples
    bandSpikeData.timestamps = bandSpikeData.timestamps/bandSpikeData.samplingRate
    bandEventData.timestamps = bandEventData.timestamps/bandEventData.samplingRate
    
    # --- get behaviour data associated with bandwidth sessions ---
    behavFile = os.path.join(settings.BEHAVIOR_PATH,cell['animal'],cell['bandwidthBehavSession'])
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')
    
    # --- produce inputs for raster plot ---
    bandEachTrial = bdata['currentBand']
    numBands = np.unique(bandEachTrial)
    firstSortLabels = ['{}'.format(band) for band in np.unique(bandEachTrial)]
    
    # sort by laser trials for SOM-Arch animal, otherwise by amplitude of noise in bandwidth trials
    if cell['animal']=='band025':
        secondSort = bdata['laserTrial']
        numSec = np.unique(secondSort)
        secondSortLabels = ['no laser','laser'] 
    else:
        secondSort = bdata['currentAmp']
        numSec = np.unique(secondSort)
        secondSortLabels = ['{} dB'.format(amp) for amp in np.unique(secondSort)]
        
    bandTimeRange = [-0.2, 1.5]
    bandEventOnsetTimes = bandEventData.get_event_onset_times()
    bandSpikeTimestamps = bandSpikeData.timestamps
    bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           secondSort, 
                                                                           numSec)
    bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        bandTimeRange)
    
    
    
    # --- produce input for bandwidth tuning curve ---
    soundDuration = 1.0
    print('WARNING! The sound duration is HARDCODED.')
    timeRange = [0.0, soundDuration]
    bandSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, timeRange)
    spikeArray = np.zeros((len(numBands), len(numSec))) # Average firing rate
    errorArray = np.zeros_like(spikeArray)
    for thisSecVal in range(len(numSec)):
        trialsThisSecVal = bandTrialsEachCond[:,:,thisSecVal]
        for band in range(len(numBands)):
            trialsThisBand = trialsThisSecVal[:,band]
            if bandSpikeCountMat.shape[0] != len(trialsThisBand):
                bandSpikeCountMat = bandSpikeCountMat[:-1,:]
            thisBandCounts = bandSpikeCountMat[trialsThisBand].flatten()
            spikeArray[band, thisSecVal] = np.mean(thisBandCounts)/soundDuration
            errorArray[band, thisSecVal] = stats.sem(thisBandCounts)/soundDuration # Error is standard error of the mean
    
            
    # --- load spike and event data for laser trials ---
    laserEphysSession = cell['laserEphysSession']
    if laserEphysSession is not None:
        #loads spike and event data for laser sessions
        eventFilename=os.path.join(ephysBaseDir,
                                   laserEphysSession,
                                   'all_channels.events')
        spikesFilename=os.path.join(ephysBaseDir,
                                    laserEphysSession,
                                    'Tetrode{}.spikes'.format(tetrode))
        laserEventData=loadopenephys.Events(eventFilename)
        laserSpikeData = loadopenephys.DataSpikes(spikesFilename)
        clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(laserEphysSession))
        clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
        laserSpikeData.set_clusters(clustersFile)
        laserSpikeData.samples=laserSpikeData.samples[laserSpikeData.clusters==cell['cluster']]
        laserSpikeData.timestamps=laserSpikeData.timestamps[laserSpikeData.clusters==cell['cluster']]
        
        # convert to seconds and millivolts
        laserSpikeData.samples = laserSpikeData.samples.astype(float)-2**15
        laserSpikeData.samples = (1000.0/laserSpikeData.gain[0,0]) * laserSpikeData.samples
        laserSpikeData.timestamps = laserSpikeData.timestamps/laserSpikeData.samplingRate
        laserEventData.timestamps = laserEventData.timestamps/laserEventData.samplingRate
        
        # --- produce input for laser rasters ---
        laserTimeRange = [-0.1, 0.4]
        laserEventOnsetTimes = laserEventData.get_event_onset_times()
        laserSpikeTimestamps = laserSpikeData.timestamps
        laserSpikeTimesFromEventOnset, trialIndexForEachSpike, laserIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        laserSpikeTimestamps, 
                                                                                                        laserEventOnsetTimes,
                                                                                                        laserTimeRange)
    ### Save bandwidth data ###    
    outputFile = 'example_bandwidth_tuning_{}_{}_T{}_c{}.npz'.format(cell['animal'], cell['date'], cell['tetrode'],cell['cluster'])
    if cell['animal']=='band025':
        outputFullPath = os.path.join(SOMDataDir,outputFile)
    else:
        outputFullPath = os.path.join(photoDataDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=bandSpikeTimestamps, eventOnsetTimes=bandEventOnsetTimes,
             spikeCountMat=bandSpikeCountMat, spikeArray=spikeArray, errorArray=errorArray,
             possibleBands=numBands, possibleSecondSort=numSec, firstSortLabels=firstSortLabels,
             secondSortLabels=secondSortLabels, spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
             indexLimitsEachTrial=bandIndexLimitsEachTrial, timeRange=bandTimeRange,trialsEachCond=bandTrialsEachCond, **cell)
    print outputFile + " saved"

    ### Save laser data ###
    if laserEphysSession is not None:
        outputFile = 'example_laser_response_{}_{}_T{}_c{}.npz'.format(cell['animal'], cell['date'], cell['tetrode'],cell['cluster'])
        outputFullPath = os.path.join(photoDataDir,outputFile)
        np.savez(outputFullPath, spikeTimesFromEventOnset=laserSpikeTimesFromEventOnset, indexLimitsEachTrial=laserIndexLimitsEachTrial, timeRange=laserTimeRange, **cell)
        print outputFile + " saved"

    
