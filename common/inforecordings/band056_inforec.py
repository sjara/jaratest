from jaratoolbox import celldatabase
reload(celldatabase)

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

exp1.add_site(900, tetrodes=[2,3,4,6,7,8])
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


exp2 = celldatabase.Experiment(subject, '2018-03-27', 'left_AC', info=['lateralDiO','TT1ant','soundright'])
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
