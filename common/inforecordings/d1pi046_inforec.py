from jaratoolbox import celldatabase

subject = 'd1pi046'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-02-15', 'right_AudStr',
info=['anteriorDiI', 'TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.0
1.0: 2.05, 24.5
1.5: 2.7, 31.2
2.0: 3.35, 38.0
2.5: 4.05, 45.1
3.0: 4.95, 54.2
3.5: 6.0, 65.5
4.0: 6.85, 74.2
"""

# Animal in rig at: 2:20
# Probe in at: 3:32
# originally wanted to record from left, but mouse bled a ton there,
# so went to right instead to avoid what happened with 45

exp0.add_site(2700, tetrodes=[2,4,5,6,7,8])
# exp0.add_session('16-04-25', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('16-05-56', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('16-07-10', None, 'lasertrain', 'am_tuning_curve')
# changed reference to TT3 because TT5 was getting huge noise from laser
exp0.add_session('16-09-42', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-10-59', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-12-08', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-14-01', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-17-14', 'b', 'am', 'am_tuning_curve')

exp0.add_site(2800, tetrodes=[1,2,5,6,8])
exp0.add_session('16-34-25', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-35-35', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-36-44', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-38-32', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-41-05', 'd', 'am', 'am_tuning_curve')
exp0.add_session('16-47-31', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('17-25-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-26-27', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-27-41', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-29-38', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-32-14', 'g', 'am', 'am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('17-46-14', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-47-26', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-48-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-50-25', 'h', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-52-57', 'i', 'am', 'am_tuning_curve')

exp0.add_site(3100, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('18-07-12', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-08-23', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-09-32', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-11-22', 'j', 'tuningTest', 'am_tuning_curve')
exp0.add_session('18-14-21', 'k', 'am', 'am_tuning_curve')
exp0.add_session('18-20-26', 'l', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('19-00-16', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-01-25', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-02-39', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('19-04-32', 'm', 'tuningTest', 'am_tuning_curve')
exp0.add_session('19-07-06', 'n', 'am', 'am_tuning_curve')
exp0.add_session('19-13-09', 'o', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('19-48-30', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-49-39', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-50-59', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('19-52-48', 'p', 'tuningTest', 'am_tuning_curve')
exp0.add_session('19-55-21', 'q', 'am', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('20-09-59', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('20-11-10', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('20-12-30', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('20-14-21', 'r', 'tuningTest', 'am_tuning_curve')
exp0.add_session('20-17-06', 's', 'am', 'am_tuning_curve')
exp0.add_session('20-23-13', 't', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('20-59-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('21-00-38', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('21-01-54', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('21-03-45', 'u', 'tuningTest', 'am_tuning_curve')
exp0.add_session('21-06-06', 'v', 'am', 'am_tuning_curve')
exp0.add_session('21-12-38', 'w', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('21-48-58', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('21-50-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('21-51-27', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('21-53-16', 'x', 'tuningTest', 'am_tuning_curve')
exp0.add_session('21-55-34', 'y', 'am', 'am_tuning_curve')
exp0.add_session('22-01-57', 'z', 'tuningCurve', 'am_tuning_curve')

exp0.maxDepth = 3600
