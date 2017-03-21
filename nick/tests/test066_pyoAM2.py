import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()


# make a fader

duration = 2.0
soundAmp = [0.2, 0]

halfAmp = [x*0.5 for x in soundAmp]

envelope = pyo.Sine(freq=5,
                    mul=halfAmp,
                    add=halfAmp,phase=0.75)

soundObj = pyo.Fader(fadein=0.5, fadeout=0.5, dur=duration)

a = pyo.Noise(mul=envelope*soundObj).out()

# Make 2 sounds, out to diff channels, mul by the fader
b = pyo.Sine(freq=2000, mul=[0, 0.2]).out()

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
