from jaratoolbox import celldatabase

subject = 'band044'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-01-09', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.35,
    '1.0':1.7,
    '1.5':2.15,
    '2.0':2.6,
    '2.5':3.1,
    '3.0':3.65,
    '3.5':4.3
}

# exp0.add_site(975, tetrodes=[4,6,8])
# exp0.add_session('10-58-39', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('11-00-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1000, tetrodes=[4,6,8])
# exp0.add_session('11-11-55', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1025, tetrodes=[4,6,8])
# exp0.add_session('11-26-35', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('11-27-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[6])
# exp0.add_session('12-16-30', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-17-21', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[6,8])
# exp0.add_session('12-39-19', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-40-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1125, tetrodes=[6,8])
# exp0.add_session('13-04-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[5,6,8])
# exp0.add_session('13-19-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1175, tetrodes=[5,6,7,8])
# exp0.add_session('13-26-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes=[5,6,7,8])
# exp0.add_session('13-30-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1225, tetrodes=[5,6,8])
# exp0.add_session('13-47-47', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('13-48-39', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1250, tetrodes=[2,6,7,8])
# exp0.add_session('14-03-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1275, tetrodes=[2,7,8])
# exp0.add_session('14-15-44', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[2,7,8])
exp0.add_session('14-19-48', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-20-36', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-21-50', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-29-55', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-34-10', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-36-31', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-40-25', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('15-00-15', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('15-18-33', 'e', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1350, tetrodes=[1,2,4,6,7,8])
# exp0.add_session('15-25-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1375, tetrodes=[1,2,4,5,7,8])
# exp0.add_session('15-28-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1400, tetrodes=[1,2,5,6,7,8])
# exp0.add_session('15-32-22', None, 'laserPulse', 'am_tuning_curve')

exp0.maxDepth = 1400


exp1 = celldatabase.Experiment(subject, '2018-01-10', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.35,
    '2.0':2.9,
    '2.5':3.5,
    '3.0':4.1,
    '3.5':4.85
}

# exp1.add_site(1100, tetrodes=[2,6])
# exp1.add_session('12-39-59', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1150, tetrodes=[2,7])
# exp1.add_session('12-58-55', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1250, tetrodes=[2,7])
# exp1.add_session('14-43-09', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-04-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-05-56', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-07-37', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-15-52', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('16-20-27', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-22-34', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('16-25-36', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-44-32', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('16-56-56', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1300


exp2 = celldatabase.Experiment(subject, '2018-01-11', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.35,
    '2.0':2.95,
    '2.5':3.55,
    '3.0':4.1,
    '3.5':4.75
}
# exp2.add_site(950, tetrodes=[2,4])
# exp2.add_session('11-20-50', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1000, tetrodes=[1,2,4])
# exp2.add_session('11-25-47', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('11-27-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1100, tetrodes=[1,6,7,8])
# exp2.add_session('11-39-53', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1150, tetrodes=[1,2,6,7,8])
# exp2.add_session('11-53-12', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1175, tetrodes=[1,2,6,7])
# exp2.add_session('12-02-58', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes=[1,2,6,7,8])
# exp2.add_session('12-12-35', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-13-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1225, tetrodes=[1,2,6,7])
# exp2.add_session('12-25-27', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('12-26-45', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1250, tetrodes=[1,2,4,6])
exp2.add_session('13-03-21', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-04-21', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-05-42', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-14-09', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-18-30', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-20-35', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-24-42', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-52-23', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('14-04-54', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1300, tetrodes=[1,2,4,6,7])
exp2.add_session('14-14-44', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-16-03', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-18-53', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-27-29', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('14-32-18', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-35-13', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-41-21', 'h', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-59-44', 'i', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-26-25', 'j', 'harmonics', 'bandwidth_am')
exp2.add_session('15-39-09', 'k', 'harmonics', 'bandwidth_am')
exp2.add_session('15-58-54', 'l', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1300


exp3 = celldatabase.Experiment(subject, '2018-01-12', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.45,
    '1.0':2.0,
    '1.5':2.7,
    '2.0':3.25,
    '2.5':3.9,
    '3.0':4.6,
    '3.5':5.6
}

# exp3.add_site(700, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('12-00-24', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('12-01-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(725, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('12-20-27', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(750, tetrodes=[2,4,5,6,7,8])
exp3.add_session('12-28-54', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-30-27', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-32-01', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-40-04', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-46-25', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-48-31', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-52-25', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-16-45', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-30-59', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(800, tetrodes=[2,4,6,7,8])
# exp3.add_session('13-51-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(825, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('13-55-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(850, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('14-01-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(875, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('14-09-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(900, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('14-13-37', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(925, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('14-17-28', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-18-26', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-20-29', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-28-36', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('14-33-00', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-35-10', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-37-55', 'h', 'bandwidth', 'bandwidth_am')
exp3.add_session('14-57-34', 'i', 'harmonics', 'bandwidth_am')
exp3.add_session('15-08-59', 'j', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('15-24-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1025, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('15-39-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('15-51-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('15-58-50', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('15-59-51', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-05-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-09-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-12-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-15-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-19-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1225, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-22-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('16-25-44', None, 'laserPulse', 'am_tuning_curve')

exp3.maxDepth = 1250


exp4 = celldatabase.Experiment(subject, '2018-01-15', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.8,
    '2.5':3.35,
    '3.0':3.9,
    '3.5':4.6
}

# exp4.add_site(700, tetrodes=[2,4,6,8])
# exp4.add_session('12-02-11', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-03-08', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(725, tetrodes=[2,4,6,8])
# exp4.add_session('12-16-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(750, tetrodes=[2,4,6,8])
# exp4.add_session('12-21-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(775, tetrodes=[2,4,6,8])
# exp4.add_session('12-29-19', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(800, tetrodes=[2,4,6,8])
exp4.add_session('12-35-22', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-37-26', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-39-07', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-47-11', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('12-51-27', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-53-36', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('12-57-06', 'c', 'bandwidth', 'bandwidth_am')
exp4.add_session('13-20-01', 'd', 'harmonics', 'bandwidth_am')
exp4.add_session('13-33-16', 'e', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(850, tetrodes=[2,4,6,8])
# exp4.add_session('13-51-46', None, 'laserPulse', 'am_tuning_curve')

# exp4.add_site(875, tetrodes=[2,4,6,8])
# exp4.add_session('13-56-04', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('13-57-06', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
# exp4.add_session('13-58-01', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-59-32', 'f', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('14-08-03', 'g', 'AM', 'am_tuning_curve')
# exp4.add_session('14-12-17', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('14-14-38', None, 'laserTrain', 'am_tuning_curve')
# exp4.add_session('14-17-10', 'h', 'bandwidth', 'bandwidth_am')
# exp4.add_session('14-36-55', 'i', 'harmonics', 'bandwidth_am')
# exp4.add_session('14-48-08', 'j', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(925, tetrodes=[2,4,6,8])
exp4.add_session('14-58-11', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-59-44', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-01-10', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-09-30', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('15-15-08', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-17-35', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('15-20-38', 'm', 'bandwidth', 'bandwidth_am')
exp4.add_session('15-39-04', 'n', 'harmonics', 'bandwidth_am')
exp4.add_session('15-50-13', 'o', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1000, tetrodes=[2,4,6,8])
# exp4.add_session('16-02-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1025, tetrodes=[2,4,6,8])
# exp4.add_session('16-10-13', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1050, tetrodes=[2,4,6,8])
exp4.add_session('16-14-45', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-17-06', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-19-11', 'p', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-27-13', 'q', 'AM', 'am_tuning_curve')
exp4.add_session('16-31-33', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-33-56', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('16-36-31', 'r', 'bandwidth', 'bandwidth_am')
exp4.add_session('16-54-55', 's', 'harmonics', 'bandwidth_am')
exp4.add_session('17-06-28', 't', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1100, tetrodes=[2,4,6,8])
# exp4.add_session('17-18-26', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1125, tetrodes=[2,4,6,8])
exp4.add_session('17-27-47', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('17-29-11', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('17-30-59', 'u', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('17-39-23', 'v', 'AM', 'am_tuning_curve')
exp4.add_session('17-44-46', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('17-46-52', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('17-51-35', 'w', 'bandwidth', 'bandwidth_am')
exp4.add_session('18-12-08', 'x', 'harmonics', 'bandwidth_am')
exp4.add_session('18-24-06', 'y', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1125


exp5 = celldatabase.Experiment(subject, '2018-01-16', 'left_AC', info=['lateralDiI','TT1ant','sound_right'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.9,
    '2.5':3.5,
    '3.0':4.05,
    '3.5':4.75
}

# exp5.add_site(700, tetrodes=[2])
# exp5.add_session('13-09-51', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(750, tetrodes=[2])
# exp5.add_session('13-43-50', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('13-44-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(800, tetrodes=[2,6])
# exp5.add_session('13-55-29', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(825, tetrodes=[1,2,4,6,8])
exp5.add_session('14-10-16', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-11-17', None, 'laserPulse', 'am_tuning_curve') #2.5mW
exp5.add_session('14-12-07', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-13-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-22-22', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('14-26-42', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-29-10', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('14-32-52', 'c', 'bandwidth', 'bandwidth_am')
exp5.add_session('14-55-40', 'd', 'harmonics', 'bandwidth_am')
exp5.add_session('15-11-36', 'e', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(900, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('15-32-28', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-33-40', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('15-35-34', 'f', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-43-35', 'g', 'AM', 'am_tuning_curve')
exp5.add_session('15-47-53', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('15-50-26', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('15-54-25', 'h', 'bandwidth', 'bandwidth_am')
exp5.add_session('16-13-51', 'i', 'bandwidth', 'bandwidth_am')
exp5.add_session('16-32-31', 'j', 'harmonics', 'bandwidth_am')
exp5.add_session('16-43-51', 'k', 'harmonics', 'bandwidth_am')
exp5.add_session('16-54-53', 'l', 'noiseAmps', 'am_tuning_curve')

# exp5.add_site(950, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('17-08-30', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('17-09-41', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(975, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('17-16-41', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('17-17-52', 'm', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-26-58', 'n', 'AM', 'am_tuning_curve')
exp5.add_session('17-31-26', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('17-33-30', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('17-37-28', 'o', 'bandwidth', 'bandwidth_am')
exp5.add_session('17-56-29', 'p', 'harmonics', 'bandwidth_am')
exp5.add_session('18-08-27', 'q', 'noiseAmps', 'am_tuning_curve')

# exp5.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('18-23-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('18-28-51', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('18-32-58', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('18-34-31', 'r', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-42-34', 's', 'AM', 'am_tuning_curve')
exp5.add_session('18-46-54', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('18-49-00', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('18-54-16', 't', 'bandwidth', 'bandwidth_am')
exp5.add_session('19-12-41', 'u', 'harmonics', 'bandwidth_am')
exp5.add_session('19-26-11', 'v', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1100
