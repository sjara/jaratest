from jaratoolbox import celldatabase

subject = 'band058'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-04-26', 'left_AC', info=['medialDiD','TT1ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.4,
    '2.0':3.9,
    '3.0':4.45,
    '4.0':5.0,
    '5.0':5.6,
    '7.5':6.9,
    '10.0':8.35
    }

# exp0.add_site(1000, tetrodes=[1,2,7,8])
# exp0.add_session('13-07-09', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[2,7,8])
# exp0.add_session('13-22-38', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1100, tetrodes=[2,7,8])
# exp0.add_session('14-21-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[2,7,8])
# exp0.add_session('14-31-12', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1200, tetrodes=[2,7,8])
# exp0.add_session('15-14-01', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1300, tetrodes=[2,7,8])
# exp0.add_session('15-44-34', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1400, tetrodes=[2,7,8])
# exp0.add_session('16-08-16', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1450, tetrodes=[2,7,8])
# exp0.add_session('16-34-40', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1500, tetrodes=[2,7,8])
# exp0.add_session('17-16-32', None, 'noisebursts', 'am_tuning_curve')

exp0.maxDepth = 1500


exp1 = celldatabase.Experiment(subject, '2018-05-01', 'left_AC', info=['lateralDiO','TT1ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.35,
    '2.0':3.9,
    '3.0':4.4,
    '4.0':4.95,
    '5.0':5.45,
    '7.5':6.85,
    '10.0':8.2
    }

# exp1.add_site(1000, tetrodes=[1,2,4,7,8])
# exp1.add_session('10-44-10', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[8])
exp1.add_session('12-05-13', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-06-14', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('12-07-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-11-52', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-18-16', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('12-46-14', 'd', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1200, tetrodes=[2,6,7,8])
# exp1.add_session('13-03-35', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[2,4,7,8])
exp1.add_session('13-17-20', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-18-38', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-21-46', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-26-12', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('13-33-02', 'g', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-58-25', 'h', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1300


exp2 = celldatabase.Experiment(subject, '2018-05-02', 'left_AC', info=['middleDiD','TT1ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.3,
    '2.0':3.85,
    '3.0':4.4,
    '4.0':4.95,
    '5.0':5.5,
    '7.5':6.9,
    '10.0':8.3
    }

exp2.add_site(1100, tetrodes=[2,4,8])
exp2.add_session('13-19-25', None, 'noisebursts', 'am_tuning_curve')

exp2.maxDepth = 1325


exp3 = celldatabase.Experiment(subject, '2018-05-03', 'left_AC', info=['middleDiO','TT1ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.3,
    '2.0':3.8,
    '3.0':4.35,
    '4.0':4.9,
    '5.0':5.4,
    '7.5':6.8,
    '10.0':8.1
    }
#shank 4 not going in

# exp3.add_site(1150, tetrodes=[2,4,6])
# exp3.add_session('13-22-21', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[2,4,6])
# exp3.add_session('14-08-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1250, tetrodes=[1,2,4,6])
# exp3.add_session('14-16-11', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1300, tetrodes=[1,2,4])
exp3.add_session('14-22-50', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-23-59', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('14-25-33', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-30-09', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('14-36-54', 'c', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('15-01-42', 'd', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1400, tetrodes=[1,2,4])
exp3.add_session('15-14-44', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-16-28', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('15-18-39', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-24-29', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('15-31-02', 'g', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('15-55-52', 'h', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1500, tetrodes=[1,2])
exp3.add_session('16-09-21', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-10-39', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-13-27', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-18-22', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('16-24-56', 'k', 'laserBandwidth', 'bandwidth_am')
exp3.add_session('16-48-59', 'l', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1500


exp4 = celldatabase.Experiment(subject, '2018-05-04', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.3,
    '2.0':3.85,
    '3.0':4.4,
    '4.0':4.9,
    '5.0':5.45,
    '7.5':6.8,
    '10.0':8.1
    }

#Signals went totally silent... pulling out after 1150 um
exp4.maxDepth = 1150


exp5 = celldatabase.Experiment(subject, '2018-05-08', 'right_AC', info=['medialDiO','TT1ant','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.45,
    '2.0':4.15,
    '3.0':4.9,
    '4.0':5.6,
    '5.0':6.3,
    '7.5':8.05,
    '9.6':10.0
    }

exp5.add_site(850, tetrodes=[5,6,7,8])
exp5.add_session('13-40-19', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-44-08', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('13-45-37', 'a', 'tuningCurve', 'am_tuning_curve')

# exp5.add_site(950, tetrodes=[3,5,6,7,8])
# exp5.add_session('13-55-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1050, tetrodes=[7,8])
# exp5.add_session('14-02-26', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1100, tetrodes=[7,8])
# exp5.add_session('14-07-31', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1200, tetrodes=[7,8])
# exp5.add_session('14-12-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1300, tetrodes=[5,6,7,8])
# exp5.add_session('14-27-58', None, 'noisebursts', 'am_tuning_curve')
#
# exp5.add_site(1400, tetrodes=[6,7,8])
# exp5.add_session('14-36-20', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(1500, tetrodes=[4,5,6,8])
exp5.add_session('14-55-51', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-57-04', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('14-58-42', 'b', 'tuningCurve', 'am_tuning_curve')

# exp5.add_site(1600, tetrodes=[2,4,5,6,7,8])
# exp5.add_session('15-20-14', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(1650, tetrodes=[2,4,5,6,7,8])
exp5.add_session('15-40-13', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-42-08', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('15-43-31', 'c', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(1700, tetrodes=[2,3,4,5,6,7,8])
exp5.add_session('16-00-54', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-02-12', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('16-03-31', 'd', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-09-41', 'e', 'AM', 'am_tuning_curve')
exp5.add_session('16-18-43', 'f', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('16-44-20', 'g', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1700


exp6 = celldatabase.Experiment(subject, '2018-05-10', 'right_AC', info=['lateralDiO','TT1ant','soundleft'])
experiments.append(exp6)

exp6.laserCalibration = {
    '1.0':3.45,
    '2.0':4.2,
    '3.0':4.9,
    '4.0':5.6,
    '5.0':6.35,
    '7.5':8.15,
    '9.5':10.0
    }

# exp6.add_site(1350, tetrodes=[2])
# exp6.add_session('15-07-26', None, 'noisebursts', 'am_tuning_curve')
#
# exp6.add_site(1450, tetrodes=[7,8])
# exp6.add_session('15-37-08', None, 'noisebursts', 'am_tuning_curve')

exp6.maxDepth = 1600


exp7 = celldatabase.Experiment(subject, '2018-05-15', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp7)

exp7.laserCalibration = {
    '1.0':3.55,
    '2.0':4.25,
    '3.0':5.0,
    '4.0':5.75,
    '5.0':6.4,
    '7.5':8.5,
    '9.0':9.9
    }

# exp7.add_site(1100, tetrodes=[2,3,4,7,8])
# exp7.add_session('12-33-42', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1150, tetrodes=[1,2,4,6,8])
# exp7.add_session('12-53-20', None, 'noisebursts', 'am_tuning_curve')
#
# exp7.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
# exp7.add_session('13-06-45', None, 'noisebursts', 'am_tuning_curve')

exp7.add_site(1250, tetrodes=[1,2,3,4,6,7,8])
exp7.add_session('13-14-26', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('13-15-41', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('13-17-50', 'a', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('13-22-32', 'b', 'AM', 'am_tuning_curve')
exp7.add_session('13-28-24', 'c', 'laserBandwidth', 'bandwidth_am')
exp7.add_session('14-05-45', 'd', 'noiseAmps', 'am_tuning_curve')

exp7.add_site(1350, tetrodes=[1,2,4,5,6,7,8])
exp7.add_session('14-32-44', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('14-33-55', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('14-35-46', 'e', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('14-40-25', 'f', 'AM', 'am_tuning_curve')
exp7.add_session('14-46-57', 'g', 'laserBandwidth', 'bandwidth_am')
exp7.add_session('15-13-35', 'h', 'noiseAmps', 'am_tuning_curve')

exp7.add_site(1450, tetrodes=[1,2,4,5,6,7,8])
exp7.add_session('15-24-30', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('15-25-49', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('15-27-51', 'i', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('15-32-28', 'j', 'AM', 'am_tuning_curve')
exp7.add_session('15-40-56', 'k', 'laserBandwidth', 'bandwidth_am')
exp7.add_session('16-05-05', 'l', 'noiseAmps', 'am_tuning_curve')

exp7.add_site(1550, tetrodes=[1,2,4,5,6,7,8])
exp7.add_session('16-14-40', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('16-18-14', None, 'lasernoisebursts', 'bandwidth_am')

exp7.add_site(1650, tetrodes=[1,2,4,5,6,7,8])
exp7.add_session('16-52-20', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('16-53-57', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('16-56-37', 'm', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('17-01-20', 'n', 'AM', 'am_tuning_curve')
exp7.add_session('17-07-49', 'o', 'laserBandwidth', 'bandwidth_am')
exp7.add_session('17-35-13', 'p', 'laserBandwidth', 'bandwidth_am')
exp7.add_session('17-59-30', 'q', 'noiseAmps', 'am_tuning_curve')

exp7.maxDepth = 1650
