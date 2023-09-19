"""
Load pixel change ROI from Facemap file to detect running.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

#filename = '/data/video/acid006/test_proc.npy'
#filename = '/data/video/acid006/acid006_oddball_sequence_20230322_01pre_proc.npy'
filename = '/data/videos_processed/acid010/acid010_oddball_sequence_20230809_03doi_proc.npy'

proc = np.load(filename, allow_pickle=True).item()
pixchange = proc['pixelchange'][0]  # A dict inside a 1-item list, so you need to get the first element
blink = proc['blink'][0]  # A dict inside a 1-item list, so you need to get the first element

winsize = 10
smoothAvg = np.convolve(pixchange, np.ones(winsize), mode='same')/winsize
smoothAvgBlink = np.convolve(blink, np.ones(winsize), mode='same')/winsize

# Threshold for sync light. 
blinkThreshold = np.quantile(blink, 0.50)
blinkBoolean = blink < blinkThreshold

# Counts the peaks of the blinkBoolean
trialCount = len(sig.find_peaks(blinkBoolean)[0])

runningThreshold = 3
runningBoolean = smoothAvg > runningThreshold




plt.clf()
plt.plot(pixchange,'.-')
plt.plot(smoothAvg, '-', lw=2)
plt.plot(runningBoolean*10, '-', lw=4)
plt.show()

# plt.hist(smoothAvg,20)



