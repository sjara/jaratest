'''
Loads the raw LFP data.
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

nSamplesToProcess = int(0.4 * sampleRate)  # 0.4 sec
traceToProcess = rawdata[:nSamplesToProcess, :] * bitVolts  # In uV 
tvec = np.arange(nSamplesToProcess) / sampleRate

## Display a heatmap of a subset of LFP data
#plt.figure(figsize=(15,20))
plt.clf()
#plt.imshow(contData.data[:1000,:].T)
plt.imshow(traceToProcess.T, origin='lower',
           extent=[0, nSamplesToProcess/sampleRate, 0, nChannels])
plt.xlabel('Time (s)')
plt.ylabel('Channel index')
plt.title(f"Heatmap of the raw LFP data across all channels for the first {nSamplesToProcess} samples")
plt.colorbar(label='Amplitude (uV)')
plt.show()
