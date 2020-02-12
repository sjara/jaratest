from jaratoolbox import celldatabase

subject = 'band032'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-07-14', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.5,
    '1.0':2.2,
    '1.5':3.0,
    '2.0':3.8,
    '2.5':4.8,
    '3.0':5.9,
    '3.5':7.35
}

# exp0.add_site(850, tetrodes=[2,3,4,5,6,7,8])
# exp0.add_session('13-28-32', None, 'laserPulse', 'am_tuning_curve') #no direct laser responses, but interesting off response on TT5
# exp0.add_session('13-30-09', None, 'noisebursts', 'am_tuning_curve') #TT5 cell appears to have small off response to sound as well
#
# exp0.add_site(900, tetrodes=[2,3,4,5,6,8])
# exp0.add_session('13-35-27', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(950, tetrodes=[2,3,4,5,6,8])
exp0.add_session('13-39-02', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-40-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-42-03', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-48-08', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-52-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-54-41', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-57-39', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('14-21-36', 'd', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1025, tetrodes = [2,3,4,5,6,8])
# exp0.add_session('14-30-28', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes = [1,2,3,4,8])
# exp0.add_session('14-34-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1075, tetrodes = [1,2,3,4,8])
# exp0.add_session('14-37-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes = [1,2,3,4,8])
# exp0.add_session('14-40-14', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('14-41-56', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1120, tetrodes = [1,2,3,4])
# exp0.add_session('14-46-10', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1140, tetrodes = [1,2,3,4,6,8])
exp0.add_session('14-49-45', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-51-18', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-53-20', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-59-02', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('15-03-14', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-05-22', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-08-14', 'g', 'bandwidth', 'bandwidth_am')
exp0.add_session('15-26-38', 'h', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1200, tetrodes = [2,3,4,6])
# exp0.add_session('15-36-47', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1225, tetrodes = [2,3,4,6])
exp0.add_session('15-39-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-40-46', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-42-57', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-48-37', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('15-52-50', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-54-57', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-58-05', 'k', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-16-47', 'l', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1300, tetrodes = [2,3,4,6])
# exp0.add_session('16-25-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1320, tetrodes = [2,3,4,6])
# exp0.add_session('16-29-05', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1340, tetrodes = [2,3,4,6,8])
# exp0.add_session('16-35-35', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('16-37-41', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1360, tetrodes = [2,3,4,6,8])
# exp0.add_session('16-40-58', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1380, tetrodes = [1,2,3,4,6,8])
exp0.add_session('16-44-57', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-46-00', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-47-45', 'm', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-53-17', 'n', 'AM', 'am_tuning_curve')
exp0.add_session('16-57-30', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-59-36', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('17-03-10', 'o', 'bandwidth', 'bandwidth_am')
exp0.add_session('17-25-51', 'p', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1380


exp1 = celldatabase.Experiment(subject, '2017-07-17', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.45,
    '1.0':2.05,
    '1.5':2.75,
    '2.0':3.45,
    '2.5':4.2,
    '3.0':5.1,
    '3.5':6.3
}

# exp1.add_site(1000, tetrodes = [2,4,7,8])
# exp1.add_session('14-16-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1050, tetrodes = [4,7,8])
# exp1.add_session('14-22-45', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes = [4,7,8])
# exp1.add_session('14-28-48', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1150, tetrodes = [4,6,7,8])
# exp1.add_session('14-34-44', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1200, tetrodes = [3,4,5,6,7,8])
# exp1.add_session('14-40-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1225, tetrodes = [2,3,4,5,6,7,8])
# exp1.add_session('14-46-07', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1250, tetrodes = [2,3,4,5,6,7,8])
# exp1.add_session('14-53-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1235, tetrodes = [2,3,4,5,6,7,8])
# exp1.add_session('14-57-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1275, tetrodes = [2,3,4,5,6,7,8])
# exp1.add_session('15-03-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes = [2,3,4,5,6,7,8])
# exp1.add_session('15-14-57', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1320, tetrodes = [2,3,4,5,6,7,8])
exp1.add_session('15-23-02', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-24-14', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-25-42', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-31-27', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('15-35-39', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('15-38-13', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('15-41-12', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('16-03-56', 'd', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1400, tetrodes = [2,5,6,7,8])
# exp1.add_session('16-24-15', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1425, tetrodes = [5,6,7,8])
# exp1.add_session('16-27-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1450, tetrodes = [5,6,7,8])
# exp1.add_session('16-31-24', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1475, tetrodes = [5,6,7,8])
# exp1.add_session('16-37-20', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1500, tetrodes = [5,6,7,8])
# exp1.add_session('16-41-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1525, tetrodes = [5,6,7,8])
# exp1.add_session('16-46-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1550, tetrodes = [5,6,7,8])
# exp1.add_session('16-51-13', None, 'laserPulse', 'am_tuning_curve')

exp1.maxDepth = 1550


# exp2 = celldatabase.Experiment(subject, '2017-07-21', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':1.75,
#     '1.0':2.8,
#     '1.5':4.0,
#     '2.0':5.5,
#     '2.5':7.8
# }
#
# #shanks bending, could not find any signals whatsoever, perhaps not in brain but other tissue?


exp3 = celldatabase.Experiment(subject, '2017-07-21', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.75,
    '1.0':2.8,
    '1.5':4.0,
    '2.0':5.5,
    '2.5':7.8
}

# exp3.add_site(950, tetrodes = [7,8])
# exp3.add_session('14-51-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes = [1,2,4,7,8])
# exp3.add_session('14-56-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('15-04-39', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('15-09-47', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1125, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('15-13-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1150, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('15-18-03', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1175, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('15-24-19', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1200, tetrodes = [2,4,6,7,8])
exp3.add_session('15-29-43', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-31-00', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-32-30', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-38-06', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('15-43-26', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-45-40', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('15-49-37', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('16-09-29', 'd', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1275, tetrodes = [1,2,4,6,7,8])
# exp3.add_session('16-19-55', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1300, tetrodes = [1,2,4,6,7,8])
exp3.add_session('16-24-40', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-25-45', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-30-03', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-35-57', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('16-42-09', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-44-50', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('16-50-13', 'g', 'bandwidth', 'bandwidth_am') #12kHz, 64Hz for TT6
exp3.add_session('17-11-10', 'h', 'bandwidth', 'bandwidth_am') #6kHz, 64Hz for TT2
exp3.add_session('17-29-48', 'i', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1300


#could not find spot to penetrate in right AC
# exp4 = celldatabase.Experiment(subject, '2017-07-23', 'left_AC', info=['lateralDiI','TT1ant','sound_right'])
# experiments.append(exp4)
#
# exp4.laserCalibration = {
#     '0.5':1.6,
#     '1.0':2.5,
#     '1.5':3.5,
#     '2.0':4.25,
#     '2.5':5.5,
#     '3.0':6.55,
#     '3.5':9.8
# }

# exp4.add_site(1350, tetrodes = [2])
# exp4.add_session('16-06-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1400, tetrodes = [2])
# exp4.add_session('16-13-13', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1450, tetrodes = [2])
# exp4.add_session('16-21-53', None, 'laserPulse', 'am_tuning_curve')
#
# exp4.add_site(1500, tetrodes = [1,2,4])
# exp4.add_session('16-28-26', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('16-29-46', None, 'noisebursts', 'am_tuning_curve')
