import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt

dataDir = '/home/nick/data/2pdata/imag003/'

session = '000_007'
FnROI = 'imag003_{}_rigid.segment.mat'.format(session)

#Read the file with the ROI masks
roiMat = os.path.join(dataDir, FnROI)
roiData = io.loadmat(roiMat)
roiImg = roiData['mask']

indROI = 10

#Map of ROIs
roiLocs = roiImg>0

#Mask to show highlighted ROI in red
maskedArr = np.ma.masked_where(roiImg!=indROI+1,roiLocs) #The ROIs start from 1

plt.clf()
plt.imshow(roiLocs, cmap='gray')
plt.imshow(maskedArr, cmap='autumn')
plt.title("ROI {}".format(indROI))
plt.show()
