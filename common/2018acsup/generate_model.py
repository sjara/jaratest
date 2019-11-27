"""
Simulate model with many parameters.
"""

import os
import numpy as np
from jaratoolbox import settings
import studyparams
import figparams
import model_suppression as suppmodel
reload(suppmodel)

figName = 'figure_model'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)

# -- Simulate model --
nCells = 101

RANDOMIZED = 1
np.random.seed(1)

def random_in_range(low,high,shape):
    """Return equally distributed random numbers in specified range"""
    width = high-low
    randVec = width*np.random.rand(shape) + low
    return randVec

if RANDOMIZED:
    nSamples = 200
    rfWidths = {'PV':5, 'SOM':5, 'Thal':5}
    ampPVvec = random_in_range(-2, -44, nSamples)
    ampSOMvec = random_in_range(-2, -44, nSamples)
    stdThalvec = random_in_range(5, 10, nSamples)
    suppIndexVec = np.empty((3,nSamples))     # 3:Control, PV, SOM
    changeAtPeakVec = np.empty((2,nSamples))  # 2:PV-Control, SOM-Control
    changeAtWNVec = np.empty((2,nSamples))    # 2:PV-Control, SOM-Control

    for inds in range(nSamples):
        wParams = {'ampPV':ampPVvec[inds], 'stdPV':10,
                   'ampSOM':ampSOMvec[inds], 'stdSOM':30,
                   'ampThal':100, 'stdThal':stdThalvec[inds]}
        net = suppmodel.Network(nCells, wParams, rfWidths)
        centerCellOutput,  bandwidths, condLabels = net.simulate_inactivation()
        suppIndex = suppmodel.suppression_index(centerCellOutput)
        changeAtPeak, changeAtWN = suppmodel.change_in_response(centerCellOutput)
        suppIndexVec[:,inds] = suppIndex
        changeAtPeakVec[:,inds] = changeAtPeak
        changeAtWNVec[:,inds] = changeAtWN
else:
    ampPVvec = np.arange(-2,-44, -4)  # -20
    ampSOMvec = np.arange(-2,-44, -4) # -20
    stdThalvec = [5,7,9]#np.arange(3, 15, 2)  # 6

    suppIndexAll = np.empty((3,len(ampPVvec),len(ampSOMvec),len(stdThalvec)))     # 3:Control, PV, SOM
    changeAtPeakAll = np.empty((2,len(ampPVvec),len(ampSOMvec),len(stdThalvec)))  # 2:PV-Control, SOM-Control
    changeAtWNAll = np.empty((2,len(ampPVvec),len(ampSOMvec),len(stdThalvec)))    # 2:PV-Control, SOM-Control

    for indPV,ampPV in enumerate(ampPVvec):
        for indSOM,ampSOM in enumerate(ampSOMvec):
            for indThal,stdThal in enumerate(stdThalvec):
                wParams = {'ampPV':ampPV, 'stdPV':10,
                           'ampSOM':ampSOM, 'stdSOM':30,
                           'ampThal':100, 'stdThal':stdThal}
                net = suppmodel.Network(nCells, wParams)
                centerCellOutput,  bandwidths, condLabels = net.simulate_inactivation()
                suppIndex = suppmodel.suppression_index(centerCellOutput)
                changeAtPeak, changeAtWN = suppmodel.change_in_response(centerCellOutput)
                suppIndexAll[:,indPV,indSOM,indThal] = suppIndex
                changeAtPeakAll[:,indPV,indSOM,indThal] = changeAtPeak
                changeAtWNAll[:,indPV,indSOM,indThal] = changeAtWN
    nConds = len(ampPVvec)*len(ampSOMvec)*len(stdThalvec)     
    suppIndexVec = suppIndexAll.reshape([3,nConds])
    changeAtPeakVec = changeAtPeakAll.reshape([2,nConds])
    changeAtWNVec = changeAtWNAll.reshape([2,nConds])

      
import matplotlib.pyplot as plt

plt.clf()

markerSize = 3

# -- Plot supp index --
plt.subplot(2,2,1)
plt.plot(suppIndexVec[0],suppIndexVec[1],'sb', mfc='none', ms=markerSize)
plt.plot(suppIndexVec[0],suppIndexVec[2],'or', mfc='none', ms=markerSize)
xLims = [-0.1,1.1]
plt.xlim(xLims)
plt.ylim(xLims)
plt.plot(xLims,xLims,'--',color='0.5')
plt.xlabel('Suppression Index (control)')
plt.ylabel('Suppression Index (inactivation)')
plt.axis('square')

plt.subplot(2,2,2)
avgSIchangePV = np.median(suppIndexVec[1]-suppIndexVec[0])
avgSIchangeSOM = np.median(suppIndexVec[2]-suppIndexVec[0])
plt.bar(1,avgSIchangePV, fc='w', ec='b', lw=2)
plt.bar(2,avgSIchangeSOM, fc='w', ec='r', lw=2)


# -- Plot change in response --
plt.subplot(2,2,3)
plt.plot(changeAtPeakVec[0,:],changeAtWNVec[0,:],'sb', mfc='none', ms=markerSize)
plt.plot(changeAtPeakVec[1,:],changeAtWNVec[1,:],'or', mfc='none', ms=markerSize)
xLims = [-50,1500]
plt.xlim(xLims)
plt.ylim(xLims)
plt.plot(xLims,xLims,'--',color='0.5')
plt.xlabel('Change in response to preferred bandwidth')
plt.ylabel('Change in response to WN')
plt.axis('square')

plt.subplot(2,2,2)


# -- Save data --
outputFile = 'response_change_summary.npz'
outputFullPath = os.path.join(dataDir,outputFile)

np.savez(outputFullPath, suppIndexVec=suppIndexVec,
         changeAtPeakVec=changeAtPeakVec, changeAtWNVec=changeAtWNVec,
         condLabels=condLabels)
print("Saved {}".format(outputFullPath))
