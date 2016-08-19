
'''
Example of using spikesorting module (which uses KlustaKwik) for spike sorting
'''

from jaratoolbox import spikesorting
import numpy as np
import allcells_test017 as allcells





animalName = 'test017'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

ephysSessionEachCell = []
for cellID in range(0,numOfCells):
    ephysSessionEachCell.append(allcells.cellDB[cellID].ephysSession)

ephysSessionArray = np.unique(ephysSessionEachCell)

for indEphys,ephysSession in enumerate(ephysSessionArray):
    for tetrode in range(1,9):
        oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode)
        oneTT.create_fet_files()
        oneTT.run_clustering()
        oneTT.save_report()
