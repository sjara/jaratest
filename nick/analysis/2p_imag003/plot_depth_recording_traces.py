import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt

dataDir = '/home/nick/data/2pdata/imag003/'

session = '002_003'
sigFn = 'imag003_{}_rigid.signals.mat'.format(session)


#Read the file with the extracted signals
sigMat = os.path.join(dataDir, sigFn)
sigData = io.loadmat(sigMat)

#Get number of frames and extracted ROIs
signals = sigData['sig']
nFrames, nROIs = np.shape(signals)

plt.clf()
for indROI in range(nROIs):
    plt.plot(signals[:, indROI]-signals[0, indROI])
plt.show()

