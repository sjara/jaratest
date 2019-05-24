from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band042'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-12-07', 'left_AC', info=['medialDiI','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.7,
    '2.5':3.3,
    '3.0':3.85,
    '3.5':4.4
}

exp0.add_site(700, tetrodes=[2,4,6,8])
exp0.add_session('12-21-45', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(725, tetrodes=[6,8])
exp0.add_session('12-37-27', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(775, tetrodes=[4,6,8])
exp0.add_session('12-48-54', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-50-18', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[5,6,8])
exp0.add_session('13-33-09', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[8])
exp0.add_session('13-55-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-56-23', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[5,6,7,8])
exp0.add_session('14-04-13', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-05-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-20-02', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-26-58', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-30-03', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-33-33', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('15-00-02', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('15-15-27', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1350, tetrodes=[7,8])
exp0.add_session('16-14-40', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[7,8])
exp0.add_session('16-19-30', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1425, tetrodes=[7,8])
exp0.add_session('16-26-59', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1450, tetrodes=[7,8])
exp0.add_session('16-47-00', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1475, tetrodes=[7,8])
exp0.add_session('16-55-08', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1500, tetrodes=[7,8])
exp0.add_session('17-01-06', None, 'laserPulse', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-12-08', 'left_AC', info=['middleDiD','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.3,
    '2.0':2.85,
    '2.5':3.45,
    '3.0':4.1,
    '3.5':4.9
}
