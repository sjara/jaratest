#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:47:32 2021

@author: jarauser
"""


from jaratoolbox import celldatabase

subject = 'pals002'
experiments=[]

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
exp0 = celldatabase.Experiment(subject, '2021-02-04', 'right_AC', None, info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp0)

# Add any relevant information about laser power, speakers used, probe used, etc.



# Animal in rig at: 9:45 
# Probe in at: 
# Site parameters: 11:15 depth, tetrodes.
exp0.add_site(795)
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_session('11-18-07', 'a', 'psycurve_test', 'headfixed_twochoice')
exp0.add_session('11-26-48', 'b', 'tuningtest', 'am_tuning_curve')
exp0.add_session('11-33-09', 'c', 'am', 'am_tuning_curve')
exp0.add_session('11-47-42', 'd', 'chord', 'am_tuning_curve')

exp0.add_site(1102)
exp0.add_session('12-01-39', 'e' 'tuningtest', 'am_tuning_curve')
exp0.add_session('12-05-24', 'f' 'chord', 'am_tuning_curve')

exp0.add_site(1210)
exp0.add_session('12-15-27', 'g' 'tuningtest', 'am_tuning_curve')
exp0.add_session('12-19-00', 'h' 'chord', 'am_tuning_curve')


exp0.maxDepth = 1210
# Animal out at:12:45
