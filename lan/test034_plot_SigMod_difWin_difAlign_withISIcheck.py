'''
Plot recorded activity during behavior for different frequencies(leftward or rightward) in different blocks.
Lan Guo 20160404
'''
from jaratoolbox import settings_2 as settings
import os
import numpy as np
from jaratoolbox import extraplots
#from jaratoolbox import celldatabase
from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
from jaratoolbox.test.lan import test022_plot2afc_given_cell_rew_change as cellplotter
reload(cellplotter)
import matplotlib.pyplot as plt
import sys
import importlib

alignment = sys.argv[1] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
if sys.argv[2]=='0':
    countTimeRange = [int(sys.argv[2]),float(sys.argv[3])]
elif sys.argv[3]=='0':
    countTimeRange = [float(sys.argv[2]),int(sys.argv[3])]
else:
    countTimeRange = [float(sys.argv[2]),float(sys.argv[3])]
#second and third argument are numbers specify the start and end of countTimeRange in seconds, e.g. 0 0.1
subjectList = sys.argv[4:] #the fourth argument onwards are the mouse names to tell the script which allcells file to use

window= str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'


for subject in subjectList:
    allcellsFileName = 'allcells_'+subject
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
    print numOfCells
    fullOutputDir = '/home/languo/data/ephys/'+subject+'/'+subject+'_stats'

    if subject=='adap015' or subject=='adap013' or subject=='adap017':
        experimenter = 'billy'
    else:
        experimenter = 'lan'

    allCellDB = allcells.cellDB
    modulatedCellDB = celldatabase.CellDatabase()

    sigModFilename = 'sigMod_'+alignment+'_'+window+'ISIchecked'
    #try:
    sigModI_file = open('%s/%s.txt' %(fullOutputDir,sigModFilename), 'r')
    for line in sigModI_file:
        cellID=int(line.split(':')[1].split()[0])
        modulatedCellDB.append(allCellDB[cellID])
    sigModI_file.close()
    #except:
        #print sigModFilename+' does not exist.'
        #continue

    numOfModulatedCells = len(modulatedCellDB)
    print numOfModulatedCells

    #######Plot ephys plots for each modulated cell and store in new folder########
    for cellID in range(0,numOfModulatedCells):
        oneCell = modulatedCellDB[cellID]
        #####make new folder######
        dstDir = fullOutputDir+'/'+alignment+'_'+window+'_ISIchecked_modulated/'
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)

        figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,window)
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment)
            plt.savefig(full_fig_path, format = 'png')

        figname='{0}_{1}_TT{2}_c{3}_{4}_{5}_{6}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,window,'right')
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment,choiceSide='right')
            plt.savefig(full_fig_path, format = 'png')

        figname='{0}_{1}_TT{2}_c{3}_{4}_{5}_{6}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,window,'left')
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment,choiceSide='left')
            plt.savefig(full_fig_path, format = 'png')

