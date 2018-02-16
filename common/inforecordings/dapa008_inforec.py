from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa008'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-11-05', 'left_AudStr', info='AnteriorfacingPosteriorDiI')
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.75,
    '1.0':1.1,
    '1.5':1.5,
    '2.0':1.9,
    '2.5':2.3,
    '3.0':2.75,
    '3.5':3.25,
    '4.0':3.9
}

exp0.add_site(2000, tetrodes=[7,8])
exp0.add_session('17-26-05', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2050, tetrodes=[7,8])
exp0.add_session('17-40-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-42-49', 'a', 'tuningCurve', 'am_tuning_curve') #forgot to save behavior

exp0.add_site(2100, tetrodes=[7,8])
exp0.add_session('18-12-41', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-15-39', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2150, tetrodes=[7,8])
exp0.add_session('18-49-17', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-51-58', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2300, tetrodes=[7,8])
exp0.add_session('19-36-38', None, 'noisebursts', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-11-08', 'left_AudStr', info='MedialfacingPosteriorDiD')
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.4,
    '1.0':1.8,
    '1.5':2.3,
    '2.0':2.75,
    '2.5':3.15,
    '3.0':3.8,
    '3.5':4.5,
    '4.0':5.3
}

exp1.add_site(2000, tetrodes=[7,8])
exp1.add_session('13-16-47', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2100, tetrodes=[7,8])
exp1.add_session('13-24-34', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2150, tetrodes=[7,8])
exp1.add_session('13-30-37', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2200, tetrodes=[7,8])
exp1.add_session('13-39-50', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2250, tetrodes=[7,8])
exp1.add_session('13-45-08', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-47-55', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2300, tetrodes=[7,8])
exp1.add_session('14-18-18', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-20-59', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2350, tetrodes=[7,8])
exp1.add_session('14-52-37', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-54-50', 'c', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2400, tetrodes=[7,8])
exp1.add_session('15-25-21', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-27-34', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2017-11-21', 'left_AudStr', info='MedialfacingPosteriorDiI')
experiments.append(exp2)
#Both speakers plugged in; 2.5 mW

exp2.laserCalibration = {
    '0.5':1.2,
    '1.0':2.1,
    '1.5':3.3,
    '2.0':4.75,
    '2.5':6.2,
    '3.0':7.45,
    '3.5':10.0
}

exp2.add_site(2000, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('17-07-16', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-10-22', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(2050, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('17-49-12', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-51-52', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(2150, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('18-51-15', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('18-53-30', 'c', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(2250, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('19-34-46', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('19-37-01', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

exp2.add_site(2300, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('20-29-10', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('19-37-01', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3 = celldatabase.Experiment(subject, '2017-11-22', 'left_AudStr', info='PosteriorfacingPosteriorDiD')
experiments.append(exp3)
#Both speakers plugged in; 2.5 mW

exp3.laserCalibration = {
    '0.5':0.7,
    '1.0':0.9,
    '1.5':1.25,
    '2.0':1.6,
    '2.5':1.9,
    '3.0':2.3,
    '3.5':3.65
}

exp3.add_site(2000, tetrodes=[1])
exp3.add_session('12-29-06', None, 'noisebursts', 'am_tuning_curve')
#Set threshold to 55 mv due to background non-spike shape responses
exp3.add_session('12-33-57', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-36-37', 'a', 'laserTuningCurve', 'laser_am_tuning_curve')

exp3.add_site(2050, tetrodes=[1,5,6,7,8])
exp3.add_session('13-34-07', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-38-11', 'b', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2100, tetrodes=[3,4,5,6,7,8])
exp3.add_session('13-45-15', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-49-09', 'c', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2150, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('13-52-19', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-49-09', 'd', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2175, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('13-58-51', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-00-27', 'e', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2200, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-03-10', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-05-49', 'f', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2250, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-09-03', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-10-52', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-14-08', 'h', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2300, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-17-15', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-18-59', 'i', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2350, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-22-20', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-23-48', 'j', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2400, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-26-50', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-28-13', 'k', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-30-34', 'l', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2450, tetrodes=[1,2,6,7,8])
exp3.add_session('14-35-12', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-37-06', 'm', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2500, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('14-40-22', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-41-45', 'n', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2550, tetrodes=[1,2,3,6,7,8])
exp3.add_session('14-46-02', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-47-51', 'o', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2600, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('14-50-35', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-53-05', 'p', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2650, tetrodes=[1,2,4])
exp3.add_session('14-58-28', None, 'noisebursts', 'am_tuning_curve') #looks like two neuron on tet 4
exp3.add_session('15-00-20', 'q', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2700, tetrodes=[1,2,4,8])
exp3.add_session('15-04-23', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-06-49', 'r', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2750, tetrodes=[1,2,3,4,5,8])
exp3.add_session('15-09-32', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-10-53', 's', 'tuningCurve', 'am_tuning_curve')

exp3.add_site(2800, tetrodes=[1,2,3,4,7,8])
exp3.add_session('15-13-39', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-14-53', 't', 'tuningCurve', 'am_tuning_curve')


exp4 = celldatabase.Experiment(subject, '2017-11-24', 'right_AudStr', info='PosteriorfacingPosteriorDiI')
experiments.append(exp4)
#Both speakers plugged in; 2.5 mW

exp4.laserCalibration = {
    '0.5':0.8,
    '1.0':1.2,
    '1.5':1.65,
    '2.0':2.1,
    '2.5':2.6,
    '3.0':3.2,
    '3.5':3.85
}

#Probe messed up; couldn't record

exp5 = celldatabase.Experiment(subject, '2017-11-29', 'right_AudStr', info='PosteriorfacingPosteriorDiD')
experiments.append(exp5)
#Both speakers plugged in; 2.5 mW

exp5.laserCalibration = {
    '0.5':0.75,
    '1.0':1.15,
    '1.5':1.55,
    '2.0':2.1,
    '2.5':2.5,
    '3.0':3.0,
    '3.5':3.7
}

exp5.add_site(2000, tetrodes=[1,2,3,4,8])
exp5.add_session('13-20-06', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-22-57', 'a', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2050, tetrodes=[1,2,3,4,6,8])
exp5.add_session('13-26-20', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-27-42', 'b', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2100, tetrodes=[1,2,3,4,6,8])
exp5.add_session('13-30-27', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-32-28', 'c', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2150, tetrodes=[1,2,3,4,5,6,7,8])
exp5.add_session('13-36-07', None, 'noisebursts', 'am_tuning_curve')
#Switched to 16 freq from here on
exp5.add_session('13-37-50', 'd', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2200, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('13-43-01', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-44-26', 'e', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2250, tetrodes=[1,2,3,4,7,8])
exp5.add_session('13-48-15', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-50-46', 'f', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2300, tetrodes=[1,2,3,4,5,6,7,8])
exp5.add_session('13-54-56', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-57-02', 'g', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2350, tetrodes=[5,6])
exp5.add_session('14-02-51', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-05-13', 'h', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2400, tetrodes=[5,6,7,8])
exp5.add_session('14-11-29', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-13-11', 'i', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2450, tetrodes=[5,6,7,8])
exp5.add_session('14-17-13', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-19-00', 'j', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2500, tetrodes=[5,6,7,8])
exp5.add_session('14-22-12', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-23-50', 'k', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2550, tetrodes=[1,5,6,7,8])
exp5.add_session('14-27-34', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-29-07', 'l', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2600, tetrodes=[5,6,7,8])
exp5.add_session('14-34-08', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-35-44', 'm', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2650, tetrodes=[5,6,7,8])
exp5.add_session('14-39-24', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-41-40', 'n', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2700, tetrodes=[5,6,7,8])
exp5.add_session('14-45-03', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-46-30', 'o', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2750, tetrodes=[5,6,7,8])
exp5.add_session('14-49-44', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-51-41', 'p', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2800, tetrodes=[5,6,7,8])
exp5.add_session('14-56-26', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-58-04', 'q', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2850, tetrodes=[5,6,7,8])
exp5.add_session('15-01-54', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-03-10', 'r', 'tuningCurve', 'am_tuning_curve')

exp5.add_site(2900, tetrodes=[5,6,7,8])
exp5.add_session('15-06-47', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-08-38', 's', 'tuningCurve', 'am_tuning_curve')
