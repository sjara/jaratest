# -*- coding: utf-8 -*-
"""
Created on Tue May 11 13:38:36 2021

@author: isabe
"""
"""
Plot histogram of lick times aligned to sound onset and sound change (on change detection task).
"""

import sys
import numpy as np
import pandas as pd
from pandas import DataFrame, ExcelWriter
import seaborn 
seaborn.set()
from matplotlib import pyplot as plt
from jaratoolbox import loadbehavior 
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis

    
subjects = ['pals010',
            'pals011',
            'pals012',
            'pals013',
            'pals014']
            

sessions = [#'20210530a', '20210531a', '20210601a', '20210602a', '20210603a', '20210604a', 
            #'20210605a', '20210606a','20210607a', '20210608a','20210609a'
            #'20210610a',  '20210611a', '20210612a', '20210613a', 
            '20210614a', '20210615a', '20210616a', '20210618a', '20210619a']
nSessions = (len(sessions))

paradigm = 'twochoice'  

mouse_lick = {}
for subject in subjects: 
    for session in sessions:
        #bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)
    
        behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        bdata = loadbehavior.BehaviorData(behavFile)  
        
        nTrials = len(bdata['outcome'])
        soundOnTime = np.empty(nTrials)
        playsound = bdata.stateMatrix['statesNames']['playTarget']
        lastEventThisTrial = 0
        
        
        for indTrial in range(nTrials):
            lastEventPreviousTrial = lastEventThisTrial
            lastEventThisTrial = bdata.events['indexLastEventEachTrial'][indTrial]
            statesThisTrial = bdata.events['nextState'][lastEventPreviousTrial:lastEventThisTrial]
            eventTimesThisTrial = bdata.events['eventTime'][lastEventPreviousTrial:lastEventThisTrial]
            if playsound in statesThisTrial:
                firstPlayPre = np.flatnonzero(statesThisTrial==playsound)[0]
                soundOnTime[indTrial] = eventTimesThisTrial[firstPlayPre]
            else:
                soundOnTime[indTrial] = np.nan
        
        leftLicksTimes = bdata.events['eventTime'][bdata.events['eventCode']==bdata.stateMatrix['eventsNames']['Lin']]
        rightLicksTimes = bdata.events['eventTime'][bdata.events['eventCode']==bdata.stateMatrix['eventsNames']['Rin']]
        
        
        
            
        timeRange = [-0.4,1]
        (lickTimesFromEventOnsetL,trialIndexForEachLickL,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(leftLicksTimes, soundOnTime, timeRange)
        (lickTimesFromEventOnsetR,trialIndexForEachLickR,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(rightLicksTimes, soundOnTime, timeRange)
        
        #trialIndexForEachLickL_array = trialIndexForEachLickL.ndarray
        df_trial_lick_left = pd.DataFrame({'lickTimesFromEventOnsetL': lickTimesFromEventOnsetL, 
                                      'trialIndexForEachLickL': trialIndexForEachLickL
                                      }) 
        
        first_lick_left = df_trial_lick_left.groupby(by =['trialIndexForEachLickL']) .min()
        average_licktime_left = round(first_lick_left['lickTimesFromEventOnsetL'].mean(), 3)
        
        
        
        df_trial_lick_right = pd.DataFrame({'lickTimesFromEventOnsetR': lickTimesFromEventOnsetR, 
                                      'trialIndexForEachLickR': trialIndexForEachLickR
                                      }) 
        
        first_lick_right = df_trial_lick_right.groupby(by =['trialIndexForEachLickR']) .min()
        average_licktime_right = round(first_lick_right['lickTimesFromEventOnsetR'].mean(), 3)
        
        mouse_lick[subject, session] = pd.DataFrame({'average_licktime_right': average_licktime_right,
                                                           'average_licktime_left': average_licktime_left}, index=[0])
       

        #mouse_lick.to_excel(r'C:\Users\isabe\data\behavior_graphs\pals_lickraster\average_licktimes.xlsx',  sheet_name='average_licktime', index = False)
        
        
        # fig = plt.figure() 
        # plt.scatter(subject, average_licktime_right, color = 'blue', label = 'Left')
        # # plt.plot(unique_sessionID, left_performance, color = 'blue')
        # # plt.scatter(unique_sessionID, right_performance, color = 'red' , label = 'Right')
        # # plt.plot(unique_sessionID, right_performance, color = 'red')
        # # plt.scatter(unique_sessionID, percent_correct, color = 'black', label = 'Percent Correct')
        # # plt.title(subject + 'Performance')
        # plt.xlabel('Sessions in stage 3-3.5')
        # plt.ylabel('average lick time')
        # # plt.legend(loc = 1)
        # #plt.xticks(ticks=unique_sessionID)
        # plt.ylim(0, 0.6)
        # plt.show() 
        
        #plotting the lick raster    
        fontsizeLabels = 14
        fig = plt.figure()
        #plt.clf()
        axTop = plt.subplot(2,1,1)
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
        xLabel = 'Time from first sound onset (s)'
        plt.plot(lickTimesFromEventOnsetL, trialIndexForEachLickL, '.k')
        plt.ylim([-1,nTrials])
        plt.ylabel('Trial', fontsize=fontsizeLabels)
        plt.title('Licks LEFT; first lick left average: {}' .format(average_licktime_left))
        plt.subplot(2,1,2, sharex=axTop)
        
        plt.plot(lickTimesFromEventOnsetR, trialIndexForEachLickR, '.k')
        plt.ylim([-1,nTrials])
        plt.xlim(timeRange)
        plt.ylabel('Trial', fontsize=fontsizeLabels)
        plt.xlabel('Time from sound onset (s)')
        plt.title('Licks RIGHT; first lick right average: {}' .format(average_licktime_right))
        plt.gcf().suptitle('{} - {}'.format(subject,session), fontweight='bold')
        # fig.savefig(r'C:\Users\isabe\data\behavior_graphs\pals_lickraster\{}_{}_lickraster.png' .format(subject, session), dpi=100)

        
