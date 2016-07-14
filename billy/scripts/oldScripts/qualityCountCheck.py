'''
author:Billy
Checks if there are the correct number of quality-numbers for each cluster in the quality allcells file.
'''
from jaratoolbox import settings
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    try:
        clusterQuality = oneCell.quality[cluster-1]
    except:
        print 'missing '+behavSession+' tetrode: '+str(tetrode)+' cluster: '+str(cluster)
