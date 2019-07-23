from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa006'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-09-27', 'left_AudStr', info='AnteriorfacingAnteriorDiI')
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':1.6,
    '1.0':2.28,
    '1.5':2.94,
    '2.0':3.5,
    '2.5':4.58,
    '3.0':5.6,
    '3.5':7.4
}

exp0.add_site(2000, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('18-48-03', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-53-05', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')
#Computer full; open-ephys froze mid recording

exp1 = celldatabase.Experiment(subject, '2017-09-27', 'left_AudStr', info='MedialfacingAnteriorDiD')
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.6,
    '1.0':2.25,
    '1.5':3.0,
    '2.0':3.4s5,
    '2.5':4.2,
    '3.0':5.45,
    '3.5':6.25
}

exp1.add_site(2000, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('18-02-15', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2050, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('18-06-09', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('18-08-42', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2100, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('19-10-03', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('19-12-15', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2200, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('20-17-30', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2250, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('20-21-54', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('20-24-08', 'c', 'laserTuningCurve', 'laser_am_tuning_curve') #Realized laser wasn't on for this or previous sessions

exp1.add_site(2300, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('21-15-22', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2350, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('21-18-02', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('21-20-19', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2400, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('22-21-45', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('22-24-02', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')
