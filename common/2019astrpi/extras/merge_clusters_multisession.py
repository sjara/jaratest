"""
Merge clusters for all sessions associated with a pair of clusters.

The cells we looked at to merge were 
739 (d1pi036, 2019-05-29, 2900.0um, T6c4) and
740 (d1pi036, 2019-05-29, 2900.0um, T6c5)
"""

from jaratoolbox import celldatabase
from jaratoolbox import spikesorting

# -- Clusters to merge --
subject = 'd1pi036'
sessionDate = '2019-05-29'
depth = 2900
tetrode = 6
clustersToMerge = [4,5]

# databaseFile = '/data/figuresdata/2019astrpi/astrpi_all_cells_tuning_20200304.h5'
databaseFile = 'C:\\Users\\devin\\data\\figuresdata\\2019astrpi\\astrpi_all_cells.h5'
#databaseFile = '/data/figuresdata/2019astrpi/tempdb_subset_good.h5'

# Loads database for plotting
print('Loading database...', flush=True)
columnsToLoad = ['index', 'subject', 'date', 'depth', 'tetrode', 'cluster', 'ephysTime', 'sessionType']
cellDB = celldatabase.load_hdf(databaseFile, columns=columnsToLoad)
print('Done loading')

indRow, dbRow = celldatabase.find_cell(cellDB, subject, sessionDate, depth, tetrode, clustersToMerge[0])

# for inds, oneSessionTime in enumerate(dbRow['ephysTime']):
#     ephysSession = f'{sessionDate}_{oneSessionTime}'
#     sessionType = dbRow['sessionType'][inds]
#     print(f'Processing: {ephysSession} ({sessionType})')
#     spikesorting.merge_kk_clusters(subject, ephysSession, tetrode, clustersToMerge, reportDir='/tmp/')


