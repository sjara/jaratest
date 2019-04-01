import os
import numpy as np
from scipy import io
from jaratoolbox import loadbehavior
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
from skimage.external import tifffile

dataDir = '/home/nick/data/2pdata/imag003/'

# good example
session = '002_010'
roi = 0

# The ROIs segmented in sbxsegmenttool
fnROI = 'imag003_{}_rigid.segment.mat'.format(session)

# The traces extracted by scanbox
fnSig = 'imag003_{}_rigid.signals.mat'.format(session)

# The TIFF of the recording itself
fnRecAligned = 'imag003_{}_rigid.tif'.format(session)
fnRec = 'imag003_{}.tif'.format(session)

sigPath = os.path.join(dataDir, fnSig)
sigData = io.loadmat(sigPath)

roiPath = os.path.join(dataDir, fnROI)
roiData = io.loadmat(roiPath)

recPath = os.path.join(dataDir, fnRec)
recData = tifffile.TiffFile(recPath)
recArr = recData.asarray()

recPathAligned = os.path.join(dataDir, fnRecAligned)
recDataAligned = tifffile.TiffFile(recPathAligned)
recArrAligned = recDataAligned.asarray()

# Mask for the first ROI
# We are going to mask out the parts not in the ROI,
# so we set inside ROI to 0 and outsde to 1
mask = np.logical_not(roiData['mask']==roi+1)
mask3d = np.broadcast_to(mask, recArr.shape)

# Mask the data array with the cell ROI mask
maskedArr = np.ma.masked_array(recArr, mask=mask3d)
maskedArrAligned = np.ma.masked_array(recArrAligned, mask=mask3d)

roiMean = np.mean(maskedArr, axis=(1, 2))
roiMeanAligned = np.mean(maskedArrAligned, axis=(1, 2))

plt.clf()
plt.plot(sigData['sig'][:,roi], 'k-', label='Scanbox extraction')
plt.plot(roiMeanAligned, 'r-', label='Jaratest extraction, aligned')
plt.plot(roiMean, 'b-', label='Jaratest extraction, not aligned')
plt.legend(frameon=False)
ax = plt.gca()
extraplots.boxoff(ax)
plt.ylabel('Average pixel value')
plt.xlabel('Frame')
plt.tight_layout()
plt.show()


