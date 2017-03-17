import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()


# make a fader

duration = 2.0
soundAmp = [0.05, 0.05]

soundObj = pyo.Fader(fadein=0, fadeout=0, dur=duration, mul=soundAmp)

a = pyo.Noise(mul=soundObj).out()

# play the fader.
# -- Set recording parameters --
soundFilename = '/tmp/test.wav'
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj.play()
ss.start()

# # -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

os.system('aplay {0}'.format(soundFilename))
