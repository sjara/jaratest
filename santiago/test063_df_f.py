'''
Calculating df/f
'''

from __future__ import division
import numpy as np
import tifffile
from matplotlib import pyplot as plt

#datafile = '/data/exampleNeurolabware/stacks/stack100_240x160_nomotion.tif'
#outputfile = '/data/exampleNeurolabware/stacks/stack100_240x160_dff.tif'
datafile = '/data/exampleNeurolabware/stacks/stack80_796x701.tif'
outputfile = '/data/exampleNeurolabware/stacks/stack80_796x701_dff.tif'

imdata = tifffile.imread(datafile)

offset = 4
imdata = imdata[:, offset:-offset, offset:-offset]

imdata[imdata<1]=1  #Hack to avoid dividing by zero
f0 = np.percentile(imdata, 10, axis=0)
dffdata = imdata-f0/imdata

tifffile.imsave(outputfile,dffdata.astype(np.uint16))