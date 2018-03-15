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


exp1 = celldatabase.Experiment(subject, '2018-02-06', 'left_AudStr', info='MidAnteriorMedialDiD')
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; probe 76B1 (from Anna)

exp1.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.3,
    '2.0':1.6,
    '2.5':1.9,
    '3.0':2.3,
    '3.5':2.65,
    '4.0':3.05
}

#Tetrode 3 has reference; threshold set to 55mV
exp1.add_site(2500, tetrodes=[4])
exp1.add_session('13-18-35', None, 'noisebursts', 'am_tuning_curve')

#Not much activity; possibly issues with ground?
exp1.add_site(2650, tetrodes=[4])
exp1.add_session('13-24-13', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-25-43', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2700, tetrodes=[2,4])
exp1.add_session('13-29-41', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2775, tetrodes=[2])
exp1.add_session('13-41-05', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2850, tetrodes=[1,2])
exp1.add_session('13-44-42', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2900, tetrodes=[1,2])
exp1.add_session('13-48-25', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2950, tetrodes=[1,2])
exp1.add_session('13-54-34', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-56-02', 'b', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[2])
exp1.add_session('14-01-56', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-03-31', 'c', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3050, tetrodes=[2])
exp1.add_session('14-09-44', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[2,4])
exp1.add_session('14-20-35', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(3150, tetrodes=[1,2,4])
exp1.add_session('14-24-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-26-00', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-28-52', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-39-45', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2018-02-07', 'left_AudStr', info='MedialMedialDiI')
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; probe 76B1 (from Anna)

exp2.laserCalibration = {
    '0.5':0.7,
    '1.0':1.55,
    '1.5':2.2,
    '2.0':2.9,
    '2.5':3.8,
    '3.0':4.85,
    '3.5':4.0,
    '4.0':6.75
}

#Tetrode 3 has reference; threshold set to 55mV
exp2.add_site(2500, tetrodes=[2])
exp2.add_session('11-02-18', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(2600, tetrodes=[2])
exp2.add_session('11-09-41', None, 'noisebursts', 'am_tuning_curve')
#exp2.add_session('14-26-00', 'a', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2650, tetrodes=[2,6])
exp2.add_session('11-13-15', None, 'noisebursts', 'am_tuning_curve')
#exp2.add_session('14-26-00', 'a', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2700, tetrodes=[2,4])
exp2.add_session('11-16-40', None, 'noisebursts', 'am_tuning_curve')
#exp2.add_session('14-26-00', 'a', 'tuningCurve', 'am_tuning_curve')

#Set threshold to 42 mV to try and find more signals
exp2.add_site(2750, tetrodes=[1,2,4,5,6,7])
exp2.add_session('11-20-34', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-22-04', 'a', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2800, tetrodes=[1,2,4,5,6])
exp2.add_session('11-26-31', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-28-07', 'b', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2850, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('11-33-56', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-35-14', 'c', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2900, tetrodes=[1,2,4,5,6])
exp2.add_session('11-39-35', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-41-50', 'd', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2950, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('11-46-45', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(3000, tetrodes=[1,2,4,5,6])
exp2.add_session('11-50-03', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-52-18', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-57-02', 'f', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3100, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('12-15-14', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-16-27', 'g', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3150, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('12-21-24', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-23-18', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-25-46', 'i', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3200, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('12-43-19', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-44-43', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-47-15', 'k', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-02-44', 'l', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3250, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('13-33-13', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-34-37', 'm', 'tuningCurve', 'am_tuning_curve')


exp3 = celldatabase.Experiment(subject, '2018-02-13', 'left_AudStr', info='PosteriorMedialDiD')
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; probe 76B1 (from Anna)

exp3.laserCalibration = {
    '0.5':0.9,
    '1.0':1.25,
    '1.5':1.75,
    '2.0':2.25,
    '2.5':2.7,
    '3.0':3.3,
    '3.5':4.2,
    '4.0':5.0
}

#Tetrode 3 has reference; threshold set to 55mV
exp3.add_site(2600, tetrodes=[])
exp3.add_session('13-20-30', None, 'noisebursts', 'am_tuning_curve')
#No real signals down to a depth of 3000; decided to stop to see if I can figure out why


exp4 = celldatabase.Experiment(subject, '2018-02-14', 'right_AudStr', info='AnteriorMedialDiI')
experiments.append(exp4)
exp4.laserCalibration = {
    '0.5':0.7,
    '1.0':0.85,
    '1.5':1.05,
    '2.0':1.3,
    '2.5':1.5,
    '3.0':1.85,
    '3.5':2.1,
    '4.0':2.4
}

#Tetrode 3 has reference; threshold set to 55mV
exp4.add_site(2550, tetrodes=[2,4,6,7])
exp4.add_session('10-16-00', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-17-42', 'a', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2600, tetrodes=[1,2,4,6])
exp4.add_session('10-21-55', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(2650, tetrodes=[1,2,4,6,8])
exp4.add_session('10-25-30', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-27-08', 'b', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2700, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('10-31-45', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-33-11', 'c', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2750, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('10-36-50', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-38-08', 'd', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2800, tetrodes=[1,2,4,6,7,8])
exp4.add_session('10-42-07', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(2850, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('10-44-22', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-45-43', 'e', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2900, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('10-50-42', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-52-00', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-55-40', 'g', 'tuningCurve', 'am_tuning_curve') #two freqs, longer ISI; full tuning curve session

exp4.add_site(2950, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('11-12-04', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-13-27', 'h', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3000, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('11-17-30', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-19-15', 'i', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3050, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('11-23-39', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-24-57', 'j', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3100, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('11-30-25', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-31-58', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-34-48', 'l', 'tuningCurve', 'am_tuning_curve') #two freqs, longer ISI; full tuning curve session
exp4.add_session('11-50-17', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3150, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('12-20-14', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-21-37', 'n', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-24-14', 'o', 'tuningCurve', 'am_tuning_curve') #two freqs, longer ISI; full tuning curve session
exp4.add_session('12-40-15', 'p', 'laserTuningCurve', 'laser_am_tuning_curve')



exp5 = celldatabase.Experiment(subject, '2018-02-20', 'right_AudStr', info='PosteriorMiddleDiD')
experiments.append(exp5)
exp5.laserCalibration = {
    '0.5':0.95,
    '1.0':1.5,
    '1.5':2.1,
    '2.0':2.8,
    '2.5':3.7,
    '3.0':4.8,
    '3.5':6.1,
    '4.0':6.9
}

#Tetrode 3 has reference; threshold set to 55mV
exp5.add_site(2500, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('12-47-55', None, 'noisebursts', 'am_tuning_curve')
#Signals super noisy, with coordinated activity across tetrodes; Nick and Anna couldn't find anything specifically wrong
#other than the optical fiber being deflected, so I'll take the probe out and test it


exp6 = celldatabase.Experiment(subject, '2018-02-21', 'right_AudStr', info='PosteriorMiddleDiD')
experiments.append(exp6)
exp6.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.2,
    '2.0':1.5,
    '2.5':1.8,
    '3.0':2.1,
    '3.5':2.45,
    '4.0':2.8
}

#Tetrode 3 has reference; threshold set to 55mV
#Still seeing some coordinated activity across tetrodes, especially on 4 and 6, but the signals aren't as high,
#and for the most part don't cross the threshold; noise bursts and the laser don't seem
#to affect this coordinated activity, so I iwill try to record with the probe
exp6.add_site(2500, tetrodes=[1,2,4,5,6,7,8])
exp6.add_session('10-03-25', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2550, tetrodes=[2,5,6,7,8])
exp6.add_session('10-07-26', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2600, tetrodes=[2,5,6,7,8])
exp6.add_session('10-15-44', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2650, tetrodes=[2,5,6,7,8])
exp6.add_session('10-28-47', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2750, tetrodes=[5,6,7,8])
exp6.add_session('10-33-45', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2800, tetrodes=[4,5,6,7,8])
exp6.add_session('10-38-46', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2850, tetrodes=[6,7,8])
exp6.add_session('10-43-01', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2900, tetrodes=[])
exp6.add_session('10-52-22', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(2950, tetrodes=[])
exp6.add_session('10-56-51', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(3000, tetrodes=[2,5,6,7,8])
exp6.add_session('11-00-39', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('11-02-36', 'b', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(3050, tetrodes=[2,5,6,7,8])
exp6.add_session('11-10-59', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(3100, tetrodes=[2,5,6,7,8])
exp6.add_session('11-10-59', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(3150, tetrodes=[2,5,6,7,8])
exp6.add_session('11-29-53', None, 'noisebursts', 'am_tuning_curve')


#On 2018-02-22, tested with fresh probe; didn't see coordinated activity
#across tetrodes, but also didn't see any other activity
