from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa011'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-02-04', 'left_AudStr', info='AnteriorMedialDiI')
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe 76B1 (from Anna)

exp0.laserCalibration = {
    '0.5':0.8,
    '1.0':1.2,
    '1.5':1.7,
    '2.0':2.1,
    '2.5':2.8,
    '3.0':3.45,
    '3.5':4.3,
    '4.0':5.4
}

#Tetrode 3 has reference; threshold set to 55mV
exp0.add_site(2500, tetrodes=[1,2,5,6,7,8])
exp0.add_session('13-44-33', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-47-26', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('13-52-34', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-53-57', 'b', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-57-07', 'c', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-14-13', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-15-44', 'd', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2650, tetrodes=[1,2,4,7,8])
exp0.add_session('14-19-52', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-21-08', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2700, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-25-19', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-26-50', 'f', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2750, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-32-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-33-36', 'g', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2800, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-39-58', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-41-22', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-44-13', 'i', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2850, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-00-56', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-02-28', 'j', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-11-44', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-13-24', 'k', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-16-05', 'l', 'tuningCurve', 'am_tuning_curve')
