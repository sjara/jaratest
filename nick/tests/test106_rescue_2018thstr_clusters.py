import os
import time
import numpy as np
import pandas as pd
from sklearn import neighbors
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
reload(ephyscore)
from jaratest.nick.reports import pinp_report
reload(pinp_report)

'''
This is an attempt to rescue clusters that have too many ISI violations. The idea is to start removing
spikes from the cluster, starting with the ones that have the farthest nearest-neighbor distance in
feature space. We can keep removing spikes until we hit any arbitrary ISI violation threshold, and then
evaluate whether there is anything left over. Truly horrible clusters will hopefully have so few spikes
left over at the end that they will be easy to exclude.

TODO:
* I still need to figure out how to save modified .clu files after we are done with this.
** We should save something like TT1.clu.modified or something, and then anytime we are loading
   clusters we can specify whether we want to load the original clusters or the modified cluster if they exist.
'''

needsCuttingFn = '/home/nick/Desktop/20180329_needsCutting.txt'
outputDir =  '/home/nick/Desktop/20180330_doneCutting_NN'
# outputDir =  '/home/nick/Desktop/20180330_doneCutting_mahalanobis'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
needsCuttingFile = open(needsCuttingFn, 'r')
needsCuttingCells = [line.strip() for line in needsCuttingFile.readlines()]

dbFn = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
db = pd.read_hdf(dbFn, key='dataframe')

for cellName in needsCuttingCells:
    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    index, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
    cell = ephyscore.Cell(dbRow)
    timestamps, samples, recordingNumber = cell.load_all_spikedata()

    isiViolations = spikesorting.calculate_ISI_violations(timestamps)
    print "isi violations: %{}".format(isiViolations*100)
    print "nSpikes: {}".format(len(timestamps))
    featuresMat = spikesorting.calculate_features(samples, ['peakFirstHalf', 'valleyFirstHalf', 'energy'])

    #To sort by nearest-neighbor distance
    print "Calculating NN distance"
    tic = time.time()
    #This will use all the processors
    nbrs = neighbors.NearestNeighbors(n_neighbors=2, algorithm='auto', n_jobs=-1).fit(featuresMat)
    distances, indices = nbrs.kneighbors(featuresMat)
    toc = time.time()
    elapsed = toc-tic
    print "NN done, elapsed time: {}".format(elapsed/60.)
    sortArray = np.argsort(distances[:,1]) #Take second neighbor distance because first is self (0)

    #To sort by mahalanobis distance to the cluster centroid
    # centroid = featuresMat.mean(axis=0)

    spikesToRemove = 0
    thisISIviolation = isiViolations #The isi violations including all the spikes
    jumpBy = int(len(timestamps)*0.01) #Jump by 1% of spikes each time
    while thisISIviolation>0.02:
        spikesToRemove+=jumpBy
        #We start to throw spikes at the end of the sort array away
        includeBool = sortArray < (len(sortArray)-spikesToRemove)
        # timestampsToInclude = sortedTimestamps[:-1*spikesToRemove]
        timestampsToInclude = timestamps[includeBool]
        thisISIviolation = spikesorting.calculate_ISI_violations(np.sort(timestampsToInclude))
        print "Removing {} spikes, ISI violations: {}".format(spikesToRemove, thisISIviolation)
    print "Final included spikes: {} out of {}".format(len(timestampsToInclude), len(timestamps))

    #The inds of all the spikes that get to stay (have to have a low number in sort array)
    #Sort array is in chronological order, so this include bool array is also chronological
    # includeBool = sortArray < (len(sortArray)-spikesToRemove)

    for thisRecordingNum in np.unique(recordingNumber):
        #Which spikes in the total come from this recording
        indsThisRecording = np.flatnonzero(recordingNumber == thisRecordingNum)
        #What are the values in includeBool for those inds?
        includeThisRecording = includeBool[indsThisRecording]

        #load the .clu file
        #Need the recording info
        subject = cell.dbRow['subject']
        date = cell.dbRow['date']
        ephysTimeThisRecording = cell.dbRow['ephysTime'][thisRecordingNum]
        clusterDir = "{}_kk".format("_".join([date, ephysTimeThisRecording]))
        clusterFullPath = os.path.join(settings.EPHYS_PATH, subject, clusterDir)
        clusterFile = os.path.join(clusterFullPath,'Tetrode{}.clu.1'.format(tetrode))

        allClustersThisTetrode = np.fromfile(clusterFile,dtype='int32',sep=' ')[1:]

        nClusters = len(np.unique(allClustersThisTetrode))

        #The inds of the spikes from the cluster we are working on
        indsThisCluster = np.flatnonzero(allClustersThisTetrode == cluster)

        #For each spike from this cluster we have a bool value to include it or not
        assert len(indsThisCluster) == len(includeThisRecording)

        #For every spike in the cluster, we determine whether to keep or remove
        for indIter, indThisSpike in enumerate(indsThisCluster):
            includeThisSpike = includeThisRecording[indIter]
            if includeThisSpike == 0: #If we remove, just set the value in allClustersThisTetrode to 0
                allClustersThisTetrode[indThisSpike] = 0

        #Then just re-save the allClustersThisTetrode as a modified clu file
        modifiedClusterFile = os.path.join(clusterFullPath,'Tetrode{}.clu.modified'.format(tetrode))

        # FIXME: Make sure that adding cluster 0 does not mess up creating databases or
        #        other processes where we need to read the clu file
        fid = open(modifiedClusterFile,'w')
        #We added a new garbage cluster (0)
        fid.write('{0}\n'.format(nClusters+1))
        print "Writing .clu.modified file for session {}".format(ephysTimeThisRecording)
        for cn in allClustersThisTetrode:
            fid.write('{0}\n'.format(cn))
        fid.close()

    print "Plotting report"
    plt.clf()
    cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)
    pinp_report.plot_pinp_report(cell.dbRow, useModifiedClusters=True)
    figsize = (9, 11)
    plt.gcf().set_size_inches(figsize)
    subject = cell.dbRow['subject']
    date = cell.dbRow['date']
    depth = cell.dbRow['depth']
    tetrode = cell.dbRow['tetrode']
    taggedCellCluster = int(cell.dbRow['cluster'])
    fullName = os.path.join(outputDir, cellName)
    plt.savefig(fullName,format='png')


