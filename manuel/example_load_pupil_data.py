"""
This is an example script showing how to load files created by FaceMap.
It assumes you have processed a video which resulted in the creation
of the file 'myvideo_proc.npy'.
"""

import numpy as np

proc = np.load('myvideo_proc.npy').item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']
