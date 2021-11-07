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
freqFactor = 1     # 1 for human hearing range, 8 for mice.
nFT = 2
nVOT = 2

syRange = speechsynth.SyllableRange(nFT, nVOT, sampFreq=sampFreq, freqFactor=freqFactor)
syRange.save('/tmp/speechsounds')

#sys.exit()

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
