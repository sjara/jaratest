import pyo
import os
import numpy as np

#These will live in rigsettings
SOUND_SYNC_CHANNEL=None
SYNC_SIGNAL_AMPLITUDE=0.2
SYNC_SIGNAL_FREQUENCY=500

# Run this the first time
if 1:
    ss = pyo.Server(audio="offline")
    ss.boot()

soundParams = {}
soundParams.update({'amplitude':[0.1, 0.1]})

risetime=0.02
falltime=0.02
duration=0.1


case=1
soundWaveObjs = []
if SOUND_SYNC_CHANNEL is not None:
    #Add the sync signal to the list of soundWaveObjs
    soundParams['amplitude'][SOUND_SYNC_CHANNEL]=0 #Silence all other sounds in the sync channel


soundAmp = soundParams['amplitude']
if case==0:
    soundObj = pyo.Fader(fadein=risetime, fadeout=falltime,
                            dur=duration)
    soundWaveObjs.append(pyo.Sine(2000, mul=soundObj*soundAmp).out())

if case==1:
    soundObj = pyo.Fader(fadein=risetime, fadeout=falltime,
                            dur=duration, mul=soundAmp)
    soundWaveObjs.append(pyo.Sine(2000, mul=soundObj).out())

if case==2:
    modFreq = 8
    halfAmp = [0.5*x for x in soundParams['amplitude']]
    envelope = pyo.Sine(freq=modFreq,
                        mul=halfAmp,
                        add=halfAmp,phase=0.75)

    soundObj = pyo.Fader(fadein=risetime, fadeout=falltime,
                            dur=duration)
    soundWaveObjs.append(envelope)
    soundWaveObjs.append(pyo.Noise(mul=envelope).out())

if SOUND_SYNC_CHANNEL is not None:
    syncAmp = [0,0]
    syncAmp[SOUND_SYNC_CHANNEL]=SYNC_SIGNAL_AMPLITUDE #Only set the sync signal to play in the sync channel
    syncFreq = SYNC_SIGNAL_FREQUENCY
    soundWaveObjs.append(pyo.Sine(float(syncFreq), mul=syncAmp).out())

soundFilename = '/tmp/original_method.wav'
ss.recordOptions(dur=duration, filename=soundFilename,
                fileformat=0, sampletype=0)

soundObj.play()
ss.start()

# # -- Shutdown the server and delete the variable --
ss.shutdown()
del ss

# os.system('aplay {0}'.format(soundFilename))


