from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band075'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-08-18', 'right_AC', info=['medialDiI','TT1ant','soundleft'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.3,
    '2.0':3.75,
    '3.0':4.25,
    '4.0':4.75,
    '5.0':5.2,
    '7.5':6.45,
    '10.0':7.65
    }

exp0.add_site(1000, tetrodes=[2,4,6,8])
exp0.add_session('13-52-57', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1050, tetrodes=[1,2,4,6])
exp0.add_session('14-12-12', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-13-24', None, 'lasernoisebursts', 'bandwidth_am')

exp0.add_site(1100, tetrodes=[1,2,4,6])
exp0.add_session('14-45-35', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('14-46-48', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[1,2,4,6,8])
exp0.add_session('14-52-50', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1175, tetrodes=[1,2,3,4,6,8])
exp0.add_session('14-58-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-59-47', None, 'lasernoisebursts', 'bandwidth_am')

exp0.add_site(1200, tetrodes=[1,2,3,4,6,8])
exp0.add_session('15-05-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-06-14', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('15-09-08', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-13-40', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('15-19-39', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('15-22-08', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-46-14', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,3,4,6,8])
exp0.add_session('15-59-37', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-01-13', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-03-40', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-07-52', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('16-12-14', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('16-15-42', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-39-40', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[1,2,3,4,6,8])
exp0.add_session('16-51-15', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-52-53', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-55-09', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-59-20', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('17-03-42', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('17-06-41', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('17-30-40', 'l', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('17-43-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-44-46', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('17-47-22', 'm', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-51-49', 'n', 'AM', 'am_tuning_curve')
exp0.add_session('17-56-34', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('18-00-22', 'o', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('18-24-19', 'p', 'noiseAmps', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2018-08-19', 'right_AC', info=['middleDiD','TT1ant','soundleft'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.3,
    '2.0':3.75,
    '3.0':4.2,
    '4.0':4.7,
    '5.0':5.2,
    '7.5':6.4,
    '10.0':7.65
    }

exp1.add_site(1100, tetrodes=[2])
exp1.add_session('13-28-11', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-29-52', None, 'lasernoisebursts', 'bandwidth_am')

exp1.add_site(1200, tetrodes=[2,4,6])
exp1.add_session('13-38-59', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[2,4,6,8])
exp1.add_session('13-44-48', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-46-08', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-48-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-52-58', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-57-22', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('13-59-39', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('14-24-00', 'd', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1350, tetrodes=[1,2,3,4,6])
exp1.add_session('14-39-23', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1450, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('14-50-03', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-51-46', None, 'lasernoisebursts', 'bandwidth_am')

exp1.add_site(1500, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-03-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-04-48', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-06-52', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-11-17', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('15-15-33', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('15-18-59', 'g', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('15-42-58', 'h', 'noiseAmps', 'am_tuning_curve')