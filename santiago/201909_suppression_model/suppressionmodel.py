"""
Neural model that accounts for differences in surround supression
between PV and SOM cells in auditory cortex.
"""

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

def gaussian(x, mu, amp, sigma, offset):
    return offset + amp * np.exp(-((x-mu)/sigma)**2)

def rect(vecsize, midpoint, width):
    """
    bw is the width and needs to be an odd number.
    """
    vec = np.zeros(vecsize)
    vec[midpoint-width//2:midpoint+width//2+1] = 1
    return vec

class Neuron(object):
    def __init__(self):
        pass


class Network(object):
    def __init__(self, nCellsPerLayer):
        self.nColumns = nCellsPerLayer

        self.wPV = []
        self.wSOM = []
        self.wThal = []
        self.outputVec = []
        self.activationVec = []
        self.inputVec = []
        
        self.setPV(-1, self.nColumns/10)
        self.setSOM(-2, self.nColumns/2)
        self.setThal(4, self.nColumns/10)
        
    def make_weights_mat(self, stdev):
        xVec = np.arange(3*self.nColumns)
        midPoint = self.nColumns+self.nColumns//2
        gaussianWeights = gaussian(xVec, midPoint, 1, stdev, 0)
        wMat = np.empty((self.nColumns, self.nColumns))
        for indr in range(self.nColumns):
            wMat[indr,:] = -gaussianWeights[midPoint-indr:midPoint+self.nColumns-indr]
        return wMat
    
    def setPV(self, ampPV, stdPV):
        self.wPV = -ampPV * self.make_weights_mat(stdPV)
        
    def setSOM(self, ampSOM, stdSOM):
        self.wSOM = -ampSOM * self.make_weights_mat(stdSOM)
        
    def setThal(self, ampThal, stdThal):
        self.wThal = -ampThal * self.make_weights_mat(stdThal)
        
    def run(self, center, bandwidth):
        """
        Calculate output.
        center (int): in units of number of cells. Zero means the center cell.
        bandwidth (odd int): width of input in units of number of cells.
        """
        midpoint = self.nColumns//2 - center
        self.inputVec = rect(self.nColumns, midpoint, bandwidth)
        self.activationVec = np.dot(self.wPV, self.inputVec) + \
                         np.dot(self.wSOM, self.inputVec) + \
                         np.dot(self.wThal, self.inputVec)
        self.outputVec = self.activationVec*(self.activationVec>0)
        
    def run_manybw(self, center, bandwidths):
        """
        Calculate the output of the center cell for a set of bandwidths.
        center (int): center of stim.
        bandwidths (np.array): bandwidths of stim.
        """
        midpoint = self.nColumns//2
        centerOutput = np.zeros(len(bandwidths))
        for indbw, oneBW in enumerate(bandwidths):
            self.run(center, oneBW)
            centerOutput[indbw] = self.outputVec[midpoint]
        return centerOutput
            
    def plot_weights(self):
        plt.clf()
        plt.subplot(1,3,1)
        plt.imshow(self.wSOM)
        plt.title('wSOM')
        plt.colorbar()
        plt.subplot(1,3,2)
        plt.imshow(self.wPV)
        plt.title('wPV')
        plt.colorbar()
        plt.subplot(1,3,3)
        plt.imshow(self.wThal)
        plt.title('wThal')
        plt.colorbar()

    def plot_output(self):
        plt.clf()
        cellVec = np.arange(self.nColumns)-self.nColumns//2
        plt.subplot(2,1,1)
        plt.bar(cellVec, self.inputVec, fc='0.5')
        plt.ylabel('Input')
        plt.subplot(2,1,2)
        plt.bar(cellVec, self.outputVec)
        plt.ylabel('Exc')

if __name__ == '__main__':

    nCells = 41

    net = Network(nCells)

    plt.figure(2)
    plt.clf()

    ampPV = -1; stdPV = 4
    ampSOM = -1.25; stdSOM = 20
    ampThal = 6; stdThal = 4
    for CASE in [0,1,2]:
        if CASE==0:
            '''Control'''
            net.setPV(ampPV, stdPV)
            net.setSOM(ampSOM, stdSOM)
            net.setThal(ampThal, stdThal)

            plt.figure(1)
            net.plot_weights()
        if CASE==1:
            '''No PV'''
            net.setPV(0, stdPV)
            net.setSOM(ampSOM, stdSOM)
            net.setThal(ampThal, stdThal)
        if CASE==2:
            '''No SOM'''
            net.setPV(ampPV, stdPV)
            net.setSOM(0, stdSOM)
            net.setThal(ampThal, stdThal)

        bandwidths = np.arange(3,41+2,2)
        centerOutput = net.run_manybw(0, bandwidths)

        plt.figure(2)
        #plt.clf()
        plt.plot(bandwidths,centerOutput,'.-')

    plt.legend(['Control','No PV','No SOM'])
    plt.show()

    
    '''
    # -- Plot output of all neurons for one stimulus --
    net.run(0, 13)
    plt.figure(2)
    net.plot_output()
    plt.show()
    '''
    
    
