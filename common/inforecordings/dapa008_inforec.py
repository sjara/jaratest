from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa008'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-11-05', 'left_AudStr', info='AnteriorfacingPosteriorDiI')
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.75,
    '1.0':1.1,
    '1.5':1.5,
    '2.0':1.9,
    '2.5':2.3,
    '3.0':2.75,
    '3.5':3.25,
    '4.0':3.9
}

exp0.add_site(2000, tetrodes=[7,8])
exp0.add_session('17-26-05', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2050, tetrodes=[7,8])
exp0.add_session('17-40-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-42-49', 'a', 'tuningCurve', 'am_tuning_curve') #forgot to save behavior

exp0.add_site(2100, tetrodes=[7,8])
exp0.add_session('18-12-41', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-15-39', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2150, tetrodes=[7,8])
exp0.add_session('18-49-17', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-51-58', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2300, tetrodes=[7,8])
exp0.add_session('19-36-38', None, 'noisebursts', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-11-08', 'left_AudStr', info='MedialfacingPosteriorDiD')
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.75,
    '2.5':3.15,
    '3.0':3.8,
    '3.5':4.5,
    '4.0':5.3
}

exp1.add_site(2000, tetrodes=[7,8])
exp1.add_session('13-16-47', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2100, tetrodes=[7,8])
exp1.add_session('13-24-34', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2150, tetrodes=[7,8])
exp1.add_session('13-30-37', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2200, tetrodes=[7,8])
exp1.add_session('13-39-50', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2250, tetrodes=[7,8])
exp1.add_session('13-45-08', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-47-55', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2300, tetrodes=[7,8])
exp1.add_session('14-18-18', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-20-59', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2350, tetrodes=[7,8])
exp1.add_session('14-52-37', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-54-50', 'c', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2400, tetrodes=[7,8])
exp1.add_session('15-25-21', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-27-34', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')
