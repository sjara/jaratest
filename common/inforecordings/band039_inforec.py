from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band039'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-10-24', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.35,
    '2.0':2.95,
    '2.5':3.75,
    '3.0':4.2,
    '3.5':5.0
}

# exp0.add_site(900, tetrodes=[2])
# exp0.add_session('13-28-46', None, 'noisebursts', 'am_tuning_curve')
# 
# exp0.add_site(920, tetrodes=[2])
# exp0.add_session('13-34-33', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-36-08', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(940, tetrodes=[2])
# exp0.add_session('13-40-49', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-41-44', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(960, tetrodes=[2])
# exp0.add_session('13-47-22', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-48-33', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(980, tetrodes=[2])
# exp0.add_session('13-54-22', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-55-33', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1000, tetrodes=[2,4])
# exp0.add_session('13-58-44', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1020, tetrodes=[2,4])
# exp0.add_session('14-05-56', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1040, tetrodes=[2,4,6])
# exp0.add_session('14-13-30', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1060, tetrodes=[1,2,4,6])
exp0.add_session('14-17-51', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-18-48', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-20-11', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-26-13', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-30-27', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-32-33', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-35-27', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('14-54-16', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('15-05-39', 'e', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1100, tetrodes=[1,2,4,6])
# exp0.add_session('15-29-35', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1120, tetrodes=[2,4,6])
# exp0.add_session('15-36-50', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1140, tetrodes=[1,2,4,6])
# exp0.add_session('15-44-08', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1160, tetrodes=[1,2,4,6])
# exp0.add_session('15-52-53', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1180, tetrodes=[1,2,4,6,8])
# exp0.add_session('15-59-56', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1200, tetrodes=[1,2,6,8])
# exp0.add_session('16-02-42', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1220, tetrodes=[1,2,6,8])
# exp0.add_session('16-07-25', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1240, tetrodes=[1,2,4,6,8])
# exp0.add_session('16-10-23', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('16-12-05', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('16-13-59', 'f', 'tuningCurve', 'am_tuning_curve')
# exp0.add_session('16-19-57', 'g', 'AM', 'am_tuning_curve')
# exp0.add_session('16-24-51', None, 'laserPulse', 'am_tuning_curve')
# # lost the laser responsive cell!!
# 
# exp0.add_site(1230, tetrodes=[1,2,4,6])
# exp0.add_session('16-27-51', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1250, tetrodes=[1,2,6])
# exp0.add_session('16-32-18', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1260, tetrodes=[1,2,6])
# exp0.add_session('16-35-57', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1270, tetrodes=[1,2,6])
# exp0.add_session('16-42-15', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1280, tetrodes=[1,2,6])
# exp0.add_session('16-45-29', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1300, tetrodes=[1,2,6,8])
# exp0.add_session('16-50-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1320, tetrodes=[1,2,6,8])
# exp0.add_session('16-55-24', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1340, tetrodes=[1,2,6,8])
# exp0.add_session('17-00-13', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1350, tetrodes=[1,2,6,8])
# exp0.add_session('17-04-20', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-05-50', None, 'noisebursts', 'am_tuning_curve')
# 
# exp0.add_site(1360, tetrodes=[1,2])
# exp0.add_session('17-09-46', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-12-32', 'h', 'tuningCurve', 'am_tuning_curve')
# exp0.add_session('17-18-49', 'i', 'AM', 'am_tuning_curve')
# exp0.add_session('17-23-38', None, 'laserPulse', 'am_tuning_curve')
# # lost laser responsive cell AGAIN
# # I give up

exp0.maxDepth = 1360


exp1 = celldatabase.Experiment(subject, '2017-10-25', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.35,
    '1.0':1.7,
    '1.5':2.1,
    '2.0':2.6,
    '2.5':3.1,
    '3.0':3.65,
    '3.5':4.3
}

# exp1.add_site(850, tetrodes=[2,4,6,8])
# exp1.add_session('11-25-31', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(875, tetrodes=[2,4,5,6,8])
# exp1.add_session('11-46-22', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('11-47-25', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(900, tetrodes=[4,6,8])
# exp1.add_session('11-58-46', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('11-59-58', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(925, tetrodes=[2,4,5,6,8])
# exp1.add_session('12-03-15', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(950, tetrodes=[4,5,6,8])
# exp1.add_session('12-07-16', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('12-08-57', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(975, tetrodes=[2,4,5,6,8])
# exp1.add_session('12-12-41', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('12-21-03', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1000, tetrodes=[2,4,5,6,8])
# exp1.add_session('12-38-45', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1020, tetrodes=[2,4,5,6,8])
# exp1.add_session('12-53-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1040, tetrodes=[2,4,5,6,8])
# exp1.add_session('13-00-54', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1060, tetrodes=[2,4,5,6,8])
# exp1.add_session('13-09-48', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1080, tetrodes=[2,4,5,6,8])
# exp1.add_session('13-14-36', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1100, tetrodes=[2,4,5,6,8])
# exp1.add_session('13-27-05', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1120, tetrodes=[2,4,5,6,8])
# exp1.add_session('13-33-25', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1140, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-01-51', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('16-02-52', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(1160, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-14-21', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1180, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-20-27', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1200, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-25-59', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1220, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-31-28', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1240, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-36-34', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1260, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-45-09', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1280, tetrodes=[1,2,4,5,6,8])
# exp1.add_session('16-52-48', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1300, tetrodes=[2,4,5,6,8])
# exp1.add_session('16-56-24', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('16-58-31', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(1320, tetrodes=[2,4,5,6,8])
# exp1.add_session('17-03-00', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1330, tetrodes=[2,4,5,6,8])
exp1.add_session('17-08-29', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('17-11-29', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('17-13-21', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-19-18', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('17-25-07', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('17-27-30', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('17-31-37', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('17-50-56', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('18-09-24', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1330


exp2 = celldatabase.Experiment(subject, '2017-10-26', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.85,
    '2.5':3.45,
    '3.0':4.05,
    '3.5':4.7
}

# exp2.add_site(850, tetrodes=[1,2,4,6])
# exp2.add_session('11-44-28', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(900, tetrodes=[1,2,4,6,8])
# exp2.add_session('11-54-09', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('11-55-26', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(920, tetrodes=[1,2,4,6,8])
# exp2.add_session('12-00-44', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(940, tetrodes=[1,2,4,6,7,8])
exp2.add_session('12-13-50', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-15-11', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-16-51', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-23-29', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('12-28-11', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-30-17', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('12-32-49', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('12-51-20', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('13-02-43', 'e', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1000, tetrodes=[1,2,4,6,8])
# exp2.add_session('13-12-41', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1020, tetrodes=[1,2,4,6,8])
# exp2.add_session('13-18-10', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1040, tetrodes=[1,2,4,6,8])
# exp2.add_session('13-22-55', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('13-24-00', None, 'laserPulse', 'am_tuning_curve') #2.5 mW laser
# exp2.add_session('13-25-13', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1060, tetrodes=[1,2,4,6,8])
# exp2.add_session('13-30-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1080, tetrodes=[1,2,4,6,8])
# exp2.add_session('13-35-39', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1100, tetrodes=[1,2,4,6,8])
exp2.add_session('13-40-05', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-41-39', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-43-29', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-49-25', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('13-53-39', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-55-43', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-58-43', 'h', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-18-21', 'i', 'harmonics', 'bandwidth_am')
exp2.add_session('14-33-38', 'j', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1150, tetrodes=[1,2,4,6,8])
# exp2.add_session('14-55-21', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1160, tetrodes=[1,2,4,6,8])
# exp2.add_session('14-59-58', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('15-02-04', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1180, tetrodes=[1,2,4,6,8])
# exp2.add_session('15-13-47', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-15-00', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1200, tetrodes=[1,2,4,6,8])
# exp2.add_session('15-33-30', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('15-35-55', 'k', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('15-41-27', 'l', 'AM', 'am_tuning_curve')
# exp2.add_session('15-45-39', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('15-48-09', None, 'laserTrain', 'am_tuning_curve')
# # honestly a pretty shitty laser response
# 
# exp2.add_site(1220, tetrodes=[1,2,4,6,8])
# exp2.add_session('15-53-35', None, 'laserPulse', 'am_tuning_curve')

exp2.maxDepth = 1220


exp3 = celldatabase.Experiment(subject, '2017-10-31', 'left_AC', info=['mediallDiI','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.35,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.7,
    '2.5':3.3,
    '3.0':3.8,
    '3.5':4.45
}

exp3.add_site(850, tetrodes=[2,4,7,8])
exp3.add_session('13-04-30', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-05-32', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-07-19', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-09-15', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-16-08', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('13-20-36', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-22-52', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-25-31', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('13-46-28', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('13-57-40', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(900, tetrodes=[2,4,7,8])
# exp3.add_session('14-16-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(925, tetrodes=[2,4,7,8])
# exp3.add_session('14-22-24', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(950, tetrodes=[2,4,7,8])
exp3.add_session('14-28-25', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-29-33', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-30-31', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-36-25', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('14-40-39', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-42-48', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-46-41', 'h', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-05-25', 'i', 'harmonics', 'bandwidth_am')
exp3.add_session('15-16-44', 'j', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1000, tetrodes=[1,2,4])
# exp3.add_session('15-31-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1020, tetrodes=[1,2,4])
# exp3.add_session('15-38-50', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1040, tetrodes=[1,2,4])
# exp3.add_session('15-45-13', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1050, tetrodes=[1,2,4])
# exp3.add_session('15-49-48', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1075, tetrodes=[1,2,4,8])
exp3.add_session('15-55-52', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('15-56-57', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-02-24', 'l', 'AM', 'am_tuning_curve')
exp3.add_session('16-07-21', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('16-09-52', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('16-14-19', 'm', 'bandwidth', 'bandwidth_am')
exp3.add_session('16-33-22', 'n', 'harmonics', 'bandwidth_am')
exp3.add_session('16-44-43', 'o', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1150, tetrodes=[1,2,4,7,8])
# exp3.add_session('16-56-49', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('16-58-20', None, 'noisebursts', 'am_tuning_curve')
# 
# exp3.add_site(1160, tetrodes=[2,4])
# exp3.add_session('17-02-45', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('17-03-47', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1170, tetrodes=[2,4])
# exp3.add_session('17-07-35', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('17-08-44', 'p', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('17-15-21', None, 'noisebursts', 'am_tuning_curve')
# # amazing SOM cell completely unresponsive to sound...

exp3.maxDepth = 1170


exp4 = celldatabase.Experiment(subject, '2017-11-02', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.3,
    '2.0':2.85,
    '2.5':3.4,
    '3.0':4.0,
    '3.5':4.6
}

# exp4.add_site(920, tetrodes=[2,8])
# exp4.add_session('12-05-55', None, 'noisebursts', 'am_tuning_curve')
# 
# exp4.add_site(975, tetrodes=[2,8])
# exp4.add_session('12-18-09', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1000, tetrodes=[2,8])
exp4.add_session('12-25-13', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-26-19', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-28-26', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-33-56', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('12-38-10', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-40-17', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('12-43-07', 'c', 'bandwidth', 'bandwidth_am')
exp4.add_session('13-02-14', 'd', 'harmonics', 'bandwidth_am')
exp4.add_session('13-13-52', 'e', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1050, tetrodes=[2,6,8])
# exp4.add_session('13-24-54', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1060, tetrodes=[2,6,7,8])
# exp4.add_session('13-28-43', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1080, tetrodes=[2,4,6,7,8])
# exp4.add_session('13-32-35', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1100, tetrodes=[2,4,6,7,8])
exp4.add_session('13-37-45', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-38-59', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-40-03', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-47-36', 'g', 'AM', 'am_tuning_curve')
exp4.add_session('13-52-27', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('13-54-44', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('13-57-06', 'h', 'bandwidth', 'bandwidth_am')
exp4.add_session('14-15-46', 'i', 'harmonics', 'bandwidth_am')
exp4.add_session('14-27-21', 'j', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1125, tetrodes=[2,4,6,8])
# exp4.add_session('14-37-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1150, tetrodes=[2,4,6,7,8])
# exp4.add_session('14-43-43', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1175, tetrodes=[2,4,6,7,8])
# exp4.add_session('14-48-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1200, tetrodes=[2,4,6,7,8])
# exp4.add_session('14-54-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1220, tetrodes=[2,4,6,7,8])
# exp4.add_session('14-58-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1230, tetrodes=[2,4,6,7,8])
# exp4.add_session('15-01-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1240, tetrodes=[2,4,6,7,8])
# exp4.add_session('15-05-10', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1260, tetrodes=[2,4,6,7,8])
# exp4.add_session('15-08-42', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1280, tetrodes=[1,2,4,6,7,8])
# exp4.add_session('15-12-49', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1300, tetrodes=[1,2,4,6,7,8])
# exp4.add_session('15-16-58', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('15-18-34', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('15-21-59', 'k', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('15-27-27', 'l', 'AM', 'am_tuning_curve')
# exp4.add_session('15-31-41', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('15-33-47', None, 'laserTrain', 'am_tuning_curve')
# 
# exp4.add_site(1320, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('15-40-46', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1340, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('15-45-05', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1350, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('15-48-56', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1360, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('15-53-00', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-55-49', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-06-29', 'm', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-11-58', 'n', 'AM', 'am_tuning_curve')
exp4.add_session('16-16-15', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-18-30', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('16-20-57', 'o', 'bandwidth', 'bandwidth_am')
exp4.add_session('16-40-18', 'p', 'harmonics', 'bandwidth_am')
exp4.add_session('16-57-03', 'q', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1360


exp5 = celldatabase.Experiment(subject, '2017-11-03', 'left_AC', info=['lateralDiI','TT1ant','sound_right'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.4,
    '2.0':2.95,
    '2.5':3.6,
    '3.0':4.15,
    '3.5':4.9
}

# exp5.add_site(950, tetrodes=[2,4,6,8])
# exp5.add_session('13-19-57', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('13-21-14', None, 'noisebursts', 'am_tuning_curve')
# 
# exp5.add_site(980, tetrodes=[2,4,6,7,8])
# exp5.add_session('13-28-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1000, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('13-34-59', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1020, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('13-40-16', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1040, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('13-46-07', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1060, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('13-50-48', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1080, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('13-55-28', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1100, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('14-00-25', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1120, tetrodes=[1,2,4,6,7,8])
exp5.add_session('14-06-38', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-08-29', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-10-27', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-16-00', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('14-20-22', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-23-28', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('14-25-45', 'c', 'bandwidth', 'bandwidth_am')
exp5.add_session('14-44-08', 'd', 'harmonics', 'bandwidth_am')
exp5.add_session('14-55-21', 'e', 'noiseAmps', 'am_tuning_curve')

# exp5.add_site(1150, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('15-03-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1175, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('15-06-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1200, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('15-09-56', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1220, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('15-15-18', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1240, tetrodes=[1,2,4,6,7,8])
# exp5.add_session('15-19-11', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(1260, tetrodes=[1,2,4,6,7,8])
exp5.add_session('15-23-13', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('15-24-36', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-26-06', 'f', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-31-34', 'g', 'AM', 'am_tuning_curve')
exp5.add_session('15-35-48', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('15-37-54', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('15-40-23', 'h', 'bandwidth', 'bandwidth_am')
exp5.add_session('15-59-25', 'i', 'harmonics', 'bandwidth_am')
exp5.add_session('16-11-20', 'j', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1260
