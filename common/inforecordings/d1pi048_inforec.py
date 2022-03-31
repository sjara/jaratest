from jaratoolbox import celldatabase


subject = 'd1pi048'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-02-29', brainArea='right_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 20.1
1.0: 2.0, 25.1
1.5: 2.55, 30.8
2.0: 3.25, 37.9
2.5: 3.85, 44.6
3.0: 4.95, 55.4
3.5: 6.05, 66.9
4.0: 7.2, 78.9
"""

# Animal in rig at: 1:10
# Probe in at: 1:28 (three shanks, no TT1/2)

exp0.add_site(2900, egroups=[4,5,6,7,8])
exp0.add_session('13-38-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-40-20', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-41-29', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-43-18', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-45-35', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3000, egroups=[3,5,6,7,8])
exp0.add_session('14-02-49', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-04-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-05-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-07-12', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-09-31', 'd', 'am', 'am_tuning_curve')
exp0.add_session('14-15-37', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3100, egroups=[3,5,6,7,8])
exp0.add_session('14-55-32', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-56-40', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-57-52', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-59-47', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-02-05', 'g', 'am', 'am_tuning_curve')
exp0.add_session('15-08-08', 'h', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, egroups=[3,5,6,7,8])
exp0.add_session('15-43-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-45-04', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-46-29', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-48-18', 'i', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-50-54', 'j', 'am', 'am_tuning_curve')
exp0.add_session('15-56-59', 'k', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, egroups=[3,5,6,7,8])
exp0.add_session('16-35-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-36-11', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-37-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-39-12', 'l', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-41-44', 'm', 'am', 'am_tuning_curve')

exp0.add_site(3400, egroups=[3,4,5,7,8])
exp0.add_session('16-57-36', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-58-48', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-59-57', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-01-47', 'n', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-04-10', 'o', 'am', 'am_tuning_curve')
exp0.add_session('17-10-17', 'p', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, egroups=[3,4,5,6,7])
exp0.add_session('17-47-22', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-48-41', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-50-06', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-52-22', 'q', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-54-42', 'r', 'am', 'am_tuning_curve')
exp0.add_session('18-00-51', 's', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, egroups=[3,4,5,6,7])
exp0.add_session('18-44-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-45-27', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-46-40', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-48-30', 't', 'tuningTest', 'am_tuning_curve')
exp0.add_session('18-50-51', 'u', 'am', 'am_tuning_curve')
exp0.add_session('18-56-58', 'v', 'tuningCurve', 'am_tuning_curve')

exp0.maxDepth = 3600


exp1 = celldatabase.Experiment(subject, '2020-03-01', 'right_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft'])
experiments.append(exp1)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P429/D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 20.3
1.0: 1.85, 24.7
1.5: 2.35, 29.7
2.0: 2.95, 35.9
2.5: 3.45, 41.1
3.0: 4.0, 47.0
3.5: 4.95, 56.8
4.0: 5.7, 65.3
"""

# Animal in rig at: 12:09
# Probe P429 in at: 12:15
# Probe seemed fine at first, but signals went away pretty quickly when I descended to 3000
# Probe D65D in at: 12:31 (three shanks, no TT1/2)

exp1.add_site(3000, egroups=[3,4,6,7,8])
exp1.add_session('12-40-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-41-56', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-43-06', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-44-56', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-47-16', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3200, egroups=[7,8])
exp1.add_session('13-01-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-02-47', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-03-58', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-06-02', 'c', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-08-23', 'd', 'am', 'am_tuning_curve')

exp1.add_site(3400, egroups=[7])
exp1.add_session('13-38-38', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-39-47', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-40-55', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-42-48', 'e', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-45-15', 'f', 'am', 'am_tuning_curve')
exp1.add_session('13-51-22', 'g', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3500, egroups=[7,8])
exp1.add_session('14-29-15', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-30-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-31-37', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-33-28', 'h', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-35-48', 'i', 'am', 'am_tuning_curve')

exp1.add_site(3600, egroups=[7])
exp1.add_session('14-50-05', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-51-16', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-52-44', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-54-34', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-57-49', 'k', 'am', 'am_tuning_curve')

exp1.add_site(3700, egroups=[3,5,7,8])
exp1.add_session('15-13-01', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-14-11', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-15-20', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-17-33', 'l', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-19-55', 'm', 'am', 'am_tuning_curve')
exp1.add_session('15-26-18', 'n', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3800, egroups=[3,5,7,8])
exp1.add_session('16-09-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-10-33', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-11-42', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-13-33', 'o', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-16-14', 'p', 'am', 'am_tuning_curve')

exp1.add_site(3900, egroups=[3,5,7])
exp1.add_session('16-30-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-31-42', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-32-53', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-34-44', 'q', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-37-15', 'r', 'am', 'am_tuning_curve')

exp1.add_site(4000, egroups=[7])
exp1.add_session('16-51-25', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-52-34', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-53-45', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-55-51', 's', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-58-41', 't', 'am', 'am_tuning_curve')

exp1.maxDepth = 4000


exp2 = celldatabase.Experiment(subject, '2020-03-02', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight'])
experiments.append(exp2)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.1
1.0: 2.05, 24.5
1.5: 2.7, 31.2
2.0: 3.35, 37.7
2.5: 4.05, 44.9
3.0: 4.95, 54.5
3.5: 6.05, 65.9
4.0: 6.85, 73.9
"""

# Animal in rig at: 10:18
# Probe in at: 10:34 (three shanks, no TT1/2)

exp2.add_site(3300, egroups=[4,6])
exp2.add_session('11-30-09', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-31-19', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('11-32-27', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-33-57', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('11-36-18', 'b', 'am', 'am_tuning_curve')
exp2.add_session('11-42-21', 'c', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3400, egroups=[3,4,6])
exp2.add_session('12-44-49', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-45-58', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-47-07', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-49-24', 'd', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-51-58', 'e', 'am', 'am_tuning_curve')

exp2.add_site(3600, egroups=[3,4,5,6])
exp2.add_session('14-44-44', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-45-54', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-47-03', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-48-34', 'f', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-51-56', 'g', 'am', 'am_tuning_curve')

exp2.add_site(3700, egroups=[3,4,5,6])
exp2.add_session('15-28-45', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-29-54', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-31-03', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-33-17', 'h', 'tuningTest', 'am_tuning_curve')
exp2.add_session('15-35-50', 'i', 'am', 'am_tuning_curve')

exp2.add_site(3800, egroups=[3,4,5,6])
exp2.add_session('15-52-10', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-53-28', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-55-22', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-58-41', 'j', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-02-14', 'k', 'am', 'am_tuning_curve')
exp2.add_session('16-08-22', 'l', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-36-57', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-38-07', None, 'lasertrain', 'am_tuning_curve')

exp2.add_site(3900, egroups=[3,4])
exp2.add_session('16-49-11', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-50-31', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-51-42', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-53-44', 'm', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-56-05', 'n', 'am', 'am_tuning_curve')
exp2.add_session('17-02-06', 'o', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(4000, egroups=[3,4])
exp2.add_session('17-40-14', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('17-41-26', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('17-42-46', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('17-44-52', 'p', 'tuningTest', 'am_tuning_curve')
exp2.add_session('17-48-58', 'q', 'am', 'am_tuning_curve')
exp2.add_session('17-55-03', 'r', 'tuningCurve', 'am_tuning_curve')

exp2.maxDepth = 4000

# exp3 = celldatabase.Experiment(subject, '2020-03-03', 'left_AudStr', 'middleDiD',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp3)
#
# # 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# # Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2; THREE SHANKER ALERT (missing shank 1)
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.45, 19.3
# 1.0: 1.94, 24.1
# 1.5: 2.48, 29.7
# 2.0: 3.02, 35.4
# 2.5: 3.65, 42.0
# 3.0: 4.30, 48.8
# 3.5: 5.45, 60.5
# 4.0: 6.30, 69.3
# """
#
# # Animal in rig at: 10:49
# # Probe in at: 10:58 (three shanks, no TT1/2)
#
# # Initial signals look suspiciously quiet
# exp3.maxDepth = 3300


# exp4 = celldatabase.Experiment(subject, '2020-03-04', 'left_AudStr', 'posteriorDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp4)
#
# # 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# # Used right speaker; laser (445 nm) set to 2.0 mW; Probe P429; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.5, 19.1
# 1.0: 2.05, 24.5
# 1.5: 2.7, 31.2
# 2.0: 3.35, 37.7
# 2.5: 4.05, 44.9
# 3.0: 4.95, 54.5
# 3.5: 6.05, 65.9
# 4.0: 6.85, 73.9
# """
#
# # Animal in rig at: 11:15
# # Probe in at: 11:21
#
# # Again, signals look quiet
# # Changed to M680
#
# exp4.add_site(3100, egroups=[2,8])
# exp4.add_session('13-13-43', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('13-14-55', None, 'laserpulse', 'am_tuning_curve')
# exp4.add_session('13-16-03', None, 'lasertrain', 'am_tuning_curve')
# exp4.add_session('13-17-35', 'a', 'tuningTest', 'am_tuning_curve')
# exp4.add_session('13-20-39', 'b', 'am', 'am_tuning_curve')
#
# # Signals went away again...
# exp4.maxDepth = 3200
