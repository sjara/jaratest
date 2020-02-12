from jaratoolbox import celldatabase

subject = 'band015'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2016-11-08','right_AC',info=['lateralDiI','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':0.95,
#     '1.0':1.8,
#     '1.5':2.5,
#     '2.0':3.75,
#     '2.5':4.7,
#     '3.0':5.8,
#     '3.5':6.7
# }

# exp0.add_site(950, tetrodes = [2])
# exp0.add_session('15-27-14', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-30-37', None, 'laserPulse', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject, '2016-11-10', 'right_AC', info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.1,
    '1.0':2.0,
    '1.5':2.9,
    '2.0':4.4,
    '2.5':5.8,
    '3.0':6.8,
    '3.5':8.2
}

# exp1.add_site(1090, tetrodes = [2])
# exp1.add_session('13-17-42', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-20-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1175, tetrodes = [2,6,8])
# exp1.add_session('13-35-16', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-37-29', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1225, tetrodes = [2,6])
exp1.add_session('13-51-34', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-54-14', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-58-01', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-10-55', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('14-18-03', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-29-13', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-31-35', None, 'laserTrain', 'am_tuning_curve')

# exp1.add_site(1275, tetrodes = [2,6])
# exp1.add_session('14-43-39', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1325, tetrodes = [2,6])
exp1.add_session('14-49-30', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-51-42', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-54-14', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-04-53', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('15-12-03', 'f', 'bandwidth', 'bandwidth_am')
exp1.add_session('15-23-05', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-25-53', None, 'laserTrain', 'am_tuning_curve')

exp1.add_site(1400, tetrodes = [2,6,8])
exp1.add_session('15-40-21', None, 'noisebursts' ,'am_tuning_curve')
exp1.add_session('15-42-29', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-45-44', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-57-01', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('16-03-07', 'i', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-13-10', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-17-36', None, 'laserTrain', 'am_tuning_curve')

# exp1.add_site(1450, tetrodes = [2,6,8])
# exp1.add_session('16-28-33', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('16-30-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1500, tetrodes = [1,2,4,5,6,8])
# exp1.add_session('16-52-54', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('16-55-03', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1510, tetrodes = [1,2,4,5,6,7,8])
exp1.add_session('16-59-39', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('17-00-51', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('17-04-51', 'j', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-15-33', 'k', 'AM', 'am_tuning_curve')
exp1.add_session('17-21-38', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('17-24-15', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('17-27-13', 'l', 'bandwidth', 'bandwidth_am')

exp1.maxDepth = 1510


exp2 = celldatabase.Experiment(subject, '2016-11-11', 'left_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.75,
    '1.0':1.2,
    '1.5':1.7,
    '2.0':2.25,
    '2.5':2.85,
    '3.0':3.65,
    '3.5':4.4
}

# exp2.add_site(875, tetrodes = [2,4,6,8])
# exp2.add_session('12-49-57', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-52-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(900, tetrodes = [2,4,6,8])
# exp2.add_session('12-59-28', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-01-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(925, tetrodes = [2,6,8])
# exp2.add_session('13-06-27', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(950, tetrodes = [1,2,4,6,7,8])
exp2.add_session('13-15-46', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-18-06', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-23-23', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-34-17', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-41-15', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-45-54', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-48-01', 'c', 'bandwidth', 'bandwidth_am')

exp2.add_site(1000, tetrodes = [1,2,3,4,6,7,8])
exp2.add_session('14-06-01', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-08-11', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-11-30', 'd', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-22-31', 'e', 'AM', 'am_tuning_curve')
exp2.add_session('14-29-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-31-50', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-34-08', 'e', 'bandwidth', 'bandwidth_am')

exp2.add_site(1026, tetrodes = [1,2,4,6,7,8])
exp2.add_session('14-47-21', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-50-27', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-53-28', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-06-08', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('15-12-02', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-14-23', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-17-22', 'h', 'bandwidth', 'bandwidth_am')

exp2.add_site(1100, tetrodes = [1,2,4,5,6,7,8])
exp2.add_session('15-34-00', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-37-21', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-40-11', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-42-49', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-53-29', 'j', 'AM', 'am_tuning_curve')
exp2.add_session('15-58-16', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-00-45', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-03-53', 'k', 'bandwidth', 'bandwidth_am')

exp2.maxDepth = 1100

exp3 = celldatabase.Experiment(subject, '2016-11-12', 'left_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.7,
    '1.0':1.1,
    '1.5':1.5,
    '2.0':2.05,
    '2.5':2.55,
    '3.0':3.2,
    '3.5':4.0
}

exp3.add_site(950, tetrodes = [2,4,6,8])
exp3.add_session('10-57-51', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('10-59-57', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('11-03-27', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('11-14-05', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('11-19-15', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('11-21-33', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('11-23-40', 'c', 'bandwidth', 'bandwidth_am')

exp3.add_site(1000, tetrodes = [1,2,4,6,7,8])
exp3.add_session('11-50-46', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-53-01', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('11-56-50', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-12-40', 'e', 'AM', 'am_tuning_curve')
exp3.add_session('12-19-00', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-21-23', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-23-23', 'f', 'bandwidth', 'bandwidth_am')

exp3.add_site(1100, tetrodes = [1,2,3,4,6,7,8])
exp3.add_session('12-43-09', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-46-05', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-52-37', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-03-28', 'h', 'AM', 'am_tuning_curve')
exp3.add_session('13-09-33', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-11-53', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-14-28', 'i', 'bandwidth', 'bandwidth_am')

exp3.add_site(1150, tetrodes = [1,2,3,4,6,7,8])
exp3.add_session('13-30-38', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-34-02', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-36-06', 'j', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-47-18', 'k', 'AM', 'am_tuning_curve')
exp3.add_session('13-53-27', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-56-27', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-58-43', 'l', 'bandwidth', 'bandwidth_am')

# exp3.add_site(1200, tetrodes = [1,2,3,4,6,7,8])
# exp3.add_session('14-13-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes = [1,2,3,4,6,7,8])
# exp3.add_session('14-21-33', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1275, tetrodes = [1,2,3,4,6,7,8])
exp3.add_session('14-28-13', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-30-58', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-33-29', 'm', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-45-19', 'n', 'AM', 'am_tuning_curve')
exp3.add_session('14-56-16', 'o', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-05-53', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-07-50', None, 'laserTrain', 'am_tuning_curve')

exp3.maxDepth = 1275


exp4 = celldatabase.Experiment(subject, '2016-11-13', 'left_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':0.7,
    '1.0':1.1,
    '1.5':1.55,
    '2.0':2.05,
    '2.5':2.55,
    '3.0':3.3,
    '3.5':4.05
}

# exp4.add_site(875, tetrodes = [2])
# exp4.add_session('12-21-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(900, tetrodes = [2,4])
# exp4.add_session('12-26-32', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-30-17', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-32-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(910, tetrodes = [2,4])
# exp4.add_session('12-35-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(930, tetrodes = [2,4,6])
# exp4.add_session('12-40-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(980, tetrodes = [2,4])
# exp4.add_session('12-48-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(995, tetrodes = [2,4,6])
# exp4.add_session('12-52-12', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-54-49', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1025, tetrodes = [1,2,4,6])
exp4.add_session('13-00-55', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-03-20', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-06-04', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-16-48', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('13-22-34', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-24-45', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('13-26-51', 'c', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1075, tetrodes = [1,2,4,6,8])
# exp4.add_session('13-39-36', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('13-42-48', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1080, tetrodes = [1,2,3,4,6,8])
exp4.add_session('13-46-16', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-48-54', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-50-30', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-01-08', 'e', 'AM', 'am_tuning_curve')
exp4.add_session('14-05-48', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-08-34', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-11-07', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-13-51', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('14-16-42', 'f', 'bandwidth', 'bandwidth_am')

exp4.add_site(1150, tetrodes = [1,2,3,4,5,6,8])
exp4.add_session('14-30-28', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-33-01', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-34-56', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-45-29', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('14-51-01', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-54-57', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('14-57-30', 'i', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1225, tetrodes = [1,2,3,4,5,6,8])
# exp4.add_session('15-15-59', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1260, tetrodes = [1,2,3,4,6,7,8])
exp4.add_session('15-20-51', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-23-24', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-27-08', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-29-53', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-31-46', 'j', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-44-03', 'k', 'AM', 'am_tuning_curve')
exp4.add_session('15-49-06', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-51-12', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('15-53-37', 'l', 'bandwidth', 'bandwidth_am')

exp4.maxDepth = 1260
