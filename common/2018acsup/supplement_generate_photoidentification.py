''' 
Generates inputs to plot example laser responses of PV/SOM/Exc. cells and average spike shapes

Inputs generated:
* rasters of example cell laser responses
* average normalised spike waveforms for all cells
* spike widths of all cells for sorting excitatory cells
* median Exc., PV, and SOM waveform
* laser-induced change in firing rate for each cell
'''

import os
import pandas as pd
import numpy as np
import scipy.stats

from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams
import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_photoidentification'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

PVCells = bestCells.query(studyparams.PV_CELLS)
SOMCells = bestCells.query(studyparams.SOM_CELLS)

# -- find cells unresponsive to laser (putative pyramidal, not using queries from studyparams because we want the ones with narrow spikes as well) --
ExCells = bestCells.query("laserUStat<0 or laserPVal>0.5")
ExCells = ExCells.loc[ExCells['subject'].isin(studyparams.SOM_CHR2_MICE)]

PVpeaks = PVCells['spikePeakAmplitudes']
SOMpeaks = SOMCells['spikePeakAmplitudes']
ExPeaks = ExCells['spikePeakAmplitudes']

PVnormSpikeShapes = np.stack(PVCells['spikeShape']/np.abs(PVpeaks.str[1]))
SOMnormSpikeShapes = np.stack(SOMCells['spikeShape']/np.abs(SOMpeaks.str[1]))
ExNormSpikeShapes = np.stack(ExCells['spikeShape']/np.abs(ExPeaks.str[1]))

PVmedianSpikeShape = np.median(PVnormSpikeShapes, axis=0)
SOMmedianSpikeShape = np.median(SOMnormSpikeShapes, axis=0)
ExMedianSpikeShape = np.median(ExNormSpikeShapes, axis=0)

PVspikeWidths = PVCells['spikeWidth']
SOMspikeWidths = SOMCells['spikeWidth']
ExcSpikeWidths = ExCells['spikeWidth']

SAMPLING_RATE = 30000.0
timestamps = 1.0*np.arange(PVnormSpikeShapes.shape[1])/SAMPLING_RATE #relative time of each point of waveform considering the 30kHz sampling rate

### Save bandwidth data ###    
outputFile = 'photoidentified_cells_waveforms.npz'

outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVnormSpikeShapes = PVnormSpikeShapes,
         SOMnormSpikeShapes = SOMnormSpikeShapes,
         ExcNormSpikeShapes = ExNormSpikeShapes,
         PVmedianSpikeShape = PVmedianSpikeShape,
         SOMmedianSpikeShape = SOMmedianSpikeShape,
         ExcMedianSpikeShape = ExMedianSpikeShape,
         timestamps = timestamps,
         PVspikeWidths = PVspikeWidths,
         SOMspikeWidths = SOMspikeWidths,
         ExcSpikeWidths = ExcSpikeWidths)
print outputFile + " saved"

# -- get laser-induced changes in firing rate for all cells collected from each type of mouse --

bestCellsPVmice = bestCells.loc[bestCells['subject'].isin(studyparams.PV_CHR2_MICE)]
bestCellsSOMmice = bestCells.loc[bestCells['subject'].isin(studyparams.SOM_CHR2_MICE)]

PVlaserChangeFR = bestCellsPVmice['laserChangeFR']
SOMlaserChangeFR = bestCellsSOMmice['laserChangeFR']

PVlaserPVal = bestCellsPVmice['laserPVal']
SOMlaserPVal = bestCellsSOMmice['laserPVal']

PVlaserUStat = bestCellsPVmice['laserUStat']
SOMlaserUStat = bestCellsSOMmice['laserUStat']

PVspikeWidths = bestCellsPVmice['spikeWidth']
SOMspikeWidths = bestCellsSOMmice['spikeWidth']

### Save bandwidth data ###    
outputFile = 'all_cells_laser_responses.npz'

outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         laserChangePVmice = PVlaserChangeFR,
         laserChangeSOMmice = SOMlaserChangeFR,
         laserPValPVmice = PVlaserPVal,
         laserPValSOMmice = SOMlaserPVal,
         laserUStatPVmice = PVlaserUStat,
         laserUStatSOMmice = SOMlaserUStat,
         spikeWidthPVmice = PVspikeWidths,
         spikeWidthSOMmice = SOMspikeWidths)
print outputFile + " saved"

# -- same list of cells as for figure 1 to demonstrate their laser response --
cellList =  [{'subject' : 'band016',
            'date' : '2016-12-11',
            'depth' : 950,
            'tetrode' : 6,
            'cluster' : 6}, #example AC cell
            
            {'subject' : 'band029',
            'date' : '2017-05-25',
            'depth' : 1240,
            'tetrode' : 2,
            'cluster' : 2}, #another AC cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1140,
            'tetrode' : 1,
            'cluster' : 3}, #another AC cell
            
            {'subject' : 'band044',
            'date' : '2018-01-16',
            'depth' : 975,
            'tetrode' : 7,
            'cluster' : 4}, #another AC cell
            
            {'subject' : 'band060',
            'date' : '2018-04-02',
            'depth' : 1275,
            'tetrode' : 4,
            'cluster' : 2}, #another AC cell
             
            {'subject' : 'band026',
            'date' : '2017-04-27',
            'depth' : 1350,
            'tetrode' : 4,
            'cluster' : 2}, #PV cell
            
            {'subject' : 'band026',
            'date' : '2017-04-26',
            'depth' : 1470,
            'tetrode' : 4,
            'cluster' : 5}, #PV cell
            
            {'subject' : 'band032',
            'date' : '2017-07-21',
            'depth' : 1200,
            'tetrode' : 6,
            'cluster' : 2}, #PV cell
            
            {'subject' : 'band033',
            'date' : '2017-07-27',
            'depth' : 1700,
            'tetrode' : 4,
            'cluster' : 5}, #PV cell
            
            {'subject' : 'band015',
            'date' : '2016-11-12',
            'depth' : 1000,
            'tetrode' : 8,
            'cluster' : 4}, #SOM cell
            
            {'subject' : 'band029',
            'date' : '2017-05-22',
            'depth' : 1320,
            'tetrode' : 4,
            'cluster' : 2}, #SOM cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1280,
            'tetrode' : 1,
            'cluster' : 4}, #SOM cell
            
            {'subject' : 'band060',
            'date' : '2018-04-04',
            'depth' : 1225,
            'tetrode' : 3,
            'cluster' : 4}] #SOM cell

cellTypes = ['AC', 'AC', 'AC', 'AC', 'AC', 'PV', 'PV', 'PV', 'PV', 'SOM', 'SOM', 'SOM', 'SOM']

for indCell, thisCell in enumerate(cellList):
    # -- find the cell we want based on dictionary --
    cellInd, dbRow = celldatabase.find_cell(db, **thisCell)
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    
    # --- loads spike and event data for laser pulse sessions ---
    laserEphysData, noBehav = cell.load('laserPulse')
    laserEventOnsetTimes = laserEphysData['events']['laserOn']
    laserSpikeTimestamps = laserEphysData['spikeTimes']
    timeRange = [-0.1, 0.3]
    
    laserSpikeTimesFromEventOnset, trialIndexForEachSpike, laserIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserSpikeTimestamps, laserEventOnsetTimes, timeRange)
    
    # --- loads waveform for this specific cell ---
    peaks = dbRow['spikePeakAmplitudes']
    normSpikeShape = np.array(dbRow['spikeShape']/np.abs(peaks[1]))
    
    ### Save laser data for each cell ###    
    outputFile = 'example_{}_laser_response_{}_{}_{}um_T{}_c{}.npz'.format(cellTypes[indCell],dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])

    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath,
             spikeTimesFromEventOnset = laserSpikeTimesFromEventOnset,
             indexLimitsEachTrial = laserIndexLimitsEachTrial,
             rasterTimeRange = timeRange,
             normSpikeShape = normSpikeShape)
    print outputFile + " saved"
    