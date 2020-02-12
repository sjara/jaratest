from jaratoolbox import celldatabase

subject = 'band033'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-07-27', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':2.3,
    '1.0':3.9,
    '1.5':6.4,
    '2.0':10.0
} #looks like I got quite a bit of dye on the fiber

# exp0.add_site(1400, tetrodes=[2,4,6,8])
# exp0.add_session('13-28-16', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('13-29-46', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1425, tetrodes=[2,4,6,8])
# exp0.add_session('13-34-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1450, tetrodes=[4,8])
# exp0.add_session('13-37-09', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('13-38-23', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1475, tetrodes=[1,2,8])
# exp0.add_session('13-45-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1500, tetrodes=[1,2,6,8])
# exp0.add_session('13-50-34', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1525, tetrodes=[1,2,8])
# exp0.add_session('13-55-40', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1550, tetrodes=[2,6,8])
# exp0.add_session('14-18-42', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1575, tetrodes=[2,3,8])
# exp0.add_session('14-24-16', None, 'laserPulse', 'am_tuning_curve')
#
# exp0.add_site(1600, tetrodes=[2,3,8])
# exp0.add_session('14-30-28', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1625, tetrodes=[1,2,3,4,7,8])
exp0.add_session('14-37-01', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-38-32', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-40-31', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-47-32', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-51-53', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-53-56', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-57-25', 'c', 'bandwidth', 'bandwidth_am') #18kHz, 8Hz
exp0.add_session('15-15-52', 'd', 'bandwidth', 'bandwidth_am') #12khz, 8Hz
exp0.add_session('15-34-14', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1700, tetrodes=[1,2,4,7,8])
exp0.add_session('15-44-31', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-46-04', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-47-33', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-53-01', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('15-57-14', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-59-20', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('16-03-16', 'h', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-22-22', 'i', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1700


exp1 = celldatabase.Experiment(subject, '2017-08-02', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.5,
    '1.0':2.15,
    '1.5':3.0,
    '2.0':3.7,
    '2.5':4.6,
    '3.0':5.7,
    '3.5':6.7
}

# exp1.add_site(1200, tetrodes=[1,2,3,4,6,8])
# exp1.add_session('11-55-38', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('11-57-24', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
# exp1.add_session('12-05-42', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1260, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('12-11-37', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-13-01', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-15-48', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-21-16', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-25-30', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-27-34', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-31-16', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('12-50-42', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('12-57-34', 'e', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1300, tetrodes=[1,2,3,4,5,6,7,8])
# exp1.add_session('13-08-44', None, 'laserPulse', 'am_tuning_curve')

# exp1.add_site(1325, tetrodes=[1,2,3,4,5,6,7,8])
# exp1.add_session('13-14-19', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('13-15-41', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-18-51', 'f', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('13-24-19', 'g', 'AM', 'am_tuning_curve')
# exp1.add_session('13-28-34', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('13-30-39', None, 'laserTrain', 'am_tuning_curve')
# # lost laser responsive cell. Recordings really noisy as well due to lack of ground

exp1.add_site(1350, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-38-15', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-39-31', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-41-51', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-47-41', 'i', 'AM', 'am_tuning_curve')
exp1.add_session('13-52-20', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-55-39', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('14-00-27', 'j', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-18-58', 'k', 'harmonics', 'bandwidth_am') #18kHz center frequency
exp1.add_session('14-40-59', 'l', 'noiseAmps', 'am_tuning_curve')
exp1.add_session('14-46-47', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-00-45', 'm', 'harmonics', 'bandwidth_am') #22kHz center frequency


# exp1.add_site(1400, tetrodes=[1,2,3,4,5,6,8])
# exp1.add_session('15-32-09', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1425, tetrodes=[1,2,3,4,5,6,8])
# exp1.add_session('15-42-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1450, tetrodes=[1,2,3,4,5,6,8])
# exp1.add_session('15-51-12', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1475, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('15-55-21', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1500, tetrodes=[1,2,3,4,5,6,7])
# exp1.add_session('15-59-30', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1525, tetrodes=[1,2,3,4,5,6,7])
# exp1.add_session('16-05-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1550, tetrodes=[1,2,3,4,5,6,7])
# exp1.add_session('16-09-11', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1575, tetrodes=[1,2,3,4,5,6,7])
# exp1.add_session('16-15-33', None, 'laserPulse', 'am_tuning_curve')
#
# exp1.add_site(1600, tetrodes=[1,2,3,4,5,6,7])
# exp1.add_session('16-22-06', None, 'laserPulse', 'am_tuning_curve')

exp1.maxDepth = 1600


exp2 = celldatabase.Experiment(subject, '2017-08-10', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.65,
    '1.0':2.6,
    '1.5':3.65,
    '2.0':4.7,
    '2.5':6.1,
    '3.0':8.0
}

# exp2.add_site(1150, tetrodes=[1,2,3,4,8])
# exp2.add_session('12-30-53', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1200, tetrodes=[1,2,3,4,6,8])
exp2.add_session('12-45-10', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-46-55', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-48-50', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-54-26', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('12-58-41', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-00-47', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-06-58', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('13-28-44', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('13-40-04', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1250, tetrodes=[1,2,3,4,5,7,8])
exp2.add_session('13-48-34', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-49-50', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-50-53', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-56-50', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('14-01-03', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-03-20', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('14-06-33', 'h', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-26-08', 'i', 'harmonics', 'bandwidth_am')
exp2.add_session('14-37-11', 'j', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1300, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-46-33', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('14-47-54', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-49-41', 'k', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-55-14', 'l', 'AM', 'am_tuning_curve')
exp2.add_session('14-59-35', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-01-50', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-05-21', 'm', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-26-38', 'n', 'harmonics', 'bandwidth_am')
exp2.add_session('15-37-46', 'o', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1350, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('15-54-55', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-57-34', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-02-08', 'p', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-08-47', 'q', 'AM', 'am_tuning_curve')
exp2.add_session('16-13-03', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-15-14', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-18-42', 'r', 'bandwidth', 'bandwidth_am') #10kHz, 64Hz for TT6
exp2.add_session('16-37-45', 's', 'bandwidth', 'bandwidth_am') #18kHz, 64Hz for TT8
exp2.add_session('16-56-59', 't', 'harmonics', 'bandwidth_am') #10kHz
exp2.add_session('17-08-32', 'u', 'harmonics', 'bandwidth_am') #18kHz
exp2.add_session('17-19-37', 'v', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1350


exp3 = celldatabase.Experiment(subject, '2017-08-11', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.6,
    '1.0':2.35,
    '1.5':3.25,
    '2.0':4.15,
    '2.5':5.1,
    '3.0':6.2,
    '3.5':7.9
}

# exp3.add_site(900, tetrodes=[1,2,5,6,7,8])
# exp3.add_session('11-49-56', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(950, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('11-54-54', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(975, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('11-57-48', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
# exp3.add_session('12-01-04', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1025, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('12-04-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('12-07-31', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1075, tetrodes=[1,2,4,6,8])
# exp3.add_session('12-09-47', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,4,6,8])
exp3.add_session('12-21-39', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-22-45', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-25-01', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-30-38', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-34-52', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-36-56', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-41-03', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-03-15', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-14-18', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1150, tetrodes=[1,2,6,8])
# exp3.add_session('13-23-41', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1175, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('13-28-10', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('13-34-32', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1225, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('13-40-00', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('13-41-11', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes=[1,2,4,5,6,8])
# exp3.add_session('13-46-38', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1275, tetrodes=[1,2,4,6,8])
# exp3.add_session('13-50-17', None, 'laserPulse', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[1,2,3,4,6,8])
# exp3.add_session('13-54-05', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('13-55-13', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('13-56-04', 'f', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('14-01-31', 'g', 'AM', 'am_tuning_curve')
# exp3.add_session('14-05-44', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('14-07-48', None, 'laserTrain', 'am_tuning_curve')

exp3.maxDepth = 1300
