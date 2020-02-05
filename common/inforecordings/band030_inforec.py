from jaratoolbox import celldatabase

subject = 'band030'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-06-05', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.85,
    '2.0':2.4,
    '2.5':3.1,
    '3.0':3.9,
    '3.5':4.7
}

# exp0.add_site(1250, tetrodes = [4])
# exp0.add_session('11-02-54', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('11-04-38', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1260, tetrodes = [4])
# exp0.add_session('11-06-58', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('11-08-30', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('11-10-06', 'a', 'tuningCurve', 'am_tuning_curve')
#
# exp0.add_site(1350,  tetrodes = [2,4,6,7,8])
# exp0.add_session('11-29-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1400, tetrodes = [1,2,4,7,8])
# exp0.add_session('11-46-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1420, tetrodes = [2,4,6,7,8])
# exp0.add_session('11-53-34', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1440, tetrodes = [1,2,4,6,7,8])
exp0.add_session('12-02-18', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-03-27', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-05-05', 'b', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-13-03', 'c', 'AM', 'am_tuning_curve')
exp0.add_session('12-19-31', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-21-36', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('12-24-30', 'd', 'bandwidth', 'bandwidth_am')
exp0.add_session('12-44-15', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1440


exp1 = celldatabase.Experiment(subject, '2017-06-07', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.9,
    '1.0':1.55,
    '1.5':2.2,
    '2.0':3.0,
    '2.5':4.0,
    '3.0':5.0,
    '3.5':6.3
}

# exp1.add_site(1000, tetrodes = [2,3,4])
# exp1.add_session('10-26-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1050, tetrodes = [2,3,4])
# exp1.add_session('10-36-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1075, tetrodes = [2,3,4,8])
# exp1.add_session('10-42-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes = [2,3,4])
# exp1.add_session('10-46-33', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1120, tetrodes = [2,3,4,8])
exp1.add_session('10-49-20', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('10-50-30', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-52-33', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-57-58', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('11-02-10', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('11-04-26', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('11-07-34', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('11-34-25', 'd', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1160, tetrodes = [2,3,4])
# exp1.add_session('11-43-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1180, tetrodes = [1,2,3,4,8])
# exp1.add_session('11-48-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1200, tetrodes = [1,2,3,4,6,8])
# exp1.add_session('11-50-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1210, tetrodes = [1,2,3,4])
# exp1.add_session('11-54-41', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('11-55-44', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1220, tetrodes = [1,2,3,4,8])
# exp1.add_session('12-00-50', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1240, tetrodes = [1,2,3,4,8])
exp1.add_session('12-05-28', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-06-30', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-08-08', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-14-06', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('12-18-19', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-20-51', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-23-25', 'g', 'bandwidth', 'bandwidth_am')
exp1.add_session('12-41-51', 'h', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1240


exp2 = celldatabase.Experiment(subject, '2017-06-23', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.9,
    '1.0':3.0,
    '1.5':4.65,
    '2.0':7.0
}

exp2.add_site(900, tetrodes=[1,2,3,4,6,8])
exp2.add_session('13-56-25', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-00-26', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-03-06', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-08-43', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-13-04', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-15-58', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-19-15', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-40-36', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(950, tetrodes=[1,2,3,4,6,8])
# exp2.add_session('14-51-05', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(975, tetrodes=[1,2,3,4,6,8])
exp2.add_session('14-59-03', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-00-16', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-01-53', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-07-35', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('15-11-55', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-14-05', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-19-59', 'g', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-38-41', 'h', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1050, tetrodes=[1,2,3,4,6,8])
# exp2.add_session('15-46-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1075, tetrodes=[1,2,3,4,6,8])
# exp2.add_session('15-53-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1100, tetrodes=[1,2,3,4,6,8])
# exp2.add_session('15-59-05', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1125, tetrodes=[1,2,3,4,6,8])
exp2.add_session('16-04-06', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-05-19', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-07-15', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-12-53', 'j', 'AM', 'am_tuning_curve')
exp2.add_session('16-18-30', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-20-43', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-27-50', 'k', 'bandwidth', 'bandwidth_am')
exp2.add_session('16-48-34', 'l', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1125


# exp3 = celldatabase.Experiment(subject, '2017-06-26', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
# experiments.append(exp3)
#
# exp3.laserCalibration = {
#     '0.5':2.6,
#     '1.0':4.7,
#     '1.5':7.9
# }
