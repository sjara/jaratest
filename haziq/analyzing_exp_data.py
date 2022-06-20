import numpy as np
import matplotlib.pyplot as plt
import csv

from jaratoolbox import loadbehavior  

# load data
subject = 'pamo026'                                                     
paradigm = '2afc'     
session = '20220310a'                                                   
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)    
#print(type(behavFile))  
bdata = loadbehavior.BehaviorData(behavFile) # bdata is string contains path 
#print(type(bdata))  
## Analyzing data

# counting no of valid trials, correct trial performed by animal and calculating average performance of animal in the session
valid_trials_count = np.count_nonzero(bdata['valid'] == True)  #no of valid trials type int    
correct_trials_count = np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['correct']) #no of correct trials type int
free_trials_count = np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['free']) #no of correct trials type int
#print (correct_trials_count)
#print (free_trials_count)
average_performance = (correct_trials_count/valid_trials_count)*100 # type float

#counting no of trials presented on each side by program
no_of_rewardPress_r = np.count_nonzero(bdata['rewardSide'] == bdata.labels['rewardSide']['right']) 
no_of_rewardPress_l = np.count_nonzero(bdata['rewardSide'] == bdata.labels['rewardSide']['left']) 

# counting no of choice animal make on each sides
no_of_choices_r = np.count_nonzero(bdata['choice'] == bdata.labels['choice']['right']) 
no_of_choices_l = np.count_nonzero(bdata['choice'] == bdata.labels['choice']['left']) 

# calculating the percentage of successfull trial for each side
#print(bdata['outcome'])
#print(bdata['choice'])
 
successFull_trial_r=bdata['outcome']*bdata['choice'] #to get array for right side
choice_l=np.logical_not(bdata['choice']).astype(int) #inverting to get array for left side
successFull_trial_l=bdata['outcome']*choice_l #to get array for left side

no_of_successFull_trial_r=np.count_nonzero(successFull_trial_r == 1) # counting trials for right side
no_of_successFull_trial_l=np.count_nonzero(successFull_trial_l == 1) # counting trials for left side

percent_for_correct_trial_right_side = (no_of_successFull_trial_r/no_of_rewardPress_r)*100
percent_for_correct_trial_left_side = (no_of_successFull_trial_l/no_of_rewardPress_l)*100


#print analsis results
print(f'Following information is regarding the exp  by {subject} performed on {session} ')
print(f'valid trials perforemd = 	{valid_trials_count}') 
print(f'correct trials perforemd = 	{correct_trials_count}') #(correct_trials_count)
print(f'The average performance = 	{average_performance:0.2f}%')
print(f'Percentage of correct trials on left side = {percent_for_correct_trial_left_side:0.2f}%,	right side = {percent_for_correct_trial_right_side:0.2f}%')
print(f'No. of reward presentation on 	left Side = {no_of_rewardPress_l},	right side = {no_of_rewardPress_r}')
print(f'No. of correct trials 		left Side = {no_of_successFull_trial_l},	right side = {no_of_successFull_trial_r}')   
print(f'No. of Animal choice were 	left Side = {no_of_choices_l},	right side = {no_of_choices_r}')





#print(successFull_trial_r)
#print(no_of_successFull_trial_r)
#print(no_of_successFull_trial_l)
#successFull_trial_l=

'''
print(np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['correct']))
print(np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['error']))
print(np.count_nonzero(bdata['outcome'] == bdata.labels['outcome']['nochoice']))

print(bdata['rewardSide'])
print(bdata['choice'])
print(bdata['outcome'])

'''




#print(f'trials with right side choice = {no_of_choices_r}')
#print(f'trials with left side choice = {no_of_choices_l}')
#print(f'trials with right side reward = {no_of_rewardPress_r}')
#print(f'trials with left side reward = {no_of_rewardPress_l}')


#print(successFull_trial_r)
#print(no_of_successFull_r)
#print(no_of_successFull_l)

#print(no_of_choices_r)
#print(no_of_choices_l)
#print(valid_trials_count)


