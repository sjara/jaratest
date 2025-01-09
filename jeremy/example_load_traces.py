"""
Load LFP data from Neuropixels 1.0.
"""

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
rawdata = contData.data
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

nSamplesToProcess = 1 * sampleRate  # 4 sec
traceToProcess = rawdata[:nSamplesToProcess, :20] * bitVolts  # In uV 
tvec = np.arange(nSamplesToProcess) / sampleRate

if 0:
    plt.clf()
    plt.plot(tvec, traceToProcess)
    plt.show()

# -- Load events --
# NOTE: I don't know yet whether the events we need are those from Neuropix-PXI-100.1/TTL_2
#       or those from Neuropix-PXI-100.0/TTL_1
events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times()
