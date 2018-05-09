from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa014'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-04-23', 'left_AudStr', info=['FacingPosterior', 'AnteriorDiI'])
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp0.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.8,
    '2.0':2.3,
    '2.5':2.8,
    '3.0':3.4,
    '3.5':4.25,
    '4.0':5.05
}

#Tetrode 7 has reference; threshold set to 55mV
exp0.add_site(2900, tetrodes=[1,3,4,5,6])
exp0.add_session('16-05-43', None, 'noisebursts', 'am_tuning_curve')
#Lots of noise; couldn't find any useable signals

exp1 = celldatabase.Experiment(subject, '2018-04-24', 'left_AudStr', info=['FacingPosterior', 'AnteriorMidDiD'])
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp1.laserCalibration = {
    '0.5':0.95,
    '1.0':1.55,
    '1.5':2.1,
    '2.0':2.7,
    '2.5':3.3,
    '3.0':4.3,
    '3.5':5.3,
    '4.0':6.4
}

#Tetrode 1 has reference; threshold set to 55mV
exp1.add_site(2900, tetrodes=[2,3,4,5,6])
exp1.add_session('13-03-16', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-05-07', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2950, tetrodes=[2,3,4,5,6])
exp1.add_session('13-11-46', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-14-38', 'b', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[2,3,4,5,6])
exp1.add_session('13-21-09', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-23-10', 'c', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-29-00', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-43-51', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3050, tetrodes=[2,3,4,5,6])
exp1.add_session('14-23-44', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-25-34', 'f', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[2,3,4,5,6])
exp1.add_session('14-31-05', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-33-07', 'g', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3150, tetrodes=[2,3,4,5,6])
exp1.add_session('14-38-45', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-40-50', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-44-28', 'i', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-58-10', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3200, tetrodes=[2,3,4,5,6])
exp1.add_session('15-28-33', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-30-14', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-34-13', 'l', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-47-23', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3250, tetrodes=[2,3,4,5,6])
exp1.add_session('16-17-32', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-18-40', 'n', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-22-19', 'o', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-35-28', 'p', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3300, tetrodes=[2,3,4,5,6])
exp1.add_session('17-04-57', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('17-06-41', 'q', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-09-16', 'r', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-22-23', 's', 'laserTuningCurve', 'laser_am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2018-04-25', 'left_AudStr', info=['FacingPosterior', 'PosteriorMidDiI'])
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp2.laserCalibration = {
    '0.5':0.75,
    '1.0':1.1,
    '1.5':1.5,
    '2.0':1.95,
    '2.5':2.3,
    '3.0':2.8,
    '3.5':3.3,
    '4.0':4.0
}

#Tetrode 1 has reference; threshold set to 55mV
exp2.add_site(2900, tetrodes=[2,3,4,5,6])
exp2.add_session('12-09-48', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-11-53', 'a', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2950, tetrodes=[2,3,4,5,6])
exp2.add_session('12-17-38', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-19-01', 'b', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-22-02', 'c', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-35-15', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3000, tetrodes=[2,3,4,5,6])
exp2.add_session('13-07-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-09-17', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-11-51', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-24-59', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3050, tetrodes=[2,3,4,5,6])
exp2.add_session('13-55-45', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-57-37', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-01-11', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-15-19', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3100, tetrodes=[2,3,4,5,6])
exp2.add_session('14-48-37', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-49-57', 'k', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3150, tetrodes=[2,3,4,5,6])
exp2.add_session('14-53-41', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-54-58', 'l', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-57-30', 'm', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-11-42', 'n', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3200, tetrodes=[2,3,4,5,6])
exp2.add_session('15-42-27', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-43-40', 'o', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-45-59', 'p', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-59-04', 'q', 'laserTuningCurve', 'laser_am_tuning_curve')


exp3 = celldatabase.Experiment(subject, '2018-04-26', 'left_AudStr', info=['FacingPosterior', 'PosteriorDiD'])
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp3.laserCalibration = {
    '0.5':0.8,
    '1.0':1.2,
    '1.5':1.6,
    '2.0':2.0,
    '2.5':2.25,
    '3.0':3.3,
    '3.5':3.9,
    '4.0':4.5
}

#Tetrode 1 has reference; threshold set to 55mV
exp3.add_site(2900, tetrodes=[1,2,3,4,6])
exp3.add_session('12-30-10', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-34-33', 'a', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2950, tetrodes=[1,2,3,4,6])
exp3.add_session('12-41-14', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-43-30', 'b', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-47-30', 'c', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-00-46', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

#Tetrode 4 has reference; threshold set to 55mV
exp3.add_site(3000, tetrodes=[1,2,3,5,6])
exp3.add_session('13-32-52', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-35-21', 'e', 'tuningCurve', 'am_tuning_curve')

#Tetrode 3 has reference; threshold set to 55mV
exp3.add_site(3050, tetrodes=[1,2,4,5,6])
exp3.add_session('13-44-42', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-48-01', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-52-03', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-05-15', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(3100, tetrodes=[1,2,4,5,6])
exp3.add_session('14-36-10', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-38-21', 'i', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3150, tetrodes=[1,2,4,5,6])
exp3.add_session('14-43-51', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-46-53', 'j', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-50-38', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-03-51', 'l', 'laserTuningCurve', 'laser_am_tuning_curve')


exp4 = celldatabase.Experiment(subject, '2018-05-03', 'right_AudStr', info=['FacingPosterior', 'AnteriorDiI'])
experiments.append(exp4)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp4.laserCalibration = {
    '0.5':0.8,
    '1.0':1.25,
    '1.5':1.7,
    '2.0':2.3,
    '2.5':2.65,
    '3.0':3.3,
    '3.5':4.0,
    '4.0':4.7
}

#Didn't end up recording
#Tetrode 1 has reference; threshold set to 55mV


exp5 = celldatabase.Experiment(subject, '2018-05-08', 'right_AudStr', info=['FacingPosterior', 'AnteriorMidDiI'])
experiments.append(exp5)
#Used both speakers; 2.5 mW for laser; probe DAF6

exp5.laserCalibration = {
    '0.5':0.75,
    '1.0':1.1,
    '1.5':1.45,
    '2.0':1.85,
    '2.5':2.4,
    '3.0':2.7,
    '3.5':3.15,
    '4.0':3.8
}

#Tetrode 6 has reference; threshold set to 55mV
exp5.add_site(2900, tetrodes=[1,2,3,4,5])
exp5.add_session('11-51-40', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-53-21', 'a', 'tuningCurve', 'am_tuning_curve')

#Tetrode 7 has reference; threshold set to 55mV
exp5.add_site(2950, tetrodes=[1,2,3,4,5,6])
exp5.add_session('11-58-35', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('12-00-00', 'b', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-04-07', 'c', 'tuningCurve', 'am_tuning_curve')
#exp5.add_session('12-18-38', 'd', 'laserTuningCurve', 'laser_am_tuning_curve') #Forgot to save behavior data

#Tetrode 1 has reference
exp5.add_site(3000, tetrodes=[2,3,4,5,6])
exp5.add_session('12-53-49', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('12-58-07', 'e', 'tuningCurve', 'am_tuning_curve')

#Tetrode 7 has reference
exp5.add_site(3050, tetrodes=[1,2,3,4,5,6])
exp5.add_session('13-04-04', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-05-54', 'f', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3100, tetrodes=[1,2,3,4,5,6])
exp5.add_session('13-10-38', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-11-59', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-15-34', 'h', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-28-48', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3150, tetrodes=[1,2,3,4,5,6])
exp5.add_session('14-03-11', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-06-43', 'j', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3200, tetrodes=[1,2,3,4,5,6])
exp5.add_session('14-14-53', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-16-23', 'k', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-19-51', 'l', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-33-24', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3250, tetrodes=[1,2,3,4,5,6])
exp5.add_session('15-04-44', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-07-08', 'n', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3300, tetrodes=[1,2,3,4,5,6])
exp5.add_session('15-12-55', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-14-20', 'o', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3350, tetrodes=[1,2,3,4,5,6])
exp5.add_session('15-22-15', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-23-44', 'p', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-27-13', 'q', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-40-23', 'r', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3400, tetrodes=[1,2,3,4,5,6])
exp5.add_session('16-12-26', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-14-06', 's', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-17-37', 't', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-30-46', 'u', 'laserTuningCurve', 'laser_am_tuning_curve')
