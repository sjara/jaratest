import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()


# make a fader

duration = 2.0
soundAmp = [0.2, 0.2]

### One way of doing it
halfAmp = [x*0.5 for x in soundAmp]

envelope = pyo.Sine(freq=5,
                    mul=halfAmp,
                    add=halfAmp,phase=0.75)

soundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=envelope)

# Make 2 sounds, out to diff channels, mul by the fader
a = pyo.Noise(mul=soundObj).out()
# b = pyo.Sine(freq=2000, mul=soundObj).out(chnl=1)

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
