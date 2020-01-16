from jaratoolbox import celldatabase

subject = 'band027'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2017-05-03', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':0.9,
#     '1.0':1.45,
#     '1.5':2.15,
#     '2.0':2.9,
#     '2.5':4.05,
#     '3.0':5.2,
#     '3.5':6.4
# }

#nothing but spooky signals all the way down... Nick's probe sucks.

exp1 = celldatabase.Experiment(subject, '2017-05-05', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.9,
    '1.0':1.45,
    '1.5':2.05,
    '2.0':2.7,
    '2.5':3.5,
    '3.0':4.4,
    '3.5':5.3
}

# exp1.add_site(1282, tetrodes = [2,4,6,8])
# exp1.add_session('10-32-01', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1289, tetrodes = [2,4,6,8])
exp1.add_session('10-34-34', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('10-36-07', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-38-33', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-44-05', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('10-48-20', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('10-52-59', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('10-56-03', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('11-14-42', 'd', 'noiseAmps', 'am_tuning_curve')


# exp1.add_site(1526, tetrodes = [2,4,6,8])
# exp1.add_session('11-28-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1573, tetrodes = [2,4,6,8])
# exp1.add_session('11-32-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1660, tetrodes = [2,4,6,8])
# exp1.add_session('11-40-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1678, tetrodes = [2,4,6,8])
# exp1.add_session('11-43-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1769, tetrodes = [2,4,6,8])
# exp1.add_session('11-47-37', None, 'laserPulse', 'am_tuning_curve')

exp1.maxDepth = 1769


exp2 = celldatabase.Experiment(subject, '2017-05-06', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.8,
    '2.0':2.35,
    '2.5':3.1,
    '3.0':3.9,
    '3.5':4.8
}

# exp2.add_site(1265, tetrodes= [2,4,6,8])
# exp2.add_session('12-49-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1272, tetrodes = [2,4,6,8])
# exp2.add_session('12-52-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1292, tetrodes = [2,4,6,7,8])
# exp2.add_session('12-56-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1316, tetrodes = [2,3,4,6,7,8])
# exp2.add_session('12-59-05', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1367, tetrodes = [1,2,4,6,8])
exp2.add_session('13-02-55', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-04-18', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-05-51', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-12-19', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-16-33', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-18-59', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-21-06', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-39-49', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1409, tetrodes = [2,4,6,8])
# exp2.add_session('13-47-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1500, tetrodes = [2,3,4,6,8])
# exp2.add_session('13-49-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1560, tetrodes = [2,4,6,7,8])
# exp2.add_session('13-52-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1565, tetrodes = [2,4,6,8])
# exp2.add_session('13-55-04', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('13-56-10', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1580, tetrodes = [2,3,4,6,7,8])
exp2.add_session('13-58-43', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-59-59', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-01-51', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-07-51', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('14-12-04', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-14-15', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-16-44', 'g', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-36-13', 'h', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1653, tetrodes = [2,4,6,8])
# exp2.add_session('14-43-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1734, tetrodes = [2,4,6,7,8])
# exp2.add_session('14-47-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1765, tetrodes = [1,2,3,4,6,7,8])
# exp2.add_session('14-51-38', None, 'laserPulse', 'am_tuning_curve')

exp2.maxDepth = 1765


exp3 = celldatabase.Experiment(subject, '2017-05-07', 'right_AC', info=['posteriormedialDiD','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.95,
    '1.0':1.6,
    '1.5':2.3,
    '2.0':3.0,
    '2.5':3.9,
    '3.0':5.0,
    '3.5':6.3
}

# exp3.add_site(1050, tetrodes = [2,4,6,7,8])
# exp3.add_session('11-57-01', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1090, tetrodes = [1,2,3,4,6,8])
# exp3.add_session('11-59-01', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1097, tetrodes = [2,4,6,7,8])
exp3.add_session('12-00-40', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-01-39', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-03-21', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-10-15', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-14-32', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-17-42', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-19-42', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('12-38-13', 'd', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1226, tetrodes = [2,4,6,8])
# exp3.add_session('12-46-51', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1233, tetrodes = [2,4,6,7,8])
exp3.add_session('12-48-13', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-49-17', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-50-43', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-56-11', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('13-00-23', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-03-44', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-05-42', 'g', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-26-37', 'h', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1365, tetrodes = [2,4,6,8])
# exp3.add_session('13-36-38', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('13-42-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1375, tetrodes = [2,4,6,8])
# exp3.add_session('13-44-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1525, tetrodes = [2,3,4,6,8])
# exp3.add_session('13-57-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1551, tetrodes = [2,4,6,8])
# exp3.add_session('14-06-38', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1555, tetrodes = [2,3,4,6,7,8])
exp3.add_session('14-11-01', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-12-24', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-14-59', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-20-34', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('14-25-31', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-27-50', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-29-58', 'k', 'bandwidth', 'bandwidth_am')
exp3.add_session('14-48-58', 'l', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1620, tetrodes = [2,3,4,6,8])
# exp3.add_session('14-57-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1656, tetrodes = [1,2,4,6,8])
# exp3.add_session('15-00-03', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('15-02-57', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1665, tetrodes = [1,2,3,4,6,8])
exp3.add_session('15-04-33', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-06-18', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-09-35', 'm', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-15-38', 'n', 'AM', 'am_tuning_curve')
exp3.add_session('15-20-30', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-22-47', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-24-47', 'o', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-44-36', 'p', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1665


# exp4 = celldatabase.Experiment(subject, '2017-05-08', 'right_AC', info=['posteriorlateralDiI','TT1ant','sound_left'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':0.8,
#     '1.0':1.35,
#     '1.5':1.95,
#     '2.0':2.55,
#     '2.5':3.2,
#     '3.0':3.95,
#     '3.5':4.8
# }
