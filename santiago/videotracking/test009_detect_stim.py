'''
Detect color in video frame.
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt


videoFilename = '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
# This video contains 6 left and 6 right stimulations

thresholdIntensity = 20

rectLeftX = [271, 306]; rectLeftY = [65, 87] # Left
rectRightX = [271, 306]; rectRightY = [65, 87] # Right
#rectCornersX = [528, 556]; rectCornersY = [60, 77] # Right

cap = cv2.VideoCapture(videoFilename)
frameSize = (600,800)

nFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) # 1621 for d1pi013_20160519-5.mkv
#nFrames = 1000

avgIntensity = np.empty(nFrames)

for indf in range(nFrames):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    chunkLeft = gray[rectLeftY[0]:rectLeftY[1], rectLeftX[0]:rectLeftX[1]]
    chunkRight = gray[rectRightY[0]:rectRightY[1], rectRightX[0]:rectRightX[1]]
    avgIntensity[indf] = np.mean(chunk)
    #if avgIntensity[indf]>5: break
cap.release()

plt.clf()
fig = plt.gcf()
plt.subplot(2,1,1)
plt.imshow(gray,vmin=0,vmax=255)
plt.subplot(2,1,2)
plt.plot(avgIntensity,'.-')

plt.show()
#fig.canvas.mpl_disconnect(cid)


# rectCorners = [(170,15),(317,128)]

