from jaratoolbox import celldatabase

subject = 'd1pi042'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2019-09-07', 'right_AudStr', 'anteriourDiI',
    # info=['TT1left', 'soundLeft', 'A4x2-tet'])
# experiments.append(exp0)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
# #Used left speaker;laser (445 nm) set to 2.0 mW; Probe ????; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.4, 20.0
# 1.0: 1.8, 24.1
# 1.5: 2.3, 29.1
# 2.0: 2.85, 34.6
# 2.5: 3.4, 40.3
# 3.0: 4.0, 46.6
# 3.5: 5.0, 56.9
# 4.0: 5.95, 66.6
# """
#
# # Animal in rig at: 11:43
# # Probe in at:
#
# # Extensive bleeding in right craniotomy. Bled for an hour and a half before
# # being sealed with gel foam
#
# exp0.maxDepth = 0

exp1 = celldatabase.Experiment(subject, '2019-09-10', 'left_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 18.4
1.0: 1.95, 23.4
1.5: 2.60, 30.0
2.0: 3.20, 36.5
2.5: 3.75, 42.5
3.0: 4.40, 49.3
3.5: 5.32, 59.1
4.0: 6.10, 67.6
"""

# Animal in rig at: 10:40
# Probe in at:11:06

exp1.add_site(2500, egroups=[1,2,5,6,7,8])
exp1.add_session('12-14-05', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-15-19', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-17-02', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-18-47', 'a', 'tuningTest', 'am_tuning_curve')

exp1.add_site(2600, egroups=[1,5,6,7,8])
exp1.add_session('12-38-58', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-40-36', 'b', 'tuningTest', 'am_tuning_curve')

exp1.add_site(2700, egroups=[1,2,4,6,7,8])
exp1.add_session('13-50-32', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-51-53', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-53-36', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-55-47', 'c', 'tuningTest', 'am_tuning_curve')

exp1.add_site(2900, egroups=[1,2,3,7,8])
exp1.add_session('14-34-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-36-00', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-37-17', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-39-52', 'd', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3000, egroups=[1,2,4,7])
exp1.add_session('15-37-49', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-39-32', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-40-42', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-42-42', 'e', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3300, egroups=[7])
exp1.add_session('16-37-22', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-38-31', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-40-44', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-42-26', 'f', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3400, egroups=[1,3,4,6,7])
exp1.add_session('17-00-26', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-01-36', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-02-49', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-04-29', 'g', 'tuningTest', 'am_tuning_curve')

exp1.maxDepth = 3400

exp2 = celldatabase.Experiment(subject, '2019-09-11', 'left_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.52, 19.4
1.0: 2.15, 25.8
1.5: 2.80, 32.6
2.0: 3.50, 39.8
2.5: 4.15, 46.9
3.0: 5.18, 58.0
3.5: 5.98, 66.6
4.0: 6.95, 77.1
"""

# Animal in rig at:
# Probe in at: 11:01 (stopped initialy at 900 um for 10 min so brain could rise up)

exp2.add_site(2700, egroups=[1,2,7])
exp2.add_session('11-57-41', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-59-08', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-01-03', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-02-37', 'a', 'tuningTest', 'am_tuning_curve')

exp2.add_site(2800, egroups=[2,4,7])
exp2.add_session('12-26-26', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-27-51', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-29-07', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-30-40', 'b', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-34-30', 'c', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-03-47', 'd', 'am', 'am_tuning_curve')

exp2.add_site(2900, egroups=[1,2,3,4,7,8])
exp2.add_session('13-23-37', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-25-01', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-26-25', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-28-03', 'e', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-32-20', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-17-29', 'g', 'am', 'am_tuning_curve')

exp2.add_site(3000, egroups=[1,2,3,4,5,6,7,8])  # all sites seem to have spikes so no reference
exp2.add_session('14-50-11', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-51-42', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-52-52', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-54-24', 'h', 'tuningTest', 'am_tuning_curve')
exp2.add_session('15-02-00', 'i', 'tuningTest', 'am_tuning_curve') # Retried with reference on 3
exp2.add_session('15-07-32', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-38-49', 'k', 'am', 'am_tuning_curve')

exp2.add_site(3100, egroups=[1,2,3,4,6,7,8])
exp2.add_session('16-08-08', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-09-22', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-10-47', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-12-45', 'l', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-16-33', 'm', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-45-20', 'n', 'am', 'am_tuning_curve')

# very confusing site because SOMEONE JUST COPY PASTES ENTIRE BLOCKS OF CODE LIKE A NEANDERTHAL/DRAGOON
exp2.add_site(3200, egroups=[1,2,3,4,5,6,8])
exp2.add_session('17-04-00', 'o', 'tuningTest', 'am_tuning_curve') # moved reference to TT7
exp2.add_session('17-08-40', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('17-09-59', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('17-11-51', None, 'noiseburst', 'am_tuning_curve') # obligatory noisebursts because someone's fragile code doesn't work without them
exp2.add_session('17-13-05', 'p', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-50-48', 'q', 'am', 'am_tuning_curve')

exp2.add_site(3300, egroups=[1,2,3,4,5,6,8])
exp2.add_session('18-12-04', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('18-13-13', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('18-14-38', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('18-19-36', 'r', 'tuningTest', 'am_tuning_curve')
exp2.add_session('18-24-01', 's', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('18-53-34', 't', 'am', 'am_tuning_curve')

exp2.add_site(3400, egroups=[1,2,3,4,5,6,8])
exp2.add_session('19-13-34', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('19-14-55', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('19-16-28', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('19-24-04', 'u', 'tuningTest', 'am_tuning_curve')
exp2.add_session('19-30-15', 'v', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('19-59-17', 'w', 'am', 'am_tuning_curve')

exp2.maxDepth = 3400

# exp3 = celldatabase.Experiment(subject, '2019-09-17', 'left_AudStr', 'anteriorDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp3)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
# #Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.45, 20.3
# 1.0: 1.88, 24.9
# 1.5: 2.40, 30.2
# 2.0: 2.95, 36.0
# 2.5: 3.52, 41.9
# 3.0: 4.24, 49.4
# 3.5: 5.30, 60.5
# 4.0: 6.10, 69.0
# """

# Animal in rig at:10:47
# Probe in at:
# Animal has large amounts of bleeding on one side and sylgard fell out of the
# other creating a solidified surface. Removed decent amount of tissue but
# ultimately had to remove animal due to it hunching in pain while squeaking

# exp4 = celldatabase.Experiment(subject, '2019-09-18', 'left_AudStr', 'anteriorDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp4)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
# #Used left speaker;laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.45, 19.3
# 1.0: 1.92, 24.2
# 1.5: 2.40, 30.2
# 2.0: 3.05, 36.0
# 2.5: 3.65, 42.3
# 3.0: 4.28, 48.9
# 3.5: 5.25, 69.1
# 4.0: 6.00, 67.0
# """
#
# # Animal in rig at: 10:47
# # Probe in at:
