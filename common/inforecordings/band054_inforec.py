from jaratoolbox import celldatabase

subject = 'band054'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-02-20', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.8,
    '1.0':2.9,
    '1.5':4.1,
    '2.0':5.85,
    '2.5':9.1
}

# exp0.add_site(750, tetrodes=[1,2,4])
# exp0.add_session('10-44-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(800, tetrodes=[1,2,4])
# exp0.add_session('11-04-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(825, tetrodes=[1,2,4])
# exp0.add_session('11-13-13', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(850, tetrodes=[1,2,3,4])
# exp0.add_session('11-19-43', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(875, tetrodes=[1,2,4])
# exp0.add_session('11-44-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(900, tetrodes=[1,2,4,8])
# exp0.add_session('11-51-00', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-04-02', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(950, tetrodes=[1,2,4])
# exp0.add_session('13-14-45', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(975, tetrodes=[2,3,4,7,8])
# exp0.add_session('13-52-44', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1000, tetrodes=[1,2,4,6,7,8])
# exp0.add_session('14-02-49', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('14-15-47', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[2,4,6,8])
# exp0.add_session('15-08-18', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('15-25-07', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('15-34-16', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1250, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('15-40-23', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1300, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('15-47-55', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-49-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1325, tetrodes=[1,2,3,4])
# exp0.add_session('15-54-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1350, tetrodes=[2,3,4])
# exp0.add_session('16-00-37', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1375, tetrodes=[1,2,3,4])
exp0.add_session('16-07-32', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-08-48', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-10-02', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-31-04', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-38-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-40-49', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('16-43-37', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('17-19-29', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('17-30-39', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1375


exp1 = celldatabase.Experiment(subject, '2018-02-21', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.6,
    '1.0':2.3,
    '1.5':3.15,
    '2.0':4.2,
    '2.5':5.2,
    '3.0':6.3,
    '3.5':7.45
}

# exp1.add_site(700, tetrodes=[2,3,8])
# exp1.add_session('09-24-47', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(750, tetrodes=[2,8])
# exp1.add_session('09-48-43', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(825, tetrodes=[2,8])
# exp1.add_session('10-15-27', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(850, tetrodes=[2,8])
# exp1.add_session('10-26-26', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(900, tetrodes=[2,3,8])
# exp1.add_session('10-45-42', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[2,3,8])
# exp1.add_session('11-43-52', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[1,2,3,8])
# exp1.add_session('12-59-12', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1500, tetrodes=[2,3,8])
# exp1.add_session('15-30-52', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('15-31-44', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1525, tetrodes=[2,3,8])
# exp1.add_session('15-44-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1550, tetrodes=[2,8])
# exp1.add_session('15-52-18', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('15-53-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1575, tetrodes=[8])
# exp1.add_session('16-04-00', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1600, tetrodes=[2,8])
# exp1.add_session('16-15-04', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1625, tetrodes=[2,8])
exp1.add_session('16-26-47', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-27-45', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-29-04', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-37-12', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('16-41-30', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-44-10', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('16-48-20', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('17-07-40', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('17-20-01', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1625


exp2 = celldatabase.Experiment(subject, '2018-02-23', 'left_AC', info=['lateralDiI','TT1ant','sound_right'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.6,
    '1.0':2.35,
    '1.5':3.2,
    '2.0':4.05,
    '2.5':5.1,
    '3.0':6.5,
    '3.5':8.2
}

# exp2.add_site(1000, tetrodes=[2,4,8])
# exp2.add_session('13-34-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1100, tetrodes=[2,4,8])
# exp2.add_session('14-08-18', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1400, tetrodes=[2])
# exp2.add_session('16-40-41', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-41-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1425, tetrodes=[2])
# exp2.add_session('16-47-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1450, tetrodes=[2])
# exp2.add_session('16-54-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1475, tetrodes=[2])
# exp2.add_session('17-00-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1500, tetrodes=[2])
# exp2.add_session('17-06-33', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1520, tetrodes=[1,2,8])
exp2.add_session('17-12-11', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('17-13-15', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-16-05', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-24-53', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('17-29-21', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('17-31-25', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('17-34-31', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('17-56-34', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('18-08-57', 'e', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1540, tetrodes=[1,2,8])
# exp2.add_session('18-16-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1560, tetrodes=[1,2,8])
# exp2.add_session('18-24-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1580, tetrodes=[1,2,6,8])
# exp2.add_session('18-29-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1600, tetrodes=[1,2,4,6,8])
# exp2.add_session('18-34-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1620, tetrodes=[1,2,4,6,8])
# exp2.add_session('18-41-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1640, tetrodes=[1,2,4,6,8])
# exp2.add_session('18-45-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1660, tetrodes=[1,2,4,6,8])
# exp2.add_session('18-52-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1680, tetrodes=[1,2,4,6,7,8])
# exp2.add_session('18-55-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1700, tetrodes=[1,2,4,6,7,8])
# exp2.add_session('19-00-40', None, 'laserPulse', 'am_tuning_curve')

exp2.maxDepth = 1700


# exp3 = celldatabase.Experiment(subject, '2018-02-24', 'left_AC', info=['medialDiD','TT1ant','sound_right'])
# experiments.append(exp3)
#
# exp3.laserCalibration = {
#     '0.5':1.6,
#     '1.0':2.4,
#     '1.5':3.2,
#     '2.0':4.0,
#     '2.5':5.05,
#     '3.0':6.3,
#     '3.5':7.8
# }

# exp3.add_site(800, tetrodes=[8])
# exp3.add_session('11-41-07', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(850, tetrodes=[8])
# exp3.add_session('11-49-38', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(950, tetrodes=[7,8])
# exp3.add_session('12-22-07', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[7,8])
# exp3.add_session('12-31-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1025, tetrodes=[6,7,8])
# exp3.add_session('12-40-00', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('12-41-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes=[3,4,7,8])
# exp3.add_session('13-02-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[8])
# exp3.add_session('13-12-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[7,8])
# exp3.add_session('13-44-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1500, tetrodes=[8])
# exp3.add_session('15-02-37', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('15-03-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1525, tetrodes=[8])
# exp3.add_session('15-12-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1550, tetrodes=[8])
# exp3.add_session('15-18-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1575, tetrodes=[8])
# exp3.add_session('15-26-23', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1600, tetrodes=[8])
# exp3.add_session('15-31-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1625, tetrodes=[8])
# exp3.add_session('15-40-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1650, tetrodes=[8])
# exp3.add_session('15-43-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1675, tetrodes=[8])
# exp3.add_session('15-51-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1700, tetrodes=[8])
# exp3.add_session('15-56-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1725, tetrodes=[8])
# exp3.add_session('16-01-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1750, tetrodes=[7,8])
# exp3.add_session('16-07-41', None, 'laserPulse', 'am_tuning_curve')


# exp4 = celldatabase.Experiment(subject, '2018-02-27', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':1.6,
#     '1.0':2.4,
#     '1.5':3.2,
#     '2.0':4.0,
#     '2.5':5.05,
#     '3.0':6.3,
#     '3.5':7.8
# } #switched probe after initial insertion, using previous laser calibration for this probe

# exp4.add_site(750, tetrodes=[2,3,4,6,8])
# exp4.add_session('09-55-46', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(800, tetrodes=[2,4,6,8])
# exp4.add_session('10-25-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(850, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('10-38-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(875, tetrodes=[2,4,6,8])
# exp4.add_session('10-43-18', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('10-44-27', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
#
# exp4.add_site(900, tetrodes=[2,4,6])
# exp4.add_session('10-58-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(925, tetrodes=[2,4,6])
# exp4.add_session('11-13-45', None, 'laserPulse', 'am_tuning_curve') #realised laser was not connected because I'm an idiot
#
# exp4.add_site(950, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('11-22-30', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('11-30-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(975, tetrodes=[2,3,4,5,6,8])
# exp4.add_session('11-41-52', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1000, tetrodes=[1,2,5,7])
# exp4.add_session('11-53-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1020, tetrodes=[1,2,5,6,7,8])
# exp4.add_session('12-06-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1040, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('12-19-51', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-28-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1060, tetrodes=[1,2,3,4,8])
# exp4.add_session('12-39-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1080, tetrodes=[1,2,7,8])
# exp4.add_session('12-54-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1100, tetrodes=[1,2,7,8])
# exp4.add_session('13-01-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1120, tetrodes=[2,4])
# exp4.add_session('13-08-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1140, tetrodes=[2,4,8])
# exp4.add_session('13-15-38', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('13-20-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1160, tetrodes=[1,2,4,8])
# exp4.add_session('13-31-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1180, tetrodes=[2,4,6,8])
# exp4.add_session('13-41-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[1,2,4,8])
# exp4.add_session('13-48-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1220, tetrodes=[1,2,3,4,8])
# exp4.add_session('13-57-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1240, tetrodes=[2,4,6,8])
# exp4.add_session('14-10-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1260, tetrodes=[1,2,4,8])
# exp4.add_session('14-19-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1280, tetrodes=[1,2,4,8])
# exp4.add_session('14-29-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1300, tetrodes=[1,2,4,8])
# exp4.add_session('14-40-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1325, tetrodes=[1,2,4,8])
# exp4.add_session('14-47-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1350, tetrodes=[1,2,8])
# exp4.add_session('14-57-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1400, tetrodes=[1,2])
# exp4.add_session('15-07-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1450, tetrodes=[1,2,4,8])
# exp4.add_session('15-17-04', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('15-18-25', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1490, tetrodes=[1,2,4,8])
# exp4.add_session('15-27-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1510, tetrodes=[1,2,8])
# exp4.add_session('15-37-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1550, tetrodes=[2,7,8])
# exp4.add_session('15-48-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1575, tetrodes=[1,2,8])
# exp4.add_session('15-59-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1600, tetrodes=[1,2,8])
# exp4.add_session('16-09-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1625, tetrodes=[1,2])
# exp4.add_session('16-16-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1650, tetrodes=[1,2,8])
# exp4.add_session('16-27-08', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1675, tetrodes=[1,2,8])
# exp4.add_session('16-37-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1700, tetrodes=[2,8])
# exp4.add_session('16-50-13', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('16-51-26', None, 'noisebursts', 'am_tuning_curve')


# exp5 = celldatabase.Experiment(subject, '2018-03-01', 'right_AC', info=['medialDiD','TT1ant','sound_left'])
# experiments.append(exp5)
#
# exp5.laserCalibration = {
#     '0.5':1.55,
#     '1.0':2.2,
#     '1.5':2.9,
#     '2.0':3.7,
#     '2.5':4.65,
#     '3.0':6.0,
#     '3.5':7.45
# }

# exp5.add_site(800, tetrodes=[8])
# exp5.add_session('12-15-17', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(850, tetrodes=[8])
# exp5.add_session('12-24-26', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(900, tetrodes=[6,8])
# exp5.add_session('12-39-52', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(925, tetrodes=[6,8])
# exp5.add_session('12-51-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(950, tetrodes=[6,8])
# exp5.add_session('13-08-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(975, tetrodes=[6,8])
# exp5.add_session('13-14-44', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('13-15-38', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1000, tetrodes=[6,8])
# exp5.add_session('13-23-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1025, tetrodes=[4,6,8])
# exp5.add_session('13-47-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1050, tetrodes=[6,8])
# exp5.add_session('13-57-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1075, tetrodes=[4,6,8])
# exp5.add_session('14-12-29', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1100, tetrodes=[4,6,8])
# exp5.add_session('14-28-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1125, tetrodes=[4,6,8])
# exp5.add_session('14-40-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1150, tetrodes=[4,6,8])
# exp5.add_session('14-49-27', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('14-50-26', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1175, tetrodes=[4,5,6,8])
# exp5.add_session('15-06-13', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('15-07-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1200, tetrodes=[4,5,6,8])
# exp5.add_session('15-16-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1225, tetrodes=[4,5,6,8])
# exp5.add_session('15-28-22', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('15-30-32', 'a', 'tuningCurve', 'am_tuning_curve')
# #not really sound responsive
#
# exp5.add_site(1250, tetrodes=[4,5,6,8])
# exp5.add_session('15-50-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1275, tetrodes=[3,6,8])
# exp5.add_session('15-59-23', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1300, tetrodes=[8])
# exp5.add_session('16-12-37', None, 'laserPulse', 'am_tuning_curve')


exp6 = celldatabase.Experiment(subject, '2018-03-02', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp6)

exp6.laserCalibration = {
    '0.5':1.6,
    '1.0':2.45,
    '1.5':3.25,
    '2.0':4.15,
    '2.5':5.35,
    '3.0':6.8,
    '3.5':8.4
}

# exp6.add_site(925, tetrodes=[8])
# exp6.add_session('12-37-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1050, tetrodes=[2,4,8])
# exp6.add_session('14-18-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1100, tetrodes=[2,4,8])
# exp6.add_session('14-27-43', None, 'laserPulse', 'am_tuning_curve')

exp6.add_site(1125, tetrodes=[2,4,6,8])
exp6.add_session('14-34-56', None, 'laserPulse', 'am_tuning_curve')
exp6.add_session('14-35-56', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-37-19', 'a', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('14-46-01', 'b', 'AM', 'am_tuning_curve')
exp6.add_session('14-50-15', None, 'laserPulse', 'am_tuning_curve')
# RIP laser response

# exp6.add_site(1150, tetrodes=[2,4,7,8])
# exp6.add_session('14-57-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1175, tetrodes=[1,2,4,7,8])
# exp6.add_session('15-03-53', None, 'laserPulse', 'am_tuning_curve')
# exp6.add_session('15-05-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp6.add_site(1200, tetrodes=[1,2,4,7,8])
# exp6.add_session('15-09-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1225, tetrodes=[1,2,4,8])
# exp6.add_session('15-14-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1250, tetrodes=[1,2,3,4,8])
# exp6.add_session('15-25-51', None, 'laserPulse', 'am_tuning_curve')
# exp6.add_session('15-27-42', 'c', 'tuningCurve', 'am_tuning_curve')
#
# exp6.add_site(1275, tetrodes=[1,2,3,4,8])
# exp6.add_session('15-39-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1300, tetrodes=[1,2,3,4,8])
# exp6.add_session('15-48-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1325, tetrodes=[1,2,3,4,8])
# exp6.add_session('15-56-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1350, tetrodes=[1,2,3,4,8])
# exp6.add_session('16-09-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1375, tetrodes=[1,2,3,4,8])
# exp6.add_session('16-20-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp6.add_site(1400, tetrodes=[1,2,3,4,8])
# exp6.add_session('16-26-55', None, 'laserPulse', 'am_tuning_curve')

exp6.add_site(1425, tetrodes=[1,2,3,4,8])
exp6.add_session('16-33-46', None, 'laserPulse', 'am_tuning_curve')
exp6.add_session('16-35-23', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-37-57', 'd', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('16-47-07', 'e', 'AM', 'am_tuning_curve')
exp6.add_session('16-51-28', None, 'laserPulse', 'am_tuning_curve')
exp6.add_session('16-54-11', None, 'laserTrain', 'am_tuning_curve')
#RIP laser response AGAIN

exp6.maxDepth = 1425


# exp7 = celldatabase.Experiment(subject, '2018-03-06', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
# experiments.append(exp7)
#
# exp7.laserCalibration = {
#     '0.5':1.5,
#     '1.0':2.2,
#     '1.5':2.95,
#     '2.0':3.65,
#     '2.5':4.5,
#     '3.0':5.7,
#     '3.5':6.8
# }

# exp7.add_site(1000, tetrodes=[2,4,6,8])
# exp7.add_session('13-00-36', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1075, tetrodes=[2,4,6,8])
# exp7.add_session('13-28-06', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1100, tetrodes=[2,4,6,8])
# exp7.add_session('13-45-56', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1150, tetrodes=[2,4,8])
# exp7.add_session('14-09-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1175, tetrodes=[2,4,8])
# exp7.add_session('14-19-09', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1200, tetrodes=[2,4,8])
# exp7.add_session('14-29-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1225, tetrodes=[2,4,6,8])
# exp7.add_session('14-38-59', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1250, tetrodes=[2,4,8])
# exp7.add_session('14-53-33', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1275, tetrodes=[2,4,6,8])
# exp7.add_session('15-00-33', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1300, tetrodes=[2,4,8])
# exp7.add_session('15-06-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1325, tetrodes=[2,4,8])
# exp7.add_session('15-13-23', None, 'noisebursts', 'am_tuning_curve')
# exp7.add_session('15-14-23', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1350, tetrodes=[2,4,6,8])
# exp7.add_session('15-26-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1375, tetrodes=[2,4,6,8])
# exp7.add_session('15-35-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1400, tetrodes=[2,4,6,8])
# exp7.add_session('15-41-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1425, tetrodes=[2,4,6,8])
# exp7.add_session('15-48-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1450, tetrodes=[2,4,6,8])
# exp7.add_session('15-53-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1475, tetrodes=[2,4,6,8])
# exp7.add_session('16-03-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1500, tetrodes=[2,4,6,7,8])
# exp7.add_session('16-16-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1525, tetrodes=[2,4,6,7,8])
# exp7.add_session('16-24-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1550, tetrodes=[2,4,6,7,8])
# exp7.add_session('16-33-12', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1575, tetrodes=[2,4,7,8])
# exp7.add_session('16-39-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1600, tetrodes=[2,4,7,8])
# exp7.add_session('16-50-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1625, tetrodes=[2,4,7,8])
# exp7.add_session('16-56-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1650, tetrodes=[2,4,7,8])
# exp7.add_session('17-04-08', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1675, tetrodes=[2,4,7,8])
# exp7.add_session('17-13-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp7.add_site(1700, tetrodes=[2,4,7,8])
# exp7.add_session('17-22-17', None, 'laserPulse', 'am_tuning_curve')
