'''
Detect color in video frame.
'''

import numpy as np
import cv2
from pylab import *

videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
cap = cv2.VideoCapture(videoFilename)

vidlist = []
for indf in range(10):
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vidlist.append(frame)
cap.release()

vid = np.array(vidlist)

oneimage = vidlist[9]

'''
figure(1)
for ind in range(3):
    subplot(1,3,ind)
    imshow(oneimage[:,:,ind],cmap='gray')
show()
'''

# Set limits
# Note that colors are in BGR (not RGB)
limitsR = [[40, 20, 150],
           [90, 70, 255]]
limitsG = [[70, 160, 110],
           [150, 250, 150]]
lowerR = np.array(limitsR[0], dtype = "uint8")
upperR = np.array(limitsR[1], dtype = "uint8")
lowerG = np.array(limitsG[0], dtype = "uint8")
upperG = np.array(limitsG[1], dtype = "uint8")

# find the colors within the specified boundaries and apply
# the mask
maskR = cv2.inRange(oneimage, lowerR, upperR)
maskG = cv2.inRange(oneimage, lowerG, upperG)
outputR = cv2.bitwise_and(oneimage, oneimage, mask = maskR)
outputG = cv2.bitwise_and(oneimage, oneimage, mask = maskG)

figure(2)
imshow(outputG)
show()
