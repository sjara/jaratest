#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Objects and methods for keeping information about isolated cells'''
#Modification: added clusterQuality in EphysSessionInfo, CellInfo, and CellDatabase to store quality score for each cluster. Added laserSession in EphysSessionInfo, CellInfo, and CellDatabase for use in PINP experiments.

import numpy as np
import os
from jaratoolbox import settings

class EphysSessionInfo(object):
     def __init__(self, animalName, ephysSession, behavSession, laserSession,
                  clustersEachTetrode={}, clusterQuality={}, soundResponse={}, trialsToExclude=[]):
         '''
         animalName [string] 'test000'
         ephysSession [string] '2014-06-25_18-33-30'
         behavSession [string] '20111209a'
         clustersEachTetrode [dict] {2:[2,5,6], 6:[3,8,10]}  {tetrodeInd:[cluster1,cluster2], ...}
         trialsToExclude [list of lists] [(2,5,range(100:200)), (6,10,range(600,650))]
            [(tetrodeInd,clusterInd,trialrange), ...]
         '''
         self.animalName = animalName
         self.ephysSession = ephysSession
         self.behavSession = behavSession
         self.clustersEachTetrode = clustersEachTetrode
         self.clusterQuality = clusterQuality
         #self.soundResponse = soundResponse
         self.trialsToExclude = trialsToExclude

class CellInfo(object):
    '''
    Container of information for one cell. 
    '''
    def __init__(self, animalName, ephysSession, behavSession, laserSession, tetrode, cluster, quality,
                 trialsToExclude=[]):
        # -- Basic info --
        self.animalName = animalName
        self.ephysSession = ephysSession
        self.behavSession = behavSession
        self.laserSession = laserSession
        self.tetrode = tetrode
        self.cluster = cluster
        self.quality = quality
        #self.response = response
        # -- Trial selection --
        self.trialsToExclude = np.array(trialsToExclude,dtype=int)
        # -- Response properties --
        #self.soundResponsive = None
    def get_filename(self):
        ephysDir = settings.EPHYS_PATH
        filenameOnly = 'Tetrode{0}.spikes'.format(self.tetrode)
        fullPath = os.path.join(ephysDir,self.animalName,self.ephysSession,filenameOnly)
        return fullPath
    def __repr__(self):
        objStrings = []
        for key,value in sorted(vars(self).iteritems()):
            objStrings.append('%s: %s\n'%(key,str(value)))
        return ''.join(objStrings)
    def __str__(self):
        objStr = '%s %s T%dc%d'%(self.animalName,self.ephysSession,
                                 self.tetrode,self.cluster)
        return objStr

class MultiUnitInfo(object):
    '''
    Container of information for a multiunit site
    '''
    def __init__(self, animalName, ephysSession,behavSession, laserSession, tetrode, clusters=[]):
        '''Parameter 'clusters' can be empty (all spikes will be included)'''
        # -- Basic info --
        self.animalName = animalName
        self.ephysSession = ephysSession
        self.behavSession = behavSession
        self.laserSession = laserSession
        self.tetrode = tetrode
        self.clusters = clusters
        # -- Response properties --
        #self.soundResponsive = None
    def __repr__(self):
        objStrings = []
        for key,value in sorted(vars(self).iteritems()):
            objStrings.append('%s: %s\n'%(key,str(value)))
        return ''.join(objStrings)
    def __str__(self):
        objStr = '%s %s T%d'%(self.animalName,self.ephysSession,
                              self.tetrode)
        return objStr


class CellDatabase(list):
    '''
    Container of set of cells.
    '''
    def __init__(self):
        super(CellDatabase, self).__init__()
    def append_session(self,sessionInfo):
        '''
        sessionInfo [of type EphysSessionInfo]
        '''
        for tetrode in sorted(sessionInfo.clustersEachTetrode.keys()):
            for cluster in sessionInfo.clustersEachTetrode[tetrode]:
                oneCell = CellInfo(animalName = sessionInfo.animalName,
                                   ephysSession = sessionInfo.ephysSession,
                                   behavSession = sessionInfo.behavSession,
                                   laserSession = sessionInfo.laserSession,
                                   tetrode = tetrode,
                                   cluster = cluster,
                                   quality = sessionInfo.clusterQuality[tetrode][cluster-1],
                                   #response = sessionInfo.soundResponse[tetrode],
                                   trialsToExclude = [])
                for trialset in sessionInfo.trialsToExclude:
                    if trialset[0]==tetrode and trialset[1]==cluster:
                        oneCell.trialsToExclude = trialset[2]
                    else:
                        print "Format of 'trialsToExclude' is not correct ({0})".format(oneCell)
                self.append(oneCell)

        
    def findcell(self,firstParam,behavSession='',tetrode=-1,cluster=-1):
        '''
        Find index of cell. It can be used in two ways:
        >> cellDB.findcell('test000','20001201a',1,11)
        >> cellDB.findcell(onecell)
        '''
        if isinstance(firstParam,str):
            onecell = CellInfo(firstParam,'',behavSession,tetrode,cluster)
        else:
            onecell = firstParam
        cellIndex = None
        for ind,cell in enumerate(self):
            if onecell.animalName==cell.animalName:
                if onecell.behavSession==cell.behavSession:
                    if onecell.tetrode==cell.tetrode:
                        if onecell.cluster==cell.cluster:
                            cellIndex = ind
        return cellIndex
    def set_soundResponsive(self,zScores,threshold=3):
        '''
        Set soundResponsive flag for each cell, given zScores
        zScores: numpy array (nTimeBins,nConditions,nCells)
        threshold: above this or below negative this it is considered responsive
        '''
        for indcell,onecell in enumerate(self):
            onecell.soundResponsive = np.any(abs(zScores[:,:,indcell])>threshold)
    def get_vector(self,varname):
        '''
        EXAMPLE: cellDB.get_vector('tetrode')
        '''
        return np.array([getattr(onecell, varname) for onecell in self])
    def subset(self,indexes):
        subsetDB = CellDatabase()
        if isinstance(indexes,np.ndarray) and indexes.dtype==bool:
            indexes = np.flatnonzero(indexes)
        for ind in indexes:
            subsetDB.append(self[ind])
        return subsetDB
    def __str__(self):
        objStrings = []
        for ind,c in enumerate(self):
            objStrings.append('[%d] %s\n'%(ind,c))
        return ''.join(objStrings)
    def save_locked_spikes(self,outputDir,timeRange=np.array([-0.3,0.9]),lockTo=1):
        sessionanalysis.save_data_each_cell(self,outputDir,timeRange=timeRange,lockTo=lockTo)
    def evaluate_response(self):
        # NOTE IMPLEMENTED
        pass


class MultiUnitDatabase(list):
    '''Container of set of multiunit sites.
    '''
    def __init__(self):
        super(MultiUnitDatabase, self).__init__()
    def __str__(self):
        objStrings = []
        for ind,c in enumerate(self):
            objStrings.append('[%d] %s\n'%(ind,c))
        return ''.join(objStrings)
    def save_locked_spikes(self,outputDir,timeRange=np.array([-0.3,0.9]),lockTo=1):
        sessionanalysis.save_data_each_mu(self,outputDir,timeRange=timeRange,lockTo=1)



