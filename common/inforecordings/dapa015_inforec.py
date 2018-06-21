from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa015'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-05-22', 'right_AudStr', info=['FacingPosterior', 'AnteriorMidDiI'])
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp0.laserCalibration = {
    '0.5':0.75,
    '1.0':1.05,
    '1.5':1.4,
    '2.0':1.75,
    '2.5':2.1,
    '3.0':2.55,
    '3.5':3.0,
    '4.0':3.6
}

#Tetrode 7 has reference; threshold set to 55mV
exp0.add_site(2900, tetrodes=[1,2,5,6,8])
exp0.add_session('10-47-21', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('10-49-07', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2950, tetrodes=[1,2,5,6,8])
exp0.add_session('10-55-47', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('10-57-08', 'b', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,5,6,8])
#exp0.add_session('11-04-15', None, 'noisebursts', 'am_tuning_curve')
#exp0.add_session('11-04-15', 'c', 'tuningCurve', 'am_tuning_curve') #Forgot to reset session; repeating these two
exp0.add_session('11-11-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-12-12', 'd', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3050, tetrodes=[1,2,5,6,8])
exp0.add_session('11-21-45', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-23-08', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3100, tetrodes=[1,2,6,7,8])
#exp0.add_session('11-32-53', None, 'noisebursts', 'am_tuning_curve')
#moved reference to tetrode 5
exp0.add_session('11-34-35', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-36-15', 'f', 'tuningCurve', 'am_tuning_curve')

#moved reference to tetrode 7
exp0.add_site(3150, tetrodes=[1,2,5,6,8])
exp0.add_session('11-41-12', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-42-57', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-47-10', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,2,5,6,8])
exp0.add_session('12-40-04', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-41-13', 'i', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3250, tetrodes=[1,2,5,6,8])
exp0.add_session('12-53-04', None, 'noisebursts', 'am_tuning_curve')
#exp0.add_session('12-54-17', 'j', 'tuningCurve', 'am_tuning_curve') #forgot to save behavior data
exp0.add_session('12-57-31', 'j', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-00-01', 'k', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(3300, tetrodes=[1,2,5,6,8])
exp0.add_session('14-07-57', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-09-16', 'l', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3350, tetrodes=[1,2,5,6,8])
exp0.add_session('14-22-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-24-05', 'm', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[1,2,5,6,8])
exp0.add_session('14-29-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-30-24', 'n', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3450, tetrodes=[1,2,5,6,8])
exp0.add_session('14-35-38', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-36-55', 'o', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-40-49', 'p', 'laserTuningCurve', 'laser_am_tuning_curve')
exp0.add_session('15-13-41', 'q', 'laserTuningCurve', 'laser_am_tuning_curve') #Control test

exp0.maxDepth = 3450


exp1 = celldatabase.Experiment(subject, '2018-05-24', 'right_AudStr', info=['FacingPosterior', 'PosteriorMidDiD'])
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp1.laserCalibration = {
    '0.5':0.75,
    '1.0':1.05,
    '1.5':1.35,
    '2.0':1.75,
    '2.5':2.1,
    '3.0':2.5,
    '3.5':2.9,
    '4.0':3.4
}

#Tetrode 5 has reference; threshold set to 55mV
exp1.add_site(2900, tetrodes=[1,2,6,7,8])
exp1.add_session('12-09-28', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-11-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-14-25', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')
exp1.add_session('12-45-21', 'c', 'laserTuningCurve', 'laser_am_tuning_curve') #aborted early
exp1.add_session('12-51-16', 'd', 'laserAM', 'laser_am_tuning_curve')

exp1.add_site(2950, tetrodes=[1,2,6,7,8])
exp1.add_session('13-11-08', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-14-50', 'e', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[1,2,6,7,8])
exp1.add_session('13-24-09', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-26-28', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-29-59', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')
exp1.add_session('14-01-16', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3050, tetrodes=[1,2,6,7,8])
exp1.add_session('14-37-15', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-38-38', 'i', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-42-22', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')
exp1.add_session('15-11-29', 'k', 'laserAM', 'laser_am_tuning_curve')

exp1.add_site(3100, tetrodes=[1,2,6,7,8])
exp1.add_session('15-28-11', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-29-29', 'l', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-32-23', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')
exp1.add_session('16-01-51', 'n', 'laserAM', 'laser_am_tuning_curve')

exp1.add_site(3150, tetrodes=[1,2,6,7,8])
exp1.add_session('16-18-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-20-04', 'o', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3200, tetrodes=[1,2,6,7,8])
exp1.add_session('16-23-55', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-25-12', 'p', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3250, tetrodes=[1,2,6,7,8])
exp1.add_session('16-37-06', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-38-22', 'q', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-41-32', 'r', 'laserTuningCurve', 'laser_am_tuning_curve')
exp1.add_session('17-10-37', 's', 'laserAM', 'laser_am_tuning_curve')

exp1.maxDepth = 3250


exp2 = celldatabase.Experiment(subject, '2018-05-28', 'right_AudStr', info=['FacingPosterior', 'PosteriorDiI'])
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp2.laserCalibration = {
    '0.5':0.75,
    '1.0':1.05,
    '1.5':1.4,
    '2.0':1.85,
    '2.5':2.15,
    '3.0':2.6,
    '3.5':3.05,
    '4.0':3.8
}

#Tetrode 5 has reference; threshold set to 55mV
exp2.add_site(2900, tetrodes=[1,2,6,7,8])
exp2.add_session('10-50-00', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-51-55', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-54-58', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')
exp2.add_session('11-24-57', 'c', 'laserAM', 'laser_am_tuning_curve')

#Tetrode 8 has reference; threshold set to 55mV
exp2.add_site(2950, tetrodes=[1,2,6,7,8])
exp2.add_session('12-50-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-51-31', 'd', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-54-51', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')
exp2.add_session('13-25-46', 'f', 'laserTuningCurve', 'laser_am_tuning_curve') #control

exp2.add_site(3000, tetrodes=[1,2,6,7,8])
exp2.add_session('14-15-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-16-44', 'g', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-19-14', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')
exp2.add_session('14-48-27', 'i', 'laserAM', 'laser_am_tuning_curve')

exp2.add_site(3050, tetrodes=[1,2,6,7,8])
exp2.add_session('15-06-08', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-07-25', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-09-52', 'k', 'laserTuningCurve', 'laser_am_tuning_curve')
exp2.add_session('15-41-02', 'l', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.maxDepth = 3050


exp3 = celldatabase.Experiment(subject, '2018-05-29', 'left_AudStr', info=['FacingPosterior', 'AnteriorMidDiI'])
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp3.laserCalibration = {
    '0.5':0.75,
    '1.0':1.1,
    '1.5':1.5,
    '2.0':1.9,
    '2.5':2.25,
    '3.0':2.75,
    '3.5':3.25,
    '4.0':4.0
}

#Tetrode 5 has reference; threshold set to 55mV
exp3.add_site(2900, tetrodes=[1,2,6,7,8])
exp3.add_session('13-39-03', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-40-48', 'a', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2950, tetrodes=[1,2,6,7,8])
exp3.add_session('13-57-54', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-59-25', 'b', 'tuningCurve', 'am_tuning_curve')

#Tetrode 7 has reference
exp3.add_site(3000, tetrodes=[1,2,5,6,8])
exp3.add_session('14-44-23', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-45-47', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-49-07', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')
exp3.add_session('15-22-44', 'g', 'laserAM', 'laser_am_tuning_curve')

#Tetrode 7 has reference
exp3.add_site(3050, tetrodes=[1,2,5,6,8])
exp3.add_session('15-45-06', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-46-47', 'h', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-50-19', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')
exp3.add_session('16-19-24', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

#Tetrode 6 has reference
exp3.add_site(3100, tetrodes=[1,2,5,7,8])
exp3.add_session('16-50-42', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-51-59', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-55-19', 'l', 'laserTuningCurve', 'laser_am_tuning_curve')
exp3.add_session('17-25-00', 'm', 'laserAM', 'laser_am_tuning_curve')

exp3.add_site(3150, tetrodes=[1,2,5,7,8])
exp3.add_session('17-41-54', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-43-08', 'n', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('17-47-08', 'o', 'laserTuningCurve', 'laser_am_tuning_curve')
exp3.add_session('18-21-04', 'p', 'laserAM', 'laser_am_tuning_curve')

exp3.maxDepth = 3150


exp4 = celldatabase.Experiment(subject, '2018-05-30', 'left_AudStr', info=['FacingPosterior', 'PosteriorMidDiD'])
experiments.append(exp4)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp4.laserCalibration = {
    '0.5':0.75,
    '1.0':1.05,
    '1.5':1.35,
    '2.0':1.7,
    '2.5':2.0,
    '3.0':2.4,
    '3.5':2.85,
    '4.0':3.25
}

#Tetrode 7 has reference; threshold set to 55mV
exp4.add_site(2900, tetrodes=[1,2,5,6,8])
exp4.add_session('12-45-54', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-47-45', 'a', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(2950, tetrodes=[1,2,5,6,8])
exp4.add_session('12-54-07', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-55-26', 'b', 'tuningCurve', 'am_tuning_curve')

#raised threshold to 72mV in order to reduce noise
exp4.add_site(3000, tetrodes=[1,2,5,6,8])
exp4.add_session('13-01-28', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-02-45', 'c', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3050, tetrodes=[1,2,5,6,8])
exp4.add_session('13-07-48', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-09-04', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-11-50', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')
exp4.add_session('13-43-03', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3100, tetrodes=[1,2,5,6,8])
exp4.add_session('14-19-41', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-20-59', 'g', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3150, tetrodes=[1,2,5,6,8])
exp4.add_session('14-27-14', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-28-49', 'h', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3200, tetrodes=[1,2,5,6,8])
exp4.add_session('14-43-54', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-45-09', 'i', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3250, tetrodes=[1,2,5,6,8])
exp4.add_session('14-49-35', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-50-46', 'j', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3300, tetrodes=[1,2,5,6,8])
exp4.add_session('14-56-11', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-57-39', 'k', 'tuningCurve', 'am_tuning_curve')

exp4.add_site(3350, tetrodes=[1,2,5,6,8])
exp4.add_session('15-01-48', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-03-16', 'l', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-06-29', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')
exp4.add_session('15-35-45', 'n', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.maxDepth = 3350


exp5 = celldatabase.Experiment(subject, '2018-06-05', 'left_AudStr', info=['FacingPosterior', 'PosteriorDiI'])
experiments.append(exp4)
#Used both speakers; 2.5 mW for laser; probe DD45

exp5.laserCalibration = {
    '0.5':1.05,
    '1.0':1.9,
    '1.5':2.75,
    '2.0':4.05,
    '2.5':5.15,
    '3.0':6.5,
    '3.5':7.5,
    '4.0':9.8
}

exp5.maxDepth = 0

#Didn't find any signals down to a depth of 3000 nm
