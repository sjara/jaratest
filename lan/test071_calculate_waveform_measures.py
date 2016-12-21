'''
Script that uses spikesorting.estimate_spike_peaks to calculate peak amplitude and time for capacitant, sodium, and potasium peaks for each cell respectively. 
Iterates through an animal's allcells files, only calculate waveform for good quality cells at this point.

Lan Guo 20161123
'''
import sys
import importlib
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
CASE = 2
# -- Choose to which experiments to analyze and store results separately -- #
if CASE == 1:
    # Analyze psychometric curve cells
    #animalList = ['adap013','adap017','adap015','test053','test055']
    animalList = ['test055']
    nameOfFile = 'psychometric'

elif CASE == 2:
    # Analyze switching cells
    animalList = ['test059','test017','test089','adap020'] 
    nameOfFile = 'switching'

##################################################################################
all_waveform_measures = pd.DataFrame()

for animal in animalList:
    allcellsFileName = 'allcells_'+animal+'_quality'
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    cellsThisAnimal = allcells.cellDB

    waveformData = pd.DataFrame(index=range(0,len(cellsThisAnimal)), columns=['animalName','behavSession','tetrode','cluster','peakCapAmp','peakNaAmp','peakKAmp','peakCapTime','peakNaTime','peakKTime'])

    for index,oneCell in enumerate(cellsThisAnimal):
        print oneCell.tetrode, oneCell.cluster
        cellQuality = oneCell.quality[oneCell.cluster-1] # This is specific to Billy's allcells_animal_quality files!!

        if cellQuality!=1 and cellQuality!=6:
            # Only calculate waveform measures for good quality cells
            waveformDataThis=[oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,0,0,0,0,0,0]

        else:
            # These files are on jarastore so have to use custom loader
            spkData = loader.load_remote_2afc_spikes(oneCell)
            waveforms = spkData.samples #loader has already applied the subtraction and division by gain
            #waveforms = spkData.spikes.samples.astype(float) - 2**15 # FIXME: this is specific to OpenEphys
            # FIXME: This assumes the gain is the same for all channels and records
            #waveforms = (1000.0/spkData.spikes.gain[0,0]) * waveforms #this converts waveforms's unit to uV
            samplingRate = spkData.samplingRate

            (peakTimes, peakAmplitudes, avWaveform) = spikesorting.estimate_spike_peaks(waveforms,samplingRate)
            peakCapAmp,peakNaAmp,peakKAmp=peakAmplitudes
            peakCapTime,peakNaTime,peakKTime=peakTimes
            waveformDataThis=[oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,peakCapAmp,peakNaAmp,peakKAmp,peakCapTime,peakNaTime,peakKTime]
        waveformData.ix[index,:]=waveformDataThis
    waveformData.sort(['behavSession','tetrode','cluster'],ascending=True,inplace=True)
    #all_waveform_measures=pd.concat((all_waveform_measures,waveformData), ignore_index=True)
    waveformData.to_hdf('/home/languo/data/ephys/{0}_summary_stats/{1}_{2}_waveforms.h5'.format(nameOfFile,animal,nameOfFile),key=animal+'_'+nameOfFile)


#all_waveform_measures.to_hdf('/home/languo/data/ephys/{0}_summary_stats/{1}_waveforms.h5'.format(nameOfFile,nameOfFile),key=nameOfFile)
