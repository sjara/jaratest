"""
Toy model to replicate signal detection behavior
during inactivation of SOM and PV interneurons.

Santiago Jaramillo - 2020-04-26
"""

import numpy as np
from matplotlib import pyplot as plt

def make_weights_mat(wVec):
    nCells = len(wVec)
    wMat = np.empty((nCells,nCells))
    for ind in range(nCells):
        wMat[ind,:] = np.roll(wVec,ind-nCells//2)
    return wMat

inputVec = np.array([ 1, 1, 1, 2, 1, 1, 1])
#inputVec = np.array([ 1, 1, 1, 1, 1, 1, 1])
nCells = len(inputVec)
midCell = nCells//2

CASE = 1

if CASE==0:
    vThal = np.array([ 0, 0, 0, 6, 0, 0, 0])
    vPV   = np.array([ 0, 0, 0,-1, 0, 0, 0])
    vSOM  = np.array([-1,-1,-1, 0,-1,-1,-1])
elif CASE==1:
    vThal = np.array([ 0, 0, 0, 10, 0, 0, 0])
    vPV   = np.array([ 0, 0, 0,-2, 0, 0, 0])
    vSOM  = np.array([-1,-1,-1,-2,-1,-1,-1])

wThal = make_weights_mat(vThal)
wPV = make_weights_mat(vPV)
wSOM = make_weights_mat(vSOM)

if 0:
    print(wThal)
    print(wPV)
    print(wSOM)

outputVecControl = np.dot(inputVec,wThal) + \
                   np.dot(inputVec,wPV) + \
                   np.dot(inputVec,wSOM)

outputVecNoSOM = np.dot(inputVec,wThal) + \
                 np.dot(inputVec,wPV)

outputVecNoPV = np.dot(inputVec,wThal) + \
                np.dot(inputVec,wSOM)

diffControl = outputVecControl[midCell]-outputVecControl[midCell-1]
diffSOM = outputVecNoSOM[midCell]-outputVecNoSOM[midCell-1]
diffPV = outputVecNoPV[midCell]-outputVecNoPV[midCell-1]

if 1:
    print('Control  (Δ = {})'.format(diffControl))
    print(outputVecControl)
    
    print('No SOM  (Δ = {})'.format(diffSOM))
    print(outputVecNoSOM)
    
    print('No PV  (Δ = {})'.format(diffPV))
    print(outputVecNoPV)

    
plt.clf()

plt.subplot(3,1,1)
plt.bar(np.arange(nCells), outputVecControl)
plt.ylabel('Control')
plt.title('Activity of each E neuron')

plt.subplot(3,1,2)
plt.bar(np.arange(nCells), outputVecNoSOM)
plt.ylabel('No SOM')

plt.subplot(3,1,3)
plt.bar(np.arange(nCells), outputVecNoPV)
plt.ylabel('No PV')
plt.xlabel('E neuron')

plt.show()


