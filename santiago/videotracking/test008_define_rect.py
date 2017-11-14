'''
Detect color in video frame.
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt


videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'


def onclick(event):
    print('x={0}, ydata={1}'.format(int(event.xdata), int(event.ydata)))

cap = cv2.VideoCapture(videoFilename)
frameSize = (600,800)

frameIndex = 59 # left
#frameIndex = 490 # right

'''
for indf in range(frameIndex):
    ret, frame = cap.read()
'''

'''
# This method loads only one frame, but the image is not complete
# because it would need to load a few previous ones given compression
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,frameIndex);
ret, frame = cap.read()
'''
# Here is a fix for that method, but the nBack parameters would be a guess.
nBack = 45
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,frameIndex-nBack);
for indf in range(nBack):
    ret, frame = cap.read()
    
cap.release()

plt.clf()
fig = plt.gcf()
plt.imshow(frame)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
#fig.canvas.mpl_disconnect(cid)


# rectCorners = [(170,15),(317,128)]

