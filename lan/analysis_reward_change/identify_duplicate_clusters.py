'''
Calcualte the average waveform(4 channels) of clusters produced by spike-sorting, identify duplicate cells in the same session or in sessions of the same depth by cross correlation between waveforms.
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting
# from jaratoolbox import celldatabase
from jaratoolbox import loadopenephys
from jaratoolbox import settings
reload(settings)
import itertools #For making string combinations of all comparisons
import pickle #For saving the waveform objects

#For calling rsync to get just the data we need
#import subprocess

import pandas as pd

#from jaratoolbox import ephyscore


STUDY_NAME = '2017rewardchange'

def find_2afc_ephys_sessions(celldb, tetrode):
    celldbThisTetrode = celldb.loc[celldb['tetrode']==tetrode]
    inds = celldbThisTetrode['sessiontype'].apply(lambda x: x.index('behavior'))
    behavEphysSessionsEachCell = celldbThisTetrode.apply(lambda row: row['ephys'][inds[row.name]], axis=1)
    sortedUniqueEphysSessions = sorted(set(behavEphysSessionsEachCell.values))
    return sortedUniqueEphysSessions

def waveforms_many_sessions(subject, cellDB, ephysSessions, tetrode,  wavesize=160):
    '''
    Create a list of arrays containing waveforms for each session for one tetrode.
    '''
    waveformsOneTetrode = []
    for oneSession in ephysSessions:
        waves = calculate_avg_waveforms(subject, cellDB, oneSession, tetrode,
                                 wavesize=wavesize)
        waveformsOneTetrode.append(waves)
    return waveformsOneTetrode

def calculate_avg_waveforms(subject, cellDB, ephysSession, tetrode,  wavesize=160):
    '''
    NOTE: This methods should look through sessions, not clusters.
          The idea is to compare clusters within a tetrode, and then across sessions
          but still within a tetrode.
    NOTE: This method is inefficient because it load the spikes file for each cluster.
    '''
    
    date = ephysSession.split('_')[0]
    #passingClusters = np.array(np.repeat(0,12), dtype=bool) #default to all false
    cells = cellDB.loc[(cellDB.date==date) & (cellDB.tetrode==tetrode)]
    if len(cells) == 0: #This tetrode doesn't exist in this session
        allWaveforms = None
    else:
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
        clustersThisSession = np.unique(clusters)
        numClustersThisTetrode = len(cells) #Sometimes clustersThisSession don't include all the possible clusters this tetrode!
        # DONE: loop through clusters
        allWaveforms = np.empty((numClustersThisTetrode,wavesize))
        for indc, cluster in enumerate(clustersThisSession):
            print 'Estimating average waveform for {0} T{1}c{2}'.format(ephysSession,tetrode,cluster)

            # DONE: get waveforms for one cluster
            waveforms = spikes.samples[clusters==cluster, :, :]
            alignedWaveforms = spikesorting.align_waveforms(waveforms)
            meanWaveforms = np.mean(alignedWaveforms,axis=0)
            allWaveforms[cluster-1,:] = meanWaveforms.flatten()
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
    #inds=-1 # Needed in case only one waveform
    for inds in range(len(waveforms)-1):
        if np.any(waveforms[inds]) and np.any(waveforms[inds+1]):
            ccSelf.append(row_corrcoeff(waveforms[inds],waveforms[inds]))
            ccAccross.append(row_corrcoeff(waveforms[inds],waveforms[inds+1]))
        else:
            continue
    if np.any(waveforms[inds+1]):
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


def locate_cell_in_celldb(celldb, animal, behavSession, tetrode, cluster):
    '''
    Given a cell's parameters and a celldb(pandas DataFrame), locate the cell. Returns either an empty dataframe or a dataframe(subset of original) containing this cell.
    '''
    cell = allce.loc[(celldb.animalName==animal) & (celldb.behavSession==behavSession) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)]
    return cell


def comparison_quality_filter(cellDB, session1, session2, tetrode, isiThresh=0.02, qualityThresh=2.5):  
    '''
    OVERWRITE this function, now using database look up. 
    Returns a matrix where pair comparisons between good cells are 1 and 0 otherwise.
    '''
    session1good = session_good_clusters(cellDB, session1, tetrode, isiThresh, qualityThresh).astype(int)
    #print session1good
    session2good = session_good_clusters(cellDB, session2, tetrode, isiThresh, qualityThresh).astype(int)
    #print session2good
    #Make a boolean matrix from the two quality vectors, with 1 only if both are 1
    #DONE: Which should come first for the across session comparisons?
    #session 1 becomes the rows, which is the same as the corr function
    qualityMat = np.outer(session1good.astype(int), session2good.astype(int)).astype(bool)

    return qualityMat
  
def session_good_clusters(cellDB, session, tetrode, isiThresh, qualityThresh, consistencyChecked=True):
    '''
    Now this function uses database look up to determine quality of clusters. Return a 12-item bool vector, containing True if the cluster was good quality and False otherwise
    '''
    # The 'session' passed is the ephys session, need to convert it to the date
    date = session.split('_')[0]
    #passingClusters = np.array(np.repeat(0,12), dtype=bool) #default to all false
    cells = cellDB.loc[(cellDB.date==date) & (cellDB.tetrode==tetrode)]
    if len(cells) > 12:
        print 'ATTENTION: for {} on {}, 2afc session has {} clusters'.format(animal, date, tetrode, len(cells))
    
    if np.any(cells):
        goodQualityCells = (cells.shapeQuality >= qualityThresh)
        lowISICells = (cells.isiViolations <= isiThresh)
        if consistencyChecked:
            consistentFiring = (cells.consistentInFiring == True)
            passingClusters = (goodQualityCells & lowISICells & consistentFiring).values
        else:
            passingClusters = (goodQualityCells & lowISICells).values
    else:
        passingClusters = np.zeros(12)
    return passingClusters

    
def comparison_label_array(cellDB, session1, session2, tetrode):
    '''
    Returns an array of strings that describe the comparisons made between two sessions
    '''
    date1 = session1.split('_')[0]
    date2 = session2.split('_')[0]
    cells1 = cellDB.loc[(cellDB.date==date1) & (cellDB.tetrode==tetrode)]
    cells2 = cellDB.loc[(cellDB.date==date2) & (cellDB.tetrode==tetrode)]

    clabs1 = ['{}_T{}c{}'.format(session1, tetrode, cnum) for cnum in cells1.cluster]
    clabs2 = ['{}_T{}c{}'.format(session2, tetrode, cnum) for cnum in cells2.cluster]
    labs = ['{} x {}'.format(cl1, cl2) for cl1, cl2 in itertools.product(clabs1, clabs2)]
    larray = np.array(labs, dtype=str).reshape((len(cells1), len(cells2)))
    return larray

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
    isiThresh = 0.02 #The upper threshold for ISI violations
    qualityThresh = 3 #2.5
    consistencyChecked=True
    
    CASE = 3

    #ANIMALS = ['adap017','adap013']
    brainRegion = 'ac'
    ANIMALS = ['gosi004','gosi010']
    # -- Calculate waveform, correlations within and across 2 consecutive sessions for each tetrode in each animal -- #
    if CASE==1:
        for animal in ANIMALS:
            subject = animal
            tetrodes = range(1, 9)
            #corrThresh = 0.7 #The lower limit for the correlation value 
            #goodQualityList = [1,6] #Qaulity score for good cells
            ## -- Load cellDB of this animal -- #
            celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(brainRegion))
            cellDBAll = pd.read_hdf(celldbPath, key='reward_change')
            
            cellDB = cellDBAll.loc[cellDBAll['subject'] == animal].reset_index()
            #cellDB = cellDB.drop_duplicates(['subject','date','tetrode','cluster'])

            ### -- DO THIS PER TETRODE -- ###
            waveDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/wavefiles/{}'.format(STUDY_NAME)) 
            corrDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/corrfiles/{}'.format(STUDY_NAME))
            resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values/{}'.format(STUDY_NAME))
            for folder in (waveDesFolder, corrDesFolder, resultsDesFolder):
                if not os.path.exists(folder):
                    os.mkdir(folder)

            for tetrode in tetrodes:
                #Find all the 2afc sessions for this animal this tetrode
                sessions = find_2afc_ephys_sessions(cellDB, tetrode)
                clusterDirs = ['{}_kk'.format(session) for session in sessions]
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
                    sessionWaves = waveforms_many_sessions(subject, cellDB, sessions, tetrode)
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

                for indSession, session in enumerate(sessions):
                    try:
                        selfCompThisSession = ccSelf[indSession]
                        qualityMat = comparison_quality_filter(cellDB, session, session, tetrode, isiThresh, qualityThresh)
                        qualityMat = triangle_filter(qualityMat)
                        larray = comparison_label_array(cellDB, session, session, tetrode)
                        goodCorrVals = selfCompThisSession[qualityMat]
                        goodCompLabs = larray[qualityMat]
                        #corrAboveThreshold = goodCorrVals[goodCorrVals>corrThresh]
                        #compsAboveThreshold = goodCompLabs[goodCorrVals>corrThresh]
                        #save out the values
                        allSelfCorrVals.extend(list(goodCorrVals))
                        allSelfCorrLabs.extend(list(goodCompLabs))
                    except IndexError: # This is when a tetrode don't have data for all the sessions
                        continue
                outputFile = os.path.join(resultsDesFolder,'{}_TT{}_SELF_corr.npz'.format(subject, tetrode))
                np.savez(outputFile, subject=subject, tetrode=tetrode, ephysSessions=sessions, allSelfCorrVals=allSelfCorrVals, allSelfCorrLabs=allSelfCorrLabs)

                #DONE: Name the file according to animal and tetrode
                allCrossCorrVals = []; allCrossCorrLabs = []
                #allCrossCorrComps = []
                
                for indComp, (session1, session2) in enumerate(zip(sessions, sessions[1:])):
                    try:
                        crossCompTheseSessions = ccAcross[indComp]
                        qualityMat = comparison_quality_filter(cellDB, session1, session2, tetrode, isiThresh, qualityThresh)
                        larray = comparison_label_array(cellDB, session1, session2, tetrode)
                        goodCorrVals = crossCompTheseSessions[qualityMat]
                        goodCompLabs = larray[qualityMat]
                        #corrAboveThreshold = goodCorrVals[goodCorrVals>corrThresh]
                        #compsAboveThreshold = goodCompLabs[goodCorrVals>corrThresh]
                        #save out the values
                        allCrossCorrVals.extend(list(goodCorrVals))
                        allCrossCorrLabs.extend(list(goodCompLabs))
                    except IndexError: # This is when a tetrode don't have data for all the sessions
                        continue
                outputFile = os.path.join(resultsDesFolder,'{}_TT{}_CROSS_corr.npz'.format(subject, tetrode))
                np.savez(outputFile, subject=subject, tetrode=tetrode, ephysSessions=sessions, allCrossCorrVals=allCrossCorrVals, allCrossCorrLabs=allCrossCorrLabs)

    # -- Isolate and plot side by side comparisons of cell pairs that has a correlation surpassing some threshold -- #
    elif CASE==2:
        import sys
        import pdb
        import importlib
        import matplotlib.pyplot as plt
        from jaratoolbox import settings
        from jaratoolbox import spikesorting
        from jaratest.lan.analysis_reward_change import reward_change_loader_plotter_functions as rcfuncs
        reload(rcfuncs)
        
        #subject = 'gosi001'        
        corrThresh = 0.9
        resultsDesFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values/{}'.format(STUDY_NAME))

        for animal in ANIMALS:
            subject = animal
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

            outputDir = os.path.join(settings.EPHYS_PATH, 'cluster_analysis', subject)
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)
            #pdb.set_trace()
            # -- Parse corr label to get cell infos -- #
            if not np.any(corrValsOverThresh):
                pass
            for (val,lab) in zip(corrValsOverThresh,corrLabsOverThresh):
                cell1,cell2 = lab.split(' x ')
                cellParamsList = []
                for cell in lab.split(' x '):
                    date = cell.split('_')[0]
                    behavSession = cell.split('_')[0].replace('-','')
                    behavSession = behavSession + 'a'
                    ephysSession = '_'.join((date,cell.split('_')[1]))
                    tetrode = cell.split('_')[2][1]
                    cluster = float(cell.split('_')[2][3:])
                    cellParams = {'animal':subject,
                                  'ephysSession':ephysSession,
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
                    # -- Plot waveform, ISI, events-in-time based on 2afc session recording -- #
                    animal = cellParams['animal']
                    rcEphysThisCell = cellParams['ephysSession']
                    rcBehavThisCell = '{}_2afc_{}.h5'.format(animal,cellParams['behavSession'])
                    tetrode = cellParams['tetrode']
                    cluster = cellParams['cluster']
                    ax1 = plt.subplot2grid((numRows,numCols), (0,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                    rcfuncs.plot_isi_loghist_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                    ax2 = plt.subplot2grid((numRows,numCols), (1,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                    rcfuncs.plot_waveform_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                    ax3 = plt.subplot2grid((numRows,numCols), (2,ind*colsEachPan*panEachCell), colspan=colsEachPan)
                    rcfuncs.plot_events_in_time_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                    # -- Plot 2afc raster -- #
                    ax4 = plt.subplot2grid((numRows,numCols), (0,ind*colsEachPan*panEachCell+2), colspan=colsEachPan, rowspan=3)
                    rcfuncs.plot_reward_change_raster(animal, rcBehavThisCell, rcEphysThisCell, tetrode, cluster, freqToPlot='both', byBlock=True, alignment='sound', timeRange=[-0.3,0.4]) 
                figname = '{}_{}x{}'.format(subject, cell1, cell2)
                plt.suptitle(figname+'\n correlation: {}'.format(val))
                plt.savefig(figpath, format='png')

    
    elif CASE==3:
        # -- For Reward-change Mice: Pick out cell pairs with correlation value above threshold, only include the cell that has higher maxZ value in 2afc task. Do this separately for within and cross session correlations. --    
        
        import pdb

        corrThresh = 0.9
        #brainRegion = 'astr'
        rewardChangeMice = ['adap013','adap015','adap017']
        
        # -- Import databases -- #
        #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(brainRegion))
        #allcells_rewardChange = pd.read_hdf(celldbPath, key='reward_change')
        goodCorrFolder = os.path.join(settings.EPHYS_PATH, 'cluster_analysis/good_corr_values/{}'.format(STUDY_NAME))
        #allcells_rewardChange = allcells_rewardChange.drop('level_0',1)
        #allMiceDfs = []
        for animal in rewardChangeMice:
            celldbPath = os.path.join(settings.DATABASE_PATH,'{}_database.h5'.format(animal))
            # Process one mouse at a time
            #dfThisMouse = allcells_rewardChange.loc[allcells_rewardChange['subject'] == animal].reset_index()
            dfThisMouse = pd.read_hdf(celldbPath, key='reward_change')
            excludeDf = dfThisMouse[['animalName', 'date', 'tetrode','cluster']]
            ## !! REWARD-CHANGE MAX SOUND RESPONSE BASED ON RESPONSE TO THE TWO FREQS !! ##
            #excludeDf['maxSoundRes'] = np.max(np.abs(dfThisMouse[['maxZSoundMid1','maxZSoundMid2']].values),axis=1)
            excludeDf['maxSoundRes'] = dfThisMouse.behavZscore.apply(lambda x: np.max(np.abs(x))).values
            excludeDf['script'] = os.path.realpath(__file__)
            excludeDf['duplicate_self'] = 0
            excludeDf['duplicate_cross'] = 0
            excludeDf['duplicate_self_keep'] = 0
            excludeDf['duplicate_cross_keep'] = 0
            
            tetrodeNames = ['TT' + str(i) for i in range(1,9)]
            # -- Get all the cell pairs with correlation value over threshold -- #
            # First go through the SELF (same session) correlations; THE STRATEGY HERE IS TO POOL ALL DUPLICATE CELLS FROM THE SAME SESSION AND KEEP THE ONE WITH THE BIGGEST SOUND RESPONSE
            for tetrodeName in tetrodeNames:
                print 'Finding same session duplicates for {}'.format(tetrodeName)
                filenameSelf = animal + '_' + tetrodeName +'_SELF_corr.npz'
                fullFilenameSelf = os.path.join(goodCorrFolder, filenameSelf)
                selfCorrDb = np.load(fullFilenameSelf)
                tetrode = int(selfCorrDb['tetrode'])
                corrValsSelf = selfCorrDb['allSelfCorrVals']
                corrLabsSelf = selfCorrDb['allSelfCorrLabs']
                corrValsOverThreshSelf = corrValsSelf[corrValsSelf>=corrThresh]
                corrLabsOverThreshSelf = corrLabsSelf[corrValsSelf>=corrThresh]
                print 'Label pairs that crossed threshold:', len(corrLabsOverThreshSelf)
                behavSessionList = [] #Keep a list of the sessions with clusters showing high self correlation 
                behavSessionPre = ''
                cellsThisSession = []
                dateLastSess = ''
                for lab in sorted(corrLabsOverThreshSelf):
                    cell1,cell2 = lab.split(' x ')
                    behavSession = cell1.split('_')[0].replace('-','') + 'a'
                    date = cell1.split('_')[0]
                    if behavSession == behavSessionPre:
                        cellsThisSession.extend([cell1,cell2])
                    elif (behavSession != behavSessionPre) & (len(cellsThisSession) != 0):
                        behavSessionList.append(behavSession)
                        print 'Finding same session duplicates for {} {}'.format(dateLastSess, tetrodeName)
                        # -- Pick one cell out of all duplicates for the session that was just done processing (the last session!) -- #
                        tetrode = int(tetrodeName[-1])
                        clusterList = [int(float(cellstr.split('_')[2][3:])) for cellstr in cellsThisSession]
                        print 'tetrode {}, clusters: {}'.format(tetrode, clusterList)
                        cells = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.date==dateLastSess) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster.isin(clusterList))] 
                        excludeDf.ix[cells.index,'duplicate_self'] = 1
                        #maxSoundResEachCell = np.max(np.abs(cells[['maxZSoundHigh','maxZSoundMid','maxZSoundLow']].values),axis=1)
                        cellToKeepIndex = np.argmax(cells.maxSoundRes, axis=1)
                        excludeDf.ix[cellToKeepIndex, 'duplicate_self_keep'] = 1
                        cellsThisSession = [cell1,cell2]
                    else:
                        cellsThisSession = [cell1,cell2]
                    behavSessionPre = behavSession
                    dateLastSess = date

                # -- Look at cross correlations and mark cells: whether they are duplicated cross sessions or not, and whether to keep them or not -- #    
                print 'Finding cross session duplicates for {}'.format(tetrodeName)
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
                        date = cellstr.split('_')[0]
                        tetrode = int(tetrodeName[-1])
                        cluster = int(float(cellstr.split('_')[2][3:]))
                        cell = excludeDf.loc[(excludeDf.animalName==animal) & (excludeDf.date==date) & (excludeDf.tetrode==tetrode) & (excludeDf.cluster==cluster)]
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

            # -- Put excludeDf together with this animal's rewardChange celldb -- #
            dfs = [dfThisMouse,excludeDf]
            
            dfAllThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['animalName','date','tetrode','cluster'],how='inner'), dfs)      
            dfAllThisMouse.to_hdf(celldbPath, key = 'reward_change')
            #allMiceDfs.append(dfAllThisMouse)

        #dfAllRewardChangeMouse = pd.concat(allMiceDfs, ignore_index=True)
        #dfAllRewardChangeMouse.to_hdf(rewardChangeFullPath, key='rewardChange')
                       
     

