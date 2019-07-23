'''
Testing CaImAn for analysis of two-photon data.
https://github.com/flatironinstitute/CaImAn
'''

from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots

datafile = '/data/exampleCaImAn/demoMovie.tif'
#datafile = '/data/exampleNeurolabware/stacks/stack100_240x160.tif'

imdata = io.imread(datafile)
nFrames,width,height = imdata.shape
#print(imdata.shape)

plt.clf()
#extraplots.FlipThrough(plt.imshow, imdata) # Does not work on Mac+Anaconda
plt.imshow(imdata[600,:,:])
plt.axis('scaled')
plt.show()