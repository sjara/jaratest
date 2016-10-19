'''
This script takes Billy's allcell files for mice recorded on the psychometric curve task, finds the 'sound-responsive' cells (Z score >= 3 or <= -3). 
Stores the index of the selected cells for each animal in a hdf5 file. 
Plots tuning raster for each cell thus selected.
'''

import os
import numpy as np
import pandas as pd
#from jaratoolbox import settings
#from jaratest.lan import test061_read_switching_measurement_txtfiles as reader
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as plotter


def read_sound_maxZ_file_psychometric_return_Df(maxZFilename):
    '''
    Reads txt files containing maximal Z scores of sound responses calculated by each chord frequencies presented in the 2afc task. 
    '''
    maxZFile = open(maxZFilename, 'r')
    class nestedDict(dict):#This is for maxZDict
        def __getitem__(self, item):
            try:
                return super(nestedDict, self).__getitem__(item)
            except KeyError:
                value = self[item] = type(self)()
                return value
    maxZDict = nestedDict()
    behavName = ''
    for line in maxZFile:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
        else:
            maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]
    maxZFile.close()

    maxZDf = pd.DataFrame()
    numCellsPerSession = 96
    for behavSession in maxZDict.keys():
        allFreqsSorted = sorted(maxZDict[behavSession].keys())
        maxZAllFreqs = np.zeros((numCellsPerSession,6)) #initialize ndarray for all cells and all 6 frequencies in the psychometric, some sessions may not have all 6 so those values will be zero
        for indf,freq in enumerate(allFreqsSorted):
            maxZThisFreq = maxZDict[behavSession][freq]
            maxZAllFreqs[:,indf] = maxZThisFreq
        thisSessionDf = pd.DataFrame({'session':np.tile(behavSession,numCellsPerSession),'tetrode':np.repeat(range(1,9),12),'cluster':np.tile(range(1,13),8),'maxZsound1':maxZAllFreqs[:,0],'maxZsound2':maxZAllFreqs[:,1],'maxZsound3':maxZAllFreqs[:,2],'maxZsound4':maxZAllFreqs[:,3],'maxZsound5':maxZAllFreqs[:,4],'maxZsound6':maxZAllFreqs[:,5]})
        maxZDf = maxZDf.append(thisSessionDf, ignore_index=True)

    return maxZDf
        
   
MOUNTED_EPHYS_PATH = '/home/languo/data/jarastorephys'
mouseNames = ['adap015','adap017','adap013','test053','test055'] # Names of the mice recorded on the psychometric curve task
numCellsPerSession = 96

allMouseDf = pd.DataFrame()
for mouse in mouseNames:
    processedDir = os.path.join(MOUNTED_EPHYS_PATH,mouse+'_processed') # Directory storing all computed measurements in txt files (Billy's data only)
    maxZFilename = os.path.join(processedDir,'maxZVal.txt')
    maxZDf = read_sound_maxZ_file_psychometric_return_Df(maxZFilename)
    maxZDf['animalName'] = np.tile(mouse, maxZDf.shape[0])
    allMouseDf = allMouseDf.append(maxZDf, ignore_index=True)

#allMouseDf.to_csv('/home/languo/data/behavior_reports/psychometric_tuning.csv')

allMouseDf.to_hdf('/home/languo/data/behavior_reports/all_cells_tuning_maxZ.h5',key='psychometric')
       
