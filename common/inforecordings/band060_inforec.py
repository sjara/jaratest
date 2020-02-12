from jaratoolbox import celldatabase

subject = 'band060'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2018-03-29', 'right_AC', info=['medialDiD','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':1.6,
#     '1.0':2.35,
#     '1.5':3.3,
#     '2.0':4.15,
#     '2.5':5.65,
#     '3.0':7.0,
#     '3.5':9.7
# }

# exp0.add_site(1450, tetrodes=[1,2,6,8])
# exp0.add_session('17-00-55', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('17-03-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1500, tetrodes=[1,2])
# exp0.add_session('17-13-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1525, tetrodes=[1,2,4,8])
# exp0.add_session('17-23-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1550, tetrodes=[1,2])
# exp0.add_session('17-30-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1575, tetrodes=[1,2])
# exp0.add_session('17-42-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1600, tetrodes=[1,2])
# exp0.add_session('17-55-02', None, 'laserPulse', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2018-04-02', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.6,
    '1.0':2.5,
    '1.5':3.4,
    '2.0':4.4,
    '2.5':5.8,
    '3.0':7.2,
    '3.5':10.0
}

# exp1.add_site(1000, tetrodes=[2,4,6])
# exp1.add_session('10-31-14', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1050, tetrodes=[2,4,6,8])
# exp1.add_session('10-43-13', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('10-44-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1075, tetrodes=[2,4,6,8])
# exp1.add_session('10-54-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-05-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1125, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-15-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1150, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-21-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1175, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-41-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1200, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-58-34', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1225, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('12-11-30', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-13-38', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-14-36', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-19-13', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-26-29', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('12-52-22', 'd', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-16-24', 'e', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1250, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('14-30-03', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1275, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('14-45-18', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('14-46-58', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-48-09', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-56-10', 'g', 'AM', 'am_tuning_curve')
exp1.add_session('15-00-24', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-02-35', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('15-05-18', 'h', 'bandwidth', 'bandwidth_am')
exp1.add_session('15-31-34', 'i', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1275


# exp2 = celldatabase.Experiment(subject, '2018-04-03', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':1.65,
#     '1.0':2.5,
#     '1.5':3.4,
#     '2.0':4.35,
#     '2.5':5.8,
#     '3.0':7.15,
#     '3.5':9.6
# }

# exp2.add_site(900, tetrodes=[5,6,7,8])
# exp2.add_session('09-27-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1050, tetrodes=[5,6,7,8])
# exp2.add_session('09-59-43', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1150, tetrodes=[4,6])
# exp2.add_session('10-09-05', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes=[4,6,8])
# exp2.add_session('10-16-02', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1300, tetrodes=[3,4,6])
# exp2.add_session('10-27-14', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1325, tetrodes=[3,4,6])
# exp2.add_session('10-39-31', None, 'noisebursts', 'am_tuning_curve')
# #observed TT1/2 and 7/8 bending/not penetrating, not very good signals

#trying again on other side
exp3 = celldatabase.Experiment(subject, '2018-04-03', 'left_AC', info=['lateralDiD','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.65,
    '1.0':2.5,
    '1.5':3.4,
    '2.0':4.35,
    '2.5':5.8,
    '3.0':7.15,
    '3.5':9.6
}

exp3.add_site(900, tetrodes=[2,4,5,6,7,8])
exp3.add_session('11-44-53', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-45-57', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('11-47-47', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-12-31', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-16-58', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-19-13', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-26-00', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('12-48-35', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-04-23', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(950, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('13-41-26', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('13-42-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(975, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('14-20-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('14-47-18', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-51-41', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1025, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('15-05-36', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-06-47', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-08-43', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-21-27', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('15-26-44', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-28-54', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-33-30', 'h', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-54-22', 'i', 'harmonics', 'bandwidth_am')
exp3.add_session('16-05-31', 'j', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('16-16-42', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-18-02', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-19-33', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-31-37', 'l', 'AM', 'am_tuning_curve')
exp3.add_session('16-39-13', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-51-48', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('16-54-38', 'm', 'bandwidth', 'bandwidth_am')
exp3.add_session('17-28-39', 'n', 'harmonics', 'bandwidth_am')
exp3.add_session('17-40-10', 'o', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('17-55-30', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1225, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('18-04-36', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-05-32', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('18-07-06', 'p', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('18-15-10', 'q', 'AM', 'am_tuning_curve')
exp3.add_session('18-19-22', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('18-21-43', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('18-25-22', 'r', 'bandwidth', 'bandwidth_am')
exp3.add_session('18-48-45', 's', 'harmonics', 'bandwidth_am')
exp3.add_session('18-59-49', 't', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1225


exp4 = celldatabase.Experiment(subject, '2018-04-04', 'left_AC', info=['middleDiI','TT1ant','sound_right'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.6,
    '1.0':2.45,
    '1.5':3.35,
    '2.0':4.25,
    '2.5':5.65,
    '3.0':6.8,
    '3.5':8.75
}

# exp4.add_site(900, tetrodes=[1,2,5,6,7,8])
# exp4.add_session('10-09-50', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('10-11-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(925, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('10-24-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(950, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('10-36-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(975, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('10-51-17', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('10-52-38', None, 'laserPulse', 'am_tuning_curve') #2.5 mW
#
# exp4.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('11-09-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1025, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('11-24-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('11-35-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('11-51-00', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('11-58-26', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('12-05-30', None, 'laserPulse', 'am_tuning_curve') #3.5 mW
exp4.add_session('12-07-11', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-08-37', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-16-48', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('12-21-01', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-23-07', None, 'laserTrain', 'am_tuning_curve')
#lost laser responsive cell

# exp4.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('12-45-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1175, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('12-53-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('12-59-49', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1225, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('13-25-48', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-27-32', 'c', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-36-50', 'd', 'AM', 'am_tuning_curve')
exp4.add_session('13-41-20', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-43-30', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('13-47-38', 'e', 'bandwidth', 'bandwidth_am')
exp4.add_session('14-09-37', 'f', 'bandwidth', 'bandwidth_am')
exp4.add_session('14-28-45', 'g', 'harmonics', 'bandwidth_am')
exp4.add_session('14-38-35', 'h', 'harmonics', 'bandwidth_am')
exp4.add_session('15-11-49', 'i', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1225


exp5 = celldatabase.Experiment(subject, '2018-04-05', 'left_AC', info=['medialDiD','TT1ant','sound_right'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.6,
    '1.0':2.35,
    '1.5':3.25,
    '2.0':4.1,
    '2.5':5.5,
    '3.0':6.55,
    '3.5':8.2
}

# exp5.add_site(800, tetrodes=[1,2,4,5,6,8])
# exp5.add_session('11-03-04', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(850, tetrodes=[1,2,4,6,8])
# exp5.add_session('11-19-03', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(900, tetrodes=[2,4,6,7,8])
# exp5.add_session('11-24-35', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(925, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('12-00-14', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('12-01-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(950, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-08-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(975, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-11-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-16-27', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('12-17-34', None, 'laserPulse', 'am_tuning_curve') #2.5mW
#
# exp5.add_site(1025, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-22-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-29-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1075, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-34-01', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-41-36', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1125, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('12-50-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp5.add_session('13-01-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1175, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('13-09-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('13-19-25', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1225, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('13-26-11', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('13-28-42', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-38-52', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('13-43-08', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('13-45-23', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('13-49-04', 'c', 'bandwidth', 'bandwidth_am')
exp5.add_session('14-07-50', 'd', 'harmonics', 'bandwidth_am')
exp5.add_session('14-18-54', 'e', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1225
