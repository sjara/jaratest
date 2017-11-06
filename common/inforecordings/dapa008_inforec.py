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


