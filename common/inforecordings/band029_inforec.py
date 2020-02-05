from jaratoolbox import celldatabase

subject = 'band029'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-05-22', 'right_AC', info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.85,
    '1.0':1.45,
    '1.5':2.1,
    '2.0':3.0,
    '2.5':4.1,
    '3.0':5.3,
    '3.5':6.1
}

# exp0.add_site(1140, tetrodes = [1,2,4,6,7,8])
# exp0.add_session('11-47-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1160, tetrodes = [1,2,4,6,8])
# exp0.add_session('11-52-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1180, tetrodes = [1,2,4,6,8])
# exp0.add_session('11-57-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes = [2,4,6,8])
# exp0.add_session('12-00-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1220, tetrodes = [1,2,4,6,7,8])
# exp0.add_session('12-04-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1240, tetrodes = [1,2,3,4,6,7,8])
# exp0.add_session('12-08-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1260, tetrodes = [1,2,3,4,6,7,8])
# exp0.add_session('12-14-42', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-15-56', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1280, tetrodes = [1,2,4,6,8])
# exp0.add_session('12-21-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1300, tetrodes = [1,2,3,4,6,8])
# exp0.add_session('12-26-32', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1320, tetrodes = [1,2,3,4,6,7,8])
exp0.add_session('12-30-27', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-31-37', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-33-31', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-39-31', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('12-43-41', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-45-46', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('12-47-43', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('13-06-05', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1320


# exp1 = celldatabase.Experiment(subject, '2017-05-24', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
# experiments.append(exp1)
#
# exp1.laserCalibration = {
#     '0.5':0.85,
#     '1.0':1.3,
#     '1.5':1.85,
#     '2.0':2.3,
#     '2.5':3.3,
#     '3.0':4.2,
#     '3.5':4.9
# }

# exp1.add_site(1500, tetrodes = [2,4,6,7,8])
# exp1.add_session('12-18-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1520, tetrodes = [2,4,8])
# exp1.add_session('12-32-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1540, tetrodes = [2,4,8])
# exp1.add_session('12-39-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1580, tetrodes = [2,4,8])
# exp1.add_session('12-49-01', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1600, tetrodes = [2,4])
# exp1.add_session('12-58-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1620, tetrodes = [2,4,6])
# exp1.add_session('13-06-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1640, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-18-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1660, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-27-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1680, tetrodes = [1,2,4,6,8])
# exp1.add_session('13-36-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1700, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-45-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1710, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-49-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1720, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-52-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1725, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-55-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1730, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('13-59-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1715, tetrodes = [1,2,3,4,6,7,8])
# exp1.add_session('14-01-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1735, tetrodes = [1,2,3,4])
# exp1.add_session('14-03-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1740, tetrodes = [1,2,3,4,6,7,8])
# exp1.add_session('14-08-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1732, tetrodes = [1,2,3,4])
# exp1.add_session('14-12-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1727, tetrodes = [1,2,4])
# exp1.add_session('14-16-08', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1716, tetrodes = [1,2,4,8])
# exp1.add_session('14-17-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1712, tetrodes = [1,2,3,4])
# exp1.add_session('14-18-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1750, tetrodes = [1,2,3,4])
# exp1.add_session('14-22-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1760, tetrodes = [1,2,4])
# exp1.add_session('14-27-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1770, tetrodes = [1,2,3,4])
# exp1.add_session('14-30-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1755, tetrodes = [1,2,4])
# exp1.add_session('14-32-50', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('14-34-30', None, 'laserPulse', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-05-25', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.9,
    '2.0':2.45,
    '2.5':3.1,
    '3.0':4.0,
    '3.5':4.8
}

# exp2.add_site(1120, tetrodes = [1,2,4,6,8])
# exp2.add_session('12-44-48', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1130, tetrodes = [1,2,3,4,6,7,8])
exp2.add_session('12-49-38', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-50-55', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-52-50', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-58-26', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-02-48', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-05-30', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-07-56', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-27-20', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1180, tetrodes = [1,2,3,4,6,8])
# exp2.add_session('13-39-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes = [1,2,3,4,6,8])
# exp2.add_session('13-44-11', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('13-45-29', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1220, tetrodes = [1,2,3,4,6,8])
# exp2.add_session('13-51-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1230, tetrodes = [2,3,4,6,8])
# exp2.add_session('13-56-00', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1240, tetrodes = [2,3,4,6,8])
exp2.add_session('14-00-07', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-01-13', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-02-47', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-09-05', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('14-13-17', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-15-48', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-18-16', 'g', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-38-05', 'h', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1300, tetrodes = [2,3,4,6,8])
# exp2.add_session('14-50-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1320, tetrodes = [2,3,4,6,8])
# exp2.add_session('14-56-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1340, tetrodes = [3,4,6])
# exp2.add_session('15-01-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1360, tetrodes = [2,3,4,6])
# exp2.add_session('15-07-52', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1400, tetrodes = [1,2,3,4,6,7,8])
# exp2.add_session('15-13-40', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1420, tetrodes = [1,2,3,4,6,7,8])
exp2.add_session('15-18-40', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-20-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-22-56', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-29-32', 'j', 'AM', 'am_tuning_curve')
exp2.add_session('15-34-02', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-36-08', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-38-25', 'k', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-59-40', 'l', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1420


exp3 = celldatabase.Experiment(subject, '2017-05-26', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.85,
    '1.0':1.6,
    '1.5':2.2,
    '2.0':3.55,
    '2.5':4.75,
    '3.0':5.95,
    '3.5':6.8
}

# exp3.add_site(980, tetrodes = [1,2,4,6,8])
# exp3.add_session('11-58-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes = [1,2,4,6,8])
# exp3.add_session('12-03-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(990, tetrodes = [1,2,3,4,6,8])
# exp3.add_session('12-07-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1020, tetrodes = [2,4,6,8])
# exp3.add_session('12-11-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1040, tetrodes = [1,2,4,6,8])
# exp3.add_session('12-17-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes = [2,4,6,8])
# exp3.add_session('12-20-57', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1060, tetrodes = [1,2,4,6,8])
exp3.add_session('12-25-10', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-26-31', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-28-37', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-34-51', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-39-42', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-41-46', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-44-06', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-03-42', 'd', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1120, tetrodes = [3,4,6,8])
# exp3.add_session('13-14-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1130, tetrodes = [2,4,6,8])
# exp3.add_session('13-18-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1110, tetrodes = [1,2,4,6,8])
# exp3.add_session('13-23-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes = [2,4,6,8])
# exp3.add_session('13-29-11', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1090, tetrodes = [2,4,6,8])
exp3.add_session('13-34-05', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-35-08', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-36-28', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-42-09', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('13-46-26', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-48-30', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-50-19', 'g', 'bandwidth', 'bandwidth_am')
exp3.add_session('14-09-40', 'h', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1200, tetrodes = [2,4,6,7,8])
# exp3.add_session('14-21-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1220, tetrodes = [2,3,4,6,7,8])
# exp3.add_session('14-26-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1230, tetrodes = [2,3,4,6,7,8])
# exp3.add_session('14-33-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1215, tetrodes = [2,3,4,6,7,8])
# exp3.add_session('14-40-57', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1225, tetrodes = [2,3,4,6,7,8])
exp3.add_session('14-45-27', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-46-36', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-48-08', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-53-35', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('14-57-54', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-00-21', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-02-56', 'k', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-21-25', 'l', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1225


# exp4 = celldatabase.Experiment(subject, '2017-05-28', 'right_AC', info=['posteriourmiddleDiD','TT1ant','sound_left'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':0.95,
#     '1.0':1.55,
#     '1.5':2.25,
#     '2.0':3.0,
#     '2.5':4.0,
#     '3.0':4.85,
#     '3.5':6.0
# }
