from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa010'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-01-11', 'left_AudStr', info='AnteriorMedialDiI')
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; tetrodes

exp0.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.3,
    '2.0':1.6,
    '2.5':1.9,
    '3.0':2.3,
    '3.5':2.65,
    '4.0':3.0
}

#Tetrode 6 has reference
exp0.add_site(2100, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('14-16-49', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-20-13', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-24-30', 'b', 'tuningCurve', 'am_tuning_curve')
