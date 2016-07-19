'''
Script to calculate peak, valley, half width from waveforms, using the most prominent channel the spike appears in.
'''

import numpy as np
import sys
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting
from jaratoolbox import settings
from jaratoolbox.test.lan import test022_plot2afc_given_cell_rew_change as cellplotter
import importlib

'''
def calculate_waveform_features(waveforms,featureNames):
    
    Parameters:
      waveforms: [nSpikes,nChannels,nSamples]
      featureNames: list of strings: 'peak','peakFirstHalf','valley','halfWidth'...
    
    nFeatures = len(featureNames)
    [nSpikes,nChannels,nSamples] = waveforms.shape
    featureValues = np.empty((nSpikes,0),dtype=float)
    for oneFeature in featureNames:
        print 'Calculating {0} ...'.format(oneFeature)
        if oneFeature=='peak':
            theseValues = np.amax(waveforms.max(axis=2),axis=1)
            featureValues = np.hstack((featureValues,theseValues))
        elif oneFeature=='peakFirstHalf':
            halfSample = waveforms.shape[2]/2
            theseValues = np.amax(waveforms[:,:,:halfSample].max(axis=2),axis=1)
            featureValues = np.hstack((featureValues,theseValues))
        elif oneFeature=='valley':
            theseValues = np.amax(waveforms.min(axis=2), axis=1)
            featureValues = np.hstack((featureValues,theseValues))
        elif oneFeature=='valleyFirstHalf':
            halfSample = waveforms.shape[2]/2
            theseValues = np.amax(waveforms[:,:,:halfSample].min(axis=2),axis=1)
            featureValues = np.hstack((featureValues,theseValues))
        elif oneFeature=='energy':
            theseValues = np.sqrt(np.sum(waveforms.astype(float)**2,axis=2))
            theseValues = np.amax(theseValues,axis=1)
            featureValues = np.hstack((featureValues,theseValues))
        elif oneFeature=='halfWidth':
            

    return featureValues
    
'''





allcellsFileName = 'allcells_adap012'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

oneCell = allcells.cellDB[391]

_,waveforms,_,_ = cellplotter.load_ephys_per_cell(oneCell)

print waveforms.shape

plt.plot(waveforms[10,0,:])
plt.plot(waveforms[10,1,:])
plt.plot(waveforms[10,2,:])
plt.plot(waveforms[10,3,:])

plt.show()
