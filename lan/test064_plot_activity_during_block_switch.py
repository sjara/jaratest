'''
Using only good cells, find 30 valid trials before and after block switch in the switching task. Plot activity overtime. 
'''

import sys
import importlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
reload(loader)

numTrialsToPlot = 30
soundTriggerChannel = 0
mouseName = 'test059'
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

'''
cellParams = {'behavSession':'20150624a',
              'tetrode':2,
              'cluster':6}

cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)
thisCell = allcells.cellDB[cellIndex]
'''

currentBehavSession = ''
spikeTimesToPlotThisSession = {'spikeTimes':np.empty(0,dtype='float64'),'cellIndexEachSpike':np.empty(0,dtype='int'),'switchNum':np.empty(0,dtype='int')}

for thisCell in allcells.cellDB:
    quality = thisCell.quality[thisCell.cluster-1]
    if (quality == 1) | (quality == 6):
        
        (eventData, spikeData, bData) = loader.load_remote_2afc_data(thisCell)
        spikeTimestamps = spikeData.spikes.timestamps
        # -- If encounter a new behavSession, find trials where the block switches -- #
        if thisCell.behavSession != currentBehavSession:
            # -- Plot results of last session -- #
            # -- Plot raster and time histogram -- #
            if np.any(spikeTimesToPlotThisSession['spikeTimes']):
                spikeTimesDf = pd.DataFrame(spikeTimesToPlotThisSession)
                spikeTimesDf.groupby(['switchNum']).plot(x='spikeTimes',y='cellIndexEachSpike',kind='scatter')
                plt.show()
                #spikeTimes = spikeTimesToPlotThisSession['spikeTimes']
                #cellIndex = spikeTimesToPlotThisSession['cellIndexEachSpike']
                #trialsEachSwitch = spikeTimesToPlotThisSession['switchNum']
                #extraplots.raster(spikeTimes,cellIndex,timeRange=None,trialsEachCond=trialsEachSwitch,colorEachCond=[b,r,g,k,y,'grey'])
                #plt.vlines(soundOnsetTimes[lastTrialsBeforeSwitch:(lastTrialsAfterSwitch+1)])
                plt.show()
            
            cellIndex = 1   
            currentBehavSession = thisCell.behavSession
            currentBlock = bData['currentBlock']
            blockSwitch = np.r_[0,np.diff(currentBlock)]
            blockSwitchTrialIndex = np.nonzero(blockSwitch)[0]
            #spikeTimesToPlotThisSession = {}
            #cellIndexEachSpike = {}
            spikeTimesToPlotThisSession = {'spikeTimes':np.empty(0,dtype='float64'),'cellIndexEachSpike':np.empty(0,dtype='int'),'switchNum':np.empty(0,dtype='int')}

            #nSwitches = len(blockSwitchTrialIndex)
            #for inds, switch in nSwitches:
            #    spikeTimesToPlotThisSession[inds] = np.empty(0,dtype='float64')
            #    cellIndexEachSpike[inds] = np.empty(0,dtype='int')

            validTrials =  bData['nValid']
            # -- Get all sound onset event times -- #
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            eventOnsetTimes=np.array(eventData.timestamps)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

            # -- Find 30 valid trials before and after the block switch -- #
            timeRangeToPlotThisSession = []
            for trialIndex in blockSwitchTrialIndex:
                lastTrialsBeforeSwitch = np.nonzero(validTrials == (validTrials[trialIndex]-numTrialsToPlot))[0][0]
                lastTrialsAfterSwitch = np.nonzero(validTrials == (validTrials[trialIndex]+numTrialsToPlot))[0][0]

                # -- Find spike time stamps in the specified time range (-30 to +30 valid trials) spanning block switch-- #
                timeRangeToPlotThisSession.append(tuple([soundOnsetTimes[lastTrialsBeforeSwitch],soundOnsetTimes[lastTrialsAfterSwitch]]))


        for indt, timeRange in enumerate(timeRangeToPlotThisSession):
            spikeTimesThisTimeRange = spikeTimestamps[(spikeTimestamps>=timeRange[0])&(spikeTimestamps<=timeRange[1])]
            spikeTimesThisTimeRange -= spikeTimesThisTimeRange[0]
            nSpikes = len(spikeTimesThisTimeRange)
            spikeTimesToPlotThisSession['spikeTimes'] = np.concatenate((spikeTimesToPlotThisSession['spikeTimes'],spikeTimesThisTimeRange))
            spikeTimesToPlotThisSession['cellIndexEachSpike'] = np.concatenate((spikeTimesToPlotThisSession['cellIndexEachSpike'],np.repeat(cellIndex,nSpikes)))
            spikeTimesToPlotThisSession['switchNum'] = np.concatenate((spikeTimesToPlotThisSession['switchNum'],np.repeat(indt+1,nSpikes)))

        cellIndex += 1

    else:
        continue


if np.any(spikeTimesToPlotThisSession['spikeTimes']):
    spikeTimesDf = pd.DataFrame(spikeTimesToPlotThisSession)
    spikeTimesDf.groupby(['switchNum']).plot(x='spikeTimes',y='cellIndexEachSpike',kind='scatter')
    plt.show()
    #spikeTimes = spikeTimesToPlotThisSession['spikeTimes']
    #cellIndex = spikeTimesToPlotThisSession['cellIndexEachSpike']
    #trialsEachSwitch = spikeTimesToPlotThisSession['switchNum']
    #extraplots.raster(spikeTimes,cellIndex,timeRange=None,trialsEachCond=trialsEachSwitch,colorEachCond=[b,r,g,k,y,'grey'])
    #plt.vlines(soundOnsetTimes[lastTrialsBeforeSwitch:(lastTrialsAfterSwitch+1)])
    plt.show()

### Since all the cells don't have the same number of spikes/timestamps, can do a binned count?
    
