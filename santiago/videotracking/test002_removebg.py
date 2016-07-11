import numpy as np
import cv2
from pylab import *

videoFilename = '/data/videos/d1pi013/d1pi013_20160511--11.mkv'
cap = cv2.VideoCapture(videoFilename)

vidlist = []
for indf in range(1000):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vidlist.append(gray)
cap.release()

vid = np.array(vidlist)

bg = np.median(vid,axis=0)

vidnobg = vid-bg

imshow(bg,cmap='gray')
show()

'''
threshold = -50
for indf in range(100):
    imshow(vidnobg[indf]<threshold,cmap='gray')
    show()
    waitforbuttonpress()
'''
