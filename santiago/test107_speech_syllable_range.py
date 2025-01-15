"""
Create a range of syllables with different Formant Transitions and VOTs.
"""

import sys
import time
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import speechsynth

from importlib import reload
reload(speechsynth)


sampFreq = 192000  # 44100
freqFactor = 8    # 1 for human hearing range, 8 for mice.
nFT = 1 # 4
nVOT = 6 # 4
votscale = 'log' # 'linear' 'log'

syRange = speechsynth.SyllableRange(nFT, nVOT, sampFreq=sampFreq, freqFactor=freqFactor,
                                    votscale=votscale)
#syRange.save(f'/tmp/ft_vot_{freqFactor}x')

#print(syRange.syllables[0][0].info())
#print(syRange.info())

sys.exit()

syRange.spectrograms(5000*freqFactor)
filename = f'/tmp/spectrograms_{freqFactor}x_{nVOT}x{nFT}.png'
plt.savefig(filename, format='png')

sys.exit()
syRange.plot_waveforms()

'''
# -- Compare instances of the same sound --
import scipy.io.wavfile
f1 = '/tmp/ft_vot_8x/syllable_8x_vot100_ft000.wav'
f2 = '/home/sjara/src/jarasounds/ft_vot_8x_20220115/syllable_8x_vot100_ft000.wav'
fs1, s1 = scipy.io.wavfile.read(f1)
fs2, s2 = scipy.io.wavfile.read(f2)
plot(s1-s2)

## diff /tmp/ft_vot_8x/syllable_8x_vot100_ft000.wav ~/src/jarasounds/ft_vot_8x_20220115/syllable_8x_vot100_ft000.wav
## diff /tmp/ft_vot_8x/syllable_8x_vot100_ft000.wav /tmp/xft_vot_8x/syllable_8x_vot100_ft000.wav

clf(); speechsynth.show_spectrogram(s1,fs1); ylim([0,20000]) 
clf(); speechsynth.show_spectrogram(s2,fs2); ylim([0,20000]) 

'''


'''
plt.clf()
ax0 = plt.subplot(2,1,1)
syRange.syllables[0][0].spectrogram(5000*freqFactor, pad=0)
ax1 = plt.subplot(2,1,2, sharex=ax0)
syRange.syllables[0][0].spectrogram(5000*freqFactor, pad=1)
plt.show()
'''


'''
plt.clf()
for indft in range(nFT):
    for indvot in range(nVOT):
        syRange.syllables[indvot][indft].play();
        #time.sleep(0.3)

        if 1:
            plt.subplot2grid([nVOT, nFT], [indvot, indft])
            syRange.syllables[indvot][indft].spectrogram()
            plt.ylim([0, 5000*freqFactor])
            plt.show()
            wait = input("Press Enter to continue.")
'''
