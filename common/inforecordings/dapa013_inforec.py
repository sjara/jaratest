from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa013'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-04-03', 'left_AudStr', info=['FacingPosterior', 'AnteriorDiI'])
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp0.laserCalibration = {
    '0.5':0.85,
    '1.0':1.3,
    '1.5':1.65,
    '2.0':2.0,
    '2.5':2.3,
    '3.0':2.85,
    '3.5':3.35,
    '4.0':4.05
}

#Tetrode 7 has reference; threshold set to 55mV
exp0.add_site(2500, tetrodes=[5,6,8])
exp0.add_session('13-13-44', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-18-20', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[5,6,8])
exp0.add_session('13-24-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-26-17', 'b', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[5,6,8])
exp0.add_session('13-32-24', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2650, tetrodes=[5,6,8])
exp0.add_session('13-38-09', None, 'noisebursts', 'am_tuning_curve')
#exp0.add_session('13-39-44', 'c', 'tuningCurve', 'am_tuning_curve') forgot to save behavior

exp0.add_site(2700, tetrodes=[1,2,4,5,6,8])
exp0.add_session('13-54-28', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-56-53', 'c', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2750, tetrodes=[1,2,4,5,6,8])
exp0.add_session('14-07-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-09-12', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-12-42', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-27-48', 'f', 'laserTuningCurve', 'laser_am_tuning_curve') #had to open the door a couple times to add saline

exp0.add_site(2800, tetrodes=[1,2,4,5,6,8])
exp0.add_session('15-03-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-04-38', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-08-05', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-22-14', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2850, tetrodes=[1,2,4,5])
exp0.add_session('16-00-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-01-39', 'j', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-08-34', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-10-06', 'k', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-13-16', 'l', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-27-15', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,4,8])
exp0.add_session('17-00-31', None, 'noisebursts', 'am_tuning_curve')

exp0.maxDepth = 3000


exp1 = celldatabase.Experiment(subject, '2018-04-04', 'left_AudStr', info=['FacingPosterior', 'AntMidDiD'])
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp1.laserCalibration = {
    '0.5':0.95,
    '1.0':1.6,
    '1.5':2.5,
    '2.0':3.3,
    '2.5':4.6,
    '3.0':6.2,
    '3.5':7.15,
    '4.0':8.1
}

#Tetrode 3 has reference; threshold set to 55mV
exp1.add_site(2700, tetrodes=[2,6,7,8])
exp1.add_session('10-53-30', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-55-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-00-09', 'b', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[1,2])
exp1.add_session('12-37-58', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(3050, tetrodes=[1,2])
exp1.add_session('12-44-41', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-47-04', 'c', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-54-29', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-56-21', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-59-48', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-13-04', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3150, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('13-44-32', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-46-02', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-49-11', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-03-45', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3200, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('14-48-05', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-50-13', 'j', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3250, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('14-56-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-58-37', 'k', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3300, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('15-07-58', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-10-22', 'l', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-13-45', 'm', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-27-00', 'n', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.maxDepth = 3300


exp2 = celldatabase.Experiment(subject, '2018-04-05', 'left_AudStr', info=['FacingPosterior', 'PostMidDiI'])
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp2.laserCalibration = {
    '0.5':0.95,
    '1.0':1.5,
    '1.5':2.0,
    '2.0':2.55,
    '2.5':3.05,
    '3.0':3.9,
    '3.5':4.9,
    '4.0':6.1
    }

#Tetrode 1 has reference; threshold set to 55mV
exp2.add_site(3000, tetrodes=[2,3,4])
exp2.add_session('09-12-00', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-14-00', 'a', 'tuningCurve', 'am_tuning_curve')

#Tetrode 3 has reference
exp2.add_site(3050, tetrodes=[1,2,4])
exp2.add_session('09-29-53', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-32-14', 'b', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3100, tetrodes=[1,2,4])
exp2.add_session('09-40-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-42-12', 'c', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3150, tetrodes=[1,2,4,8])
exp2.add_session('09-49-26', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-51-20', 'd', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3200, tetrodes=[1,2,4,6,8])
exp2.add_session('09-58-19', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-59-53', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-02-56', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-16-05', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(3250, tetrodes=[1,2,6,8])
exp2.add_session('10-48-26', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-49-57', 'h', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3300, tetrodes=[1,2,4,6,8])
exp2.add_session('10-55-20', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-56-51', 'i', 'tuningCurve', 'am_tuning_curve')

#Reference on tetrode 8
exp2.add_site(3350, tetrodes=[1,2,3,4,5,6])
exp2.add_session('11-02-25', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-04-24', 'j', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3400, tetrodes=[1,2,3,4])
exp2.add_session('11-21-52', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-23-30', 'k', 'tuningCurve', 'am_tuning_curve')
#Didn't find anything sound-responsive, so tried at a higher depth

#Reference on tetrode 7
exp2.add_site(2950, tetrodes=[1,2,4,8])
exp2.add_session('11-38-43', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-40-15', 'l', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2900, tetrodes=[1,2,3,4,5,8])
exp2.add_session('11-44-26', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-45-44', 'm', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(2850, tetrodes=[1,2,3,4,5,8])
exp2.add_session('11-51-45', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-53-31', 'n', 'tuningCurve', 'am_tuning_curve')
#Still didn't find anything, so moved back down

exp2.add_site(3450, tetrodes=[1,2,3,4])
exp2.add_session('12-13-41', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-16-50', 'o', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3500, tetrodes=[1,2,3,4,6,8])
exp2.add_session('12-21-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-23-00', 'p', 'tuningCurve', 'am_tuning_curve')

exp2.maxDepth = 3500


exp3 = celldatabase.Experiment(subject, '2018-04-10', 'right_AudStr', info=['FacingPosterior', 'AnteriorDiI'])
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp3.laserCalibration = {
    '0.5':0.95,
    '1.0':1.45,
    '1.5':1.95,
    '2.0':2.55,
    '2.5':3.15,
    '3.0':4.3,
    '3.5':5.25,
    '4.0':6.3
    }

#Tetrode 6 has reference; threshold set to 55mV
exp3.add_site(2750, tetrodes=[2,3,5,7,8])
exp3.add_session('13-30-22', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-33-45', 'a', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2800, tetrodes=[2,3,5,7,8])
exp3.add_session('13-39-06', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-41-29', 'b', 'tuningCurve', 'am_tuning_curve')

#Tetrode 4 has reference
exp3.add_site(2850, tetrodes=[1,2,3,5,7,8])
exp3.add_session('13-47-30', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-49-30', 'c', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2900, tetrodes=[1,2,3,5,7,8])
exp3.add_session('13-55-57', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-57-44', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-01-14', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-15-42', 'f', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(2950, tetrodes=[2,3,5,6,7,8])
exp3.add_session('14-51-18', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-53-21', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-56-43', 'h', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-10-02', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(3000, tetrodes=[2,6,7,8])
exp3.add_session('15-40-20', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-41-54', 'j', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3050, tetrodes=[1,2,3,6,7,8])
exp3.add_session('15-47-45', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-49-24', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-55-13', 'l', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-08-31', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(3100, tetrodes=[1,2,3,6,7,8])
exp3.add_session('16-38-27', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-40-13', 'n', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3150, tetrodes=[1,2,3,6,7,8])
exp3.add_session('16-45-05', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-46-49', 'o', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3200, tetrodes=[1,2,5,6,7,8])
exp3.add_session('16-51-22', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-53-23', 'p', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3250, tetrodes=[1,2,5,6,7,8])
exp3.add_session('16-57-31', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-59-29', 'q', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(3300, tetrodes=[1,2,5,6,7,8])
exp3.add_session('17-05-08', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-06-48', 'r', 'tuningCurve', 'am_tuning_curve')

exp3.maxDepth = 3300


exp4 = celldatabase.Experiment(subject, '2018-04-12', 'right_AudStr', info=['FacingPosterior', 'AnteriorMidDiD'])
experiments.append(exp4)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp4.laserCalibration = {
    '0.5':0.9,
    '1.0':1.25,
    '1.5':1.65,
    '2.0':2.05,
    '2.5':2.5,
    '3.0':3.1,
    '3.5':3.9,
    '4.0':4.65
    }

#Tetrode 7 has reference; threshold set to 55mV
exp4.add_site(2900, tetrodes=[3,4,5,6,8])
exp4.add_session('10-45-57', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-47-32', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-50-39', 'b', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-04-19', 'c', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(2950, tetrodes=[1,3,4,5,6,8])
exp4.add_session('11-36-19', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-38-36', 'd', 'tuningCurve', 'am_tuning_curve')

#Tetrode 8 has reference
exp4.add_site(3000, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('11-46-17', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-47-56', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-52-04', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-05-36', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3050, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('12-36-13', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-37-46', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-41-32', 'i', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-08-12', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3100, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('13-40-23', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-42-46', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-46-30', 'l', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-01-01', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3150, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('14-31-40', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-33-33', 'n', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-36-32', 'o', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-50-02', 'p', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3200, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('15-20-38', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-22-12', 'q', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-25-35', 'r', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-39-07', 's', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.add_site(3250, tetrodes=[1,2,3,4,5,6,7])
exp4.add_session('16-09-55', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-11-29', 't', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-14-37', 'u', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-28-25', 'v', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.maxDepth = 3250


exp5 = celldatabase.Experiment(subject, '2018-04-13', 'right_AudStr', info=['FacingPosterior', 'PosteriorMidDiI'])
experiments.append(exp5)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp5.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.35,
    '2.0':1.65,
    '2.5':2.0,
    '3.0':2.4,
    '3.5':2.75,
    '4.0':3.2
    }

#Tetrode 5 has reference; threshold set to 55mV
exp5.add_site(2900, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('10-56-18', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('10-58-18', 'a', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2950, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('11-04-13', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-05-32', 'b', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3000, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('11-13-21', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-14-39', 'c', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3050, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('11-19-04', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-20-27', 'd', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3100, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('11-31-30', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-32-53', 'e', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3150, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('11-37-19', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-38-40', 'f', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('11-41-29', 'g', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('11-54-47', 'h', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3200, tetrodes=[6,7,8])
exp5.add_session('12-25-27', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('12-27-14', 'i', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-30-15', 'j', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-44-04', 'k', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3250, tetrodes=[6,7,8])
exp5.add_session('13-15-48', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-17-34', 'l', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(3300, tetrodes=[6,7,8])
exp5.add_session('13-23-17', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-24-31', 'm', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-27-49', 'n', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-42-15', 'o', 'laserTuningCurve', 'laser_am_tuning_curve')

#Tetrode 6 has reference
exp5.add_site(3350, tetrodes=[5,7,8])
exp5.add_session('14-12-26', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-13-52', 'p', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-17-37', 'q', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-31-05', 'r', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3400, tetrodes=[5,8])
exp5.add_session('15-00-43', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-01-52', 's', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-04-20', 't', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-17-46', 'u', 'laserTuningCurve', 'laser_am_tuning_curve')

exp5.add_site(3450, tetrodes=[8])
exp5.add_session('15-47-58', None, 'noisebursts', 'am_tuning_curve')

exp5.add_site(3500, tetrodes=[7,8])
exp5.add_session('15-50-26', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-51-43', 'v', 'tuningCurve', 'am_tuning_curve')

exp5.maxDepth = 3500


exp6 = celldatabase.Experiment(subject, '2018-04-17', 'right_AudStr', info=['FacingPosterior', 'PosteriorDiD'])
experiments.append(exp6)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp6.laserCalibration = {
    '0.5':0.8,
    '1.0':1.2,
    '1.5':1.6,
    '2.0':2.1,
    '2.5':2.5,
    '3.0':3.15,
    '3.5':3.9,
    '4.0':4.7
}

#Tetrode 6 has reference; threshold set to 55mV
exp6.add_site(2900, tetrodes=[1,2,3,4])
exp6.add_session('13-44-31', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('13-48-53', 'a', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(2950, tetrodes=[1,2,3,4])
exp6.add_session('14-02-45', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-06-04', 'b', 'tuningCurve', 'am_tuning_curve')

#Tetrode 5 has reference
exp6.add_site(3000, tetrodes=[1,2,3,4,6])
exp6.add_session('14-16-36', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-18-13', 'c', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('14-21-44', 'd', 'tuningCurve', 'am_tuning_curve') #Attempted to record video, but video failed

exp6.add_site(3050, tetrodes=[1,2,3,4])
exp6.add_session('14-34-46', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-36-11', 'e', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('14-41-27', 'f', 'tuningCurve', 'am_tuning_curve') #Reduced number of freqs to test movement artifacts

exp6.add_site(3100, tetrodes=[1,2,3,4])
exp6.add_session('14-46-13', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-47-36', 'g', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(3150, tetrodes=[1,2,3,4,6])
exp6.add_session('14-53-50', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-55-22', 'h', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('14-58-07', 'i', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('15-11-35', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

exp6.add_site(3200, tetrodes=[1,2,3,4,6])
exp6.add_session('15-44-32', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('15-45-59', 'k', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(3250, tetrodes=[1,2,3,4,6])
exp6.add_session('15-52-24', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('15-53-39', 'l', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('15-56-29', 'm', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('16-09-54', 'n', 'laserTuningCurve', 'laser_am_tuning_curve')

exp6.add_site(3300, tetrodes=[2,3,4])
exp6.add_session('16-39-38', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-41-30', 'o', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(3350, tetrodes=[1,2,3,4,6])
exp6.add_session('16-45-57', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-47-16', 'p', 'tuningCurve', 'am_tuning_curve')

exp6.add_site(3400, tetrodes=[1,2,3,4,6])
exp6.add_session('16-51-56', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('16-53-03', 'q', 'tuningCurve', 'am_tuning_curve')

exp6.maxDepth = 3400