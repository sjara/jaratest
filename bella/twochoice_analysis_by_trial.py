# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 12:54:55 2021

@author: isabe
"""


import numpy as np
import pandas as pd
import seaborn 
seaborn.set()
from jaratoolbox import behavioranalysis 
from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt  


subjects = [
            'chad055',
            'chad056',
            'chad057',
            'chad058'
            ]


paradigm = 'twochoice'
sessionsEachSubject = { 
    'chad055': ['20201212a', '20201213a'],
    'chad056': ['20201216a', '20201217a'],
    'chad057': ['20210104a','20210105a'],
    'chad058': [ '20201215a','20201216a']
    }

mouse_cumulative = {}
mouse_perf = {}
for subject in subjects: 
    sessions = sessionsEachSubject[subject]    
    bdata = behavioranalysis.load_many_sessions(subject,paradigm='twochoice',sessions=sessions)
        
    target_frequency = bdata['targetFrequency']
    ntrials = len(bdata['outcome'])
    trial_range = np.arange(0,ntrials)
    
    valid_choice = (bdata['choice'] != bdata.labels['choice']['none']).astype(int)
    nchoice = len(valid_choice)
    choice_range = np.arange(0,nchoice)
    
    
    choice = bdata['choice']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']
    valid_choice = (bdata['choice'] != bdata.labels['choice']['none']).astype(int)
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    
    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
    total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
    
    hit_outcome = ((bdata['outcome'] == bdata.labels['outcome']['hit']) & valid_choice).astype(int)
    misses = (bdata['outcome'] == bdata.labels['outcome']['miss']).astype(int)
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    left_errors = valid_left_trials & choice_right
    right_errors = valid_right_trials & choice_left
    total_errors = (right_errors + left_errors).astype(int)
    
    total_errors_right = bdata['nErrorsRight']
    total_licks_left = bdata['nLicksLeft']
    total_licks_right = bdata['nLicksRight']
    
    false_alarms_right = bdata['nFalseAlarmsRight']
    false_alarms_left = bdata['nFalseAlarmsLeft']
    false_alarms = (bdata['outcome'] == bdata.labels['outcome']['falseAlarm']).astype(int)
    missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
    misses_left = bdata['nMissesLeft']
    misses_right = bdata['nMissesRight']

    #because we are only interested in the choices the animal makes and not the entire trials I commented out information that is not needed for the analysis of valid choices. Kept it written because I  might need it for the future but you can ignore them for now. 
    trial_information = pd.DataFrame({'choice_range': choice_range,
                              'trial_range': trial_range,                        
                              'valid_choice': valid_choice,
                              'hits': hit_outcome,
                              'errors': total_errors,
                              'false_alarms': false_alarms,
                              'misses': misses,
                              'left_hits': left_hits,
                              'right_hits': right_hits
                              })
    
    trial_information['choice_bins'] = pd.cut(trial_information.choice_range,
                                             bins=pd.interval_range(start=0, end=3500, periods=5))    
    trial_information['trial_bins'] = pd.cut(trial_information.choice_range,
                                             bins=pd.interval_range(start=0, end=3500, periods=5)) 
     
    binned_trial_info = trial_information.groupby('trial_bins') .sum()
    binned_choice_info = trial_information.groupby('choice_bins') .sum()
    print(binned_trial_info.drop(['trial_range'], axis=1))
    print(subject)
    print(binned_choice_info.drop(['choice_range'], axis=1))
    print(nchoice)
    
    percent_correct = (binned_choice_info['hits']/ binned_choice_info['valid_choice']) * 100
   
    mouse_perf[subject] = pd.DataFrame({
                                        '%_correct': round(percent_correct, 2)
                                        })
    

    '''
#This plot shows the trials
  
    ax = binned_trial_info[['hits', 'errors', 'false_alarms', 'misses']].plot(kind='bar', figsize=(15, 10), legend=True, fontsize=20, color=('purple', 'green', 'orange', 'blue'))
    ax.set_xlabel("Trial number", fontsize=18)
    plt.xticks(rotation=0)
    ax.set_ylabel("Amount of hits, errors, or false alarms", fontsize=18)
    plt.title('Mouse: {} ; Session Date: {}'.format(subject, session), fontsize=20)
    ax.legend(fontsize=18)
    plt.show()
    '''
    '''
#This plot shows only the valid choices and is most relevant to our analysis. 
    bx = percent_correct.plot(kind='bar', figsize=(15, 10), legend=True, fontsize=20,)
    bx.set_xlabel("{} Trials".format(nchoice), fontsize=18)
    plt.xticks(rotation=0)
    plt.ylim([0,100])
    bx.set_ylabel("Percent Correct (%)", fontsize=18)
    plt.title('Mouse: {} ; Session Date: {}'.format(subject, sessions), fontsize=20)
    #bx.legend(fontsize=18)
    plt.show()
    '''
#Lines below calculate and graph the cumulative sum outcomes by trial which  give us a better idea of how the animal performs 
    cumulative_sum = pd.DataFrame({'choice_trials': valid_choice,
                              'trial_range': trial_range,    
                              'hits': hit_outcome,
                              'errors': total_errors,
                              'false_alarms': false_alarms,
                              'misses': misses
                              })
    
    cumulative_sum['sum_hits'] = cumulative_sum.hits.cumsum()
    cumulative_sum['sum_errors'] = cumulative_sum.errors.cumsum()
    cumulative_sum['sum_false_alarms'] = cumulative_sum.false_alarms.cumsum()
    cumulative_sum['sum_misses'] = cumulative_sum.misses.cumsum()
    cumulative_sum['sum_choices'] = cumulative_sum.choice_trials.cumsum()
    
    mouse_cumulative[subject]= pd.DataFrame({'hits':cumulative_sum['sum_hits'],
                                      'errors':cumulative_sum['sum_errors']})

    
'''

#plots the cumulative number of hits/ choice trial 
    #plt.scatter(choice_range, cumulative_sum['sum'], color = 'blue')
    plt.plot(trial_range, cumulative_sum['sum_hits'], color = 'blue', label = 'Hits')
    plt.plot(trial_range, cumulative_sum['sum_errors'], color = 'red', label = 'Errors')
    #plt.plot(trial_range, cumulative_sum['sum_choices'], color = 'pink', label = 'Choice')
    #plt.plot(choice_range, cumulative_sum['sum_false_alarms'], color = 'orange', label = 'False Alarms')
    plt.plot(trial_range, cumulative_sum['sum_misses'], color = 'green', label = 'Misses')
    plt.title('{} choices on {} '.format(subject, sessions))
    plt.xlabel('Trial #')
    plt.ylabel('Cumulative Trial Outcome')
    plt.legend(loc = 0)
    #plt.savefig('{}_{}.png'.format(subject,sessions), dpi=300)
    #plt.ylim(0, 2000)
    plt.show() 
'''
    
'''
chad055 = mouse_cumulative['chad055']
chad056 = mouse_cumulative['chad056']
chad057 = mouse_cumulative['chad057']
chad058 = mouse_cumulative['chad058']

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)


#Plot is used to graph the all of the animals, notice how you have to add each mouse. Will fix this later
ax1.plot(chad055['hits'], color = 'red', label='Hits')
ax1.plot(chad055['errors'], 'r--', label = 'Errors')
ax1.plot(chad056['hits'], color ='g')
ax1.plot(chad056['errors'],'g--')
ax1.plot(chad057['hits'], color ='c')
ax1.plot(chad057['errors'],'c--')
ax1.plot(chad058['hits'],color = 'm')
ax1.plot(chad058['errors'],'m--')
ax1.legend(loc='upper left', frameon=False)
ax1.set_xlabel('Trials')
ax1.set_ylabel('Cumulative Hits')
#fig1.savefig('average_cumhits.png'.format(subject,sessions), dpi=300)
'''
