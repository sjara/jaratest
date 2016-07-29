'''
Estimate spike shape. Calculates the times and magnitudes of the capacitive peak, sodium peak, and potasium peak respectively. 
20160518 Have moved this to wrtie_all_cells_records.
'''

from pylab import *
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import spikesorting
#from scipy.interpolate import interp1d
#import sys
import pandas as pd
import matplotlib.gridspec as gridspec
import importlib
import os

subject = sys.argv[1]
allcellsFileName = 'allcells_'+subject
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
outputDir = '/home/languo/data/ephys/'+subject+'/'
processedDir = os.path.join(outputDir,subject+'_stats')

# -- Load spike data --

#import allcells_adap012_copy as allcells
#cellID = allcells.cellDB.findcell('adap012','20160209a',6,10,quality=6)

#allMeasuresGoodCells=pd.read_csv(processedDir +'/all_measures_goodISI_'+subject+'.csv') #checked ISI first
allMeasuresGoodCells=pd.read_csv(processedDir +'/all_measures_'+subject+'.csv') #without checking ISI 

#goodCellIDs=allMeasuresGoodCells['X']  #only calculates waveform parameters for ISI-checked cells
goodCellIDs=range(0,len(allcells.cellDB))  #calculate waveform parameters for all cells

waveformData = pd.DataFrame(index=range(0,len(goodCellIDs)), columns=['peakCapAmp','peakNaAmp','peakKAmp','peakCapTime','peakNaTime','peakKTime','widthWaveform'])
#gs=gridspec.GridSpec(10,1)
#widthWaveform,peakCapTime,peakNaTime,peakKTime,peakCapAmp,peakNaAmp,peakKAmp=[],[],[],[],[],[],[]

for index,goodCell in enumerate(goodCellIDs):
    oneCell = allcells.cellDB[goodCell]
    if oneCell.quality!=1 and oneCell.quality!=6:
        waveformDataThis=[0,0,0,0,0,0,0]
    else:
        spkData = ephyscore.CellData(oneCell)
        #waveforms = spkData.spikes.samples
        waveforms = spkData.spikes.samples.astype(float) - 2**15 # FIXME: this is specific to OpenEphys
        # FIXME: This assumes the gain is the same for all channels and records
        waveforms = (1000.0/spkData.spikes.gain[0,0]) * waveforms #this converts waveforms's unit to uV
        samplingRate = spkData.spikes.samplingRate

        (peakTimes, peakAmplitudes, avWaveform) = spikesorting.estimate_spike_peaks(waveforms,samplingRate)
        peakCapAmp,peakNaAmp,peakKAmp=peakAmplitudes
        peakCapTime,peakNaTime,peakKTime=peakTimes
        widthWaveform=peakKTime-peakCapTime
        waveformDataThis=[peakCapAmp,peakNaAmp,peakKAmp,peakCapTime,peakNaTime,peakKTime,widthWaveform]
    waveformData.ix[index,:]=waveformDataThis

    #timeVec = np.arange(0,len(avWaveform)/samplingRate,1/samplingRate) #unit is sec
    #ax=subplot(gs[index])
    
    #hold(1)
    #ax.plot(timeVec,avWaveform,'.-')
    #plot(interpSampVals,interpSpikeShape,'g-')
    #ax.axvline(peakTimes[1],ls='--',color='r')
    #ax.axvline(peakTimes[0],ls='--',color='0.75')
    #ax.axvline(peakTimes[2],ls='--',color='0.75')
    #hold(0)

#show()

allMeasuresGoodCells=pd.concat((allMeasuresGoodCells,waveformData), axis=1)
#allMeasuresGoodCells.to_csv(path_or_buf=(processedDir +'/all_measures_goodISI_'+subject+'.csv')) #Did ISI check first
allMeasuresGoodCells.to_csv(path_or_buf=(processedDir +'/all_measures_'+subject+'.csv'))#without checking ISI
