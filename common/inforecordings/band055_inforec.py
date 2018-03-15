from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band055'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-03-14', 'right_AC', info=['medialDiI','TT1ant','soundleft'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.4,
    '2.0':3.8,
    '3.0':4.4,
    '4.0':4.9,
    '5.0':5.4,
    '7.5':6.75,
    '10.0':8.05
}

#trying 5mW laser to start
exp0.add_site(900, tetrodes=[1,2,4,6,8])
exp0.add_session('10-57-53', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-01-37', None, 'lasernoisebursts', 'bandwidth_am')
#no particular difference between laser and non-laser trials

exp0.add_site(925, tetrodes=[1,2,4,6,8])
exp0.add_session('11-21-00', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-22-13', None, 'lasernoisebursts', 'bandwidth_am')

exp0.add_site(950, tetrodes=[1,2,4,6,8])
exp0.add_session('11-35-36', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-36-54', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('11-39-05', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-47-24', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('11-54-25', 'c', 'laserBandwidth', 'bandwidth_am')

exp0.add_site(1000, tetrodes=[1,2,4,6,8])
exp0.add_session('12-36-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-37-52', None, 'lasernoisebursts', 'bandwidth_am')
#laser up to 7.5mW
exp0.add_session('12-40-04', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('12-42-31', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-52-35', 'e', 'AM', 'am_tuning_curve')
exp0.add_session('12-58-32', 'f', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('13-22-58', 'g', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[1,2,3,4,6,8])
exp0.add_session('14-42-08', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-43-22', None, 'lasernoisebursts', 'bandwidth_am')

exp0.add_site(1175, tetrodes=[1,2,3,4,6,8])
exp0.add_session('15-22-55', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[2,4,8])
exp0.add_session('15-41-41', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1250, tetrodes=[1,2,4,6,7,8])
exp0.add_session('15-51-35', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-52-46', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('15-55-11', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-03-24', 'i', 'AM', 'am_tuning_curve')
exp0.add_session('16-09-57', 'j', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-36-36', 'k', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,4,6,7,8])
exp0.add_session('16-54-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-55-52', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-58-12', 'l', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-06-49', 'm', 'AM', 'am_tuning_curve')
exp0.add_session('17-13-49', 'n', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('17-39-15', 'o', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1375, tetrodes=[1,2,4,6,7,8])
exp0.add_session('17-54-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-56-01', None, 'lasernoisebursts', 'bandwidth_am') #back to 5mW
exp0.add_session('17-58-00', 'p', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('18-06-48', 'q', 'AM', 'am_tuning_curve')
exp0.add_session('18-13-01', 'r', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('18-40-19', 's', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1425, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('18-57-17', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-58-47', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('19-00-05', 't', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('19-08-18', 'u', 'AM', 'am_tuning_curve')
#looks like same cells as previous site
