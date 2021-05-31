#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:14:18 2021

@author: jarauser
"""
from jaratoolbox import celldatabase

subject = 'pals015'
experiments=[]

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
exp0 = celldatabase.Experiment(subject, '2021-05-31', 'right_AC', info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp0)


# Add any relevant information about laser power, speakers used, probe used, etc.
# first session done using tetrode 4 as a reference channel, second session done using tetrode 2. After first session all done with tetrode 2 as reference.


# Animal in rig at: 12:03
# Probe in at: 12:14
# Site parameters: depth, tetrodes.
exp0.add_site(1003, tetrodes =[3,6,7,8])
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_session('12-22-24', 'a', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')
exp0.add_session('12-36-26', 'b', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')

exp0.add_site(1135, tetrodes =[3, 4, 6, 7, 8])
exp0.add_session('12-55-52', 'c', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')
exp0.add_session('13-05-12', 'd', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')

exp0.add_site(1259, tetrodes =[4, 6, 8])
exp0.add_session('13-23-00', 'e', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')
exp0.add_session('13-37-24', 'f', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')

exp0.add_site(1357, tetrodes =[1,4, 6, 7])
exp0.add_session('13-52-17', 'g', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')
exp0.add_session('13-59-39', 'h', 'stage 1; high & low frequency', 'bellatest_headfixed_twochoice.py')

exp0.maxDepth = 1357
