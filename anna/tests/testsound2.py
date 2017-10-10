'''
Generating different BPN sounds and saving to a file.
'''

import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()

duration = 2.0
octaves = 1.0
soundAmp = 0.3
modRate = 10
centerFreq = 8000

freqhigh = centerFreq * np.power(2, octaves/2)
freqlow = centerFreq / np.power(2, octaves/2)
envelope = pyo.Sine(freq=modRate, mul=soundAmp/2, add=soundAmp/2, phase=0.75)
soundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=envelope)
freqcent = (freqhigh + freqlow)/2
bandwidth = freqhigh - freqlow
n = pyo.Noise(mul=soundObj)
soundwaveObj = pyo.IRWinSinc(n, freq=freqcent, bw = bandwidth, type=3, order=400).out()



# -- Set recording parameters --
soundFilename = '/home/jarauser/workspace/sounds/{0}octaves.wav'.format(octaves)
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj.play()
ss.start()

# -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

os.system('aplay {0}'.format(soundFilename))
