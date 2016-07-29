'''
Generating different sounds and saving to a file.
'''

import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()

duration = 2.0
soundAmp = 0.2

soundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=soundAmp)
n = pyo.Noise(mul=soundObj)
soundWaveObj = pyo.EQ(n, freq=14000, q=1, boost = 10, type=0).mix(2).out()


# -- Set recording parameters --
soundFilename = '/home/jarauser/workspace/sounds/EQtest.wav'
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj.play()
ss.start()

# -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

os.system('aplay {0}'.format(soundFilename))
