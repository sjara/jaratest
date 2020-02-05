from jaratoolbox import celldatabase

subject = 'band005'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2016-09-16', 'left_AC',info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.7,
    '1.0':1.15,
    '1.5':1.6,
    '2.0':2.1,
    '2.5':2.65,
    '3.0':3.35,
    '3.5':4.1
}

# exp0.add_site(1037, tetrodes=[2])
# exp0.add_session('12-14-13', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-17-37', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-20-17', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-22-56', None, 'laserTrain', 'am_tuning_curve')
# exp0.add_session('12-25-50', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(1140, tetrodes=[2,4,6])
exp0.add_session('12-54-16', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-56-52', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-00-40', 'b', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-13-32', 'c', 'AM', 'am_tuning_curve')
exp0.add_session('13-19-50', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-22-36', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-25-23', 'd', 'bandwidth', 'bandwidth_am')

exp0.add_site(1270, tetrodes=[1,2,4,6])
exp0.add_session('13-53-37', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-57-34', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-00-49', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-14-35', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('14-21-52', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-25-43', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-29-09', 'g', 'bandwidth', 'bandwidth_am')

exp0.add_site(1310, tetrodes=[1,2,3,4,6])
exp0.add_session('14-59-37', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-02-11', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-05-28', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-16-14', 'i', 'AM', 'am_tuning_curve')
exp0.add_session('15-22-46', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-25-27', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-27-50', 'j', 'bandwidth', 'bandwidth_am')

exp0.maxDepth = 1310


# exp1 = celldatabase.Experiment(subject, '2016-09-20', 'left_AC',info=['middleDiI','TT1ant','sound_left'])
# experiments.append(exp1)
#
# exp1.laserCalibration = {
#     '0.5':0.65,
#     '1.0':1.0,
#     '1.5':1.35,
#     '2.0':1.75,
#     '2.5':2.2,
#     '3.0':2.7,
#     '3.5':3.35
# }
#
# exp2 = celldatabase.Experiment(subject, '2016-09-21', 'left_AC', info=['middleDiI','TT1ant','sound_left'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '0.5':0.8,
#     '1.0':1.4,
#     '1.5':2.05,
#     '2.0':2.75,
#     '2.5':3.75,
#     '3.0':4.65,
#     '3.5':5.5
# }
