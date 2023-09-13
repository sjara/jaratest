"""
Generates a 3d numpy array of running data.


Saves array of:
array[0]: date (typ: string) 
array[1]: reagent (typ: string)
array[2]: HighFreq trials (type: array of bool)
array[3]: LowFreq trials (type: array of bool)
array[4]: FM_Down trials (type: array of bool)
array[5]: FM_Up trials (type: array of bool)


If there are fewer sync light trials than behavior trials after sync light corrections, script assumes the missing trials are from the 
end of the video. Script adds missing trials and marks them as True when selecting for nonrunning trials (before trials are inverted) 
and False when selecting for running trials. This, in effect, removes the additional trials.

"""


import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import facemapanalysis
from jaratoolbox import celldatabase
from jaratoolbox import loadbehavior
import oddball_analysis_functions as odbl
from jaratoolbox import settings
from importlib import reload
import studyparams
reload(facemapanalysis)

#def main(runOrNon):

#equalArraySize = True

runOrNon = 'non' #enter 'run' or 'non'

subjects = ['acid006']
#subjects = studyparams.SUBJECTS
for subject in subjects:

    proc_dir = os.path.join(settings.VIDEO_PATH, f'{subject}_processed')
    behav_dir = os.path.join(settings.BEHAVIOR_PATH, f'{subject}/')

    inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
    inforec = celldatabase.read_inforec(inforecFile)
    
    #dbFilename = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, f'celldb_{subject}.h5')
    #celldb = celldatabase.load_hdf(dbFilename)
    

    #filename = '/home/jarauser/Max/allAcidCombined.h5'
    #celldb = celldatabase.load_hdf(filename)

    #celldb = celldb.query("date == '2023-03-22'")

    syncDate = studyparams.SYNC_LIGHT_DATE #date when pre/post light was added

    reagents = studyparams.REAGENTS


    
    dates = []
    for indExpriment, experiment in enumerate(inforec.experiments):
        dates.append(inforec.experiments[indExpriment].date)

    #dates = celldb['date'].unique()

    
    data = []
    videoSuffix = ''
    session_numbers = ["01", "02", "03", "04"]

    """
    running_each_trial_list = {'pre': [], 'saline': [], 'doi': []}
    running_count_each_trial = {'pre': [], 'saline': [], 'doi': []}
    sync_light_count = {'pre': [], 'saline': [], 'doi': []}
    date_list = []
    sessionType_list = []
    injection_list = []
    """

    running_each_trial_list = {'01': [], '02': [], '03': [], '04': []}
    running_count_each_trial = {'01': [], '02': [], '03': [], '04': []}
    sync_light_count = {'01': [], '02': [], '03': [], '04': []}
    date_list = []
    sessionType_list = []
    injection_list = []


    brokenList = []
    ################################

    for date in dates:
        for index, reagent in enumerate(reagents):
        #for session_number in session_numbers:
            injection_list.append(reagent)
            date_list.append(date)
            #sessionType_list.append(session_number)
            #row_data = {'date':dates, 'experiment':session_number}

            for session_number in session_numbers:
            #for reagent in reagents:
                dateFix = date.replace('-','')
                proc_filename = f'{subject}_oddball_sequence_{dateFix}_{session_number}{reagent}_proc.npy'

                proc = np.load(os.path.join(proc_dir,proc_filename), allow_pickle=True).item()
                pixchange = proc['pixelchange'][0]  # A dict inside a 1-item list, so you need to get the first element
                # Check if sync light 'blink' exists.
                if proc['blink']:
                    sync_light = proc['blink'][0]  # A dict inside a 1-item list, so you need to get the first element

                    if dateFix >= syncDate: #date when pre/post light was added
                        # -- Find onsets of sync light --
                        sync_light_onset = odbl.find_sync_light_onsets(sync_light, fixmissing=True, prepost=True)
                    else:
                        sync_light_onset = odbl.find_sync_light_onsets(sync_light, fixmissing=True, prepost=False) 

                    # -- Estimate running on each trial --
                    running_threshold = 3
                    running_each_trial, running_trace_smooth = facemapanalysis.estimate_running_each_trial(pixchange,
                    sync_light_onset, smoothsize=10, presamples=4, threshold=running_threshold)

                    if session_number == '01':
                        videoSuffix = 'a'
                    if session_number == '02':
                        videoSuffix = 'b'
                    if session_number == '03':
                        videoSuffix = 'c'
                    if session_number == '04':
                        videoSuffix = 'd'

                    behavfilename = f'{behav_dir}{subject}_oddball_sequence_{dateFix}{videoSuffix}{reagent}.h5'
                    behaviorData = loadbehavior.BehaviorData(behavfilename)
                    bdataTrialCount = len(behaviorData['currentStartFreq'])

                
                
                    # Check for 1 extra sync light trial and remove it if present.

                    if len(running_each_trial) == bdataTrialCount+1:
                        running_each_trial = running_each_trial[:bdataTrialCount]

                
                    if runOrNon == 'run':
                        # Checks for mismatch between trial count from sync light and behavior. If missing trials are present,
                        # assumes missing trials are from end of video and marks trials as TRUE for running.
                        if len(running_each_trial) < bdataTrialCount:
                            lengthDiff = bdataTrialCount - len(running_each_trial)
                            for missingTrial in range(lengthDiff):
                                running_each_trial = np.append(running_each_trial, False)

                    elif runOrNon == 'non':
                        # Checks for mismatch between trial count from sync light and behavior. If missing trials are present,
                        # assumes missing trials are from end of video and marks trials as TRUE for running.
                        if len(running_each_trial) < bdataTrialCount:
                            lengthDiff = bdataTrialCount - len(running_each_trial)
                            for missingTrial in range(lengthDiff):
                                running_each_trial = np.append(running_each_trial, True)
                        running_each_trial = ~running_each_trial
                    else:
                        print('select whether to get the trials for running or nonrunning')
                        exit()
                
                
                    """
                # Due to the way 'celldatabase.save_hdf()' function works, length of runningArray for each cell has to be the 
                    # same length for vstack. This function checks if length of array is above '501' and removes the excess trials if so.
                    if equalArraySize == True:
                        if len(running_each_trial) > 501:
                            lengthDiff = len(running_each_trial) - 501
                            running_each_trial = running_each_trial[:len(running_each_trial)-lengthDiff]

                    #if len(running_each_trial) != len(behavior['currentStartFreq']):
                    #    brokenList.append(behavfilename)

                
                    """

                    if len(running_each_trial) != bdataTrialCount:
                        brokenList.append(behavfilename)

                    # Append values to the initialized lists in dictionaries
                    running_each_trial_list[session_number].append(running_each_trial)
                    running_count_each_trial[session_number].append(sum(running_each_trial))
                    sync_light_count[session_number].append(sum(sync_light_onset))

                else:
                    # no sync light detected. Fill this index with empty data.
                    print(f'no sync light detected in proc file for {subject}_{date}')
                    running_each_trial_list[session_number].append([0])
                    running_count_each_trial[session_number].append(0)
                    sync_light_count[session_number].append(-1)
                """
                    # Append values to the initialized lists in dictionaries
                    running_each_trial_list[reagent].append(running_each_trial.astype(np.int))
                    running_count_each_trial[reagent].append(sum(running_each_trial))
                    sync_light_count[reagent].append(sum(sync_light_onset))

                else:
                    # no sync light detected. Fill this index with empty data.
                    print(f'no sync light detected in proc file for {subject}_{date}')
                    running_each_trial_list[reagent].append([0])
                    running_count_each_trial[reagent].append(0)
                    sync_light_count[reagent].append(0)

                """
                #row_data[f'{injection_type}_running_trial_count'] =  sum(running_each_trial)
                #row_data[f'{injection_type}_runningBooleanArray'] = running_each_trial

            #data.append(row_data)

    """
    runningDataFrame = pd.DataFrame({
        'date': date_list,
        'experiment': sessionType_list,
        'pre_running_trial_count': running_count_each_trial['pre'],
        'saline_running_trial_count': running_count_each_trial['saline'],
        'doi_running_trial_count': running_count_each_trial['doi'],
        'pre_running_array': running_each_trial_list['pre'],
        'saline_running_array': running_each_trial_list['saline'],
        'doi_running_array': running_each_trial_list['doi']
    })
    """
    runningArray = np.array([date_list,injection_list,running_each_trial_list['01'],running_each_trial_list['02'],running_each_trial_list['03'],running_each_trial_list['04']])

    for list in brokenList:
        print(f'{list}')

    newdbDir = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
    #newdbFilename = os.path.join(newdbDir, f'{subject}_runningBooleanDB.h5')

    if runOrNon == 'run':
        othername = os.path.join(newdbDir, f'{subject}_runningBooleanArrayRun')
    if runOrNon == 'non':
        othername = os.path.join(newdbDir, f'{subject}_runningBooleanArrayNon')
    #celldatabase.save_hdf(runningDataFrame, newdbFilename)
    np.save(othername, runningArray)
    print(f'saved file to {othername}')


"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_database.py 'run' or 'nonrun' ")
    else:
        argument = sys.argv[1]
        if argument != 'run' and argument != 'nonrun':
            print("Usage: python generate_database.py 'run' or 'nonrun' ")
        else:
            main(argument)
"""