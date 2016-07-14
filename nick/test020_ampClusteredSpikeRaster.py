
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
import os
from matplotlib.mlab import PCA
from sklearn.mixture import GMM
from pylab import *
import matplotlib.pyplot as plt

GAIN = 5000.0

ephys_session = '/home/nick/data/ephys/hm4d002/2014-08-25_16-33-38'

tetrode = 4

# -- Read ephys data
ephys_file = os.path.join(ephys_session, 'Tetrode{0}.spikes'.format(tetrode))
spikes = loadopenephys.DataSpikes(ephys_file)

convertedSamples=(spikes.samples-32768.0)/GAIN*1000.0

