import os
import sys; sys.path.append('/home/nick/data')
import jaratoolbox; reload(jaratoolbox)
from jaratoolbox import settings; reload(settings)
from inforecordings import test098_inforec as inforec
reload(inforec)
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
import matplotlib.pyplot as plt
print inforec.test098
import pandas as pd
import numpy as np

exp = inforec.test098.experiments[1]

animalName = exp.subject
sessionInds = [1, 5]

sessionList = []

for ind in sessionInds:
    session = exp.sites[0].sessions[ind]
    sessionStr = '{}_{}'.format(session.date, session.timestamp)
    sessionList.append(sessionStr)

siteName = '{}_before_1hr_after'.format(exp.date)

for tetrode in range(1, 9):
    plt.clf()
    oneTT = cms.MultipleSessionsToCluster(animalName, sessionList, tetrode, siteName)
    oneTT.load_all_waveforms()

    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)

    if os.path.isfile(clusterFile):
        oneTT.set_clusters_from_file()
    else:
        oneTT.create_multisession_fet_files()
        oneTT.run_clustering()
        oneTT.set_clusters_from_file()
        # oneTT.save_single_session_clu_files() #Don't do this yet because it will overwrite
        plt.clf()
        oneTT.save_multisession_report()

    for indCluster, cluster in enumerate(np.unique(oneTT.clusters)):
        clusterTimesBefore = oneTT.timestamps[((oneTT.clusters==cluster) & (oneTT.recordingNumber==0))]
        clusterTimesAfter = oneTT.timestamps[((oneTT.clusters==cluster) & (oneTT.recordingNumber==1))]

        ## The before session
        subplot2grid((12, 2), (indCluster, 0))

        eventFn = os.path.join(settings.EPHYS_PATH, animalName, sessionList[0], 'all_channels.events')


        print eventFn
        dataEvents = loadopenephys.Events(eventFn)
        dataEvents.timestamps = dataEvents.timestamps/SAMPLING_RATE

        #Limit the events to ID 1 and Channel 0
        dataEvents.timestamps = dataEvents.timestamps[((dataEvents.eventID==1) & (dataEvents.eventChannel==0))]

        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(clusterTimesBefore,dataEvents.timestamps,timeRange)

        plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
        xlim([-0.5, 1])
        ylim([0, 55])
        ylabel('c{}'.format(cluster))
        if indCluster==0:
            plt.title(sessionList[0])

        #The after session
        subplot2grid((12, 2), (indCluster, 1))

        eventFn = os.path.join(settings.EPHYS_PATH, animalName, sessionList[1], 'all_channels.events')
        print eventFn
        dataEvents = loadopenephys.Events(eventFn)
        dataEvents.timestamps = dataEvents.timestamps/SAMPLING_RATE

        #Limit the events to ID 1 and Channel 0
        dataEvents.timestamps = dataEvents.timestamps[((dataEvents.eventID==1) & (dataEvents.eventChannel==0))]

        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(clusterTimesAfter,dataEvents.timestamps,timeRange)

        plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
        xlim([-0.5, 1])
        ylim([0, 55])

        if indCluster==0:
            title(sessionList[1])

    pltFn = os.path.join(oneTT.clustersDir, 'TT{}_before-after.png'.format(tetrode))
    plt.savefig(pltFn)
