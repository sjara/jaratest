"""
Toy model to replicate signal detection behavior during inactivation of SOM and PV interneurons by copy-pasting
the model we used to simulate surround suppression.
"""

import numpy as np
from matplotlib import pyplot as plt


def make_weights_mat(wVec):
    nCells = len(wVec)
    wMat = np.empty((nCells, nCells))
    for ind in range(nCells):
        wMat[ind, :] = np.roll(wVec, ind - nCells // 2)
    return wMat


inputVec = np.array([1, 1, 1, 1, 2, 1, 1, 1, 1])  # high bw + signal
# inputVec = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1]) # high bw noise
# inputVec = np.array([0,0,0,1,2,1,0,0,0]) # low bw + signal
# inputVec = np.array([0,0,0,1,1,1,0,0,0]) # low bw noise
nCells = len(inputVec)
midCell = nCells // 2

vThal = np.array([0, 0, 0, 0, 6, 0, 0, 0, 0])
vPV = np.array([0, 0, 0, -0.5, -1, -0.5, 0, 0, 0])
vSOM = np.array([-0.1, -0.1, -0.2, -0.3, -0.5, -0.3, -0.2, -0.1, -0.1])

# vThal = np.array([0, 0, 0, 0, 10, 0, 0, 0, 0])
# vPV   = np.array([0, 0, 0, -2,-2,-2, 0, 0, 0])
# vSOM  = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1])

wThal = make_weights_mat(vThal)
wPV = make_weights_mat(vPV)
wSOM = make_weights_mat(vSOM)

outputVecControl = np.dot(inputVec, wThal) + \
                   np.dot(inputVec, wPV) + \
                   np.dot(inputVec, wSOM)
outputVecControl = outputVecControl.clip(min=0)

outputVecNoSOM = np.dot(inputVec, wThal) + \
                 np.dot(inputVec, wPV)
outputVecNoSOM = outputVecNoSOM.clip(min=0)

outputVecNoPV = np.dot(inputVec, wThal) + \
                np.dot(inputVec, wSOM)
outputVecNoPV = outputVecNoPV.clip(min=0)

toneReportWeights = np.array([-0.2, -0.2, -0.2, -0.2, 1.3, -0.2, -0.2, -0.2,
                              -0.2])  # synaptic strengths from each E neuron to the "go right for 8kHz" neuron

toneReportControl = np.dot(outputVecControl, toneReportWeights)
toneReportNoSOM = np.dot(outputVecNoSOM, toneReportWeights)
toneReportNoPV = np.dot(outputVecNoPV, toneReportWeights)

if 1:
    print('Control  ("go right" input" = {})'.format(toneReportControl))
    # print(outputVecControl)

    print('No SOM  ("go right" input" = {})'.format(toneReportNoSOM))
    # print(outputVecNoSOM)

    print('No PV  ("go right" input" = {})'.format(toneReportNoPV))
    # print(outputVecNoPV)

plt.clf()

plt.subplot(3, 1, 1)
plt.plot(np.arange(nCells), outputVecControl)
plt.ylabel('Control')
plt.title('Activity of each E neuron')

plt.subplot(3, 1, 2)
plt.plot(np.arange(nCells), outputVecNoSOM)
plt.ylabel('No SOM')

plt.subplot(3, 1, 3)
plt.plot(np.arange(nCells), outputVecNoPV)
plt.ylabel('No PV')
plt.xlabel('E neuron')

plt.show()
