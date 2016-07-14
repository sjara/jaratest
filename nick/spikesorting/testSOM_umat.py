import pandas as pd
import time as time
import numpy as np
import os
from matplotlib import pyplot as plt
from jaratoolbox import loadopenephys
import sys
import SOMPY



animalName='pinp013'
ephysLoc = '/home/nick/data/ephys/'
ephysPath = os.path.join(ephysLoc, animalName)
ephysFn='2016-05-27_14-13-26'
tetrode=3
spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode{}.spikes'.format(tetrode))
dataSpikes = loadopenephys.DataSpikes(spikesFn)



(numSpikes, numChans, numSamples) = np.shape(dataSpikes.samples)

allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

import timeit
start_time = timeit.default_timer()

msz0 = 30
msz1 = 30

sm = SOMPY.sompy.SOM(allWaves, neighborhood=SOMPY.neighborhood.GaussianNeighborhood(), normalizer=SOMPY.normalization.VarianceNormalizator(), mapsize = [msz0, msz1], initialization='pca', name='sm')
sm.train(n_job = 4, shared_memory = 'yes')

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)

codebookVecs = sm.codebook.matrix
