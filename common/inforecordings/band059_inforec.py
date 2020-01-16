from jaratoolbox import celldatabase

subject = 'band059'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2018-03-08', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':1.55,
#     '1.0':2.3,
#     '1.5':3.15,
#     '2.0':4.0,
#     '2.5':5.0,
#     '3.0':6.3,
#     '3.5':7.6
# }

# exp0.add_site(1350, tetrodes=[2,8])
# exp0.add_session('16-35-39', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1400, tetrodes=[2,8])
# exp0.add_session('16-45-43', None, 'noisebursts', 'am_tuning_curve')


# exp1 = celldatabase.Experiment(subject, '2018-03-09', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
# experiments.append(exp1)
#
# exp1.laserCalibration = {
#     '0.5':1.45,
#     '1.0':2.0,
#     '1.5':2.7,
#     '2.0':3.25,
#     '2.5':3.95,
#     '3.0':4.75,
#     '3.5':5.9
# }

#Signals suddenly all went silent??


# exp2 = celldatabase.Experiment(subject, '2018-03-11', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':1.5,
#     '1.0':2.1,
#     '1.5':2.8,
#     '2.0':3.55,
#     '2.5':4.35,
#     '3.0':5.45,
#     '3.5':6.7
# }

#bad probe, no signal


exp3 = celldatabase.Experiment(subject, '2018-03-11', 'right_AC', info=['lateralDiD','TT1ant','sound_left'])
experiments.append(exp3)

# no laser calibration as had to switch out probe with mouse already in rig, using previous calibration for this probe
#
# exp3.add_site(925, tetrodes=[4,8])
# exp3.add_session('14-06-23', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1450, tetrodes=[8])
# exp3.add_session('15-45-11', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('15-46-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1500, tetrodes=[8])
# exp3.add_session('16-06-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1525, tetrodes=[8])
# exp3.add_session('16-23-52', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1550, tetrodes=[8])
# exp3.add_session('16-31-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1575, tetrodes=[8])
# exp3.add_session('16-38-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1600, tetrodes=[4,7,8])
# exp3.add_session('16-46-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1625, tetrodes=[4,7,8])
# exp3.add_session('16-52-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1650, tetrodes=[4,7,8])
# exp3.add_session('17-00-18', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1675, tetrodes=[2,4,7,8])
exp3.add_session('17-06-21', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('17-07-43', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-09-04', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('17-17-57', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('17-24-20', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('17-26-26', None, 'laserTrain', 'am_tuning_curve')
#LASER RESPONSIVE CELL GONE YET AGAIN

exp3.maxDepth = 1675


# exp4 = celldatabase.Experiment(subject, '2018-03-19', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':1.65,
#     '1.0':2.5,
#     '1.5':3.5,
#     '2.0':4.55,
#     '2.5':6.05,
#     '3.0':7.7
# }

# exp4.add_site(925, tetrodes=[2,6,7,8])
# exp4.add_session('11-39-50', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('11-41-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(950, tetrodes=[8])
# exp4.add_session('11-57-29', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1000, tetrodes=[2,4,6,7,8])
# exp4.add_session('12-05-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1050, tetrodes=[2,4,6,7,8])
# exp4.add_session('12-11-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1100, tetrodes=[2,4,6,7,8])
# exp4.add_session('12-24-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1125, tetrodes=[2,4,6,8])
# exp4.add_session('12-31-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1150, tetrodes=[2,3,4,6,8])
# exp4.add_session('12-36-14', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-37-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1175, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('12-45-23', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('13-00-10', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-01-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1225, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('13-07-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1250, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('13-13-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1300, tetrodes=[1,2,3,4,6,8])
# exp4.add_session('13-19-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1350, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('15-43-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1400, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('15-52-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1450, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('15-59-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('16-12-13', None, 'laserPulse', 'am_tuning_curve')


exp5 = celldatabase.Experiment(subject, '2018-03-26', 'left_AC', info=['lateralDiD','TT1ant','sound_right'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.85,
    '1.0':3.0,
    '1.5':4.2,
    '2.0':6.1,
    '2.5':8.1
}

# exp5.add_site(850, tetrodes=[1,2,4,6,8])
# exp5.add_session('11-57-38', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('11-59-01', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(875, tetrodes=[1,2,4,6,8])
# exp5.add_session('12-20-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(900, tetrodes=[1,2,4,6,8])
# exp5.add_session('12-26-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(925, tetrodes=[1,2,4,6,8])
# exp5.add_session('12-32-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(950, tetrodes=[1,2,4,6,8])
# exp5.add_session('12-38-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(975, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('12-43-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1000, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('12-48-25', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1025, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('12-54-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1050, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('13-01-07', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1075, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('13-07-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1100, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('13-13-00', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1125, tetrodes=[1,2,3,4,6,8])
# exp5.add_session('13-17-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1150, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('14-18-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1175, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('14-25-19', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('14-31-32', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-33-05', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-41-49', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('14-46-06', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-48-47', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('14-52-41', 'c', 'bandwidth', 'bandwidth_am')
exp5.add_session('15-11-03', 'd', 'noiseAmps', 'am_tuning_curve')
exp5.add_session('15-15-28', 'e', 'harmonics', 'bandwidth_am')

# exp5.add_site(1225, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('15-35-39', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('15-45-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1250, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('15-49-20', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1260, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('15-54-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1275, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-01-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1300, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-07-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1325, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-19-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1350, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-28-14', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1375, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-34-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1400, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-40-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1425, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-47-35', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1450, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('16-53-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1475, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-00-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-05-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1525, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-12-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1550, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-17-43', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1575, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-23-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp5.add_site(1600, tetrodes=[1,2,3,4,6,7,8])
# exp5.add_session('17-28-01', None, 'laserPulse', 'am_tuning_curve')

exp5.maxDepth = 1600
