from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band041'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-11-21', 'left_AC', info=['medialDiI','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.35,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.65,
    '2.5':3.2,
    '3.0':3.75,
    '3.5':4.4
}

exp0.add_site(750, tetrodes=[1,2,4,6,8])
exp0.add_session('12-52-49', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-54-29', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-56-46', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-05-46', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-10-05', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-12-15', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-16-29', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('13-36-40', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('13-48-41', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(800, tetrodes=[1,2,4,6,8])
exp0.add_session('13-59-23', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(850, tetrodes=[1,2,4,6,8])
exp0.add_session('14-06-54', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-08-31', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-10-04', None, 'noisebursts', 'am_tuning_curve') #left speaker
exp0.add_session('14-14-30', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-23-10', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('14-27-26', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-29-34', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-35-17', 'h', 'bandwidth', 'bandwidth_am')
exp0.add_session('14-55-30', 'i', 'harmonics', 'bandwidth_am')
exp0.add_session('15-06-39', 'j', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(950, tetrodes=[1,2,4,6,8])
exp0.add_session('15-23-58', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(975, tetrodes=[2,4,5,6,8])
exp0.add_session('15-39-46', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[1,2,4,5,6,8])
exp0.add_session('15-43-53', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1025, tetrodes=[1,2,4,5,6,8])
exp0.add_session('15-49-11', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1050, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-03-29', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1075, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-08-48', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-17-17', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1125, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-22-52', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-28-28', None, 'laserPulse', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-11-28', 'left_AC', info=['middleDiD','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.8,
    '2.5':3.25,
    '3.0':3.9,
    '3.5':4.6
}

exp1.add_site(752, tetrodes=[1,2,4,5,6,8])
exp1.add_session('12-21-52', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-22-52', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-25-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-33-59', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-38-50', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-40-59', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-44-58', 'c', 'bandwidth', 'bandwidth_am') #40kHz, 64Hz
exp1.add_session('13-06-47', 'd', 'bandwidth', 'bandwidth_am') #12kHz, 32Hz
exp1.add_session('13-25-55', 'e', 'harmonics', 'bandwidth_am') #12kHz, 32Hz
exp1.add_session('13-37-04', 'f', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(800, tetrodes=[1,2,4,5,6,8])
exp1.add_session('13-50-24', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(825, tetrodes=[1,2,4,5,6,8])
exp1.add_session('14-47-50', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(850, tetrodes=[2,4,6,8])
exp1.add_session('15-05-55', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-06-58', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(875, tetrodes=[1,2,4,5,6,8])
exp1.add_session('15-20-18', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(900, tetrodes=[1,2,4,5,6,8])
exp1.add_session('15-27-18', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(925, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('15-36-38', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(950, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('15-42-25', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(975, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('15-49-36', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-56-23', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-05-32', None, 'laserPulse', 'am_tuning_curve')
#checked mouse, well almost totally dry

exp1.add_site(1025, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-15-05', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-18-55', None, 'laserPulse', 'am_tuning_curve')
# laser artifacts gone!

exp1.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-25-33', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-31-45', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-36-12', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-37-13', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('16-44-10', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-45-48', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('16-47-28', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-55-45', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('17-00-37', None, 'laserPulse', 'am_tuning_curve') #RIP really nice TT4 cell
exp1.add_session('17-02-44', None, 'laserTrain', 'am_tuning_curve')
# laser responsive cell gone


exp2 = celldatabase.Experiment(subject, '2017-11-30', 'left_AC', info=['lateralDiI','TT1ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.7,
    '2.5':3.3,
    '3.0':3.85,
    '3.5':4.5
}

exp2.add_site(700, tetrodes=[2,4,6,8])
exp2.add_session('13-00-47', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-01-49', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(750, tetrodes=[2,4,6,8])
exp2.add_session('13-12-46', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-13-51', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-15-03', None, 'laserPulse', 'am_tuning_curve') #2.5 mW

exp2.add_site(775, tetrodes=[1,2,4,6,8])
exp2.add_session('13-29-27', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(800, tetrodes=[1,2,3,4,6,8])
exp2.add_session('13-38-25', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-39-23', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-40-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-54-12', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-58-28', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-00-57', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-04-38', 'c', 'bandwidth', 'bandwidth_am') #22kHz, 64Hz for TT2
exp2.add_session('14-23-04', 'd', 'bandwidth', 'bandwidth_am') #10kHz, 64Hz for TT8
exp2.add_session('14-41-53', 'e', 'harmonics', 'bandwidth_am') #22kHz
exp2.add_session('14-59-36', 'f', 'harmonics', 'bandwidth_am') #10kHz
exp2.add_session('15-12-02', 'g', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(850, tetrodes=[1,2,4,6,8])
exp2.add_session('15-31-11', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(900, tetrodes=[2,4,6,8])
exp2.add_session('15-38-10', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(925, tetrodes=[1,2,4,6,8])
exp2.add_session('15-42-15', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(950, tetrodes=[1,2,4,6,7,8])
exp2.add_session('15-57-44', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(975, tetrodes=[1,2,4,6,7,8])
exp2.add_session('16-03-13', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-04-39', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-06-59', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-16-33', 'i', 'AM', 'am_tuning_curve')
exp2.add_session('16-21-47', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-24-55', None, 'laserTrain', 'am_tuning_curve')
#laser responsive cells, not very good tuning
exp2.add_session('16-29-54', 'j', 'bandwidth', 'bandwidth_am')
exp2.add_session('16-48-23', 'k', 'harmonics', 'bandwidth_am')
exp2.add_session('16-59-28', 'l', 'noiseAmps', 'am_tuning_curve')


exp3 = celldatabase.Experiment(subject, '2017-12-01', 'left_AC', info=['lateralDiD','TT1ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.35,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.7,
    '2.5':3.25,
    '3.0':3.8,
    '3.5':4.4
}

exp3.add_site(750, tetrodes=[1,2,4,6,7,8])
exp3.add_session('13-53-00', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-54-18', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(775, tetrodes=[1,2,4,6,8])
exp3.add_session('15-04-00', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-04-56', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-08-36', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-16-52', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('15-21-06', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-23-19', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-27-02', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-45-27', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('15-57-19', 'e', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(825, tetrodes=[1,2,4,6,8])
exp3.add_session('16-05-10', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(850, tetrodes=[1,2,4,6,8])
exp3.add_session('16-08-57', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-10-02', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-11-30', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-20-27', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('16-25-03', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-27-11', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('16-30-29', 'h', 'bandwidth', 'bandwidth_am')
exp3.add_session('16-48-53', 'i', 'harmonics', 'bandwidth_am')
exp3.add_session('17-00-14', 'j', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(900, tetrodes=[1,2,4,6,8])
exp3.add_session('17-09-09', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('17-10-25', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(925, tetrodes=[1,2,4,6,8])
exp3.add_session('17-16-17', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('17-17-59', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('17-26-07', 'l', 'AM', 'am_tuning_curve')
exp3.add_session('17-30-20', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('17-32-37', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('17-36-13', 'm', 'bandwidth', 'bandwidth_am')
exp3.add_session('17-54-53', 'n', 'harmonics', 'bandwidth_am')
exp3.add_session('18-06-01', 'o', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(975, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('18-15-58', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-18-01', 'p', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('18-26-03', 'q', 'AM', 'am_tuning_curve')
exp3.add_session('18-30-17', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-32-41', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('18-36-57', 'r', 'bandwidth', 'bandwidth_am')
exp3.add_session('18-55-17', 's', 'harmonics', 'bandwidth_am')
exp3.add_session('19-06-32', 't', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1050, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('19-16-50', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1075, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('19-22-32', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,3,4,5,6,8])
exp3.add_session('19-26-31', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1125, tetrodes=[1,2,3,4,5,6,8])
exp3.add_session('19-30-46', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1150, tetrodes=[1,2,3,4,5,6,8])
exp3.add_session('19-34-18', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1175, tetrodes=[1,2,3,4,5,6,8])
exp3.add_session('19-37-27', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('19-39-11', 'u', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('19-47-27', 'v', 'AM', 'am_tuning_curve')
exp3.add_session('19-51-41', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('19-54-15', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('19-57-38', 'w', 'bandwidth', 'bandwidth_am')
exp3.add_session('20-16-38', 'x', 'harmonics', 'bandwidth_am')
exp3.add_session('20-27-46', 'y', 'noiseAmps', 'am_tuning_curve')


exp4 = celldatabase.Experiment(subject, '2017-12-05', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.85,
    '2.5':3.4,
    '3.0':4.0,
    '3.5':4.8
}

exp4.add_site(750, tetrodes=[1,2,4])
exp4.add_session('12-54-08', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-55-24', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(775, tetrodes=[1,2,4])
exp4.add_session('13-02-30', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-03-27', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-05-03', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-14-35', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('13-19-16', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-21-31', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('13-24-43', 'c', 'bandwidth', 'bandwidth_am')
exp4.add_session('13-45-19', 'd', 'harmonics', 'bandwidth_am')
exp4.add_session('13-56-50', 'e', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(850, tetrodes=[1,2,4,6,7])
exp4.add_session('14-07-29', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-08-43', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(875, tetrodes=[1,2,4,6,7])
exp4.add_session('14-13-34', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(900, tetrodes=[1,2,4,6,7])
exp4.add_session('14-17-43', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(925, tetrodes=[1,2,4,6,7])
exp4.add_session('14-22-14', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-23-02', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-24-39', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-33-53', 'g', 'AM', 'am_tuning_curve')
exp4.add_session('14-38-20', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-40-34', None, 'laserTrain', 'am_tuning_curve')
# good cells gone

exp4.add_site(950, tetrodes=[1,2,4,6,7,8])
exp4.add_session('14-47-50', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(975, tetrodes=[1,2,4,6,7,8])
exp4.add_session('14-51-57', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1000, tetrodes=[1,2,4,6,7,8])
exp4.add_session('14-55-47', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1025, tetrodes=[1,2,4,6,7,8])
exp4.add_session('15-03-32', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-04-27', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-12-36', 'i', 'AM', 'am_tuning_curve')
exp4.add_session('15-17-05', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-19-50', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('15-22-47', 'j', 'bandwidth', 'bandwidth_am')
exp4.add_session('15-41-39', 'k', 'harmonics', 'bandwidth_am')
exp4.add_session('15-53-32', 'l', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1075, tetrodes=[1,2,4,6])
exp4.add_session('16-08-42', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-11-01', 'm', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-18-59', 'n', 'AM', 'am_tuning_curve')
exp4.add_session('16-23-13', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-25-22', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('16-28-43', 'o', 'bandwidth', 'bandwidth_am')
exp4.add_session('16-47-24', 'p', 'harmonics', 'bandwidth_am')
exp4.add_session('16-58-41', 'q', 'noiseAmps', 'am_tuning_curve')


exp5 = celldatabase.Experiment(subject, '2017-12-06', 'right_AC', info=['middleDiI','TT1ant','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.8,
    '2.5':3.4,
    '3.0':4.0,
    '3.5':4.6
}

exp5.add_site(725, tetrodes=[2,4])
exp5.add_session('10-35-29', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('10-36-49', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(750, tetrodes=[2,4])
exp5.add_session('10-41-15', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(775, tetrodes=[2,4])
exp5.add_session('10-46-47', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(800, tetrodes=[2,4])
exp5.add_session('10-53-17', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(825, tetrodes=[2,4,6])
exp5.add_session('10-58-26', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('10-59-34', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(850, tetrodes=[2,4,6,8])
exp5.add_session('11-04-10', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(875, tetrodes=[1,2,4,6,8])
exp5.add_session('11-16-23', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(900, tetrodes=[1,2,4,6,8])
exp5.add_session('11-23-00', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('11-23-54', None, 'laserPulse', 'am_tuning_curve') #2.5mW
exp5.add_session('11-24-54', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(925, tetrodes=[1,2,4,6,8])
exp5.add_session('11-33-09', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-34-34', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(950, tetrodes=[2,4,6,7,8])
exp5.add_session('12-05-04', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(975, tetrodes=[2,4,5,6,7,8])
exp5.add_session('12-18-42', None, 'laserPulse', 'am_tuning_curve') #back to 1.5mW
exp5.add_session('12-40-19', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1000, tetrodes=[2,4,5,6,7,])
exp5.add_session('12-46-42', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1025, tetrodes=[2,4,5,6,7,8])
exp5.add_session('12-58-05', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1050, tetrodes=[1,2,4,5,6,8])
exp5.add_session('13-01-15', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('13-03-44', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-04-58', 'a', 'tuningCurve', 'am_tuning_curve') #just wanted to see if weird-ass TT5 cell had any tuning!

exp5.add_site(1075, tetrodes=[2,4,5,6,7,8])
exp5.add_session('13-31-10', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('13-36-18', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('17-25-22', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1125, tetrodes=[1,2,4,6,8])
exp5.add_session('17-30-28', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1150, tetrodes=[1,2,4,6,7,8])
exp5.add_session('17-36-51', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1175, tetrodes=[1,2,4,6,7,8])
exp5.add_session('17-41-09', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1200, tetrodes=[1,2,4,6,7,8])
exp5.add_session('17-47-49', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1225, tetrodes=[1,2,4,6,7,8])
exp5.add_session('17-53-12', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1250, tetrodes=[1,2,4,6,7,8])
exp5.add_session('17-56-40', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1275, tetrodes=[1,2,4,6,7,8])
exp5.add_session('18-06-05', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1300, tetrodes=[1,2,4,6,7,8])
exp5.add_session('18-13-53', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1325, tetrodes=[1,2,4,6,7,8])
exp5.add_session('18-17-28', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('18-18-52', 'b', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-26-58', 'c', 'AM', 'am_tuning_curve')
exp5.add_session('18-31-15', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('18-33-58', None, 'laserTrain', 'am_tuning_curve')
# bad laser response
