from jaratoolbox import celldatabase

subject = 'd1pi043'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-01-13', 'right_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.65, 19.4
1.0: 2.45, 27.8
1.5: 3.22, 35.7
2.0: 3.82, 42.6
2.5: 4.45, 49.8
3.0: 5.58, 61.8
3.5: 6.35, 70.0
4.0: 7.42, 81.8
"""

# Animal in rig at: 11:02
# Probe in at: 11:15, resting at 700 um to see if brain lifts

exp0.add_site(2800, egroups=[7,8])
exp0.add_session('12-17-20', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-18-41', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('12-19-59', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-22-26', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-31-31', 'b', 'am','am_tuning_curve')
exp0.add_session('12-39-08', 'c', 'tuningCurve', 'am_tuning_curve')
# No laser information for this session as am_tuning.py was still set to present the green laser instead of the blue laser

exp0.add_site(3000, egroups=[6,7,8])
exp0.add_session('14-33-48', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-43-47', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-45-24', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-50-34', 'd', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-55-03', 'e', 'am','am_tuning_curve')

exp0.maxDepth = 3000

exp1 = celldatabase.Experiment(subject, '2020-01-14', 'right_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.60, 19.9
1.0: 2.12, 25.6
1.5: 2.74, 32.2
2.0: 3.40, 39.2
2.5: 4.00, 45.6
3.0: 4.92, 55.6
3.5: 5.60, 65.0
4.0: 6.55, 73.6
"""

# Animal in rig at: 10:37
# Probe in at: 10:42, reinserted at 11:40. Middle cant be penetrated due to large blood vessel abou 900 um deep

# exp1.add_site(2900, egroups=[2,4,6,7])
# exp1.add_session('12-14-54', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('12-16-03', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('12-17-36', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('12-19-36', 'a', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(3000, egroups=[1,2,4,6,7,8])
# exp1.add_session('12-34-46', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('12-35-52', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('12-37-01', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('12-38-35', 'b', 'tuningTest', 'am_tuning_curve')
# exp1.add_session('12-42-26', 'c', 'am', 'am_tuning_curve') # No am

# exp1.add_site(3100, egroups=[4,6,8])
# exp1.add_session('13-01-18', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('13-02-44', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('13-06-23', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('13-10-02', 'd', 'tuningTest', 'am_tuning_curve')
# exp1.add_session('13-13-47', 'e', 'am', 'am_tuning_curve') # No am

exp1.add_site(3300, egroups=[1,2,4,6,8])
exp1.add_session('13-36-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-37-21', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-38-32', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-40-06', 'f', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-43-29', 'g', 'am', 'am_tuning_curve') # Yes am
exp1.add_session('13-50-20', 'h', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3400, egroups=[2,4,6,8])
exp1.add_session('14-42-47', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-44-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-45-48', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-47-21', 'i', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-51-07', 'j', 'am', 'am_tuning_curve')

exp1.maxDepth = 3400

exp2 = celldatabase.Experiment(subject, '2020-01-15', 'left_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.75, 19.2
1.0: 2.54, 27.9
1.5: 3.30, 36.2
2.0: 4.05, 44.3
2.5: 4.82, 45.6
3.0: 5.82, 62.0
3.5: 6.42, 70.7
4.0: 7.80, 83.6
"""

# Animal in rig at:11:45
# Probe in at: 12:40; Had to attach a satellite dish as well as clean off a cell blockage. Decent amount of bleeding

# exp2.add_site(2900, egroups=[1,2,5,6,7])
# exp2.add_session('13-24-58', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('13-26-16', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('13-28-06', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('13-29-40', 'a', 'tuningTest', 'am_tuning_curve')
# exp2.add_session('13-33-39', 'b', 'am', 'am_tuning_curve') # No am

exp2.add_site(3000, egroups=[1,4,5,6,8])
exp2.add_session('14-06-40', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-08-00', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-09-39', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-13-02', 'c', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-16-44', 'd', 'am', 'am_tuning_curve')
exp2.add_session('14-24-10', 'e', 'tuningCurve', 'am_tuning_curve')

# exp2.add_site(3100, egroups=[2,4,5,6,8])
# exp2.add_session('15-14-11', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('15-15-26', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('15-26-40', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('15-18-15', 'f', 'tuningTest', 'am_tuning_curve')
# exp2.add_session('15-21-40', 'g', 'am', 'am_tuning_curve') # No am

exp2.add_site(3200, egroups=[6,8])
exp2.add_session('15-51-27', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-54-07', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-57-48', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-00-18', 'h', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-03-12', 'i', 'am', 'am_tuning_curve')
exp2.add_session('16-09-59', 'j', 'tuningCurve', 'am_tuning_curve')

exp2.maxDepth = 3200

exp3 = celldatabase.Experiment(subject, '2020-01-16', 'left_AudStr',
                               recordingTrack='medialDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp3)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 20.2
1.0: 1.85, 24.2
1.5: 2.30, 29.0
2.0: 2.85, 34.7
2.5: 3.45, 40.6
3.0: 4.10, 47.4
3.5: 5.32, 59.2
4.0: 6.30, 70.1
"""

# Animal in rig at: 10:45
# Probe in at: 11:15; Extensive bleeding again from the edge of the well as well as the anterior part of the craniotomy

exp3.add_site(3000, egroups=[1,2,5])
exp3.add_session('12-34-02', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-35-22', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('12-36-37', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('12-38-10', 'a', 'tuningTest', 'am_tuning_curve')
exp3.add_session('12-40-53', 'b', 'am', 'am_tuning_curve')
exp3.add_session('13-00-43', 'c', 'tuningCurve', 'am_tuning_curve')

# exp3.add_site(3100, egroups=[1,2,5,7])
# exp3.add_session('15-02-35', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('15-03-44', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('15-05-12', None, 'lasertrain', 'am_tuning_curve')
# exp3.add_session('15-06-58', 'd', 'tuningTest', 'am_tuning_curve')
# exp3.add_session('15-10-16', 'e', 'am', 'am_tuning_curve')

exp3.maxDepth = 3100

exp4 = celldatabase.Experiment(subject, '2020-01-17', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp4)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 20.2
1.0: 1.85, 24.2
1.5: 2.30, 29.0
2.0: 2.85, 34.7
2.5: 3.45, 40.6
3.0: 4.10, 47.4
3.5: 5.32, 59.2
4.0: 6.30, 70.1
"""

# Animal in rig at: 10:45
# Probe in at: 11:15; Extensive bleeding again from the edge of the well as well as the anterior part of the craniotomy

# ref TT6
# exp4.add_site(2800, egroups=[1,2,4])
# exp4.add_session('11-40-07', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('11-42-05', None, 'laserpulse', 'am_tuning_curve')
# exp4.add_session('11-43-22', None, 'lasertrain', 'am_tuning_curve')
# exp4.add_session('11-44-53', 'a', 'tuningTest', 'am_tuning_curve') # shit tuning, but one spike on TT2 has noise and laser response
# exp4.add_session('11-49-10', 'b', 'am', 'am_tuning_curve')

# changed ref to TT3
exp4.add_site(2900, egroups=[1,2,4,7,8])
exp4.add_session('12-08-12', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('12-09-35', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('12-10-45', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('12-12-15', 'c', 'tuningTest', 'am_tuning_curve')
exp4.add_session('12-15-21', 'd', 'am', 'am_tuning_curve')
exp4.add_session('12-21-52', 'e', 'tuningCurve', 'am_tuning_curve') # cells on TT2 look a little tuned

###### HEY MATT CONSIDER CHANGING THE DATE ON YOUR EXPERIMENT WHEN YOU COPY PASTE ########
# No

exp4.add_site(3000, egroups=[1,2,4])
exp4.add_session('13-02-43', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-04-53', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-06-07', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-07-56', 'f', 'tuningTest', 'am_tuning_curve')
exp4.add_session('13-11-04', 'g', 'am', 'am_tuning_curve')

exp4.add_site(3100, egroups=[1,2,4,8])
exp4.add_session('13-31-59', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-33-08', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-34-17', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-35-55', 'h', 'tuningTest', 'am_tuning_curve')
# exp4.add_session('13-39-51', 'i', 'am', 'am_tuning_curve')

exp4.add_site(3200, egroups=[1,2,4,7,8])
exp4.add_session('13-58-01', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-59-18', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('14-01-36', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('14-03-07', 'j', 'tuningTest', 'am_tuning_curve')
exp4.add_session('14-15-17', 'k', 'am', 'am_tuning_curve')

exp4.maxDepth = 3200
