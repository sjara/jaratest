import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

subject = 'pamo006'
paradigm = '2afc'
sessions = ['20211206a','20211205a','20211112a','20211111a','20211009a','20211006a']
#sessions = ['20220204a','20220203a','20220202a','20220201a']
#sessions = ['20220114a','20220115a','20220216a','20220217a']
bdata = behavioranalysis.load_many_sessions(subject, paradigm=paradigm, sessions=sessions)
'''
data analyzing part
'''
sessionID = bdata['sessionID'] + 1
nValid = bdata['nValid'] 
nReward = bdata['nRewarded']
valid = bdata['valid']
correct_rewarded = bdata['outcome'] == bdata.labels['outcome']['correct']
aftererror_rewarded = bdata['outcome'] == bdata.labels['outcome']['aftererror'] #no of correct trials type int
free_rewarded = bdata['outcome'] == bdata.labels['outcome']['free'] #no of correct trials type int
#free_rewarded = bdata['outcome'] == bdata.labels['outcome']['free']
outcome_mode = bdata['outcomeMode']
psycurve_mode = bdata['psycurveMode']
antibias_mode = bdata['antibiasMode']
no_of_rewardPress_r = bdata['rewardSide'] == bdata.labels['rewardSide']['right'] 
no_of_rewardPress_l = bdata['rewardSide'] == bdata.labels['rewardSide']['left'] 
choice_only_r = bdata['choice'] == bdata.labels['choice']['right']
successFull_trial_r=bdata['outcome']*choice_only_r #to get array for right side
choice_only_l = bdata['choice'] == bdata.labels['choice']['left'] 
successFull_trial_l=bdata['outcome']*choice_only_l

'''
creating data frame
'''
df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                          'N_valid': nValid,
                                          'N_reward': nReward,
                                          'valid': valid,
                                          'C_N rewards': correct_rewarded,
                                          'Ae_N rewards': aftererror_rewarded,
                                          'F_N rewards': free_rewarded,
                                          'l_reward_press':no_of_rewardPress_l,
                                          'r_reward_press':no_of_rewardPress_r,
                                          'l_success_trial':successFull_trial_l,
                                          'r_success_trial':successFull_trial_r,
                                          'out_mode':outcome_mode,
                                          'bias_mode':antibias_mode,
                                          'psy_mode':psycurve_mode
                                          })
                                                                     
session_information = df_trial_information.groupby(['sessionID'])
df_session_information = df_trial_information.groupby(['sessionID']).sum()
stage_information = df_trial_information.groupby(['sessionID']) .max()

psycurve_mode = stage_information['psy_mode']

condlist = [(stage_information['out_mode'] == 0) & (stage_information['psy_mode'] == 0), (stage_information['out_mode'] == 1) & (stage_information['psy_mode'] == 0), (stage_information['out_mode'] == 2) & (stage_information['psy_mode'] == 0), (stage_information['out_mode'] == 3) & (stage_information['psy_mode'] == 0),(stage_information['out_mode'] == 3) & (stage_information['psy_mode'] == 1)]
choicelist = ['0','1', 2, 3, 4]
choicelist_l=['Nan','Nan','Nan', round(((df_session_information['l_success_trial'] /df_session_information['l_reward_press']) *100),2), round(((df_session_information['l_success_trial'] /df_session_information['l_reward_press']) *100),2)]
choicelist_r=['Nan','Nan','Nan', round(((df_session_information['r_success_trial'] /df_session_information['r_reward_press']) *100),2), round(((df_session_information['r_success_trial'] /df_session_information['r_reward_press']) *100),2)]
stage_information['stage'] = np.select(condlist, choicelist)
valid_options = [df_session_information['valid'], df_session_information['valid'], df_session_information['valid'], df_session_information['valid'], df_session_information['valid']]
reward_options = [df_session_information['F_N rewards'],df_session_information['F_N rewards'], (df_session_information['C_N rewards']+df_session_information['Ae_N rewards']), df_session_information['C_N rewards'], df_session_information['C_N rewards']]
Valid_trials = np.select(condlist,valid_options).astype(np.int)
#an_array.astype(np.int)
rewarded = np.select(condlist,reward_options).astype(np.int)
print(type(Valid_trials))
print(type(rewarded))
Avgperformance = ((rewarded/Valid_trials)*100)
L_correct = np.select(condlist,choicelist_l)
R_correct = np.select(condlist,choicelist_r)
df_stage_information = pd.DataFrame({'Date': sessions,
                                          'stage': stage_information['stage'],
                                          'antibias': stage_information['bias_mode'],
                                          'val': Valid_trials,
                                          'rew': rewarded,
                                          'Avg_perf': np.round(Avgperformance,2),
                                          'L correctness':L_correct,
                                          'R correctness':R_correct
                                          })
'''                                          
                                          'C_N_reward':df_session_information['C_N rewards'],
                                          'F_N_reward':df_session_information['F_N rewards'],
                                          'Ae_N_reward':df_session_information['Ae_N rewards'],
                                          })
'''                                          
print(df_stage_information)

