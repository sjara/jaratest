#Making an inforec
from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'test000'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-06-25', 'right_AudStr', info=['posteriorDiD', 'FacingPosterior'])
experiments.append(exp0)
#Comment about speakers used, power of laser, and specific probe used

exp0.laserCalibration = {
'OutputDecimal':LevelDecimal
#0.5-4.0
}

#tetrode 6 is the reference, threshold is
exp0.add_site(2500, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('12-26-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-31-02', None, 'laser', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('12-41-13', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-43-43', None, 'laser', 'am_tuning_curve')
exp0.add_session('12-50-44', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-58-17', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('14-36-29', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-41-19', None, 'laser', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('14-36-29', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-41-19', None, 'laser', 'am_tuning_curve')

exp0.maxDepth = 2600
