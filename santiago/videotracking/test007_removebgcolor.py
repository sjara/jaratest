import numpy as np
import cv2
from pylab import *

#videoFilename = '/data/videos/d1pi013/d1pi013_20160511--11.mkv'
videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
cap = cv2.VideoCapture(videoFilename)

vidlist = []
for indf in range(100):
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vidlist.append(frame)
cap.release()

vid = np.array(vidlist)

bg = np.median(vid,axis=0)

vidnobg = vid.astype(float)-bg.astype(float)

imshow(bg)
#imshow(bg,cmap='gray')
show()
