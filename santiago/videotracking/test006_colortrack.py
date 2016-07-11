'''
Detect color in video frame.
'''

import numpy as np
import cv2
from pylab import *

videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
cap = cv2.VideoCapture(videoFilename)
frameSize = (600,800)
###fps = 24
###  outVideo = cv2.VideoWriter('/tmp/trackvideo.avi',-1,fps,frameSize)  ### Doesn't work


# Set limits (Note that colors in OpenCV are in BGR, not RGB)
limitsR = [[40, 20, 150],
           [90, 70, 255]]
limitsG = [[70, 170, 110],
           [150, 255, 150]]
lowerR = np.array(limitsR[0], dtype = "uint8")
upperR = np.array(limitsR[1], dtype = "uint8")
lowerG = np.array(limitsG[0], dtype = "uint8")
upperG = np.array(limitsG[1], dtype = "uint8")


nFrames = 10000
vidlist = []
for indf in range(2600,nFrames):
    ret, frame = cap.read()
    #vidlist.append(frame)
    oneimage = frame
    onemaskR = cv2.inRange(oneimage, lowerR, upperR)
    onemaskG = cv2.inRange(oneimage, lowerG, upperG)
    #outputR = cv2.bitwise_and(oneimage, oneimage, mask = maskR)
    #outputG = cv2.bitwise_and(oneimage, oneimage, mask = maskG)
    maskR = onemaskR
    maskG = onemaskG

    #newimg = np.dstack((maskR,maskG,np.zeros(frameSize,dtype=uint8))) # RGB
    newimg = np.dstack((np.zeros(frameSize,dtype=uint8),maskG,maskR)) # BGR

    cv2.imwrite('/tmp/frames/frame{0:08}.png'.format(indf), newimg)
    if not (indf%100):
        print indf
    #outVideo.write(newimg)
    #imshow(newimg); draw(); show()

# -- Run this at the end (if stopped with Ctrl-C) --
cap.release()
### outVideo.release() ### Doesn't work
