'''
Count D1-expressing cells from GENSAT characterization of D1 mouse.
'''

import os
import numpy as np
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
from scipy import stats

dataDir = os.path.join(settings.HISTOLOGY_PATH,'gensat_drd1','cellcounts') #'cellcounts_sj')

mmPerUnit = 0.000735 # From scale on GENSAT images, 1mm is 1360 units on the x axis at scale factor of 1.
countWinSquareSideLenInUnit = 500
countWinSizeInMm2 = np.square(countWinSquareSideLenInUnit * mmPerUnit)
countFiles = {'AnteriorStr': ['p027a','p027b','p028a','p028b','p029a','p029b','p030a','p030b'],
              'PosteriorStr': ['p040a','p040b','p041a','p041b','p042a','p042b','p043a','p043b']}
cellCounts = {'AnteriorStr': [],
              'PosteriorStr': []}
cellCountsPerMm2 = {'AnteriorStr': [],
                    'PosteriorStr': []}
meanCount = {'AnteriorStr': 0, 'PosteriorStr': 0}
stdCount = {'AnteriorStr': 0, 'PosteriorStr': 0}
meanCountPerMm2 = {'AnteriorStr': 0, 'PosteriorStr': 0}
stdCountPerMm2 = {'AnteriorStr': 0, 'PosteriorStr': 0}

for brainArea,sections in countFiles.iteritems():
    for oneSection in sections:
        filenameCSV = os.path.join(dataDir,oneSection)+'.csv'
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=1)
        nCells = coords.shape[1]
        nCellsPerMm2 = nCells / countWinSizeInMm2
        cellCounts[brainArea].append(nCells)
        cellCountsPerMm2[brainArea].append(nCellsPerMm2)
        print('{} {}: {}'.format(brainArea, oneSection, nCells)) ### DEBUG
    meanCount[brainArea] = np.mean(cellCounts[brainArea])
    stdCount[brainArea] = np.std(cellCounts[brainArea])
    meanCountPerMm2[brainArea] = np.mean(cellCountsPerMm2[brainArea])
    stdCountPerMm2[brainArea] = np.std(cellCountsPerMm2[brainArea])
    print('Average count per square millimeter ({}) = {} +/- {}'.format(brainArea,
                                                  meanCountPerMm2[brainArea],
                                                  stdCountPerMm2[brainArea]))

# -- Stats -- #
Z, pVal = stats.ranksums(cellCountsPerMm2.values()[0], cellCountsPerMm2.values()[1])
print('Using Wilcoxon rank-sum test comparing the mean counts per square millimeter between brain regions, p value is {:.3f}'.format(pVal))
#print cellCounts
#print meanCount
