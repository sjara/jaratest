import sys
import numpy as np
from jaratoolbox import spikesorting
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratest.lan.Ephys import celldatabase_quality_vlan as cellDB

def load_one_cell_waveform(oneCell):
    '''
    This function takes a cell of the class CellInfo (from jaratoolbox.celldatabase) and gets the waveform data for that cell.
    '''
    ephysData=ephyscore.CellData(oneCell) #ephyscore's CellData object uses loadopenephys.DataSpikes method, gets back a DataSpikes object that is stored in CellData.spikes, with fields: nSpikes, samples, timestamps(ephyscore already divides this by sampling rate),gain,samplingRate.
    spikeData=ephysData.spikes #so this is the DataSpikes object from loadopenephys
    waveforms = spikeData.samples.astype(float)-2**15 #This is specific to open Ephys
    waveforms = (1000.0/spikeData.gain[0,0]) * waveforms #converting to microvolt,specific to open Ephys
        
    return waveforms

def calculate_ave_waveform(waveforms):
    alignedWaveforms = spikesorting.align_waveforms(waveforms)
    meanWaveforms = np.mean(alignedWaveforms,axis=0)
    return meanWaveforms

        

if __name__ == '__main__':
            
    ### Loading allcells file for a specified mouse ###
    mouseName = 'adap017'
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    ## On Billy's and Lan's computer, path to allcells file looks like this:  ALLCELLS_PATH = '/home/languo/src/jaratoolbox/test/lan/Allcells' ##
    allcells = importlib.import_module(allcellsFileName)

    checkQuality = True #decide whether to just get waveform for 'good quality' cells
    goodClusterQuality = [1,6] #cluster quality that are considered 'good cell'

    for cell in allcells.cellDB:
    ## each 'cell' is a CellInfo object
        clusterQuality=cell.quality
        ## If decide just to look at the 'good quality' cells, check cluster quality and filter out those with bad quality
        if checkQuality and clusterQuality not in goodClusterQuality:
            continue
        
        waveformsThisCell = load_one_cell_waveform(cell)
        
        aveWaveformThisCell = calculate_ave_waveform(waveformsThisCell)

