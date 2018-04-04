'''
Measuring Mahalanobis distance between each point and the centroid of a point cloud
'''

import numpy as np
from scipy import spatial
from matplotlib import pyplot as plt

#distance.mahalanobis

np.random.seed(0)

nPoints = 1000
factorMat = np.array([ [2, 2], [0.2, 4] ])
#factorMat = np.array([ [2, -1], [-1, 2] ])
meanVec = np.array([ [2], [3] ])
points = np.dot(factorMat,np.random.randn(2,nPoints))  + meanVec

pMean = points.mean(axis=1)
zPoints = points-pMean[:,np.newaxis]

pCov = np.cov(zPoints)
pInvCov = np.linalg.inv(pCov)

# Mahalanobis distance to zero:  d = sqrt ( xT * invCov * x )
'''
# -- This method calculates distances between all point --
term2 = np.dot(pInvCov, zPoints)
term1 = np.dot(zPoints.T, term2)
dMahalanobis = np.sqrt(term1)
'''
# -- Calculate distance from each point to origin --
dMahalanobis = np.empty(points.shape[1])
for ind in range(nPoints):
    zPoint = zPoints[:,ind]
    term2 = np.dot(pInvCov, zPoint)
    term1 = np.dot(zPoint.T, term2)
    dMahalanobis[ind] = np.sqrt(term1)


# -- Plot results --
plt.clf()
plt.hold(True)
plt.plot(points[0,:], points[1,:], '.')
plt.axis('equal')
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.grid(True)

plt.plot(pMean[0], pMean[1], '+', color=[0,1,0], mew=2, ms=10)
#plt.plot(zPoints[0,:], zPoints[1,:], 'r.')

outside = dMahalanobis>2.0
plt.plot(points[0,outside], points[1,outside], '.r')

plt.show()


