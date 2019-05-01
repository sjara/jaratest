import os
import numpy as np
from scipy import io
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
from skimage.external import tifffile

dataDir = '/home/nick/data/2pdata/imag003/'

# sessionsToPlot = [0, 1, 2, 3, 4, 5, 6, 8, 10, 13, 14, 15, 17, 18, 19]
sessionsToPlot = [8]
# session = '002_019'

for ses in sessionsToPlot:

    Fn = 'imag003_002_{0:03d}_rigid.signals.mat'.format(ses)

    #Read the file with the extracted signals
    sigMat = os.path.join(dataDir, Fn)
    sigData = io.loadmat(sigMat)

    #Get number of frames and extracted ROIs
    signals = sigData['sig']
    nFrames, nROIs = np.shape(signals)

    minSig = np.min(signals.ravel())
    maxSig = np.max(signals.ravel())
    sdSig = np.std(signals.ravel())
    timebase = np.arange(nFrames)

    plt.clf()
    for indROI in range(nROIs):

        yOffset = (4*sdSig) * indROI
        plt.plot(timebase, signals[:,indROI]+yOffset, 'k')

    plt.title('imag003_002_{0:03d}'.format(ses))
    plt.xlabel('Frame')
    extraplots.boxoff(plt.gca(), yaxis=False)
    plt.gca().set_yticks([])
    # plt.show()
    plt.tight_layout()
    plt.show()
    # plt.savefig('/home/nick/data/2pdata/depthReportFigs/{0:03d}.png'.format(ses))

