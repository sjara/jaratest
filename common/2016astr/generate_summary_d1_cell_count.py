'''
Count D1-expressing cells from GENSAT characterization of D1 mouse.
'''

import os
import numpy as np
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings


dataDir = os.path.join(settings.HISTOLOGY_PATH,'gensat_drd1','cellcounts_sj')

countFiles = {'AnteriorStr': ['p027a','p027b'],
              'PosteriorStr': ['p043a','p043b']}
cellCounts = {'AnteriorStr': [],
              'PosteriorStr': []}
meanCount = {'AnteriorStr': 0, 'PosteriorStr': 0}
stdCount = {'AnteriorStr': 0, 'PosteriorStr': 0}

for brainArea,sections in countFiles.iteritems():
    for oneSection in sections:
        filenameCSV = os.path.join(dataDir,oneSection)+'.csv'
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=1)
        nCells = coords.shape[1]
        cellCounts[brainArea].append(nCells)
        print('{} {}: {}'.format(brainArea, oneSection, nCells)) ### DEBUG
    meanCount[brainArea] = np.mean(cellCounts[brainArea])
    stdCount[brainArea] = np.std(cellCounts[brainArea])
    print('Average count ({}) = {} +/- {}'.format(brainArea,
                                                  meanCount[brainArea],
                                                  stdCount[brainArea]))

#print cellCounts
#print meanCount
