#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[ ]:

#this is just pulling values and categorizing them, so I can make a learning curve dictionary which makes plotting easier. 
path= r'file location'
filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

This lets you see many mice but only on one day
for nSub in range(len(subject)):
    behavFile = loadbehavior.path_to_behavior_data(subject[nSub], paradigm, session)
    bdata = loadbehavior.BehaviorData(behavFile)
    all_days_mice
# # Generating task varibles

# In[ ]:


taskMode=[] 
numLicksL=[]
numLicksR=[]

leftCorrect=[]
leftError =[]
leftInvalid=[]
rightCorrect=[]
rightError=[]
rightInvalid=[]
rightPercentCorrect=[]

leftTrials=[]
rightTrials=[]
leftChoice=[]
rightChoice=[]
valid=[]
noChoice=[]
earlyLick=[]

#start_time=[]
subject_name=[]

for ii,ff in enumerate(filenames):
    bdata = h5py.File(os.path.join(path,ff), "r")
 
    taskMode = bdata.labels['taskMode'][:][bdata['taskMode'][-1]] #hmm
    numLicksL = bdata['nLicksLeft'][:]
    numLicksR = bdata['nLicksRight'][:]
    
    if 'task_mode' in bdata:
        taskVersion=f['task_mode'][()]
    else:
        task_mode=''
    subjectName=f['subjectName'][()]
    #startTime=f['startTime'][()]  #not sure I need
    
    
    numInterruptL=0 #len(numInterruptL) Don't think this is a counter?
    numInterruptR=0
    numEarlyLicksL=0
    numEarlyLicksR=0
    numNoResponseL=0
    numNoResponseR=0
    
    if 'interrupt' in bdata.labels['outcome']: #think I need to add counter here +=1
        numInterruptL = bdata['nInterruptsLeft'][:]
        numInterruptR = bdata['nInterruptsRight'][:]
        numEarlyLicksL = bdata['nEarlyLicksLeft'][:]
        numEarlyLicksR = bdata['nEarlyLicksRight'][:]
        numNoResponseL = bdata['nNoResponsesLeft'][:]
        numNoResponseR = bdata['nNoResponsesRight'][:]
        
    if bdata['taskMode'][:] == bdata.labels['taskMode']['discriminate_stim']: #unsure if needed [-1]
        leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
        rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
        leftChoice = bdata['choice'] == bdata.labels['choice']['left']
        rightChoice = bdata['choice'] == bdata.labels['choice']['right']
        valid = bdata['choice'] != bdata.labels['choice']['none']
        noChoice = bdata['choice'] == bdata.labels['choice']['none']
        if 'interrupt' in bdata.labels['outcome']:
            earlyLick = bdata['outcome'] == bdata.labels['outcome']['earlyLick']
            interrupt = bdata['outcome'] == bdata.labels['outcome']['interrupt']
            noChoice = noChoice & ~earlyLick & ~interrupt
        else:
            earlyLick = bdata['outcome'] == bdata.labels['outcome']['falseAlarm']
            noChoice = noChoice & ~earlyLick
        
        leftCorrect = leftTrials & leftChoice
        leftError = leftTrials & rightChoice
        leftInvalid = leftTrials & noChoice
        rightCorrect = rightTrials & rightChoice
        rightError = rightTrials & leftChoice
        rightInvalid = rightTrials & noChoice
        rightPercentCorrect = round(sum(rightCorrect)/sum(rightTrials & valid)*100,2)
        leftPercentCorrect = round(sum(leftCorrect)/sum(leftTrials & valid)*100,2)
        
        taskMode.append(taskMode) 
        numLicksL.append(numLicksL) 
        numLicksR.append(numLicksR) 

        leftCorrect.append(leftCorrect) 
        leftError.append(leftError) 
        leftInvalid.append(leftInvalid) 
        rightCorrect.append(rightCorrect) 
        rightError.append(rightError) 
        rightInvalid.append(rightInvalid) 
        rightPercentCorrect.append(rightPercentCorrect) 

        leftTrials.append(leftTrials) 
        rightTrials.append(rightTrials) 
        leftChoice.append(leftChoice) 
        rightChoice.append(rightChoice) 
        valid=.append(valid) 
        noChoice.append(noChoice) 
        earlyLick.append(earlyLick) 

        #start_time=[]
        subject_name.append(subject_name) 


# In[ ]:


learning_curve_df={
    'taskMode':taskMode 
   'numLicksL':numLicksL
    'numLicksR':numLicksR 

    'leftCorrect':leftCorrect
    'taskMode':taskMode 
    'numLicksL':numLicksL
    'numLicksR':numLicksR

    'leftCorrect':leftCorrect
    'leftError':leftError
    'leftInvalid':leftInvalid
    'rightCorrect':rightCorrect
    'rightError':rightError
    'rightInvalid':rightInvalid
    'rightPercentCorrect':rightPercentCorrect

    'leftTrials':leftTrials
    'rightTrials':rightTrials
    'leftChoice':leftChoice
    'rightChoice:rightChoice
    'valid':valid
    'noChoice':noChoice
   ' earlyLick':earlyLick

    #start_time=[]
    'subject_name':subject_name
}

learning_curve_df=pd.DataFrame.from_dict(learning_curve_df)


# In[ ]:


#if we want to look at proportion of trials
fig,ax=plt.subplots(1,1,figsize=(9,4))

ax.plot(learning_curve_df['thing_one']/learning_curve_df['thing_two'])


ax.legend(['label', 'label'],bbox_to_anchor = (1.05, 0.6))
ax.set_ylabel('proportion of trials')
ax.set_xlabel('session')

plt.suptitle(subjectName)

fig.tight_layout()



# In[ ]:

#this lets us look at number of responses
fig2,ax2=plt.subplots()
#ax2=ax2.flatten()
plt.plot(Thing_one,color='green', linestyle='solid', label='# hits') 
plt.plot(Thing_two,color='red', linestyle='solid', label='# false alarms')
plt.plot(Over_all_response,color='blue', linestyle='solid', label='# of trials responded') 
plt.title(subjectName+' Responses')
plt.ylabel('Number of responses')
plt.xlabel('Day')
leg = ax2.legend();
plt.show()

