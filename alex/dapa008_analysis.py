import os, sys
import pdb
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
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


subject = 'dapa008'
dbpath = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
db = pd.read_hdf(dbpath, key='database')

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')

#Plot raster for noise bursts
def noise_raster(ephysData, gs):
    plt.subplot(gs[0, 0])

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.3, 0.6]

    trialsEachCond = []

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond)

    xlabel = 'time (s)'
    ylabel = 'Trial'

    plt.title('Noise Bursts')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    '''
    print("Saving Noise Bursts for Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    '''


#Plot raster for normal tuning curves
def tuning_raster(bdata, ephysdata, gs):
    plt.subplot(gs[0, 1])

    freqEachTrial = bdata['currentFreq']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.3, 0.6]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    #print len(freqEachTrial), len(eventOnsetTimes)



    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=freqLabels)


    xlabel = 'time (s)'
    ylabel = 'Frequency (kHz)'

    plt.title('Tuning Curve')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    '''
    print("Saving Tuning Curve for Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    '''

#Plot tuning curve
def tuning_curve(bdata, ephysData, gs):
    plt.subplot(gs[3, 0])

    freqEachTrial = bdata['currentFreq']
    intEachTrial = bdata['currentIntensity']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [0.0, 0.1]

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

        try:
            freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)
        except:
            behavIndexLimitsEachTrial = indexLimitsEachTrial[0:2,:-1]
            freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavIndexLimitsEachTrial)
        
        xpoints = [x for x in range(0, len(possiblefreqs))]
        #plt.semilogx(possiblefreqs, freq_avgs, linestyle = line, color = 'black', label = curveName)
        #plt.plot(log(possiblefreqs), freq_avgs, linestyle = line, color = 'black', label = curveName, xlabels = possiblefreqs)
        plt.plot(xpoints, freq_avgs, linestyle = line, color = 'black', marker = 'o', label = curveName)
        plt.xticks(xpoints, freqLabels)
        plt.hold(True)
    plt.title('Frequency Tuning Curve')
    plt.legend(fontsize = 'x-small')
    plt.hold(False)


#Plot raster for laser tuning curves
def laser_tuning_raster(bdata, ephysData, gs):
    freqEachTrial = bdata['currentFreq']
    laserEachTrial = bdata['laserOn']
    intEachTrial = bdata['currentIntensity']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [-0.3, 0.6]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]
    possiblelaser = np.unique(laserEachTrial)
    possibleInts = np.unique(intEachTrial)

    #trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    laserTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, laserEachTrial, possiblelaser)
    intTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, intEachTrial, possibleInts)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)

    #plt.figure()

    for intInd, inten in enumerate(possibleInts):
        for indLaser in possiblelaser:
            #plt.subplot(2, 1, indLaser)
            plt.subplot(gs[intInd+1, indLaser])
            if indLaser == 0:
                title = "No Laser " + str(inten) + " dB"
            else:
                title = "Laser " + str(inten) + " dB"
            trialsEachCond = laserTrialsEachCond[:,:,indLaser] & intTrialsEachCond[:,:,intInd]

            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                       trialsEachCond=trialsEachCond, labels=freqLabels)


            xlabel = 'time (s)'
            ylabel = 'Frequency (kHz)'

            plt.title(title)
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

#Plot laser tuning curve
def laser_tuning_curve(bdata, ephysData, gs):
    plt.subplot(gs[3, 1])

    freqEachTrial = bdata['currentFreq']
    laserEachTrial = bdata['laserOn']
    intEachTrial = bdata['currentIntensity']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']

    timeRange = [0.0, 0.1]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]
    possiblelaser = np.unique(laserEachTrial)
    possibleInts = np.unique(intEachTrial)

    laserTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, laserEachTrial, possiblelaser)
    intTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, intEachTrial, possibleInts)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)
   

    for intInd, inten in enumerate(possibleInts):
        line = '-'
        if intInd == 0:
            line = '--'
        for indLaser in possiblelaser:
            color = 'black'
            if indLaser == 1:
                color = 'blue'

            laser = 'No Laser - '
            if indLaser == 1:
                laser = 'Laser - '
            curveName = laser + str(inten) + ' dB'

            trialsEachCond = laserTrialsEachCond[:,:,indLaser] & intTrialsEachCond[:,:,intInd]

            try:
                freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)
            except:
                behavIndexLimitsEachTrial = indexLimitsEachTrial[0:2,:-1]
                freq_avgs = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, behavIndexLimitsEachTrial)
            
            xpoints = [x for x in range(0, len(possiblefreqs))]
            #plt.semilogx(possiblefreqs, freq_avgs, linestyle = line, color = color, label = curveName)
            #plt.plot(xvalues, freq_avgs, linestyle = line, color = 'black', label = curveName, xlabels = possiblefreqs)
            plt.plot(xpoints, freq_avgs, linestyle = line, color = color, marker = 'o', label = curveName)
            plt.xticks(xpoints, freqLabels)
            plt.hold(True)
    plt.title('Frequency Tuning Curve - Laser Session')
    plt.legend(fontsize = 'x-small')
    plt.hold(False)


for indRow, dbRow in goodCells.iterrows():
    #Create a cell object using the database row
    print(indRow)
    cell = ephyscore.Cell(dbRow)
    #Find the inds for the noiseburst sessions
    noiseSessionInds = cell.get_session_inds('noisebursts')

    plt.figure(figsize = (12, 16))

    gs = gridspec.GridSpec(4, 2)
    gs.update(hspace=0.3)

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


    #Find the inds for the laser tuning curve sessions
    laserTuningSessionInds = cell.get_session_inds('laserTuningCurve')

    #Go through the tuning curve sessions and plot the rasters
    if len(laserTuningSessionInds) != 0:
        for sessionInd in laserTuningSessionInds:
            try:
                bdata = cell.load_behavior_by_index(sessionInd)
                ephysData = cell.load_ephys_by_index(sessionInd)
                laser_tuning_raster(bdata, ephysData, gs)
                laser_tuning_curve(bdata, ephysData, gs)
            except:
                print("no laser tuning curve")
        

    print("Saving Cell " + str(indRow))
    #figname = '/home/jarauser/data/reports_alex/dapa010/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    figname = '/home/jarauser/data/reports_alex/{}/test/{}_depth{}_T{}_C{}.png'.format(subject, dbRow['date'], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.close()


sys.exit()

'''
subject = 'dapa008'
dbpath = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
db = pd.read_hdf(dbpath, key='database')

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')

for indRow, dbRow in goodCells.iterrows():
    #Create a cell object using the database row
    cell = ephyscore.Cell(dbRow)
    #Find the inds for a specific sessiontype that was recorded several times
    try:
        sessionInds = cell.get_session_inds('tuningCurve')
        print(sessionInds)
    except:
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

    #Plot report with the data
    freqEachTrial = bdata['currentFreq']
    
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.1, 1.0]

    possiblefreqs = np.unique(freqEachTrial)

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    #print len(freqEachTrial), len(eventOnsetTimes)



    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=possiblefreqs)


    xlabel = 'time (s)'
    ylabel = 'Trial'

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    #plt.setp(pRaster, ms=ms)
    print("Saving Cell " + str(indRow))
    figname = '/home/jarauser/data/reports_alex/dapa008/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    plt.savefig(figname)
    
    plt.clf()
    #plt.show()
'''


'''
subject = 'dapa008'
filename = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
db = pd.read_hdf(filename, key='database')

for ind in db.index:
    thisCell = db.loc[ind]
    tetrode = int(thisCell['tetrode'])
    cluster = int(thisCell['cluster'])
    depth = int(thisCell['depth'])
    if len(thisCell['behavior'])<2:
      continue
    behavFileName = thisCell['behavior'][1]
    session = thisCell['ephys'][1]

    ###############CURRENT POSITION - NEED CELL TO ANALYZE#################

    #Load ephys data
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, subject)
    eventFilename=os.path.join(ephysBaseDir,
                               session,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                session,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(session))
    clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
    spikeData.set_clusters(clustersFile)
    if cluster is not None:
        spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]

    # convert to seconds and millivolts
    spikeData.samples = spikeData.samples.astype(float)-2**15
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
    eventData.timestamps = eventData.timestamps/eventData.samplingRate

    if behavFileName == None:
        continue
    behavFile = os.path.join(settings.BEHAVIOR_PATH,subject,behavFileName)
    try:
        bdata = loadbehavior.BehaviorData(behavFile,readmode='full')
    except:
        continue

    # LOAD YOUR SHIT
    #eventData, spikeData = load_ephys_data(subject, session, tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    #tuningBData = bdata   


    freqEachTrial = bdata['currentFreq']
    laserEachTrial = bdata['laserOn']
    
    timeRange = [-0.1, 1.0]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]
    possiblelaser = np.unique(laserEachTrial)

    #trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    laserTrialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possiblefreqs, laserEachTrial, possiblelaser)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)

    plt.figure()

    for indLaser in possiblelaser:
        plt.subplot(2, 1, indLaser)
        if indLaser == 0:
            laser = "No Laser"
        else:
            laser = "Laser"
        trialsEachCond = laserTrialsEachCond[:,:,indLaser]

        pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=freqLabels)


        xlabel = 'time (s)'
        ylabel = 'Trial'

        plt.title(laser)
        if indLaser == 0:
            plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        

        #plt.setp(pRaster, ms=ms)
    
    
    print("Saving Cell " + str(ind))
    figname = '/home/jarauser/data/reports_alex/dapa008/' + str(session) + '_depth' + str(depth) + '_T' + str(tetrode) + '_C' + str(cluster)+ '.png'
    plt.savefig(figname)
    
    plt.clf()
    #plt.show()
'''
