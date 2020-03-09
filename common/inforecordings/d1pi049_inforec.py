from jaratoolbox import celldatabase

subject = 'd1pi049'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-03-07', 'left_AudStr',
info=['anteriorDiI', 'TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.55, 21.7
1.0: 2.2, 28.4
1.5: 2.95, 36.0
2.0: 3.8, 44.8
2.5: 4.75, 55.2
3.0: 5.8, 66.6 (nice)
3.5: 7.25, 82.2
4.0: 10.0, 111.7
"""

# Animal in rig at: 11:35
# I feel like I can see bubbles/vacuums forming under glue and it's making me nervous
# also a decent amount of bleeding from right craniotomy, tried left instead
# Probe in at: 12:39

exp0.add_site(3000, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('12-50-56', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-52-06', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-53-16', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-55-08', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-57-27', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3100, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('13-14-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-15-18', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-16-28', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-18-29', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-20-51', 'd', 'am', 'am_tuning_curve')
exp0.add_session('13-29-39', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('14-05-37', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-06-46', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-07-55', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-09-48', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-12-07', 'g', 'am', 'am_tuning_curve')

exp0.add_site(3300, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-28-10', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-29-19', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-30-28', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-32-17', 'h', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-34-37', 'i', 'am', 'am_tuning_curve')
exp0.add_session('14-40-38', 'j', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-17-20', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-18-29', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-19-36', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-21-28', 'k', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-23-51', 'l', 'am', 'am_tuning_curve')
exp0.add_session('15-29-54', 'm', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('16-10-53', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-12-03', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-13-11', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-15-06', 'n', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-17-27', 'o', 'am', 'am_tuning_curve')
exp0.add_session('16-23-55', 'p', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('17-00-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-01-21', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-02-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-05-27', 'q', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-08-00', 'r', 'am', 'am_tuning_curve')

exp0.add_site(3700, tetrodes=[1,2,3,5,6,7,8])
exp0.add_session('17-23-03', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-24-14', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-25-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-27-12', 's', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-29-45', 't', 'am', 'am_tuning_curve')
exp0.add_session('17-35-51', 'u', 'tuningCurve', 'am_tuning_curve')

exp0.maxDepth = 3700


exp1 = celldatabase.Experiment(subject, '2020-03-08', 'left_AudStr',
info=['middleDiD', 'TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.55, 20.0
1.0: 2.2, 26.4
1.5: 2.95, 34.2
2.0: 3.75, 42.5
2.5: 4.55, 50.7
3.0: 5.75, 63.6
3.5: 6.65, 72.6
4.0: 8.25, 89.6
"""

# Animal in rig at: 11:31
# Probe in at: 11:38

exp1.add_site(3000, tetrodes=[2,3,4,7,8])
exp1.add_session('11-50-27', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-51-38', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('11-52-47', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('11-54-58', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('11-57-29', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[1,2,3,4,7,8])
exp1.add_session('12-18-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-20-00', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-21-08', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-22-39', 'c', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-24-58', 'd', 'am', 'am_tuning_curve')

exp1.add_site(3200, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('12-44-56', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-46-13', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-47-24', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-48-54', 'e', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-51-19', 'f', 'am', 'am_tuning_curve')

exp1.add_site(3300, tetrodes=[1,2,3,4,7,8])
exp1.add_session('13-09-00', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-10-16', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-11-26', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-13-16', 'g', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-15-36', 'h', 'am', 'am_tuning_curve')
exp1.add_session('13-22-02', 'i', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3400, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('14-04-20', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-05-32', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-06-48', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-08-19', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-10-57', 'k', 'am', 'am_tuning_curve')

exp1.add_site(3500, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('14-26-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-27-44', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-28-56', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-30-26', 'l', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-34-50', 'm', 'am', 'am_tuning_curve')

exp1.add_site(3600, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('14-52-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-54-06', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-55-30', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-57-02', 'n', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-59-21', 'o', 'am', 'am_tuning_curve')

exp1.add_site(3700, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-13-02', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-14-19', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-15-53', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-17-40', 'p', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-20-01', 'q', 'am', 'am_tuning_curve')

exp1.add_site(3800, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-35-27', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-36-37', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-37-55', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-39-26', 'r', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-41-45', 's', 'am', 'am_tuning_curve')
exp1.add_session('16-26-32', 't', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3900, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('17-04-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-05-43', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-06-53', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-08-55', 'u', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-11-36', 'v', 'am', 'am_tuning_curve')

exp1.add_site(4000, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('17-24-23', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-25-33', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-26-42', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-28-36', 'w', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-31-11', 'x', 'am', 'am_tuning_curve')
exp1.add_session('17-37-16', 'y', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(4100, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('18-12-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-13-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-14-35', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-16-24', 'z', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-18-56', 'aa', 'am', 'am_tuning_curve')

exp1.maxDepth = 4100
