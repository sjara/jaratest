'''
Check behavior performance of multiple animals (on each recorded session),
and save an HTML table with the summary.
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings

# -- Define subjects and sessions --
subjects = ['sole021', 'sole022']  # Replace with your subject IDs
# sessions = []  # They are automatically read from the data folder
paradigm = '2afc'

# -- Process data for each mouse --
mouse_perf = {}
for subject in subjects:
    # Find all session files for this subject
    behavDataPath = settings.BEHAVIOR_PATH
    subjectPath = os.path.join(behavDataPath, subject)
    sessionFiles = []
    if os.path.isdir(subjectPath):
        sessionFiles = os.listdir(subjectPath)
        sessionFiles = [f.split('_')[-1][:-3] for f in sessionFiles if f.endswith('.h5')]
        sessionFiles.sort()
    
    # Store sessions for this subject
    sessions[subject] = sessionFiles
    # Load behavior data for all sessions
    bdata = behavioranalysis.load_many_sessions(subject, paradigm=paradigm, 
                                                sessions=sessions[subject])
    
    # Extract relevant behavioral metrics
    sessionID = bdata['sessionID'] + 1
    nValid = bdata['nValid']
    nRewarded = bdata['nRewarded']
    
    # Create DataFrame with trial information
    df_trial_information = pd.DataFrame({
        'sessionID': sessionID,
        'nValid': nValid,
        'nRewarded': nRewarded,
    })
    
    # Group by session to get summary statistics
    df_session_information = df_trial_information.groupby(by=['sessionID']).sum()
    
    # Create performance summary DataFrame
    mouse_perf[subject] = pd.DataFrame({
        'session': sessions[subject],
        'nValid': df_session_information['nValid'].astype(int),
        'nRewarded': df_session_information['nRewarded'].astype(int),
        'performance': (df_session_information['nRewarded'] / 
                       df_session_information['nValid'] * 100).round(1)
    })
    
    print(f'\nPerformance summary for {subject}:')
    print(mouse_perf[subject])
    
    # Save to HTML
    output_file = f'/tmp/behavior_performance_{subject}.html'
    extraplots.dataframe_to_html(mouse_perf[subject].iloc[::-1], output_file)
    print(f'Saved performance report to: {output_file}')



