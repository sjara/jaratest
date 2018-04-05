'''
Measuring Mahalanobis distance between each point and the centroid of a point cloud
'''

import numpy as np
from scipy import spatial
from matplotlib import pyplot as plt
from jaratoolbox import spikesorting
reload(spikesorting)

#distance.mahalanobis

np.random.seed(0)

nPoints = 1000
factorMat = np.array([ [2, 2], [0.2, 4] ])
#factorMat = np.array([ [2, -1], [-1, 2] ])
meanVec = np.array([ [2], [3] ])
points = np.dot(factorMat,np.random.randn(2,nPoints))  + meanVec
pointsT = points.T

dM = spikesorting.distance_to_centroid(pointsT)

# -- Plot results --
plt.clf()
plt.hold(True)
plt.plot(points[0,:], points[1,:], '.')
plt.axis('equal')
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.grid(True)

# plt.plot(pMean[0], pMean[1], '+', color=[0,1,0], mew=2, ms=10)
#plt.plot(zPoints[0,:], zPoints[1,:], 'r.')

outside = dM>2.0
plt.plot(points[0,outside], points[1,outside], '.r')

plt.show()

