from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa009'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-12-12', 'left_AudStr', info='AnteriorfacingPosteriorDiI')
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser

exp0.laserCalibration = {
    '0.5':0.85,
    '1.0':1.3,
    '1.5':1.75,
    '2.0':2.25,
    '2.5':2.7,
    '3.0':3.4,
    '3.5':4.2,
    '4.0':5.0
}

exp0.add_site(2000, tetrodes=[1,2,3,8])
exp0.add_session('12-03-04', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-05-28', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2050, tetrodes=[1,2,3,4,8])
exp0.add_session('12-09-56', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-11-42', 'b', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2100, tetrodes=[1,2])
exp0.add_session('12-16-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-17-42', 'c', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2150, tetrodes=[1,2])
exp0.add_session('12-24-19', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-25-44', 'd', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2200, tetrodes=[1,2,4])
exp0.add_session('12-29-43', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-31-15', 'e', 'tuningCurve', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-12-17', 'right_AudStr', info='AnteriorfacingPosteriorDiI')
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser

exp1.laserCalibration = {
    '0.5':1.0,
    '1.0':1.75,
    '1.5':2.45,
    '2.0':3.3,
    '2.5':4.45,
    '3.0':5.8,
    '3.5':6.9,
    '4.0':7.7
}

#Threshold set to 55 mV
exp1.add_site(2000, tetrodes=[7])
exp1.add_session('19-10-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('19-12-29', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2100, tetrodes=[7])
exp1.add_session('19-18-48', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('19-20-42', 'b', 'tuningCurve', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-12-21', 'right_AudStr', info='MedialfacingPosteriorDiD')
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser

exp2.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.25,
    '2.0':1.6,
    '2.5':1.9,
    '3.0':2.25,
    '3.5':2.6,
    '4.0':3.0
}

#Tissue too tough for tetrodes
