from jaratoolbox import celldatabase

subject = 'band056'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-03-22', 'left_AC', info=['lateralDiO','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.35,
    '4.0':4.9,
    '5.0':5.45,
    '7.5':6.75,
    '10.0':8.2
}

exp0.add_site(900, tetrodes=[2,4,6,8])
exp0.add_session('16-39-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-40-59', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-42-29', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-50-57', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-58-12', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('17-22-28', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1000, tetrodes=[2,4,6,8])
exp0.add_session('17-40-25', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-41-44', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('17-43-02', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-47-47', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('17-55-40', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('18-20-55', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[2,4,6,7,8])
exp0.add_session('18-39-29', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-41-02', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('18-42-24', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('18-49-27', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('18-56-39', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('19-22-22', 'l', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1100


exp1 = celldatabase.Experiment(subject, '2018-03-23', 'left_AC', info=['middleDiD','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.25,
    '2.0':3.75,
    '3.0':4.25,
    '4.0':4.8,
    '5.0':5.3,
    '7.5':6.7,
    '10.0':8.05
}

exp1.add_site(900, tetrodes=[2,3,6,7,8])
exp1.add_session('09-14-00', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('09-15-07', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('09-16-16', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('09-22-04', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('09-29-28', 'c', 'laserBandwidth', 'bandwidth_am')

exp1.add_site(1000, tetrodes=[2,6,7,8])
exp1.add_session('10-45-17', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-46-42', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('10-48-26', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-54-17', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('11-01-30', 'f', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('11-25-24', 'g', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[6,7,8])
exp1.add_session('11-48-06', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-49-36', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('11-51-44', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-56-03', 'i', 'AM', 'am_tuning_curve')
exp1.add_session('12-01-10', 'j', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('12-29-52', 'k', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[2,4,6,7,8])
exp1.add_session('12-47-21', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-48-35', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('12-50-17', 'l', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-54-39', 'm', 'AM', 'am_tuning_curve')
exp1.add_session('13-02-00', 'n', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-26-25', 'o', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[2,4,6,7,8])
exp1.add_session('13-42-19', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-43-35', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-44-50', 'p', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-53-54', 'q', 'AM', 'am_tuning_curve')
exp1.add_session('13-59-42', 'r', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('14-24-06', 's', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1300


exp2 = celldatabase.Experiment(subject, '2018-03-27', 'left_AC', info=['medialDiO','TT1ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.35,
    '4.0':4.8,
    '5.0':5.35,
    '7.5':6.65,
    '10.0':7.9
}
#shank 1 not going in

# exp2.add_site(800, tetrodes=[4,6])
# exp2.add_session('10-37-46', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(900, tetrodes=[8])
# exp2.add_session('11-18-12', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1050, tetrodes=[8])
exp2.add_session('11-48-47', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-49-48', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('11-51-43', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-56-18', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('12-01-56', 'c', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('12-26-03', 'd', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1150, tetrodes=[6,7,8])
exp2.add_session('12-35-51', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-37-02', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('12-38-19', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-42-52', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('12-49-16', 'g', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('13-13-20', 'h', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1250, tetrodes=[6,7,8])
exp2.add_session('13-27-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-28-50', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('13-30-06', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-34-40', 'j', 'AM', 'am_tuning_curve')
exp2.add_session('13-41-00', 'k', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('14-13-06', 'l', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1350, tetrodes=[6,7,8])
exp2.add_session('14-32-01', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-33-45', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('14-35-02', 'm', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-40-28', 'n', 'AM', 'am_tuning_curve')
exp2.add_session('14-51-26', 'o', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('15-15-40', 'p', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1450, tetrodes=[7,8])
# exp2.add_session('15-27-20', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-28-34', None, 'lasernoisebursts', 'bandwidth_am')
#very unimpressive sound responses

exp2.maxDepth = 1450


exp3 = celldatabase.Experiment(subject, '2018-03-28', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.3,
    '4.0':4.8,
    '5.0':5.35,
    '7.5':6.65,
    '10.0':7.9
}

# exp3.add_site(950, tetrodes=[2,6,7,8])
# exp3.add_session('09-18-53', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[2,6,7,8])
# exp3.add_session('09-28-57', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1050, tetrodes=[2,6,7,8])
# exp3.add_session('09-37-05', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[2,6,7,8])
# exp3.add_session('09-45-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1150, tetrodes=[6,7,8])
# exp3.add_session('10-00-02', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[6,8])
# exp3.add_session('10-08-41', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes=[7,8])
# exp3.add_session('10-17-41', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[7,8])
# exp3.add_session('10-29-00', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1350, tetrodes=[1,2,7,8])
# exp3.add_session('10-37-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1400, tetrodes=[6,7,8])
# exp3.add_session('10-42-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1450, tetrodes=[1,6,7,8])
# exp3.add_session('10-47-04', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1500, tetrodes=[2,4,6,7,8])
# exp3.add_session('10-52-17', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1550, tetrodes=[4,5,6,7,8])
exp3.add_session('10-57-21', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('10-58-18', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('10-59-26', 'a', 'tuningCurve', 'am_tuning_curve')
# no tuning

exp3.add_site(1600, tetrodes=[4,5,6,7,8])
exp3.add_session('11-08-32', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-10-17', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('11-11-30', 'b', 'tuningCurve', 'am_tuning_curve')

# exp3.add_site(1650, tetrodes=[1,4,5,6,7,8])
# exp3.add_session('11-24-40', None, 'noisebursts', 'am_tuning_curve')

exp3.maxDepth = 1650


exp4 = celldatabase.Experiment(subject, '2018-03-29', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.35,
    '2.0':3.85,
    '3.0':4.4,
    '4.0':4.95,
    '5.0':5.5,
    '7.5':6.8,
    '10.0':8.1
}

# exp4.add_site(1000, tetrodes=[8])
# exp4.add_session('09-42-58', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1050, tetrodes=[8])
# exp4.add_session('10-00-10', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('10-01-17', None, 'lasernoisebursts', 'bandwidth_am')
#
# exp4.add_site(1100, tetrodes=[8])
# exp4.add_session('10-13-42', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1150, tetrodes=[7,8])
# exp4.add_session('10-35-13', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('10-36-29', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('10-38-06', 'a', 'tuningCurve', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[7,8])
# exp4.add_session('11-07-23', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1250, tetrodes=[6,7,8])
exp4.add_session('11-13-17', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-14-42', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('11-16-03', 'b', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-21-37', 'c', 'AM', 'am_tuning_curve')
exp4.add_session('11-27-55', 'd', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('11-53-30', 'e', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1350, tetrodes=[6,7,8])
exp4.add_session('12-08-27', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-09-50', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('12-11-05', 'f', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(1450, tetrodes=[5,7,8])
exp4.add_session('12-25-08', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-26-23', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('12-27-40', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-32-33', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('12-41-17', 'i', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('13-06-53', 'j', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1550, tetrodes=[6,7,8])
exp4.add_session('13-43-33', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-45-32', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-47-11', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-54-07', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('14-03-12', 'm', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-27-16', 'n', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1550


exp5 = celldatabase.Experiment(subject, '2018-03-30', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.35,
    '4.0':4.9,
    '5.0':5.3,
    '7.5':6.7,
    '10.0':8.0
}

exp5.add_site(1150, tetrodes=[8])
exp5.add_session('11-39-36', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-41-12', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('11-42-19', 'a', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(1200, tetrodes=[2,7,8])
exp5.add_session('11-55-53', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-56-59', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('11-58-05', 'b', 'tuningCurve', 'am_tuning_curve')

#observed middle two shanks not going in

exp5.add_site(1300, tetrodes=[2,7,8])
exp5.add_session('12-21-43', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('12-22-51', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('12-25-34', 'c', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-32-48', 'd', 'AM', 'am_tuning_curve')
exp5.add_session('12-38-47', 'e', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('13-04-57', 'f', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1400, tetrodes=[2,7,8])
exp5.add_session('13-16-38', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-17-55', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('13-20-16', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-26-46', 'h', 'AM', 'am_tuning_curve')
exp5.add_session('13-35-45', 'i', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('14-01-53', 'j', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1400


exp6 = celldatabase.Experiment(subject, '2018-03-31', 'right_AC', info=['lateralDiO','TT1ant','soundleft'])
experiments.append(exp6)

#tether not attached
exp6.laserCalibration = {
    '1.0':3.1,
    '2.0':3.25,
    '3.0':3.4,
    '4.0':3.6,
    '5.0':3.8,
    '7.5':4.3,
    '10.0':4.8
}

# exp6.add_site(1150, tetrodes=[1,2])
# exp6.add_session('15-49-50', None, 'noisebursts', 'am_tuning_curve')
#
# exp6.add_site(1250, tetrodes=[2])
# exp6.add_session('16-01-38', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1300, tetrodes=[1,2,8])
exp6.add_session('16-10-05', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-11-03', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('16-12-15', 'a', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('16-16-47', 'b', 'AM', 'am_tuning_curve')
exp6.add_session('16-23-01', 'c', 'laserBandwidthControl', 'bandwidth_am')
exp6.add_session('16-47-11', 'd', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1400, tetrodes=[1,2,6,7,8])
exp6.add_session('16-59-40', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('17-01-03', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('17-02-17', 'e', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('17-09-13', 'f', 'AM', 'am_tuning_curve')
exp6.add_session('17-15-37', 'g', 'laserBandwidthControl', 'bandwidth_am')
exp6.add_session('17-40-26', 'h', 'noiseAmps', 'am_tuning_curve')

exp6.maxDepth = 1400
