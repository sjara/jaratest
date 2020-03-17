import os
import numpy as np

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

# figname =
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]
    

laserAccuracy = []
controlAccuracy = []

laserBias = []
controlBias = []

for indType, mice in enumerate(mouseType):
    
    thisLaserAccuracy = np.zeros(len(mice))
    thisControlAccuracy = np.zeros_like(thisLaserAccuracy)
        
    thisLaserBias = np.zeros_like(thisLaserAccuracy)
    thisControlBias = np.zeros_like(thisLaserAccuracy)
    
    for indMouse, mouse in enumerate(mice):
        
        laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)
        
        trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], np.unique(laserBehavData['laserSide']))
        
        # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome']==laserBehavData.labels['outcome']['correct']
        
        laserValid = valid[trialsEachLaser[:,1]]
        laserCorrect = correct[trialsEachLaser[:,1]]
            
        thisLaserAccuracy[indMouse] = 100.0*np.sum(laserCorrect)/np.sum(laserValid)
        
        controlValid = valid[trialsEachLaser[:,0]]
        controlCorrect = correct[trialsEachLaser[:,0]]
            
        thisControlAccuracy[indMouse] = 100.0*np.sum(controlCorrect)/np.sum(controlValid)
        
        # -- compute bias to a side as difference/sum --
        left = laserBehavData['choice']==laserBehavData.labels['choice']['left']
        right = laserBehavData['choice']==laserBehavData.labels['choice']['right']
         
        laserLeft = left[trialsEachLaser[:,1]]
        laserRight = right[trialsEachLaser[:,1]]
        
        thisLaserBias[indMouse] = 1.0*(np.sum(laserRight)-np.sum(laserLeft))/(np.sum(laserRight)+np.sum(laserLeft))
        
        controlLeft = left[trialsEachLaser[:,0]]
        controlRight = right[trialsEachLaser[:,0]]
        
        thisControlBias[indMouse] = 1.0*(np.sum(controlRight)-np.sum(controlLeft))/(np.sum(controlRight)+np.sum(controlLeft))
        
    laserAccuracy.append(thisLaserAccuracy)
    controlAccuracy.append(thisControlAccuracy)
    
    laserBias.append(thisLaserBias)
    controlBias.append(thisControlBias)
    
    