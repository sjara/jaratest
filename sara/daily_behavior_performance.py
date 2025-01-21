'''
Check behavior performance of multiple animals (on each recorded session).

USAGE: 
python daily_behavior_performance.py
python daily_behavior_performance.py N_SESSIONS
(where N_SESSIONS is the number of session to load, starting from the last session)
'''

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings

# Create a list from sole048 to sole056 without a generator
subjects = ['sole048', 'sole049', 'sole050', 'sole051', 'sole052', 'sole053', 'sole054', 'sole055', 'sole056']
paradigm = '2afc'

# Get lastNsessions from command line argument
import sys
if len(sys.argv) > 1:
    lastNsessions = int(sys.argv[1])
else:
    lastNsessions = None

# -- Process data for each mouse --
summaryPerformance = {}
sessions = {}
for subject in subjects:
    summaryPerformance[subject] = pd.DataFrame(columns=['sessionID', 'nValid', 'nRewarded', 'rig'])

    # Find all session files for this subject
    behavDataPath = settings.BEHAVIOR_PATH
    subjectPath = os.path.join(behavDataPath, subject)
    sessionFiles = []
    if os.path.isdir(subjectPath):
        sessionFiles = os.listdir(subjectPath)
        sessionFiles = [f.split('_')[-1][:-3] for f in sessionFiles if f.endswith('.h5')]
        sessionFiles.sort()
    
    if lastNsessions is None:
        sessions[subject] = sessionFiles
    else:
        sessions[subject] = sessionFiles[-lastNsessions:]

    for indsession, session in enumerate(sessions[subject]):
        behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
        try:
            bdata = loadbehavior.BehaviorData(behavFile)
            nValid = bdata['nValid'][-1]
            nRewarded = bdata['nRewarded'][-1]
            rig = int(bdata.session['hostname'].split('jararig')[-1].replace("'", ""))
        except:
            print(f'\nERROR: Could not load session {session} for subject {subject}')
            nValid = np.nan
            nRewarded = np.nan
            rig = None
    
        summaryPerformance[subject] = summaryPerformance[subject].append({
            'sessionID': session,
            'nValid': nValid,
            'nRewarded': nRewarded,
            'rig': rig,
        }, ignore_index=True)
        
    print(f'\n--- {subject} ---')
    print(summaryPerformance[subject].iloc[::-1])
    
# -- Calculate average number of rewarded trials grouped by rig --
summaryPerformanceAll = pd.concat(summaryPerformance.values(), keys=subjects)
summaryPerformanceAll = summaryPerformanceAll.dropna()
summaryPerformanceAllGrouped = summaryPerformanceAll.drop(columns='sessionID').groupby('rig').mean()
print('\n=== Average performance per rig ===')
print(summaryPerformanceAllGrouped)
