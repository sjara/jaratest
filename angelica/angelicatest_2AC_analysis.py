#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:01:50 2021

@author: angelicamejia
"""

import numpy as np
import pandas as pd
import seaborn 
seaborn.set()
import matplotlib.pyplot as plt 
#import sys
from jaratoolbox import behavioranalysis 
from jaratoolbox import extraplots
#from jaratoolbox import settings 


#Add the subject/dates you want to look at. 
subjects =  [ 
                    # 'pals010', 
                    # 'pals012',
                    # 'pals013', 
                    # 'pals014',
                    # 'pals015', 
                    'pals016',
                    # 'pals017',
                    # 'pals018', 
                    # 'pals020', 
                    # 'pals021', 
                    # 'pals022',
                    # 'pals024',
                    # 'pals025',
                    # 'pals026'
             ]


angelica_protocol = ['pals015', 'pals016', 'pals017', 'pals024', 'pals025', 'pals026']
bella_protocol = ['pals010', 'pals012', 'pals013', 'pals014', 'pals018']
sean_protocol = ['pals020', 'pals021', 'pals022']

paradigm = 'twochoice'

#Add the specific dates you want to look at. The reason they are separated like this is for personal organization. You can come up with your own system!
sessionsEachSubject = { 
    
     # 'pals010': ['20210602a', '20210603a', '20210604a', '20210605a', '20210606a', '20210607a', '20210608a', '20210609a', 
     #              '20210610a', '20210611a', '20210612a', '20210613a', '20210614a', '20210615a', '20210616a', '20210617a',
     #              '20210618a', '20210619a', '20210621a', '20210622a', '20210623a', '20210624a', '20210625a',
     #              '20210626a', '20210627a', '20210628a', '20210629a', '20210630a', '20210701a', '20210702a', '20210703a', '20210706a', 
     #              '20210707a', '20210708a', '20210709a', '20210710a', '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', 
     #              '20210716a', '20210717a', '20210719a'
     #             ],

    
     'pals012': [
                  # '20210602a', '20210603a', '20210604a', '20210605a', '20210606a', '20210607a', '20210608a', '20210609a', 
                  # '20210610a', '20210611a', '20210612a', '20210613a', '20210614a', '20210615a', '20210616a', '20210617a',
                  # '20210618a', '20210619a', '20210621a', '20210622a', '20210623a', '20210624a', '20210625a',
                  # '20210626a', '20210628a', '20210629a', '20210630a', '20210701a', '20210702a', '20210703a', '20210706a', 
                  # '20210707a', '20210708a', '20210709a', '20210710a', '20210711a', 
                 #Stage 3.5
                   '20210713a', '20210714a', '20210715a', '20210716a', '20210717a', '20210718a', '20210719a', '20210720a', '20210721a', 
                   '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', '20210727a', '20210728a', '20210729a', '20210730a', 
                   '20210730b', '20210731a', '20210801a', '20210802a', '20210803a', '20210804a', '20210805a', '20210806a', '20210807a', 
                   '20210809a'
                  ],
    
     # 'pals013': ['20210601a', '20210602a', '20210603a', '20210604a', '20210605a', '20210606a', '20210607a', '20210608a', '20210609a', 
     #             '20210610a', '20210611a', '20210612a', '20210613a', '20210614a', '20210615a', '20210616a', '20210617a', '20210618a', 
     #             '20210619a', '20210621a', '20210622a', '20210623a', '20210624a', '20210625a',
     #             '20210626a', '20210627a', '20210628a', '20210629a', '20210630a', '20210701a', '20210702a', '20210703a', '20210706a', 
     #             '20210707a', '20210708a', '20210709a', '20210710a', '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', 
     #             '20210716a', '20210717a', '20210718a', '20210719a'],
    
     # 'pals014': ['20210602a', '20210603a', '20210604a', '20210605a', '20210606a', '20210608a', '20210609a', 
     #             '20210610a', '20210611a', '20210612a', '20210613a', '20210614a', '20210615a', '20210616a', '20210617a', '20210618a', 
     #             '20210619a', '20210621a', '20210622a', '20210623a', '20210624a', '20210625a', '20210626a', '20210627a', 
     #             '20210628a', '20210629a', '20210630a', '20210701a', '20210702a', '20210703a', '20210706a', '20210707a', '20210708a',
     #             '20210709a', '20210710a', '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', '20210716a', '20210717a', 
     #             '20210718a', '20210719a'],
    
    'pals015': [
                '20210628a', '20210629a', '20210630a', '20210701a', '20210702a', '20210703a', '20210706a', 
                '20210707a', '20210708a', '20210709a', '20210710a', '20210711a', '20210712a', '20210713a', 
                #stage 4.0
                # '20210714a', '20210715a', '20210716a', '20210718a', '20210719a', 
                # '20210725a', 
                # '20210726a', 
                # '20210727a', '20210728a', '20210729a', '20210730a', '20210731a', '20210801a', '20210802a', 
                # #stage 0.5
                # '20210803a', '20210803b', '20210804a', '20210804b', '20210807a', '20210807b', '20210808a', '20210808b', 
                # stage 4.0 again
                # '20210809a', '20210811a', '20210812a', '20210813a', '20210815a', '20210817a', '20210818a', '20210819a', '20210820a', '20210821a', 
                # '20210822a',
            ],
    
    'pals016': [
                # '20210628a', '20210629a', '20210630a', 
                # '20210701a', 
                # '20210702a', 
                # '20210703a',
                # '20210706a',
                # '20210707a', 
                # '20210708a', '20210709a', 
    # #             #stage 4.0
                # '20210710a', '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', '20210716a', '20210717a', '20210718a', 
                # '20210719a', '20210720a', '20210721a', '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', '20210727a',
                # '20210728a', '20210729a', '20210730a', '20210731a', '20210801a', '20210802a' , 
                # # # stage 0.5
                # # '20210803b', '20210804a', '20210804b','20210805a', '20210805b', '20210806a', '20210806b', 
                # # # # stage 4.0 again
                # '20210807a', '20210808a', '20210809a', '20210810a', '20210811a', '20210812a', '20210813a', '20210815a', 
                # '20210816a','20210817a', '20210818a', '20210819a', '20210820a', '20210821a', '20210822a', '20210823a', '20210824a', 
                '20210825a', 
                # # stage 4.5
                # '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', 
                # '20210903a', '20210904a', '20210906a', '20210907a', '20210908a', '20210909a', '20210913a', '20210914a', '20210915a', 
                # '20210916a', '20210917a', '20210920a'
                ],
            
    
    'pals017': [
                '20210628a', '20210629a', '20210630a',
                '20210701a',
                '20210702a', 
                  '20210703a',
                '20210706a', 
                '20210707a', 
                '20210708a', 
                # # stage 4.0
                # '20210709a', '20210710a', '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', '20210716a', '20210717a', 
                # '20210718a', '20210719a', '20210720a', '20210721a', '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', 
                # '20210727a', '20210728a', '20210729a', '20210730a', '20210731a', '20210801a', '20210802a',  
                # # #stage 0.5
                # # '20210803a', '20210803b', '20210804a', '20210804b', '20210805a', '20210805b', '20210806a', '20210806b', 
                # # '20210807a', '20210807b', '20210808a', '20210808b', 
                # # stage 4.0 again
                # '20210809a', '20210810a', '20210811a', '20210812a', '20210813a', 
                # '20210815a', '20210816a','20210817a', '20210818a',  '20210819a', '20210820a', '20210821a', '20210822a', '20210825a', 
                # # Stage 4.5
                # '20210826a', '20210827a', '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', 
                # '20210904a', '20210906a', '20210907a', '20210908a', '20210909a', '20210913a', '20210914a', '20210915a', '20210916a', 
                # '20210917a', '20210920a' 
                ],
        
    # 'pals018': [
    #             '20210701a', '20210702a', '20210703a', '20210706a', '20210707a', 
    #             '20210708a', '20210709a', '20210710a', 
    #             '20210711a', '20210712a', '20210713a', '20210714a', '20210715a', '20210716a', '20210717a'],
    
    'pals020': [ '20210718a', '20210719a', '20210720a', '20210721a', '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', 
                '20210727a', '20210729a', '20210730a', '20210731a', '20210801a', 
                '20210804a', '20210807a', '20210808a', '20210809a', '20210810a', '20210811a', '20210812a', '20210813a', '20210814a', '20210815a', 
                '20210817a', '20210818a', '20210819a', '20210820a', '20210821a', '20210822a', '20210823a', '20210824a', '20210825a', '20210826a', 
                '20210827a', '20210828a', '20210829a',  '20210830a', '20210831a','20210901a', '20210902a', '20210903a', '20210904a', '20210907a', 
                '20210908a', '20210909a', '20210910a', '20210911a', '20210912a', '20210913a', '20210914a', '20210920a', '20210921a', '20210922a', 
                '20210923a', '20210924a', '20210925a', '20210926a', '20210927a', '20210928a', '20211009a', '20211010a', '20211011a', '20211012a', 
                '20211013a'
                ], 
    
    'pals021': ['20210718a', '20210719a', '20210720a', '20210721a', '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', 
                '20210727a', '20210729a', '20210730a', '20210731a', '20210801a', '20210804a', '20210806a', '20210807a', '20210808a', 
                '20210809a', '20210810a', '20210811a', '20210812a', '20210813a', '20210814a', '20210815a', '20210817a', '20210818a', 
                '20210819a', '20210820a', '20210821a', '20210822a', '20210823a', '20210824a', '20210825a', '20210826a', '20210827a', 
                '20210828a', '20210829a', '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', '20210904a', '20210906a', 
                '20210907a', '20210908a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a', '20210926a', 
                '20210927a', '20210928a', '20211009a', '20211010a', '20211011a', '20211012a', '20211013a'],
    
    'pals022': ['20210718a', '20210719a', '20210720a', '20210721a', '20210722a', '20210723a', '20210724a', '20210725a', '20210726a', 
                '20210727a', '20210728a', '20210729a', '20210730a', '20210731a', '20210801a', '20210804a', '20210805a', '20210806a', 
                '20210807a', '20210808a', '20210809a', '20210810a', '20210811a', '20210812a', '20210813a', '20210814a', '20210815a', 
                '20210817a', '20210818a', '20210819a', '20210820a', '20210821a', '20210822a', '20210823a', '20210824a', '20210825a', 
                '20210826a', '20210827a', '20210828a', '20210829a',  '20210830a', '20210831a', '20210901a', '20210902a', '20210903a', 
                '20210904a', '20210906a', '20210907a', '20210908a', '20210909a', '20210910a', '20210911a', '20210912a', '20210913a', 
                '20210914a', '20210915a', '20210920a', '20210921a', '20210922a', '20210923a', '20210924a', '20210925a', '20210926a', 
                '20210927a', '20210928a', '20211009a', '20211010a', '20211011a', '20211012a', '20211013a'] ,   
    
    'pals024': [
                '20210803a',
                 '20210804a', '20210805a', '20210806a', '20210808a', '20210809a', '20210810a', '20210811a', '20210812a', 
                '20210813a','20210814a', '20210815a', 
                # Stage 4.0
                '20210817a', '20210818a', '20210819a', '20210820a', '20210821a', 
                '20210823a', '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210830a', '20210831a', '20210901a', 
                '20210902a', '20210903a', '20210906a', '20210907a', '20210908a', '20210909a', '20210910a', '20210911a', '20210912a', 
                '20210913a', '20210914a', '20210915a', '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', 
                '20210924a', '20210925a', '20210926a', '20210927a', '20210928a', '20210929a', '20210930a', '20211001a', '20211002a', 
                '20211003a', '20211004a', '20211005a', '20211006a', '20211007a', '20211008a', '20211010a', '20211011a', '20211012a', 
                '20211013a', '20211014a', '20211015a', '20211016a', '20211014a'
                ],
     
    'pals025': [
    '20210803a', '20210804a', '20210805a', '20210806a', '20210807a', '20210808a', '20210809a', '20210810a', '20210812a', 
                '20210813a', '20210814a', '20210815a', '20210816a','20210817a', 
                # Stage 4.0
                '20210818a', '20210819a', '20210820a', '20210821a', 
                '20210823a', '20210824a', '20210825a', '20210826a', '20210827a', '20210828a', '20210830a', '20210831a', '20210901a', 
                '20210902a', '20210903a', '20210906a', '20210907a', '20210908a', '20210909a', '20210910a', '20210911a', '20210912a', 
                '20210913a', '20210914a', '20210915a', '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', 
                '20210924a', '20210925a', '20210926a', '20210927a', '20210928a', '20210929a', '20210930a', '20211001a', '20211002a', 
                '20211003a', '20211004a', '20211005a', '20211006a', '20211007a', '20211008a', '20211010a', '20211011a', '20211012a', 
                '20211013a'
                ],
                  
    'pals026': [
                '20210803a', '20210804a', '20210805a', '20210806a', '20210807a', '20210808a', '20210809a', '20210810a', '20210811a', 
                '20210812a', 
                # Stage 4.0
                '20210813a', '20210814a', '20210815a','20210817a', '20210818a', '20210819a', '20210820a', '20210821a', 
                '20210823a', '20210824a', '20210825a', '20210826a', '20210827a', '20210828a',  '20210830a', '20210831a', '20210901a', 
                '20210902a', '20210903a', '20210906a', '20210907a', '20210908a', '20210909a', '20210910a', '20210911a', '20210912a', 
                '20210913a', '20210914a', '20210915a', '20210916a', '20210917a', '20210920a', '20210921a', '20210922a', '20210923a', 
                '20210924a', '20210925a', '20210926a', '20210927a', '20210928a', '20210929a', '20210930a', '20211001a', '20211002a', 
                '20211003a', '20211004a', '20211005a', '20211006a', '20211007a', '20211008a', '20211010a', '20211011a', '20211012a', 
                '20211013a'
                ]
   }


mouse_perf = {}
for subject in subjects: 
    sessions = sessionsEachSubject[subject]    
    bdata = behavioranalysis.load_many_sessions(subject,paradigm='twochoice',sessions=sessions)
    
    sessionID = bdata['sessionID'] + 1
    unique_sessionID = np.unique(sessionID) 
    task_mode = bdata['taskMode']
    lick_offset = bdata['lickBeforeStimOffset']
    lick_on_stim = bdata['taskMode'] == bdata.labels['taskMode']['lick_on_stim']
    #water_after_sound = bdata['taskMode'] == bdata.labels['taskMode']['water_after_sound']
    discriminate_stim = bdata['taskMode'] == bdata.labels['taskMode']['discriminate_stim']
    sound_type = bdata['soundType']
    
    
    choice = bdata['choice']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']
    valid_choice = bdata['choice'] != bdata.labels['choice']['none']
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    
    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
    total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
    
    reward_side_mode = bdata['rewardSideMode']
    targetAMdepth = bdata['targetAMdepth']
    
    hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    left_errors = valid_left_trials & choice_right
    right_errors = valid_right_trials & choice_left
    total_errors = right_errors + left_errors

    
    total_errors_right = bdata['nErrorsRight']
    total_licks_left = bdata['nLicksLeft']
    total_licks_right = bdata['nLicksRight']
    total_licks = total_licks_left + total_licks_right
    
    # early_licks_left = bdata['nEarlyLicksLeft']
    
    # rewarded_trials = bdata.events['nextState'] == bdata.stateMatrix['statesNames']['stopReward']
    # #valid_rewarded_trial = rewarded_trials & choice
    # total_rewards = sum(rewarded_trials)
    # punishment_left = max(bdata['nPunishmentLeft'])
    # punishment_right = max(bdata['nPunishmentRight'])
    # total_punishment = punishment_left + punishment_right
    
    false_alarms_right = bdata['nFalseAlarmsRight']
    false_alarms_left = bdata['nFalseAlarmsLeft']
    
    # false_alarms_left2 = (bdata['outcome'] == bdata.labels['outcome']['falseAlarm']) & (bdata.events['eventCode']==bdata.stateMatrix['eventsNames']['Lin'])
    # false_alarms_right2 = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & (bdata['outcome'] == bdata.labels['outcome']['falseAlarm'])

    missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
    misses_left = bdata['nMissesLeft']
    misses_right = bdata['nMissesRight']
    
    reward = bdata['outcome'] == (-1 or 1)

    
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
                                         'missed_outcomes': missed_outcomes,
                                         'misses_left' : misses_left,
                                         'misses_right': misses_right,
                                         'total_misses' : missed_outcomes,
                                         # 'early_licks_left': early_licks_left,
                                         'left_choice': choice_left,
                                         'right_choice': choice_right,
                                         'valid_left_trials': valid_left_trials,
                                         'valid_right_trials': valid_right_trials,
                                         'valid_choice': valid_choice,
                                         'total_left_trials': total_left_trials,
                                         'total_right_trials': total_right_trials,
                                         'reward_side_mode': reward_side_mode,
                                         'task_mode': task_mode,
                                         'lick_offset' : lick_offset,
                                         'targetAMdepth' : targetAMdepth,
                                         'reward': reward
                                         #'rewarded_trials': rewarded_trials
                                         # 'punishment_left': punishment_left,
                                         # 'punishment_right': punishment_right
                                         
                                         })
    
    #Use this groupby to gather the data that should be summed per session
    df_session_information = df_trial_information.groupby(by = ['sessionID']).sum()
    
    #Use this groupby to gather the information that should be maxed per session
    stage_information = df_trial_information.groupby(by =['sessionID']).max()
    
    if subject in angelica_protocol: 
        
        conditions = [
        (stage_information['reward_side_mode'] == 2) | (stage_information['reward_side_mode'] == 3),
        (stage_information['task_mode'] == 0) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 0),
        (stage_information['task_mode'] == 0) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 2) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 2), 
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 0)
        ]
    
        values = [0.5, 1, 2, 3, 4, 4.5, 5]    
        
    elif subject in bella_protocol: 
       conditions = [
        (stage_information['task_mode'] == 0) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 0),
        (stage_information['task_mode'] == 2) & (stage_information['reward_side_mode'] == 4),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 2), 
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 0)
        ]
       
       values = [1, 2, 3, 3.5, 4]
       
    else: 
          conditions = [
        (stage_information['task_mode'] == 0) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 1), 
        (stage_information['task_mode'] == 2) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 3),
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 4) & (stage_information['lick_offset'] == 2), 
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 3), 
        (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 1),
        # (stage_information['task_mode'] == 3) & (stage_information['reward_side_mode'] == 0) & (stage_information['lick_offset'] == 1) 
        ]
          
          values = [1, 2, 3, 3.5, 4, 5]

       
    stage_information['stage'] = np.select(conditions, values)  
    stage_information.head() 
    
    # Used to calculate performance
    percent_correct = ((df_session_information['hit_outcome']) /df_session_information['valid_choice'] *100)
    left_performance = ((df_session_information['left_hits'] / df_session_information['valid_left_trials']) *100)
    right_performance = ((df_session_information['right_hits'] / df_session_information['valid_right_trials']) *100)
    mean_side_performance = ((left_performance + right_performance)/ 2 )
    # percent_rewarded = ((total_rewards/ len(choice)) *100)
    
    df_overall_performance = pd.DataFrame({'percent_correct': round(percent_correct, 2),
                                            'left_performance': round(left_performance, 2),
                                            'right_performance': round(right_performance, 2),
                                            'mean_side_performance' : round(mean_side_performance, 2)
                                            })
    
    #used to identify task mode per session
    df_id_reward_mode = pd.DataFrame({'sessionID': sessionID,
                                         'task_mode' : task_mode,
                                         'reward_side_mode': reward_side_mode,
                                         'lick_on_stim': lick_on_stim,
                                         #'water_after_sound': water_after_sound,
                                         'discriminate_stim': discriminate_stim,
                                         'sound_type': sound_type
                                         })

    rewards = (df_session_information['reward']).astype(int)
    total_trials = (df_session_information['total_left_trials']+df_session_information['total_right_trials']).astype(int)
    percent_rewarded = rewards / total_trials
    
   # this dataframe consolidates all of the other information to one dataframe that gets saved to an xlsx sheet
   # comment and uncomment certain pieces of information, depending on what you want to show up in the file
    mouse_perf[subject] = pd.DataFrame({'sessions':sessions,
                               'stage': (stage_information['stage']),
                               'hit_outcome': df_session_information['hit_outcome'],
                               'left_hits': (df_session_information['left_hits']).astype(int),
                               'right_hits': (df_session_information['right_hits'].astype(int)),
                               'false_alarms_left': (stage_information['false_alarms_left'].astype(int)),
                               'false_alarms_right': (stage_information['false_alarms_right'].astype(int)),
                               'left_errors': (df_session_information['left_errors'].astype(int)),
                               'right_errors': (df_session_information['right_errors']).astype(int),         
                               'left_perf': (df_overall_performance['left_performance']),
                               'right_perf': (df_overall_performance['right_performance']),
                               'percent_correct': (df_overall_performance['percent_correct']),
                               'licks_left': (stage_information['total_licks_left'].astype(int)),
                               'licks_right': (stage_information['total_licks_right'].astype(int)),
                               'misses': (df_session_information['missed_outcomes'].astype(int)),
                                'misses_right': (stage_information['misses_right'].astype(int)),
                                'left_trials': (df_session_information['total_left_trials'].astype(int)),
                                'right_trials': (df_session_information['total_right_trials'].astype(int)),
                               # 'percent_rewarded': percent_rewarded
                                # 'early_licks_left': (stage_information['early_licks_left'].astype(int))
                               })
    

    #We used to use this to make excel tables before we transfered to html
    #prints the session ID, task mode, and number of trials. 
    print(subject)
    # print(mouse_perf[subject])
    #Saves the specified dataframe to an excel document 
    # mouse_perf[subject].to_excel('/users/angelicamejia/Desktop/research/data/behaviorgraphs/{}.xlsx'.format(subject),  sheet_name='{}'.format(subject), index = False)
    
    #Use this one instead, the graphs are 'beautified' and more modern looking
    # extraplots.dataframe_to_html(mouse_perf[subject].iloc[::-1], '/users/angelicamejia/Desktop/research/data/behaviorgraphs/{}.html' .format(subject),) 





# # # #BELOW IS CODE USED FOR PLOTS OF PERFORMANCE AND THE PLOTS TYPICALLY USED IN STAGE 3 AND 3.5

#     #plots the correct performance and how the animal performed with each side. Reminder that stage 1 will not be printed.

    fig = plt.figure()
    plt.scatter(unique_sessionID, left_performance, color = 'blue', label = 'Left')
    plt.plot(unique_sessionID, left_performance, color = 'blue')
    plt.scatter(unique_sessionID, right_performance, color = 'red' , label = 'Right')
    plt.plot(unique_sessionID, right_performance, color = 'red')
    plt.scatter(unique_sessionID, percent_correct, color = 'black', label = 'Percent Correct')
    plt.plot(unique_sessionID, percent_correct, color = 'black')
    plt.title(subject + ' Performance in Stage 4.0')
    plt.xlabel('Sessions in Stage 4.0')
    plt.ylabel('Percent animal chose the correct side (%)')
    plt.legend(loc = 3)
    plt.xticks(ticks=unique_sessionID, fontsize = 7)
    # plt.axhline(0.25, linestyle='--')
    plt.axvline(x= 24, linestyle='--')
    plt.ylim(0, 100)
    plt.show()
    # Take in  mind this is going to have to be specified depending on where you want your figures to save
    fig.savefig('/Users/angelicamejia/Desktop/research/data/behaviorgraphs/images/{}remedialefficacy.png' .format(subject), dpi=100)    
    
#     #plots the hits in each session. You can also uncomment out the errors and side hits if that is something you are interested in looking at. 
#     fig0 = plt.figure() 
#     plt.scatter(unique_sessionID, df_session_information['hit_outcome'], color = 'grey', label = 'hits')
#     plt.plot(unique_sessionID, df_session_information['hit_outcome'], color = 'grey')
#     plt.scatter(unique_sessionID, (df_session_information['left_choice'] + df_session_information['right_choice']), color = 'black', label = 'choices')
#     plt.plot(unique_sessionID, (df_session_information['left_choice'] + df_session_information['right_choice']), color = 'black')
# #     # plt.plot(unique_sessionID, df_session_information['total_errors'])
# #     # plt.scatter(unique_sessionID, df_session_information['total_errors'])
#     # plt.scatter(unique_sessionID, df_session_information['left_hits'], color = 'blue', label = 'left')
#     # plt.scatter(unique_sessionID, df_session_information['right_hits'], color = 'red', label = 'right')    
#     plt.title(subject + ' Total hits and choices in each session, Stage 3.5')
#     plt.xlabel('Sessions in Stage 3.5')
#     plt.ylabel('Number of hits per side')
#     plt.ylim(0,500)
#     plt.xticks(ticks=unique_sessionID, fontsize = 7)
#     plt.legend(loc = 1)
#     plt.show()
# # #     #Take in  mind this is going to have to be specified depending on where you want your figures to save
#     fig0.savefig('/Users/angelicamejia/Desktop/research/data/behaviorgraphs/images/{}hitsstage3,5.png' .format(subject), dpi=100)
    
## Fig 5 shows what comprises the number of trials in the mouse's performance
    # percent_falsealarms = mouse_perf[subject]['false_alarms_right'] / mouse_perf[subject]['false']
    # percent_earlylick = mouse_perf[subject]['early_licks_left'] / mouse_perf[subject]['left_trials']

#We will not use this until we get to stage 4 because it looks at the average performance across many mice and also includes different ways of combining many mice on one graph
# pals001 = mouse_perf['pals001']
# pals002 = mouse_perf['pals002']
# pals003 = mouse_perf['pals003']
# # #pals004 = mouse_perf['pals004']
# pals005 = mouse_perf['pals005']
# pals007 = mouse_perf['pals007']
# pals017p = mouse_perf['pals017']
# pals016p = mouse_perf['pals016']
# pals015p = mouse_perf['pals015']

# #PLOTS THE AVERAGE PERFORMANCE OF MICE BUT NEEDS TO BE SPECIFIED IN 260
# df_concat_c1 = pd.concat((pals001, pals003, pals005))
# session_groupby = df_concat_c1.groupby(level=0).mean()


# result = df_concat_c1.groupby(level=0, as_index=False).agg(
#                       {'percent_correct':['mean','std','sem']})
# #plots the average between the mice. Need to add each mouse individually. Will change in future
# plt.scatter(unique_sessionID, result.percent_correct['mean'], color = 'red')
# plt.plot(unique_sessionID, result.percent_correct['mean'], color = 'red')
# plt.errorbar(unique_sessionID, result.percent_correct['mean'], yerr=result.percent_correct['sem'])
# plt.title('Average performance of pals001,003, & 005')
# plt.xlabel('Days in stage 3')
# plt.ylabel('Average Percent Correct (%)')
# plt.xticks(ticks=unique_sessionID)
# plt.ylim(0,100)
# plt.show    


# #FIG 1 AND 2 plots the individual performance of ALL mice in one graph. 
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111)
# ax1.plot(pals001['percent_correct'], color = 'red', label = 'pals001')
# ax1.plot(pals003['percent_correct'], color ='g', label = 'pals003')
# #ax1.plot(pals004['percent_correct'], color ='c')
# ax1.plot(pals005['percent_correct'],color = 'm', label = 'pals005')
# ax1.legend(loc='upper right', frameon=False)
# ax1.set_xticks(np.arange(1,12,1))
# ax1.set_xlabel('Sessions in stage 3')
# ax1.set_yticks(np.arange(0,110, 20))
# ax1.set_ylabel('Percent Correct (%)')
# ax1.set_title('Performance of Cohort 1 on stage 3')
#fig1.savefig(r'C:\Users\isabe\data\behavior_graphs\performance_cohort1.png', dpi=300)

# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# ax2.plot(pals002['percent_correct'], color = 'black', label = 'pals002')
# ax2.plot(pals007['percent_correct'], color ='orange', label = 'pals007')
# #ax1.plot(pals004['percent_correct'], color ='c')pals
# ax2.plot(pals008['percent_correct'],color = 'cyan', label = 'pals008')
# ax2.legend(loc='upper right', frameon=False)
# ax2.set_xticks(unique_sessionID)
# ax2.set_xlabel('Sessions in stage 3')
# ax2.set_yticks(np.arange(0,110, 20))
# ax2.set_ylabel('Percent Correct (%) ')
# ax2.set_title('Performance of Cohort 2 on stage 3')
# fig2.savefig(r'C:\Users\isabe\data\behavior_graphs\performance_cohort2.png', dpi=300)


# FIG 3 & 4 PLOT THE DAYS THE ANIMAL WAS IN EACH STAGE .
# subjects_to_graph = ['pals016', 'pals017']
# fig3 = plt.figure()
# ax3 = fig3.add_subplot(111)
# for subject in subjects: 
#     ax3.plot(mouse_perf[subject]['stage'], label = subject)
# ax3.legend(loc='upper right', frameon=False)
# ax3.set_xticks(np.arange(1,15))
# ax3.set_xlabel('Sessions')
# ax3.set_yticks(values)
# ax3.set_ylabel('Stage')
# ax3.set_title('Sessions in Stage X')
# fig3.show
# fig3.savefig('/Users/angelicamejia/Desktop/research/data/behaviorgraphs/images/stagedays_headfixedcohort3.png' .format(subject), dpi=100)


# fig4 = plt.figure()
# ax4 = fig4.add_subplot(111)
# ax4.plot(pals002['stage'], color = 'orange', label = 'pals001')
# ax4.plot(pals007['stage'], color ='magenta', label = 'pals003')
# ax4.plot(pals008['stage'], color ='blue', label = 'pals005')
# ax4.legend(loc='upper right', frameon=False)
# ax4.set_xticks(np.arange(1,12))
# ax4.set_xlabel('Sessions')
# ax4.set_yticks(values)
# ax4.set_ylabel('Stage')
# ax4.set_title('Cohort 2, sessions in stage x')
#fig4.savefig(r'C:\Users\isabe\data\behavior_graphs\stagedays_cohort2.png', dpi=300)



    
    
    
    
    