from jaratoolbox import celldatabase

subject = 'd1pi044'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-01-21', 'right_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM
#Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.1
1.0: 2.00, 24.7
1.5: 2.50, 29.7
2.0: 3.08, 35.9
2.5: 3.82, 43.2
3.0: 4.70, 52.1
3.5: 6.00, 64.5
4.0: 7.05, 75.3
"""

# Animal in rig at: 11:04
# Probe in at: 11:23

# NO TUNING CURVE ONLY TUNING TEST
# exp0.add_site(2807, egroups=[1,2,6])
# exp0.add_session('11-52-44', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('11-54-29', 'a', 'tuningTest', 'am_tuning_curve')

exp0.add_site(2901, egroups=[1,2,4])
exp0.add_session('12-13-24', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-14-55', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-16-20', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-18-52', 'b', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-21-56', 'c', 'am', 'am_tuning_curve')

exp0.add_site(3000, egroups=[1,2])
exp0.add_session('12-39-02', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-40-24', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-42-25', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-45-07', 'd', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-51-53', 'e', 'am', 'am_tuning_curve')

exp0.add_site(3100, egroups=[1,2,8])
exp0.add_session('13-15-27', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-16-45', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-18-05', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-19-57', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-23-14', 'g', 'am', 'am_tuning_curve')

exp0.maxDepth = 3100

exp1 = celldatabase.Experiment(subject, '2020-01-23', 'right_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM
#Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.50, 18.9
1.0: 2.00, 23.7
1.5: 2.60, 30.3
2.0: 3.25, 37.0
2.5: 3.90, 43.2
3.0: 4.75, 52.2
3.5: 6.30, 67.5
4.0: 7.50, 79.6
"""

# Animal in rig at: 11:22
# Probe in at: 11:30

# exp1.add_site(3000, egroups=[8])
# exp1.add_session('12-12-49', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('12-14-08', 'a', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(3100, egroups=[8])
# exp1.add_session('12-39-47', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('12-41-54', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('12-43-29', 'b', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(3300, egroups=[7])
# exp1.add_session('13-21-42', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('13-23-15', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('13-25-41', 'c', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(3400, egroups=[2,4,6,8])
# exp1.add_session('13-38-32', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('13-41-27', 'd', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(3500, egroups=[3,4,6])
# exp1.add_session('13-58-09', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('14-00-00', 'e', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3600, egroups=[4,6])
exp1.add_session('14-11-37', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-14-10', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-16-04', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-19-45', 'f', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-25-38', 'g', 'am', 'am_tuning_curve')
exp1.add_session('14-33-45', 'h', 'tuningCurve', 'am_tuning_curve')

exp1.maxDepth = 3600

# exp2 = celldatabase.Experiment(subject, '2020-01-27', 'left_AudStr', 'posteriorDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp2)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM
# #Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.60, 18.9
# 1.0: 2.25, 25.7
# 1.5: 2.92, 33.3
# 2.0: 3.50, 39.0
# 2.5: 4.10, 43.2
# 3.0: 4.95, 54.8
# 3.5: 5.80, 64.1
# 4.0: 6.45, 71.2
# """
#
# # Animal in rig at: 11:02
# # Probe in at: 11:24
#
# # Mouse started bleeding after probe was inside. Signlas are wonky
# # Moving from 2900 to 3100 seems to have helped stabilize the signals
# # exp2.add_site(3100, egroups=[6])
# # exp2.add_session('11-57-49', None, 'noiseburst', 'am_tuning_curve')
# # exp2.add_session('11-59-00', None, 'laserpulse', 'am_tuning_curve')
# # exp2.add_session('12-00-09', None, 'lasertrain', 'am_tuning_curve')
# # exp2.add_session('12-01-45', 'a', 'tuningTest', 'am_tuning_curve')
#
# # exp2.add_site(3400, egroups=[3,4])
# # exp2.add_session('12-43-41', None, 'noiseburst', 'am_tuning_curve')
# # exp2.add_session('12-45-03', None, 'laserpulse', 'am_tuning_curve')
# # exp2.add_session('12-46-47', None, 'lasertrain', 'am_tuning_curve')
# # exp2.add_session('12-48-56', 'b', 'tuningTest', 'am_tuning_curve')
#
# exp2.maxDepth = 3400

exp3 = celldatabase.Experiment(subject, '2020-01-28', 'left_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp3)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM
#Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.60, 18.9
1.0: 2.25, 25.7
1.5: 2.92, 33.3
2.0: 3.50, 39.0
2.5: 4.10, 43.2
3.0: 4.95, 54.8
3.5: 5.80, 64.1
4.0: 6.45, 71.2
"""

# Animal in rig at: 10:31
# Probe in at: 10:37
# Went to 2900

# exp3.add_site(3000, egroups=[2,4])
# exp3.add_session('11-01-29', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('11-02-43', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('11-07-09', None, 'lasertrain', 'am_tuning_curve')
# exp3.add_session('11-09-46', 'a', 'tuningTest', 'am_tuning_curve')

exp3.add_site(3500, egroups=[2,4])
exp3.add_session('12-18-54', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-21-03', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('12-22-29', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('12-26-12', 'b', 'tuningTest', 'am_tuning_curve')
exp3.add_session('12-37-58', 'c', 'tuningCurve', 'am_tuning_curve')

exp3.maxDepth = 3600
