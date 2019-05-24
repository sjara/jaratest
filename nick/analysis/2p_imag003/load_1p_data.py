#Loading the 1p data is annoying because it is saved as a ton of individual images.

import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt
from skimage.external import tifffile


'''
Attempting to use the following func to read the PGM files - found it at: https://stackoverflow.com/questions/7368739/numpy-and-16-bit-pgm/7369986
'''
import re
import numpy

def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))

# fullFile = '/home/nick/data/1pdata/imag003/20181217_noiseburst/fc2_save_2018-12-17-121550-0000.pgm'
dataDir = '/home/nick/data/1pdata/imag003/20181217_noiseburst/'
dataFiles = sorted(os.listdir(dataDir))

#Only load every 4th frame
skipBy = 4

im = read_pgm(os.path.join(dataDir, dataFiles[0]))
indsToRead = range(0, len(dataFiles), skipBy)
imgArr = np.empty((len(indsToRead), im.shape[0], im.shape[1]))

for indFrame, indFile in enumerate(indsToRead):
    im = read_pgm(os.path.join(dataDir, dataFiles[indFile]))
    imgArr[indFrame, :, :] = im

#Save out intermediate data
saveDir = '/home/nick/data/1pdata/tmpData'
outputFn = 'imag003_noiseburst_skipby{}.npy'.format(skipBy)

np.save(os.path.join(saveDir, outputFn), imgArr.astype('uint8'))

# im = read_pgm(fullFile)

# plt.clf()
# plt.imshow(im)
# plt.show()


