from jaratoolbox import celldatabase

subject = 'd1pi046'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-02-15', 'right_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P429; Rig 2

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

exp0.add_site(2700, egroups=[2,4,5,6,7,8])
# exp0.add_session('16-04-25', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('16-05-56', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('16-07-10', None, 'lasertrain', 'am_tuning_curve')
# changed reference to TT3 because TT5 was getting huge noise from laser
exp0.add_session('16-09-42', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-10-59', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-12-08', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-14-01', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-17-14', 'b', 'am', 'am_tuning_curve')

exp0.add_site(2800, egroups=[1,2,5,6,8])
exp0.add_session('16-34-25', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-35-35', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-36-44', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-38-32', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-41-05', 'd', 'am', 'am_tuning_curve')
exp0.add_session('16-47-31', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, egroups=[1,2,4,5,6,7,8])
exp0.add_session('17-25-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-26-27', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-27-41', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-29-38', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-32-14', 'g', 'am', 'am_tuning_curve')

exp0.add_site(3000, egroups=[1,2,4,5,6,7,8])
exp0.add_session('17-46-14', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-47-26', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-48-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-50-25', 'h', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-52-57', 'i', 'am', 'am_tuning_curve')

exp0.add_site(3100, egroups=[1,2,4,5,6,7,8])
exp0.add_session('18-07-12', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-08-23', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-09-32', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-11-22', 'j', 'tuningTest', 'am_tuning_curve')
exp0.add_session('18-14-21', 'k', 'am', 'am_tuning_curve')
exp0.add_session('18-20-26', 'l', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, egroups=[1,2,4,5,6,7,8])
exp0.add_session('19-00-16', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-01-25', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-02-39', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('19-04-32', 'm', 'tuningTest', 'am_tuning_curve')
exp0.add_session('19-07-06', 'n', 'am', 'am_tuning_curve')
exp0.add_session('19-13-09', 'o', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, egroups=[1,2,4,5,6,7,8])
exp0.add_session('19-48-30', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-49-39', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-50-59', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('19-52-48', 'p', 'tuningTest', 'am_tuning_curve')
exp0.add_session('19-55-21', 'q', 'am', 'am_tuning_curve')

exp0.add_site(3400, egroups=[1,2,4,5,6,7,8])
exp0.add_session('20-09-59', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('20-11-10', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('20-12-30', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('20-14-21', 'r', 'tuningTest', 'am_tuning_curve')
exp0.add_session('20-17-06', 's', 'am', 'am_tuning_curve')
exp0.add_session('20-23-13', 't', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, egroups=[1,2,4,5,6,7,8])
exp0.add_session('20-59-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('21-00-38', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('21-01-54', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('21-03-45', 'u', 'tuningTest', 'am_tuning_curve')
exp0.add_session('21-06-06', 'v', 'am', 'am_tuning_curve')
exp0.add_session('21-12-38', 'w', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, egroups=[1,2,4,5,6,7,8])
exp0.add_session('21-48-58', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('21-50-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('21-51-27', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('21-53-16', 'x', 'tuningTest', 'am_tuning_curve')
exp0.add_session('21-55-34', 'y', 'am', 'am_tuning_curve')
exp0.add_session('22-01-57', 'z', 'tuningCurve', 'am_tuning_curve')

# mouse has enormous clot on left side filling entire well
# managed to remove it without inciting more bleeding

exp0.maxDepth = 3600


exp1 = celldatabase.Experiment(subject, '2020-02-16', 'right_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp1)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P429; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.8
1.0: 2.0, 25.1
1.5: 2.65, 31.6
2.0: 3.3, 38.5
2.5: 3.85, 44.2
3.0: 4.75, 54.1
3.5: 5.7, 63.9
4.0: 6.55, 72.6
"""

# Animal in rig at: 10:29
# Probe in at: 10:43

exp1.add_site(3100, egroups=[5,8])
exp1.add_session('12-00-13', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-01-57', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-03-17', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-05-10', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-08-03', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3400, egroups=[7,8])
exp1.add_session('13-08-36', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-09-45', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-11-07', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-14-11', 'c', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-16-44', 'd', 'am', 'am_tuning_curve')

# hypothesised that I'm not getting good signals because there's way too much dye on the sites
# moved up and down a bunch between 3200 and 3400 to try to rub it off

exp1.add_site(3500, egroups=[7,8])
exp1.add_session('13-48-10', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-49-19', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-50-50', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-52-52', 'e', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-55-15', 'f', 'am', 'am_tuning_curve')
exp1.add_session('14-01-41', 'g', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3600, egroups=[7,8])
exp1.add_session('14-42-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-44-11', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-48-32', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-50-44', 'h', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-57-00', 'i', 'am', 'am_tuning_curve')
exp1.add_session('15-04-42', 'j', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3700, egroups=[6,7,8])
exp1.add_session('15-50-58', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-52-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-53-17', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-55-07', 'k', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-57-29', 'l', 'am', 'am_tuning_curve')
exp1.add_session('16-03-36', 'm', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3800, egroups=[5,6,7,8])
exp1.add_session('16-38-12', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-39-22', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-40-37', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-42-27', 'n', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-44-46', 'o', 'am', 'am_tuning_curve')
exp1.add_session('16-50-52', 'p', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3900, egroups=[5,6,7,8])
exp1.add_session('17-27-35', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-28-45', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-29-58', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-31-48', 'r', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-34-18', 's', 'am', 'am_tuning_curve')
exp1.add_session('17-40-21', 't', 'tuningCurve', 'am_tuning_curve')

exp1.maxDepth = 3900


exp2 = celldatabase.Experiment(subject, '2020-02-17', 'right_AudStr',
                               recordingTrack='middleDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp2)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P429; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.3
1.0: 1.95, 24.3
1.5: 2.5, 29.8
2.0: 3.15, 36.2
2.5: 3.65, 41.7
3.0: 4.35, 49.0
3.5: 5.35, 59.6
4.0: 6.15, 68.3
"""

# Animal in rig at: 8:56
# Probe in at: 9:03

exp2.add_site(2900, egroups=[1,3,8])
exp2.add_session('09-20-31', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('09-21-44', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('09-22-56', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('09-24-46', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('09-27-05', 'b', 'am', 'am_tuning_curve')

exp2.add_site(3100, egroups=[6])
exp2.add_session('10-16-56', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('10-18-54', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('10-20-37', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('10-22-36', 'c', 'tuningTest', 'am_tuning_curve')
exp2.add_session('10-26-48', 'd', 'am', 'am_tuning_curve')

exp2.add_site(3500, egroups=[7,8])
exp2.add_session('13-40-34', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-41-42', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-42-51', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-44-42', 'e', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-47-01', 'f', 'am', 'am_tuning_curve')

exp2.add_site(3600, egroups=[7,8])
exp2.add_session('14-08-43', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-10-57', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-12-14', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-15-04', 'g', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-17-59', 'h', 'am', 'am_tuning_curve')

exp2.add_site(3700, egroups=[7,8])
exp2.add_session('14-37-40', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-38-59', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-40-35', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-42-25', 'i', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-45-04', 'j', 'am', 'am_tuning_curve')

exp2.maxDepth = 3700


exp3 = celldatabase.Experiment(subject, '2020-02-18', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp3)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.95, 24.7
1.5: 2.45, 30.3
2.0: 3.1, 36.6
2.5: 3.65, 42.4
3.0: 4.35, 49.9
3.5: 5.4, 60.8
4.0: 6.2, 69.0 (nice)
"""

# Animal in rig at: 9:12
# Probe in at: 9:29 (P429)
# little bit of bleeding, but not like on Saturday
# all channels look silent, don't even get noise with light on
# Probe in at: 9:47 (D65D)

exp3.add_site(2900, egroups=[1,6,7,8])
exp3.add_session('09-56-29', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('09-57-38', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('09-58-48', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('10-00-41', 'a', 'tuningTest', 'am_tuning_curve')
exp3.add_session('10-03-02', 'b', 'am', 'am_tuning_curve')

exp3.add_site(3100, egroups=[2,4,6,7,8])
exp3.add_session('10-22-57', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('10-24-05', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('10-25-13', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('10-27-03', 'c', 'tuningTest', 'am_tuning_curve')
exp3.add_session('10-29-28', 'd', 'am', 'am_tuning_curve')

exp3.add_site(3200, egroups=[4,5,6,7,8])
exp3.add_session('10-56-14', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('10-57-23', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('10-58-33', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('11-00-22', 'e', 'tuningTest', 'am_tuning_curve')
exp3.add_session('11-03-25', 'f', 'am', 'am_tuning_curve')
exp3.add_session('11-09-47', 'g', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3300, egroups=[2,4,5,6,7,8])
exp3.add_session('12-14-29', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-15-39', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('12-16-56', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('12-20-51', 'h', 'tuningTest', 'am_tuning_curve')
exp3.add_session('12-24-00', 'i', 'am', 'am_tuning_curve')
exp3.add_session('12-31-32', 'j', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3400, egroups=[2,4,5,6,7,8])
exp3.add_session('13-54-06', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-55-20', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('13-56-49', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('13-58-23', 'k', 'tuningTest', 'am_tuning_curve')
exp3.add_session('14-00-53', 'l', 'am', 'am_tuning_curve')
exp3.add_session('14-07-36', 'm', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3500, egroups=[2,3,4,5,6,7,8])
exp3.add_session('15-33-45', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-34-56', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('15-36-23', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('15-38-29', 'n', 'tuningTest', 'am_tuning_curve')
exp3.add_session('15-42-57', 'o', 'am', 'am_tuning_curve')
exp3.add_session('15-49-44', 'p', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3600, egroups=[1,2,4,5,6,7,8])
exp3.add_session('16-29-28', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('16-30-36', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('16-31-46', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('16-33-36', 'q', 'tuningTest', 'am_tuning_curve')
exp3.add_session('16-35-54', 'r', 'am', 'am_tuning_curve')
exp3.add_session('16-41-56', 's', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3700, egroups=[1,2,3,4,6,7,8])
exp3.add_session('17-23-48', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-25-01', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-26-10', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('17-28-00', 't', 'tuningTest', 'am_tuning_curve')
exp3.add_session('17-30-23', 'u', 'am', 'am_tuning_curve')
exp3.add_session('17-36-29', 'v', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3800, egroups=[1,2,4,5,6,7,8])
exp3.add_session('18-16-27', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('18-17-36', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('18-18-48', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('18-20-41', 'w', 'tuningTest', 'am_tuning_curve')
exp3.add_session('18-23-02', 'x', 'am', 'am_tuning_curve')
exp3.add_session('18-29-05', 'y', 'tuningCurve', 'am_tuning_curve')

exp3.maxDepth = 3800

exp4 = celldatabase.Experiment(subject, '2020-02-19', 'left_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp4)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.95, 24.7
1.5: 2.45, 30.3
2.0: 3.1, 36.6
2.5: 3.65, 42.4
3.0: 4.35, 49.9
3.5: 5.4, 60.8
4.0: 6.2, 69.4
"""

# Animal in rig at: 11:22
# Probe in at: 11:28

exp4.add_site(3000, egroups=[2,3,4])
exp4.add_session('12-06-47', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('12-08-12', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('12-09-51', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('12-11-43', 'a', 'tuningTest', 'am_tuning_curve')
exp4.add_session('12-15-20', 'b', 'am', 'am_tuning_curve')

exp4.add_site(3100, egroups=[1,2,3,4])
exp4.add_session('12-55-30', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('12-58-55', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-00-20', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-01-59', 'c', 'tuningTest', 'am_tuning_curve')
exp4.add_session('13-04-42', 'd', 'am', 'am_tuning_curve')

exp4.add_site(3200, egroups=[1,2,8])
exp4.add_session('13-27-24', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-28-40', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-29-50', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-31-29', 'e', 'tuningTest', 'am_tuning_curve')
exp4.add_session('13-34-34', 'f', 'am', 'am_tuning_curve')

exp4.add_site(3300, egroups=[1,2,3,6,8])
exp4.add_session('13-59-27', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('14-00-51', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('14-02-02', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('14-04-41', 'g', 'tuningTest', 'am_tuning_curve')
exp4.add_session('14-07-12', 'h', 'am', 'am_tuning_curve')

exp4.add_site(3400, egroups=[1,2,6,8])
exp4.add_session('14-26-56', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('14-28-07', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('14-31-55', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('14-35-15', 'i', 'tuningTest', 'am_tuning_curve')
exp4.add_session('14-37-39', 'j', 'am', 'am_tuning_curve')
exp4.add_session('14-46-51', 'k', 'tuningCurve', 'am_tuning_curve')

exp4.maxDepth = 3400

# exp5 = celldatabase.Experiment(subject, '2020-02-20', 'left_AudStr', 'posteriorDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp5)
#
# # 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# # Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.50, 19.3
# 1.0: 2.05, 24.7
# 1.5: 2.62, 30.8
# 2.0: 3.2, 37.0
# 2.5: 3.80, 43.4
# 3.0: 4.44, 550.3
# 3.5: 5.5, 61.6
# 4.0: 6.2, 69.1
# """
#
# # Animal in rig at: 10:30
# # Probe in at: 10:37
#
# exp5.add_site(3400, egroups=[4,5,6])
# exp5.add_session('11-25-57', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('11-27-06', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('11-28-21', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('11-30-19', 'a', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('11-33-37', 'b', 'am', 'am_tuning_curve')
#
# exp5.add_site(3500, egroups=[8])
# exp5.add_session('12-04-41', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('12-09-42', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('12-10-52', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('12-12-42', 'c', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('12-20-14', 'd', 'am', 'am_tuning_curve')
#
# exp5.add_site(3700, egroups=[5,6,8])
# exp5.add_session('12-58-30', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('12-59-40', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('13-00-56', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('13-02-48', 'e', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('13-05-07', 'f', 'am', 'am_tuning_curve')
#
# exp5.add_site(3800, egroups=[4,6,7,8])
# exp5.add_session('13-27-55', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('13-29-06', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('13-30-18', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('13-32-14', 'g', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('13-34-33', 'h', 'am', 'am_tuning_curve')
#
# exp5.add_site(3900, egroups=[5,6,8])
# exp5.add_session('14-00-50', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('14-01-58', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('14-03-06', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('14-04-58', 'i', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('14-07-19', 'j', 'am', 'am_tuning_curve')
#
# exp5.add_site(4000, egroups=[4,5,6,8])
# exp5.add_session('14-25-51', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('14-26-59', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('14-28-07', None, 'lasertrain', 'am_tuning_curve')
# exp5.add_session('14-29-55', 'k', 'tuningTest', 'am_tuning_curve')
# exp5.add_session('14-32-14', 'l', 'am', 'am_tuning_curve')
#
# exp5.maxDepth = 4000
