from jaratoolbox import celldatabase

subject = 'band045'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-01-25', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.35,
    '2.0':2.8,
    '2.5':3.4,
    '3.0':3.9,
    '3.5':4.6
}

# exp0.add_site(950, tetrodes=[2,4])
# exp0.add_session('13-13-29', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-14-50', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(975, tetrodes=[1,2,4,6,8])
exp0.add_session('13-23-25', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-24-25', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-26-05', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-34-10', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-38-27', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-40-36', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-43-41', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('14-02-07', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('14-13-17', 'e', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1025, tetrodes=[2,4,6,8])
# exp0.add_session('14-31-53', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-33-07', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[2,4,6,8])
# exp0.add_session('14-41-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1075, tetrodes=[2,4,6,8])
# exp0.add_session('14-48-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[2,4,6,8])
# exp0.add_session('15-04-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1125, tetrodes=[2,4,5,6,7,8])
# exp0.add_session('15-14-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[2,4,5,6,7,8])
# exp0.add_session('15-18-53', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-30-48', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-31-51', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-33-26', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-43-18', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('15-51-50', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-54-18', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-57-24', 'h', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-15-52', 'i', 'harmonics', 'bandwidth_am')
exp0.add_session('16-27-06', 'j', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1175


exp1 = celldatabase.Experiment(subject, '2018-01-26', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.75,
    '2.5':3.35,
    '3.0':3.85,
    '3.5':4.5
}
#TT7,8 flexing, not really penetrating

# exp1.add_site(1150, tetrodes=[2])
# exp1.add_session('15-37-57', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1200, tetrodes=[2])
# exp1.add_session('15-43-41', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[2,4,6])
# exp1.add_session('15-57-36', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('15-58-51', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1325, tetrodes=[1,2,4,6])
exp1.add_session('16-03-32', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-04-43', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-07-32', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-15-59', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('16-21-06', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-23-14', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('16-25-58', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-45-23', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('16-57-21', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1325


exp2 = celldatabase.Experiment(subject, '2018-01-30', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.75,
    '2.5':3.35,
    '3.0':3.85,
    '3.5':4.5
}

# exp2.add_site(900, tetrodes=[2,4])
# exp2.add_session('10-18-46', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('10-19-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(920, tetrodes=[2])
# exp2.add_session('10-32-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(940, tetrodes=[2,4])
# exp2.add_session('12-01-57', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(960, tetrodes=[2,4])
# exp2.add_session('12-10-39', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-11-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(980, tetrodes=[2,4])
# exp2.add_session('12-35-02', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1000, tetrodes=[1,2,4])
# exp2.add_session('12-42-25', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1020, tetrodes=[1,2,4])
# exp2.add_session('12-53-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1040, tetrodes=[2,4])
# exp2.add_session('12-59-43', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1060, tetrodes=[1,2,4])
# exp2.add_session('13-06-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1080, tetrodes=[1,2,4])
# exp2.add_session('13-11-49', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-12-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1100, tetrodes=[1,2,4])
# exp2.add_session('13-21-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1120, tetrodes=[1,2,4])
# exp2.add_session('13-26-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1140, tetrodes=[1,2,4])
# exp2.add_session('13-32-00', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1160, tetrodes=[1,2,4])
# exp2.add_session('13-36-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1180, tetrodes=[1,2,4])
# exp2.add_session('13-40-07', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-41-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes=[1,2,4])
# exp2.add_session('13-48-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1220, tetrodes=[1,2,4])
# exp2.add_session('13-53-03', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('13-54-09', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
# exp2.add_session('13-55-08', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1240, tetrodes=[1,2,4,8])
# exp2.add_session('14-06-05', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-06-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1260, tetrodes=[1,2,4,8])
# exp2.add_session('14-12-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1280, tetrodes=[1,2,4,8])
# exp2.add_session('14-17-41', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1300, tetrodes=[1,2,4,8])
exp2.add_session('14-23-02', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-23-53', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-24-56', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-33-00', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-37-38', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-39-49', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-41-50', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-16-45', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('15-45-53', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1300


exp3 = celldatabase.Experiment(subject, '2018-01-31', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.3,
    '2.0':2.8,
    '2.5':3.35,
    '3.0':3.9,
    '3.5':4.55
}

# exp3.add_site(750, tetrodes=[2,4,6])
# exp3.add_session('11-18-23', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('11-19-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(775, tetrodes=[2,4,6])
# exp3.add_session('11-55-41', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('11-56-47', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(800, tetrodes=[2,4,5,6])
# exp3.add_session('12-09-37', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('12-10-40', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(825, tetrodes=[2,4,5,6])
exp3.add_session('12-18-09', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-19-06', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-20-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-29-12', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-33-31', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-36-38', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-39-52', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-00-21', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-13-03', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(850, tetrodes=[2,4,5,6])
# exp3.add_session('13-35-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(875, tetrodes=[2,4,5,6])
# exp3.add_session('13-47-38', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(900, tetrodes=[2,4,5,6,7,8])
exp3.add_session('15-50-47', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-51-44', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-59-22', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-07-45', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('16-12-09', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-15-26', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('16-18-57', 'h', 'bandwidth', 'bandwidth_am')
exp3.add_session('16-37-24', 'i', 'harmonics', 'bandwidth_am')
exp3.add_session('16-48-33', 'j', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(950, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('17-04-52', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('17-06-12', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
#
# exp3.add_site(975, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('17-10-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('17-16-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1025, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('17-22-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes=[2,5,6,7,8])
# exp3.add_session('17-30-10', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('17-31-06', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes=[2,5,6,7,8])
# exp3.add_session('17-36-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[2,4,6,7,8])
# exp3.add_session('17-44-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1125, tetrodes=[1,2,4,6,7,8])
# exp3.add_session('17-50-28', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('17-51-36', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('18-02-11', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('18-03-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('18-08-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('18-13-04', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('18-15-12', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1225, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('18-21-07', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('18-22-09', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('18-29-25', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-30-52', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('18-34-28', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('18-42-39', 'l', 'AM', 'am_tuning_curve')
exp3.add_session('18-48-48', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-50-56', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('18-54-21', 'm', 'bandwidth', 'bandwidth_am')
exp3.add_session('19-14-35', 'n', 'harmonics', 'bandwidth_am')
exp3.add_session('19-26-04', 'o', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1250


exp4 = celldatabase.Experiment(subject, '2018-02-01', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.45,
    '1.0':1.85,
    '1.5':2.4,
    '2.0':3.1,
    '2.5':3.7,
    '3.0':4.5,
    '3.5':5.3
}

# exp4.add_site(1100, tetrodes=[2])
# exp4.add_session('13-23-29', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1150, tetrodes=[2,4])
# exp4.add_session('13-29-21', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[2,4])
# exp4.add_session('13-34-02', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-35-07', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1225, tetrodes=[2,4])
# exp4.add_session('13-47-18', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1250, tetrodes=[2,4])
# exp4.add_session('13-56-03', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1275, tetrodes=[1,2,4])
# exp4.add_session('14-13-40', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1300, tetrodes=[1,2,4])
# exp4.add_session('14-27-42', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1325, tetrodes=[1,2,4])
# exp4.add_session('14-33-24', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1350, tetrodes=[1,2,4])
exp4.add_session('14-51-58', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-53-05', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-54-41', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-02-56', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('15-07-14', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-09-21', None, 'laserTrain', 'am_tuning_curve')
#laser responsive units not sound responsive

exp4.maxDepth = 1350
