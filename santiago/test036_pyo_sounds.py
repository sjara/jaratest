'''
Generating different sounds and saving to a file.
'''

import pyo
import os

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()

duration = 0.4
soundAmp = 0.1

#a=pyo.Sine(mul=0.1).out(dur=duration)

soundObj = pyo.Fader(fadein=0.002, fadeout=0.002,
                     dur=duration, mul=soundAmp)
soundwaveObjs = []
for oneFreq in [800,1200]:
    soundwaveObjs.append(pyo.Sine(freq=oneFreq,
                                  mul=soundObj).mix(2).out())

# -- Set recording parameters --
soundFilename = '/tmp/tempsound.wav'
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj.play()
ss.start()

# -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

os.system('aplay {0}'.format(soundFilename))
