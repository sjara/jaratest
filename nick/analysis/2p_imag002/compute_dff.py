from matplotlib import pyplot as plt
import numpy as np
from skimage import io
import time

fn = '/home/nick/data/imag002_20181201/imag002_20181201_000_000.tif'
im = io.imread(fn)

imF = np.mean(im, axis=0)
imDFF = np.empty(np.shape(im))

for indFrame in range(np.shape(im)[0]):
    imDFF[indFrame, :, :] = (im[indFrame, :, :]-imF)/imF

from skimage.external import tifffile
tifffile.imsave('/tmp/000_000_dff.tif', imDFF)
