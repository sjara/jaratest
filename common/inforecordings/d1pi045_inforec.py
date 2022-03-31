from jaratoolbox import celldatabase

subject = 'd1pi045'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-02-07', 'left_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.55, 19.4
1.0: 2.20, 25.9
1.5: 2.95, 33.7
2.0: 3.65, 40.9
2.5: 4.55, 50.1
3.0: 5.75, 62.7
3.5: 6.80, 73.5
4.0: 8.65, 92.7
"""

# Animal in rig at: 9:25
# Probe in at: 9:40

exp0.add_site(2700, egroups=[2,8])
exp0.add_session('09-57-06', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2800, egroups=[1,2,5,6,7,8])
exp0.add_session('10-05-45', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('10-07-00', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('10-09-31', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('10-10-52', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('10-12-48', 'b', 'am', 'am_tuning_curve')

# sound may have not actually been presenting for this site?
exp0.add_site(2900, egroups=[1,2,5,6,7,8])
exp0.add_session('10-38-48', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('10-40-05', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('10-41-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('10-43-12', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('10-50-57', 'd', 'am', 'am_tuning_curve')
exp0.add_session('10-58-38', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3000, egroups=[7,8])
exp0.add_session('12-24-59', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(3100, egroups=[7,8])
exp0.add_session('12-34-16', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-36-23', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3200, egroups=[7,8])
# exp0.add_session('12-47-33', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-49-19', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3600, egroups=[5])
# exp0.add_session('13-43-15', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3700, egroups=[5,6])
# exp0.add_session('14-52-44', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('14-54-02', None, 'laserpulse', 'am_tuning_curve')

exp0.maxDepth = 3700


exp1 = celldatabase.Experiment(subject, '2020-02-08', 'left_AudStr',
                               recordingTrack='posteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe M680; Rig 2
# Probe D65D had extremely high impedances, so used M680 instead

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.4, 20.1
1.0: 1.8, 23.9
1.5: 2.25, 28.4
2.0: 2.8, 34.0
2.5: 3.2, 38.8
3.0: 3.75, 44.3
3.5: 4.45, 51.8
4.0: 5.35, 61.1
"""

# Animal in rig at: 1:10
# Probe in at: 1:22

exp1.add_site(2600, egroups=[1,2,5,6,7,8])
exp1.add_session('13-58-07', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-00-13', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-01-47', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-03-40', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-06-59', 'b', 'am', 'am_tuning_curve')
exp1.add_session('14-13-35', 'c', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2700, egroups=[1,5,6,7,8])
exp1.add_session('15-09-30', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-11-01', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-12-16', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-14-06', 'd', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-16-28', 'e', 'am', 'am_tuning_curve')
exp1.add_session('15-22-43', 'f', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2800, egroups=[1,2,5,6,7,8])
exp1.add_session('16-00-44', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-01-55', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-03-06', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-05-07', 'g', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-07-30', 'h', 'am', 'am_tuning_curve')
exp1.add_session('16-13-58', 'i', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2900, egroups=[5,6,7,8])
exp1.add_session('16-50-08', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-51-36', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-52-46', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-54-36', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-57-07', 'k', 'am', 'am_tuning_curve')

exp1.add_site(3000, egroups=[5,6,7,8])
exp1.add_session('17-09-48', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-11-02', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-12-11', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-14-26', 'l', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-16-46', 'm', 'am', 'am_tuning_curve')
exp1.add_session('17-22-52', 'n', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3100, egroups=[5,6,7,8])
exp1.add_session('17-59-20', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-00-29', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-01-46', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-03-35', 'o', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-05-57', 'p', 'am', 'am_tuning_curve')

exp1.add_site(3200, egroups=[1,5,6,7,8])
exp1.add_session('18-17-49', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-18-59', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-20-10', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-22-10', 'q', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-24-31', 'r', 'am', 'am_tuning_curve')
exp1.add_session('18-30-58', 's', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3300, egroups=[2,5,6,7,8])
exp1.add_session('19-07-35', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('19-08-57', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('19-10-26', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('19-12-20', 't', 'tuningTest', 'am_tuning_curve')
exp1.add_session('19-14-39', 'u', 'am', 'am_tuning_curve')

exp1.add_site(3400, egroups=[2,5,6,7,8])
exp1.add_session('19-25-39', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('19-26-50', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('19-28-57', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('19-30-48', 'v', 'tuningTest', 'am_tuning_curve')
exp1.add_session('19-33-09', 'w', 'am', 'am_tuning_curve')
exp1.add_session('19-39-15', 'x', 'tuningCurve', 'am_tuning_curve')

exp1.maxDepth = 3400


exp2 = celldatabase.Experiment(subject, '2020-02-09', 'left_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe M680; Rig 2
# Now M680 and D65D both have high impedance, using M680 because it gave good signals most recently

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 18.8
1.0: 1.85, 23.1
1.5: 2.35, 28.3
2.0: 2.95, 33.9
2.5: 3.5, 40.1
3.0: 4.1, 46.0
3.5: 4.85, 53.8
4.0: 5.85, 64.1
"""

# Animal in rig at: 11:26
# Probe in at: 11:38, shanks weren't penetrating, reinserted 12:02

exp2.add_site(2600, egroups=[2,5,6,7,8])
exp2.add_session('12-17-32', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-18-57', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-20-10', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-23-01', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-25-20', 'b', 'am', 'am_tuning_curve')

exp2.add_site(2700, egroups=[1,2,3,5,6,7,8])
exp2.add_session('12-39-44', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-41-03', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-42-15', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-44-19', 'c', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-46-37', 'd', 'am', 'am_tuning_curve')

exp2.add_site(2800, egroups=[1,2,3,5,6,7,8])
exp2.add_session('12-57-51', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-59-00', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-00-34', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-02-33', 'e', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-05-06', 'f', 'am', 'am_tuning_curve')

exp2.add_site(2900, egroups=[1,2,3,5,6,7,8])
exp2.add_session('13-16-50', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-17-59', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-19-21', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-21-13', 'g', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-23-31', 'h', 'am', 'am_tuning_curve')

exp2.add_site(3000, egroups=[1,2,4,5,6,7,8])
exp2.add_session('13-38-22', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-39-30', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-40-38', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-42-33', 'i', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-44-55', 'j', 'am', 'am_tuning_curve')
exp2.add_session('13-50-59', 'k', 'tuningCurve', 'am_tuning_curve')

# quality of recording decreased substantially after moving to 3100
# no longer using reference
exp2.add_site(3100, egroups=[2,3,4,8])
exp2.add_session('14-27-20', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-28-36', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-29-48', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-31-41', 'l', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-34-16', 'm', 'am', 'am_tuning_curve')

# back to using a reference
exp2.add_site(3200, egroups=[2,3,4,5,6,7,8])
exp2.add_session('14-48-14', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-49-26', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-50-34', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-52-27', 'n', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-55-10', 'o', 'am', 'am_tuning_curve')

exp2.add_site(3300, egroups=[2,3,4,5,6,7,8])
exp2.add_session('15-07-42', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-09-02', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-10-15', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-14-02', 'p', 'tuningTest', 'am_tuning_curve')
exp2.add_session('15-16-26', 'q', 'am', 'am_tuning_curve')

exp2.add_site(3400, egroups=[1,2,3,4,5,6,8])
exp2.add_session('15-28-00', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-29-10', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-30-19', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-32-10', 'r', 'tuningTest', 'am_tuning_curve')
exp2.add_session('15-34-29', 's', 'am', 'am_tuning_curve')

# exp2.add_site(3500, egroups=[4])
# exp2.add_session('15-45-34', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('15-46-42', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('15-47-52', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('15-49-45', 't', 'tuningTest', 'am_tuning_curve')
# exp2.add_session('15-52-42', 'u', 'am', 'am_tuning_curve')

# signals went away for good

exp2.maxDepth = 3500


# exp3 = celldatabase.Experiment(subject, '2020-02-11', 'right_AudStr', 'posteriorDiI',
#     info=['TT1left', 'soundLeft', 'A4x2-tet'])
# experiments.append(exp3)
#
# # 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# # Used left speaker; laser (445 nm) set to 2.0 mW; Probe P429; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.5, 19.7
# 1.0: 1.95, 24.4
# 1.5: 2.5, 30.4
# 2.0: 3.15, 36.6
# 2.5: 3.65, 42.5
# 3.0: 4.45, 50.4
# 3.5: 5.5, 61.9
# 4.0: 6.2, 69.3
# """
#
# # Animal in rig at: 9:10, bleeding pretty heavily from right craniotomy
# # Probe in at: 9:30, started bleeding again during penetration, pulled out, stuck in diagonally 9:50
#
# exp3.add_site(2900, egroups=[1,2,3,6,7])
# exp3.add_session('10-02-48', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('10-02-48', None, 'laserpulse', 'am_tuning_curve')
#
# # Upon opening rig, mouse and wheel were covered in blood
# exp3.maxDepth = 2900
