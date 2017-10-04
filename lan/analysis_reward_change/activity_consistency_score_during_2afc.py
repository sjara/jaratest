import os
import pdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.lan.analysis_reward_change import reward_change_loader_plotter_functions as rcfuncs

animalLists = [['adap005','adap012', 'adap013', 'adap015', 'adap017'], ['gosi001','gosi004', 'gosi008','gosi010']]
animalLabels = ['astr', 'ac']

qualityThreshold = 2.5 #3 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05
numBins = 20
consistentZthreshold = 1.3 #This is the unit of std that a bin has to exceed to be scored as inconsistent firing rate
maxInconsistentBins = 4 #Number of bins that varied significantly from baseline to call a cell inconsistent firing
initialWinSize = 2
sd2mean=0.5

def score_compare_ave_std(timestamps, numBins, sd2mean=0.5):
    '''
    MOST RELAXED CRITERIA
    Compare the overall mean and std from all the firing rate bins, a cell is judged to be inconsistent in activity if std is over the specified fraction (sd2mean) of mean.
    '''
    consistentFiring = True
    counts, binEdges = np.histogram(timestamps, bins=numBins) #turn timestamps data into counts data
    countsMean = np.mean(counts)
    countsStd = np.std(counts)
    if countsStd >= sd2mean * countsMean:
        consistentFiring = False
    '''    
    #Ploting code used for testing.
    plt.figure()
    label = '{}'.format(consistentFiring)
    plt.bar(range(numBins), counts, label=label)
    plt.axhline(countsMean, color='red')
    plt.axhline(countsMean + countsStd)
    plt.axhline(countsMean - countsStd)
    plt.text(0.5*numBins,0.5*counts[0], label)
    plt.show()
    '''
    return consistentFiring 

def score_overall_ave_std(timestamps, numBins, consistentZthreshold=1.5, maxInconsistentBins=4):
    '''
    Use the overall average and std of all the bins to determine if a bin crosses detection threshold as being inconsistent with overall firing rate patterns.
    '''
    consistentFiring = True
    #nbins = int(np.ceil(timestamps[-1] / binSize)) #divide whole time period into bins of 10min length
    nbins = numBins
    counts, binEdges = np.histogram(timestamps, bins=nbins) #turn timestamps data into counts data
    countsMean = np.mean(counts)
    countsStd = np.std(counts)
    higherFiring =  (np.array(counts) > countsMean + consistentZthreshold*countsStd)
    lowerFiring = (np.array(counts) < countsMean - consistentZthreshold*countsStd)
    inconsistencyEachBin = np.logical_or(higherFiring, lowerFiring)
    print counts, countsMean, countsStd, higherFiring, lowerFiring, inconsistencyEachBin
    inconsistentBins = np.sum(inconsistencyEachBin)
    if inconsistentBins >= maxInconsistentBins:
        consistentFiring = False
    '''    
    #Ploting code used for testing.
    plt.figure()
    label = '{}_{}'.format(inconsistentBins,consistentFiring)
    plt.bar(range(nbins), counts, label=label)
    plt.axhline(countsMean + consistentZthreshold*countsStd)
    plt.axhline(countsMean - consistentZthreshold*countsStd)
    plt.text(0.5*nbins,0.5*counts[0], label)
    plt.show()
    '''
    return consistentFiring

    
def score_running_ave_std(timestamps, numBins, initialWinSize=2, consistentZthreshold=3, maxInconsistentBins=4):
    '''
    Use a running calculation of average and std to determine if a bin crosses detection threshold as being inconsistent with previous firing rate patterns.
    '''
    #nbins = int(np.ceil(timestamps[-1] / binSize)) #divide whole time period into bins of 10min length
    nbins = numBins
    counts, binEdges = np.histogram(timestamps, bins=nbins) #turn timestamps data into counts data
    #pdb.set_trace()
    #initialWinSize = 2
    baselineMean = np.mean(counts[:initialWinSize])
    baselineStd = np.std(counts[:initialWinSize])
    print counts, baselineMean, baselineStd
    consistentFiring = True
    inconsistentCounts = 0
    filteredCounts = counts.copy()
    for indb, count in enumerate(counts[initialWinSize:]):
        if (counts[indb+initialWinSize] > baselineMean + consistentZthreshold*baselineStd) or (counts[indb+initialWinSize] < baselineMean - consistentZthreshold*baselineStd):
            print '{} is inconsistent with baseline'.format(counts[indb+initialWinSize])
            inconsistentCounts += 1
            # Filter annd update baselineMean&Std in such a way that this inconsistent bin will not contribute to change that
            filteredCounts[indb+initialWinSize] = baselineMean
            baselineMean = np.mean(filteredCounts[:indb+initialWinSize+1])
            baselineStd = np.std(filteredCounts[:indb+initialWinSize+1])
        else:
            baselineMean = np.mean(filteredCounts[:indb+initialWinSize+1])
            baselineStd = np.std(filteredCounts[:indb+initialWinSize+1])
    if inconsistentCounts >= maxInconsistentBins:
        consistentFiring = False
    '''    
    #Ploting code used for testing.
    plt.figure()
    label = '{}_{}'.format(inconsistentCounts,consistentFiring)
    plt.bar(range(nbins), counts, label=label)
    plt.text(0.5*nbins,0.5*counts[0], label)
    plt.show()
    '''
    return consistentFiring

if __name__ == '__main__':
    for indRegion, (label,animalList) in enumerate(zip(animalLabels, animalLists)):
        celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
        celldb = pd.read_hdf(celldbPath, key='reward_change')
        celldb = celldb.reset_index()
        goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))
        #goodQualCells = goodQualCells[-25:]
        consistencyArray = np.zeros(len(celldb), dtype=bool)
        for ind, cell in goodQualCells.iterrows():
            indc = cell.name
            animal = cell['animalName']
            date = cell['date']
            tetrode = int(cell['tetrode'])
            cluster = int(cell['cluster'])
            rcInd = cell['sessiontype'].index('behavior')
            rcEphysThisCell = cell['ephys'][rcInd]
            #rcBehavThisCell = cell['behavior'][rcInd]

            spikeData = rcfuncs.load_spike_data(animal, rcEphysThisCell, tetrode, cluster)
            timestamps = spikeData.timestamps
            timestamps = timestamps - timestamps[0] #timestamps unit is seconds
            
            #consistentFiring = score_overall_ave_std(timestamps, numBins, consistentZthreshold, maxInconsistentBins)
            #consistentFiring = score_running_ave_std(timestamps, numBins, initialWinSize, consistentZthreshold, maxInconsistentBins)
            consistentFiring = score_compare_ave_std(timestamps, numBins, sd2mean)
            consistencyArray[indc] = consistentFiring
            #pdb.set_trace()

            #raw_input('Press Enter')
        celldb['consistentInFiring'] = consistencyArray
        celldb.to_hdf(celldbPath, key='reward_change')
