# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:39:25 2020

@author: isabe
"""


import numpy as np
import pandas as pd
#from jaratoolbox import extraplots
import matplotlib.pyplot as plt 
#from statsmodels.stats.proportion import proportion_confint
#import sys
from jaratoolbox import behavioranalysis 
#from jaratoolbox import settings 
#from scipy.stats import norm

#Add the dates you want to look at. 
subject = 'chad055'
#subject = 'chad056'
#subject = 'chad057'
#subject = 'chad058'
#subject = 'chad059'
paradigm = 'twochoice'

sessions = [ '20201206a', '20201207a', '20201208a', '20201209a', '20201210a', '20201211a']

bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)

sessionID = bdata['sessionID'] 
unique_sessionID = np.unique(sessionID) + 1
task_mode = bdata['taskMode']
lick_after_stim = bdata['taskMode'] == bdata.labels['taskMode']['lick_after_stim']
water_on_sound = bdata['taskMode'] == bdata.labels['taskMode']['water_on_sound']
discriminate_stim = bdata['taskMode'] == bdata.labels['taskMode']['discriminate_stim']

choice = bdata['choice']
choice_left = bdata['choice'] == bdata.labels['choice']['left']
choice_right = bdata['choice'] == bdata.labels['choice']['right']
valid_choice = bdata['choice'] != bdata.labels['choice']['none']
no_choice = bdata['choice'] == bdata.labels['choice']['none']

valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])

hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']
left_hits = valid_left_trials & choice_left 
right_hits = valid_right_trials & choice_right
left_errors = valid_left_trials & choice_right
right_errors = valid_right_trials & choice_left
total_errors = right_errors + left_errors


total_licks_left = bdata['nLicksLeft']
total_licks_right = bdata['nLicksRight']

false_alarms_right = bdata['nFalseAlarmsRight']
false_alarms_left = bdata['nFalseAlarmsLeft']
missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
misses_left = bdata['nMissesLeft']
misses_right = bdata['nMissesRight']


# Dataframe below collects the information needed for each trial. 
df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                     'hit_outcome': hit_outcome,
                                     'right_hits': right_hits,
                                     'left_hits': left_hits,
                                     'total_licks_left': total_licks_left,
                                     'total_licks_right': total_licks_right,
                                     'right_errors': right_errors,
                                     'left_errors': left_errors,
                                     'total_errors': total_errors,
                                     'false_alarms_left': false_alarms_left,
                                     'false_alarms_right' : false_alarms_right,
                                     'misses_left' : misses_left,
                                     'misses_right': misses_right,
                                     'total_misses' : missed_outcomes,
                                     'left_choice': choice_left,
                                     'right_choice': choice_right,
                                     'valid_left_trials': valid_left_trials,
                                     'valid_right_trials': valid_right_trials,
                                     'valid_choice': valid_choice,
                                     'total_left_trials': total_left_trials,
                                     'total_right_trials': total_right_trials
                                     })

#Use this groupby to gather the data that should be summed per session
df_session_information = df_trial_information.groupby(by = ['sessionID']) .sum()

#Use this groupby to gather the information that should be maxed per session
stage_one_information = df_trial_information.groupby(by =['sessionID']) .max()

#Used to calculate performance
percent_correct = ((df_session_information['hit_outcome']) /df_session_information['valid_choice'] *100)
left_performance = ((df_session_information['left_hits'] / df_session_information['valid_left_trials']) *100)
right_performance = ((df_session_information['right_hits'] / df_session_information['valid_right_trials']) *100)
mean_side_performance = ((left_performance + right_performance)/ 2 )
df_overall_performance = pd.DataFrame({'percent_correct': percent_correct,
                                       'left_performance': left_performance,
                                       'right_performance': right_performance,
                                       'mean_side_performance' : mean_side_performance,
                                       })
#used to identify task mode per session
df_id_reward_mode = pd.DataFrame({'sessionID': sessionID,
                                     'task_mode' : task_mode,
                                     'lick_after_stim': lick_after_stim,
                                     'water_on_sound': water_on_sound,
                                     'discriminate_stim': discriminate_stim
                                     })

print(subject)

#prints the session ID, task mode, and number of trials. 
print(df_id_reward_mode.groupby(['sessionID', 'task_mode']).size())

#prints the specific response information of each session  
print(df_session_information[['total_left_trials', 'total_right_trials']])
print(stage_one_information[['total_licks_left', 'total_licks_right']])
print(df_session_information[['left_hits', 'right_hits','left_errors', 'right_errors']])
print(stage_one_information[['false_alarms_left', 'false_alarms_right', 'misses_left', 'misses_right']])

#prints the performance of the animal in each session 
print(df_overall_performance[['left_performance', 'right_performance', 'percent_correct']])

#plots the correct performance and how the animal performed with each side. Reminder that stage 1 will not be printed.
plt.scatter(unique_sessionID, left_performance, color = 'blue', label = 'Left')
plt.plot(unique_sessionID, left_performance, color = 'blue')
plt.scatter(unique_sessionID, right_performance, color = 'red' , label = 'Right')
plt.plot(unique_sessionID, right_performance, color = 'red')
plt.scatter(unique_sessionID, percent_correct, color = 'black', label = 'Percent Correct')
plt.title(subject + 'Performance')
plt.xlabel('session')
plt.ylabel('Percent animal correctly chose left/Right (%)')
plt.legend(loc = 3)
plt.xticks(ticks=unique_sessionID)
plt.ylim(0, 100)
plt.show() 
