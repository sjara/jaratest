import sys
import importlib
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader

cellParams = {'mouseName':'test059',
              'behavSession':'20150624a',
              'tetrode':1,
              'cluster':4}

mouseName = cellParams['mouseName']
    
allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

### Using cellDB methode to find the index of this cell in the cellDB ###
cellIndex = allcells.cellDB.findcell(**cellParams)


(eventOnsetTimes, spikeTimestamps, bData) = loader.load_remote_tuning_data(thisCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)

# -- Calculate data for tuning raster -- #
freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']
possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)
if len(possibleIntensity) != 1:
    intensity = 50dB #This is the stimulus intensity used in 2afc task
    ###Just select the trials with a given intensity###
    trialsThisIntensity = [intensityEachTrial==intensity]
    freqEachTrial = freqEachTrial[trialsThisIntensity]
    #intensityEachTrial = intensityEachTrial[trialsThisIntensity]
    eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

    
outputDir = '/home/languo/data/mnt/figures_papers'
outputFile = 'example_freq_tuning_raster.npz'
np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=eventOnsetTimes,
    freqEachTrial=freqEachTrial)

# -- Calculate data for tuning raster -- #
