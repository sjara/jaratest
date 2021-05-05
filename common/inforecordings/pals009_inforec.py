#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 13:47:42 2021

@author: jarauser
"""


from jaratoolbox import celldatabase

subject = 'pals009'
experiments=[]

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
exp0 = celldatabase.Experiment(subject, '2021-04-09', 'right_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp0)

# Add any relevant information about laser power, speakers used, probe used, etc.



# Animal in rig at: 12:40 (not exact)
# Probe in at: 1:30 (not exact)
# Site parameters: depth, tetrodes.
exp0.add_site(1076.1)
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_session('13-49-59', 'a', 'high frequency', 'bella_headfixed_2choice')
exp0.add_session('13-53-57', 'b', 'low frequency', 'bella_headfixed_2choice')


exp0.add_site(1108)
exp0.add_session('14-04-25 ', 'c' 'low frequency', 'bella_headfixed_2choice')
exp0.add_session('14-10-33', 'd' 'high frequency. bad run. same sounds next', 'bella_headfixed_2choice')
exp0.add_session('14-15-25', 'e' 'high frequency', 'bella_headfixed_2choice')


exp0.add_site(1208)
exp0.add_session('14-25-57', 'f' 'low frequency', 'bella_headfixed_2choice')
exp0.add_session('14-31-28', 'g' 'high frequency', 'bella_headfixed_2choice')

exp0.add_site(1309.8)
exp0.add_session('14-41-33', 'h' 'low frequency', 'bella_headfixed_2choice')
exp0.add_session('14-51-16', 'i' 'high frequency', 'bella_headfixed_2choice')

exp0.add_site(1398.4)
exp0.add_session('15-03-20', 'j' 'low frequency', 'bella_headfixed_2choice')
exp0.add_session('15-08-17', 'k' 'high frequency', 'bella_headfixed_2choice')

exp0.maxDepth = 1398.4
# Animal out at:13:08

# Animal in rig at: 10:40 (not exact)
# Probe in at: 11:23 
# Site parameters: depth, tetrodes.

exp1 = celldatabase.Experiment(subject, '2021-05-01', 'left_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
#experiments.append(exp2)


exp1.add_site(1265.3)
exp1.add_session('11-50-25', None, 'high & low frequency', 'bella_headfixed_2choice')
exp1.add_session('11-58-20', 'a', 'high & low frequency', 'bella_headfixed_2choice') #changed reference from tetrode 4 to 7


exp1.add_site(1365.3, tetrodes =[2,6,4,8])
exp1.add_session('12-10-03', 'b', 'high & low frequency', 'bella_headfixed_2choice')
exp1.add_session('12-21-17', 'c', 'high & low frequency', 'bella_headfixed_2choice') #changed reference from 7 to 5 

exp1.add_site(1461.2, tetrodes =[1,2,4,6,8])
exp1.add_session('12-32-05', 'd', 'high & low frequency', 'bella_headfixed_2choice')
exp1.add_session('12-40-33', 'e', 'high & low frequency', 'bella_headfixed_2choice') 

exp1.add_site(1551.1, tetrodes =[1,2,4,6,8])
exp1.add_session('12-50-32', 'f', 'high & low frequency', 'bella_headfixed_2choice')
exp1.add_session('12-56-19', 'g', 'high & low frequency', 'bella_headfixed_2choice')


exp1.maxDepth = 1551.1