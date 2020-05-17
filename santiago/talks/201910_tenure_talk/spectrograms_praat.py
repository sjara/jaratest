'''
Show spectrograms of speech.
'''

import speechsynth
reload(speechsynth)
from matplotlib import pyplot as plt


#sbapa = speechsynth.BaPaRange(3)
sbada = speechsynth.BaDaRange(3, sampFreq=4*44100, freqFactor=1)

plt.clf()
spectrogram = sbada[0].to_spectrogram(window_length=0.01, time_step=0.0001,
                                      frequency_step = 40,
                                      maximum_frequency=3000)
speechsynth.show_spectrogram(spectrogram, dynamic_range=60, cmap='viridis')
plt.ylim([0,3000])
plt.xlim([plt.xlim()[0],0.2])
plt.show()


