from jaratoolbox import celldatabase

subject = 'band031'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-06-29', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.65,
    '1.0':2.45,
    '1.5':3.5,
    '2.0':4.4,
    '2.5':5.8,
    '3.0':7.6
}

# exp0.add_site(950, tetrodes=[2,4,6,7,8])
# exp0.add_session('12-22-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1000, tetrodes=[2,4,6,7,8])
# exp0.add_session('12-45-10', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-53-05', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1020, tetrodes=[2,4,6,7,8])
exp0.add_session('12-58-56', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-00-08', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-02-46', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-08-31', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-13-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-15-49', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-21-26', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('13-39-46', 'd', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('13-51-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('14-04-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1120, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('14-08-35', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1140, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-12-50', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-14-10', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-16-01', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-21-57', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('14-26-19', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-28-26', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-31-48', 'g', 'bandwidth', 'bandwidth_am') #6kHz for TT1 and 8
exp0.add_session('14-51-54', 'h', 'bandwidth', 'bandwidth_am') #4kHz for TT4
exp0.add_session('15-10-19', 'i', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('15-21-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1220, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('15-25-50', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1240, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('15-30-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1260, tetrodes=[1,2,4,5,6,7,8])
# exp0.add_session('15-33-58', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1280, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-38-27', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-41-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-44-56', 'j', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-51-00', 'k', 'AM', 'am_tuning_curve')
exp0.add_session('15-55-59', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-58-32', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('16-01-18', 'l', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-19-47', 'm', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1280


exp1 = celldatabase.Experiment(subject, '2017-06-30', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.5,
    '1.0':2.1,
    '1.5':2.8,
    '2.0':3.55,
    '2.5':4.35,
    '3.0':5.4,
    '3.5':6.4
}

# exp1.add_site(1050, tetrodes=[2,4,6,8])
# exp1.add_session('12-50-12', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1075, tetrodes=[2,4,6,8])
# exp1.add_session('12-55-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[2,4,6,8])
# exp1.add_session('12-58-37', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1120, tetrodes=[2,4,6,8])
exp1.add_session('13-01-42', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-02-57', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-04-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-10-08', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-14-31', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-16-44', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-19-37', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('13-39-01', 'd', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1120
