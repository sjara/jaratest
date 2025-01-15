"""
Test speech synthesis module.
"""

import sys
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import speechsynth

from importlib import reload
reload(speechsynth)


sampFreq = 192000 #44100 # 
freqFactor = 8 # 1 for human hearing range, 8 for mice.
burstDuration = 0.000001#0.004
vowelDuration = 0.22 # 0.315
silenceDuration = 0.02
formantTransitionDuration = 0.035
prevoiceDuration = 0
aspPoint = 0 #.08 # 0.08 # 0
formantSetBA = np.array([[80, 100, 0],
                         [220, 710, 50],
                         [900, 1240, 70],
                         [2000, 2500, 110]], dtype='float')

syllableObj = speechsynth.Syllable(vowelDuration, formantTransitionDuration, aspPoint,
                                   burstDuration, prevoiceDuration, silenceDuration,
                                   formantSetBA*freqFactor, sampFreq)
sound = syllableObj.create_sound()

#syllableObj.play()

plt.clf()
plt.subplot(2,1,1)
syllableObj.spectrogram()
plt.ylim([0, 5000*freqFactor])
plt.subplot(2,1,2)
tvec, swave = syllableObj.as_array()
plt.plot(tvec, swave)
plt.show()

sys.exit()


# -- Compare spectrograms from Praat and speechsynth.py --
plt.figure(2)
plt.clf()
spectrogram = sound.to_spectrogram(window_length=0.02, time_step=0.0001,
                                   maximum_frequency=5000*freqFactor)
ax1 = plt.subplot(2,1,1)
speechsynth.show_praat_spectrogram(spectrogram, 140)
ax2 = plt.subplot(2,1,2,sharex=ax1)
syllableObj.spectrogram(cmap='binary')
plt.ylim([0, 5000*freqFactor])
plt.xlim((0.0196139556940549, 0.2043860443059451))
plt.show()




'''
freqFactor = 1
#sound = speechsynth.ba()
sy = speechsynth.ba(speechsynth.formantSetBA)
sound = sy.create_sound()
sys.exit()
plt.clf()
spectrogram = sound.to_spectrogram(window_length=0.02, time_step=0.0001, maximum_frequency=5000*freqFactor)
speechsynth.show_praat_spectrogram(spectrogram, 100)
plt.show()
sys.exit()
'''

'''
sampFreq = 192000 #44100
freqFactor = 1 # 1 for human hearing range, 8 for mice.

burstDuration = 0.004
vowelDuration = 0.2 # 0.315
formantTransitionDuration = 0.035
prevoiceDuration = 0
aspPoint = 0
nFormants = 3
syllableObj = speechsynth.Syllable(vowelDuration, formantTransitionDuration, aspPoint,
                           burstDuration, prevoiceDuration, nFormants, sampFreq)
syllableObj.set_pitch(80*freqFactor, 120*freqFactor)
if nFormants>0:
    syllableObj.set_formant(1, 220*freqFactor, 710*freqFactor, 50*freqFactor)
if nFormants>1:
    syllableObj.set_formant(2, 900*freqFactor, 1240*freqFactor, 70*freqFactor)
if nFormants>2:
    syllableObj.set_formant(3, 2000*freqFactor, 2500*freqFactor, 110*freqFactor)
#syllableObj.set_formant(4, 3600*freqFactor, 3600*freqFactor, 170*freqFactor)
#syllableObj.set_formant(5, 4500*freqFactor, 4500*freqFactor, 250*freqFactor)

sound = syllableObj.create_sound()

if 0:
    plt.clf()
    spectrogram = sound.to_spectrogram(window_length=0.02, time_step=0.0001, maximum_frequency=5000*freqFactor)
    speechsynth.show_praat_spectrogram(spectrogram, 100)
else:
    plt.figure(1)
    plt.clf()
    swave = sound.as_array().squeeze()
    NFFT = 4*2048  # 4096 replicates Praat
    cmap = 'viridis'
    #cmap = 'binary'
    plt.specgram(swave, NFFT=NFFT, noverlap=int(NFFT*0.95),  Fs=sampFreq, cmap=cmap, vmin=-150)
    plt.ylim([0, 5000*freqFactor])
    plt.xlim([0, 0.25])
    plt.xlim((0.0196139556940549, 0.2043860443059451))
    timeVec = np.arange(0,len(swave))/sampFreq
    plt.figure(2); plt.clf(); plt.plot(timeVec, swave)
plt.show()

#pad_to=NFFT*2,

    

syllableObj.play()


#speechsynth.BaPaRange(6, freqFactor=8, sampFreq=sampFreq, outputDir='~/tmp/soundsBaPa/')
'''
