"""
This is a check for the dtype of the ROI's of FaceMap
"""
import numpy as np
import matplotlib.pyplot as plt

proc = np.load('your_video_proc.npy', allow_pickle = True).item() 
pupil = proc['pupil'][0]
pArea = pupil['area']

plt.plot(pArea)
plt.show()
print('works!')

def findroi(roi):
    if 'blink' in proc:
     print('it exists')
    else:
     return False 
    
roi = proc
findroi(proc)                                                                                                                                                                                               
'it exists'

blink = proc['blink'][0]
type(blink)                                                                                                                                                                                          
numpy.ndarray

blink1 = proc['blink']
type(blink1)                                                                                                                                                                                         
list
  
plt.plot(blink)
plt.show()
