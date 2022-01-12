#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:36:26 2021

@author: angelicamejia
"""

import numpy as np
import pandas as pd
import seaborn 
seaborn.set()
import matplotlib.pyplot as plt 
#import sys
from jaratoolbox import behavioranalysis 
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings

subjects = [
            'amod015',
            # 'amod016',
            'amod017',
            'amod018',
            'amod019',
            'amod020',
            ]
            
sessions = { 
    
    'amod015': ['20211101a', '20211102a', '20211103a', '20211104a', '20211105a',
                '20211106a', '20211107a', '20211108a', '20211109a', '20211111a',
                '20211112a', '20211113a', '20211114a', '20211115a', '20211116a', 
                '20211117a', '20211118a', '20211119a'
                #Stage 4.0
                # '20211120a', '20211121a', 
                # '20211122a', '20211123a', '20211130a', '20211202a', '20211203a', 
                # '20211204a', '20211205a', '20211206a', '20211207a', '20211208a', 
                # '20211209a', '20211210a'
                ],
                
    'amod016': ['20211101a', '20211102a', '20211103a', '20211104a', '20211105a',
                '20211106a', '20211107a', '20211108a', '20211109a', '20211111a', 
                '20211112a', '20211113a', '20211114a', '20211115a', '20211116a', 
                '20211117a', '20211118a', '20211119a', '20211120a', '20211121a', 
                '20211122a', '20211123a', '20211130a', '20211201a', '20211202a', 
                '20211203a', '20211204a', '20211205a', '20211206a', '20211207a', 
                '20211208a', '20211209a', '20211210a'],
                
    'amod017': ['20211101a', '20211102a', '20211103a', '20211104a', '20211105a',
                '20211106a', '20211107a', '20211108a', '20211109a', '20211111a', 
                '20211112a', '20211113a', '20211114a', '20211115a', '20211116a', 
                '20211117a', '20211118a', '20211119a', '20211120a', '20211121a', 
                '20211122a', '20211123a', '20211130a', '20211201a', '20211202a', 
                '20211203a', '20211204a', 
                # Stage 4.0
                # '20211205a', '20211206a','20211207a', 
                # '20211208a', '20211209a', '20211210a', '20211211a', '20211212a', 
                # '20211214a', '20211215a', '20211216a', '20211217a', 
                # '20211218a', '20211219a'
                ],
    
    'amod018': ['20211101a', '20211103a', '20211104a', '20211105a', '20211106a',
                '20211107a', '20211108a', '20211110a', '20211111a', '20211112a', 
                '20211113a', '20211114a', '20211116a', '20211117a', '20211118a', 
                '20211119a', '20211120a', '20211121a', '20211122a', '20211123a', 
                '20211130a', '20211201a', '20211202a', '20211203a',  '20211204a', 
                '20211205a', '20211206a', 
                # Stage 4.0
                # '20211207a', '20211208a', '20211209a', 
                # '20211210a', '20211211a', '20211212a', 
                # '20211214a', '20211215a', '20211216a', '20211217a', 
                # '20211218a', '20211219a'
                ],
    
    'amod019': ['20211101a', '20211102a', '20211103a', '20211104a', '20211105a',
                '20211106a', '20211107a', '20211108a', '20211110a', '20211111a', 
                '20211112a', '20211113a', '20211114a', '20211116a', '20211117a', 
                # Stage 4.0
                # '20211118a', '20211119a', '20211120a', '20211121a', '20211122a', 
                # '20211123a', '20211130a', '20211201a', '20211202a', '20211203a', 
                # '20211204a', '20211205a', '20211206a', '20211207a', '20211208a', '20211209a'
            
                ],
    
    'amod020': [
                '20211101a', '20211102a', '20211103a', '20211104a', '20211105a',
                '20211106a', '20211107a', '20211108a', '20211110a', '20211111a', 
                '20211112a', '20211113a', '20211114a', 
                '20211115a', '20211116a', 
                # Stage 4.0
                # '20211117a', '20211118a',
                # '20211120a', '20211121a',  '20211122a', '20211123a', '20211130a', 
                # '20211201a', '20211202a', '20211203a',  '20211204a', '20211205a', 
                # '20211206a', '20211207a', '20211208a', '20211209a', '20211210a'
                ],

    }

paradigm = '2afc'

mouse_perf = {}
for subject in subjects:  
    session = sessions[subject]    
    bdata = behavioranalysis.load_many_sessions(subject,paradigm=paradigm,sessions=session)
    
    sessionID = bdata['sessionID'] + 1
    #unique_sessionID = np.unique(sessionID)
    valid = bdata['valid']
    # valid_left = bdata['valid'] == 1 & bdata['rewardSide'] == 0
    # valid_right = bdata['valid'] == 1 & bdata['rewardSide'] == 1
    # nRewarded = bdata['outcome'] & bdata['valid']
    # nRewarded = (bdata['outcome'] == bdata['outcome']['correct'])
    #nRewarded = nRewarded / 2
    rewarded = bdata['nRewarded'] 
    # rewarded_left = bdata['outcome'] == 1 & bdata['rewardSide'] == 0
    # rewarded_right = bdata['outcome'] == 1 & bdata['rewardSide'] == 1
    # trials = bdata['fractionRewarded']
    errors = bdata['outcome'] == bdata.labels['outcome']['error']
    invalid = bdata['outcome'] == bdata.labels['outcome']['invalid']
    valid_choice = bdata['choice'] != bdata.labels['choice']['none']
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']

    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    
    unique_sessionID = np.unique(sessionID) 
    outcome_mode = bdata['outcomeMode']
    # active_port = bdata['activePort']
    allow_early_withdrawal = bdata['allowEarlyWithdrawal']
    anti_bias_mode = bdata['antibiasMode']
    automation_mode = bdata['automationMode']
    psycurve_mode = bdata['psycurveMode']
    rig = bdata.session['hostname']
    info = bdata.session
    # infosnapshots = []
    # for session in sessions: 
    #     info = bdata.session        
    #     infosnapshots.append()
    
    df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                          'valid': valid, 
                                          'valid_left_trials': valid_left_trials,
                                          'valid_right_trials': valid_right_trials,
                                          'left_hits': left_hits,
                                          'right_hits': right_hits,
                                          # 'valid_left': valid_left,
                                          # 'valid_right': valid_right,
                                          'rewarded': rewarded,
                                          # 'rewarded_left': rewarded_left,
                                          # 'rewarded_right': rewarded_right,
                                          # 'trials': trials,
                                          'outcome_mode': outcome_mode,
                                          # 'active_port': active_port,
                                          'allow_early_withdrawal': allow_early_withdrawal,
                                          'anti_bias_mode': anti_bias_mode,
                                          'automation_mode': automation_mode,
                                          'errors': errors,
                                          'invalid': invalid,
                                          'psycurve_mode': psycurve_mode, 
                                          'valid_choice': valid_choice,
                                          'choice_left': choice_left, 
                                          'choice_right': choice_right,
                                          'rig':rig
                                          })
    
    df_session_information = df_trial_information.groupby(by = ['sessionID']) .sum()
    stage_information = df_trial_information.groupby(by =['sessionID']) .max()
        
    conditions = [
        (stage_information['outcome_mode'] == 0) & (stage_information['anti_bias_mode'] == 0) & (stage_information['psycurve_mode'] == 0), 
        (stage_information['outcome_mode'] == 1) & (stage_information['anti_bias_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
        (stage_information['outcome_mode'] == 2) & (stage_information['anti_bias_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
        (stage_information['outcome_mode'] == 3) & (stage_information['anti_bias_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
        (stage_information['outcome_mode'] == 3) & (stage_information['anti_bias_mode'] == 1) & (stage_information['psycurve_mode'] == 0),
        (stage_information['outcome_mode'] == 3) & (stage_information['anti_bias_mode'] == 0) & (stage_information['psycurve_mode'] == 1),
        ]
    values = [0, 1, 2, 3, 3.5, 4]
        
    stage_information['stage'] = np.select(conditions, values)  
    stage_information.head()
    
    
    # Used to calculate performance
    # percent_correct = ((df_s ession_information['hit_outcome']) /df_session_information['valid_choice'] *100)
    left_performance = ((df_session_information['left_hits'] / df_session_information['valid_left_trials']) *100)
    right_performance = ((df_session_information['right_hits'] / df_session_information['valid_right_trials']) *100)
    #percent_correct = ((stage_information['rewarded'] /df_session_information['trials']) *100)
    percent_correct = ((stage_information['rewarded'] /df_session_information['valid']) *100)
    choice_percent_left = (df_session_information['choice_left'] / df_session_information['valid_choice'])
    choice_percent_right = (df_session_information['choice_right'] / df_session_information['valid_choice'])
    
    df_overall_performance = pd.DataFrame({'percent_correct': round(percent_correct, 0),
                                            'left_performance': round(left_performance, 0),
                                            'right_performance': round(right_performance, 0),
                                            'choice_percent_left':round(choice_percent_left, 0),
                                            'choice_percent_right':round(choice_percent_right, 0)})
    
    
    mouse_perf[subject] = pd.DataFrame({'session': session,
                                        'stage': (stage_information['stage']),
                                        # 'trials': (df_session_information['trials']).astype(int), 
                                        'valid': (df_session_information['valid']).astype(int),
                                        'rewarded': (stage_information['rewarded']).astype(int),
                                        'errors': (df_session_information['errors']).astype(int),
                                        # 'invalid': (df_session_information['invalid']).astype(int),
                                        'percent_correct': (df_overall_performance['percent_correct']),
                                        'left_perf': (df_overall_performance['left_performance']),
                                        'right_perf': (df_overall_performance['right_performance']),
                                        # '% left': round(choice_percent_left, 0),
                                        # '% right': round(choice_percent_right, 0),
                                        # '% right': (df_overall_performance['choice_percent_right']),
                                        'rig': stage_information['rig']
                                #'outcome_mode': (df_session_information['outcome_mode']),
                               # 'active_port': (df_session_information['active_port']),
                                #'allow_early_withdrawal': (df_session_information['allow_early_withdrawal']),
                                #'anti_bias_mode': (df_session_information['anti_bias_mode']),
                                             
                                })
    # print(subject)
    
    # extraplots.dataframe_to_html(mouse_perf[subject].iloc[::-1], '/users/angelicamejia/Desktop/research/data/behaviorgraphs/{}.html' .format(subject),)
    
    #days in stage = session date of next stage - first day on session for current stage
    #then, graph ????
    
    # fig = plt.figure()
    # plt.scatter(unique_sessionID, df_session_information['valid'], label = 'Valid', color = 'green')
    # plt.plot(unique_sessionID, df_session_information['valid'], color = 'green')
    # plt.scatter(unique_sessionID, stage_information['rewarded'], label = 'Rewarded', color = 'blue')
    # plt.plot(unique_sessionID, stage_information['rewarded'], color = 'blue')
    # #plt.scatter(unique_sessionID, df_overall_performance['percent_correct'], label = 'Percent Correct', color = 'red')
    # #plt.plot(unique_sessionID, df_overall_performance['percent_correct'], color = 'red')
    # plt.title(subject + ' Performance in Stage 6')
    # plt.xlabel('Sessions')
    # plt.ylabel('Number of Valid and Rewarded trials')
    # plt.legend(loc = 1)
    # plt.xticks(ticks=unique_sessionID)
    # plt.ylim(0, 1300)
    # fig.savefig('/Users/seankyne/Documents/dataAnalysis/data/frem_data/{}performance_stage6.png' .format(subject), dpi=100)
    # plt.show() 
    
    
    
    # fig0 = plt.figure()
    # plt.scatter(unique_sessionID, df_overall_performance['percent_correct'], label = 'Percent Correct', color = 'red')
    # plt.plot(unique_sessionID, df_overall_performance['percent_correct'], color = 'red')
    # plt.title(subject + ' Performance in Stage 5')
    # plt.xlabel('Sessions')
    # plt.ylabel('Percentage of Correct Trials')
    # plt.legend(loc = 1)
    # plt.xticks(ticks=unique_sessionID)
    # plt.ylim(0, 100)
    # fig0.savefig('/Users/seankyne/Documents/dataAnalysis/data/frem_data/{}percent_correct_stage6.png' .format(subject), dpi=100)
    # plt.show()
    

# frem001 = mouse_perf['frem001']
# frem002 = mouse_perf['frem002']
# frem003 = mouse_perf['frem003']
# frem004 = mouse_perf['frem004']
# frem005 = mouse_perf['frem005']

# all_data = [frem001, frem002, frem003, frem004, frem005]
# #loop through each mouse data and identify max number of days
# max_length = 0
# x_ticks = []
# for mouse in all_data:
#     if max_length < len(mouse):
#         max_length =  len(mouse)
# #create a list of days for the x axis
# for i in range(1, max_length + 1):
#     x_ticks.append(i)
    
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(frem001['percent_correct'], color = 'red', label = 'frem001')
# ax1.plot(frem002['percent_correct'], color = 'green', label = 'frem002')
# ax1.plot(frem003['percent_correct'], color = 'blue', label = 'frem003')
# ax1.plot(frem004['percent_correct'], color = 'purple', label = 'frem004')
# ax1.plot(frem005['percent_correct'], color = 'orange', label = 'frem005')
# ax1.legend(loc='lower right', frameon=False)
# ax1.set_xticks(ticks=x_ticks)
# ax1.set_xlabel('Sessions')
# ax1.set_yticks(np.arange(0, 110, 10))
# ax1.set_ylabel('Percent Correct (%)')
# ax1.set_title('Performance of frem mice on stage 5')
#fig.savefig('/Users/seankyne/Documents/dataAnalysis/data/frem_data/frem_mice_performance_stage5.png', dpi=100)

# plots the number of days that the animals were on each stage
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
for subject in subjects: 
    ax3.plot(mouse_perf[subject]['stage'], label = subject)
ax3.legend(loc='lower right', frameon=False)
ax3.set_xticks(np.arange(1,30))
ax3.set_xlabel('Sessions')
ax3.set_yticks(values)
ax3.set_ylabel('Stage')
ax3.set_title('Sessions in Stage X')
fig3.show
fig3.savefig('/Users/angelicamejia/Desktop/research/data/behaviorgraphs/images/stagedays_amfreelymoving', dpi=100)
