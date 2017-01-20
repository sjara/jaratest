'''
Script to generate examples of change in head-angle after stimulation outside of the task.

You first need to create head_angle_SUBJECT_SESSION.npz files using script:
generate_summary_photostim_outside_task.py
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

paneldataFilename = 'example_photostim_outside_task.npz'
paneldataFullPath = os.path.join(outputDir,paneldataFilename)

allSessions = []
allSessions.append({'subject':'d1pi013', 'session':'20160519-5', 'stimRegion':'frontStr',
                    'sampleRangeLeft':[1050,1250], 'sampleRangeRight':[916,1116], 'offset':-4})
allSessions.append({'subject':'d1pi013', 'session':'20160523--6', 'stimRegion':'backStr',
                    'sampleRangeLeft':[661,861], 'sampleRangeRight':[493,693], 'offset':3})
stimSamples = [73,109] ### HARDCODED: this is the time of the stimulus in the chosen range

#[910,1250]
#[487,850]

plt.clf()
ax1 = plt.subplot(2,2,1)
plt.hold(1)
plt.ylabel('Head angle')
ax2 = plt.subplot(2,2,3,sharex=ax1)
plt.hold(1)
plt.ylabel('Stim')
ax3 = plt.subplot(2,2,2)
plt.hold(1)
plt.ylabel('Head angle')
ax4 = plt.subplot(2,2,4,sharex=ax3)
plt.hold(1)
plt.ylabel('Stim')

headAngleEachCond = []
stimBoolEachCond = []
stimSideEachCond = []
stimRegionEachCond = []
for inds,oneSession in enumerate(allSessions):
    subject = oneSession['subject']
    session = oneSession['session']
    sampleRangeLeft = oneSession['sampleRangeLeft']
    sampleRangeRight = oneSession['sampleRangeRight']
    samplesLeft = range(*sampleRangeLeft)
    samplesRight = range(*sampleRangeRight)
    headangleFilename = 'head_angle_{0}_{1}.npz'.format(subject,session)
    headangleFullPath = os.path.join(outputDir,headangleFilename)
    
    haFile = np.load(headangleFullPath)
    headAngle = haFile['headAngle']
    stimBool = haFile['stimBool']
    headAngleEachCond.append(headAngle[samplesLeft]-oneSession['offset'])
    stimBoolEachCond.append(stimBool[:,samplesLeft])
    stimSideEachCond.append('left')
    stimRegionEachCond.append(oneSession['stimRegion'])

    headAngleEachCond.append(headAngle[samplesRight]-oneSession['offset'])
    stimBoolEachCond.append(stimBool[:,samplesRight])
    stimSideEachCond.append('right')
    stimRegionEachCond.append(oneSession['stimRegion'])

    SHOW_FULLSESSION = 0
    if SHOW_FULLSESSION:
        plt.clf()
        plt.hold(1)
        ax1 = plt.subplot(2,1,1)
        plt.plot(headAngle,'.-')
        plt.ylabel('Head angle')
        ax2 = plt.subplot(2,1,2,sharex=ax1)
        plt.plot(stimBool.T,'.-')
        plt.ylabel('Stim')
        plt.show()
        plt.waitforbuttonpress()

stimSideEachCond = np.array(stimSideEachCond)
stimRegionEachCond = np.array(stimRegionEachCond)

plt.axes(ax1)
thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='frontStr'))[0]
plt.plot(headAngleEachCond[thisCond],'.-')
thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='backStr'))[0]
plt.plot(headAngleEachCond[thisCond],'.-')

plt.axes(ax2)
thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='frontStr'))[0]
plt.plot(stimBoolEachCond[thisCond][0,:],'.-')
thisCond = np.flatnonzero((stimSideEachCond=='left') & (stimRegionEachCond=='backStr'))[0]
plt.plot(stimBoolEachCond[thisCond][0,:],'.-')

plt.axes(ax3)
thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='frontStr'))[0]
plt.plot(headAngleEachCond[thisCond],'.-')
thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='backStr'))[0]
plt.plot(headAngleEachCond[thisCond],'.-')

plt.axes(ax4)
thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='frontStr'))[0]
plt.plot(stimBoolEachCond[thisCond][1,:],'.-')
thisCond = np.flatnonzero((stimSideEachCond=='right') & (stimRegionEachCond=='backStr'))[0]
plt.plot(stimBoolEachCond[thisCond][1,:],'.-')

plt.show()


np.savez(paneldataFullPath, allSessions=allSessions, stimSamples=stimSamples,
         stimSideEachCond=stimSideEachCond, stimRegionEachCond=stimRegionEachCond,
         headAngleEachCond=headAngleEachCond, stimBoolEachCond=stimBoolEachCond,
         script=scriptFullPath)
print 'Saved results to {}'.format(paneldataFullPath)


