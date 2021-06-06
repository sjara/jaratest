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
exp0.add_session('12-22-24', 'a', 'stage 1; high & low frequency', 'twochoice')
exp0.add_session('12-36-26', 'b', 'stage 1; high & low frequency', 'twochoice')

exp0.add_site(1135, tetrodes =[3, 4, 6, 7, 8])
exp0.add_session('12-55-52', 'c', 'stage 1; high & low frequency', 'twochoice')
exp0.add_session('13-05-12', 'd', 'stage 1; high & low frequency', 'twochoice')

exp0.add_site(1259, tetrodes =[4, 6, 8])
exp0.add_session('13-23-00', 'e', 'stage 1; high & low frequency', 'twochoice')
exp0.add_session('13-37-24', 'f', 'stage 1; high & low frequency', 'twochoice')

exp0.add_site(1357, tetrodes =[1, 4, 6, 7])
exp0.add_session('13-52-17', 'g', 'stage 1; high & low frequency', 'twochoice')
exp0.add_session('13-59-39', 'h', 'stage 1; high & low frequency', 'twochoice')

exp0.maxDepth = 1357


exp1 = celldatabase.Experiment(subject, '2021-06-02', 'right_AC', info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp1)


# Animal in rig at:12:36
# Probe in at: 12:50
# trained water restricted animal with water_on_sound (stage 1)

exp1.add_site(1046, tetrodes =[3, 5, 6, 8]) #TT2 Reference
exp1.add_session('12-59-06', 'a', 'stage 1; high & low frequency', 'twochoice')
exp1.add_session('13-06-21', 'b', 'stage 1; high & low frequency', 'twochoice')

exp1.add_site(1146, tetrodes =[1, 3, 6, 8]) #TT2 Reference
exp1.add_session('13-28-39', 'c', 'stage 1; high & low frequency', 'twochoice')
exp1.add_session('13-35-36', 'd', 'stage 1; high & low frequency', 'twochoice')

exp1.add_site(1246, tetrodes =[1, 3, 6, 8]) #TT1 Reference
exp1.add_session('13-49-11', 'e', 'stage 1; high & low frequency', 'twochoice')
exp1.add_session('13-57-06', 'f', 'stage 1; high & low frequency', 'twochoice')

exp1.add_site(1346, tetrodes =[3, 6, 7, 8]) #TT1 Reference
exp1.add_session('14-09-29', 'g', 'stage 1; high & low frequency', 'twochoice')
exp1.add_session('14-21-04', 'h', 'stage 1; high & low frequency', 'twochoice')

exp1.maxDepth = 1246

exp2 = celldatabase.Experiment(subject, '2021-06-03', 'right_AC', info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp2)

# Animal in rig at:2:00
# Probe in at: 2:11
# trained water restricted animal with water_on_sound (stage 2)

exp2.add_site(982, tetrodes =[4, 8, 6, 7]) #TT3 Reference. Mouse grooming and moving a lot.
exp2.add_session('14-20-32', 'a', 'stage 2; high & low frequency', 'twochoice')
exp2.add_session('14-32-30', 'b', 'stage 2; high & low frequency', 'twochoice')

exp2.add_site(1150, tetrodes =[2, 6, 8, 7]) #TT1 Reference. had to change probe, last one broke.
exp2.add_session('14-59-02', 'c', 'stage 2; high & low frequency', 'twochoice')
exp2.add_session('15-06-07', 'd', 'stage 2; high & low frequency', 'twochoice')

exp2.add_site(1250, tetrodes =[2, 3, 8, 7]) #TT6
exp2.add_session('15-18-55', 'e', 'stage 2; high & low frequency', 'twochoice')
exp2.add_session('15-28-15', 'f', 'stage 2; high & low frequency', 'twochoice')

exp2.add_site(1353, tetrodes =[2,6]) #TT5 Reference. had to change probe, last one broke.
exp2.add_session('15-41-54', 'g', 'stage 2; high & low frequency', 'twochoice')
exp2.add_session('15-51-00', 'h', 'stage 2; high & low frequency', 'twochoice')


exp2.maxDepth = 1353


exp3 = celldatabase.Experiment(subject, '2021-06-05', 'right_AC', info=[['TT1ant','soundLeft','A4x2-tet']])
experiments.append(exp3)

# Animal in rig at:
# Probe in at:
# trained water restricted animal with water_on_sound (stage 2)

exp3.add_site(1370, tetrodes =[4, 5, 7, 8]) #TT2 Reference
exp3.add_session('13-44-17', 'a', 'stage 1; high & low frequency', 'twochoice') #done using stage 1. after, all is in stage 2
exp3.add_session('13-54-26', 'b', 'stage 1; high & low frequency', 'twochoice')

exp3.add_site(1470, tetrodes =[3, 4, 5, 7, 8]) #TT1 Reference
exp3.add_session('14-08-03', 'c', 'stage 2; high & low frequency', 'twochoice')
exp3.add_session('14-17-04', 'd', 'stage 2; high & low frequency', 'twochoice')
exp3.add_session('14-25-22', 'e', 'stage 2; high & low frequency', 'twochoice') #short trial. edited the behavior code.
exp3.add_session('14-34-26', 'f', 'stage 2; high & low frequency', 'twochoice') #short trial. edited the behavior code.

exp3.add_site(1570, tetrodes =[4, 5, 6, 7, 8]) #TT1 Reference
exp3.add_session('14-49-51', 'g', 'stage 2; high & low frequency', 'twochoice')
exp3.add_session('14-59-59', 'h', 'stage 2; high & low frequency', 'twochoice')

exp3.add_site(1670, tetrodes =[2, 3, 4, 6, 7, 8]) #TT1 Reference
exp3.add_session('15-13-28', 'i', 'stage 2; high & low frequency', 'twochoice')
exp3.add_session('15-21-57', 'j', 'stage 2; high & low frequency', 'twochoice')
exp3.add_session('15-29-56', 'k', 'stage 1; high & low frequency', 'twochoice')#stage1

exp3.maxDepth = 1670
