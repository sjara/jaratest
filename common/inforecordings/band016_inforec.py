from jaratoolbox import celldatabase

subject = 'band016'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2016-12-11', 'left_AC', info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.65,
    '1.0':0.9,
    '1.5':1.25,
    '2.0':1.55,
    '2.5':1.95,
    '3.0':2.35,
    '3.5':2.75
}

exp0.add_site(850, tetrodes = [2,6])
exp0.add_session('13-45-58', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-47-57', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-51-30', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-02-27', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-08-29', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-11-00', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-13-19', 'c', 'bandwidth', 'bandwidth_am')

# exp0.add_site(900, tetrodes = [2,3,4,6])
# exp0.add_session('14-35-05', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(950, tetrodes = [2,3,4,5,6])
exp0.add_session('14-41-15', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-43-59', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-46-15', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-57-01', 'e', 'AM', 'am_tuning_curve')
exp0.add_session('15-02-44', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-05-00', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-07-28', 'f', 'bandwidth', 'bandwidth_am')

# exp0.add_site(1000, tetrodes = [2,6])
# exp0.add_session('15-34-22', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes = [2,5,6])
# exp0.add_session('15-44-12', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1075, tetrodes = [2,4,5,6])
# exp0.add_session('15-50-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1275, tetrodes = [2,4,5,6])
# exp0.add_session('16-01-32', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1325, tetrodes = [2,3,4,5,6])
exp0.add_session('16-05-56', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-08-38', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-11-07', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-14-26', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-25-18', 'h', 'AM', 'am_tuning_curve')
exp0.add_session('16-30-42', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('16-34-10', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('16-36-21', 'i', 'bandwidth', 'bandwidth_am')

exp0.maxDepth = 1325


exp1 = celldatabase.Experiment(subject, '2016-12-12', 'right_AC', info=['middleDiI','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.35,
    '2.0':1.85,
    '2.5':2.3,
    '3.0':2.7,
    '3.5':3.45
}

# exp1.add_site(690, tetrodes = [2,4,5,6])
# exp1.add_session('11-55-58', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(720, tetrodes = [2,6])
# exp1.add_session('12-00-07', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(850, tetrodes = [2,4,6])
# exp1.add_session('12-30-44', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(910, tetrodes = [2,4,6])
exp1.add_session('12-43-17', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-44-49', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-46-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-57-37', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-02-26', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-04-39', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-07-02', 'c', 'bandwidth', 'bandwidth_am')

exp1.maxDepth = 910


# exp2 = celldatabase.Experiment(subject, '2016-12-22','AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':0.7,
#     '1.0':1.05,
#     '1.5':1.45,
#     '2.0':1.85,
#     '2.5':2.3,
#     '3.0':2.75,
#     '3.5':3.25
# }

#exp2.add_site(500, tetrodes = [2,4])
#exp2.add_session('14-05-04', None, 'noisebursts', 'am_tuning_curve')

# exp2.add_site(600, tetrodes = [2,4,6,8])
# exp2.add_session('14-14-06', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(640, tetrodes = [2,4,6,8])
# exp2.add_session('14-20-17', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-21-49', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(700, tetrodes = [1,2,4,5,6,8])
# exp2.add_session('14-29-31', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-30-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(760, tetrodes = [2,4,6,8])
# exp2.add_session('14-37-22', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-38-59', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(820, tetrodes = [1,2,4,5,6,8])
# exp2.add_session('14-46-37', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-48-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(860, tetrodes = [1,2,3,4,5,6,8])
# exp2.add_session('14-55-36', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-57-42', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('15-00-57', 'a', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('15-12-18', 'b', 'AM', 'am_tuning_curve')
#
# exp2.add_site(930, tetrodes = [3,5,7,8])
# exp2.add_session('15-24-02', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-25-47', None, 'laserPulse', 'am_tuning_curve')
