from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band036'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-09-22', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.9,
    '2.5':3.5,
    '3.0':4.1,
    '3.5':4.8
}

# exp0.add_site(1050, tetrodes=[4,8])
# exp0.add_session('14-42-31', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1100, tetrodes=[4,6,8])
# exp0.add_session('14-52-04', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1150, tetrodes=[4,6,8])
# exp0.add_session('15-03-59', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('15-05-13', None, 'noisebursts', 'am_tuning_curve')
# 
# exp0.add_site(1200, tetrodes=[4,6,8])
# exp0.add_session('15-26-16', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1250, tetrodes=[4,6,8])
# exp0.add_session('16-03-11', None, 'laserPulse', 'am_tuning_curve')
# 
# exp0.add_site(1300, tetrodes=[2,4,6,8])
# exp0.add_session('16-28-54', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('16-30-02', None, 'noisebursts', 'am_tuning_curve')

#not really getting any laser or sound responses; withdrawing from site


exp1 = celldatabase.Experiment(subject, '2017-09-25', 'left_AC', info=['medialDiI','TT1ant','sound_right'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.45,
    '1.0':1.9,
    '1.5':2.5,
    '2.0':3.25,
    '2.5':3.9,
    '3.0':4.6,
    '3.5':5.5
}

# exp1.add_site(950, tetrodes=[2,3,4,6,7,8])
# exp1.add_session('11-47-45', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('11-48-40', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1000, tetrodes=[2,3,4,6,7,8])
# exp1.add_session('11-58-48', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1050, tetrodes=[2,3,4,7,8])
# exp1.add_session('12-07-19', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1100, tetrodes=[2,3,4,6,7,8])
# exp1.add_session('12-22-09', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1150, tetrodes=[2,3,4,7,8])
# exp1.add_session('15-16-53', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1200, tetrodes=[1,2,4,5,6,7,8])
# exp1.add_session('15-24-37', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('15-26-09', None, 'noisebursts', 'am_tuning_curve')
# 
# exp1.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
# exp1.add_session('15-29-21', None, 'laserPulse', 'am_tuning_curve')
# 
# exp1.add_site(1300, tetrodes=[1,2,4,5,6,7,8])
# exp1.add_session('15-32-55', None, 'laserPulse', 'am_tuning_curve')

#nothing is even the slightest bit laser responsive. Is this even a PV mouse?


exp2 = celldatabase.Experiment(subject, '2017-09-27', 'left_AC', info=['middleDiD','TT1ant','sound_right'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':1.45,
    '1.0':1.9,
    '1.5':2.5,
    '2.0':3.2,
    '2.5':3.95,
    '3.0':4.65,
    '3.5':5.6
}

# exp2.add_site(1000, tetrodes=[4,6,8])
# exp2.add_session('14-55-50', None, 'laserPulse', 'am_tuning_curve')
# exp2.add_session('14-57-13', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1050, tetrodes=[4,6,8])
# exp2.add_session('15-08-19', None, 'noisebursts', 'am_tuning_curve')
