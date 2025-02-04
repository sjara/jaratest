'''
Loads the raw LFP data and behavior. 
Displays a heatmap of a subset of LFP data. 
x-axis is time from sample 0 to sample 1000. 
y-axis is channel index. 
Intensity is proportional to electric potential.
'''

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadneuropix
from jaratoolbox import settings
from importlib import reload
reload(loadneuropix)

subject = 'feat018'
session = '2024-06-14_11-20-22'
dataStream = 'Neuropix-PXI-100.1'

rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', session)

info = loadneuropix.read_oebin(rawDataPath, dataStream)
contData = loadneuropix.Continuous(rawDataPath, dataStream)
rawdata = contData.data # Data x Acquisition channels (384 channels in total)
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

## Display a heatmap of a subset of LFP data
plt.figure(figsize=(15,20))
plt.imshow(contData.data[:1000,:].T)
plt.title("Heatmap of the LFP data across all acquisition channels from n=0 to n=1000 | yellow = high, purple = low")
plt.colorbar()
plt.show()