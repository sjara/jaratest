'''
Detect color in video frame.
'''

import numpy as np
import cv2
from pylab import *

videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
cap = cv2.VideoCapture(videoFilename)

frameSize = [600,800]

nFrames = 20
vidlist = []
for indf in range(nFrames):
    ret, frame = cap.read()
    vidlist.append(frame)
cap.release()

#vid = np.array(vidlist)

# Set limits
# Note that colors are in BGR (not RGB)
limitsR = [[40, 20, 150],
           [90, 70, 255]]
limitsG = [[70, 170, 110],
           [150, 255, 150]]
lowerR = np.array(limitsR[0], dtype = "uint8")
upperR = np.array(limitsR[1], dtype = "uint8")
lowerG = np.array(limitsG[0], dtype = "uint8")
upperG = np.array(limitsG[1], dtype = "uint8")

clf()
for indf in range(nFrames):
    oneimage = vidlist[indf]
    onemaskR = cv2.inRange(oneimage, lowerR, upperR)
    onemaskG = cv2.inRange(oneimage, lowerG, upperG)
    #outputR = cv2.bitwise_and(oneimage, oneimage, mask = maskR)
    #outputG = cv2.bitwise_and(oneimage, oneimage, mask = maskG)
    maskR = onemaskR
    maskG = onemaskG

    newimg = np.dstack((maskR,maskG,np.zeros(frameSize,dtype=uint8)))
    imshow(newimg)
    draw()
    show()



'''
    subplot(1,2,1); imshow(maskR,cmap='bwr')
    subplot(1,2,2); imshow(maskG,cmap='winter')
    draw()
    show()
    #waitforbuttonpress()
'''
