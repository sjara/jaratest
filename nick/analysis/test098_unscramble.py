#We need to unscramble the spike data from the recording on 2016-07-28
#

import numpy as np
from jaratest.nick.probes import probelayout as newlayout
from jaratest.nick.probes import oldmapping_INCORRECT as oldlayout
reload(newlayout)
reload(oldlayout)

newmapping = newlayout.channelMap
oldmapping = oldlayout.OLDMAPPING + 1 #new layout was increased by 1 to match openephys GUI


#oldmapping
# array([[31, 28, 21, 22],
#        [27, 23, 26, 18],
#        [24, 17, 19, 25],
#        [29, 32, 30, 20],
#        [ 3,  9,  8,  1],
#        [14, 15,  7, 16],
#        [ 5, 12, 11,  2],
#        [ 6, 13,  4, 10]])

#newmapping
# array([[18, 21, 28, 27],
#        [22, 26, 23, 31],
#        [25, 32, 30, 24],
#        [20, 17, 19, 29],
#        [14,  8,  9, 16],
#        [ 3,  2, 10,  1],
#        [12,  5,  6, 15],
#        [11,  4, 13,  7]])


for indTet, tetrode in enumerate(oldmapping):
    print 'Tetrode {}'.format(indTet+1)
    for indChan, channel in enumerate(tetrode):
        whereLoc = np.argwhere(newmapping==channel)
        print '{} - {}'.format(channel, whereLoc+1)

'''
output:

Tetrode 1
31 - [[2 4]]
28 - [[1 3]]
21 - [[1 2]]
22 - [[2 1]]

Tetrode 2
27 - [[1 4]]
23 - [[2 3]]
26 - [[2 2]]
18 - [[1 1]]

Tetrode 3
24 - [[3 4]]
17 - [[4 2]]
19 - [[4 3]]
25 - [[3 1]]

Tetrode 4
29 - [[4 4]]
32 - [[3 2]]
30 - [[3 3]]
20 - [[4 1]]

Tetrode 5
3 - [[6 1]]
9 - [[5 3]]
8 - [[5 2]]
1 - [[6 4]]

Tetrode 6
14 - [[5 1]]
15 - [[7 4]]
7 - [[8 4]]
16 - [[5 4]]

Tetrode 7
5 - [[7 2]]
12 - [[7 1]]
11 - [[8 1]]
2 - [[6 2]]

Tetrode 8
6 - [[7 3]]
13 - [[8 3]]
4 - [[8 2]]
10 - [[6 3]]

'''

#Newclusters has a list for each tetrode with (tetrode, cluster) pairs
newclusters = {
    'T1': [(1, 4), (1, 12)],
    'T2': [(2, 6), (2, 7), (2, 10)],
    'T3': [(3, 5)],
    'T5': [(5, 8), (5, 9), (5, 12)],
    'T6': [(7, 4), (7, 6)]
}

#Analysis with these tetrode/cluster pairs

from jaratest.nick.inforecordings import test098_inforec as inforec
reload(inforec)
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
import numpy as np
import matplotlib.pyplot as plt
import os
from jaratoolbox import settings
from jaratoolbox import loadopenephys

sessionList = inforec.experiments[1].sites[0].session_ephys_dirs()
date = '2016-07-28'
siteName = '{}_all_sessions_clustered'.format(date)
animalName = 'test098'

def plot_time_report(clusterlist, animalName, sessionList, siteName):
    '''
    clusterlist in format [(tetrode, cluster), (tetrode, cluster), etc.]
    #NOTE: I am here
    '''

    for indPair, (tetrode, cluster) in enumerate(clusterlist):

        oneTT = cms.MultipleSessionsToCluster(animalName, sessionList, tetrode, siteName)
        oneTT.load_all_waveforms()

        clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)

        oneTT.set_clusters_from_file()

        normSpikeCount=0
        spikeTimestamps = oneTT.timestamps[oneTT.clusters==cluster]
        chunkStarts = []
        chunkSpikeCounts = []
        EPHYS_SAMPLING_RATE=30000.0

        #Get the start and end times of each session from the cont data
        #Cont channel 31 was recorded for each sesssion
        contFn = '109_CH31.continuous'
        sessionLims=np.empty((len(sessionList), 2))
        for indSession, session in enumerate(sessionList):
            contFile = os.path.join(settings.EPHYS_PATH, animalName, session, contFn)
            dataCont = loadopenephys.DataCont(contFile)
            dataCont.timestamps=dataCont.timestamps/EPHYS_SAMPLING_RATE
            sessionLims[indSession,0]=dataCont.timestamps[0]
            sessionLims[indSession,1]=dataCont.timestamps[-1]

        for indLims, lims in enumerate(sessionLims):
            #Break the session into 2 min segments and discard the last non-full segment
            splits = np.arange(lims[0], lims[1], 120)
            chunks = zip(splits, splits[1:])
            for indChunk, chunk in enumerate(chunks):
                spikesThisChunk = spikeTimestamps[((spikeTimestamps > chunk[0]) & (spikeTimestamps<chunk[1]))]
                chunkStarts.append(chunk[0])
                chunkSpikeCounts.append(len(spikesThisChunk))
            if indLims==1:
                normSpikeCount=len(spikesThisChunk)


        plt.subplot2grid((3, 1), (indPair, 0))
        timebase = np.array(chunkStarts)/60.0
        timebase = timebase-timebase[0]
        spikeCounts = np.array(chunkSpikeCounts)/np.double(normSpikeCount)
        plt.plot(timebase, spikeCounts, 'ko-', lw=2)
        plt.hold(1)
        plt.axvline(x=(sessionLims[1, 1]-sessionLims[0, 0])/60.0, color='r', lw=3)
        plt.axhline(y=1, color='0.5', lw=1)
        plt.ylabel('tt{}c{}'.format(tetrode, cluster))
        plt.ylim([0, 2.5])

    # tight_layout()

# plt.figure()
for key, val in newclusters.iteritems():
    plt.clf()
    plot_time_report(val, animalName, sessionList, siteName)
    plt.suptitle('{} - {} {} unscramble'.format(key, animalName, date))
    # plt.show()
    plt.savefig('/home/nick/data/reports/nick/20160902_test098_unscramble/{}.png'.format(key))
