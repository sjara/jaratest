from jaratoolbox import celldatabase

subject = 'band062'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-05-17', 'left_AC', info=['lateralDiD','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.55,
    '2.0':4.2,
    '3.0':5.0,
    '4.0':5.7,
    '5.0':6.4,
    '7.5':8.2,
    '9.8':10.0
    }

exp0.add_site(1050, tetrodes=[2,3,4,6,8])
exp0.add_session('12-40-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-41-44', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('12-44-04', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-48-45', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('12-55-17', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('13-23-33', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[2,4,6,8])
exp0.add_session('13-44-46', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-46-06', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('13-48-10', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-53-13', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('13-58-44', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('14-23-36', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1250, tetrodes=[2,4,6,8])
exp0.add_session('14-44-32', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-45-53', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('14-47-48', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-52-27', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('14-58-02', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-22-27', 'l', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1350, tetrodes=[2,4,5,6,8])
# exp0.add_session('15-34-22', None, 'noisebursts', 'am_tuning_curve')

exp0.maxDepth = 1350


exp1 = celldatabase.Experiment(subject, '2018-05-21', 'left_AC', info=['lateralDiO','TT1ant','soundright'])
experiments.append(exp1)

#directly from tether for control day
exp1.laserCalibration = {
    '1.0':3.05,
    '2.0':3.2,
    '3.0':3.4,
    '4.0':3.6,
    '5.0':3.8,
    '7.5':4.35,
    '10.0':4.85
    }

exp1.add_site(900, tetrodes=[1,2,4,6,7,8])
exp1.add_session('11-11-41', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-13-31', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('11-14-54', 'a', 'tuningCurve', 'am_tuning_curve')

# exp1.add_site(950, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('11-45-40', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('11-53-37', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1050, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('12-39-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
# exp1.add_session('13-20-19', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1150, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('14-19-17', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-21-14', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('14-23-10', 'b', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('15-02-31', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-03-41', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-05-51', 'c', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-10-26', 'd', 'AM', 'am_tuning_curve')
exp1.add_session('15-15-57', 'e', 'laserBandwidthControl', 'bandwidth_am')
exp1.add_session('15-41-10', 'f', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('15-59-44', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-01-18', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('16-02-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-04-16', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-09-07', 'h', 'AM', 'am_tuning_curve')

exp1.add_site(1400, tetrodes=[1,2,3,4,7,8])
exp1.add_session('16-22-16', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-23-30', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('16-25-07', 'i', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-30-35', 'j', 'AM', 'am_tuning_curve')
exp1.add_session('16-41-03', 'k', 'laserBandwidthControl', 'bandwidth_am')
exp1.add_session('17-05-24', 'l', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1400


exp2 = celldatabase.Experiment(subject, '2018-05-22', 'left_AC', info=['medialDiD','TT1ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.7,
    '2.0':4.55,
    '3.0':5.4,
    '4.0':6.25,
    '5.0':6.9,
    '7.5':9.0
    }

exp2.add_site(1400, tetrodes=[4,6])
exp2.add_session('14-32-24', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-33-45', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('14-35-03', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-39-40', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-45-14', 'c', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('15-24-53', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1600, tetrodes=[4])
# exp2.add_session('15-53-13', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1650, tetrodes=[2,4,6])
# exp2.add_session('16-07-53', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-13-10', None, 'noisebursts', 'am_tuning_curve')

exp2.maxDepth = 1650


exp3 = celldatabase.Experiment(subject, '2018-05-23', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.55,
    '2.0':4.3,
    '3.0':5.05,
    '4.0':5.85,
    '5.0':6.6,
    '7.5':8.5
    }

# exp3.add_site(950, tetrodes=[2,4])
# exp3.add_session('11-29-14', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1000, tetrodes=[2,4])
exp3.add_session('11-36-12', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-37-16', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('11-38-48', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('11-43-21', 'b', 'AM', 'am_tuning_curve')

# exp3.add_site(1100, tetrodes=[1,2,4])
# exp3.add_session('12-20-56', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1200, tetrodes=[1,2,4])
exp3.add_session('13-08-30', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-09-44', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('13-11-39', 'c', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-16-45', 'd', 'AM', 'am_tuning_curve')
exp3.add_session('13-22-37', 'e', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('13-54-21', 'f', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1300, tetrodes=[2,4,6,8])
# exp3.add_session('14-27-08', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('14-28-21', None, 'lasernoisebursts', 'bandwidth_am')
# exp3.add_session('15-53-37', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('15-54-53', None, 'lasernoisebursts', 'bandwidth_am')

exp3.add_site(1400, tetrodes=[2,4,8])
exp3.add_session('16-07-12', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-08-23', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-14-10', 'g', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(1450, tetrodes=[1,2,8])
exp3.add_session('16-31-25', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-32-34', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-35-37', 'h', 'tuningCurve', 'am_tuning_curve')

# exp3.add_site(1500, tetrodes=[2])
# exp3.add_session('16-52-55', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1550, tetrodes=[2])
# exp3.add_session('16-59-53', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1600, tetrodes=[2,4,8])
# exp3.add_session('17-07-31', None, 'noisebursts', 'am_tuning_curve')

exp3.maxDepth = 1600


exp4 = celldatabase.Experiment(subject, '2018-05-24', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.6,
    '2.0':4.35,
    '3.0':5.2,
    '4.0':5.95,
    '5.0':6.75,
    '7.5':8.75
    }

exp4.add_site(1000, tetrodes=[2,4])
exp4.add_session('13-16-28', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-17-37', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-20-56', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-25-15', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('13-31-44', 'c', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('13-55-46', 'd', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1100, tetrodes=[2,4,8])
exp4.add_session('14-14-24', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-15-45', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('14-17-26', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-22-06', 'f', 'AM', 'am_tuning_curve')
exp4.add_session('14-28-05', 'g', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-56-35', 'h', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1200, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('15-28-50', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-30-11', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-31-39', 'i', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-38-46', 'j', 'AM', 'am_tuning_curve')
#nothing has good frequency tuning!

exp4.add_site(1300, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('15-53-49', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-55-09', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-56-35', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-01-28', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('16-09-29', 'm', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('16-34-19', 'n', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('16-46-06', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-47-56', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('16-50-00', 'o', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-55-02', 'p', 'AM', 'am_tuning_curve')
exp4.add_session('17-01-14', 'q', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('17-25-21', 'r', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1500, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('17-38-10', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('17-39-26', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('17-41-15', 's', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('17-46-18', 't', 'AM', 'am_tuning_curve')
exp4.add_session('17-54-42', 'u', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('18-18-44', 'v', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1500


exp5 = celldatabase.Experiment(subject, '2018-05-25', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.55,
    '2.0':4.35,
    '3.0':5.15,
    '4.0':6.0,
    '5.0':6.8,
    '7.5':9.0
    }

# exp5.add_site(850, tetrodes=[2,4,6])
# exp5.add_session('14-22-26', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(1000, tetrodes=[1,2,4,6])
exp5.add_session('14-58-47', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-59-53', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('15-01-08', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-05-41', 'b', 'AM', 'am_tuning_curve')

# exp5.add_site(1050, tetrodes=[1,2,4,6])
# exp5.add_session('15-27-24', None, 'noisebursts', 'am_tuning_curve')

# exp5.add_site(1100, tetrodes=[2,4,6,8])
# exp5.add_session('15-35-34', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('15-36-46', None, 'lasernoisebursts', 'bandwidth_am')

exp5.add_site(1150, tetrodes=[1,2,4,6])
exp5.add_session('15-49-43', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-50-48', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('15-52-04', 'c', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-59-49', 'd', 'AM', 'am_tuning_curve')
exp5.add_session('16-05-12', 'e', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('16-29-31', 'f', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1250, tetrodes=[1,2,3,4,5,6])
exp5.add_session('16-45-15', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-46-32', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('16-47-51', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-52-10', 'h', 'AM', 'am_tuning_curve')
exp5.add_session('16-59-53', 'i', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('17-27-19', 'j', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1350, tetrodes=[1,2,3,4,5,6,8])
exp5.add_session('17-39-59', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-41-15', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('17-42-39', 'k', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-47-38', 'l', 'AM', 'am_tuning_curve')
exp5.add_session('17-54-12', 'm', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('18-20-00', 'n', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1450, tetrodes=[1,2,3,4,5,6,8])
exp5.add_session('18-32-23', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('18-33-42', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('18-35-16', 'o', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('18-40-31', 'p', 'AM', 'am_tuning_curve')
exp5.add_session('18-48-45', 'q', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('19-12-46', 'r', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1550, tetrodes=[1,2,3,4,5,6,8])
exp5.add_session('19-25-48', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('19-27-07', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('19-28-29', 's', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('19-33-10', 't', 'AM', 'am_tuning_curve')
exp5.add_session('19-41-16', 'u', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('20-05-25', 'v', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1550


exp6 = celldatabase.Experiment(subject, '2018-05-26', 'right_AC', info=['lateralDiO','TT1ant','soundleft'])
experiments.append(exp6)

#control day, tether loose
exp6.laserCalibration = {
    '1.0':3.05,
    '2.0':3.25,
    '3.0':3.45,
    '4.0':3.65,
    '5.0':3.9,
    '7.5':4.45,
    '10.0':5.0
    }

# exp6.add_site(950, tetrodes=[2,4,8])
# exp6.add_session('14-41-12', None, 'noisebursts', 'am_tuning_curve')
#
# exp6.add_site(1000, tetrodes=[2,4,6,8])
# exp6.add_session('14-57-45', None, 'noisebursts', 'am_tuning_curve')
#
# exp6.add_site(1050, tetrodes=[2,4,6,8])
# exp6.add_session('15-05-28', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1100, tetrodes=[2,3,4,6,8])
exp6.add_session('15-14-05', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('15-25-56', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('15-27-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('15-32-52', 'b', 'AM', 'am_tuning_curve')
exp6.add_session('15-40-22', 'c', 'laserBandwidthControl', 'bandwidth_am')
exp6.add_session('16-04-20', 'd', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1200, tetrodes=[2,4,6,7,8])
exp6.add_session('16-20-17', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-21-33', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('16-23-16', 'e', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('16-28-00', 'f', 'AM', 'am_tuning_curve')
exp6.add_session('16-33-54', 'g', 'laserBandwidthControl', 'bandwidth_am')
exp6.add_session('16-57-49', 'h', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1300, tetrodes=[1,2,3,4,6,8])
exp6.add_session('17-09-41', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('17-10-57', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('17-12-20', 'i', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('17-16-49', 'j', 'AM', 'am_tuning_curve')
exp6.add_session('17-23-22', 'k', 'laserBandwidthControl', 'bandwidth_am')
exp6.add_session('17-47-13', 'l', 'noiseAmps', 'am_tuning_curve')

exp6.maxDepth = 1300
