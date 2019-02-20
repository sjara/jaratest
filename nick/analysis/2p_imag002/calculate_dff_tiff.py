import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt
from skimage.external import tifffile

dataDir = '/home/nick/data/2pdata/imag003'
session = '002_010'
Fn = 'imag003_{}.tif'.format(session)

fullFile = os.path.join(dataDir, Fn)
im0 = tifffile.TiffFile(fullFile)
im0ar = im0.asarray()

f0 = np.mean(im0ar[:10, :, :], axis=0)
# f0 = np.mean(im0ar, axis=0)
# f0_resize=np.reshape(f0.repeat(249), np.shape(im0ar))
f0_repeat=np.repeat(f0[np.newaxis, :, :], im0ar.shape[0], axis=0)

dff = (im0ar - f0_repeat) / f0_repeat

# avgImg = np.mean(im0.asarray(), axis=0)
avgImg = np.mean(dff, axis=0)

# plt.clf()
# plt.imshow(avgImg)
# plt.show()

output=True
outputFn = '/tmp/temp_dff.tiff'

if output:
    # with tifffile.TiffWriter(outputFn) as tif:
    with tifffile.TiffWriter(outputFn, imagej=True) as tif:
        for indFrame in range(dff.shape[0]):
            tif.save(dff.astype('uint16')[indFrame, :, :], compress=0)


