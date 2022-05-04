from jaratoolbox import celldatabase

subject = 'd1pi041'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-08-25', 'right_AudStr',
                               recordingTrack='anteriourDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 18.6
1.0: 2.0, 24.0
1.5: 2.6, 30.3
2.0: 3.3, 37.3
2.5: 4.0, 44.4
3.0: 4.85, 53.0
3.5: 5.85, 63.5
4.0: 6.75, 73.0
"""

# Animal in rig at: 12:43
# Probe in at: 1:36 (mouse bled a ton and had a lot of weird tissue blocking penetration)

exp0.add_site(2500, egroups=[2,4,6,7])
exp0.add_session('13-50-38', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-52-06', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(2700, egroups=[4,5,6,7,8])
exp0.add_session('13-58-53', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-00-14', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-02-14', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-05-14', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-07-06', 'b', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-35-40', 'c', 'am', 'am_tuning_curve')
exp0.add_session('14-42-01', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(2800, egroups=[4,5,6,7,8])
exp0.add_session('14-49-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-51-05', 'd', 'tuningTest', 'am_tuning_curve')

exp0.add_site(2900, egroups=[3,5,6,7,8])
exp0.add_session('15-00-45', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-02-03', 'e', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-05-11', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-33-43', 'g', 'am', 'am_tuning_curve')
exp0.add_session('15-39-47', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-41-10', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3000, egroups=[1,3,5,6,7,8])
exp0.add_session('15-51-08', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-52-27', 'h', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-54-57', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-25-08', 'j', 'am', 'am_tuning_curve')
exp0.add_session('16-32-11', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-33-32', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3100, egroups=[1,3,4,5,6,7,8])
exp0.add_session('16-42-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-43-36', 'k', 'tuningTest', 'am_tuning_curve')
exp0.add_session('16-46-07', 'l', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-14-51', 'm', 'am', 'am_tuning_curve')
exp0.add_session('17-21-04', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-22-09', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3200, egroups=[1,3,4,5,6,7,8])
exp0.add_session('17-33-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-34-37', 'n', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-37-26', 'o', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('18-06-38', 'p', 'am', 'am_tuning_curve')
exp0.add_session('18-12-44', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-14-12', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3300, egroups=[1,3,4,5,6,7,8])
exp0.add_session('18-40-43', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-42-02', 'q', 'tuningTest', 'am_tuning_curve')
exp0.add_session('18-44-44', 'r', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('19-16-14', 's', 'am', 'am_tuning_curve')
exp0.add_session('19-22-33', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-23-42', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3400, egroups=[1,2,3,5,6,7,8])
exp0.add_session('19-35-43', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-37-02', 't', 'tuningTest', 'am_tuning_curve')
exp0.add_session('19-39-57', 'u', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('20-08-34', 'v', 'am', 'am_tuning_curve')
exp0.add_session('20-14-37', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('20-15-48', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3500, egroups=[1,2,3,5,6,7,8])
exp0.add_session('20-31-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('20-32-26', 'w', 'tuningTest', 'am_tuning_curve')
exp0.add_session('20-35-00', 'x', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('21-03-33', 'y', 'am', 'am_tuning_curve')
exp0.add_session('21-09-37', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('21-10-48', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3600, egroups=[1,2,4,5,6,7,8])
exp0.add_session('21-20-31', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('21-21-48', 'z', 'tuningTest', 'am_tuning_curve')
exp0.add_session('21-24-14', 'aa', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('21-52-47', 'ab', 'am', 'am_tuning_curve')
exp0.add_session('21-58-51', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('22-00-02', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3700, egroups=[1,2,4,5,6,7,8])
exp0.add_session('22-08-13', None, 'noiseburst', 'am_tuning_curve')
# no more sound responses

exp0.maxDepth = 3700


exp1 = celldatabase.Experiment(subject, '2019-08-27', 'right_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.6, 19.9`
1.0: 2.40, 28.1
1.5: 3.25, 36.8
2.0: 4.05, 45.4
2.5: 5.17, 57.2
3.0: 6.28, 69.1
3.5: 7.50, 82.5
4.0: 9.90, 108.9
"""

# Animal in rig at: 11:08
# Probe in at: 11:24

exp1.add_site(2700, egroups=[1,3,6,7,8])
exp1.add_session('12-45-27', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-56-10', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-57-40', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-59-31', 'a', 'tuningTest', 'am_tuning_curve')

exp1.add_site(2800, egroups=[1,2,3,4,6,7,8])
exp1.add_session('13-18-21', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-20-20', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-21-49', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-23-25', 'b', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-27-40', 'c', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-56-26', 'd', 'am', 'am_tuning_curve')

exp1.add_site(2900, egroups=[1,2,6,8])
exp1.add_session('14-13-20', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-14-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-16-44', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-18-58', 'e', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3000, egroups=[1,2,4,7,8])
exp1.add_session('14-33-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-35-03', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-36-32', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-39-11', 'f', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3200, egroups=[1,2,4,5,7,8])
exp1.add_session('15-52-10', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-53-22', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-54-55', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-14-56', 'g', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-33-35', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-29-41', 'i', 'am', 'am_tuning_curve')

exp1.add_site(3300, egroups=[1,2,4,5,7,8])
exp1.add_session('18-09-37', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-11-29', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-12-43', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-15-43', 'j', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3400, egroups=[1,2,4,5,6,7,8])
exp1.add_session('18-28-04', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-29-17', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-30-30', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-32-01', 'k', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-36-30', 'l', 'tuningCurve', 'am_tuning_curve')

exp1.maxDepth = 3400


exp2 = celldatabase.Experiment(subject, '2019-08-28', 'right_AudStr',
                               recordingTrack='posteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.40, 22.5
1.0: 1.75, 26.1
1.5: 2.20, 30.7
2.0: 2.70, 35.9
2.5: 3.20, 41.0
3.0: 3.70, 46.5
3.5: 4.30, 52.8
4.0: 5.35, 64.2
"""

# Animal in rig at: 11:10
# Probe in at: 11:37 (There was weird tissue growth and a fair amount of bleeding)

exp2.add_site(3200, egroups=[2])
exp2.add_session('12-51-19', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-52-57', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-54-21', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-58-59', 'a', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3300, egroups=[1,2])
exp2.add_session('13-25-08', None, 'noiseburst', 'am_tuning_curve')

exp2.add_site(3400, egroups=[1])
exp2.add_session('13-37-00', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-38-27', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-39-46', 'b', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3500, egroups=[1,2,4])
exp2.add_session('14-17-04', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-18-12', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-19-31', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-21-39', 'c', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3600, egroups=[4,6,7,8])
exp2.add_session('15-05-05', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-06-31', 'd', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3700, egroups=[1,2,4,5,6,7,8])
exp2.add_session('15-29-06', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-30-16', 'e', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3800, egroups=[1,2,4,5,6,7,8])
exp2.add_session('16-00-36', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-01-58', 'f', 'tuningTest', 'am_tuning_curve')

exp2.add_site(3900, egroups=[1,2,4,5,6,7,8])
exp2.add_session('16-22-06', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-23-35', 'g', 'tuningTest', 'am_tuning_curve')

exp2.add_site(4000, egroups=[1,2,4,5,6,7,8])
exp2.add_session('17-31-17', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('17-32-25', 'h', 'tuningTest', 'am_tuning_curve')

exp2.add_site(4100, egroups=[1,2,4,5,6,7,8])
exp2.add_session('17-46-02', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('17-47-19', 'i', 'tuningTest', 'am_tuning_curve')

exp2.maxDepth = 4100


# exp3 = celldatabase.Experiment(subject, '2019-08-29', 'right_AudStr', 'anteriorDiD',
    # info=['TT1left', 'soundLeft', 'A4x2-tet'])
# experiments.append(exp3)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
# #Used left speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.55, 19.3
# 1.0: 2.15, 25.5
# 1.5: 2.68, 31.5
# 2.0: 3.32, 38.1
# 2.5: 3.95, 44.8
# 3.0: 4.65, 52.6
# 3.5: 5.65, 63.1
# 4.0: 6.25, 69.9
# """
#
# # Animal in rig at:12:41
# # Probe in at: 1:05 (hitting something around 1800 that is causing deflection, moved anterior and problem resolved)
#
# # Seems quiet at 2500
# exp3.add_site(2600, egroups=[1])
# exp3.add_session('14-56-14', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('14-58-16', 'a', 'tuningTest', 'am_tuning_curve')
#
# exp3.add_site(2900, egroups=[2])
# exp3.add_session('16-19-44', None, 'noiseburst', 'am_tuning_curve')
#
# exp3.maxDepth = 3400


exp4 = celldatabase.Experiment(subject, '2019-08-30', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp4)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.5, 19.1
1.0: 2.05, 24.7
1.5: 2.7, 31.4
2.0: 3.35, 38.4
2.5: 4.05, 45.5
3.0: 5.05, 55.6
3.5: 6.1, 66.9
4.0: 7.05, 76.6
"""

# Animal in rig at: 11:45
# Probe in at: 1:17 (new side, played a super fun game of "where even is the craniotomy" and "where is all this blood coming from")

# exp4.add_site(2500, egroups=[2,4,7])
# exp4.add_session('13-34-38', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('13-36-06', 'a', 'tuningTest', 'am_tuning_curve')

# exp4.add_site(2700, egroups=[1,2,3,4,6,7,8])
# exp4.add_session('13-55-40', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('13-56-58', 'b', 'tuningTest', 'am_tuning_curve')

# exp4.add_site(2900, egroups=[1,2,4,6,7,8])
# exp4.add_session('14-12-14', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-13-39', 'c', 'tuningTest', 'am_tuning_curve')
# exp4.add_session('14-16-02', None, 'laserpulse', 'am_tuning_curve')

exp4.add_site(3100, egroups=[1,2,3,4,6,7,8])
exp4.add_session('14-27-03', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('14-28-26', 'd', 'tuningTest', 'am_tuning_curve')
exp4.add_session('14-31-06', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-05-42', 'f', 'am', 'am_tuning_curve')
exp4.add_session('16-20-05', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('16-21-13', None, 'lasertrain', 'am_tuning_curve')

exp4.add_site(3200, egroups=[1,2,3,4,6,7,8])
exp4.add_session('16-31-54', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('16-33-11', 'g', 'tuningTest', 'am_tuning_curve')
exp4.add_session('16-35-39', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('17-04-30', 'i', 'am', 'am_tuning_curve')
exp4.add_session('17-10-36', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('17-11-45', None, 'lasertrain', 'am_tuning_curve')

exp4.add_site(3300, egroups=[2,3,4,5,6,7,8])
exp4.add_session('17-21-22', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('17-22-45', 'j', 'tuningTest', 'am_tuning_curve')
exp4.add_session('17-25-31', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('17-54-05', 'l', 'am', 'am_tuning_curve')
exp4.add_session('18-00-23', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('18-02-29', None, 'lasertrain', 'am_tuning_curve')

exp4.maxDepth = 3300


exp5 = celldatabase.Experiment(subject, '2019-08-31', 'left_AudStr',
                               recordingTrack='anteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp5)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe C39A; Rig 2
# Probe had very high impedances first test. Unplugged and plugged back in, adjusted ground.
# Impedances more in normal range after, but some sites very low.

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 18.6
1.0: 2.0, 23.8
1.5: 2.6, 30.2
2.0: 3.25, 36.6
2.5: 3.9, 43.6
3.0: 4.75, 52.6
3.5: 5.85, 63.2
4.0: 6.8, 73.0
"""

# Animal in rig at: 10:10
# Probe in at: 10:18

# At 2500, all channels pretty silent... Can get some spikes (maybe) by lowering threshold a lot (25).

# mouse out 11:06
# replaced probe with M680
"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.4, 19.7
1.0: 1.75, 23.4
1.5: 2.25, 28.3
2.0: 2.7, 33.1
2.5: 3.25, 38.7
3.0: 3.8, 44.3
3.5: 4.75, 54.1
4.0: 5.7, 63.6
"""
# impedances kind of high after attaching fibre and coating with dye!!
# mouse back in 12:10
# probe in 12:13

exp5.add_site(2800, egroups=[1,2,3,4,7])
exp5.add_session('12-33-30', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('12-34-49', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('12-36-06', 'a', 'tuningTest', 'am_tuning_curve')
exp5.add_session('12-39-24', 'b', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-08-02', 'c', 'am', 'am_tuning_curve')
exp5.add_session('13-14-09', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('13-15-41', None, 'lasertrain', 'am_tuning_curve')

# moved to 3000, signals suddenly go silent
# after waiting a bit, signals randomly come back, then go away again??

# signals back but kind of weak
# exp5.add_site(3100, egroups=[2,3,6,7,8])
# exp5.add_session('13-56-12', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('13-57-34', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('13-58-47', 'd', 'tuningTest', 'am_tuning_curve')

# exp5.add_site(3300, egroups=[2,4,6,7,8])
# exp5.add_session('14-09-45', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('14-11-04', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('14-12-24', 'e', 'tuningTest', 'am_tuning_curve')

# exp5.add_site(3400, egroups=[2,4,8])
# exp5.add_session('14-18-54', None, 'noiseburst', 'am_tuning_curve')

# signals decent again
exp5.add_site(3500, egroups=[2,4,6,8])
exp5.add_session('14-29-59', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('14-31-18', 'f', 'tuningTest', 'am_tuning_curve')
exp5.add_session('14-33-50', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-02-34', 'h', 'am', 'am_tuning_curve')
exp5.add_session('15-08-37', None, 'laserpulse', 'am_tuning_curve')
exp5.add_session('15-10-14', None, 'laserpulse', 'am_tuning_curve')

# signals went away again lmao
# lowered threshold (30mV) and sucked some saline out
# exp5.add_site(3600, egroups=[4,6])
# exp5.add_session('15-33-33', None, 'laserpulse', 'am_tuning_curve')

# exp5.add_site(3700, egroups=[4,8])
# exp5.add_session('15-44-07', None, 'laserpulse', 'am_tuning_curve')

exp5.maxDepth = 3700

# exp6 = celldatabase.Experiment(subject, '2019-09-03', 'left_AudStr', 'middleDiI',
    # info=['TT1left', 'soundRight', 'A4x2-tet'])
# experiments.append(exp6)
#
# #50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
# #Used right speaker;laser (445 nm) set to 2.0 mW; Probe M680; Rig 2
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 0.5: 1.40, 19.0
# 1.0: 1.85, 23.2
# 1.5: 2.35, 28.4
# 2.0: 2.85, 33.7
# 2.5: 3.50, 40.3
# 3.0: 4.08, 46.1
# 3.5: 5.95, 55.2
# 4.0: 6.00, 65.9
# """
#
# # Skull seems to have caved in on medial-anterior edge of left well. Mouse was euthanized
#
# exp6.maxDepth = 0
