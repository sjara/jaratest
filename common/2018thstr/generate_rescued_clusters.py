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
import figparams
reload(spikesorting)
reload(ephyscore)

SAVE=True

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
db = pd.read_hdf(dbPath, key='dataframe')
cellsToRescue = db.query('autoTagged==1 and isiViolations>0.02 and isiViolations<0.04')

for indRow, dbRow in cellsToRescue.iterrows():
    cell = ephyscore.Cell(dbRow, useModifiedClusters=False)
    timestamps, samples, recordingNumber = cell.load_all_spikedata()

    isiViolations = spikesorting.calculate_ISI_violations(timestamps)
    print "isi violations: %{}".format(isiViolations*100)
    print "nSpikes: {}".format(len(timestamps))
    featuresMat = spikesorting.calculate_features(samples, ['peakFirstHalf', 'valleyFirstHalf', 'energy'])

    #Sort by mahalanobis distance to the cluster centroid
    try:
        dM = spikesorting.distance_to_centroid(featuresMat)
    # except LinAlgError, errMsg: #Singular matrix error
    except: #FIXME: LinAlgError not defined??
        continue
    sortArray = np.argsort(dM)

    spikesToRemove = 0
    thisISIviolation = isiViolations #The isi violations including all the spikes
    jumpBy = int(len(timestamps)*0.01) #Jump by 1% of spikes each time
    if jumpBy==0:
        jumpBy = 1 #Jump by at least 1 spike FIXME: This is probably a terrible cluster if this happens
    while thisISIviolation>0.02:
        spikesToRemove+=jumpBy
        #We start to throw spikes at the end of the sort array away
        includeBool = sortArray < (len(sortArray)-spikesToRemove)
        # timestampsToInclude = sortedTimestamps[:-1*spikesToRemove]
        timestampsToInclude = timestamps[includeBool]
        thisISIviolation = spikesorting.calculate_ISI_violations(np.sort(timestampsToInclude))
        print "Removing {} spikes, ISI violations: {}".format(spikesToRemove, thisISIviolation)
    print "Final included spikes: {} out of {}".format(len(timestampsToInclude), len(timestamps))

    #FIXME: I don't really know what these comments are saying
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
        tetrode = int(cell.dbRow['tetrode'])
        cluster = int(cell.dbRow['cluster'])
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

    #Save the new ISI violation
    db.loc[indRow, 'modifiedISI'] = thisISIviolation

if SAVE:
    # savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
    db.to_hdf(dbPath, 'dataframe')
    print "SAVED DATAFRAME to {}".format(dbPath)
