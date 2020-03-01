from jaratoolbox import celldatabase

subject = 'd1pi048'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-02-29', 'right_AudStr',
info=['anteriorDiI', 'TT1left', 'soundLeft', 'A4x2-tet'])
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

exp0.add_site(2900, tetrodes=[4,5,6,7,8])
exp0.add_session('13-38-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-40-20', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-41-29', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-43-18', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-45-35', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3000, tetrodes=[3,5,6,7,8])
exp0.add_session('14-02-49', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-04-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-05-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-07-12', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-09-31', 'd', 'am', 'am_tuning_curve')
exp0.add_session('14-15-37', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3100, tetrodes=[3,5,6,7,8])
exp0.add_session('14-55-32', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-56-40', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-57-52', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-59-47', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-02-05', 'g', 'am', 'am_tuning_curve')
exp0.add_session('15-08-08', 'h', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[3,5,6,7,8])
exp0.add_session('15-43-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-45-04', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-46-29', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-48-18', 'i', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-50-54', 'j', 'am', 'am_tuning_curve')
exp0.add_session('15-56-59', 'k', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, tetrodes=[3,5,6,7,8])
exp0.add_session('16-35-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-36-11', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-37-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-39-12', 'l', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-41-44', 'm', 'am', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[3,4,5,7,8])
exp0.add_session('16-57-36', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-58-48', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-59-57', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-01-47', 'n', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-04-10', 'o', 'am', 'am_tuning_curve')
exp0.add_session('17-10-17', 'p', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, tetrodes=[3,4,5,6,7])
exp0.add_session('17-47-22', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-48-41', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-50-06', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-52-22', 'q', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-54-42', 'r', 'am', 'am_tuning_curve')
exp0.add_session('18-00-51', 's', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, tetrodes=[3,4,5,6,7])
exp0.add_session('18-44-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-45-27', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-46-40', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-48-30', 't', 'tuningTest', 'am_tuning_curve')
exp0.add_session('18-50-51', 'u', 'am', 'am_tuning_curve')
exp0.add_session('18-56-58', 'v', 'tuningCurve', 'am_tuning_curve')

exp0.maxDepth = 3600
