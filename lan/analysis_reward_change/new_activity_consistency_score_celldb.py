import os
import pdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.lan.analysis_reward_change import reward_change_loader_plotter_functions as rcfuncs

#animalLists = [['adap005','adap012', 'adap013', 'adap015', 'adap017'], ['gosi001','gosi004', 'gosi008','gosi010']]
#animalLabels = ['astr', 'ac']

qualityThreshold = 2.5 #3 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05
numBins = 20
consistentZthreshold = 1.3 #This is the unit of std that a bin has to exceed to be scored as inconsistent firing rate
maxInconsistentBins = 4 #Number of bins that varied significantly from baseline to call a cell inconsistent firing
initialWinSize = 2
sd2mean=0.5
sessionToUse = 'behavior'

def score_compare_ave_firing_vs_std(cellObj, sessionToUse=sessionToUse, numBins=numBins, sd2mean=sd2mean):
    '''
    MOST RELAXED CRITERIA
    Compare the overall mean and std from all the firing rate bins, a cell is judged to be inconsistent in activity if std is over the specified fraction (sd2mean) of mean.
    '''
    sessionInd = cellObj.get_session_inds(sessionToUse)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd)
    spiketimes = ephysData['spikeTimes'] 
    consistentFiring = True
    if not np.any(spiketimes): #A cluster that has no spikes in rc ephys session
        consistentFiring = False
    else:
        spiketimes = spiketimes - spiketimes[0]
        counts, binEdges = np.histogram(spiketimes, bins=numBins) #turn spiketimes data into counts data
        countsMean = np.mean(counts)
        countsStd = np.std(counts)
        if countsStd >= sd2mean * countsMean:
            consistentFiring = False
    
    return consistentFiring 



