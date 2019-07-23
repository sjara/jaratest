from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa007'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-10-05', 'left_AudStr', info='AnteriorfacingPosteriorDiI')
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.6,
    '1.0':2.3,
    '1.5':3.05,
    '2.0':3.5,
    '2.5':4.5,
    '3.0':5.4,
    '3.5':6.3
}

#Set thresholds to 55 mV due to noise
exp0.add_site(2000, tetrodes=[1,2,5,6,7,8])
exp0.add_session('17-36-45', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-39-40', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2050, tetrodes=[1,2,5,6,7,8])
exp0.add_session('18-13-39', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-16-31', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2100, tetrodes=[1,2,5,6,7,8])
exp0.add_session('18-48-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-50-52', 'c', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2150, tetrodes=[1,2,5,6,7,8])
exp0.add_session('19-25-16', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2200, tetrodes=[1,2,5,6,7,8])
exp0.add_session('19-31-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('19-34-14', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2250, tetrodes=[1,2,5,6,7,8])
exp0.add_session('20-05-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('20-07-40', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2300, tetrodes=[1,2,5,6,7,8])
exp0.add_session('20-39-32', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('20-42-00', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2350, tetrodes=[1,2,5,6,7,8])
exp0.add_session('21-14-38', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2400, tetrodes=[1,2,5,6,7,8])
exp0.add_session('21-17-35', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('21-20-19', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2450, tetrodes=[1,2,5,6,7,8])
exp0.add_session('21-53-06', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('21-55-28', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2500, tetrodes=[1,2,5,6,7,8])
exp0.add_session('22-26-45', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[1,2,5,6,7,8])
exp0.add_session('22-29-45', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('22-31-59', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-10-25', 'right_AudStr', info='MedialfacingPosteriorDiD')
experiments.append(exp1)

exp1.add_site(2000, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('17-59-45', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2050, tetrodes=[2])
exp1.add_session('18-10-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('18-31-46', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2100, tetrodes=[2])
exp1.add_session('18-50-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('18-53-13', 'b', 'tuningCurve', 'am_tuning_curve')


