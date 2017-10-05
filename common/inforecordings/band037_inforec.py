from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band037'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-10-04', 'right_AC', info=['medialDiI','TT1ant'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.9,
    '2.5':3.5,
    '3.0':4.1,
    '3.5':4.8
}

#rig 2 is messed up, no recordings done

exp1 = celldatabase.Experiment(subject, '2017-10-05', 'left_AC', info=['medialDiI','TT1ant'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.25,
    '2.0':1.55,
    '2.5':1.9,
    '3.0':2.35,
    '3.5':2.7
}

exp1.add_site(1250, tetrodes=[2,6,7,8])
exp1.add_session('13-02-19', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1275, tetrodes=[2,4,6,7,8])
exp1.add_session('13-07-26', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[2,4,6,7,8])
exp1.add_session('13-13-51', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1325, tetrodes=[2,4,6,7,8])
exp1.add_session('13-18-26', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-19-31', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1350, tetrodes=[2,4,6,8])
exp1.add_session('13-27-38', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1375, tetrodes=[1,2,4,6,8])
exp1.add_session('13-32-55', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1400, tetrodes=[1,2,4,7,8])
exp1.add_session('13-37-54', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1425, tetrodes=[2,4,7,8])
exp1.add_session('13-44-28', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1450, tetrodes=[2,4,7,8])
exp1.add_session('13-48-44', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1475, tetrodes=[1,2,3,4,7,8])
exp1.add_session('13-54-55', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1500, tetrodes=[1,2,4,6,7,8])
exp1.add_session('14-04-08', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-05-27', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-07-58', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-14-37', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('14-20-19', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-22-37', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('14-26-26', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-45-31', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('14-56-37', 'e', 'noiseAmps', 'am_tuning_curve')
