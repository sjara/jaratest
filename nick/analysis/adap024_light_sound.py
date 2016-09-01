from jaratest.nick.inforecordings import adap024_inforec as inforec
reload(inforec)
from jaratest.nick.database import dataloader_v2 as dataloader
reload(dataloader)
from jaratest.nick.utils import transferutils as tf
from jaratest.nick.database import dataplotter
reload(dataplotter)
from jaratest.nick.utils import clusterutils
reload(clusterutils)
reload(tf)
from matplotlib import pyplot as plt
import numpy as np
import os

subject=inforec.subject
sessions = inforec.experiments[0].sites[0].session_ephys_dirs()
sessionTypes = inforec.experiments[0].sites[0].session_types()
sessionBehav = inforec.experiments[0].sites[0].session_behav_filenames()

loader = dataloader.DataLoader(subject)

for session in sessions:
    tf.rsync_session_data(subject, session)

for bfile in sessionBehav:
    tf.rsync_behavior(subject, bfile)

for tetrode in range(1, 9):
    # tetrode=1 #This was the best tetrode
    #Cluster the sessions together
    idString = '2016-08-24_light_sound'
    oneTT = clusterutils.cluster_many_sessions(subject, sessions, tetrode, idString,
                                            saveSingleSessionCluFiles=True)

    for cluster in np.unique(oneTT.clusters):
        plt.clf()

        #Tuning session
        tuningIx = sessionTypes.index('tuning')
        tuningPhys = sessions[tuningIx]
        tuningBehav = sessionBehav[tuningIx]

        tuningSpikes = loader.get_session_spikes(tuningPhys, tetrode, cluster=cluster)
        tuningEvents = loader.get_session_events(tuningPhys)
        tuningEventOnsetTimes = loader.get_event_onset_times(tuningEvents)
        tuningBdata = loader.get_session_behavior(tuningBehav)

        currentFreq = tuningBdata['currentFreq']

        #Cell Tuning Plot
        plt.subplot(4, 1, 1)
        dataplotter.plot_raster(tuningSpikes.timestamps, tuningEventOnsetTimes, sortArray=currentFreq)
        plt.title('tuning - T{}c{}'.format(tetrode, cluster))
        plt.ylabel('Frequency (Hz)')

        #First behav session
        b1Ix = sessionTypes.index('behav1')
        b1Phys = sessions[b1Ix]
        b1Behav = sessionBehav[b1Ix]

        b1Spikes = loader.get_session_spikes(b1Phys, tetrode, cluster=cluster)
        b1Events = loader.get_session_events(b1Phys)
        b1EventOnsetTimes = loader.get_event_onset_times(b1Events,eventChannel=0, minEventOnsetDiff=None)
        b1Bdata = loader.get_session_behavior(b1Behav)
        targetFreq = b1Bdata['targetFrequency']
        valid = b1Bdata['valid']
        validFreq = targetFreq[valid==1]
        validEventOnsets = b1EventOnsetTimes[valid==1]

        #Behav Session 1 plot
        plt.subplot(4, 1, 2)
        dataplotter.plot_raster(b1Spikes.timestamps, validEventOnsets, sortArray=validFreq)
        plt.title('behav1')
        plt.ylabel('Frequency (Hz)')

        #Second Behav session
        b2Ix = sessionTypes.index('behav2')
        b2Phys = sessions[b2Ix]
        b2Behav = sessionBehav[b2Ix]

        b2Spikes = loader.get_session_spikes(b2Phys, tetrode, cluster=cluster)
        b2Events = loader.get_session_events(b2Phys)
        b2EventOnsetTimes = loader.get_event_onset_times(b2Events,minEventOnsetDiff=None)
        b2Bdata = loader.get_session_behavior(b2Behav)
        targetFreq = b2Bdata['targetFrequency']
        valid = b2Bdata['valid'][:-1] #One more behav session than ephys events
        validEventOnsets = b2EventOnsetTimes[valid==1]
        validFreq = targetFreq[valid==1]

        #Behav Session 2 plot
        plt.subplot(4, 1, 4)
        dataplotter.plot_raster(b2Spikes.timestamps, validEventOnsets, sortArray=validFreq)
        plt.title('behav2')
        plt.xlabel('Time from stimulus onset (s)')
        plt.ylabel('Frequency (Hz)')

        #Light Discrim Session
        lightIx = sessionTypes.index('light')
        lightPhys = sessions[lightIx]
        lightBehav = sessionBehav[lightIx]

        lightSpikes = loader.get_session_spikes(lightPhys, tetrode, cluster=cluster)
        lightEvents = loader.get_session_events(lightPhys)
        lightEventOnsetTimes = loader.get_event_onset_times(lightEvents, eventChannel=0, minEventOnsetDiff=None)
        lightBdata = loader.get_session_behavior(lightBehav)

        timeTarget = lightBdata['timeTarget']
        tCout = lightBdata['timeCenterOut']
        waitTime = tCout-timeTarget
        eventWaitTime = lightEventOnsetTimes+waitTime

        # Light discrim session plo# t
        plt.subplot(4, 1, 3)
        dataplotter.plot_raster(lightSpikes.timestamps, lightEventOnsetTimes, sortArray=waitTime,
                                fillWidth=0)
        plt.hold(1)
        pRaster = dataplotter.plot_raster(eventWaitTime, lightEventOnsetTimes, sortArray=waitTime,
                                        fillWidth=0)
        plt.setp(pRaster, color='r')
        ax = plt.gca()
        ticks = ax.get_yticklabels()
        newticks = ['' for _ in ticks]
        ax.set_yticklabels(newticks)
        plt.title('light')
        plt.ylabel('Trials sorted by Cout-TimeTarget')

        plt.tight_layout()

        figName = 'light_sound_report_TT{}c{}.png'.format(tetrode, cluster)
        figPath = os.path.join(oneTT.clustersDir, figName)
        plt.savefig(figPath)
