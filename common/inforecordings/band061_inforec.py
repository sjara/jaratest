from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band061'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-05-28', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.55,
    '2.0':4.35,
    '3.0':5.1,
    '4.0':5.9,
    '5.0':6.75,
    '7.5':8.7
    }

exp0.add_site(1400, tetrodes=[1,6])
exp0.add_session('12-36-49', None, 'noisebursts', 'am_tuning_curve')

#cll channels pretty silent, probe probably busted
exp0.maxDepth = 1500


exp1 = celldatabase.Experiment(subject, '2018-05-29', 'right_AC', info=['medialDiO','TT1ant','soundleft'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.55,
    '2.0':4.3,
    '3.0':5.05,
    '4.0':5.8,
    '5.0':6.55,
    '7.5':8.4
    }

exp1.add_site(900, tetrodes=[1,2,4,8])
exp1.add_session('12-33-14', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1000, tetrodes=[1,2,3,4,6,8])
exp1.add_session('12-45-24', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1050, tetrodes=[1,2,3,4,6,8])
exp1.add_session('13-09-13', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-11-15', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-13-19', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-26-54', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-35-43', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-43-51', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1400, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-55-48', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('14-01-16', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1600, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('14-46-24', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-47-38', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('14-49-17', 'b', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-54-42', 'c', 'AM', 'am_tuning_curve')
exp1.add_session('15-02-15', 'd', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('15-27-11', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1700, tetrodes=[1,2,3,4,6,8])
exp1.add_session('15-44-40', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-46-07', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-47-41', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-52-06', 'g', 'AM', 'am_tuning_curve')
exp1.add_session('15-58-14', 'h', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('16-26-16', 'i', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1700


exp2 = celldatabase.Experiment(subject, '2018-05-30', 'right_AC', info=['middleDiD','TT1ant','soundleft'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.6,
    '2.0':4.5,
    '3.0':5.45,
    '4.0':6.4,
    '5.0':7.1,
    '7.2':10.0
    }

exp2.add_site(1500, tetrodes=[1,2])
exp2.add_session('13-30-07', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-31-33', None, 'lasernoisebursts', 'bandwidth_am')

exp2.maxDepth = 1600


exp3 = celldatabase.Experiment(subject, '2018-06-05', 'left_AC', info=['medialDiD','TT1ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.25,
    '2.0':3.65,
    '3.0':4.1,
    '4.0':4.55,
    '5.0':5.05,
    '7.5':6.2,
    '10.0':7.3
    }

exp3.add_site(1000, tetrodes=[2])
exp3.add_session('14-43-22', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-45-12', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('14-47-18', 'a', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(1050, tetrodes=[1,2,4])
exp3.add_session('15-12-16', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('15-21-21', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1200, tetrodes=[2,3,4,5,6,7,8])
exp3.add_session('15-46-49', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1300, tetrodes=[2,3,4,5,6,7,8])
exp3.add_session('17-24-51', None, 'noisebursts', 'am_tuning_curve')

exp3.maxDepth = 1300


exp4 = celldatabase.Experiment(subject, '2018-06-06', 'left_AC', info=['middleDiO','TT8ant','soundright'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.3,
    '2.0':3.7,
    '3.0':4.15,
    '4.0':4.6,
    '5.0':5.05,
    '7.5':6.2,
    '10.0':7.3
    }

exp4.add_site(1000, tetrodes=[8])
exp4.add_session('12-41-22', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1050, tetrodes=[7,8])
exp4.add_session('13-04-44', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1150, tetrodes=[7,8])
exp4.add_session('13-26-32', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-28-43', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-30-58', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-35-42', 'b', 'AM', 'am_tuning_curve')

exp4.add_site(1300, tetrodes=[4,6,7,8])
exp4.add_session('13-48-33', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-50-40', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-53-51', 'c', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-57-58', 'd', 'AM', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[3,4,6,7,8])
exp4.add_session('15-04-35', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-06-04', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-07-51', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-14-27', 'f', 'AM', 'am_tuning_curve')

exp4.add_site(1470, tetrodes=[3,4,6,7,8])
exp4.add_session('15-27-27', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1520, tetrodes=[5,6,7,8])
exp4.add_session('15-35-44', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(1650, tetrodes=[6,7,8])
exp4.add_session('15-58-14', None, 'noisebursts', 'am_tuning_curve')


exp5 = celldatabase.Experiment(subject, '2018-06-07', 'left_AC', info=['posteriourmedialDiO','TT8ant','soundright'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.2,
    '2.0':3.6,
    '3.0':4.0,
    '4.0':4.45,
    '5.0':4.9,
    '7.5':5.9,
    '10.0':7.0
    }

exp5.add_site(1600, tetrodes=[2,4,6])
exp5.add_session('16-36-29', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-37-53', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('16-39-41', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-41-08', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-45-30', 'b', 'AM', 'am_tuning_curve')

exp5.add_site(1650, tetrodes=[2,4,6])
exp5.add_session('16-57-21', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(1700, tetrodes=[2,4,6])
exp5.add_session('17-06-38', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-07-55', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('17-10-48', 'c', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-15-09', 'd', 'AM', 'am_tuning_curve')

exp5.add_site(1800, tetrodes=[1,2,3,4,5,6])
exp5.add_session('17-28-31', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-29-52', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('17-31-59', 'e', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-36-23', 'f', 'AM', 'am_tuning_curve')


exp6 = celldatabase.Experiment(subject, '2018-06-13', 'left_AC', info=['posteriourmiddleDiD','TT8ant','soundright'])
experiments.append(exp6)

exp6.laserCalibration = {
    '1.0':3.25,
    '2.0':3.65,
    '3.0':4.05,
    '4.0':4.5,
    '5.0':4.95,
    '7.5':6.0,
    '10.0':7.1
    }

exp6.add_site(900, tetrodes=[3,4,8])
exp6.add_session('13-00-26', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('13-02-24', None, 'lasernoisebursts', 'bandwidth_am')

exp6.add_site(950, tetrodes=[3,4,6,8])
exp6.add_session('13-12-49', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1000, tetrodes=[3,4,6,7,8])
exp6.add_session('13-38-04', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1050, tetrodes=[4,6,7,8])
exp6.add_session('14-00-38', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1100, tetrodes=[3,6,7,8])
exp6.add_session('14-23-05', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1150, tetrodes=[3,6,7,8])
exp6.add_session('14-41-02', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1200, tetrodes=[5,6,7,8])
exp6.add_session('14-50-43', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1300, tetrodes=[4,6,8])
exp6.add_session('15-12-28', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1350, tetrodes=[2,3,4,6,8])
exp6.add_session('15-20-51', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1400, tetrodes=[2,4,6,8])
exp6.add_session('15-27-15', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1450, tetrodes=[2,3,4,6,8])
exp6.add_session('15-36-04', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('15-38-21', None, 'lasernoisebursts', 'bandwidth_am')

exp6.add_site(1500, tetrodes=[3,4,5,6,7,8])
exp6.add_session('15-50-06', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('15-51-35', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1550, tetrodes=[1,2,4,5,6,7,8])
exp6.add_session('15-59-32', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1600, tetrodes=[1,2,3,4,5,6,8])
exp6.add_session('16-05-40', None, 'noisebursts', 'am_tuning_curve')

exp6.maxDepth = 1600
