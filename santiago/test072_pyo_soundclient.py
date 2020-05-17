'''
Test sounds from taskontrol sound client (based on pyo)
'''

import numpy as np
from taskontrol.plugins import soundclient
reload(soundclient)

sc = soundclient.SoundClient() #(serialtrigger=False)

#s1 = {'type':'AM', 'modFrequency':10, 'duration':1, 'amplitude':0.1*np.array([1,1])}
s1 = {'type':'FM', 'frequency':500, 'duration':0.5, 'amplitude':0.1}
#s1 = {'type':'tone', 'frequency':500, 'duration':1, 'amplitude':0.1}

sc.set_sound(1,s1)
sc.start()
sc.play_sound(1)
sc.shutdown()
