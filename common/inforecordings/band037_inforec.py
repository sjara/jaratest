from jaratoolbox import celldatabase

subject = 'band037'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2017-10-04', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':1.4,
#     '1.0':1.8,
#     '1.5':2.3,
#     '2.0':2.9,
#     '2.5':3.5,
#     '3.0':4.1,
#     '3.5':4.8
# }

#rig 2 is messed up, no recordings done

exp1 = celldatabase.Experiment(subject, '2017-10-05', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
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

# exp1.add_site(1250, tetrodes=[2,6,7,8])
# exp1.add_session('13-02-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1275, tetrodes=[2,4,6,7,8])
# exp1.add_session('13-07-26', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[2,4,6,7,8])
# exp1.add_session('13-13-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1325, tetrodes=[2,4,6,7,8])
# exp1.add_session('13-18-26', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('13-19-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1350, tetrodes=[2,4,6,8])
# exp1.add_session('13-27-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1375, tetrodes=[1,2,4,6,8])
# exp1.add_session('13-32-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1400, tetrodes=[1,2,4,7,8])
# exp1.add_session('13-37-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1425, tetrodes=[2,4,7,8])
# exp1.add_session('13-44-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1450, tetrodes=[2,4,7,8])
# exp1.add_session('13-48-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1475, tetrodes=[1,2,3,4,7,8])
# exp1.add_session('13-54-55', None, 'laserPulse', 'am_tuning_curve')

# exp1.add_site(1500, tetrodes=[1,2,4,6,7,8])
# exp1.add_session('14-04-08', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('14-05-27', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('14-07-58', 'a', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('14-14-37', 'b', 'AM', 'am_tuning_curve')
# exp1.add_session('14-20-19', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('14-22-37', None, 'laserTrain', 'am_tuning_curve')
# exp1.add_session('14-26-26', 'c', 'bandwidth', 'bandwidth_am')
# exp1.add_session('14-45-31', 'd', 'harmonics', 'bandwidth_am')
# exp1.add_session('14-56-37', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1500


# exp2 = celldatabase.Experiment(subject, '2017-10-07', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':1.4,
#     '1.0':1.8,
#     '1.5':2.3,
#     '2.0':2.85,
#     '2.5':3.45,
#     '3.0':4.05,
#     '3.5':4.8
# }

# exp2.add_site(1350, tetrodes=[2,4])
# exp2.add_session('12-39-55', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-44-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1375, tetrodes=[2,4,6,8])
# exp2.add_session('12-50-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1400, tetrodes=[2,4,6,8])
# exp2.add_session('12-53-56', None, 'laserPulse', 'am_tuning_curve')

#still nothing at 1400um, pulling out and going to other side

exp3 = celldatabase.Experiment(subject, '2017-10-07', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.85,
    '2.5':3.45,
    '3.0':4.05,
    '3.5':4.8
}

# exp3.add_site(900, tetrodes=[2,4])
# exp3.add_session('13-10-15', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('13-11-19', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(950, tetrodes=[2,4,6,8])
exp3.add_session('13-15-43', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-16-52', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-18-21', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-24-02', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('13-28-16', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-30-41', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-34-15', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-53-08', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('14-04-32', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1025, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('14-14-06', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes=[2,3,4,6,8])
# exp3.add_session('14-18-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('14-22-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('14-26-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1125, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('14-30-47', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-31-55', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1150, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('14-39-02', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-41-18', 'f', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('14-46-49', 'g', 'AM', 'am_tuning_curve')
# exp3.add_session('14-51-17', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-53-36', None, 'laserTrain', 'am_tuning_curve')
# #lost the nice TT8 cell
#
# exp3.add_site(1175, tetrodes=[1,2,3,4,5,6,8])
# exp3.add_session('14-57-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[1,2,3,4,5,6,8])
# exp3.add_session('15-01-51', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1225, tetrodes=[1,2,3,4,5,6,8])
# exp3.add_session('15-05-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes=[1,2,3,4,5,6,8])
# exp3.add_session('15-09-48', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1275, tetrodes=[1,2,3,4,5,6,8])
# exp3.add_session('15-15-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('15-19-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1325, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('15-23-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1350, tetrodes=[1,2,3,4,6,7,8])
# exp3.add_session('15-26-17', None, 'laserPulse', 'am_tuning_curve')

exp3.maxDepth = 1350


# exp4 = celldatabase.Experiment(subject, '2017-10-09', 'left_AC', info=['lateralDiI','TT1ant','sound_right'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':1.35,
#     '1.0':1.7,
#     '1.5':2.15,
#     '2.0':2.6,
#     '2.5':3.15,
#     '3.0':3.65,
#     '3.5':4.25
# }
