from jaratoolbox import celldatabase

subject = 'band102'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-10-20', 'left_AC', info=['medialDiD','TT8ant','soundright'])
experiments.append(exp0)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 3.05, 06.6
2.0: 3.25, 10.0
3.0: 3.45, 13.4
4.0: 3.65, 16.5
5.0: 3.9, 19.7
6.0: 4.25, 23.8
7.0: 4.4, 27.3
"""

# Mouse in: 12:45
# Probe in: 1:05
# Probe used: P427 (no fibre yet)

# exp0.add_site(1200, tetrodes=[2,4,6,8])
# exp0.add_session('14-04-44', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1400, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('14-47-46', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1500, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('14-59-17', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1600, tetrodes=[1,2,3,4,6,7,8])
# exp0.add_session('15-24-36', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1700, tetrodes=[1,2,3,4,6,7,8])
# exp0.add_session('15-32-14', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1800, tetrodes=[1,2,3,4,6,7,8])
# exp0.add_session('15-45-08', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1900, tetrodes=[2,6,8])
# exp0.add_session('16-01-26', None, 'noisebursts', 'am_tuning_curve')

exp0.maxDepth = 1900


exp1 = celldatabase.Experiment(subject, '2019-10-21', 'left_AC', info=['middleDiO','TT8ant','soundright'])
experiments.append(exp1)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 3.05, 06.6
2.0: 3.25, 10.0
3.0: 3.45, 13.4
4.0: 3.65, 16.5
5.0: 3.9, 19.7
6.0: 4.25, 23.8
7.0: 4.4, 27.3
"""

# Mouse in: 1:30
# Probe in: 1:42
# Probe used: DD02 (3 shanks, no TT7/8)

# exp1.add_site(900, tetrodes=[1,2,4,5,6])
# exp1.add_session('14-04-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1000, tetrodes=[2,4,5,6])
# exp1.add_session('14-17-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[5,6])
# exp1.add_session('14-24-28', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1200, tetrodes=[5,6])
# exp1.add_session('14-35-53', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[1,2,4,5,6])
# exp1.add_session('14-42-37', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1400, tetrodes=[1,2,4,5,6])
# exp1.add_session('14-51-59', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1500, tetrodes=[1,2,5,6])
exp1.add_session('15-03-11', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-04-38', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-06-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-11-10', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('15-17-37', 'c', 'laserBandwidthControl', 'bandwidth_am')
exp1.add_session('15-40-56', None, 'longLaserPulse', 'am_tuning_curve')

# exp1.add_site(1600, tetrodes=[2,4,5,6])
# exp1.add_session('15-55-21', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1700, tetrodes=[1,2,4,5,6])
exp1.add_session('16-08-19', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-09-49', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('16-11-19', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-15-51', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('16-22-01', 'f', 'laserBandwidthControl', 'bandwidth_am')
exp1.add_session('16-45-01', None, 'longLaserPulse', 'am_tuning_curve')

exp1.maxDepth = 1700


exp2 = celldatabase.Experiment(subject, '2019-10-22', 'left_AC', info=['lateralDiD','TT8ant','soundright'])
experiments.append(exp2)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 3.8, 18.6
2.0: 4.9, 35.0
3.0: 6.0, 52.2
4.0: 7.05, 68.9
5.0: 8.1, 85.7
6.0: 9.3, 105.4
"""

# Mouse in: 11:37
# Probe in: 11:50
# Probe used: DD02 (3 shanks, no TT7/8)
# shanks having some trouble penetrating after ~800 um

# exp2.add_site(1200, tetrodes=[6])
# exp2.add_session('13-01-23', None, 'noisebursts', 'am_tuning_curve')

# Probe pulled out at 1:14 and repositioned more medially
# Probe pulled out again at 1:44, pulled big chunk of tissue off surface, reinserted probe at 1:59 without issue

exp2.add_site(1000, tetrodes=[2,4,6])
exp2.add_session('14-00-55', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-02-35', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('14-04-31', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-09-09', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-15-55', 'c', 'laserBandwidth', 'bandwidth_am') # 32kHz, 64Hz
exp2.add_session('14-38-51', 'd', 'laserBandwidth', 'bandwidth_am') # 8kHz, 64Hz
exp2.add_session('15-02-13', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1100, tetrodes=[2,3,4,6])
exp2.add_session('15-16-24', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-17-43', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('15-19-08', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-24-03', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('15-30-43', 'g', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('15-53-42', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1200, tetrodes=[1,2,3,4,6])
exp2.add_session('16-04-20', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-06-00', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('16-07-21', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-12-00', 'i', 'AM', 'am_tuning_curve')
exp2.add_session('16-18-28', 'j', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('16-44-47', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1300, tetrodes=[1,2,3,4,6])
exp2.add_session('16-54-33', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-56-09', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('16-57-35', 'k', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-02-03', 'l', 'AM', 'am_tuning_curve')
exp2.add_session('17-09-18', 'm', 'laserBandwidth', 'bandwidth_am') # 14kHz, 64hZ
exp2.add_session('17-35-29', 'n', 'laserBandwidth', 'bandwidth_am') # 22kHz, 64Hz
exp2.add_session('17-58-29', None, 'longLaserPulse', 'am_tuning_curve')

exp2.add_site(1400, tetrodes=[1,2,3,4,6])
exp2.add_session('18-07-30', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('18-08-56', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('18-10-22', 'o', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('18-15-57', 'p', 'AM', 'am_tuning_curve')
exp2.add_session('18-23-01', 'q', 'laserBandwidth', 'bandwidth_am') # 12kHz, 64Hz
exp2.add_session('18-46-55', 'r', 'laserBandwidth', 'bandwidth_am')# 27kHz, 64Hz
exp2.add_session('19-10-15', None, 'longLaserPulse', 'am_tuning_curve')

exp2.maxDepth = 1400


# exp3 = celldatabase.Experiment(subject, '2019-10-23', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
# experiments.append(exp3)
#
# """
# Laser Calibration (from tether, not fibre)
# Power: Value on laser dial, value in output level
# 1.0: 3.7, 19.0
# 2.0: 5.1, 37.5
# 3.0: 6.25, 55.7
# 4.0: 7.4, 74.1
# 5.0: 8.7, 94.9
# 6.0: 10.0, 116.4
# """

# Mouse in: 12:38
# Probe in: session cancelled, mouse bled continuously, heavily from cranitomy for over three hours
# Probe used: DD02 (3 shanks, no TT7/8)


exp3 = celldatabase.Experiment(subject, '2019-10-24', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp3)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 3.7, 19.0
2.0: 5.1, 37.5
3.0: 6.25, 55.7
4.0: 7.4, 74.1
5.0: 8.7, 94.9
6.0: 10.0, 116.4
"""

# Mouse in: 10:13
# Probe in: 11:05
# Probe used: DD02 (3 shanks, no TT7/8)

# exp3.add_site(1000, tetrodes=[2,4,6])
# exp3.add_session('11-17-46', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[2,4,6])
# exp3.add_session('11-55-21', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[2,4,6])
# exp3.add_session('12-12-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1400, tetrodes=[2,4,6])
# exp3.add_session('12-19-42', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('12-21-44', None, 'lasernoisebursts', 'bandwidth_am')
# exp3.add_session('12-23-09', 'a', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('12-27-42', 'b', 'AM', 'am_tuning_curve')
# pretty poor tuning

exp3.add_site(1500, tetrodes=[2,4,6])
exp3.add_session('12-43-36', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-45-03', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('12-46-51', 'c', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-51-56', 'd', 'AM', 'am_tuning_curve')
exp3.add_session('12-57-36', 'e', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('13-20-45', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1600, tetrodes=[1,2,4,6])
exp3.add_session('13-37-39', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-39-12', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('13-40-44', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-45-15', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('13-52-13', 'h', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('14-16-00', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1700, tetrodes=[1,2,4,6])
exp3.add_session('14-25-39', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-27-15', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('14-28-46', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-33-36', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('14-39-09', 'k', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('15-04-15', None, 'longLaserPulse', 'am_tuning_curve')

exp3.add_site(1800, tetrodes=[1,2,4,5,6])
exp3.add_session('16-18-56', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-20-21', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-21-41', 'l', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-27-36', 'm', 'AM', 'am_tuning_curve')
exp3.add_session('16-33-24', 'n', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('16-57-12', None, 'longLaserPulse', 'am_tuning_curve')

exp3.maxDepth = 1800


exp4 = celldatabase.Experiment(subject, '2019-10-25', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
experiments.append(exp4)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 4.1, 23.0
2.0: 5.4, 43.2
3.0: 6.7, 64.2
4.0: 8.0, 84.2
5.0: 9.4, 107.1
"""

# Mouse in: 11:40
# Probe in: 12:00, pulled out when shanks flexing, reinserted 12:42, TT5/6 not penetrating well
# Probe used: DD02 (3 shanks, no TT7/8)

# exp4.add_site(1200, tetrodes=[4])
# exp4.add_session('13-33-39', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-34-57', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('13-36-36', 'a', 'tuningCurve', 'am_tuning_curve')
# poor tuning

exp4.add_site(1300, tetrodes=[2,4])
exp4.add_session('13-53-06', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-54-27', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-55-48', 'b', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-00-26', 'c', 'AM', 'am_tuning_curve')
exp4.add_session('14-06-29', 'd', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-29-30', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[2,4])
exp4.add_session('14-43-31', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-45-53', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('14-47-25', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-52-18', 'f', 'AM', 'am_tuning_curve')
exp4.add_session('14-57-11', 'g', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('15-25-28', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1500, tetrodes=[2,4])
exp4.add_session('15-33-26', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-34-49', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-36-11', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-40-27', 'i', 'AM', 'am_tuning_curve')
exp4.add_session('15-46-47', 'j', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('16-10-26', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1600, tetrodes=[2,4])
exp4.add_session('16-23-40', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-24-58', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('16-26-26', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-30-59', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('16-36-57', 'm', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('17-00-02', None, 'longLaserPulse', 'am_tuning_curve')

exp4.add_site(1700, tetrodes=[2,4])
exp4.add_session('17-08-09', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('17-10-00', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('17-11-19', 'n', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('17-16-10', 'o', 'AM', 'am_tuning_curve')
exp4.add_session('17-21-48', 'p', 'laserBandwidth', 'bandwidth_am') # 27kHz, 64Hz
exp4.add_session('17-46-09', 'q', 'laserBandwidth', 'bandwidth_am') # 14kHz, 16Hz
exp4.add_session('18-09-16', None, 'longLaserPulse', 'am_tuning_curve')

exp4.maxDepth = 1700


exp5 = celldatabase.Experiment(subject, '2019-10-26', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp5)

"""
Laser Calibration (from tether, not fibre)
Power: Value on laser dial, value in output level
1.0: 3.7, 17.1
2.0: 4.7, 32.1
3.0: 5.7, 47.6
4.0: 6.7, 63.7
5.0: 7.6, 77.8
6.0: 8.75, 96.8
7.0: 9.8, 113.8
"""

# Mouse in: 3:13
# Probe in: 3:44, middle shank (TT3/4) not penetrating well
# Probe used: DD02 (3 shanks, no TT7/8)

# exp5.add_site(1000, tetrodes=[2,6])
# exp5.add_session('15-56-19', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(1200, tetrodes=[2,6])
exp5.add_session('16-17-47', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-19-08', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('16-20-26', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-26-01', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('16-31-14', 'c', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('16-54-12', None, 'longLaserPulse', 'am_tuning_curve')

exp5.add_site(1300, tetrodes=[1,2,6])
exp5.add_session('17-03-37', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-04-56', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('17-06-22', 'd', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-11-13', 'e', 'AM', 'am_tuning_curve')
exp5.add_session('17-17-08', 'f', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('17-40-07', None, 'longLaserPulse', 'am_tuning_curve')

exp5.add_site(1400, tetrodes=[1,2,6])
exp5.add_session('17-59-34', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('18-01-24', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('18-02-59', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-07-21', 'h', 'AM', 'am_tuning_curve')
exp5.add_session('18-12-27', 'i', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('18-35-28', None, 'longLaserPulse', 'am_tuning_curve')

exp5.add_site(1500, tetrodes=[1,2,6])
exp5.add_session('18-46-00', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('18-47-25', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('18-49-00', 'j', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-53-24', 'k', 'AM', 'am_tuning_curve')
exp5.add_session('18-58-48', 'l', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('19-21-39', None, 'longLaserPulse', 'am_tuning_curve')

exp5.maxDepth = 1500
