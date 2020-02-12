from jaratoolbox import celldatabase

subject = 'band057'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-04-05', 'left_AC', info=['lateralDiD','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.2,
    '4.0':4.7,
    '5.0':5.2,
    '7.5':6.4,
    '10.0':7.8
}

# exp0.add_site(1050, tetrodes=[1,2,7,8])
# exp0.add_session('15-26-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[1,2,7,8])
# exp0.add_session('15-46-54', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[1,2,6,7,8])
# exp0.add_session('15-54-09', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes=[1,2,4,7,8])
# exp0.add_session('16-03-49', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1250, tetrodes=[1,2,7,8])
# exp0.add_session('16-09-24', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,7,8])
exp0.add_session('16-16-08', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-17-17', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-18-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-23-04', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-29-57', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-53-58', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1300


exp1 = celldatabase.Experiment(subject, '2018-04-06', 'left_AC', info=['middleDiO','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.4,
    '4.0':4.9,
    '5.0':5.55,
    '7.5':6.9,
    '10.0':8.1
}

exp1.add_site(900, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-56-40', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-57-57', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-59-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-10-20', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('14-19-25', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('14-45-12', 'd', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('15-19-00', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('15-33-29', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-35-09', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-38-33', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-43-02' ,'g', 'AM', 'am_tuning_curve')
exp1.add_session('15-50-10', 'h', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('16-14-39', 'i', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('16-36-24', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-38-13', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('16-42-14', 'j', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-49-45', 'k', 'AM', 'am_tuning_curve')
exp1.add_session('16-57-50', 'l', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('17-21-57', 'm', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1100


exp2 = celldatabase.Experiment(subject, '2018-04-09', 'left_AC', info=['medialDiD','TT1ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.4,
    '2.0':3.9,
    '3.0':4.5,
    '4.0':5.05,
    '5.0':5.6,
    '7.5':7.05,
    '10.0':8.4
}

exp2.add_site(900, tetrodes=[2,4,8])
exp2.add_session('11-01-24', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-02-38', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('11-03-52', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-08-17', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('11-15-02', 'c', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('11-39-09', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1000, tetrodes=[1,2,4,8])
# exp2.add_session('12-42-29', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1050, tetrodes=[8])
# exp2.add_session('12-52-47', None, 'noisebursts', 'am_tuning_curve')
#
exp2.add_site(1100, tetrodes=[1,2,4,7,8])
exp2.add_session('13-00-09', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-01-15', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('13-02-52', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-07-48', 'f', 'AM', 'am_tuning_curve')
#
# exp2.add_site(1200, tetrodes=[1,2,4,8])
# exp2.add_session('13-40-12', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1250, tetrodes=[1,2,4,7,8])
exp2.add_session('13-51-17', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-52-36', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('13-54-37', 'g', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-00-03', 'h', 'AM', 'am_tuning_curve')
exp2.add_session('14-06-00', 'i', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('14-30-23', 'j', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1350, tetrodes=[1,2,7,8])
# exp2.add_session('14-42-42', None, 'noisebursts', 'am_tuning_curve')

exp2.maxDepth = 1250


exp3 = celldatabase.Experiment(subject, '2018-04-10', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.35,
    '2.0':3.9,
    '3.0':4.5,
    '4.0':5.05,
    '5.0':5.6,
    '7.5':7.05,
    '10.0':8.45
}

# exp3.add_site(950, tetrodes=[2,3,4,6])
# exp3.add_session('11-41-36', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[2,4,7,8])
# exp3.add_session('12-15-06', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[2,3,4,8])
# exp3.add_session('13-08-13', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[2,4,7,8])
# exp3.add_session('13-22-58', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1350, tetrodes=[7,8])
# exp3.add_session('13-29-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1400, tetrodes=[7,8])
# exp3.add_session('13-50-17', None, 'noisebursts', 'am_tuning_curve')

exp3.maxDepth = 1400


exp4 = celldatabase.Experiment(subject, '2018-04-11', 'right_AC', info=['antDiO','facingPost','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.35,
    '2.0':3.85,
    '3.0':4.4,
    '4.0':4.9,
    '5.0':5.45,
    '7.5':6.8,
    '10.0':8.15
}

# exp4.add_site(1000, tetrodes=[3,4,7,8])
# exp4.add_session('11-36-55', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1100, tetrodes=[6,7,8])
# exp4.add_session('11-54-19', None, 'noisebursts', 'am_tuning_curve')
#
# exp4.add_site(1200, tetrodes=[1,2,3])
# exp4.add_session('12-36-44', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1300, tetrodes=[1,2,3])
exp4.add_session('13-37-44', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-39-07', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-40-45', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-45-17', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('13-50-56', 'c', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-17-40', 'd', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1300


exp5 = celldatabase.Experiment(subject, '2018-04-12', 'right_AC', info=['antDiD','facingPost','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.3,
    '2.0':3.85,
    '3.0':4.45,
    '4.0':5.0,
    '5.0':5.6,
    '7.5':7.0,
    '10.0':8.4
}

# exp5.add_site(1000, tetrodes=[1,2,7,8])
# exp5.add_session('11-03-16', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1050, tetrodes=[1,2,7,8])
# exp5.add_session('11-22-57', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1100, tetrodes=[1,2,7,8])
# exp5.add_session('11-31-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1150, tetrodes=[2,7,8])
# exp5.add_session('12-10-03', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1350, tetrodes=[1,2,7,8])
# exp5.add_session('13-11-00', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1400, tetrodes=[2])
# exp5.add_session('13-47-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1450, tetrodes=[2])
# exp5.add_session('14-45-34', None, 'noisebursts', 'am_tuning_curve')

exp5.maxDepth = 1450
