from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'd1pi042'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-09-07', 'right_AudStr',
info=['anteriourDiI', 'TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe ????; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 18.6
1.0: 2.0, 24.0
1.5: 2.6, 30.3
2.0: 3.3, 37.3
2.5: 4.0, 44.4
3.0: 4.85, 53.0
3.5: 5.85, 63.5
4.0: 6.75, 73.0
"""

# Animal in rig at: 
# Probe in at:
