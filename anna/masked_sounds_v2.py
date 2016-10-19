import pyo
import os
import numpy as np

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()

duration = 1.0
soundAmp = 0.3
toneAmp = 1.5
frequency = 2000
modRate = 4.0
octaves = 2.0

freqhigh = frequency * np.power(2, octaves/2)
freqlow = frequency / np.power(2, octaves/2)

tone = True


halfAmp = 0.5*soundAmp
envelope = pyo.Sine(freq=modRate, mul=halfAmp, add=halfAmp, phase=0.75)
noiseSoundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=envelope)
toneSoundObj = pyo.Fader(fadein=0.002, fadeout=0.002, dur=duration, mul=(soundAmp/16.0)*toneAmp)
#noiseFaderObj = pyo.Fader(dur=duration, mul=envelope)
#toneFaderObj = pyo.Fader(dur=duration, mul=toneAmp)
if np.isinf(octaves):
    masker = pyo.Noise(mul=noiseSoundObj).mix(2).out()
else:
    freqcent = (freqhigh + freqlow)/2
    bandwidth = freqhigh - freqlow
    n = pyo.Noise(mul=noiseSoundObj)
    masker = pyo.IRWinSinc(n, freq=freqcent, bw = bandwidth, type=3, order=400).mix(2).out()
    
if tone:
    soundwaveObjs = []
    soundwaveObjs.append(pyo.Sine(freq = frequency, mul = toneSoundObj).mix(2).out())
    soundwaveObjs.append(masker)
else:
    soundwaveObj = masker

# -- Set recording parameters --
soundFilename = '/home/jarauser/workspace/sounds/{0}amp_{1}octaves_{2}.wav'.format(soundAmp, octaves, str(toneAmp)+"tone" if tone else "noTone")
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj = pyo.Mix([noiseSoundObj, toneSoundObj], voices=2).out()
soundObj.play()
noiseSoundObj.play()
toneSoundObj.play()
ss.start()

# -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

os.system('aplay {0}'.format(soundFilename))