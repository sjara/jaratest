from jaratoolbox import celldatabase

subject = 'd1pi040'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-08-13', 'left_AudStr',
                               recordingTrack='anteriourDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M679; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.75
1.0: 2.7
1.5: 3.75
2.0: 4.95
2.5: 6.55
3.0: 8.3
"""

# Animal in rig at: 09:37
# Probe in at: 9:59

exp0.add_site(2400, egroups=[1,2,3,4,6,7,8])
exp0.add_session('10-16-09', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('10-19-11', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('10-20-33', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('10-22-27', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('10-30-03', 'b', 'tuningCurve', 'am_tuning_curve') # paused recording briefly to add saline
exp0.add_session('11-01-06', 'c', 'am', 'am_tuning_curve')

exp0.add_site(2500, egroups=[1,2,3,4,6,7,8])
exp0.add_session('11-19-16', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-20-27', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('11-21-42', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('11-23-15', 'd', 'tuningTest', 'am_tuning_curve')
exp0.add_session('11-29-00', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-03-39', 'f', 'am', 'am_tuning_curve')

exp0.add_site(2600, egroups=[1,2,3,4,6,7,8])
exp0.add_session('12-19-48', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-20-57', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-22-09', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-23-44', 'g', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-27-56', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-05-55', 'i', 'am', 'am_tuning_curve')

exp0.add_site(2700, egroups=[2,3,4,5,6,7,8])
exp0.add_session('14-08-41', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-10-33', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-12-06', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-13-57', 'j', 'tuningTest', 'am_tuning_curve')

exp0.add_site(2800, egroups=[2,3,4,5,6,7,8])
exp0.add_session('14-45-29', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-46-47', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-47-57', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-49-45', 'k', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-55-15', 'l', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-33-46', 'm', 'am', 'am_tuning_curve')

exp0.add_site(2900, egroups=[1,2,3,4,5,6,7,8])
exp0.add_session('15-52-49', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-01-32', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-02-45', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-04-34', 'n', 'tuningTest', 'am_tuning_curve')

exp0.add_site(3000, egroups=[1,2,3,4,5,6,7,8])
exp0.add_session('16-24-19', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-35-02', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-36-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-38-21', 'o', 'tuningTest', 'am_tuning_curve')

exp0.add_site(3100, egroups=[2,3,4,5,6,7,8])
exp0.add_session('16-38-21', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-57-43', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-59-33', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-01-05', 'p', 'tuningTest', 'am_tuning_curve')

exp0.maxDepth = 3100

exp1 = celldatabase.Experiment(subject, '2019-08-14', 'left_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M679; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.75
1.0: 2.75
1.5: 3.8
2.0: 4.8
2.5: 6.7
3.0: 8.7
"""

# Animal in rig at: 09:59
# Probe in at: 10:04

exp1.add_site(2450, egroups=[2,3,4,5,6,7,8])
exp1.add_session('10-20-16', None, 'noiseburst', 'am_tuning_curve')

exp1.add_site(2900, egroups=[2,3,4,5,6,7,8])
exp1.add_session('10-35-39', None, 'noiseburst', 'am_tuning_curve')

exp1.maxDepth = 2900

exp2 = celldatabase.Experiment(subject, '2019-08-15', 'left_AudStr',
                               recordingTrack='posteriourDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M679; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.82
1.0: 3.00
1.5: 3.98
2.0: 5.38
2.5: 6.84
3.0: 8.28
"""

# Animal in rig at: 10:20
# Probe in at: 10:31

exp2.maxDepth = 2400

exp3 = celldatabase.Experiment(subject, '2019-08-17', 'right_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp3)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe M679; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.75
1.0: 2.65
1.5: 3.6
2.0: 4.75
2.5: 6.35
3.0: 7.9
"""

# Animal in rig at: 11:50
# Probe in at: 12:02

# 12:46: a bunch of blood gathered in the well. Also all the signals are super quiet.

# exp3.add_site(2800, egroups=[1,2,3,4,6,7,8])
# exp3.add_session('12-55-17', None, 'noisebursts', 'am_tuning_curve')

# at 3100, signals even more quiet than before

exp3.maxDepth = 3300

exp4 = celldatabase.Experiment(subject, '2019-08-20', 'right_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp4)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe 76B1; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.50
1.0: 2.10
1.5: 2.80
2.0: 3.55
2.5: 4.35
3.0: 5.60
"""

# Animal in rig at: 12:07
# Had to wait for germinator to finish warming up: 12:17
# Probe in at: 12:23

exp4.add_site(2400, egroups=[1,2,3,4,5,6])
exp4.add_session('13-02-39', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-03-49', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-05-26', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-07-02', 'a', 'tuningTest', 'am_tuning_curve')

# Things seem to have gone quiet
# Drove to 2600 and saw nothing. Replaced with different probe with no dye and are attempting to go for the same location
# New probe: C39A

exp4.maxDepth = 2600

exp5 = celldatabase.Experiment(subject, '2019-08-21', 'right_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp5)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.50
1.0: 2.02
1.5: 2.60
2.0: 3.20
2.5: 3.85
3.0: 4.52
"""

# Animal in rig at: 13:10
# Probe in at: 13:12

exp5.add_site(2506, egroups=[1,2,3,4,5,6,7,8])
exp5.add_session('13-50-43', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('13-52-32', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('13-53-39', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('13-55-23', 'a', 'tuningTest', 'am_tuning_curve')

exp5.add_site(2600, egroups=[2])
exp5.add_session('14-55-55', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('14-50-18', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('14-51-48', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('14-53-33', 'b', 'tuningTest', 'am_tuning_curve')

exp5.add_site(2700, egroups=[1,2])
exp5.add_session('15-45-20', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('15-46-40', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('15-47-50', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('15-49-51', 'c', 'tuningTest', 'am_tuning_curve')

exp5.maxDepth = 2700

exp6 = celldatabase.Experiment(subject, '2019-08-22', 'right_AudStr',
                               recordingTrack='anteriorMidDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp6)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.45 20.0
1.0: 1.95 24.7
1.5: 2.48 30.4
2.0: 3.05 37.4
2.5: 3.65 44.4
3.0: 4.25 55.0
"""

# Animal in rig at: 12:17
# Probe in at: 12:21

exp6.add_site(2401, egroups=[6,7,8])
exp6.add_session('12-50-57', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('12-52-26', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('12-54-40', 'a', 'tuningTest', 'am_tuning_curve')

exp6.add_site(2600, egroups=[5,7,8])
exp6.add_session('13-13-03', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('13-14-22', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('13-16-12', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('13-18-52', 'b', 'tuningTest', 'am_tuning_curve')

exp6.add_site(2701, egroups=[5,7,8])
exp6.add_session('13-35-52', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('13-37-35', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('13-39-14', 'c', 'tuningTest', 'am_tuning_curve')

exp6.add_site(2800, egroups=[6,7,8])
exp6.add_session('13-57-08', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('13-58-43', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('13-59-55', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('14-02-27', 'd', 'tuningTest', 'am_tuning_curve')

exp6.add_site(2900, egroups=[6,7])
exp6.add_session('14-18-17', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('14-19-33', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('14-21-41', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('14-24-22', 'e', 'tuningTest', 'am_tuning_curve')

exp6.add_site(3000, egroups=[5,6,7,8])
exp6.add_session('14-42-35', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('14-44-21', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('14-45-52', 'f', 'tuningTest', 'am_tuning_curve')

# noticed ground was out of saline, put it back

exp6.add_site(3100, egroups=[8])
exp6.add_session('14-58-26', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-01-25', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('15-02-52', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('15-04-49', 'g', 'tuningTest', 'am_tuning_curve')

exp6.add_site(3200, egroups=[2,6])
exp6.add_session('15-26-10', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-27-21', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('15-28-34', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('15-31-14', 'h', 'tuningTest', 'am_tuning_curve')

exp6.add_site(3300, egroups=[1,2,5,6,8])
exp6.add_session('15-38-52', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-40-16', 'i', 'tuningTest', 'am_tuning_curve')
exp6.add_session('15-42-49', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('15-46-19', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('15-49-33', 'j', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('16-20-44', 'k', 'am', 'am_tuning_curve') # added some noise bursts to the end

exp6.add_site(3400, egroups=[1,5,6,8])
exp6.add_session('16-36-09', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('16-37-58', 'l', 'tuningTest', 'am_tuning_curve')
exp6.add_session('16-40-51', None, 'laserpulse', 'am_tuning_curve')

exp6.add_site(3500, egroups=[5,6,8]) # Removed tetrode 4 post recording
exp6.add_session('16-52-22', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('16-53-56', 'm', 'tuningTest', 'am_tuning_curve')
exp6.add_session('16-56-46', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('16-58-05', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('17-00-07', 'n', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('17-29-33', 'o', 'am', 'am_tuning_curve')

exp6.add_site(3600, egroups=[4,5,6,8])
exp6.add_session('17-41-16', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('17-42-33', 'p', 'tuningTest', 'am_tuning_curve')
exp6.add_session('17-44-53', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('17-46-19', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('17-48-11', 'q', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('18-21-55', 'r', 'am', 'am_tuning_curve')

exp6.add_site(3700, egroups=[3,4,5,6,8])
exp6.add_session('18-43-37', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('18-44-56', 's', 'tuningTest', 'am_tuning_curve')
exp6.add_session('18-47-40', None, 'laserpulse', 'am_tuning_curve')

exp6.add_site(3800, egroups=[4,6,8])
exp6.add_session('18-55-26', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('18-57-25', 't', 'tuningTest', 'am_tuning_curve')
exp6.add_session('19-00-35', None, 'laserpulse', 'am_tuning_curve')

exp6.add_site(3900, egroups=[2,4,6])
exp6.add_session('19-10-44', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('19-12-38', 'u', 'tuningTest', 'am_tuning_curve')
exp6.add_session('19-15-18', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('19-17-23', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('19-19-37', 'v', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('19-48-55', 'w', 'am', 'am_tuning_curve')
exp6.add_session('19-54-59', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('19-57-34', None, 'lasertrain', 'am_tuning_curve')

exp6.maxDepth = 3900
