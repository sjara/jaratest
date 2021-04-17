# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from jaratoolbox import celldatabase

subject = 'pals001'
experiments=[]

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
exp0 = celldatabase.Experiment(subject, '2021-01-21', 'right_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp0)

# Add any relevant information about laser power, speakers used, probe used, etc.



# Animal in rig at: 11:30 (not exact)
# Probe in at: 12:30 (not exact)
# Site parameters: depth, tetrodes.
exp0.add_site(1000)
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_session('11-37-44', None, 'test', 'am_tuning_curve')
exp0.add_session('12-27-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-40-41', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-59-14', 'b', 'am', 'am_tuning_curve')


exp0.add_site(1100)
exp0.add_session('13-20-17', 'c' 'am', 'am_tuning_curve')
exp0.add_session('13-32-55', 'd' 'tuningTest', 'am_tuning_curve')

exp0.add_site(1205)
exp0.add_session('13-44-32', 'e' 'am', 'am_tuning_curve')
exp0.add_session('13-55-00', 'f' 'tuningTest', 'am_tuning_curve')


exp0.maxDepth = 1205
# Animal out at:13:08

exp1 = celldatabase.Experiment(subject, '2021-01-26', 'right_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp2)


exp1.add_site(1000.2, tetrodes =[2, 3, 4, 8])
exp1.add_session('12-56-58', 'am', 'g', 'am_tuning_curve')
exp1.add_session('13-09-46', 'tuningtest', 'h', 'am_tuning_curve')


exp1.add_site(1205, teterodes=[1, 3, 4, 6, 7, 8])
exp1.add_session('13-17-09', 'am', 'i', 'am_tuning_curve')
exp1.add_session('13-27-14', 'tuningtest', 'j', 'am_tuning_curve')

exp1.add_site(1308, teterodes=[1, 2, 3, 6, 7, 8])
exp1.add_session('13-31-23', 'am', 'k', 'am_tuning_curve')
exp1.add_session('13-42-55', 'tuningtest', 'l', 'am_tuning_curve')



exp1.maxDepth = 1308