from jaratoolbox import celldatabase

subject = 'd1pi049'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2020-03-07', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
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

exp0.add_site(3000, egroups=[1,2,3,4,6,7,8])
exp0.add_session('12-50-56', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-52-06', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-53-16', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-55-08', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-57-27', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3100, egroups=[1,2,3,4,6,7,8])
exp0.add_session('13-14-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-15-18', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-16-28', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-18-29', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-20-51', 'd', 'am', 'am_tuning_curve')
exp0.add_session('13-29-39', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3200, egroups=[1,2,3,4,6,7,8])
exp0.add_session('14-05-37', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-06-46', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-07-55', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-09-48', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-12-07', 'g', 'am', 'am_tuning_curve')

exp0.add_site(3300, egroups=[1,2,4,5,6,7,8])
exp0.add_session('14-28-10', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-29-19', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-30-28', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-32-17', 'h', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-34-37', 'i', 'am', 'am_tuning_curve')
exp0.add_session('14-40-38', 'j', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3400, egroups=[1,2,4,5,6,7,8])
exp0.add_session('15-17-20', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-18-29', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-19-36', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-21-28', 'k', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-23-51', 'l', 'am', 'am_tuning_curve')
exp0.add_session('15-29-54', 'm', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, egroups=[2,3,4,5,6,7,8])
exp0.add_session('16-10-53', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-12-03', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-13-11', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-15-06', 'n', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-17-27', 'o', 'am', 'am_tuning_curve')
exp0.add_session('16-23-55', 'p', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, egroups=[2,3,4,5,6,7,8])
exp0.add_session('17-00-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-01-21', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-02-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-05-27', 'q', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-08-00', 'r', 'am', 'am_tuning_curve')

exp0.add_site(3700, egroups=[1,2,3,5,6,7,8])
exp0.add_session('17-23-03', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-24-14', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-25-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-27-12', 's', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-29-45', 't', 'am', 'am_tuning_curve')
exp0.add_session('17-35-51', 'u', 'tuningCurve', 'am_tuning_curve')

exp0.maxDepth = 3700


exp1 = celldatabase.Experiment(subject, '2020-03-08', 'left_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
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

exp1.add_site(3000, egroups=[2,3,4,7,8])
exp1.add_session('11-50-27', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-51-38', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('11-52-47', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('11-54-58', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('11-57-29', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3100, egroups=[1,2,3,4,7,8])
exp1.add_session('12-18-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-20-00', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-21-08', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-22-39', 'c', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-24-58', 'd', 'am', 'am_tuning_curve')

exp1.add_site(3200, egroups=[1,2,3,4,6,7,8])
exp1.add_session('12-44-56', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-46-13', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-47-24', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-48-54', 'e', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-51-19', 'f', 'am', 'am_tuning_curve')

exp1.add_site(3300, egroups=[1,2,3,4,7,8])
exp1.add_session('13-09-00', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-10-16', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-11-26', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-13-16', 'g', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-15-36', 'h', 'am', 'am_tuning_curve')
exp1.add_session('13-22-02', 'i', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3400, egroups=[1,2,3,4,5,6,8])
exp1.add_session('14-04-20', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-05-32', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-06-48', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-08-19', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-10-57', 'k', 'am', 'am_tuning_curve')

exp1.add_site(3500, egroups=[1,2,3,4,6,7,8])
exp1.add_session('14-26-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-27-44', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-28-56', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-30-26', 'l', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-34-50', 'm', 'am', 'am_tuning_curve')

exp1.add_site(3600, egroups=[1,2,3,4,5,6,8])
exp1.add_session('14-52-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-54-06', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-55-30', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-57-02', 'n', 'tuningTest', 'am_tuning_curve')
exp1.add_session('14-59-21', 'o', 'am', 'am_tuning_curve')

exp1.add_site(3700, egroups=[1,2,3,4,5,6,8])
exp1.add_session('15-13-02', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-14-19', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-15-53', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-17-40', 'p', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-20-01', 'q', 'am', 'am_tuning_curve')

exp1.add_site(3800, egroups=[1,2,3,4,5,6,8])
exp1.add_session('15-35-27', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-36-37', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-37-55', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-39-26', 'r', 'tuningTest', 'am_tuning_curve')
exp1.add_session('15-41-45', 's', 'am', 'am_tuning_curve')
exp1.add_session('16-26-32', 't', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3900, egroups=[1,2,3,4,5,6,8])
exp1.add_session('17-04-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-05-43', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-06-53', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-08-55', 'u', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-11-36', 'v', 'am', 'am_tuning_curve')

exp1.add_site(4000, egroups=[2,3,4,5,6,7,8])
exp1.add_session('17-24-23', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-25-33', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-26-42', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-28-36', 'w', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-31-11', 'x', 'am', 'am_tuning_curve')
exp1.add_session('17-37-16', 'y', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(4100, egroups=[2,3,4,5,6,7,8])
exp1.add_session('18-12-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-13-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-14-35', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-16-24', 'z', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-18-56', 'aa', 'am', 'am_tuning_curve')

exp1.maxDepth = 4100


exp2 = celldatabase.Experiment(subject, '2020-03-09', 'left_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.55, 19.6
1.0: 2.05, 25.3
1.5: 2.75, 32.3
2.0: 3.55, 40.2
2.5: 4.1, 46.3
3.0: 5.15, 57.3
3.5: 6.15, 67.6
4.0: 7.15, 78.8
"""

# Animal in rig at: 9:21
# Probe in at: 9:32

exp2.add_site(3000, egroups=[1,5,6,8])
exp2.add_session('09-49-22', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('09-50-31', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('09-51-40', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('09-53-40', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('09-55-58', 'b', 'am', 'am_tuning_curve')
exp2.add_session('10-02-03', 'c', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3200, egroups=[2,4,5,6,7,8])
exp2.add_session('10-49-09', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('10-52-13', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('10-56-54', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('10-59-02', 'd', 'tuningTest', 'am_tuning_curve')
exp2.add_session('11-02-00', 'e', 'am', 'am_tuning_curve')

exp2.add_site(3300, egroups=[2,5,6,7,8])
exp2.add_session('11-20-54', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-24-12', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('11-25-22', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-26-58', 'f', 'tuningTest', 'am_tuning_curve')
exp2.add_session('11-30-09', 'g', 'am', 'am_tuning_curve')

exp2.add_site(3400, egroups=[2,5,6,7,8])
exp2.add_session('11-48-43', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-50-17', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('11-51-58', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-58-36', 'h', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-03-24', 'i', 'am', 'am_tuning_curve')

exp2.add_site(3600, egroups=[1,2,4,5,6,7,8])
exp2.add_session('12-33-17', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-34-26', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-35-38', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-37-28', 'j', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-39-57', 'k', 'am', 'am_tuning_curve')

exp2.add_site(3700, egroups=[1,2,4,5,6,7,8])
exp2.add_session('13-40-53', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-42-35', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-43-45', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-45-34', 'l', 'tuningTest', 'am_tuning_curve')
exp2.add_session('14-09-04', 'm', 'am', 'am_tuning_curve')

exp2.maxDepth = 3700

exp3 = celldatabase.Experiment(subject, '2020-03-11', 'right_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp3)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

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

# Animal in rig at: 10:45
# Probe in at: 12:27

# CAN'T ACTUALLY TELL WHAT KIND OF CELLS THESE WERE BECAUSE SOMEONE FORGOT TO TURN ON THE LASER
# exp3.add_site(3000, egroups=[1,2,3,4,6,8])
# exp3.add_session('13-09-19', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('13-10-36', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('13-11-47', None, 'lasertrain', 'am_tuning_curve')
# exp3.add_session('13-13-36', 'a', 'tuningTest', 'am_tuning_curve')
# exp3.add_session('13-16-31', 'b', 'am', 'am_tuning_curve')
# exp3.add_session('13-22-35', 'c', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3400, egroups=[1,2,3,4,6,8])
exp3.add_session('15-09-34', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-11-06', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('15-32-06', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('15-29-25', 'd', 'tuningTest', 'am_tuning_curve')
exp3.add_session('15-20-55', 'e', 'am', 'am_tuning_curve')
exp3.add_session('15-34-25', 'f', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3500, egroups=[2,7,8])
exp3.add_session('16-11-50', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('16-13-00', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('16-14-10', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('16-16-49', 'g', 'tuningTest', 'am_tuning_curve')
exp3.add_session('16-19-10', 'h', 'am', 'am_tuning_curve')
exp3.add_session('16-26-10', 'i', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3600, egroups=[1,2,4,7,8])
exp3.add_session('17-03-18', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-04-29', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-05-38', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('17-07-08', 'j', 'tuningTest', 'am_tuning_curve')
exp3.add_session('17-09-30', 'k', 'am', 'am_tuning_curve')

exp3.maxDepth = 3600


exp4 = celldatabase.Experiment(subject, '2020-03-12', 'right_AudStr',
                               recordingTrack='anteriorMiddleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp4)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.9
1.0: 2.0, 25.1
1.5: 2.6, 31.5
2.0: 3.35, 38.9
2.5: 3.85, 44.5
3.0: 4.8, 54.2
3.5: 5.8, 65.0
4.0: 6.85, 73.9
"""

# Animal in rig at: 10:24
# Probe in at: 10:31

exp4.add_site(3000, egroups=[7,8])
exp4.add_session('10-46-48', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('10-48-00', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('10-49-08', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('10-51-45', 'a', 'tuningTest', 'am_tuning_curve')
exp4.add_session('10-54-11', 'b', 'am', 'am_tuning_curve')

exp4.add_site(3100, egroups=[7,8])
exp4.add_session('11-18-42', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('11-28-31', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('11-30-57', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('11-32-37', 'c', 'tuningTest', 'am_tuning_curve')
exp4.add_session('11-35-07', 'd', 'am', 'am_tuning_curve')

exp4.add_site(3200, egroups=[2,7,8])
exp4.add_session('11-59-16', None, 'noiseburst', 'am_tuning_curve') # no whitenoise so no am
exp4.add_session('12-00-43', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('12-01-51', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('12-03-22', 'e', 'tuningTest', 'am_tuning_curve')

exp4.add_site(3400, egroups=[2,4,7,8])
exp4.add_session('12-39-44', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('12-41-02', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('12-42-12', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('12-44-33', 'f', 'tuningTest', 'am_tuning_curve')
exp4.add_session('12-46-54', 'g', 'am', 'am_tuning_curve')
exp4.add_session('12-53-01', 'h', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3500, egroups=[7,8])
exp4.add_session('13-29-41', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-30-55', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-37-33', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-39-32', 'i', 'tuningTest', 'am_tuning_curve')
exp4.add_session('13-42-38', 'j', 'am', 'am_tuning_curve')
exp4.add_session('13-49-53', 'k', 'tuningCurve', 'am_tuning_curve')

exp4.maxDepth = 3500

exp5 = celldatabase.Experiment(subject, '2020-03-13', 'right_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp5)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe P427; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.9
1.0: 2.0, 25.1
1.5: 2.6, 31.5
2.0: 3.35, 38.9
2.5: 3.85, 44.5
3.0: 4.8, 54.2
3.5: 5.8, 65.0
4.0: 6.85, 73.9
"""

# Animal in rig at: 10:50
# Probe in at: 11:00

exp5.add_site(3100, egroups=[2,8])
exp5.add_session('11-43-02', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('11-44-12', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('11-51-53', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('11-55-42', 'a', 'tuningTest', 'am_tuning_curve')
exp5.add_session('12-00-20', 'b', 'am', 'am_tuning_curve')

exp5.add_site(3200, egroups=[2,7,8])
exp5.add_session('12-31-23', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('12-32-46', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('12-34-10', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('12-35-48', 'c', 'tuningTest', 'am_tuning_curve')
exp5.add_session('12-38-34', 'd', 'am', 'am_tuning_curve')
exp5.add_session('12-46-08', 'e', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3300, egroups=[1,7,8])
exp5.add_session('13-28-25', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('13-30-17', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('13-31-32', None, 'lasertrain', 'am_tuning_curve')
exp5.add_session('13-33-03', 'f', 'tuningTest', 'am_tuning_curve')
exp5.add_session('13-35-37', 'g', 'am', 'am_tuning_curve')

exp5.maxDepth = 3300
