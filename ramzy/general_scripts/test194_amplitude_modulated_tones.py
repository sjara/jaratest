"""
Test sinusoidally modulated 
"""

from taskontrol.plugins import soundclient
import numpy as np
import time
from matplotlib import pyplot as plt
from importlib import reload
reload(soundclient)

sc = soundclient.SoundClient()
s1 = {'type':'AMtone', 'toneFrequency': 4000, 'modFrequency':32,
      'duration':1.0, 'modDepth':100, 'amplitude':0.2*np.array([1,1])}
sc.set_sound(1,s1)

tvec,wave = sc.get_wave(1)
plt.clf()
plt.plot(tvec, wave[0, :])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

if 1:
      sc.start()
      sc.play_sound(1)
      time.sleep(2.4)
      sc.shutdown()
