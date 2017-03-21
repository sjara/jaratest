'''
Test videoanalysis.ColorTracker
'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import videoanalysis
reload(videoanalysis)


MOUSE = 2
if MOUSE==0:
    subject = 'd1pi013'
    session = '20160519-5'
    figuredataFilename = 'example_head_angle_dmstr.npz'
    stimCoords = [ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ]
    stimThreshold = 20
elif MOUSE==1:
    subject = 'd1pi014'
    session = '20161021--2'
    figuredataFilename = 'example_head_angle_astr.npz'
    stimCoords = [ [[260, 50], [280, 60]] ]
    stimThreshold = 30
elif MOUSE==2:
    subject = 'd1pi014'
    session = '20161021--3'  # AStr Right side
    figuredataFilename = 'example_head_angle_astr.npz'
    stimCoords = [ [[520, 80], [545, 95]] ]
    stimThreshold = 30
 
videoPath = settings.VIDEO_PATH
filenameOnly = subject+'_'+session+'.mkv'
filename = os.path.join(videoPath,subject,filenameOnly)

'''
limitsR = [[39, 109, 29],
           [47, 123, 32]]
limitsG = [[29, 31, 70],
           [79, 79, 127]]
colorLimits = [limitsR,limitsG]
'''

# cv2.cvtColor(np.uint8([[[0,255,0]]]),cv2.COLOR_BGR2HSV) # Green
# cv2.cvtColor(np.uint8([[[0,0,255]]]),cv2.COLOR_BGR2HSV) # Red

# -- In OpenCV HSV ranges are (0-179, 0-255, 0-255) --
hsvLimitsG  = [[45,  70,  70],
               [75, 255, 255]]
hsvLimitsR1 = [[ 0,  50,  50],
               [10, 255, 255]]
hsvLimitsR2 = [[170,  70,  70],
               [179, 255, 255]]

colorLimits = [hsvLimitsG,hsvLimitsR2]

minArea = 25  # Minimum number of pixels to detect a color area


vid = videoanalysis.ColorTracker(filename,colorLimits)

#vid.process(minArea=minArea, lastFrame=None, showImage=True)

#mask = vid.show_mask(250)

frame = vid.show_frame(1433)

###mask = np.zeros(mask.shape,dtype=np.uint8)

'''
cntImg = mask.copy()
### http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
contours, hierarchy = cv2.findContours(cntImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(mask, contours, -1, (0,255,0), 3)
plt.cla()
plt.imshow(cntImg>1,cmap='gray')
plt.show()

contoursArea = []
for cnt in contours:
    contoursArea.append(cv2.contourArea(cnt))

print 'Areas'
print contoursArea

largestContour = contours[np.argmax(contoursArea)]

imgMoments = cv2.moments(largestContour)
xbar = imgMoments['m10']/imgMoments['m00']
ybar = imgMoments['m01']/imgMoments['m00']

print (xbar,ybar)
'''


'''
# Create a detector with the parameters
dparams = cv2.SimpleBlobDetector_Params()
dparams.filterByArea = True
dparams.filterByColor = False
dparams.filterByCircularity = False
dparams.filterByConvexity = False
dparams.filterByInertia = False
dparams.minArea = 6
detector = cv2.SimpleBlobDetector(dparams)

# Set up the detector with default parameters.
keypoints = detector.detect(mask)
print '-------- keypoints -------'
print keypoints
# You can see coords: keypoints[0].pt or size keypoints[0].size

whiteimg = np.tile(255,mask.shape).astype('uint8')
im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.cla()
plt.imshow(im_with_keypoints)
plt.show()
'''





'''
# -- Test RED hsv color from image (frame 40) --
hsvImg = cv2.cvtColor(vid.frame,cv2.COLOR_BGR2HSV)
hsvImg[365,620,:]

colorMask = cv2.inRange(hsvImg, np.array([170,  50,  50]), np.array([179, 255, 255]))
#colorMask = cv2.inRange(hsvImg, np.array([170,  50,  50], dtype = "uint8"), np.array([179, 255, 255], dtype = "uint8"))
imshow(colorMask,cmap='gray')
'''

'''
vid.process(minPixels=minPixels, lastFrame=200)
#vid.interpolate()

plt.clf()
plt.hold(1)
plt.plot(vid.colorCenter[0,:,:].T,'.-')
plt.plot(vid.colorCenter[1,:,:].T,'.-')
plt.hold(0)
plt.show()
'''
