#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 13:41:11 2021

@author: seankyne
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

subjects = ['frem001',
            # 'frem002',
            # 'frem003',
            # 'frem004',
            # 'frem005'
            ]
            
sessions = { 
    
    'frem001': ['20210817a', '20210818a', #stage 1
                '20210819a', '20210820a', '20210821a', '20210822a', '20210823a', #stage 2
                '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', '20210904a', 
                '20210906a', '20210907a', '20210908a', '20210909a', '20210910a', #stage 3.2
                '20210911a', '20210913a', '20210914a', '20210915a', #stage 3.1
                '20210916a', #stage 3.2
                '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', #stage 4
                '20210925a', '20210926a', '20210927a', '20210928a', '20210929a', '20210930a', '20211001a', '20211002a', '20211003a', '20211004a', '20211005a', '20211006a', 
                '20211007a', '20211008a', '20211009a', '20211010a', '20211011a', '20211012a', '20211013a', '20211014a', '20211016a', '20211017a', '20211018a', '20211019a',
                '20211020a', #stage 5
                '20211021a', '20211022a', '20211023a', '20211025a', '20211026a', '20211027a', '20211028a', '20211029a', '20211030a', '20211031a', '20211101a',  #stage 6
                '20211102a', '20211103a'  #stage 7
                         
                         ],
                         
    'frem002': ['20210817a', '20210818a', #stage  1
                '20210819a', #stage 2
                '20210820a',  #stage 1
                '20210821a', #stage2
                '20210822a', '20210823a', #stage 3.1
                '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', '20210904a', 
                '20210906a', #stage 3.2
                '20210907a', '20210908a', #stage 4
                '20210909a', #unknown stage
                '20210910a', #stage 5 (placed on wrong stage)
                '20210911a', #stage 3.1
                '20210913a', '20210914a', '20210915a', #stage 4
                '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a','20210926a', '20210927a', '20210928a', '20210929a', 
                '20210930a', '20211001a', '20211002a', '20211003a', '20211004a',  '20211005a','20211006a', #stage 5
                '20211007a', #stage 6
                '20211008a',  #stage 5
                '20211009a', '20211010a', '20211011a', #stage 6
                '20211012a', '20211013a', '20211014a', '20211015a', '20211016a', '20211017a', '20211018a', '20211019a', '20211020a', '20211021a', '20211022a', '20211023a',
                '20211025a', '20211026a', '20211027a', '20211028a', '20211029a', '20211030a', '20211031a', '20211101a', #stage 7
                '20211102a', '20211103a'  #stage 8
                         
                         ],
    
    'frem003': ['20210817a', '20210818a', '20210819a', #stage  1
                '20210820a', '20210821a', '20210822a',  #stage 2
                '20210823a', #stage 3.1
                '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', #stage 3.2
                '20210904a', #wrong parameters
                '20210906a', '20210907a', #stage 3.2
                '20210908a', '20210909a', #stage 4
                '20210910a', #stage 5
                '20210911a', #stage 3.1
                '20210913a', #wrong parameters
                '20210914a', '20210915a', #stage 4
                '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a','20210926a', '20210927a', '20210928a', 
                '20210929a', '20210930a', '20211001a', '20211002a', '20211003a', '20211004a', '20211005a', '20211006a', #stage 5
                '20211007a', #stage 6
                '20211008a', #stage 5
                '20211009a', '20211010a', '20211011a', #stage 6
                '20211012a', '20211013a', '20211014a', '20211015a', '20211016a', '20211017a', '20211018a', '20211019a', '20211020a', '20211021a', '20211022a', 
                '20211023a', '20211025a', '20211026a', '20211027a', '20211028a', '20211029a', '20211030a', '20211031a', '20211101a',  #stage 7
                '20211102a', '20211103a'     #stage 8
                ],
    
    'frem004': ['20210817a', '20210818a', #stage 1
                '20210819a', '20210820a', #stage 2
                '20210821a', '20210822a', '20210823a', #stage 3.1
                '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210902a', '20210903a', '20210904a', 
                '20210906a', '20210907a', '20210908a', '20210909a', #stage 3.2
                '20210911a', #stage 3.1
                '20210913a', #stage 3.2
                '20210914a', '20210915a', #stage 4.0
                '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a', '20210926a', '20210927a', '20210928a', 
                '20210929a', '20210930a', '20211001a', '20211002a', '20211004a', '20211005a', '20211006a', '20211007a', '20211008a', '20211009a', '20211010a',
                '20211011a', #stage 5
                '20211012a', '20211013a', #stage 6
                '20211014a', '20211015a', '20211016a', '20211017a', '20211018a', '20211019a', '20211020a', '20211021a',
                '20211022a', '20211023a', '20211025a', '20211026a', '20211027a', '20211028a', '20211029a', '20211030a', '20211031a', '20211101a', #stage 7
                '20211102a', '20211103a'       #stage 8
                
                ],
    
    'frem005': ['20210817a', '20210818a', #stage 1
                '20210819a', '20210820a', #stage 2
                '20210821a', '20210822a', #stage 3.1
                '20210823a', #trained on the wrong parameters
                '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', 
                '20210904a', '20210907a', #stage 3.2
                '20210908a', #stage 4
                '20210909a', #stage 3.2
                '20210910a', #stage 5
                '20210911a', #stage 3.1
                '20210913a', '20210914a', '20210915a', #stage 4
                '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a','20210926a', '20210927a', #stage 5
                '20210928a', #wrong parameters
                '20210929a', '20210930a', '20211001a', '20211002a', '20211003a', '20211004a', '20211005a', '20211006a', #stage 5
                '20211007a', #stage 6
                '20211008a', #stage 5
                '20211009a', '20211010a', '20211011a', #stage 6
                '20211012a', '20211013a', '20211014a', '20211015a', '20211016a', '20211017a', '20211018a', '20211019a', '20211020a', '20211021a', 
                '20211022a', '20211023a', '20211025a', '20211026a', '20211027a', '20211028a', '20211029a', '20211030a', '20211031a', '20211101a', #stage 7
                '20211102a', '20211103a'      #stage 8
                
                ]
    
    
    }
paradigm = '2afc'

protocol = ['frem001', 'frem002', 'frem003', 'frem004', 'frem005']    

mouse_perf = {}
for subject in subjects:  
    session = sessions[subject]    
    bdata = behavioranalysis.load_many_sessions(subject,paradigm=paradigm,sessions=session)
    
    sessionID = bdata['sessionID'] + 1
    #unique_sessionID = np.unique(sessionID)
    valid = bdata['valid']
    # nRewarded = bdata['outcome'] & bdata['valid']
    # nRewarded = (bdata['outcome'] == bdata['outcome']['correct'])
    #nRewarded = nRewarded / 2
    rewarded = bdata['nRewarded'] 
    trials = bdata['fractionRewarded']
    errors = bdata['outcome'] == bdata.labels['outcome']['error']
    invalid = bdata['outcome'] == bdata.labels['outcome']['invalid']
    
    
    unique_sessionID = np.unique(sessionID) 
    outcome_mode = bdata['outcomeMode']
    active_port = bdata['activePort']
    allow_early_withdrawal = bdata['allowEarlyWithdrawal']
    anti_bias_mode = bdata['antibiasMode']
    automation_mode = bdata['automationMode']
    psycurve_mode = bdata['psycurveMode']
    
    df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                          'valid': valid,
                                          'rewarded': rewarded,
                                          'trials': trials,
                                          'outcome_mode': outcome_mode,
                                          'active_port': active_port,
                                          'allow_early_withdrawal': allow_early_withdrawal,
                                          'anti_bias_mode': anti_bias_mode,
                                          'automation_mode': automation_mode,
                                          'errors': errors,
                                          'invalid': invalid,
                                          'psycurve_mode': psycurve_mode
                                          })
    
    df_session_information = df_trial_information.groupby(by = ['sessionID']) .sum()
    stage_information = df_trial_information.groupby(by =['sessionID']) .max()
    
    if subject in protocol:
        
        conditions = [
            (stage_information['outcome_mode'] == 0) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 1) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0), 
            (stage_information['outcome_mode'] == 1) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 1) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 2) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 1) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 2) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 0) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 2) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 0) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 1) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 3) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 0) & (stage_information['anti_bias_mode'] == 1) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 3) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 0) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 0),
            (stage_information['outcome_mode'] == 3) & (stage_information['active_port'] == 0) & (stage_information['allow_early_withdrawal'] == 0) & (stage_information['anti_bias_mode'] == 0) & (stage_information['automation_mode'] == 0) & (stage_information['psycurve_mode'] == 1),
            #(stage_information['outcome_mode'] == )
            ]
        values = [1, 2, 3.1, 3.2, 4, 5, 6, 7]
    else:
        pass
        
    stage_information['stage'] = np.select(conditions, values)  
    stage_information.head()
    
    #percent_correct = ((stage_information['rewarded'] /df_session_information['trials']) *100)
    percent_correct = ((stage_information['rewarded'] /df_session_information['valid']) *100)
    
    df_overall_performance = pd.DataFrame({'percent_correct': round(percent_correct, 0) })
    
    
    mouse_perf[subject] = pd.DataFrame({'session': session,
                                        'stage': (stage_information['stage']),
                                        'trials': (df_session_information['trials']).astype(int), 
                                        'valid': (df_session_information['valid']).astype(int),
                                        'rewarded': (stage_information['rewarded']).astype(int),
                                        'errors': (df_session_information['errors']).astype(int),
                                        'invalid': (df_session_information['invalid']).astype(int),
                                        'percent_correct': (df_overall_performance['percent_correct']),
                                #'outcome_mode': (df_session_information['outcome_mode']),
                               # 'active_port': (df_session_information['active_port']),
                                #'allow_early_withdrawal': (df_session_information['allow_early_withdrawal']),
                                #'anti_bias_mode': (df_session_information['anti_bias_mode']),
                                             
                                })
    print(subject)
    
    extraplots.dataframe_to_html(mouse_perf[subject].iloc[::-1], '/users/seankyne/Documents/dataAnalysis/data/{}.html' .format(subject, subject),)
    
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
    
