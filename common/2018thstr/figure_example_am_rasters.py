import pandas as pd
import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
from matplotlib import gridspec
import sys
import subprocess

STUDY_NAME = '2018thstr'

def spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, freqEachTrial):
    '''
    Generator func to return the spiketimes/trial indices for trials of each frequency
    '''
    possibleFreq = np.unique(freqEachTrial)
    for freq in possibleFreq:
        trialsThisFreq = np.flatnonzero(freqEachTrial==freq)
        spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        trialIndicesThisFreq = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        yield (freq, spikeTimesThisFreq, trialIndicesThisFreq)

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors

def find_cell(dataframe, subject, date, depth, tetrode, cluster):
    cell = dataframe.query("subject==@subject and date==@date and depth==@depth and tetrode==@tetrode and cluster==@cluster")
    return cell

def am_example(cell, timeRange=[-0.2, 0.7]):

    #Plot histograms of spikes relative to stimulus period?
    plotCycleHists = False

    spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times(eventID=1, eventChannel=0)
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)
    bdata = celldatabase.get_session_bdata(cell, 'am')
    colors = get_colors(len(np.unique(bdata['currentFreq'])))
    #Raster
    plt.clf()
    if plotCycleHists:
        plt.subplot2grid((11, 3), (0, 0), rowspan=11, colspan=2)
    else:
        plt.subplot(111)
    ms=2
    sortArray = bdata['currentFreq']
    trialsEachCond = behavioranalysis.find_trials_each_type(
        sortArray, np.unique(sortArray))
    labels = ['%.1f' % f for f in np.unique(sortArray)]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeData.timestamps, eventOnsetTimes, timeRange)
    pRaster, hcond, zline = extraplots.raster_plot(
        spikeTimesFromEventOnset,
        indexLimitsEachTrial,
        timeRange,
        trialsEachCond=trialsEachCond,
        labels=labels,
        colorEachCond=colors)
    plt.setp(pRaster, ms=ms)
    plt.ylabel('Highest AM sync rate')
    plt.xlabel('Time from stimulus onset (s)')

    if plotCycleHists:
        #Want to plot a hist of spike times from 0 to 2pi
        # ax3 = plt.subplot(313)
        plt.hold(True)
        for indFreq, (freq, spikeTimesThisFreq, trialIndicesThisFreq) in enumerate(spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, sortArray)):
            radsPerSec=freq*2*np.pi
            spikeRads = (spikeTimesThisFreq*radsPerSec)%(2*np.pi)
            ax = plt.subplot2grid((11, 3), (10-indFreq, 2))
            ax.hist(spikeRads, bins=50, color=colors[indFreq], histtype='step')

def rsync_session_data(subject,
                       session,
                       server = 'jarauser@jarastore',
                       serverEphysPath = '/data/ephys',
                       skipIfExists=False):
    '''
    #DONE: server user and server name as one string
    #TODO: server ephys path and user in settings file
    Rsync just the sessions you need from jarahub
    '''
    fullRemotePath = os.path.join(serverEphysPath, subject, session)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = os.path.join(settings.EPHYS_PATH, subject) + os.sep
    fullLocalPath = os.path.join(localDataPath, session)
    transferCommand = ['rsync', '-av', '--exclude=*.continuous', serverDataPath, localDataPath]
    if skipIfExists:
        if not os.path.exists(fullLocalPath):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)

def rsync_behavior(subject,
                   behavFile,
                   server = 'jarauser@jarahub',
                   serverBehavPath = '/data/behavior',
                   skipIfExists=False):
    fullRemotePath = os.path.join(serverBehavPath, subject, behavFile)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = os.path.join(settings.BEHAVIOR_PATH, subject) + os.sep
    fullLocalPath = os.path.join(localDataPath, behavFile)
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    if skipIfExists:
        if not os.path.exists(fullLocalPath):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)

if __name__=='__main__':
    dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
    db = pd.read_hdf(dbPath, key='dataframe')

    CASE=0

    if CASE==0:

        exampleCells = []

        #Thalamus, non-identified, very synchronized
        cell = {'subject':'pinp015',
                'date':'2017-02-15',
                'depth':3110,
                'tetrode':7,
                'cluster':3}
        exampleCells.append(cell)

        #Cortex, non-identified, Rate coding (higher rates)
        cell = {'subject':'pinp015',
                'date':'2017-02-02',
                'depth':975,
                'tetrode':2,
                'cluster':6}
        exampleCells.append(cell)

        #Cortex, non-identified, Rate coding (medium rates)
        cell = {'subject':'pinp018',
                'date':'2017-04-11',
                'depth':905,
                'tetrode':6,
                'cluster':5}
        exampleCells.append(cell)

        #Cortex, non-identified, Rate coding (higher rates), one of the best examples
        cell = {'subject':'pinp017',
                'date':'2017-03-23',
                'depth':1281,
                'tetrode':7,
                'cluster':2}
        exampleCells.append(cell)

        #Thalamus, Identified
        ## Synchronized to 16Hz
        cell = {'subject':'pinp016',
                'date':'2017-03-14',
                'depth':3703,
                'tetrode':2,
                'cluster':2}
        exampleCells.append(cell)

        ## Synchronized to 128Hz
        cell = {'subject':'pinp015',
                'date':'2017-02-15',
                'depth':3110,
                'tetrode':7,
                'cluster':6}
        exampleCells.append(cell)

        #Cortex, Identified
        ## Synchronized to 8Hz
        cell = {'subject':'pinp018',
                'date':'2017-04-11',
                'depth':1016,
                'tetrode':4,
                'cluster':5}
        exampleCells.append(cell)

        ## Synchronized to 32Hz
        cell = {'subject':'pinp017',
                'date':'2017-03-23',
                'depth':1281,
                'tetrode':7,
                'cluster':2}
        exampleCells.append(cell)

        #Striatum
        ## Sync'd to 4Hz max
        cell = {'subject':'pinp020',
                'date':'2017-05-10',
                'depth':2580,
                'tetrode':7,
                'cluster':3}
        exampleCells.append(cell)

        ## Sync'd to 11Hz max
        cell = {'subject':'pinp025',
                'date':'2017-09-01',
                'depth':2111,
                'tetrode':4,
                'cluster':3}
        exampleCells.append(cell)

        if len(sys.argv)>1:
            cellInd = int(sys.argv[1])
        else:
            print "Use sys.argv to select a cell. Defaulting to cell 0"
            cellInd = 0

        cellDict = exampleCells[cellInd]
        cell = find_cell(db, cellDict['subject'], cellDict['date'], cellDict['depth'], cellDict['tetrode'], cellDict['cluster']).iloc[0]
        am_example(cell)
        plt.show()

    if CASE==1:
        #Rsync all the example data
        for cellDict in exampleCells:
            cell = find_cell(db, cellDict['subject'], cellDict['date'], cellDict['depth'], cellDict['tetrode'], cellDict['cluster']).iloc[0]
            amInd = celldatabase.get_session_inds(cell, 'am')[0]
            amSession = cell['ephys'][amInd]
            rsync_session_data(cell['subject'], amSession)
            rsync_session_data(cell['subject'], '{}_kk'.format(amSession))
            amBehav = cell['behavior'][amInd]
            rsync_behavior(cell['subject'], amBehav)

    if CASE==2:
        ### THIS IS FOR PLOTTING ALL CELLS BY THEIR MAX SYNC FREQ
        def mkdir(directory):
            if not os.path.exists(directory):
                os.makedirs(directory)

        soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
        # thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
        # thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
        # thal = pd.concat([thal1, thal2])
        # ac = soundResponsive.groupby('brainarea').get_group('rightAC')
        plotOnlyIdentified = False

        if plotOnlyIdentified:
            baseDir = '/home/nick/data/reports/nick/2018thstr_am_sync_onlyID/'
            soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')
            thal1 = soundLaserResponsive.groupby('brainarea').get_group('rightThal')
            thal2 = soundLaserResponsive.groupby('brainarea').get_group('rightThalamus')
            thal = pd.concat([thal1, thal2])
            ac = soundLaserResponsive.groupby('brainarea').get_group('rightAC')
        else:
            baseDir = '/home/nick/data/reports/nick/2018thstr_am_sync/'
            thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
            thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
            thal = pd.concat([thal1, thal2])
            ac = soundResponsive.groupby('brainarea').get_group('rightAC')

        astrR = soundResponsive.groupby('brainarea').get_group('rightAstr')
        astrL = soundResponsive.groupby('brainarea').get_group('rightAstr')
        astr = pd.concat([astrR, astrL])

        thalDir = os.path.join(baseDir, 'thalamus')
        acDir = os.path.join(baseDir, 'ac')
        astrDir = os.path.join(baseDir, 'astr')
        mkdir(baseDir)

        #Thalamus
        mkdir(thalDir)
        # for indCell, cell in thal.iterrows():
        for rate in np.unique(thal['highestSync']):
            thisRateDir = os.path.join(thalDir, '{}'.format(np.round(rate, 0)))
            mkdir(thisRateDir)
            cellsThisRate = thal[thal['highestSync']==rate]
            for indCell, cell in cellsThisRate.iterrows():
                savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
                # am_example(cell, timeRange=[0.1, 0.5])
                am_example(cell)
                plt.savefig(savePath)

        #AC
        mkdir(acDir)
        # for indCell, cell in thal.iterrows():
        for rate in np.unique(ac['highestSync']):
            thisRateDir = os.path.join(acDir, '{}'.format(np.round(rate, 0)))
            mkdir(thisRateDir)
            cellsThisRate = ac[ac['highestSync']==rate]
            for indCell, cell in cellsThisRate.iterrows():
                savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
                # am_example(cell, timeRange=[0.1, 0.5])
                am_example(cell)
                plt.savefig(savePath)

        #AStr
        mkdir(astrDir)
        for rate in np.unique(astr['highestSync']):
            thisRateDir = os.path.join(astrDir, '{}'.format(np.round(rate, 0)))
            mkdir(thisRateDir)
            cellsThisRate = astr[astr['highestSync']==rate]
            for indCell, cell in cellsThisRate.iterrows():
                savePath = os.path.join(thisRateDir, 'cell{}.png'.format(indCell))
                # am_example(cell, timeRange=[0.1, 0.5])
                am_example(cell)
                plt.savefig(savePath)
