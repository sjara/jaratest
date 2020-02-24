from jaratoolbox import celldatabase

subject = 'd1pi047'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2020-02-22', 'right_AudStr',
# info=['anteriorDiI', 'TT1left', 'soundLeft', 'A4x2-tet'])
# experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.85, 24.2
1.5: 2.3, 28.9
2.0: 2.95, 35.1
2.5: 3.35, 40.1
3.0: 3.95, 46.3
3.5: 4.85, 55.6
4.0: 5.7, 64.6
"""

# Animal in rig at: 11:47
# Animal out at: 1:12
# as per usual, mouse bled a ton from left craniotomy, so switched to right
# unfortunately, right craniotomy ALSO bled a ton
# decided not to record from him today seeing as he lost so much blood and should rest to recover
# mouse super unstable on feet when taken out of rig


exp0 = celldatabase.Experiment(subject, '2020-02-24', 'left_AudStr',
info=['anteriorDiI', 'TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.85, 24.2
1.5: 2.3, 28.9
2.0: 2.95, 35.1
2.5: 3.35, 40.1
3.0: 3.95, 46.3
3.5: 4.85, 55.6
4.0: 5.7, 64.6
"""

# Animal in rig at: 8:54
# Probe in at: 9:06

exp0.add_site(2900, tetrodes=[2,6,8])
exp0.add_session('09-20-33', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('09-21-43', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('09-23-19', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('09-25-39', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('09-28-11', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,2,3,4,6])
exp0.add_session('09-40-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('09-42-57', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('09-44-05', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('09-45-55', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('09-48-27', 'd', 'am', 'am_tuning_curve')
exp0.add_session('09-54-35', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, tetrodes=[1,2,3,4,6,8])
exp0.add_session('10-34-39', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('10-35-47', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('10-36-56', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('10-38-47', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('10-41-38', 'g', 'am', 'am_tuning_curve')
exp0.add_session('10-49-02', 'h', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[2,4,6,8])
exp0.add_session('11-37-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-39-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('11-40-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('11-43-17', 'i', 'tuningTest', 'am_tuning_curve')
exp0.add_session('11-45-40', 'j', 'am', 'am_tuning_curve')
exp0.add_session('11-52-22', 'k', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('12-51-25', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-52-51', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-53-59', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-56-03', 'l', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-58-21', 'm', 'am', 'am_tuning_curve')
exp0.add_session('13-05-01', 'n', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, tetrodes=[5,6,7,8])
exp0.add_session('14-18-44', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-20-18', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-23-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-25-16', 'o', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-27-51', 'p', 'am', 'am_tuning_curve')
exp0.add_session('14-34-44', 'q','tuningCurve','am_tuning_curve')

exp0.maxDepth = 3600
