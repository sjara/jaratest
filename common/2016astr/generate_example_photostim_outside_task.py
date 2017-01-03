'''
Script to generate example of change in head-angle after stimulation of dorso-medial str.

NOTE:
- Some parameters used here were calculated using videoanalysis.DefineCoordinates()
'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import videoanalysis
reload(videoanalysis)
import figparams

# -- Select which processing stages to perform --
DEFINE_STIM_COORDS = 0
DETECT_STIMULUS = 0
TRACK_COLORS = 0
CALCULATE_HEAD_ANGLE = 1

MOUSE = 2
if MOUSE==0:
    subject = 'd1pi013'
    session = '20160519-5'  # DMStr Both sides 
    figuredataFilename = 'example_head_angle_dmstr.npz'
    stimCoords = [ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ]
    stimThreshold = 20
elif MOUSE==1:
    subject = 'd1pi014'
    session = '20161021--2'  # AStr Left side
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

outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)
scriptFullPath = os.path.realpath(__file__)

stimFilename = 'stimtrack_{0}_{1}.npz'.format(subject,session)
stimFullPath = os.path.join(outputDir,stimFilename)
ctrackFilename = 'colortrack_{0}_{1}.npz'.format(subject,session)
ctrackFullPath = os.path.join(outputDir,ctrackFilename)
figuredataFullPath = os.path.join(outputDir,figuredataFilename)

if DEFINE_STIM_COORDS:
    vid = videoanalysis.DefineCoordinates(filename)
           
if DETECT_STIMULUS:
    # -- These coords were found using videoanalysis.DefineCoordinates() --
    vid = videoanalysis.StimDetector(filename,stimCoords)
    intensity = vid.measure()
    np.savez(stimFullPath, subject=subject, session=session, coords=stimCoords,
             stimIntensity=intensity, script=scriptFullPath)
    print 'Saved results to {}'.format(stimFullPath)
    plt.clf(); plt.plot(intensity.T,'.-'); plt.show()
             
if TRACK_COLORS:
    # -- These HSV color ranges were found by hand using the Linux gpick app --
    '''
    limitsG = [[70, 170, 110],
               [150, 255, 150]]
    limitsR = [[40, 20, 150],
               [90, 70, 255]]
    colorLimits = [limitsR,limitsG]
    '''
    hsvLimitsG = [[45,  70,  70],
                  [75, 255, 255]]
    hsvLimitsR = [[170,  70,  70],
                  [179, 255, 255]]
    colorLimits = [hsvLimitsG,hsvLimitsR]

    minArea = 40  # Minimum number of pixels to detect a color area
    vid = videoanalysis.ColorTracker(filename,colorLimits)
    vid.process(minArea=minArea, lastFrame=None)
    vid.interpolate()
    np.savez(ctrackFullPath, subject=subject, session=session, colorLimits=colorLimits,
             colorCenter=vid.colorCenter, missedFrames=vid.missed, script=scriptFullPath)
    print 'Saved results to {}'.format(ctrackFullPath)
    plt.clf()
    plt.hold(1)
    plt.plot(vid.colorCenter[0,:,:].T,'.-')
    plt.plot(vid.colorCenter[1,:,:].T,'.-')
    plt.hold(0)
    plt.show()

if CALCULATE_HEAD_ANGLE:
    try:
        colortrack = np.load(ctrackFullPath)
    except IOError:
        print 'ERROR: You first need to create the color-track file using this script.'
        raise
    try:
        stimtrack = np.load(stimFullPath)
    except IOError:
        print 'ERROR: You first need to create the stim-detection file using this script.'
        raise

    colorCenter = colortrack['colorCenter']
    missedFrames = colortrack['missedFrames']
    stimIntensity = stimtrack['stimIntensity']

    headVector = colorCenter[0,:,:]-colorCenter[1,:,:]
    nSamples = headVector.shape[1]

    headAngleDiscont = np.arctan2(headVector[1,:],headVector[0,:])
    headAngle = np.unwrap(headAngleDiscont, discont=np.pi)
    headDiff = np.concatenate((np.diff(headAngle),[0]))

    stimBool = stimIntensity>stimThreshold
    nStim = stimBool.shape[0]
    
    # -- Calculate overall averages --
    if nStim==2:
        deltaAngleStim1 = np.mean(headDiff[stimBool[0,:]])
        deltaAngleStim2 = np.mean(headDiff[stimBool[1,:]])
        deltaAngleNoStim = np.mean(headDiff[~stimBool[0,:] & ~stimBool[1,:]])
    elif nStim==1:
        deltaAngleStim1 = np.mean(headDiff[stimBool[0,:]])
        deltaAngleNoStim = np.mean(headDiff[~stimBool[0,:]])
        
    dStim = np.diff(stimBool.astype(int),axis=1)
    dStim = np.hstack((np.zeros((nStim,1)),dStim)) # To ensure alignement when finding frames in a trial
    firstFrameEachTrial = nStim*[None]
    lastFrameEachTrial = nStim*[None]
    avgDeltaAngleEachTrial = nStim*[None]
    
    for stimInd in range(nStim):
        firstFrameEachTrial[stimInd] = np.flatnonzero(dStim[stimInd,:]>0)
        lastFrameEachTrial[stimInd] = np.flatnonzero(dStim[stimInd,:]<0)

        nTrials = len(firstFrameEachTrial[stimInd])
        avgDeltaAngleEachTrial[stimInd] = np.empty(nTrials)
        for indt in range(nTrials):
            framesThisTrial = range(firstFrameEachTrial[stimInd][indt],
                                    lastFrameEachTrial[stimInd][indt])
            avgDeltaAngleEachTrial[stimInd][indt] = np.mean(headDiff[framesThisTrial])
    
    np.savez(figuredataFullPath, subject=subject, session=session, headAngle=headAngle,
             missedFrames=missedFrames, stimBool=stimBool,
             firstFrameEachTrial=firstFrameEachTrial, lastFrameEachTrial=lastFrameEachTrial,
             script=scriptFullPath)
    print 'Saved results to {}'.format(figuredataFullPath)


    plt.clf()
    plt.hold(1)

    ax1 = plt.subplot(2,1,1)
    plt.plot(headAngle,'.-')
    plt.ylabel('Head angle')
    ax2 = plt.subplot(2,1,2,sharex=ax1)
    plt.plot(stimIntensity.T,'.-')
    plt.ylabel('Stim')
    plt.show()

    print 'Delta angle during stimulation:'
    print deltaAngleStim1
    if nStim>1:
        print deltaAngleStim2
    print 'Delta angle no stims:'
    print deltaAngleNoStim

    print 'Delta angle each trial'
    print avgDeltaAngleEachTrial
