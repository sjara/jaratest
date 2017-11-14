import numpy as np
import pandas
from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
reload(spikesorting)
from matplotlib import pyplot as plt
from numpy import inf

dbFn = '/home/nick/data/database/pinp016/pinp016_database.h5'
pinp016db = pandas.read_hdf(dbFn, key='database')

allShapeQuality = np.empty(len(pinp016db))

for indCell, cell in pinp016db.iterrows():

    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']

    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    allShapeQuality[indCell] = shapeQuality

allShapeQuality[allShapeQuality==inf]=0

pinp016db['shapeQuality'] = allShapeQuality

newFn = '/home/nick/data/database/pinp016/pinp016_database_shapeQual.h5'
pinp016db.to_hdf(newFn, 'database')


# badCells = np.flatnonzero(pinp016db['isiViolations']>=0.02)
# goodCells = np.flatnonzero(pinp016db['isiViolations']<0.02)

# goodShapes = allShapeQuality[goodCells]
# badShapes = allShapeQuality[badCells]

# plt.clf()
# plt.hist(goodShapes, histtype='stepfilled', edgecolor='g', facecolor='none')
# plt.hold(1)
# plt.hist(badShapes, histtype='stepfilled', edgecolor='r', facecolor='none')
# plt.show()

# percentiles = [10, 20, 30, 40, 50, 60, 70, 80, 90]

# for indp, perc in enumerate(percentiles):
#     valThisPercentile = np.percentile(allShapeQuality, perc, interpolation='nearest')
#     indThisVal = np.where(allShapeQuality==valThisPercentile)[0][0]

#     cellThisInd = pinp016db.ix[indThisVal]

#     spikeShape = cellThisInd['clusterSpikeShape']
#     spikeShapeSD = cellThisInd['clusterSpikeSD']

#     plt.subplot(9,1,indp+1)
#     plt.hold(1)
#     plt.fill_between(range(40),spikeShape+spikeShapeSD,spikeShape-spikeShapeSD,color='0.75')
#     plt.title(valThisPercentile)
#     plt.plot(spikeShape,'.-')
#     plt.hold(0)

# plt.tight_layout()
# plt.show()


#plot some examples at different values

# plt.subplot(6,1,cluster)
# plt.hold(1)
# plt.fill_between(range(nSamples),spikeShape+spikeShapeSD,spikeShape-spikeShapeSD,color='0.75')
# plt.plot(spikeShape,'.-')
# plt.hold(0)
# plt.show()
