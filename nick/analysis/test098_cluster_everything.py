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

sessionInds = range(len(exp.sites[0].sessions))
# sessionList = []

# for ind in sessionInds:
#     session = exp.sites[0].sessions[ind]
#     sessionStr = '{}_{}'.format(session.date, session.timestamp)
#     sessionList.append(sessionStr)

sessionList = exp.sites[0].session_ephys_dirs()
EPHYS_SAMPLING_RATE=30000.0

#Get the start and end times of each session from the cont data
#Cont channel 31 was recorded for each sesssion
contFn = '109_CH31.continuous'
sessionLims=np.empty((len(sessionList), 2))
for indSession, session in enumerate(sessionList):
    contFile = os.path.join(settings.EPHYS_PATH, exp.subject, session, contFn)
    dataCont = loadopenephys.DataCont(contFile)
    dataCont.timestamps=dataCont.timestamps/EPHYS_SAMPLING_RATE
    sessionLims[indSession,0]=dataCont.timestamps[0]
    sessionLims[indSession,1]=dataCont.timestamps[-1]


siteName = '{}_all_sessions_clustered'.format(exp.date)

# figure()
clf()
# for tetrode in [1]:
for tetrode in range(1, 9):
    clf()
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
        normSpikeCount=0
        spikeTimestamps = oneTT.timestamps[oneTT.clusters==cluster]
        chunkStarts = []
        chunkSpikeCounts = []
        for indLims, lims in enumerate(sessionLims):
            #Break the session into 2 min segments and discard the last non-full segment
            splits = arange(lims[0], lims[1], 120)
            chunks = zip(splits, splits[1:])
            for indChunk, chunk in enumerate(chunks):
                spikesThisChunk = spikeTimestamps[((spikeTimestamps > chunk[0]) & (spikeTimestamps<chunk[1]))]
                chunkStarts.append(chunk[0])
                chunkSpikeCounts.append(len(spikesThisChunk))
            if indLims==1:
                normSpikeCount=len(spikesThisChunk)


        subplot2grid((12, 1), (indCluster, 0))
        timebase = array(chunkStarts)/60.0
        timebase = timebase-timebase[0]
        spikeCounts = array(chunkSpikeCounts)/double(normSpikeCount)
        plot(timebase, spikeCounts, 'ko-', lw=2)
        hold(1)
        axvline(x=(sessionLims[1, 1]-sessionLims[0, 0])/60.0, color='r', lw=3)
        axhline(y=1, color='0.5', lw=1)
        ylabel('c{}'.format(cluster))
        ylim([0, 2.5])



    suptitle('TT{} - {} {}'.format(tetrode, exp.subject, exp.date))
    # tight_layout()
    savefig('/home/nick/data/reports/nick/20160805_muscimol_allSessions/TT{}.png'.format(tetrode))
