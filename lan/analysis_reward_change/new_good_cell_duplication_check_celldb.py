'''
Calcualte the average waveform(4 channels) of clusters produced by spike-sorting, identify duplicate cells in the same session or in sessions of the same depth by cross correlation between waveforms.
'''
import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting
from jaratoolbox import settings
reload(settings)
import pandas as pd
from jaratoolbox import ephyscore
import pdb

#STUDY_NAME = '2017rewardchange'
wavesize = 160

def get_all_same_session_cells(celldb):
    '''
    Find the cells recorded in the same session on the same tetrode.
    Args: 
        celldb: a pandas dataframe containing only good quality cells.
    Returns:
        sameSessionCellsDict: a dictionary where each key indicates a 
            unique date/tetrode from the celldb where more than one cell exist; 
            each value is the rows in celldb that contain cells recorded on the 
            date and tetrode indicated by the key.
    '''
    sameSessionCellsDict = {}
    for date in np.unique(celldb.date):
        cellsThisSession = celldb.loc[celldb.date==date]
        tetrodes = cellsThisSession.tetrode
        for tetrode in np.unique(tetrodes):
            cellsThisSessThisTt = cellsThisSession.query('tetrode=={}'.format(tetrode))
            if len(cellsThisSessThisTt) > 1:
                sameSessionCellsDict.update({date+'_Tt{}'.format(tetrode):cellsThisSessThisTt}) 

    return sameSessionCellsDict


def get_all_consecutive_session_cells(celldb):
    '''
    Find the cells recorded in two 'consecutive' session on the same tetrode.
    Args: 
        celldb: a pandas dataframe containing only good quality cells.
    Returns:
        consecutiveSessCellsDict: a dictionary where each key indicates a 
            unique pair of dates/tetrode from the celldb where more than one cell exist; 
            each value is the rows in celldb that contain cells recorded on those 
            dates and tetrode indicated by the key.
    NOTE: this function defines 'consecutive' dates as two neighbouring sessions in 
    the celldb, their actual recording date may or may not be 1 day different from each other.
    '''
    dateStrs = np.unique(celldb.date)
    #dates = [datetime.datetime.strptime(str, "%Y-%m-%d") for str in dateStrs]
    #possibleConsecutiveDates = []
    #for ind in range(len(dates)-1):
        #possibleConsecutiveDates.append([dates[ind], dates[ind+1]]) 
    #step = datetime.timedelta(days=1)
    #consecutiveDates = [pair for pair in possibleConsecutiveDates if (pair[0]+step==pair[1])]
    consecutiveDates = []
    for ind in range(len(dateStrs) -1):
        consecutiveDates.append([dateStrs[ind], dateStrs[ind+1]]) 
    consecutiveSessCellsDict = {}
    for pairOfDates in consecutiveDates:
        cellsDate1 = celldb.loc[celldb.date==pairOfDates[0]]
        cellsDate2 = celldb.loc[celldb.date==pairOfDates[1]]
        tetrodes = cellsDate1.tetrode
        for tetrode in np.unique(tetrodes):
            if tetrode in np.unique(cellsDate2.tetrode):
                cellsDate1ThisTt = cellsDate1.query('tetrode=={}'.format(tetrode))
                cellsDate2ThisTt = cellsDate2.query('tetrode=={}'.format(tetrode))
                consecutiveSessCellsDict.update({'_'.join((pairOfDates))+'Tt{}'.format(tetrode):[cellsDate1ThisTt, cellsDate2ThisTt]})
    pdb.set_trace()
    return consecutiveSessCellsDict
        

def get_all_waveforms_one_session(celldb, wavesize=160, sessionToUse='behavior'):
    '''
    Load waveforms for each row of a celldb for one type of session.
    Args:
        celldb: a pandas dataframe containing only good quality cells (containing n cells).
        wavesize: number of samples in a waveform, usually 160 for all 4 channels of a tetrode.
        sessionToUse: which type of session we want to load the waveform from.
    Returns:
        allWaveforms: a nd-array in the shape of (nCells, mSamples).
    '''
    numCells = len(celldb)
    allWaveforms = np.zeros((numCells, wavesize))
    for indc, (ind,cell) in enumerate(celldb.iterrows()):
        cellObj = ephyscore.Cell(cell)
        sessionInd = cellObj.get_session_inds(sessionToUse)[0]
        try:
            ephysData = cellObj.load_ephys_by_index(sessionInd)
            samples = ephysData['samples']
            alignedWaveforms = spikesorting.align_waveforms(samples)
            meanWaveforms = np.mean(alignedWaveforms,axis=0)
            allWaveforms[indc,:] = meanWaveforms.flatten()
        except ValueError:
            print 'Cell {} did not have any spikes in the {} session'.format(ind, sessionToUse)
            continue 

    return allWaveforms
   

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



def find_within_session_duplicates(celldb, threshold):
    '''
    Find within session duplicates and mark them, determine which ones to discard based on sound responsiveness.
    Args:
        celldb: a pandas dataframe containing only good quality cells (containing n cells).
        threshold: the correlation value above which two cells were qualified as 'duplicates'.
    Returns:
        excludeDf: a pandas dataframe with same number of rows as celldb,
        containing a column about whether a cell is a within-session 
        duplicate ('duplicate_self'), and a column about wheterh a cell
        is discarded ('duplicate_self_discard') based on sound responsiveness.
    '''
    excludeDf = celldb[['date', 'tetrode','cluster']]
    excludeDf['duplicate_self'] = 0
    excludeDf['duplicate_self_discard'] = 0
    excludeDf['maxSoundRes'] = celldb.behavZscore.apply(lambda x: np.max(np.abs(x))).values
    
    sameSessionCellsDict = get_all_same_session_cells(celldb)
    for (date,cellsThisSess) in sameSessionCellsDict.items():
        waveformsThisSess = get_all_waveforms_one_session(cellsThisSess, wavesize=160)
        corrMat = row_corrcoeff(waveformsThisSess, waveformsThisSess)
        corrMatFiltered = np.tril(corrMat, k=-1) > threshold
        dupInds = np.unique(np.concatenate(np.nonzero(corrMatFiltered)))
        if np.any(dupInds):
            dupCellsInds = cellsThisSess.index[dupInds]
            dupCells = excludeDf.loc[dupCellsInds] 
            excludeDf.ix[dupCellsInds, 'duplicate_self'] = 1
            cellToKeepIndex = np.argmax(dupCells.maxSoundRes, axis=1)
            cellToDiscardIndex = dupCellsInds[dupCellsInds!= cellToKeepInd]
            excludeDf.ix[cellToDiscardIndex, 'duplicate_self_discard'] = 1
    return excludeDf


def find_cross_session_duplicates(celldb, threshold):
    '''
    Find cross session duplicates and mark them, determine which ones to discard based on sound responsiveness.
    Args:
        celldb: a pandas dataframe containing only good quality cells (containing n cells).
        threshold: the correlation value above which two cells were qualified as 'duplicates'.
    Returns:
        excludeDf: a pandas dataframe with same number of rows as celldb,
        containing a column about whether a cell is duplicated in two consecutive sessions
        ('duplicate_cross'), and a column about wheterh a cell is discarded 
        ('duplicate_cross_discard') based on sound responsiveness.
    NOTE: this function assumes two cells will likely not be duplicates of one another in
    two sessions that are not 'consecutive' and do not compare or discard cells that 
    are duplicated in more than two consecutive sessions.
    '''
    excludeDf = cellDB[['date', 'tetrode','cluster']]
    excludeDf['duplicate_cross'] = 0
    excludeDf['duplicate_cross_discard'] = 0
    excludeDf['maxSoundRes'] = celldb.behavZscore.apply(lambda x: np.max(np.abs(x))).values
    
    consecutiveSessCellsDict = get_all_consecutive_session_cells(celldb)
    for (pairOfDates,[cellsSess1,cellsSess2]) in consecutiveSessCellsDict.items():
        waveformsSess1 = get_all_waveforms_one_session(cellsSess1, wavesize=160)
        waveformsSess2 = get_all_waveforms_one_session(cellsSess2, wavesize=160)
        corrMat = row_corrcoeff(waveformsSess1, waveformsSess2)
        corrMatFiltered = corrMat > threshold
        dupIndsSess1 = np.nonzero(corrMatFiltered)[0]
        dupIndsSess2 = np.nonzero(corrMatFiltered)[1]
        dupCellsInds1 = cellsSess1.index[dupIndsSess1]
        dupCellsInds2 = cellsSess2.index[dupIndsSess2]
        dupCellsInds = np.concatenate((dupCellsInds1, dupCellsInds2))
        if np.any(dupCellsInds):
            excludeDf.ix[dupCellsInds, 'duplicate_cross'] = 1
            dupCells = excludeDf.loc[dupCellsInds]
            cellToKeepIndex = np.argmax(dupCells.maxSoundRes, axis=1) 
            cellToDiscardInd = dupCellsInds[dupCellsInds!= cellToKeepInd]
            excludeDf.ix[cellToDiscardInd, 'duplicate_cross_discard'] = 1
    return excludeDf



if __name__=='__main__':
    corrThreshold = 0.9
    
    CASE = 1

    ANIMALS = ['adap013'] #['gosi004','gosi010']
    # --  -- #
    if CASE==1:
        for animal in ANIMALS:
            ## -- Load cellDB of this animal -- #
            celldbPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', '{}_database.h5'.format(animal)) 
            cellDB = pd.read_hdf(celldbPath, key='reward_change')
            print 'Finding within session duplicates for {}'.format(animal)
            excludeDfWithinSess = find_within_session_duplicates(cellDB, corrThreshold)
            cellDB = reduce(lambda left,right: pd.merge(left,right,on=['date','tetrode','cluster'],how='inner'), [cellDB, excludeDfWithinSess])
            cellDB.to_hdf(celldbPath, key='reward_change')


    if CASE == 2:
        for animal in ANIMALS:
            ## -- Load cellDB of this animal -- #
            celldbPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', '{}_database.h5'.format(animal)) 
            cellDB = pd.read_hdf(celldbPath, key='reward_change')
            print 'Finding within session duplicates for {}'.format(animal)
            excludeDfCrossSess = find_cross_session_duplicates(cellDB, corrThreshold)
            cellDB = reduce(lambda left,right: pd.merge(left,right,on=['date','tetrode','cluster'],how='inner'), [cellDB, excludeDfWithinSess])
            cellDB.to_hdf(celldbPath, key='reward_change')
