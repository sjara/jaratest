from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band038'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-10-10', 'right_AC', info=['medialDiI','TT1ant'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.35,
    '2.0':2.95,
    '2.5':3.6,
    '3.0':4.2,
    '3.5':5.0
}

exp0.add_site(1100, tetrodes=[2,4])
exp0.add_session('11-17-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-18-55', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[2,3,4,6,8])
exp0.add_session('11-24-24', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[1,2,3,4,6,8])
exp0.add_session('11-29-33', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1225, tetrodes=[1,2,3,4,6,8])
exp0.add_session('11-34-02', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('11-35-08', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1250, tetrodes=[1,2,3,4,6,8])
exp0.add_session('11-43-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('11-44-37', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-45-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-51-53', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('11-56-07', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('11-58-36', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('12-03-31', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('12-22-01', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('12-33-11', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1350, tetrodes=[2,4,5,6,8])
exp0.add_session('14-35-58', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1375, tetrodes=[2,4,6,7,8])
exp0.add_session('14-44-42', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[2,4,6,7,8])
exp0.add_session('14-50-06', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1425, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-54-57', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1450, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-57-34', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1475, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-11-33', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-13-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-15-02', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-22-05', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('15-28-38', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-30-47', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-33-52', 'h', 'bandwidth', 'bandwidth_am')
exp0.add_session('15-52-22', 'i', 'harmonics', 'bandwidth_am')
exp0.add_session('16-03-42', 'j', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1525, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-18-05', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1550, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-28-41', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1575, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-32-04', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1600, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-38-36', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1610, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-44-30', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1620, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-48-22', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-49-38', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-51-22', 'k', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-56-53', 'l', 'AM', 'am_tuning_curve')
exp0.add_session('17-01-13', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('17-03-23', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('17-07-10', 'm', 'bandwidth', 'bandwidth_am')
exp0.add_session('17-26-17', 'n', 'harmonics', 'bandwidth_am')
exp0.add_session('17-37-24', 'o', 'noiseAmps', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-10-11', 'left_AC', info=['medialDiI','TT1ant'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.45,
    '1.0':1.9,
    '1.5':2.55,
    '2.0':3.2,
    '2.5':3.9,
    '3.0':4.6,
    '3.5':5.55
}

exp1.add_site(966, tetrodes=[2,4,6,7,8])
exp1.add_session('10-48-29', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-51-20', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1050, tetrodes=[2,4,5,6,7,8])
exp1.add_session('10-59-48', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1075, tetrodes=[2,4,5,6,7,8])
exp1.add_session('11-13-04', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[2,4,5,6,7,8])
exp1.add_session('11-22-04', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1125, tetrodes=[2,4,5,6,7,8])
exp1.add_session('11-37-05', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-19-09', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1160, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-22-46', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-25-13', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-28-22', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-29-25', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1225, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-37-52', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-42-15', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1275, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-55-27', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-56-21', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-57-46', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-03-22', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-07-40', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-10-02', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-12-49', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('13-35-32', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('13-46-36', 'e', 'noiseAmps', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-10-12', 'right_AC', info=['middleDiD','TT1ant'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.25,
    '2.0':2.8,
    '2.5':3.35,
    '3.0':3.9,
    '3.5':4.6
}

exp2.add_site(1100, tetrodes=[2,4,8])
exp2.add_session('11-33-54', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-35-08', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1125, tetrodes=[2,4,6,8])
exp2.add_session('11-39-19', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1150, tetrodes=[2,4,6,8])
exp2.add_session('11-49-17', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1175, tetrodes=[2,4,6,8])
exp2.add_session('11-54-02', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1200, tetrodes=[2,4,6,8])
exp2.add_session('12-03-36', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1225, tetrodes=[1,2,4,6,8])
exp2.add_session('12-12-31', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1250, tetrodes=[1,2,4,6,8])
exp2.add_session('12-17-58', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-19-22', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1275, tetrodes=[1,2,4,6,8])
exp2.add_session('12-29-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-30-56', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-33-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-39-15', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('12-43-30', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-46-06', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('12-48-53', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-07-22', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('13-18-35', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1325, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-48-05', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1350, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-53-56', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1375, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-58-26', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-00-12', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1400, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-06-45', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1425, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-12-02', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1450, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-16-42', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1475, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-23-11', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-24-50', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1485, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-28-05', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1500, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-32-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-36-29', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1480, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-41-00', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1470, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-45-01', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1460, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-49-28', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1440, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-53-45', None, 'laserPulse', 'am_tuning_curve')
