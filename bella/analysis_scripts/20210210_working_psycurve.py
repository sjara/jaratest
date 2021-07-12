# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 18:16:00 2020

@author: isabe
"""

import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt 
from jaratoolbox import behavioranalysis 


subject = 'chad057'

#You can use the multiple sessions to average across the days. 
sessions = [#'20210105a',
            #'20210106a',
            #'20210107a',
            #'20210108a',
            #'20210120a',
            #'20210203a',
            ]


paradigm = 'twochoice'

bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)


#setting up the variables I will be looking at
sessionID = bdata['sessionID']
unique_sessionID = np.unique(sessionID) + 1


target_frequency = bdata['targetFrequency']
frequency_presented = np.unique(target_frequency)
response = bdata['choice']
valid_choice = response != bdata.labels['choice']['none']
choice_left = bdata['choice'] == bdata.labels['choice']['left']
choice_right = bdata['choice'] == bdata.labels['choice']['right']
valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
no_choice = response==bdata.labels['choice']['none']
left_errors = valid_left_trials & choice_right
right_errors = valid_right_trials & choice_left
total_errors = right_errors + left_errors


hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']


#this makes a table that has all the trials and the information/ responses for each 
df_each_trial = pd.DataFrame({'target_frequency': target_frequency,
                              'sessionID' : sessionID,
                              'choice_right': choice_right,
                              'choice_left': choice_left,
                              'valid_choice': valid_choice,
                              'response': response,
                              'no_choice': no_choice,
                              'hit_outcome': hit_outcome,
                              'total_errors': total_errors,                              
                              })

#grouping by session ant target frequency 
group_session_frequency = df_each_trial.groupby(['sessionID','target_frequency']).sum() #sum function
#Extracting out of group_session_frequency to get the percent of right choices
percent_right = ((group_session_frequency['choice_right']) / (group_session_frequency['valid_choice']) * 100)
mean_percent_by_session = percent_right.groupby(['target_frequency']).mean()

#Similar to what is done above I use group session frequency to get the percent correct
percent_correct = ((group_session_frequency['hit_outcome']) /group_session_frequency['valid_choice'] *100)
#frequency_hits = group_session_frequency['hit_outcome']
#frequency_errors = group_session_frequency['total_errors']

#Print statement are so that I can quickly see what is going on with the data
print(group_session_frequency[['hit_outcome', 'total_errors']])
print(percent_correct)
print(percent_right)

#plotting the figure
fig1, ax1 = plt.subplots()
ax1.plot(frequency_presented, mean_percent_by_session)
ax1.set_xscale('log')
ax1.set_xticks([6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_ylim([0, 100])
ax1.set_xlabel('Frequency Presented (Hz)')
ax1.set_ylabel('Percent Response Right (%)')
ax1.set_title('{} Session date: {}' .format(subject, sessions))
ax1.scatter(frequency_presented, mean_percent_by_session, color = 'r')



#Below is for individual day psycurves 
'''
session = '20201005a'
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)


#Below is to give me the psycurve 


#setting up the variables
target_frequency = bdata['targetFrequency']
frequency_presented = np.unique(target_frequency)
response = bdata['choice']
valid_choice = response != bdata.labels['choice']['none']
response_right = response==bdata.labels['choice']['right']
response_left = response==bdata.labels['choice']['left']
no_response = response==bdata.labels['choice']['none']


#this makes a table that has all the trials and the information/ responses for each 
df_each_trial = pd.DataFrame({'target_frequency': target_frequency,
                   'response_right': response_right,
                   'response_left': response_left,
                   'valid_choice': valid_choice,
                   'response': response,
                   'no_response': no_response}, columns=['target_frequency', 'valid_choice', 'response_right', ' response_left', 'no_response'])

df_by_frequency = df_each_trial.groupby(by = ['target_frequency']) .sum()

df_prcnt_right_response = ((df_by_frequency['response_right']) / (df_by_frequency['valid_choice']) * 100)

                                     
#sepparating out responses to each frequency
mean_response_right = df_by_frequency[('response_right')] 

#plotting the figure
fig1, ax1 = plt.subplots()
ax1.plot(frequency_presented, df_prcnt_right_response)
ax1.set_xscale('log')
ax1.set_xticks([6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_ylim([0, 100])
ax1.set_xlabel('Frequency Presented (Hz)')
ax1.set_ylabel('Percent Response Right (%)')
ax1.set_title('{} Session date: {}' .format(subject, session))
ax1.scatter(frequency_presented, df_prcnt_right_response, color = 'r') 
'''
