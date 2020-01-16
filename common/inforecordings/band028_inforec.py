from jaratoolbox import celldatabase

subject = 'band028'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-05-18', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.85,
    '1.0':1.45,
    '1.5':2.1,
    '2.0':2.75,
    '2.5':3.55,
    '3.0':4.8,
    '3.5':5.5
}

exp0.add_site(1258, tetrodes = [2,4,6,8])
exp0.add_session('11-22-47', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-24-34', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-30-09', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('11-34-37', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('11-36-41', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('11-39-49', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('11-59-11', 'd', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1411, tetrodes = [2,4,5,6,8])
# exp0.add_session('12-14-52', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1504, tetrodes = [1,2,4,5,6,8])
# exp0.add_session('12-18-30', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1550, tetrodes = [1,2,3,4,5,6,8])
exp0.add_session('12-21-44', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-22-52', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-24-49', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-30-15', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('12-34-51', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-37-03', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('12-40-44', 'g', 'bandwidth', 'bandwidth_am')
exp0.add_session('12-59-13', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1550

#
# exp1 = celldatabase.Experiment(subject, '2017-05-19', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
# experiments.append(exp1)
#
# exp1.laserCalibration = {
#     '0.5':0.75,
#     '1.0':1.2,
#     '1.5':1.65,
#     '2.0':2.15,
#     '2.5':2.7,
#     '3.0':3.3,
#     '3.5':4.15
# }

# exp1.add_site(1791, tetrodes = [1,4,5,6,7])
# exp1.add_session('15-06-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1782, tetrodes = [1,4,5,6,7])
# exp1.add_session('15-09-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1561, tetrodes = [2,4,5,6,7])
# exp1.add_session('15-20-29', None, 'laserPulse', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-05-20', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.85,
    '1.0':1.35,
    '1.5':1.9,
    '2.0':2.5,
    '2.5':3.1,
    '3.0':4.0,
    '3.5':4.75
}

# exp2.add_site(1141, tetrodes = [2,4])
# exp2.add_session('14-09-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1180, tetrodes = [2,4,6])
# exp2.add_session('14-11-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes = [2,4])
# exp2.add_session('14-12-48', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1210, tetrodes = [2,4])
# exp2.add_session('14-14-20', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1220, tetrodes = [2,4,8])
# exp2.add_session('14-15-53', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('14-28-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1250, tetrodes = [2,4,8])
# exp2.add_session('14-30-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1275, tetrodes = [2,4,8])
# exp2.add_session('14-32-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1300, tetrodes = [2,4,8])
# exp2.add_session('14-33-44', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('14-35-20', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-37-09', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('14-44-58', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1325, tetrodes = [1,2,3,4,6,7,8])
exp2.add_session('14-47-25', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-48-36', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-49-52', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-55-46', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('15-01-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-03-50', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-06-15', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-24-40', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1350, tetrodes = [1,2,4,6,7,8])
# exp2.add_session('15-30-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1375, tetrodes = [4,6])
# exp2.add_session('15-31-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1400, tetrodes = [2,3,4,6,8])
# exp2.add_session('15-39-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1425, tetrodes = [2,4,6,8])
# exp2.add_session('15-41-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1450, tetrodes = [1,2,3,4,6,8])
# exp2.add_session('15-54-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1475, tetrodes = [1,2,3,4,6,8])
# exp2.add_session('15-56-05', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('15-57-20', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-59-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1500, tetrodes = [1,2,3,4,8])
# exp2.add_session('16-08-48', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('16-10-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1525, tetrodes = [2,4,8])
# exp2.add_session('16-26-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1550, tetrodes = [2,4,8])
# exp2.add_session('16-28-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1575, tetrodes = [1,2,3,4,8])
# exp2.add_session('16-37-23', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1541, tetrodes = [1,2,3,4,8])
exp2.add_session('16-39-33', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-40-50', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-42-30', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-47-59', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('16-52-10', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-54-16', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-57-28', 'g', 'bandwidth', 'bandwidth_am')
exp2.add_session('17-16-22', 'h', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1541


exp3 = celldatabase.Experiment(subject, '2017-05-21', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.9,
    '2.0':2.5,
    '2.5':3.1,
    '3.0':3.95,
    '3.5':4.8
}

# exp3.add_site(1425, tetrodes = [2,4,6,8])
# exp3.add_session('15-05-24', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('15-07-01', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1450, tetrodes = [2,4,6,8])
exp3.add_session('15-09-10', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-10-25', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-12-19', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-18-36', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('15-22-49', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-24-56', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-27-43', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-51-23', 'd', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1500, tetrodes = [1,2,4,6,8])
# exp3.add_session('15-57-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1525, tetrodes = [2,4,6,8])
# exp3.add_session('16-11-29', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1550, tetrodes = [2,4,6,8])
# exp3.add_session('16-18-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1575, tetrodes = [2,4,6,8])
# exp3.add_session('16-28-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1600, tetrodes = [2,3,4,6,8])
# exp3.add_session('16-38-12', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1625, tetrodes = [2,3,4,6,8])
exp3.add_session('16-44-53', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-46-15', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-47-46', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-53-21', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('16-57-35', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-59-40', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('17-02-38', 'g', 'bandwidth', 'bandwidth_am')
exp3.add_session('17-22-29', 'h', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1625
