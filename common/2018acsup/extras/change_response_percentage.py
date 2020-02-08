import os
import numpy as np
from scipy import stats

from jaratoolbox import settings

STUDY_NAME = '2018acsup'
FIGNAME = 'figure_inhibitory_cell_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

summaryFileName = 'all_inactivated_cells_stats.npz'

summaryDataFullPath = os.path.join(dataDir,summaryFileName)
summaryData = np.load(summaryDataFullPath)

PVsustainedSuppressionNoLaser = summaryData['fitPVsustainedSuppressionNoZeroNoLaser']
PVsustainedSuppressionLaser = summaryData['fitPVsustainedSuppressionNoZeroLaser']

SOMsustainedSuppressionNoLaser = summaryData['fitSOMsustainedSuppressionNoZeroNoLaser']
SOMsustainedSuppressionLaser = summaryData['fitSOMsustainedSuppressionNoZeroLaser']

noPVsupDiff = PVsustainedSuppressionLaser-PVsustainedSuppressionNoLaser
noSOMsupDiff = SOMsustainedSuppressionLaser-SOMsustainedSuppressionNoLaser

nonZeroSOM = np.nonzero(SOMsustainedSuppressionNoLaser)

allSOMpercentChange = noSOMsupDiff[nonZeroSOM]/SOMsustainedSuppressionNoLaser[nonZeroSOM]

SOMranks = stats.rankdata(SOMsustainedSuppressionNoLaser)

topquart = stats.rankdata(SOMsustainedSuppressionNoLaser)>41

supNoLaser = SOMsustainedSuppressionNoLaser[topquart]
supLaser = SOMsustainedSuppressionLaser[topquart]
SOMchangeTopQuart = supLaser-supNoLaser

topQuartSOMpercentChange = SOMchangeTopQuart/supNoLaser