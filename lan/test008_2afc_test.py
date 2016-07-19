from jaratoolbox.test.nick.database import cellDB
reload(cellDB)
from jaratoolbox.test.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)
from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}
 
exp0914 = cellDB.Experiment(animalName='d1pi004', date ='2015-09-14', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp0914.add_site(depth = 3040, tetrodes = range(1,9)) #all TTs laser-responsive, TT7 clearly sound-responsive
site1.add_session('10-41-47', None, sessionTypes['lp']) #1mW,10ms
site1.add_session('10-44-04', None, sessionTypes['nb']) #amp=0.1
site1.add_session('10-48-08', None, sessionTypes['lt'])
site1.add_session('10-51-08', 'a', sessionTypes['tc']) 
site1.add_session('11-24-34', 'a', sessionTypes['2afc'], paradigm='2afc')

site=site1
main2afcind=4

oneTT = cluster_site(site1, 'site1', tetrode=7)
possibleClusters=np.unique(oneTT.clusters)


#Iterate through the clusters, making a new figure for each cluster.

main2afcsession = site.get_mouse_relative_ephys_filenames()[main2afcind]
main2afcbehavFilename = site.get_mouse_relative_behav_filenames()[main2afcind]
#mainTCtype = site.get_session_types()[main2afcind]

bdata = loader.get_session_behavior(main2afcbehavFilename)
#plotTitle = loader.get_session_filename(main2afcsession)
eventData = loader.get_session_events(main2afcsession)
spikeData = loader.get_session_spikes(main2afcsession, tetrode)
for indClust, cluster in enumerate(possibleClusters):
    spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

    eventOnsetTimes=np.array(eventData.timestamps)/SAMPLING_RATE
    #eventOnsetTimes = loader.get_event_onset_times(eventData) #These are already only the sound onset events
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

    freqEachTrial = bdata['targetFrequency']
    possibleFreq = np.unique(freqEachTrial)

    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    # Set this to 1 to plot only correct trials
    if 1:
        rightward &= correct
        leftward &= correct

    trialsEachCond = np.c_[invalid,leftward,rightward] 
    colorEachCond = ['0.75','g','r']

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                                                                             spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

    plt.clf()

    ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,
               colorEachCond=colorEachCond,fillWidth=None,labels=None)
    plt.ylabel('Trials')

    #dataplotter.two_axis_sorted_raster(spikeTimestamps, soundOnsetTimes, secondSortArray=trialsEachCond, secondSortLabels=['invalid', 'leftward', 'rightward'], timeRange=timeRange) #this doesn't work because trialsEachCond is a boolean array of shape [nTrials,nConditions]


    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    smoothWinSize = 3
    ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
             colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate (spk/sec)')

    plt.show()
