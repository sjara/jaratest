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
exp0.add_session('14-20-13', 'a', 'tuningCurve', 'laser_am_tuning_curve')
exp0.add_session('14-24-30', 'b', 'tuningCurve', 'laser_am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2018-01-16', 'left_AudStr', info='AnteriorMedialDiD')
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; tetrodes

exp1.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.3,
    '2.0':1.6,
    '2.5':1.85,
    '3.0':2.25,
    '3.5':2.6,
    '4.0':2.95
}

#Tetrode 1 has reference; threshold at 0 mV
exp1.add_site(2100, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('13-57-35', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-59-29', 'a', 'tuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2150, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('14-04-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-06-10', 'b', 'tuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2200, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('14-09-49', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-11-27', 'c', 'tuningCurve', 'laser_am_tuning_curve')

#Set threshold to 55 mV
exp1.add_site(2250, tetrodes=[5,8])
exp1.add_session('14-19-06', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2300, tetrodes=[2,5,8])
exp1.add_session('14-24-26', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2350, tetrodes=[2,5,6,7,8])
exp1.add_session('14-26-39', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2400, tetrodes=[2,5,6,7,8])
exp1.add_session('14-30-20', None, 'noisebursts', 'am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2018-01-24', 'left_AudStr', info='MediallateralDiI')
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; tetrodes

exp2.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.3,
    '2.0':1.6,
    '2.5':1.9,
    '3.0':2.25,
    '3.5':2.6,
    '4.0':2.95
}

#Tetrode 1 has reference; threshold set to 50 mV
exp2.add_site(2500, tetrodes=[])
exp2.add_session('10-54-30', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-56-12', 'a', 'tuningCurve', 'am_tuning_curve')

#Tetrode 2 has reference; threshold set to 42 mV
exp2.add_site(2550, tetrodes=[])
exp2.add_session('11-02-21', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-06-53', 'b', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2650, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('11-12-58', None, 'noisebursts', 'am_tuning_curve')
#Set threshold to 20 mV
exp2.add_session('11-14-45', None, 'noisebursts', 'am_tuning_curve')
#exp2.add_session('11-06-56', 'b', 'tuningCurve', 'am_tuning_curve')

#Set threshold back to 42 mV
exp2.add_site(2700, tetrodes=[8])
exp2.add_session('11-19-14', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(2750, tetrodes=[2])
exp2.add_session('11-22-23', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(2850, tetrodes=[4])
exp2.add_session('11-26-37', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-28-38', 'c', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2900, tetrodes=[4])
exp2.add_session('11-34-49', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-36-31', 'd', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3000, tetrodes=[4])
exp2.add_session('11-42-06', None, 'noisebursts', 'am_tuning_curve')
#Mid recording, signals changed from having large variations coordinated between channels to
#very small signals, more like those seen from silicon probes

exp2.add_site(3100, tetrodes=[])
exp2.add_session('11-48-39', None, 'noisebursts', 'am_tuning_curve')
#Signals returned to how they were previously

#Signals became small again, accompanied briefly by one very strong neuronal signal
exp2.add_site(3200, tetrodes=[4])
exp2.add_session('11-53-21', None, 'noisebursts', 'am_tuning_curve')
#Signals returned to how they were previously
#Discovered there was a leak in the well, which was draining the saline


exp3 = celldatabase.Experiment(subject, '2018-01-27', 'left_AudStr', info='posteriorlateralDiD')
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; tetrodes

exp3.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.25,
    '2.0':1.5,
    '2.5':1.8,
    '3.0':2.15,
    '3.5':2.45,
    '4.0':2.8
}

#Tetrode 1 has reference; threshold set to 42 mV; signals look much better (smoother) than last time
exp3.add_site(2500, tetrodes=[5,7])
exp3.add_session('16-12-53', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(2550, tetrodes=[5,6,7])
exp3.add_session('16-16-38', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-18-49', 'a', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2600, tetrodes=[5,6,7])
exp3.add_session('16-25-30', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(2650, tetrodes=[1,3,4,5,7])
exp3.add_session('16-28-34', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-30-32', 'b', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2750, tetrodes=[3,4,5,6,7])
exp3.add_session('16-37-41', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-39-26', 'c', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2800, tetrodes=[3,4,5,7])
exp3.add_session('16-44-26', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-46-07', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-49-53', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(2850, tetrodes=[1,3,4,5,7,8])
exp3.add_session('17-21-43', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-24-01', 'f', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2900, tetrodes=[1,3,4,5,6,7,8])
exp3.add_session('17-30-29', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-32-36', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('17-35-30', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(2950, tetrodes=[1,3,4,5,6,7,8])
exp3.add_session('18-04-23', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('18-05-52', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('18-08-54', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(3000, tetrodes=[3,4,5,6,7,8])
exp3.add_session('18-37-44', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('18-39-56', 'k', 'tuningCurve', 'am_tuning_curve')
#exp3.add_session('18-08-54', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')
