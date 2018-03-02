import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import settings
import sklearn.metrics

STUDY_NAME = '2017rc'

#FIGNAME = 'reward_modulation_movement_selective_cells'
FIGNAME = 'roc_auc_overtime'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)
dataDir = os.path.join('/tmp/', STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

# -- These example cells I picked manually  --#
cellParamsList = []

exampleCell = {'subject':'adap012',
              'date':'2016-02-04',
              'tetrode':3,
               'cluster':3,
               'brainRegion':'astr',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-03-09',
              'tetrode':3,
               'cluster':2,
               'brainRegion':'astr',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-03-24',
              'tetrode':6,
               'cluster':6,
               'brainRegion':'astr',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-28',
              'tetrode':4,
               'cluster':5,
               'brainRegion':'astr',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-28',
              'tetrode':8,
               'cluster':8,
               'brainRegion':'astr',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-30',
              'tetrode':1,
               'cluster':3,
               'brainRegion':'astr',
               'freqsToPlot':'low'} # low freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi001',
              'date':'2017-05-06',
              'tetrode':3,
               'cluster':5,
               'brainRegion':'ac',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-02-13',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac',
               'freqsToPlot':'low'} # low freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-15',
              'tetrode':6,
               'cluster':7,
               'brainRegion':'ac',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-18',
              'tetrode':3,
               'cluster':4,
               'brainRegion':'ac',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-04-06',
              'tetrode':7,
               'cluster':5,
               'brainRegion':'ac',
               'freqsToPlot':'high'
               }
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-14',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac',
               'freqsToPlot':'high'} # high freq
cellParamsList.append(exampleCell)

# -- Select an example cell or generate all cells based on sys argv -- #
if len(sys.argv) == 1:
    cellParamsList = cellParamsList
    print 'Plotting roc auc over time for all cells'
elif len( sys.argv) == 2:
    cellIndToPlot = int(sys.argv[1])
    cellParamsList = [cellParamsList[cellIndToPlot]]

#freqsToPlot = ['low', 'high']
alignment = 'center-out' #'side-in' 

#plt.figure()

for cellParams in cellParamsList:
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    freq = cellParams['freqsToPlot']
    
    aucFile = 'binned_auc_roc_{}aligned_{}freq_{}_{}_T{}_c{}.npz'.format(alignment, freq, animal, date, tetrode, cluster)
    aucFullPath = os.path.join(dataDir, aucFile)
    aucOverTime = np.load(aucFullPath)
    slidingWinEdges = aucOverTime['slidingWinEdges']
    aucEachSlidingWin = aucOverTime['aucEachSlidingWin']
    ci = aucOverTime['auc95ConfidenceInterval']
    aucMax = aucEachSlidingWin.max()
    maxInd = aucEachSlidingWin.argmax()
    aucMaxTimeWin = slidingWinEdges[maxInd, :]
    ciThisWin = [ci[:, maxInd].min(axis=0), ci[:, maxInd].max(axis=0)]

    print 'For {}freq_{}_{}_T{}_c{}, maximum auc is {:.3f} at time period {}, the 95% confidence interval is {}'.format(freq, animal, date, tetrode, cluster, aucMax, aucMaxTimeWin, ciThisWin)

