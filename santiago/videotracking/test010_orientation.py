'''
Measure orientation change from tracked colors
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt

# Data comes from '/data/videos/d1pi013/d1pi013_20160519-5.mkv'
# created using videoanalysis.py (see __main__)


colortrack = np.load('/var/tmp/colortrack.npz')
colorCenter = colortrack['colorCenter']
stimtrack = np.load('/var/tmp/stimtrack.npz')
stimIntensity = stimtrack['stimIntensity']

headVectorWithNaN = colorCenter[:,:,0]-colorCenter[:,:,1]
nSamples = headVectorWithNaN.shape[1]
headVector = headVectorWithNaN.copy()

# -- Interpolate missing values --
for inds in range(1,nSamples):
    if np.isnan(headVector[0,inds]):
        headVector[0,inds] = headVector[0,inds-1]
        headVector[1,inds] = headVector[1,inds-1]

headAngleDiscont = np.arctan2(headVector[1,:],headVector[0,:])

discontThreshold = np.pi
headAngle = np.unwrap(headAngleDiscont, discont=discontThreshold)
#headAngle = headAngleDiscont

headDiff = np.concatenate((np.diff(headAngle),[0]))

# -- Saturate headDiff --
SATURATE = 0
if SATURATE:
    satuThreshold = 1
    satuValue = 1
    headDiff[headDiff>satuThreshold]=satuValue
    headDiff[headDiff<-satuThreshold]=-satuValue

stimBool = stimIntensity>20
deltaAngleStim1 = np.mean(headDiff[stimBool[0,:]])
deltaAngleStim2 = np.mean(headDiff[stimBool[1,:]])
deltaAngleNoStim = np.mean(headDiff[~stimBool[0,:] & ~stimBool[1,:]])

print 'Delta angle during stimulation:'
print deltaAngleStim1
print deltaAngleStim2
print 'Delta angle no stims:'
print deltaAngleNoStim


plt.clf()
plt.hold(1)
CASE=3
if CASE==1:  # Plot detected position in 2D
    plt.xlim([0,800]); plt.ylim([0,600])
    plt.gca().invert_yaxis()
    for indc in range(2):
        plt.plot(colorCenter[0,:,indc],colorCenter[1,:,indc],'.-')
        plt.draw()
elif CASE==2: # Plot detected coords in 1D
    for indc in range(2):
        ax1 = plt.subplot(3,1,1)
        plt.plot(colorCenter[0,:,indc],'.-')
        ax2 = plt.subplot(3,1,2,sharex=ax1)
        plt.plot(colorCenter[1,:,indc],'.-')
        ax3 = plt.subplot(3,1,3,sharex=ax1)
        plt.plot(stimIntensity.T,'.-')
    plt.draw()
elif CASE==3: # Plot headVector and angle
    ax1 = plt.subplot(3,1,1)
    plt.plot(headAngle,'.-')
    #plt.plot(headVector[0,:,indc],'.-')
    plt.ylabel('Head angle')
    ax2 = plt.subplot(3,1,2,sharex=ax1)
    plt.plot(headDiff,'.-')
    plt.ylabel('Delta head angle')
    ax3 = plt.subplot(3,1,3,sharex=ax1)
    plt.plot(stimIntensity.T,'.-')
    plt.ylabel('Stim')
    plt.draw()

    # Good trials are from samples 900 to 1400
    
plt.show()



'''
    plt.clf()
    ax1 = plt.subplot(2,1,1)
    plt.hold(1)
    plt.plot(colorCenter[:,:,0].T,'.-')
    plt.plot(colorCenter[:,:,1].T,'.-')
    plt.hold(0)
    ax2 = plt.subplot(2,1,2,sharex=ax1)
    plt.hold(1)
    from jaratoolbox import extrafuncs
    for indColor in range(2):
        for coord in range(2):
            colorCenter[coord,:,indColor] = extrafuncs.interpolate_nan(colorCenter[coord,:,indColor])
    plt.plot(colorCenter[:,:,0].T,'.-')
    plt.plot(colorCenter[:,:,1].T,'.-')
    plt.hold(0)
    plt.show()

'''


