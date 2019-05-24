from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band040'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-11-07', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.35,
    '1.0':1.7,
    '1.5':2.2,
    '2.0':2.65,
    '2.5':3.2,
    '3.0':3.75,
    '3.5':4.35
}

# exp0.add_site(800, tetrodes=[2,4])
# exp0.add_session('12-38-39', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('12-39-50', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(825, tetrodes=[2,4])
# exp0.add_session('12-50-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(850, tetrodes=[2,4,7])
# exp0.add_session('12-56-35', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(875, tetrodes=[2,4,6,8])
# exp0.add_session('13-01-15', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(900, tetrodes=[2,4,5,6,7,8])
exp0.add_session('13-07-26', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-08-19', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-09-37', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-15-08', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-19-22', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-21-26', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('13-23-32', 'c', 'bandwidth', 'bandwidth_am')
exp0.add_session('13-42-00', 'd', 'harmonics', 'bandwidth_am')
exp0.add_session('13-53-30', 'e', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(950, tetrodes=[1,2,4,6,7,8])
# exp0.add_session('14-04-42', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(975, tetrodes=[1,2,4,6,8])
# exp0.add_session('14-13-28', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1000, tetrodes=[2,4,6,8])
# exp0.add_session('14-19-04', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1020, tetrodes=[2,4,6,8])
# exp0.add_session('14-23-35', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1040, tetrodes=[2,4,6,8])
# exp0.add_session('14-28-34', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1060, tetrodes=[1,2,4,6,8])
# exp0.add_session('14-33-09', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1080, tetrodes=[1,2,4,6,8])
# exp0.add_session('14-36-20', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('14-46-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1100, tetrodes=[1,2])
# exp0.add_session('15-00-31', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1120, tetrodes=[2])
exp0.add_session('15-22-46', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-24-55', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-27-35', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-35-17', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('15-39-32', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-42-08', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('15-44-08', 'g', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-07-52', 'h', 'harmonics', 'bandwidth_am')
exp0.add_session('16-37-19', 'i', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1175, tetrodes=[2,4])
# exp0.add_session('16-59-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1185, tetrodes=[2])
# exp0.add_session('17-13-52', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1200, tetrodes=[2,4,6])
# exp0.add_session('17-19-06', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-20-15', None, 'noisebursts', 'am_tuning_curve')
# 
# exp0.add_site(1210, tetrodes=[2,4,6])
# exp0.add_session('17-32-03', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-34-36', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1220, tetrodes=[2,4])
# exp0.add_session('17-39-59', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('17-43-15', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1250, tetrodes=[2,4])
# exp0.add_session('17-50-45', None, 'laserPulse', 'am_tuning_curve')

exp0.maxDepth = 1250


exp1 = celldatabase.Experiment(subject, '2017-11-09', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.7,
    '2.5':3.35,
    '3.0':3.9,
    '3.5':4.6
}

# exp1.add_site(850, tetrodes=[2])
# exp1.add_session('12-15-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(900, tetrodes=[2,6])
# exp1.add_session('12-24-49', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(950, tetrodes=[2])
# exp1.add_session('12-34-43', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('12-35-44', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(1000, tetrodes=[2])
# exp1.add_session('12-44-11', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('12-45-32', None, 'laserPulse', 'am_tuning_curve')

'''exp1.add_site(1020, tetrodes=[2])
exp1.add_session('12-53-04', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-54-32', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-56-07', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-01-59', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-07-11', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-09-26', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('13-11-48', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('13-31-07', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('13-42-20', 'e', 'noiseAmps', 'am_tuning_curve')''' # did not turn off sound presentation in time, fix later

# exp1.add_site(1080, tetrodes=[2])
# exp1.add_session('13-54-44', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1100, tetrodes=[2])
# exp1.add_session('13-59-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1120, tetrodes=[2])
# exp1.add_session('14-08-27', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1140, tetrodes=[2])
# exp1.add_session('14-27-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1160, tetrodes=[2])
# exp1.add_session('14-34-40', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1180, tetrodes=[2])
# exp1.add_session('14-42-39', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1200, tetrodes=[2])
# exp1.add_session('14-56-45', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1220, tetrodes=[2])
# exp1.add_session('15-06-42', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1240, tetrodes=[2])
# exp1.add_session('15-14-21', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1260, tetrodes=[2])
# exp1.add_session('15-19-49', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1280, tetrodes=[2])
# exp1.add_session('15-24-38', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1300, tetrodes=[2])
# exp1.add_session('15-30-14', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('15-31-17', None, 'noisebursts', 'am_tuning_curve')

exp1.maxDepth = 1300


exp2 = celldatabase.Experiment(subject, '2017-11-10', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.35,
    '2.0':2.95,
    '2.5':3.55,
    '3.0':4.2,
    '3.5':4.9
}

# exp2.add_site(750, tetrodes=[2,4,8])
# exp2.add_session('12-39-45', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-40-46', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(775, tetrodes=[2,4,8])
# exp2.add_session('12-51-35', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(800, tetrodes=[2,4,8])
# exp2.add_session('12-54-11', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('12-56-01', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(825, tetrodes=[2,4,8])
# exp2.add_session('13-06-16', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('13-07-31', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(850, tetrodes=[2,4,8])
# exp2.add_session('13-18-48', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-19-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(875, tetrodes=[2,4,8])
# exp2.add_session('13-25-33', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(900, tetrodes=[1,2,4,8])
# exp2.add_session('13-31-42', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(920, tetrodes=[2,4,8])
# exp2.add_session('13-36-54', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(940, tetrodes=[2,4,8])
exp2.add_session('13-40-11', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-41-10', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-42-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-48-40', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('13-53-06', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-55-20', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-58-21', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-20-58', 'd', 'harmonics', 'bandwidth_am')
exp2.add_session('14-32-08', 'e', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1000, tetrodes=[2,4,8])
# exp2.add_session('14-42-55', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1020, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-53-16', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1040, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-59-18', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1060, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('15-03-10', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1080, tetrodes=[1,2,4,6,7,8])
# exp2.add_session('15-07-18', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('15-13-19', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-15-05', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-20-53', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('15-25-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('15-27-28', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('15-31-07', 'h', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-49-40', 'i', 'harmonics', 'bandwidth_am')
exp2.add_session('16-00-58', 'j', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('16-11-36', None, 'laserPulse', 'am_tuning_curve')
# 
# exp2.add_site(1175, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('16-18-47', None, 'laserPulse', 'am_tuning_curve')

exp2.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('16-26-12', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-27-36', 'k', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-33-32', 'l', 'AM', 'am_tuning_curve')
exp2.add_session('16-37-48', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('16-39-56', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('16-43-32', 'm', 'bandwidth', 'bandwidth_am')
exp2.add_session('17-03-47', 'n', 'harmonics', 'bandwidth_am')
exp2.add_session('17-14-52', 'o', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1200


exp3 = celldatabase.Experiment(subject, '2017-11-13', 'left_AC', info=['medialDiD','TT1ant','sound_right'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.2,
    '2.0':2.75,
    '2.5':3.35,
    '3.0':3.95,
    '3.5':4.6
}

# exp3.add_site(950, tetrodes=[1,2])
# exp3.add_session('14-10-36', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('14-12-23', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1000, tetrodes=[1,2])
# exp3.add_session('14-25-18', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1025, tetrodes=[1,2])
# exp3.add_session('14-36-02', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(1050, tetrodes=[1,2])
exp3.add_session('14-40-19', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-41-35', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-42-52', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-54-10', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-56-25', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-59-02', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('15-06-06', 'c', 'bandwidth', 'bandwidth_am')
exp3.add_session('15-25-10', 'd', 'harmonics', 'bandwidth_am')
exp3.add_session('15-36-31', 'e', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1100, tetrodes=[1,2])
# exp3.add_session('15-46-08', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1125, tetrodes=[1,2])
# exp3.add_session('15-52-21', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1150, tetrodes=[1,2])
# exp3.add_session('15-57-24', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1175, tetrodes=[1,2])
# exp3.add_session('16-02-39', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1200, tetrodes=[1,2])
# exp3.add_session('16-07-44', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1225, tetrodes=[1,2])
# exp3.add_session('16-12-26', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1250, tetrodes=[1,2])
# exp3.add_session('16-21-08', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1275, tetrodes=[1,2])
# exp3.add_session('16-31-00', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1300, tetrodes=[1,2])
# exp3.add_session('16-34-54', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1325, tetrodes=[1,2])
# exp3.add_session('16-37-50', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1350, tetrodes=[1,2])
# exp3.add_session('16-41-56', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1375, tetrodes=[1,2])
# exp3.add_session('16-46-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1400, tetrodes=[1,2])
# exp3.add_session('16-50-44', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1425, tetrodes=[1,2])
# exp3.add_session('16-57-23', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1450, tetrodes=[1,2])
# exp3.add_session('17-02-00', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1475, tetrodes=[1,2,4])
# exp3.add_session('17-07-05', None, 'laserPulse', 'am_tuning_curve')
# 
# exp3.add_site(1500, tetrodes=[1,2,4])
# exp3.add_session('17-10-58', None, 'laserPulse', 'am_tuning_curve')
# exp3.add_session('17-16-17', None, 'laserPulse', 'am_tuning_curve')

exp3.maxDepth = 1500


exp4 = celldatabase.Experiment(subject, '2017-11-14', 'left_AC', info=['middleDiI','TT1ant','sound_right'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.4,
    '2.0':2.95,
    '2.5':3.55,
    '3.0':4.15,
    '3.5':4.9
}

# exp4.add_site(800, tetrodes=[1,2,4,6,8])
# exp4.add_session('12-46-50', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('12-50-07', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-51-33', 'a', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('12-57-27', 'b', 'AM', 'am_tuning_curve')
# exp4.add_session('13-01-53', None, 'laserPulse', 'am_tuning_curve') #2.5 mW laser
# exp4.add_session('13-04-09', None, 'laserTrain', 'am_tuning_curve')
# # not that great laser response, sketchy tuning

# exp4.add_site(825, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-11-02', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(850, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-15-24', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(875, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-20-36', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(900, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-24-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(925, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-27-57', None, 'laserPulse', 'am_tuning_curve')

# exp4.add_site(950, tetrodes=[1,2,4,6,8])
# exp4.add_session('13-31-37', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('13-32-23', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-33-43', 'c', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('13-40-34', 'd', 'AM', 'am_tuning_curve')
# exp4.add_session('13-44-49', None, 'laserPulse', 'am_tuning_curve')
# # LASER RESPONSIVE CELL IS GONE REEEEEEE
# 
# exp4.add_site(980, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('13-52-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1000, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('13-56-40', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1020, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('14-03-13', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1040, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('14-07-30', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1050, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('14-13-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1060, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('14-18-16', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1070, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('14-24-46', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1080, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('14-29-50', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1090, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('14-34-32', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1100, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('14-48-35', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('14-49-56', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-51-40', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-59-53', 'f', 'AM', 'am_tuning_curve')
exp4.add_session('15-04-38', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('15-07-00', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('15-12-05', 'g', 'bandwidth', 'bandwidth_am')
exp4.add_session('15-30-32', 'h', 'harmonics', 'bandwidth_am')
exp4.add_session('15-41-44', 'i', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1120, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('15-59-14', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1140, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('16-10-15', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1160, tetrodes=[1,2,4,5,6,7,8])
# exp4.add_session('16-18-08', None, 'laserPulse', 'am_tuning_curve')

exp4.add_site(1180, tetrodes=[1,2,4,5,6,8])
exp4.add_session('16-22-58', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-24-56', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-26-37', 'j', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-33-11', 'k', 'AM', 'am_tuning_curve')
exp4.add_session('16-37-34', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('16-40-11', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('16-46-10', 'l', 'bandwidth', 'bandwidth_am')
exp4.add_session('17-05-47', 'm', 'harmonics', 'bandwidth_am')
exp4.add_session('17-17-44', 'n', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1200, tetrodes=[1,2,4,6,8])
# exp4.add_session('17-26-18', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1220, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('17-31-36', None, 'laserPulse', 'am_tuning_curve')
# 
# exp4.add_site(1230, tetrodes=[1,2,4,5,6,8])
# exp4.add_session('17-35-30', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('17-36-32', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('17-38-09', 'o', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('17-44-33', 'p', 'AM', 'am_tuning_curve')
# exp4.add_session('17-48-49', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('17-51-10', None, 'laserTrain', 'am_tuning_curve')

exp4.maxDepth = 1230


exp5 = celldatabase.Experiment(subject, '2017-11-15', 'left_AC', info=['lateralDiD','TT1ant','sound_right'])
experiments.append(exp5)

exp5.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.9,
    '2.5':3.55,
    '3.0':4.15,
    '3.5':5.0
}

# exp5.add_site(850, tetrodes=[1,2,4])
# exp5.add_session('13-19-22', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('13-20-47', None, 'laserPulse', 'am_tuning_curve')
# # laser response on TT2, but extremely shitty cluster
# 
# exp5.add_site(860, tetrodes=[2,4,6])
# exp5.add_session('13-28-17', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(870, tetrodes=[2,4,6])
# exp5.add_session('13-36-59', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(880, tetrodes=[2,4,6])
# exp5.add_session('13-56-56', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(900, tetrodes=[2,4,6])
# exp5.add_session('14-06-52', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(920, tetrodes=[2,4,6])
# exp5.add_session('14-14-25', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(940, tetrodes=[2,4,6])
# exp5.add_session('14-21-31', None, 'laserPulse', 'am_tuning_curve')

exp5.add_site(950, tetrodes=[2,4,6])
exp5.add_session('14-44-48', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('14-46-51', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-49-37', None, 'laserPulse', 'am_tuning_curve') #2.5 mW laser
exp5.add_session('14-50-58', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-58-59', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('15-03-24', None, 'laserPulse', 'am_tuning_curve') # back to 1.5 mW
exp5.add_session('15-05-33', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('15-11-33', 'c', 'bandwidth', 'bandwidth_am')
exp5.add_session('15-30-02', 'd', 'harmonics', 'bandwidth_am')
exp5.add_session('15-41-20', 'e', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1000, tetrodes=[1,2,4,6,8])
exp5.add_session('15-53-47', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('15-55-07', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('15-56-35', 'f', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-03-29', 'g', 'AM', 'am_tuning_curve')
exp5.add_session('16-07-46', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('16-09-53', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('16-13-42', 'h', 'bandwidth', 'bandwidth_am')
exp5.add_session('16-34-50', 'i', 'harmonics', 'bandwidth_am')
exp5.add_session('16-48-39', 'j', 'noiseAmps', 'am_tuning_curve')

# exp5.add_site(1050, tetrodes=[1,2,4,5,6])
# exp5.add_session('17-01-06', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1075, tetrodes=[1,2,4,5,6])
# exp5.add_session('17-05-11', None, 'laserPulse', 'am_tuning_curve')
# 
# exp5.add_site(1100, tetrodes=[1,2,4,5,6])
# exp5.add_session('17-14-53', None, 'laserPulse', 'am_tuning_curve')

# exp5.add_site(1125, tetrodes=[1,2,4,5,6,8])
# exp5.add_session('17-20-04', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('17-21-14', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('17-23-15', 'k', 'tuningCurve', 'am_tuning_curve')
# exp5.add_session('17-31-18', 'l', 'AM', 'am_tuning_curve')
# exp5.add_session('17-37-05', None, 'laserPulse', 'am_tuning_curve')
# exp5.add_session('17-39-50', None, 'laserTrain', 'am_tuning_curve')

exp5.add_site(1140, tetrodes=[1,2,4,5,6,8])
exp5.add_session('17-51-43', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('17-53-29', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-55-28', 'm', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-04-09', 'n', 'AM', 'am_tuning_curve')
exp5.add_session('18-09-11', None, 'laserPulse', 'am_tuning_curve')
exp5.add_session('18-11-53', None, 'laserTrain', 'am_tuning_curve')
exp5.add_session('18-16-50', 'o', 'bandwidth', 'bandwidth_am') #14kHz for TT8
exp5.add_session('18-36-01', 'p', 'bandwidth', 'bandwidth_am') #18kHz for TT2
exp5.add_session('18-54-51', 'q', 'harmonics', 'bandwidth_am')
exp5.add_session('19-06-48', 'r', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1140


exp6 = celldatabase.Experiment(subject, '2017-11-16', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp6)

exp6.laserCalibration = {
    '0.5':1.4,
    '1.0':1.75,
    '1.5':2.25,
    '2.0':2.85,
    '2.5':3.4,
    '3.0':4.0,
    '3.5':4.7
}

# exp6.add_site(1000, tetrodes=[2,4,8])
# exp6.add_session('11-45-24', None, 'noisebursts', 'am_tuning_curve')
# exp6.add_session('11-46-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1050, tetrodes=[2,8])
# exp6.add_session('11-54-51', None, 'laserPulse', 'am_tuning_curve')

exp6.add_site(1100, tetrodes=[2,4,8])
exp6.add_session('12-12-48', None, 'laserPulse', 'am_tuning_curve')
exp6.add_session('12-13-55', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('12-15-48', 'a', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('12-24-08', 'b', 'AM', 'am_tuning_curve')
exp6.add_session('12-28-22', None, 'laserPulse', 'am_tuning_curve')
exp6.add_session('12-30-33', None, 'laserTrain', 'am_tuning_curve')
exp6.add_session('12-33-03', 'c', 'bandwidth', 'bandwidth_am')
exp6.add_session('12-52-03', 'd', 'harmonics', 'bandwidth_am')
exp6.add_session('13-03-23', 'e', 'noiseAmps', 'am_tuning_curve')

# exp6.add_site(1150, tetrodes=[2,4,8])
# exp6.add_session('13-13-59', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1175, tetrodes=[2,4,8])
# exp6.add_session('13-21-22', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1200, tetrodes=[2,8])
# exp6.add_session('13-28-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1225, tetrodes=[2,8])
# exp6.add_session('13-33-53', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1250, tetrodes=[1,2,4,8])
# exp6.add_session('13-39-16', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1275, tetrodes=[1,2,4,7,8])
# exp6.add_session('13-43-47', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1300, tetrodes=[1,2,4,7,8])
# exp6.add_session('13-48-04', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1325, tetrodes=[1,2,4,7,8])
# exp6.add_session('13-53-27', None, 'laserPulse', 'am_tuning_curve')
# 
# exp6.add_site(1350, tetrodes=[1,2,4,7,8])
# exp6.add_session('13-59-56', None, 'laserPulse', 'am_tuning_curve')

exp6.maxDepth = 1350
