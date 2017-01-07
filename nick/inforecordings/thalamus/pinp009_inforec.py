from jaratoolbox import celldatabase

subject = 'pinp009'
experiments = []

exp0 = celldatabase.Experiment(subject, '2016-02-03')
experiments.append(exp0)

# site3 = thal.add_site(depth=3902, tetrodes=[4, 5, 6])

exp0.add_site(3902, tetrodes=[4, 5, 6])
exp0.add_session('14-12-11', None, 'NoiseBurst', 'am_tuning_curve')#Good sound responses - 4 is funky
exp0.add_session('14-14-59', None, 'LaserPulse', 'am_tuning_curve')
exp0.add_session('14-17-26', None, 'LaserTrain', 'am_tuning_curve')#Some direct activation
exp0.add_session('14-20-50', 'e', 'AM', 'am_tuning_curve')
exp0.add_session('14-41-15', None, 'LaserPulse2', 'am_tuning_curve')
exp0.add_session('14-43-25', None, 'LaserTrain2', 'am_tuning_curve')
exp0.add_session('14-47-05','f', 'TuningCurve', 'am_tuning_curve')#Full TC

# site5 = thal.add_site(depth=3959, tetrodes=[4, 5, 6])

exp0.add_site(3959, tetrodes=[4, 5, 6])
exp0.add_session('15-48-09', None, 'NoiseBurst', 'am_tuning_curve')#
exp0.add_session('15-51-18', None, 'LaserPulse', 'am_tuning_curve')#
exp0.add_session('15-53-34', None, 'LaserTrain', 'am_tuning_curve')#
exp0.add_session('15-57-54', 'g', 'AM', 'am_tuning_curve')#
exp0.add_session('16-21-49', None, 'LaserPulse2', 'am_tuning_curve')#
exp0.add_session('16-24-18', None, 'LaserTrain2', 'am_tuning_curve')#

# site6 = thal.add_site(depth=4005, tetrodes=[4, 5, 6])

exp0.add_site(4005, tetrodes=[4, 5, 6])
exp0.add_session('16-31-33', None, 'NoiseBurst', 'am_tuning_curve')#
exp0.add_session('16-33-53', None, 'LaserPulse', 'am_tuning_curve')#
exp0.add_session('16-36-12', None, 'LaserTrain', 'am_tuning_curve')#
exp0.add_session('16-39-28', 'h', 'AM', 'am_tuning_curve')#
exp0.add_session('17-03-34',None, 'LaserPulse2', 'am_tuning_curve')#
