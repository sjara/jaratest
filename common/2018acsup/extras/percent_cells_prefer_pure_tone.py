import os
import numpy as np

from jaratoolbox import settings

FIGNAME = 'figure_characterisation_of_responses_by_cell_type'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', FIGNAME)
summaryFileName = 'all_photoidentified_cells_stats.npz'
summaryDataFullPath = os.path.join(dataDir,summaryFileName)
summaryData = np.load(summaryDataFullPath)

PVBW = summaryData['rawPVsustainedPrefBW']
SOMBW = summaryData['rawSOMsustainedPrefBW']
ExcBW = summaryData['rawExcSustainedPrefBW']

propPV = 1.0*np.sum(PVBW==0)/len(PVBW)
propSOM = 1.0*np.sum(SOMBW==0)/len(SOMBW)
propExc = 1.0*np.sum(ExcBW==0)/len(ExcBW)

print('Proportions of cells most responsive to pure tone\n PV:{0}\n SOM:{1}\n Exc:{2}'.format(propPV, propSOM, propExc))