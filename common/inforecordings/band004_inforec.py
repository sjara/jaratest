from jaratoolbox import celldatabase




subject = 'band004'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2016-08-29', 'right_AC', info=['centerDiO','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.8,
    '1.0':1.1,
    '1.5':1.4,
    '2.0':2.0,
    '2.5':2.5,
    '3.0':3.05,
    '3.5':3.85
}
# exp0.add_site(673, tetrodes=[2,4])
# exp0.add_session('12-24-09', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(678, tetrodes=[1,2,4])
# exp0.add_session('12-35-11', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-37-03', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-40-41', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-44-49', None, 'laserTrain', 'am_tuning_curve')
#
# exp0.add_site(686, tetrodes=[1,2,4])
# exp0.add_session('12-51-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(725, tetrodes=[1,2,4])
# exp0.add_session('12-56-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(759, tetrodes=[1,2,4,6])
# exp0.add_session('13-04-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(828, tetrodes=[1,2,4,6])
# exp0.add_session('13-09-38', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('13-12-23', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('13-15-55', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-18-37', None, 'laserPulse2.5', 'am_tuning_curve')
# exp0.add_session('13-22-03', None, 'longLaserPulse2.5', 'am_tuning_curve')

exp0.add_site(832, tetrodes = [1,2,4,6])
exp0.add_session('13-27-15', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
exp0.add_session('13-29-46', None, 'longLaserPulse', 'am_tuning_curve')
exp0.add_session('13-31-54', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-34-14', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-46-06', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-53-50', 'c', 'bandwidth', 'bandwidth_am')

exp0.add_site(884, tetrodes = [1,2,3,4,6])
exp0.add_session('14-15-29', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-18-16', None, 'longLaserPulse', 'am_tuning_curve')
exp0.add_session('14-20-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-22-28', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-33-05', 'e', 'AM', 'am_tuning_curve')
exp0.add_session('14-40-13', 'f', 'bandwidth', 'bandwidth_am')

exp0.add_site(950, tetrodes = [1,2,3,4,6])
exp0.add_session('15-02-18', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-05-07', None, 'longLaserPulse', 'am_tuning_curve')
exp0.add_session('15-07-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-09-13', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-20-00', 'h', 'AM', 'am_tuning_curve')
exp0.add_session('15-26-48', 'i', 'bandwidth', 'bandwidth_am')

exp0.maxDepth = 950


exp1 = celldatabase.Experiment(subject, '2016-08-30', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.85,
    '1.0':1.35,
    '1.5':1.7,
    '2.0':2.4,
    '2.5':3.1,
    '3.0':3.9,
    '3.5':4.6
}

# exp1.add_site(981, tetrodes=[2,4,6])
# exp1.add_session('11-57-33', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('12-00-51', None, 'longLaserPulse', 'am_tuning_curve')

exp1.add_site(992, tetrodes=[2,4,6])
exp1.add_session('12-04-33', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-07-59', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-10-23', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-21-39', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-29-08', 'c', 'bandwidth', 'bandwidth_am')

exp1.add_site(1030, tetrodes = [2,4,6])
exp1.add_session('12-52-02', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-55-28', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-57-53', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-13-27', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('13-20-15', 'f', 'bandwidth', 'bandwidth_am')
exp1.add_session('13-43-59', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-47-25', None, 'laserTrain', 'am_tuning_curve')

# exp1.add_site(1091, tetrodes=[1,2,3,4,6])
# exp1.add_session('13-54-58', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('13-57-50', None, 'laserTrain', 'am_tuning_curve')

exp1.add_site(1092, tetrodes=[1,2,3,4,6])
exp1.add_session('13-59-33', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-01-58', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('14-05-57', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-09-01', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-19-53', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('14-26-48', 'i', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-50-09', None, 'laserPulse', 'am_tuning_curve')

# exp1.add_site(1150, tetrodes=[1,2,3,4,6])
# exp1.add_session('15-01-06', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,4,5,6])
exp1.add_session('15-14-13', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-17-42', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('15-22-05', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-26-21', 'j', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-36-56', 'k', 'AM', 'am_tuning_curve')
exp1.add_session('15-47-01', 'l', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-05-26', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-10-21', 'm', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-31-43', None, 'laserPulse', 'am_tuning_curve')

exp1.maxDepth = 1200


exp2 = celldatabase.Experiment(subject, '2016-08-31', 'right_AC', info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.65,
    '1.0':1.05,
    '1.5':1.45,
    '2.0':1.9,
    '2.5':2.35,
    '3.0':2.9,
    '3.5':3.5
}

# exp2.add_site(890, tetrodes=[2,4,6])
# exp2.add_session('11-54-56', None, 'laserPulse2.5', 'am_tuning_curve')
# exp2.add_session('11-57-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(910, tetrodes=[2,4,6])
# exp2.add_session('12-03-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(950, tetrodes=[2,4,6])
# exp2.add_session('12-11-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(979, tetrodes=[2,4,6])
# exp2.add_session('12-21-06', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('12-24-11', None, 'laserTrain', 'am_tuning_curve')

exp2.add_site(980, tetrodes=[1,2,4,6])
exp2.add_session('12-35-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-37-14', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-39-57', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('12-43-56', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-55-12', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-02-22', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-20-41', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1075, tetrodes=[1,2,3,4,6])
exp2.add_session('13-35-22', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-38-21', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-42-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-45-17', 'd', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-56-17', 'e', 'AM', 'am_tuning_curve')
exp2.add_session('14-03-09', 'f', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-28-42', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-31-04', None, 'laserTrain', 'am_tuning_curve')

# exp2.add_site(1125, tetrodes=[1,2,3,4,6])
# exp2.add_session('15-03-31', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1175, tetrodes=[1,2,3,4,6])
exp2.add_session('15-12-46', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-15-39', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-19-12', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-21-02', 'g', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-34-55', 'h', 'AM', 'am_tuning_curve')
exp2.add_session('15-44-06', 'i', 'bandwidth', 'bandwidth_am')
exp2.add_session('16-02-47', None, 'laserPulse', 'am_tuning_curve')

exp2.maxDepth = 1175


exp3 = celldatabase.Experiment(subject, '2016-09-09', 'left_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.7,
    '1.0':1.05,
    '1.5':1.4,
    '2.0':1.85,
    '2.5':2.3,
    '3.0':2.8,
    '3.5':3.45
}

# exp3.add_site(1000, tetrodes = [2,3,4,5,6])
# exp3.add_session('12-13-45', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('12-15-46', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1050, tetrodes = [2,3,4,5,6])
exp3.add_session('12-21-44', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-24-22', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-26-44', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-28-54', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-31-18', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-46-07', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-52-18', 'c', 'bandwidth', 'bandwidth_am')

exp3.add_site(1051, tetrodes = [2,3,4,5,6])
exp3.add_session('13-11-00', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-14-24', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-17-03', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-19-18', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-30-44', 'e', 'AM', 'am_tuning_curve')
exp3.add_session('13-36-54', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-40-30', 'f', 'bandwidth', 'bandwidth_am')

# exp3.add_site(1150, tetrodes = [1,2,3,4,6])
# exp3.add_session('14-10-45', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-13-42', None, 'laserTrain', 'am_tuning_curve')

exp3.add_site(1220, tetrodes = [1,3,4,6])
exp3.add_session('14-22-39', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-24-51', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-27-09', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-30-16', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-40-55', 'h', 'AM', 'am_tuning_curve')
exp3.add_session('14-47-05', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-50-18', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-52-40', 'i', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-15-06', 'j', 'bandwidth', 'bandwidth_am')

exp3.maxDepth = 1220


exp4 = celldatabase.Experiment(subject, '2016-09-11', 'left_AC', info=['medialDiO','TT1ant','sound_left'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':0.7,
    '1.0':1.15,
    '1.5':1.6,
    '2.0':2.1,
    '2.5':2.6,
    '3.0':3.4,
    '3.5':4.0
}
# exp4.add_site(1066, tetrodes = [1,2,3,4,6])
# exp4.add_session('12-18-25', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-21-51', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1080, tetrodes = [1,2,3,4,6])
exp4.add_session('12-26-35', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-30-03', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-33-22', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-44-55', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('12-49-56', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-52-30', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('12-58-44', 'c', 'bandwidth', 'bandwidth_am')
exp4.add_session('13-18-11', 'd', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1200, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('13-47-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1250, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('13-55-32', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1300, tetrodes = [1,2,3,4,5,6])
exp4.add_session('14-03-20', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-07-04', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-09-27', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-20-05', 'f', 'AM', 'am_tuning_curve')
exp4.add_session('14-25-03', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-27-59', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('14-32-30', 'g', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1350, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('14-57-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1400, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('15-05-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1450, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('15-13-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1550, tetrodes = [1,2,3,4,5,6])
# exp4.add_session('15-21-41', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1575, tetrodes = [1,2,3,4,5,6])
exp4.add_session('15-25-56', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-28-17', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-30-35', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-41-49', 'i', 'AM', 'am_tuning_curve')
exp4.add_session('15-47-06', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-49-33', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('15-52-41', 'j', 'bandwidth', 'bandwidth_am')

exp4.maxDepth = 1575
