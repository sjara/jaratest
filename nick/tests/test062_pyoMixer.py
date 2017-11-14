# import pyo
# import time

# #s = pyo.Server(duplex=0, audio='pa')
# # s = s.boot()
# # s.start()

# # a = pyo.Sine(200)
# # b = pyo.Sine(400)

# # mm = pyo.Mixer(outs=2)

# # mm.addInput(0,a)
# # mm.setAmp(0,0,1)
# # mm.setAmp(0,1,0)

# # mm.addInput(1,b)
# # mm.setAmp(1,0,0)
# # mm.setAmp(1,1,1)

# # mm.out()
# # time.sleep(2)
# # mm.stop()

import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()


# make a fader

duration = 2.0
soundAmp = 0.2
soundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=soundAmp)

# Make 2 sounds, out to diff channels, mul by the fader
a = pyo.Noise(mul=soundObj).out(chnl=0)
b = pyo.Sine(freq=2000, mul=soundObj).out(chnl=1)

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

