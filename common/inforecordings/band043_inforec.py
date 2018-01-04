from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band043'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-12-12', 'left_AC', info=['medialDiI','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.8,
    '2.5':3.35,
    '3.0':3.95,
    '3.5':4.65
}

exp0.add_site(825, tetrodes=[8])
exp0.add_session('12-11-20', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-12-37', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(875, tetrodes=[6,8])
exp0.add_session('12-38-43', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(900, tetrodes=[2,4,6,7,8])
exp0.add_session('12-52-20', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-53-20', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(925, tetrodes=[6,8])
exp0.add_session('13-06-41', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(950, tetrodes=[2,6,8])
exp0.add_session('13-41-22', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-42-31', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(975, tetrodes=[2,6,7,8])
exp0.add_session('14-02-18', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[6,7,8])
exp0.add_session('14-13-07', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1025, tetrodes=[1,6,7,8])
exp0.add_session('14-22-43', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1050, tetrodes=[1,6,7,8])
exp0.add_session('14-30-29', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1075, tetrodes=[1,6,7,8])
exp0.add_session('14-36-15', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[1,6,7,8])
exp0.add_session('14-42-14', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1125, tetrodes=[2,6,7,8])
exp0.add_session('14-47-19', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[1,5,6,7,8])
exp0.add_session('14-57-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-58-28', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1175, tetrodes=[5,6,7,8])
exp0.add_session('15-01-45', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[1,5,6,7,8])
exp0.add_session('15-17-29', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1225, tetrodes=[5,6,7,8])
exp0.add_session('15-27-47', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-32-31', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-33-43', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-42-26', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('15-46-46', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-49-18', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-53-49', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-13-22', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('16-25-44', 'e', 'noiseAmps', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-12-14', 'left_AC', info=['middleDiD','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.8,
    '2.5':3.4,
    '3.0':4.0,
    '3.5':4.6
}

exp1.add_site(900, tetrodes=[2,4,6,8])
exp1.add_session('12-26-22', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-27-39', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(925, tetrodes=[2,4,6,8])
exp1.add_session('12-34-03', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-35-14', None, 'laserPulse', 'am_tuning_curve') #2.5 mW

exp1.add_site(950, tetrodes=[2,4,6,8])
exp1.add_session('12-45-17', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(975, tetrodes=[2,4,6,8])
exp1.add_session('12-56-50', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1000, tetrodes=[2,3,4,6,8])
exp1.add_session('13-16-01', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1025, tetrodes=[2,3,4,6,8])
exp1.add_session('13-31-54', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-32-58', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-34-36', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-42-37', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-47-09', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-49-53', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-53-25', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-13-56', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('14-25-25', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1075, tetrodes=[2,3,4,6,8])
exp1.add_session('14-37-41', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[1,2,3,4,6,8])
exp1.add_session('14-47-26', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1125, tetrodes=[1,2,3,4,6,8])
exp1.add_session('14-55-04', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1150, tetrodes=[1,2,3,4,6,8])
exp1.add_session('15-00-19', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1175, tetrodes=[1,2,3,4,6,8])
exp1.add_session('15-06-47', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-19-17', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1225, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-25-51', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-26-55', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-39-13', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1275, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-45-33', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-50-41', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1325, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-02-15', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-03-15', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-05-39', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-13-53', 'g', 'AM', 'am_tuning_curve')
exp1.add_session('16-18-08', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-20-56', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('16-25-18', 'h', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-44-57', 'i', 'harmonics', 'bandwidth_am')
exp1.add_session('16-56-24', 'j', 'noiseAmps', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-12-15', 'right_AC', info=['medialDiI','TT1ant','soundleft'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.85,
    '2.5':3.45,
    '3.0':4.0,
    '3.5':4.7
}

exp2.add_site(950, tetrodes=[2,4,6,7,8])
exp2.add_session('12-39-36', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1000, tetrodes=[1,2,4,5,6,8])
exp2.add_session('12-52-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-53-38', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1025, tetrodes=[1,2,4,5,6,8])
exp2.add_session('13-02-58', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1050, tetrodes=[1,2,4,5,6,8])
exp2.add_session('13-09-06', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1060, tetrodes=[1,2,4,5,6,8])
exp2.add_session('13-23-57', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-29-48', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-39-35', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-46-39', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-47-35', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-49-00', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-57-39', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-01-53', None, 'laserPulse', 'am_tuning_curve') #laser responsive cell gone
exp2.add_session('14-03-59', None, 'laserTrain', 'am_tuning_curve')
# not really any good cells/responses

exp2.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-15-09', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-22-33', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-23-33', 'c', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-31-34', 'd', 'AM', 'am_tuning_curve')
exp2.add_session('14-35-53', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-39-02', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-42-12', 'e', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-00-51', 'f', 'harmonics', 'bandwidth_am')
exp2.add_session('15-19-19', 'g', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1225, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('15-30-27', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-31-42', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1240, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('15-35-32', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-37-11', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-45-42', 'i', 'AM', 'am_tuning_curve')
exp2.add_session('15-50-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-52-13', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-57-40', 'j', 'bandwidth', 'bandwidth_am')
exp2.add_session('16-17-30', 'k', 'harmonics', 'bandwidth_am')
exp2.add_session('16-28-34', 'l', 'noiseAmps', 'am_tuning_curve')


exp3 = celldatabase.Experiment(subject, '2017-12-19', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.45,
    '1.0':1.85,
    '1.5':2.4,
    '2.0':3.0,
    '2.5':3.6,
    '3.0':4.25,
    '3.5':5.0
}

exp3.add_site(875, tetrodes=[2,4,6,8])
exp3.add_session('11-25-40', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-26-47', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(900, tetrodes=[2,4,6,8])
exp3.add_session('11-36-03', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(950, tetrodes=[2,4,6,8])
exp3.add_session('11-40-52', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(975, tetrodes=[2,4,6,8])
exp3.add_session('11-56-39', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1000, tetrodes=[2,4,6,8])
exp3.add_session('12-01-08', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1025, tetrodes=[2,4,6,8])
exp3.add_session('12-12-38', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1050, tetrodes=[1,2,4,6,8])
exp3.add_session('12-17-49', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1075, tetrodes=[1,2,4,6,8])
exp3.add_session('12-21-00', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,4,6,7,8])
exp3.add_session('12-23-51', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('12-28-38', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('12-33-09', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('12-37-47', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-38-56', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-40-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-49-58', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-54-11', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-56-37', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-00-02', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-23-18', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-35-31', 'e', 'noiseAmps', 'am_tuning_curve')
