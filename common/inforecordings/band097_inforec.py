from jaratoolbox import celldatabase

subject = 'band097'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-09-23', 'left_AC', info=['medialDiD','TT8ant','soundright'])
experiments.append(exp0)

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 3.75, 17.2
2.0: 4.7, 31.8
3.0: 5.7, 47.2
4.0: 6.7, 63.0
5.0: 7.55, 77.1
6.0: 8.6, 93.9
7.0: 9.65, 110.9
"""

# Mouse in: 11:21
# Probe in: 11:52
# Probe used: DD02 (3 shanks, no TT7/8)

# exp0.add_site(800, tetrodes=[2,4])
# exp0.add_session('12-11-48', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-15-07', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('12-17-23', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(900, tetrodes=[2])
exp0.add_session('12-35-11', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-36-41', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('12-38-15', 'b', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-45-53', 'c', 'AM', 'am_tuning_curve')
exp0.add_session('12-53-07', 'd', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('13-27-17', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[1,2,4])
exp0.add_session('13-40-36', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-41-55', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('13-43-43', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-48-26', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('13-55-25', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('14-18-22', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[1,2,4])
exp0.add_session('14-30-40', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-32-27', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('14-34-24', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-38-52', 'i', 'AM', 'am_tuning_curve')
exp0.add_session('14-46-53', 'j', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-09-55', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[1,2,3,4])
exp0.add_session('15-24-21', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-26-23', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('15-29-49', 'k', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-34-21', 'l', 'AM', 'am_tuning_curve')
exp0.add_session('15-44-00', 'm', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-07-46', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,3,4,6])
exp0.add_session('16-26-13', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-27-38', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-30-12', 'n', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-35-41', 'o', 'AM', 'am_tuning_curve')
exp0.add_session('16-42-34', 'p', 'laserBandwidth', 'bandwidth_am') # 35kHz, 64 Hz
exp0.add_session('17-05-28', 'q', 'laserBandwidth', 'bandwidth_am') # 22kHz, 64 Hz
exp0.add_session('17-28-26', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[1,2,3,4,6])
exp0.add_session('17-38-46', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-40-16', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('17-41-56', 'r', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-46-25', 's', 'AM', 'am_tuning_curve')
exp0.add_session('17-54-13', 't', 'laserBandwidth', 'bandwidth_am') # 32kHz, 64Hz
exp0.add_session('18-17-12', 'u', 'laserBandwidth', 'bandwidth_am') # 22kHz, 64Hz
exp0.add_session('18-40-14', None, 'longLaserPulse', 'am_tuning_curve')

exp0.add_site(1500, tetrodes=[1,2,3,4,6])
exp0.add_session('18-50-31', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-52-28', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('18-54-03', 'v', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('18-58-28', 'w', 'AM', 'am_tuning_curve')
exp0.add_session('19-05-39', 'x', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('19-34-55', None, 'longLaserPulse', 'am_tuning_curve')

exp0.maxDepth = 1500


exp1 = celldatabase.Experiment(subject, '2019-09-24', 'left_AC', info=['medialDiO','TT8ant','soundright'])
experiments.append(exp1)

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 3.8, 17.9
2.0: 4.8, 33.5
3.0: 5.85, 50.0
4.0: 6.8, 65.3
5.0: 7.85, 81.5
6.0: 8.85, 98.0
7.0: 10.0, 117.2
"""

# Mouse in: 8:59
# Probe in: 9:19
# Probe used: DD02 (3 shanks, no TT7/8)

# exp1.add_site(900, tetrodes=[2,6])
# exp1.add_session('09-25-26', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1000, tetrodes=[2,4])
exp1.add_session('09-34-01', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('09-35-28', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('09-37-03', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('09-41-50', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('09-49-09', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('10-12-03', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[2,4,6])
exp1.add_session('10-21-44', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-23-13', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('10-25-02', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-29-22', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('10-36-07', 'f', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('10-59-04', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,3,4,6])
exp1.add_session('11-12-59', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-14-29', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('11-16-12', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-21-06', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('11-28-25', 'i', 'laserBandwidth', 'bandwidth_am') # 32kHz, 32 Hz
exp1.add_session('11-51-34', 'j', 'laserBandwidth', 'bandwidth_am') # 12kHz, 64 Hz
exp1.add_session('12-14-29', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,3,4,6])
exp1.add_session('12-27-04', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-28-25', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('12-30-00', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-34-47', 'l', 'AM', 'am_tuning_curve')
exp1.add_session('12-40-25', 'm', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-03-25', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1400, tetrodes=[1,2,3,4,6])
exp1.add_session('13-17-49', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-19-08', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-20-49', 'n', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-25-32', 'o', 'AM', 'am_tuning_curve')
exp1.add_session('13-31-54', 'p', 'laserBandwidth', 'bandwidth_am') # 32kHz, 32Hz
exp1.add_session('13-55-51', 'q', 'laserBandwidth', 'bandwidth_am') # 10kHz, 32Hz
exp1.add_session('14-18-48', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1500, tetrodes=[1,2,3,4,6])
exp1.add_session('14-29-29', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-31-00', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('14-32-35', 'r', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-37-20', 's', 'AM', 'am_tuning_curve')
exp1.add_session('14-43-44', 't', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('15-06-43', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1600, tetrodes=[1,2,3,4,6])
exp1.add_session('15-17-53', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-19-18', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-20-54', 'u', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-25-20', 'v', 'AM', 'am_tuning_curve')
exp1.add_session('15-31-32', 'w', 'laserBandwidth', 'bandwidth_am') # 32kHz, 64Hz
exp1.add_session('15-54-35', 'x', 'laserBandwidth', 'bandwidth_am') # 22kHz, 64Hz
exp1.add_session('16-17-28', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(1700, tetrodes=[1,2,3,4,6])
exp1.add_session('16-27-13', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-28-39', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('16-30-14', 'y', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-34-47', 'z', 'AM', 'am_tuning_curve')
exp1.add_session('16-40-57', 'aa', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('17-07-35', None, 'longLaserPulse', 'am_tuning_curve')

exp1.maxDepth = 1700


# switching to right side because shitter mouse pulled sylgard out of left well
exp2 = celldatabase.Experiment(subject, '2019-09-25', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp2)

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 4.05, 21.7
2.0: 5.4, 42.9
3.0: 6.75, 63.9
4.0: 8.05, 85.0
5.0: 9.45, 107.0
"""

# Mouse in: 9:43
# Probe in: 9:50
# Probe used: DD02 (3 shanks, no TT7/8)

exp2.add_site(1000, tetrodes=[2,4,6])
exp2.add_session('10-26-33', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-29-42', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('10-31-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-35-42', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('10-41-45', 'c', 'laserBandwidth', 'bandwidth_am') # 18kHz, 64Hz
exp2.add_session('11-05-02', 'd', 'laserBandwidth', 'bandwidth_am') # 27kHz, 64Hz
exp2.add_session('11-28-01', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1100, tetrodes=[2,4,6])
exp2.add_session('11-41-26', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-42-57', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('11-44-32', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-49-12', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('11-56-10', 'g', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('12-19-20', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1200, tetrodes=[1,2,4,6])
exp2.add_session('12-39-46', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-42-36', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('12-44-10', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-48-45', 'i', 'AM', 'am_tuning_curve')
exp2.add_session('12-55-11', 'j', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('13-27-12', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1300, tetrodes=[1,2,3,4,6])
exp2.add_session('13-35-32', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-36-57', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('13-38-29', 'k', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-42-47', 'l', 'AM', 'am_tuning_curve')
exp2.add_session('13-48-30', 'm', 'laserBandwidth', 'bandwidth_am') # 27kHz, 64Hz
exp2.add_session('14-13-44', 'n', 'laserBandwidth', 'bandwidth_am') # 5kHz, 64Hz
exp2.add_session('14-39-10', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1400, tetrodes=[1,2,3,4,6])
exp2.add_session('14-59-46', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-01-17', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('15-02-51', 'o', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-07-21', 'p', 'AM', 'am_tuning_curve')
exp2.add_session('15-13-54', 'q', 'laserBandwidth', 'bandwidth_am') # 10kHz, 64Hz
exp2.add_session('15-37-23', 'r', 'laserBandwidth', 'bandwidth_am') # 22kHz, 64Hz
exp2.add_session('16-02-14', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1500, tetrodes=[1,2,4,5,6])
exp2.add_session('16-11-08', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-12-42', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('16-14-16', 's', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-18-54', 't', 'AM', 'am_tuning_curve')
exp2.add_session('16-27-20', 'u', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('16-51-58', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1600, tetrodes=[1,2,4,5,6])
exp2.add_session('17-00-25', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-01-51', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('17-03-27', 'v', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-08-25', 'w', 'AM', 'am_tuning_curve')
exp2.add_session('17-15-20', 'x', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('17-38-18', None, 'longLaserPulse', 'am_tuning_curve')

exp2.maxDepth = 1600


exp3 = celldatabase.Experiment(subject, '2019-09-26', 'right_AC', info=['medialDiO','TT1ant','soundleft'])
experiments.append(exp3)

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 4.0, 21.3
2.0: 5.25, 40.6
3.0: 6.45, 60.1
4.0: 7.65, 79.0
5.0: 8.8, 97.3
"""

# Mouse in: 10:26
# Probe in: 10:31
# Probe used: DD02 (3 shanks, no TT7/8)

exp3.add_site(1000, tetrodes=[2])
exp3.add_session('11-01-20', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-02-49', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('11-04-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('11-08-56', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('11-13-49', 'c', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('11-36-46', None, 'longLaserPulse', 'am_tuning_curve')

# exp3.add_site(1100, tetrodes=[2])
# exp3.add_session('11-47-48', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[1,4])
# exp3.add_session('11-56-13', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1300, tetrodes=[2,4,6])
exp3.add_session('12-12-53', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-14-08', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('12-15-46', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-20-31', 'e', 'AM', 'am_tuning_curve')
exp3.add_session('12-26-36', 'f', 'laserBandwidth', 'bandwidth_am') # 32kHz, 64Hz
exp3.add_session('12-54-58', 'g', 'laserBandwidth', 'bandwidth_am') # 13kHz, 64Hz
exp3.add_session('13-17-57', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1400, tetrodes=[1,2,4,6])
exp3.add_session('13-27-59', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-29-18', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('13-30-45', 'h', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-35-06', 'i', 'AM', 'am_tuning_curve')
exp3.add_session('13-40-48', 'j', 'laserBandwidth', 'bandwidth_am') # 32kHz, 64Hz
exp3.add_session('14-04-03', 'k', 'laserBandwidth', 'bandwidth_am') # 12kHz, 64Hz
exp3.add_session('14-27-00', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1500, tetrodes=[1,2,3,4,6])
exp3.add_session('14-42-16', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-44-00', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('14-45-31', 'l', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-50-12', 'm', 'AM', 'am_tuning_curve')
exp3.add_session('14-58-23', 'n', 'laserBandwidth', 'bandwidth_am') # 18kHz, 32Hz
exp3.add_session('15-21-28', 'o', 'laserBandwidth', 'bandwidth_am') # 27kHz, 64Hz
exp3.add_session('15-44-48', 'p', 'laserBandwidth', 'bandwidth_am') # 9kHz, 32Hz
exp3.add_session('16-08-38', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1600, tetrodes=[1,2,3,4,6])
exp3.add_session('16-24-13', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-25-43', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-27-16', 'q', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-31-43', 'r', 'AM', 'am_tuning_curve')
exp3.add_session('16-37-36', 's', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('17-00-41', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1700, tetrodes=[1,2,3,4,6])
exp3.add_session('17-10-14', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-11-36', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('17-13-30', 't', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('17-17-56', 'u', 'AM', 'am_tuning_curve')
exp3.add_session('17-24-01', 'v', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('17-47-43', None, 'longLaserPulse', 'am_tuning_curve')

exp3.maxDepth = 1700


exp4 = celldatabase.Experiment(subject, '2019-09-27', 'right_AC', info=['middleDiD','TT1ant','soundleft'])
experiments.append(exp4)

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 4.05, 21.8
2.0: 5.4, 42.6
3.0: 6.7, 63.7
4.0: 8.0, 84.5
5.0: 9.35, 106.3
"""

# Mouse in: 8:30
# Probe in: 8:52
# Probe used: DD02 (3 shanks, no TT7/8)

# only one shank (TT5/6) penetrating
exp4.add_site(1200, tetrodes=[6])
exp4.add_session('09-54-45', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('09-56-54', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('09-58-23', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-03-16', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('10-08-47', 'c', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('10-31-45', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1300, tetrodes=[6])
exp4.add_session('10-42-59', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-44-39', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('10-46-12', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-50-33', 'e', 'AM', 'am_tuning_curve')
exp4.add_session('10-56-21', 'f', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('11-19-23', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[6])
exp4.add_session('11-29-52', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-31-52', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('11-33-27', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-37-45', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('11-44-42', 'i', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('12-07-39', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1500, tetrodes=[5,6])
exp4.add_session('12-20-50', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-22-14', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('12-23-57', 'j', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-28-17', 'k', 'AM', 'am_tuning_curve')
exp4.add_session('12-34-15', 'l', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('12-57-11', None, 'longLaserPulse', 'am_tuning_curve')

exp4.maxDepth = 1500


# exp5 = celldatabase.Experiment(subject, '2019-09-28', 'right_AC', info=['lateralDiO','TT1ant','soundleft'])
# experiments.append(exp5)
#
# """
# Laser Calibration
# Power: Value on laser dial, value in output level
# 1.0: 3.95, 19.8
# 2.0: 5.2, 39.1
# 3.0: 6.45, 58.8
# 4.0: 7.7, 78.8
# 5.0: 8.9, 98.0
# """

# Mouse in: 9:46
# Probe in: 9:55
# Probe used: DD02 (3 shanks, no TT7/8)

# tried several locations in craniotomy, shanks would not penetrate
