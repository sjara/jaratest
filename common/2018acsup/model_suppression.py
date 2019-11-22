"""
Neural model that accounts for differences in surround supression
between PV and SOM cells in auditory cortex.
"""

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

def gaussian(x, mu, amp, sigma, offset):
    return offset + amp * np.exp(-0.5*((x-mu)/sigma)**2)

def findsigma(x, y, mu, amp):
    """Solve for sigma given Gaussian parameters and one point"""
    return (x-mu)/np.sqrt(-2*np.log(y/amp))

def rect(vecsize, midpoint, bandwidth):
    """
    bandwidth needs to be an odd number.
    """
    if not bandwidth%2:
        raise ValueError('bandwidth need to be an odd number')
    vec = np.zeros(vecsize)
    vec[midpoint-bandwidth//2:midpoint+bandwidth//2+1] = 1
    return vec

class Network(object):
    def __init__(self, nCellsPerLayer, wParams=None):
        """
        nCellsPerLayer (int): number of cells for each type.
        wParams (dict): dict with parameters that define weights, with the format
                        wParams = {'ampPV':-20, 'stdPV':10,
                                   'ampSOM':-20, 'stdSOM':30,
                                   'ampThal':100, 'stdThal':6}
        """
        self.nColumns = nCellsPerLayer

        self.wPV = []
        self.wSOM = []
        self.wThal = []
        self.outputVec = []
        self.activationVec = []
        self.inputVec = []

        if wParams is not None:
            self.setThal(wParams['ampThal'], wParams['stdThal'])
            self.setPV(wParams['ampPV'], wParams['stdPV'])
            self.setSOM(wParams['ampSOM'], wParams['stdSOM'])
                
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

    def simulate_inactivation(self):
        condLabels = ['Control','No PV','No SOM']
        cellLabels = ['PV','SOM']
        activeCells = [[1,1], [0,1], [1,0]]
        bandwidths = np.arange(1, self.nColumns, 2)
        centerCellOutput = np.empty((len(condLabels), len(bandwidths)))
        wPVcopy = np.copy(self.wPV)
        wSOMcopy = np.copy(self.wSOM)
        for indc, cond in enumerate(condLabels):
            if activeCells[indc][0]:
                self.wPV = wPVcopy
            else:
                self.wPV = 0*wPVcopy
            if activeCells[indc][1]:
                self.wSOM = wSOMcopy
            else:
                self.wSOM = 0*wSOMcopy
            centerCellOutput[indc,:] = self.run_manybw(0, bandwidths)
        self.wPV = wPVcopy
        self.wSOM = wSOMcopy
        return centerCellOutput, bandwidths, condLabels
    
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


def suppression_index(bwtunings):
    """
    Calculate suppression index given bandwidth tunings
    bwTuning (np.array): each row is one bandwidth tuning
    """
    suppIndex = np.empty(bwtunings.shape[0])
    for indr,bwtuning in enumerate(bwtunings):
        peakFiring = np.max(bwtuning)
        wnFiring = bwtuning[-1]
        suppIndex[indr] = (peakFiring-wnFiring)/peakFiring
    return suppIndex

def change_in_response(bwTunings):
    """
    Calculate change in response (with respect to a control condition)
    at peak of the response and at white noise given three bandwidth
    tunings (where the first one is the control).
    The peak is estimated from the first bandwidth tuning.
    bwTuning (np.array): 3-row array
    """
    peakBW = np.argmax(bwTunings[0,:])
    changeAtPeak = np.array([bwTunings[1,peakBW]-bwTunings[0,peakBW],
                             bwTunings[2,peakBW]-bwTunings[0,peakBW]])
    changeAtWN = np.array([bwTunings[1,-1]-bwTunings[0,-1],
                           bwTunings[2,-1]-bwTunings[0,-1]])
    return changeAtPeak, changeAtWN

        
if __name__ == '__main__':

    nCells = 41

    net = Network(nCells)

    plt.figure(2)
    plt.clf()

    ampPV = -3; stdPV = 6
    ampSOM = -1.5; stdSOM = 20
    ampThal = 10; stdThal = 4
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
    
    
