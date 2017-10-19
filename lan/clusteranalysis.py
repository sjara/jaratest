'''
Analyze the quality of clusters produced by spike-sorting
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting
# from jaratoolbox import celldatabase
from jaratoolbox import loadopenephys
from jaratoolbox import settings

import itertools #For making string combinations of all comparisons
import pickle #For saving the waveform objects

#For importing cellDB files
import sys
import importlib

#For calling rsync to get just the data we need
import subprocess

import pandas as pd

#from jaratoolbox import ephyscore


STUDY_NAME = '2016astr'


def find_ephys_sessions(cellDB):
    return list(np.unique(cellDB.get_vector('ephysSession')))

def waveforms_many_sessions(subject, ephysSessions, tetrode, clustersPerTetrode=12, wavesize=160):
    '''
    Create a list of arrays containing waveforms for each session for one tetrode.
    '''
    waveformsOneTetrode = []
    for oneSession in ephysSessions:
        waves = calculate_avg_waveforms(subject, oneSession, tetrode,
                                clustersPerTetrode=clustersPerTetrode, wavesize=wavesize)
        waveformsOneTetrode.append(waves)
    return waveformsOneTetrode

def calculate_avg_waveforms(subject, ephysSession, tetrode, clustersPerTetrode=12, wavesize=160):
    '''
    NOTE: This methods should look through sessions, not clusters.
          The idea is to compare clusters within a tetrode, and then across sessions
          but still within a tetrode.
    NOTE: This method is inefficient because it load the spikes file for each cluster.
    '''

    # DONE: Load data for one tetrodes and calculate average for each cluster.
    #ephysFilename = ???
    ephysDir = os.path.join(settings.EPHYS_PATH_REMOTE, subject, ephysSession)
    ephysFilename = os.path.join(ephysDir, 'Tetrode{}.spikes'.format(tetrode))
    spikes = loadopenephys.DataSpikes(ephysFilename)

    # DONE: Load cluster file
    #kkDataDir = os.path.dirname(self.filename)+'_kk'
    #fullPath = os.path.join(kkDataDir,clusterFilename)
    clustersDir = '{}_kk'.format(ephysDir)
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]

    # DONE: loop through clusters
    allWaveforms = np.empty((clustersPerTetrode,wavesize))
    for indc in range(clustersPerTetrode):
        print 'Estimating average waveform for {0} T{1}c{2}'.format(ephysSession,tetrode,indc+1)

        # DONE: get waveforms for one cluster
        #Add 1 to the cluster index because clusters start from 1
        waveforms = spikes.samples[clusters==indc+1, :, :]

        alignedWaveforms = spikesorting.align_waveforms(waveforms)
        meanWaveforms = np.mean(alignedWaveforms,axis=0)
        allWaveforms[indc,:] = meanWaveforms.flatten()
    return allWaveforms


###waveforms = ephysData.spikes.samples.astype(float)-2**15 #This is specific to open Ephys
###waveforms = (1000.0/ephysData.spikes.gain[0,0]) * waveforms

def row_corrcoeff(A,B):
    '''
    Row-wise correlation coefficient between two 2-D arrays.
    Note that np.corrcoeff() is not a valid replacement for this method.

    http://stackoverflow.com/questions/30143417/computing-the-correlation-coefficient-between-two-multi-dimensional-arrays
    '''
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:,None]
    B_mB = B - B.mean(1)[:,None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA,B_mB.T)/np.sqrt(np.dot(ssA[:,None],ssB[None]))


def spikeshape_correlation(waveforms):
    '''
    Find the correlation between spikes shapes for a session and across sessions.
    Args:
        waveforms (list): each item should be an np.array containing waveforms
                   for all clusters in one session with size [nClusters,nSamples]
    Returns:
        ccSelf (list): each item is an np.array containing the correlation coefficient
                   matrix across clusters for each session.
        ccAcross (list): each item is an np.array containing the corr coeff matrix
                   between clusters from one session and the next.
    '''
    ccSelf = []
    ccAccross = []
    inds=-1 # Needed in case only one waveform
    for inds in range(len(waveforms)-1):
        ccSelf.append(row_corrcoeff(waveforms[inds],waveforms[inds]))
        ccAccross.append(row_corrcoeff(waveforms[inds],waveforms[inds+1]))
    ccSelf.append(row_corrcoeff(waveforms[inds+1],waveforms[inds+1]))
    return (ccSelf,ccAccross)


def plot_correlation(ccSelf,ccAccross,cmap='hot'):
    nSessions = len(ccSelf)
    plt.clf()
    for inds in range(nSessions):
        plt.subplot2grid((2,nSessions),(0,inds))
        plt.imshow(ccSelf[inds],clim=[0,1], cmap=cmap,interpolation='nearest')
        plt.axis('image')
        #title('')
    for inds in range(nSessions-1):
        plt.subplot2grid((2,nSessions-1),(1,inds))
        plt.imshow(ccAccross[inds],clim=[0,1], cmap=cmap,interpolation='nearest')
        plt.axis('image')
    plt.colorbar()
    plt.draw()

def rsync_session_data(subject,
                       session,
                       serverUser = 'jarauser',
                       serverName = 'jarastore',
                       serverEphysPath = '/data2016/ephys',
                       skipIfExists=False):
    '''
    #NOTE: Deprecated now, use jaratest.nick.utils.transferutils module for these rsync funcs
    #TODO: server user and server name as one string
    #TODO: server ephys path and user in settings file
    Rsync just the sessions you need from jarahub
    '''
    fullRemotePath = os.path.join(serverEphysPath, subject, session)
    serverDataPath = '{}@{}:{}'.format(serverUser, serverName, fullRemotePath)
    localDataPath = os.path.join(settings.EPHYS_PATH, subject) + os.sep
    fullLocalPath = os.path.join(localDataPath, session)
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    if skipIfExists:
        if not os.path.exists(fullLocalPath):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)

def rsync_ISI_file(subject,
                   serverUser = 'jarauser',
                   serverName = 'jarastore',
                   serverEphysPath = '/data2016/ephys',
                   skipIfExists=False):

    isiFn = 'ISI_Violations.txt'
    fullRemotePath = os.path.join(serverEphysPath, '{}_processed'.format(subject), isiFn)
    serverDataPath = '{}@{}:{}'.format(serverUser, serverName, fullRemotePath)
    localDataPath = os.path.join(settings.EPHYS_PATH, subject) + os.sep
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    fullLocalFilename = os.path.join(localDataPath, isiFn)
    if skipIfExists:
        if not os.path.isfile(fullLocalFilename):
            subprocess.call(transferCommand)
    else:
        subprocess.call(transferCommand)



def comparison_label_array(session1, session2, tetrode):
    '''
    Returns an array of strings that describe the comparisons made between two sessions
    '''
    clabs1 = ['{}_T{}c{}'.format(session1, tetrode, cnum) for cnum in range(1, 13)]
    clabs2 = ['{}_T{}c{}'.format(session2, tetrode, cnum) for cnum in range(1, 13)]
    labs = ['{} x {}'.format(cl1, cl2) for cl1, cl2 in itertools.product(clabs1, clabs2)]
    larray = np.array(labs, dtype=str).reshape((12, 12))
    return larray


def read_ISI_dict(fileName):
    '''
    This is how Billy and Lan read the ISI files
    '''
    ISIFile = open(fileName, 'r')
    ISIDict = {}
    behavName = ''
    for line in ISIFile:
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1] #Drop the suffix, just keep the date
        else:
            ISIDict[behavName] = [float(x) for x in line.split(',')[0:-1]] #There is an extra comma at the end of the line, so take to  -1
    return ISIDict

'''
def session_good_clusters(cellDB, session, tetrode, isiThresh=None, isiDict=None):
    
    #DEPRECATED Return a 12-item vector, containing 1 if the cluster was good quality and zero otherwise
    
    allcellsTetrode = cellDB.get_vector('tetrode')
    allcellsSession = cellDB.get_vector('ephysSession')
    allcellsQuality = cellDB.get_vector('quality')
    #The cells to use come from this session, this tetrode
    cellsThisSession = allcellsSession==session
    cellsThisTetrode = allcellsTetrode==tetrode
    cellsToUse = (cellsThisSession & cellsThisTetrode)
    #Whether each cell in the db is good
    allcellsGoodQuality = ((allcellsQuality==1) | (allcellsQuality==6))
    #Whether the cells that we want to use are good
    goodQualityToUse = allcellsGoodQuality[cellsToUse]
    #The cluster number for each cluster (in case not full 12, or does not start at 1)
    allcellsClusterNumber = cellDB.get_vector('cluster')
    clusterNumsToUse = allcellsClusterNumber[cellsToUse]
    #Initialize to zero
    passingClusters = np.zeros(12, dtype='bool')
    # Set the good quality clusters to 1
    for indClust, clusterNum in np.ndenumerate(clusterNumsToUse):
        passingClusters[clusterNum-1]=goodQualityToUse[indClust]

    if isiThresh:
        allcellsBehavSessions = cellDB.get_vector('behavSession')
        behavSessionsThisSession = allcellsBehavSessions[cellsThisSession]
        behavSession = np.unique(behavSessionsThisSession)
        assert len(behavSession)==1, 'More than 1 behavior session for this ephys session'

        #These are already limited by session
        #DONE: Limit to cells this tetrode
        isiThisSession = np.array(isiDict[behavSession[0]])

        tetrodesThisSession = allcellsTetrode[cellsThisSession]
        cellsThisTetrode = tetrodesThisSession==tetrode
        isiThisTetrode = isiThisSession[cellsThisTetrode]

        assert len(isiThisTetrode)==len(passingClusters), "isiThisTetrode not correct length"

        isiPass = isiThisTetrode < isiThresh
        passingClusters = passingClusters & isiPass

    return passingClusters
'''

def session_good_clusters(animal, session, tetrode, isiThresh, goodQualityList):
    '''
    OVERWRITE this function using database look up. Return a 12-item bool vector, containing True if the cluster was good quality and False otherwise
    '''
    from jaratoolbox import settings
    import pandas as pd
    import numpy as np
    switchingFilePath = os.path.join(settings.FIGURESDATA,STUDY_NAME)
    switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
    switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
    allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

    psychometricFilePath = os.path.join(settings.FIGURESDATA, STUDY_NAME)
    psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
    psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
    allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')
    
    # The 'session' passed is the ephys session, need to convert it to the behav session on the same day
    behavSession = session.split('_')[0].replace('-','')
    behavSession = behavSession + 'a'

    passingClusters = np.array(np.repeat(0,12), dtype=bool) #default to all false
    for allcells in [allcells_switching, allcells_psychometric]:
        cells = allcells.loc[(allcells.animalName==animal) & (allcells.behavSession==behavSession) & (allcells.tetrode==tetrode)]
        print cells.shape
        if np.any(cells):
            goodQualityCells = cells.cellQuality.isin(goodQualityList)
            lowISICells = (cells.ISI<=isiThresh)
            passingClusters = (goodQualityCells & lowISICells).values
    return passingClusters


def locate_cell_in_celldb(celldb, animal, behavSession, tetrode, cluster):
    '''
    Given a cell's parameters and a celldb(pandas DataFrame), locate the cell. Returns either an empty dataframe or a dataframe(subset of original) containing this cell.
    '''
    cell = allce.loc[(celldb.animalName==animal) & (celldb.behavSession==behavSession) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)]
    return cell


def comparison_quality_filter(animal, session1, session2, tetrode, isiThresh=0.02, goodQualityList=[1,6]):  
    '''
    OVERWRITE this function, now using database look up. 
    Returns a matrix where pair comparisons between good cells are 1 and 0 otherwise.
    '''
    session1good = session_good_clusters(animal, session1, tetrode, isiThresh, goodQualityList).astype(int)
    print session1good
    session2good = session_good_clusters(animal, session2, tetrode, isiThresh, goodQualityList).astype(int)
    print session2good
    #Make a boolean matrix from the two quality vectors, with 1 only if both are 1
    #DONE: Which should come first for the across session comparisons?
    #session 1 becomes the rows, which is the same as the corr function
    qualityMat = np.outer(session1good.astype(int), session2good.astype(int)).astype(bool)

    return qualityMat
  
'''
def comparison_quality_filter(cellDB, session1, session2, tetrode, isiThresh=None, isiDict=None):
    #DEPRECATED
    #DONE: FINISH THIS FUNCTION

    session1good = session_good_clusters(cellDB, session1, tetrode, isiThresh, isiDict).astype(int)
    session2good = session_good_clusters(cellDB, session2, tetrode, isiThresh, isiDict).astype(int)

    #Make a boolean matrix from the two quality vectors, with 1 only if both are 1
    #DONE: Which should come first for the across session comparisons?
    #session 1 becomes the rows, which is the same as the corr function
    qualityMat = np.outer(session1good.astype(int), session2good.astype(int)).astype(bool)

    return qualityMat
'''

def triangle_filter(qualityMat):

    #For the self analysis, we want to exclude the diagonal and the top half of the
    #triangle
    #We use the -1th diagonal so that the self comparisons are filtered out
    qualityMat = np.tril(qualityMat, k=-1)
    return qualityMat

def print_reports_clusters(subject, sessions, tetrode, printer):
    '''
    Automatically print (on paper, with a printer) the cluster reports for some sessions
    use lpstat -p to find printers
    use lpadmin -p printername to add a printer as the default
    '''

    reportsDir = os.path.join(settings.EPHYS_PATH, subject, 'reports_clusters')
    for session in sessions:
        reportFilename = '{}_{}_T{}.png'.format(subject, session, tetrode)
        fullReportPath = os.path.join(reportsDir, reportFilename)
        printcommand = ['lpr', '-P {}'.format(printer), fullReportPath]
        print ' '.join(printcommand)
        # subprocess.call(printcommand)


if __name__=='__main__':
    ### Useful trick:   np.set_printoptions(linewidth=160)
    CASE = 8
    ANIMALS = ['adap017','adap013']

    if CASE==0:
        nSamples = 4*40
        nClusters = 12
        basewave = np.sin(2*np.pi*np.linspace(0,2,nSamples))
        waveforms1 = basewave + 0.5*np.random.randn(nClusters,nSamples)
        waveforms2 = basewave + 0.5*np.random.randn(nClusters,nSamples)
        waveforms3 = basewave + 0.5*np.random.randn(nClusters,nSamples)

        listwaveforms = [waveforms1,waveforms2,waveforms3]
        #listwaveforms = [waveforms1,waveforms1,waveforms1]

        #cc = np.corrcoef(waveforms1,waveforms2)
        #cc = row_corrcoeff(waveforms1,waveforms2)
        (ccSelf,ccAccross) = spikeshape_correlation(listwaveforms)

        #print ccSelf
        #print ccAccross

        plot_correlation(ccSelf,ccAccross)
    
    elif CASE==1:
        from jaratoolbox import celldatabase
        eSession = celldatabase.EphysSessionInfo
        cellDB = celldatabase.CellDatabase()
        oneES = eSession(animalName='test089',
                         ephysSession = '2015-07-31_14-40-40',
                         clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),
                                                5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                         behavSession = '20150731a')
        cellDB.append_session(oneES)
        oneES = eSession(animalName='test089',
                         ephysSession = '2015-08-21_16-16-16',
                         clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),
                                                5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                         behavSession = '20150821a')
        cellDB.append_session(oneES)

        # -- Get list of sessions --
        sessionsList = np.unique(cellDB.get_vector('ephysSession'))

        #awave = calculate_avg_waveforms(cellDB)

        #(ccSelf,ccAccross) = spikeshape_correlation([awave])
        #plot_correlation(ccSelf,ccAccross)

    elif CASE==2:

        #Load the waveforms for all the sessions and save them
        subject = 'test098'
        sessions = ['2016-07-26_12-18-39','2016-07-26_12-30-36']
        tetrode=1
        sessionWaves = waveforms_many_sessions(subject, sessions, tetrode)

        #Save the list of waveform arrays as compressed binary file
        waveFile = '/tmp/{}waves.npz'.format(subject)
        np.savez_compressed(waveFile, **dict(zip(sessions, sessionWaves)))

        #Read the saved waveforms back in as a list
        #TODO: This returns a dict, which may not be sorted
        arrFile = np.load(waveFile)
        loadWaves = [arr for name, arr in arrFile.items()]
        loadSessions = [name for name, arr in arrFile.items()]

        ccSelf, ccAcross = spikeshape_correlation(loadWaves)

        corrFile = '/tmp/{}corr.npz'.format(subject)
        np.savez_compressed(corrFile, ccSelf=ccSelf, ccAcross=ccAcross)

        loadCorr = np.load(corrFile)
        plot_correlation(loadCorr['ccSelf'], loadCorr['ccAcross'],'viridis')

    elif CASE==3:

        from jaratest.billy.scripts import celldatabase_quality_tuning as cellDB

        ##
        for animal in ANIMALS:
            subject = animal
            tetrodes = range(1, 9)
            #corrThresh = 0.7 #The lower limit for the correlation value 
            isiThresh = 0.02 #The upper threshold for ISI violations
            goodQualityList = [1,6] #Qaulity score for good cells
            ##

            ### -- DO THIS PER ANIMAL -- ###
            #Get the allcells file
            allcellsFilename = 'allcells_{}_quality'.format(subject)
            sys.path.append(settings.ALLCELLS_PATH)

            allcells = importlib.import_module(allcellsFilename)

            #Get the isi information for each cell in the allcells file
            #rsync_ISI_file(subject, skipIfExists=True)
            #isiFn = os.path.join(settings.EPHYS_PATH_REMOTE, subject+'_processed', 'ISI_Violations.txt') #TODO: this is wet
            #isiDict = read_ISI_dict(isiFn)

            #Find all the sessions for this allcells file
            sessions = find_ephys_sessions(allcells.cellDB)
            clusterDirs = ['{}_kk'.format(session) for session in sessions]

            '''
            #Rsync the data from jarastore for these sessions if needed
            for session in sessions:
                rsync_session_data(subject, session, skipIfExists=True)
            for clusterDir in clusterDirs:
                rsync_session_data(subject, clusterDir, skipIfExists=True)
            '''
            ### -- DO THIS PER TETRODE -- ###
            waveDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/wavefiles') 
            corrDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/corrfiles')
            resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')
            for tetrode in tetrodes:
                #If the waves exist, load them. If not, get them
                waveFile = os.path.join(waveDesFolder, '{}_TT{}waves.p'.format(subject, tetrode))

                # #DONE: stop calculating waves every time
                if os.path.isfile(waveFile):
                    #Load the waves
                    #NOTE: I first used np.savez, but it saved a dict and did not preserve the order of the sessions. Pickle saves the actual object.
                    #TODO: Use np.savez with the data object to save as the list of arrays
                    #TODO: Also see if we should use savez_compressed
                    print "Loading average waves for {} tetrode {}".format(subject, tetrode)
                    sessionWaves = pickle.load(open(waveFile, 'rb'))
                else:
                    print "Calculating average waves for Subject {} tetrode {}".format(subject, tetrode)
                    sessionWaves = waveforms_many_sessions(subject, sessions, tetrode)
                    pickle.dump(sessionWaves, open(waveFile, 'wb'))

                #TODO: if the correlations exist we don't need to load the waves
                corrFile = os.path.join(corrDesFolder, '{}_TT{}corr.npz'.format(subject, tetrode))
                if os.path.isfile(corrFile):
                    #Load the correlations if they already exist
                    loadCorr = np.load(corrFile)
                    ccSelf = loadCorr['ccSelf']
                    ccAcross = loadCorr['ccAcross']
                else:
                    #Calculate the pairwise correlation between spikes
                    ccSelf, ccAcross = spikeshape_correlation(sessionWaves)
                    #Save the correlations
                    np.savez_compressed(corrFile, ccSelf=ccSelf, ccAcross=ccAcross)
                    print "Saving correlation file for Subject {} tetrode {}".format(subject, tetrode)

                #Loop self comparisons WITH THRESHOLD and save to file
                #DONE: Name the file according to animal and tetrode
                allSelfCorrVals = []; allSelfCorrLabs = []
                #allSelfCorrComps = []; 

                '''
                f = open('/tmp/{}_TT{}_SELF_{}thresh.txt'.format(subject, tetrode, corrThresh), 'w')
                header = '{}  TT{}  SELF correlation'.format(subject, tetrode)
                f.write(header)
                f.write('\n')
                '''
                for indSession, session in enumerate(sessions):
                    selfCompThisSession = ccSelf[indSession]
                    qualityMat = comparison_quality_filter(subject, session, session, tetrode, isiThresh, goodQualityList)
                    qualityMat = triangle_filter(qualityMat)
                    larray = comparison_label_array(session, session, tetrode)
                    goodCorrVals = selfCompThisSession[qualityMat]
                    goodCompLabs = larray[qualityMat]
                    #corrAboveThreshold = goodCorrVals[goodCorrVals>corrThresh]
                    #compsAboveThreshold = goodCompLabs[goodCorrVals>corrThresh]
                    #save out the values
                    allSelfCorrVals.extend(list(goodCorrVals))
                    allSelfCorrLabs.extend(list(goodCompLabs))
                    '''
                    message = '\n##------------## Session {} Self Comparison ##------------##\n'.format(session)
                    f.write(message)
                    # for corr in compsAboveThreshold:
                    #     f.write(corr)
                    #     f.write('\n')
                    for ind in np.argsort(corrAboveThreshold)[::-1]: #Argsort to print in descending order
                        f.write('{0:.2f} - '.format(corrAboveThreshold[ind]))
                        f.write(compsAboveThreshold[ind])
                        f.write('\n')
                f.close()
                '''
                outputFile = os.path.join(resultsDesFolder,'{}_TT{}_SELF_corr.npz'.format(subject, tetrode))
                np.savez(outputFile, subject=subject, tetrode=tetrode, ephysSessions=sessions, allSelfCorrVals=allSelfCorrVals, allSelfCorrLabs=allSelfCorrLabs)

                #DONE: Name the file according to animal and tetrode
                allCrossCorrVals = []; allCrossCorrLabs = []
                #allCrossCorrComps = []
                '''
                f = open('/tmp/{}_TT{}_CROSS_{}thresh.txt'.format(subject, tetrode, corrThresh), 'w')
                header = '{}  TT{}  CROSS correlation'.format(subject, tetrode)
                f.write(header)
                f.write('\n')
                '''
                for indComp, (session1, session2) in enumerate(zip(sessions, sessions[1:])):
                    crossCompTheseSessions = ccAcross[indComp]
                    qualityMat = comparison_quality_filter(subject, session1, session2, tetrode, isiThresh, goodQualityList)
                    larray = comparison_label_array(session1, session2, tetrode)
                    goodCorrVals = crossCompTheseSessions[qualityMat]
                    goodCompLabs = larray[qualityMat]
                    #corrAboveThreshold = goodCorrVals[goodCorrVals>corrThresh]
                    #compsAboveThreshold = goodCompLabs[goodCorrVals>corrThresh]
                    #save out the values
                    allCrossCorrVals.extend(list(goodCorrVals))
                    allCrossCorrLabs.extend(list(goodCompLabs))
                    '''
                    message = '\n##------Cross Comp {} x {}------##\n'.format(session1, session2)
                    f.write(message)
                    for ind in np.argsort(corrAboveThreshold)[::-1]: #Argsort to print in descending order
                        f.write('{0:.2f} - '.format(corrAboveThreshold[ind]))
                        f.write(compsAboveThreshold[ind])
                        f.write('\n')
                f.close()
                '''
                outputFile = os.path.join(resultsDesFolder,'{}_TT{}_CROSS_corr.npz'.format(subject, tetrode))
                np.savez(outputFile, subject=subject, tetrode=tetrode, ephysSessions=sessions, allCrossCorrVals=allCrossCorrVals, allCrossCorrLabs=allCrossCorrLabs)

    elif CASE==4:
        # Plot histogram of correlation values to visualize the range of corr values for each tetrode of one mouse
        import matplotlib.pyplot as plt

        subject = ANIMAL
        resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')

        def plot_corr_vals(corrvals, subject, tetrode, mode=None):
            #mode is 'self' or 'cross'
            meanCorrVal = np.mean(corrvals)
            sdCorrVale = np.std(corrvals)
            plt.clf()
            plt.hist(corrvals)
            plt.axvline(x=meanCorrVal+2*sdCorrVale, color='r')
            plt.xlim([-1,1])
            figname = '{} Tt{} {} correlation.pdf'.format(subject, tetrode, mode)
            plt.title(figname.split('.')[0])
            plt.savefig(os.path.join('/tmp/',figname))


        for filename in os.listdir(resultsDesFolder):
            fullFilename = os.path.join(resultsDesFolder, filename)
            if os.path.isfile(fullFilename) and subject in filename:
                if 'SELF' in filename:
                    selfCorrDb = np.load(fullFilename)
                    tetrode = int(selfCorrDb['tetrode'])
                    selfCorrValsThisT = selfCorrDb['allSelfCorrVals'] 
                    selfCorrLabsThisT = selfCorrDb['allSelfCorrLabs']
                    plot_corr_vals(selfCorrValsThisT, subject, tetrode, mode='self')

                elif 'CROSS' in filename:
                    crossCorrDb = np.load(fullFilename)
                    tetrode = int(crossCorrDb['tetrode'])
                    crossCorrValsThisT = crossCorrDb['allCrossCorrVals'] 
                    crossCorrLabsThisT = crossCorrDb['allCrossCorrLabs']
                    plot_corr_vals(crossCorrValsThisT, subject, tetrode, mode='cross')
   
    elif CASE==5:
        # Plot histogram of correlation values to visualize the range of corr values for all tetrodes of one mouse
        import matplotlib.pyplot as plt
        subject = ANIMAL
        numOfTetrode = 8
        corrThresh = 0.8
        resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')

        def plot_corr_vals(corrvals, subject, tetrode, mode=None):
            #mode is 'self' or 'cross' or 'both'
            meanCorrVal = np.mean(corrvals)
            sdCorrVale = np.std(corrvals)
            plt.clf()
            plt.hist(corrvals, bins=100)
            plt.axvline(x=meanCorrVal+2*sdCorrVale, color='r')
            plt.xlim([-1,1])
            if tetrode==None:
                tetrode = 'All'
            figname = '{} Tt {} {} correlation.pdf'.format(subject, tetrode, mode)
            plt.title(figname.split('.')[0])
            plt.savefig(os.path.join('/tmp/',figname))
        
        allCorrVals = np.array([]); allCorrLabs = np.array([])
        for filename in os.listdir(resultsDesFolder):
            fullFilename = os.path.join(resultsDesFolder, filename)
            if os.path.isfile(fullFilename) and subject in filename:
                if 'SELF' in filename:
                    selfCorrDb = np.load(fullFilename)
                    tetrode = int(selfCorrDb['tetrode'])
                    corrValsThisT = selfCorrDb['allSelfCorrVals']
                    corrLabsThisT = selfCorrDb['allSelfCorrLabs']
                elif 'CROSS' in filename:
                    crossCorrDb = np.load(fullFilename)
                    tetrode = int(crossCorrDb['tetrode'])
                    corrValsThisT = crossCorrDb['allCrossCorrVals'] 
                    corrLabsThisT = crossCorrDb['allCrossCorrLabs']
                allCorrVals = np.append(allCorrVals, corrValsThisT)
                allCorrLabs = np.append(allCorrLabs, corrLabsThisT)
        plot_corr_vals(allCorrVals, subject, tetrode=None, mode='both')

        #corrValsOverThresh = allCorrVals[allCorrVals>=corrThresh]
        #corrLabsOverThresh = allCorrLabs[allCorrVals>=corrThresh]
        #print corrLabsOverThresh
    

    elif CASE==6:
        import sys
        import importlib
        import matplotlib.pyplot as plt
        from jaratoolbox import settings
        from jaratoolbox import spikesorting
        from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
        
        # -- Isolate and plot side by side comparisons of cell pairs that has a correlation surpassing some threshold -- #
        subject = ANIMAL        
        corrThresh = 0.8
        resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')

        allCorrVals = np.array([]); allCorrLabs = np.array([])
        for filename in os.listdir(resultsDesFolder):
            fullFilename = os.path.join(resultsDesFolder, filename)
            if os.path.isfile(fullFilename) and subject in filename:
                if 'SELF' in filename:
                    selfCorrDb = np.load(fullFilename)
                    tetrode = int(selfCorrDb['tetrode'])
                    corrValsThisT = selfCorrDb['allSelfCorrVals']
                    corrLabsThisT = selfCorrDb['allSelfCorrLabs']
                elif 'CROSS' in filename:
                    crossCorrDb = np.load(fullFilename)
                    tetrode = int(crossCorrDb['tetrode'])
                    corrValsThisT = crossCorrDb['allCrossCorrVals'] 
                    corrLabsThisT = crossCorrDb['allCrossCorrLabs']
                allCorrVals = np.append(allCorrVals, corrValsThisT)
                allCorrLabs = np.append(allCorrLabs, corrLabsThisT)
                
        corrValsOverThresh = allCorrVals[allCorrVals>=corrThresh]
        corrLabsOverThresh = allCorrLabs[allCorrVals>=corrThresh]
        
        # -- Import allcells file -- #
        allcellsFileName = 'allcells_'+subject+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)
        allcells = importlib.import_module(allcellsFileName)
        
        outputDir = os.path.join(settings.EPHYS_PATH, 'cluster_analysis', subject)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)

        # -- Parse corr label to get cell infos -- #
        for (val,lab) in zip(corrValsOverThresh,corrLabsOverThresh):
            cell1,cell2 = lab.split(' x ')
            cellParamsList = []
            for cell in lab.split(' x '):
                behavSession = cell.split('_')[0].replace('-','')
                behavSession = behavSession + 'a'
                tetrode = cell.split('_')[2][1]
                cluster = cell.split('_')[2][3:]
                cellParams = {'firstParam':subject,
                              'behavSession':behavSession,
                              'tetrode':int(tetrode),
                              'cluster':int(cluster)}
                cellParamsList.append(cellParams)
            
            numRows = 3
            colsEachPan = 2
            panEachCell = 2
            numCols = colsEachPan*panEachCell*2
            # -- Plot the two cells side by side (waveform, ISI, events-in-time, tuning) -- #
            figname = '{}_{}x{}'.format(subject, cell1, cell2)
            figpath = os.path.join(outputDir, figname)
            if os.path.isfile(figpath):
                continue

            for ind,cellParams in enumerate(cellParamsList):
                cellIndex = allcells.cellDB.findcell(**cellParams)
                thisCell = allcells.cellDB[cellIndex]
                # -- Plot waveform, ISI, events-in-time based on 2afc session recording -- #
                spkData = loader.load_remote_2afc_spikes(thisCell)
               
                spkTimestamps = spkData.timestamps
                ax1 = plt.subplot2grid((numRows,numCols), (0,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                spikesorting.plot_isi_loghist(spkTimestamps)
                
                samples = spkData.samples
                ax2 = plt.subplot2grid((numRows,numCols), (1,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                spikesorting.plot_waveforms(samples)

                ax3 = plt.subplot2grid((numRows,numCols), (2,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                spikesorting.plot_events_in_time(spkTimestamps)
                
                # -- Plot tuning raster -- #
                ax4 = plt.subplot2grid((numRows,numCols), (0,ind*colsEachPan*panEachCell+2), colspan=colsEachPan, rowspan=3)
                loader.plot_tuning_raster_one_intensity(thisCell, intensity=50.0, timeRange = [-0.3,0.8])
                #ax5 = plt.subplot2grid((numRows,numCols), (2,ind*colsEachPan*panEachCell+2), colspan=colsEachPan)
                #loader.plot_tuning_PSTH_one_intensity(thisCell, intensity=50.0, timeRange = [-0.3,0.8],binWidth=0.01,halfFreqs=True)
            #plt.tight_layout()    
            figname = '{}_{}x{}'.format(subject, cell1, cell2)
            plt.suptitle(figname+'\n correlation: {}'.format(val))
            plt.savefig(figpath, format='png')
            
    
    elif CASE==7:
        # -- For Switching Mice: Pick out cell pairs with correlation value above threshold, only include the cell that has higher maxZ value in 2afc task. Do this separately for within and cross session correlations. --    
        
        import pdb

        corrThresh = 0.8
        switchingMice = ['test059','test089','test017','adap020']
        #switchingMice = ['adap020']
                
        # -- Import databases -- #
        switchingFilePath = os.path.join(settings.FIGURESDATA,STUDY_NAME)
        switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
        switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
        allcells_switching = pd.read_hdf(switchingFullPath,key='switching')
        
        goodCorrFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')

        #allCorrVals = np.array([]); allCorrLabs = np.array([])
        allMiceDfs = []
        for animal in switchingMice:
            # Process one mouse at a time
            dfThisMouse = allcells_switching.loc[allcells_switching['animalName'] == animal].reset_index()
            excludeDf = dfThisMouse[['animalName','behavSession','tetrode','cluster']]
            excludeDf['maxSoundRes'] = np.max(np.abs(dfThisMouse[['maxZSoundHigh','maxZSoundMid','maxZSoundLow']].values),axis=1)
            excludeDf['script'] = os.path.realpath(__file__)
            excludeDf['duplicate_self'] = 0
            excludeDf['duplicate_cross'] = 0
            excludeDf['duplicate_self_keep'] = 0
            excludeDf['duplicate_cross_keep'] = 0
            
            tetrodeNames = ['TT' + str(i) for i in range(1,9)]
            # -- Get all the cell pairs with correlation value over threshold -- #
            # First go through the SELF (same session) correlations; THE STRATEGY HERE IS TO POOL ALL DUPLICATE CELLS FROM THE SAME SESSION AND KEEP THE ONE WITH THE BIGGEST SOUND RESPONSE
            for tetrodeName in tetrodeNames:
                filenameSelf = animal + '_' + tetrodeName +'_SELF_corr.npz'
                fullFilenameSelf = os.path.join(goodCorrFolder, filenameSelf)
                selfCorrDb = np.load(fullFilenameSelf)
                tetrode = int(selfCorrDb['tetrode'])
                corrValsSelf = selfCorrDb['allSelfCorrVals']
                corrLabsSelf = selfCorrDb['allSelfCorrLabs']
                corrValsOverThreshSelf = corrValsSelf[corrValsSelf>=corrThresh]
                corrLabsOverThreshSelf = corrLabsSelf[corrValsSelf>=corrThresh]
                
                behavSessionList = [] #Keep a list of the sessions with clusters showing high self correlation 
                behavSessionPre = ''
                cellsThisSession = []
                for lab in sorted(corrLabsOverThreshSelf):
                    cell1,cell2 = lab.split(' x ')
                    behavSession = cell1.split('_')[0].replace('-','') + 'a'
                    if behavSession == behavSessionPre:
                        cellsThisSession.extend([cell1,cell2])
                    elif (behavSession != behavSessionPre) & (len(cellsThisSession) != 0):
                        behavSessionList.append(behavSession)
                        # -- Pick one cell out of all duplicates for the session -- #
                        tetrode = int(tetrodeName[-1])
                        clusterList = [int(cellstr.split('_')[2][3:]) for cellstr in cellsThisSession]
                        cells = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.behavSession==behavSessionPre) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster.isin(clusterList))]
                        excludeDf.ix[cells.index,'duplicate_self'] = 1
                        #maxSoundResEachCell = np.max(np.abs(cells[['maxZSoundHigh','maxZSoundMid','maxZSoundLow']].values),axis=1)
                        cellToKeepIndex = np.argmax(cells.maxSoundRes, axis=1)
                        excludeDf.ix[cellToKeepIndex, 'duplicate_self_keep'] = 1
                        cellsThisSession = [cell1,cell2]
                    else:
                        cellsThisSession = [cell1,cell2]
                    behavSessionPre = behavSession

                # -- Look at cross correlations and mark cells: whether they are duplicated cross sessions or not, and whether to keep them or not -- #    
                filenameCross = animal + '_' + tetrodeName +'_CROSS_corr.npz'
                fullFilenameCross = os.path.join(goodCorrFolder, filenameCross)
                crossCorrDb = np.load(fullFilenameCross)
                tetrode = int(crossCorrDb['tetrode'])
                corrValsCross = crossCorrDb['allCrossCorrVals'] 
                corrLabsCross = crossCorrDb['allCrossCorrLabs']
                corrValsOverThreshCross = corrValsCross[corrValsCross>=corrThresh]
                corrLabsOverThreshCross = corrLabsCross[corrValsCross>=corrThresh]
                
                for lab in sorted(corrLabsOverThreshCross):
                    #pdb.set_trace()
                    cell1,cell2 = lab.split(' x ')
                    cellInds = np.array([],dtype=int)
                    for ind,cellstr in enumerate([cell1, cell2]):
                        behavSession = cellstr.split('_')[0].replace('-','') + 'a'    
                        tetrode = int(tetrodeName[-1])
                        cluster = int(cellstr.split('_')[2][3:])
                        cell = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.behavSession==behavSession) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster==cluster)]
                        excludeDf.ix[cell.index,'duplicate_cross'] = 1
                        cellInds = np.append(cellInds, cell.index)
                        
                    soundResBothCells = excludeDf.iloc[cellInds]['maxSoundRes']
                    cellToKeepInd = np.argmax(soundResBothCells)
                    cellToDiscardInd = cellInds[cellInds != cellToKeepInd]
                    # -- Assign value to 'duplicate_cross_keep' column: 1-keep, 0-no status, -1:discard -- #
                    if excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] == 0: #cell with bigger sound response has not been compared before
                        excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] = 1
                        excludeDf.ix[cellToDiscardInd, 'duplicate_cross_keep'] = -1
                    elif excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] in [1,-1]: #cell with bigger sound response previously determined to be kept or to be discarded, do not change its result
                        excludeDf.ix[cellToDiscardInd, 'duplicate_cross_keep'] = -1

            # -- Summarize all duplicate screening into one column deciding whether to keep a cell or not -- #
            nonduplicate = (excludeDf.duplicate_self==0) & (excludeDf.duplicate_cross==0)
            duplicateBoth = (excludeDf.duplicate_self==1) & (excludeDf.duplicate_cross==1)
            duplicateSelfOnly = (excludeDf.duplicate_self==1) & (excludeDf.duplicate_cross==0)
            duplicateCrossOnly = (excludeDf.duplicate_self==0) & (excludeDf.duplicate_cross==1)
            duplicateBothKeep = duplicateBoth & (excludeDf.duplicate_self_keep==1) & (excludeDf.duplicate_cross_keep==1)
            duplicateSelfOnlyKeep = duplicateSelfOnly & (excludeDf.duplicate_self_keep==1)
            duplicateCrossOnlyKeep = duplicateCrossOnly & (excludeDf.duplicate_cross_keep==1)
            duplicateAnyKeep = duplicateSelfOnlyKeep | duplicateCrossOnlyKeep | duplicateBothKeep
            excludeDf['keep_after_dup_test'] = nonduplicate | duplicateAnyKeep

            # -- Put excludeDf together with this animal's switching celldb -- #
            dfs = [dfThisMouse,excludeDf]
            
            dfAllThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['animalName','behavSession','tetrode','cluster'],how='inner'), dfs)                    
            allMiceDfs.append(dfAllThisMouse)

        dfAllSwitchingMouse = pd.concat(allMiceDfs, ignore_index=True)
        dfAllSwitchingMouse.to_hdf(switchingFullPath, key='switching')




    
    elif CASE==8:
        # -- For Psychometric Mice: Pick out cell pairs with correlation value above threshold, only include the cell that has higher maxZ value in 2afc task. Do this separately for within and cross session correlations. --    
        
        import pdb

        corrThresh = 0.8
        psychometricMice = ['test055','test053','adap013','adap015','adap017']
        
        # -- Import databases -- #
        psychometricFilePath = os.path.join(settings.FIGURESDATA, STUDY_NAME)
        psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
        psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
        allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')
        
        goodCorrFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values')
        #allcells_psychometric = allcells_psychometric.drop('level_0',1)
        allMiceDfs = []
        for animal in psychometricMice:
            # Process one mouse at a time
            dfThisMouse = allcells_psychometric.loc[allcells_psychometric['animalName'] == animal].reset_index()
            excludeDf = dfThisMouse[['animalName','behavSession','tetrode','cluster']]
            ## !! PSYCHOMETRIC MAX SOUND RESPONSE BASED ON RESPONSE TO THE TWO MIDDLE FREQS !! ##
            excludeDf['maxSoundRes'] = np.max(np.abs(dfThisMouse[['maxZSoundMid1','maxZSoundMid2']].values),axis=1)
            excludeDf['script'] = os.path.realpath(__file__)
            excludeDf['duplicate_self'] = 0
            excludeDf['duplicate_cross'] = 0
            excludeDf['duplicate_self_keep'] = 0
            excludeDf['duplicate_cross_keep'] = 0
            
            tetrodeNames = ['TT' + str(i) for i in range(1,9)]
            # -- Get all the cell pairs with correlation value over threshold -- #
            # First go through the SELF (same session) correlations; THE STRATEGY HERE IS TO POOL ALL DUPLICATE CELLS FROM THE SAME SESSION AND KEEP THE ONE WITH THE BIGGEST SOUND RESPONSE
            for tetrodeName in tetrodeNames:
                filenameSelf = animal + '_' + tetrodeName +'_SELF_corr.npz'
                fullFilenameSelf = os.path.join(goodCorrFolder, filenameSelf)
                selfCorrDb = np.load(fullFilenameSelf)
                tetrode = int(selfCorrDb['tetrode'])
                corrValsSelf = selfCorrDb['allSelfCorrVals']
                corrLabsSelf = selfCorrDb['allSelfCorrLabs']
                corrValsOverThreshSelf = corrValsSelf[corrValsSelf>=corrThresh]
                corrLabsOverThreshSelf = corrLabsSelf[corrValsSelf>=corrThresh]
                
                behavSessionList = [] #Keep a list of the sessions with clusters showing high self correlation 
                behavSessionPre = ''
                cellsThisSession = []
                for lab in sorted(corrLabsOverThreshSelf):
                    cell1,cell2 = lab.split(' x ')
                    behavSession = cell1.split('_')[0].replace('-','') + 'a'
                    if behavSession == behavSessionPre:
                        cellsThisSession.extend([cell1,cell2])
                    elif (behavSession != behavSessionPre) & (len(cellsThisSession) != 0):
                        behavSessionList.append(behavSession)
                        # -- Pick one cell out of all duplicates for the session -- #
                        tetrode = int(tetrodeName[-1])
                        clusterList = [int(cellstr.split('_')[2][3:]) for cellstr in cellsThisSession]
                        cells = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.behavSession==behavSession) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster.isin(clusterList))]
                        excludeDf.ix[cells.index,'duplicate_self'] = 1
                        #maxSoundResEachCell = np.max(np.abs(cells[['maxZSoundHigh','maxZSoundMid','maxZSoundLow']].values),axis=1)
                        cellToKeepIndex = np.argmax(cells.maxSoundRes, axis=1)
                        excludeDf.ix[cellToKeepIndex, 'duplicate_self_keep'] = 1
                        cellsThisSession = [cell1,cell2]
                    else:
                        cellsThisSession = [cell1,cell2]
                    behavSessionPre = behavSession

                # -- Look at cross correlations and mark cells: whether they are duplicated cross sessions or not, and whether to keep them or not -- #    
                filenameCross = animal + '_' + tetrodeName +'_CROSS_corr.npz'
                fullFilenameCross = os.path.join(goodCorrFolder, filenameCross)
                crossCorrDb = np.load(fullFilenameCross)
                tetrode = int(crossCorrDb['tetrode'])
                corrValsCross = crossCorrDb['allCrossCorrVals'] 
                corrLabsCross = crossCorrDb['allCrossCorrLabs']
                corrValsOverThreshCross = corrValsCross[corrValsCross>=corrThresh]
                corrLabsOverThreshCross = corrLabsCross[corrValsCross>=corrThresh]
                
                for lab in sorted(corrLabsOverThreshCross):
                    #pdb.set_trace()
                    cell1,cell2 = lab.split(' x ')
                    cellInds = np.array([],dtype=int)
                    for ind,cellstr in enumerate([cell1, cell2]):
                        behavSession = cellstr.split('_')[0].replace('-','') + 'a'    
                        tetrode = int(tetrodeName[-1])
                        cluster = int(cellstr.split('_')[2][3:])
                        cell = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.behavSession==behavSession) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster==cluster)]
                        excludeDf.ix[cell.index,'duplicate_cross'] = 1
                        cellInds = np.append(cellInds, cell.index)
                        
                    soundResBothCells = excludeDf.iloc[cellInds]['maxSoundRes']
                    cellToKeepInd = np.argmax(soundResBothCells)
                    cellToDiscardInd = cellInds[cellInds != cellToKeepInd]
                    # -- Assign value to 'duplicate_cross_keep' column: 1-keep, 0-no status, -1:discard -- #
                    if excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] == 0: #cell with bigger sound response has not been compared before
                        excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] = 1
                        excludeDf.ix[cellToDiscardInd, 'duplicate_cross_keep'] = -1
                    elif excludeDf.ix[cellToKeepInd, 'duplicate_cross_keep'] in [1,-1]: #cell with bigger sound response previously determined to be kept or to be discarded, do not change its result
                        excludeDf.ix[cellToDiscardInd, 'duplicate_cross_keep'] = -1

            # -- Summarize all duplicate screening into one column deciding whether to keep a cell or not -- #
            nonduplicate = (excludeDf.duplicate_self==0) & (excludeDf.duplicate_cross==0)
            duplicateBoth = (excludeDf.duplicate_self==1) & (excludeDf.duplicate_cross==1)
            duplicateSelfOnly = (excludeDf.duplicate_self==1) & (excludeDf.duplicate_cross==0)
            duplicateCrossOnly = (excludeDf.duplicate_self==0) & (excludeDf.duplicate_cross==1)
            duplicateBothKeep = duplicateBoth & (excludeDf.duplicate_self_keep==1) & (excludeDf.duplicate_cross_keep==1)
            duplicateSelfOnlyKeep = duplicateSelfOnly & (excludeDf.duplicate_self_keep==1)
            duplicateCrossOnlyKeep = duplicateCrossOnly & (excludeDf.duplicate_cross_keep==1)
            duplicateAnyKeep = duplicateSelfOnlyKeep | duplicateCrossOnlyKeep | duplicateBothKeep
            excludeDf['keep_after_dup_test'] = nonduplicate | duplicateAnyKeep

            # -- Put excludeDf together with this animal's psychometric celldb -- #
            dfs = [dfThisMouse,excludeDf]
            
            dfAllThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['animalName','behavSession','tetrode','cluster'],how='inner'), dfs)                    
            allMiceDfs.append(dfAllThisMouse)

        dfAllPsychometricMouse = pd.concat(allMiceDfs, ignore_index=True)
        dfAllPsychometricMouse.to_hdf(psychometricFullPath, key='psychometric')
                       
     

