from jaratoolbox import celldatabase

subject = 'band034'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2017-08-30', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
# experiments.append(exp0)
#
# exp0.laserCalibration = {
#     '0.5':1.5,
#     '1.0':2.1,
#     '1.5':2.85,
#     '2.0':3.6,
#     '2.5':4.35,
#     '3.0':5.4,
#     '3.5':6.4
# }

# exp0.add_site(950, tetrodes=[2,4,8])
# exp0.add_session('16-02-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1000, tetrodes=[2,4])
# exp0.add_session('16-09-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[2,4])
# exp0.add_session('16-22-19', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1075, tetrodes=[2,3,4])
# exp0.add_session('16-25-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[2,3,4])
# exp0.add_session('16-32-32', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('16-34-00', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('16-37-17', 'a', 'tuningCurve', 'am_tuning_curve') #just recording from TT2 cells even though no laser response
# # don't really have good tuning
#
# exp0.add_site(1150, tetrodes=[2,3,4])
# exp0.add_session('16-59-31', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('17-00-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes=[1,2,4,6])
# exp0.add_session('17-06-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1250, tetrodes=[1,2,4,6,8])
# exp0.add_session('17-13-27', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1275, tetrodes=[1,2,3,4,7])
# exp0.add_session('17-18-55', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1300, tetrodes=[1,2,4,8])
# exp0.add_session('17-24-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1325, tetrodes=[1,2,4])
# exp0.add_session('17-29-49', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-31-21', None, 'noisebursts', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-09-01', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.7,
    '1.0':2.65,
    '1.5':3.7,
    '2.0':4.8,
    '2.5':6.1,
    '3.0':7.9
}

# exp1.add_site(900, tetrodes=[2,4,6])
# exp1.add_session('11-09-57', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(950, tetrodes=[2,4,6])
# exp1.add_session('11-16-29', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('11-17-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1000, tetrodes=[2,4,6,7])
# exp1.add_session('11-26-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1025, tetrodes=[2,4,6])
# exp1.add_session('11-31-18', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1050, tetrodes=[2,4,5,6])
# exp1.add_session('11-38-02', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[2,4,5,6])
# exp1.add_session('11-41-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1125, tetrodes=[1,2,3,4,5,6])
# exp1.add_session('11-50-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1150, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('12-01-22', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1175, tetrodes=[1,2,4,5,6,8])
exp1.add_session('12-07-15', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-08-58', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-11-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-16-44', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-20-59', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-23-22', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-27-07', 'c', 'bandwidth', 'bandwidth_am') #5.5kHz for SOM cell
exp1.add_session('12-45-42', 'd', 'bandwidth', 'bandwidth_am') #18kHz for decent TT4 cell
exp1.add_session('13-04-12', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[2,4,5,6])
exp1.add_session('13-15-05', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-16-30', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-19-32', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-27-42', 'g', 'AM', 'am_tuning_curve')
exp1.add_session('13-32-04', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-34-09', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-37-22', 'h', 'bandwidth', 'bandwidth_am')
exp1.add_session('13-56-00', 'i', 'noiseAmps', 'am_tuning_curve')
# withdrawing from this site as I don't seem to be getting very good sound responses

exp1.maxDepth = 1250


exp2 = celldatabase.Experiment(subject, '2017-09-01', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.7,
    '1.0':2.65,
    '1.5':3.7,
    '2.0':4.8,
    '2.5':6.1,
    '3.0':7.9
}

# exp2.add_site(1000, tetrodes=[2,4])
# exp2.add_session('14-33-58', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-35-37', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1025, tetrodes=[2,4,6])
# exp2.add_session('14-39-09', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('14-40-26', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1050, tetrodes=[2,4,6])
exp2.add_session('14-44-35', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-45-55', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-47-30', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-55-46', 'k', 'AM', 'am_tuning_curve')
exp2.add_session('15-00-37', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-02-57', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-07-00', 'l', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-25-30', 'm', 'harmonics', 'bandwidth_am')
exp2.add_session('15-38-59', 'n', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1100, tetrodes=[1,2,3,4,6])
# exp2.add_session('15-51-46', None, 'laserPulse', 'am_tuning_curve')
#
# exp2.add_site(1150, tetrodes=[1,2,3,4,5,6])
# exp2.add_session('15-56-52', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1175, tetrodes=[1,2,3,4,6])
exp2.add_session('16-05-30', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-06-52', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-09-18', 'o', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-17-41', 'p', 'AM', 'am_tuning_curve')
exp2.add_session('16-21-57', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-24-14', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-27-14', 'q', 'bandwidth', 'bandwidth_am')
exp2.add_session('16-46-09', 'r', 'harmonics', 'bandwidth_am')
exp2.add_session('17-00-51', 's', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1175
