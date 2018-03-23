from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band056'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-03-22', 'left_AC', info=['lateralDiO','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.35,
    '4.0':4.9,
    '5.0':5.45,
    '7.5':6.75,
    '10.0':8.2
}

exp0.add_site(900, tetrodes=[2,4,6,8])
exp0.add_session('16-39-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-40-59', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-42-29', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-50-57', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-58-12', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('17-22-28', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[2,4,6,8])
exp0.add_session('17-40-25', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-41-44', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('17-43-02', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-47-47', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('17-55-40', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('18-20-55', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[2,4,6,7,8])
exp0.add_session('18-39-29', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-41-02', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('18-42-24', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('18-49-27', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('18-56-39', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('19-22-22', 'l', 'noiseAmps', 'am_tuning_curve')
