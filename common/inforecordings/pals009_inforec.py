#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 13:47:42 2021

@author: jarauser
"""


from jaratoolbox import celldatabase

subject = 'pals001'
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

#exp1 = celldatabase.Experiment(subject, '2021-01-26', 'right_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
#experiments.append(exp1)



#exp1.maxDepth = 1308