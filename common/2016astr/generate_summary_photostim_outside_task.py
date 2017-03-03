'''
Script to quantify change in head-angle after stimulation outside of the task
for each session.
'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import videoanalysis
reload(videoanalysis)
import figparams

FIGNAME = 'photostim_outside_task'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
scriptFullPath = os.path.realpath(__file__)

# -- Select which processing stages to perform --
DEFINE_STIM_COORDS = 0
DETECT_STIMULUS = 0
TRACK_COLORS = 0
CALCULATE_HEAD_ANGLE = 0
SAVE_ALL_TOGETHER = 1

allSessions = []
# All sessions were using continuous laser pulse at 1mW
oneSession = {'subject':'d1pi011', 'session':'20160609--4', 'stimThreshold':40, 'stimSide':'left,right',
              'stimRegion':'frontStr', 'stimCoords':[ [[275, 50], [290, 60]], [[530, 50], [545, 60]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi011', 'session':'20160609--10', 'stimThreshold':40, 'stimSide':'left,right',
              'stimRegion':'backStr', 'stimCoords':[ [[275, 50], [290, 60]], [[530, 50], [545, 60]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi013', 'session':'20160519-2', 'stimThreshold':20, 'stimSide':'left,right',
              'stimRegion':'frontStr', 'stimCoords':[ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi013', 'session':'20160519-5', 'stimThreshold':20, 'stimSide':'left,right',
              'stimRegion':'frontStr', 'stimCoords':[ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi013', 'session':'20160519-8', 'stimThreshold':20, 'stimSide':'left,right',
              'stimRegion':'backStr', 'stimCoords':[ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi013', 'session':'20160523--3', 'stimThreshold':55, 'stimSide':'left,right',
              'stimRegion':'frontStr', 'stimCoords':[ [[272, 76], [289, 87]], [[527, 74], [545, 83]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi013', 'session':'20160523--6', 'stimThreshold':20, 'stimSide':'left,right',
              'stimRegion':'backStr', 'stimCoords':[ [[272, 76], [289, 87]], [[527, 74], [545, 83]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi014', 'session':'20161021--2', 'stimThreshold':30, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[260, 50], [280, 60]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi014', 'session':'20161021--3', 'stimThreshold':30, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[520, 80], [545, 95]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi014', 'session':'20161021--4', 'stimThreshold':30, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[275, 85], [290, 95]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi014', 'session':'20161021--5', 'stimThreshold':30, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[520, 80], [545, 95]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi014', 'session':'20161109--2', 'stimThreshold':40, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[278, 50], [302, 66]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi014', 'session':'20161109--3', 'stimThreshold':40, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[539, 50], [560, 62]] ]}
#allSessions.append(oneSession) # 0.5mW
#### Repeated sessions 20161109--2 & 20161109--3 here before ####
oneSession = {'subject':'d1pi014', 'session':'20161109--4', 'stimThreshold':40, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[278, 50], [302, 66]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi014', 'session':'20161109--5', 'stimThreshold':40, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[539, 50], [560, 62]] ]}
allSessions.append(oneSession)

# -- Videos for d1pi015, nFrames does not give an accurate number of frames.
oneSession = {'subject':'d1pi015', 'session':'20160804--2', 'stimThreshold':40, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[267, 72], [283, 83]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi015', 'session':'20160804--3', 'stimThreshold':40, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[519, 74], [534, 81]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi016', 'session':'20160729--2', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'backStr', 'stimCoords':[ [[279, 81], [299, 92]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi016', 'session':'20160729--3', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'backStr', 'stimCoords':[ [[534, 76], [549, 85]] ]}
allSessions.append(oneSession)


oneSession = {'subject':'d1pi022', 'session':'20170213--1', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 29], [551, 36]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170213--2', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[266, 26], [285, 39]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170213--3', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[266, 26], [285, 39]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170213--4', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 29], [551, 36]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170214--1', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[547, 52], [561, 59]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170214--2', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[547, 52], [561, 59]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170214--3', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[547, 52], [561, 59]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170214--4', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[277, 48], [294, 59]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170214--5', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[277, 48], [294, 59]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170214--6', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[277, 48], [294, 59]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170216--1', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 43], [543, 51]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170216--2', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 43], [543, 51]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170216--3', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 43], [543, 51]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170216--4', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[532, 43], [543, 51]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170216--5', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[264, 44], [279, 52]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170216--6', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[264, 44], [279, 52]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170216--7', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[264, 44], [279, 52]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170216--8', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[264, 44], [279, 52]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi022', 'session':'20170226--1', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170226--2', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170226--3', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170226--4', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170226--5', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170226--6', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi022', 'session':'20170226--7', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi022', 'session':'20170226--8', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[,], [,]] ]}
allSessions.append(oneSession)


oneSession = {'subject':'d1pi023', 'session':'20170226--1', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170226--2', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170226--3', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi023', 'session':'20170226--4', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi023', 'session':'20170226--5', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170226--6', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170226--7', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)
oneSession = {'subject':'d1pi023', 'session':'20170226--8', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi023', 'session':'20170301--1', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170301--2', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession) 
oneSession = {'subject':'d1pi023', 'session':'20170301--3', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi023', 'session':'20170301--4', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170301--5', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession) 
oneSession = {'subject':'d1pi023', 'session':'20170301--6', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)


oneSession = {'subject':'d1pi023', 'session':'20170303--1', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170303--2', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession) 
oneSession = {'subject':'d1pi023', 'session':'20170303--3', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi023', 'session':'20170303--4', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW
oneSession = {'subject':'d1pi023', 'session':'20170303--5', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession) 
oneSession = {'subject':'d1pi023', 'session':'20170303--6', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
allSessions.append(oneSession)

oneSession = {'subject':'d1pi023', 'session':'20170303--7', 'stimThreshold':20, 'stimSide':'left',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW

oneSession = {'subject':'d1pi023', 'session':'20170303--8', 'stimThreshold':20, 'stimSide':'right',
              'stimRegion':'frontStr', 'stimCoords':[ [[0,0], [0,0]] ]}
#allSessions.append(oneSession) # 0.5mW



'''
allSessions = [oneSession]
'''


'''
oneSession = {'subject':'', 'session':'', 'stimThreshold':,
         'stimCoords':}
allSessions.append(oneSession)
'''      

'''
# == Other sessions ==
oneSession = {'subject':'d1pi011', 'session':'20160609--3', 'stimThreshold':40, 'stimSide':'left,right,both',
              'stimRegion':'frontStr', 'stimCoords':[ [[275, 50], [290, 60]], [[530, 50], [545, 60]] ],
              'notes':'Bilateral stim'}
oneSession = {'subject':'d1pi013', 'session':'20160511--6', 'stimThreshold':40, 'stimSide':'left,right',
              'stimRegion':'frontStr', 'stimCoords':[ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ],
              'notes':'No color tape'}
oneSession = {'subject':'d1pi013', 'session':'20160511--10', 'stimThreshold':40, 'stimSide':'left,right',
              'stimRegion':'', 'stimCoords':[ [[280, 70], [300, 80]], [[535, 65], [550, 75]] ],
              'notes':'No color tape'}
'''



if not SAVE_ALL_TOGETHER:
    for indSession,oneSession in enumerate(allSessions): #allSessions: #[allSessions[16]]:
        #for indSession,oneSession in enumerate(allSessions[16:17]):
        subject = oneSession['subject']
        session = oneSession['session']
        stimCoords = oneSession['stimCoords']
        stimThreshold = oneSession['stimThreshold']
        stimSide = oneSession['stimSide']

        print '==== Processing {0} {1} ===='.format(subject,session)

        videoPath = settings.VIDEO_PATH
        filenameOnly = subject+'_'+session+'.mkv'
        filename = os.path.join(videoPath,subject,filenameOnly)

        stimFilename = 'stimtrack_{0}_{1}.npz'.format(subject,session)
        stimFullPath = os.path.join(outputDir,stimFilename)
        ctrackFilename = 'colortrack_{0}_{1}.npz'.format(subject,session)
        ctrackFullPath = os.path.join(outputDir,ctrackFilename)
        headangleFilename = 'head_angle_{0}_{1}.npz'.format(subject,session)
        headangleFullPath = os.path.join(outputDir,headangleFilename)


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
            plt.pause(0.05)

        if TRACK_COLORS:
            # -- These HSV color ranges were found by hand using the Linux gpick app --
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
            plt.subplot2grid([1,4],[0,0],colspan=3)
            plt.hold(1)
            plt.plot(vid.colorCenter[0,:,:].T,'.-')
            plt.plot(vid.colorCenter[1,:,:].T,'.-')
            plt.ylabel('X and Y position')
            plt.xlabel('Frame')
            plt.hold(0)
            plt.subplot2grid([1,4],[0,3],colspan=1)
            plt.hold(1)
            plt.plot(vid.colorCenter[0,0,:],vid.colorCenter[0,1,:],'.-',color='r')
            plt.plot(vid.colorCenter[1,0,:],vid.colorCenter[1,1,:],'.-',color='b')
            plt.hold(0)
            plt.show()
            plt.pause(0.05)

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

            # Note that arctan2 takes (y,x) and that headVector[1,:] columns
            headAngleDiscont = np.arctan2(headVector[0,:],headVector[1,:])
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
            totalDeltaAngleEachTrial = nStim*[None]

            for stimInd in range(nStim):
                firstFrameEachTrial[stimInd] = np.flatnonzero(dStim[stimInd,:]>0)
                lastFrameEachTrial[stimInd] = np.flatnonzero(dStim[stimInd,:]<0)

                nTrials = len(firstFrameEachTrial[stimInd])
                avgDeltaAngleEachTrial[stimInd] = np.empty(nTrials)
                totalDeltaAngleEachTrial[stimInd] = np.empty(nTrials)
                for indt in range(nTrials):
                    framesThisTrial = range(firstFrameEachTrial[stimInd][indt],
                                            lastFrameEachTrial[stimInd][indt])
                    avgDeltaAngleEachTrial[stimInd][indt] = np.mean(headDiff[framesThisTrial])
                    totalDeltaAngleEachTrial[stimInd][indt] = np.sum(headDiff[framesThisTrial])

            np.savez(headangleFullPath, subject=subject, session=session, headAngle=headAngle,
                     missedFrames=missedFrames, stimBool=stimBool, avgDeltaAngleEachTrial=avgDeltaAngleEachTrial,
                     totalDeltaAngleEachTrial=totalDeltaAngleEachTrial,
                     firstFrameEachTrial=firstFrameEachTrial, lastFrameEachTrial=lastFrameEachTrial,
                     stimSide=stimSide, script=scriptFullPath)
            print 'Saved results to {}'.format(headangleFullPath)


            plt.clf()
            plt.hold(1)

            ax1 = plt.subplot(2,1,1)
            plt.plot(headAngle,'.-')
            plt.ylabel('Head angle')
            ax2 = plt.subplot(2,1,2,sharex=ax1)
            plt.plot(stimIntensity.T,'.-')
            plt.ylabel('Stim')
            plt.show()
            plt.pause(0.05)

            print 'Delta angle during stimulation:'
            print deltaAngleStim1
            if nStim>1:
                print deltaAngleStim2
            print 'Delta angle no stims:'
            print deltaAngleNoStim

            print 'Delta angle each trial'
            print avgDeltaAngleEachTrial

        
if SAVE_ALL_TOGETHER:
    summaryFilename = 'head_angle_summary.npz'
    summaryFullPath = os.path.join(outputDir,summaryFilename)
    subjects = []
    sessions = []
    stimSides = []
    stimRegions = []
    deltaAngleEachTrialEachSession = []
    for indSession,oneSession in enumerate(allSessions):
        subject = oneSession['subject']
        session = oneSession['session']
        stimSide = oneSession['stimSide']
        stimRegion = oneSession['stimRegion']
        print '==== Loading data from {0} {1} ===='.format(subject,session)

        headangleFilename = 'head_angle_{0}_{1}.npz'.format(subject,session)
        headangleFullPath = os.path.join(outputDir,headangleFilename)

        haFile = np.load(headangleFullPath)

        avgDeltaAngleEachTrial = haFile['avgDeltaAngleEachTrial']
        totalDeltaAngleEachTrial = haFile['totalDeltaAngleEachTrial']
        stimLabels = stimSide.split(',')

        for indstim, oneStimLabel in enumerate(stimLabels):
            subjects.append(subject)
            sessions.append(session)
            stimSides.append(oneStimLabel)
            stimRegions.append(stimRegion)
            deltaAngleEachTrialEachSession.append(totalDeltaAngleEachTrial[indstim,:])

    np.savez(summaryFullPath, subject=subjects, session=sessions, stimSide=stimSides,
             stimRegion=stimRegions, deltaAngleEachTrial=deltaAngleEachTrialEachSession,
             script=scriptFullPath)
    print 'Saved results to {}'.format(summaryFullPath)
    
