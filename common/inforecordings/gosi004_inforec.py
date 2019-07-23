from jaratoolbox import celldatabase

subject = 'gosi004'
experiments = []

'''
Experiments with <550 valid trials commented out
'''
'''
experiment = celldatabase.Experiment(subject,
                               '2017-02-06',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('17-27-51', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-29-40', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-36-07', 'a', 'tc', 'laser_tuning_curve')



experiment = celldatabase.Experiment(subject,
                               '2017-02-07',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('17-13-41', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-22-09', 'a', 'tc', 'laser_tuning_curve')

experiment = celldatabase.Experiment(subject,
                               '2017-02-08',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('17-05-30', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-16-32', 'a', 'tc', 'laser_tuning_curve')

experiment = celldatabase.Experiment(subject,
                               '2017-02-09',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('14-08-34', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-12-47', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-21-45', 'a', 'behavior', '2afc')
experiment.add_session('14-37-13', None, 'behavior2', '2afc')#unplugged during behavior
experiment.add_session('15-01-25', '4', 'behavior3', '2afc')


experiment = celldatabase.Experiment(subject,
                               '2017-02-10',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('12-30-17', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('12-35-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-45-11', 'a', 'behavior', '2afc')#unplugged during behavior


experiment = celldatabase.Experiment(subject,
                               '2017-02-11',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('15-46-30', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-49-11', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-54-13', 'a', 'behavior', '2afc')

experiment = celldatabase.Experiment(subject,
                               '2017-02-12',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-', tetrodes=range(1, 9))
experiment.add_session('15-28-18', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-30-46', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-35-00', 'a', 'behavior', '2afc')
'''

experiment = celldatabase.Experiment(subject,
                               '2017-02-13',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-02-13', tetrodes=range(1, 9))
experiment.add_session('16-50-17', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('16-52-40', 'a', 'tc', 'laser_tuning_curve') #ref=17
experiment.add_session('16-59-23', 'a', 'behavior', '2afc')#ref=17

'''

experiment.add_site(500, date='2017-02-14', tetrodes=range(1, 9))
experiment.add_session('16-13-50', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-19-01', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-24-37', 'a', 'behavior', '2afc')


experiment.add_site(500, date='2017-02-15', tetrodes=range(1, 9))
experiment.add_session('13-56-30', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('13-59-31', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-15-31', 'b', 'behavior', '2afc')
'''


experiment.add_site(500, date='2017-02-16', tetrodes=range(1, 9))
experiment.add_session('14-38-31', None, 'noiseburst', 'laser_tuning_curve')#ref=19
experiment.add_session('14-42-10', 'a', 'tc', 'laser_tuning_curve')#ref=19; 177 trials
experiment.add_session('14-49-01', 'a', 'behavior', '2afc')#ref=19

'''
experiment.add_site(580, date='2017-02-17', tetrodes=range(1, 9))
#experiment.add_session('15-39-55', None, 'noiseburst', 'laser_tuning_curve')#changed thresholds after this recording
experiment.add_session('16-06-29', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-16-10', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-23-04', 'a', 'behavior', '2afc')


experiment.add_site(580, date='2017-02-18', tetrodes=range(1, 9))
experiment.add_session('09-42-49', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('09-46-29', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('09-52-26', 'a', 'behavior', '2afc')
'''

experiment.add_site(580, date='2017-02-19', tetrodes=range(1, 9))
experiment.add_session('17-35-11', None, 'noiseburst', 'laser_tuning_curve')#ref=19
experiment.add_session('17-38-56', 'a', 'tc', 'laser_tuning_curve')#ref=19; 159 trials
experiment.add_session('18-03-10', 'a', 'behavior', '2afc')#ref=19

experiment.add_site(580, date='2017-02-20', tetrodes=range(1, 9))
experiment.add_session('16-57-19', None, 'noiseburst', 'laser_tuning_curve')#ref=19
experiment.add_session('17-03-44', 'a', 'tc', 'laser_tuning_curve')#ref=19; 162 trials
experiment.add_session('17-10-22', 'a', 'behavior', '2afc')#ref=19


experiment.add_site(620, date='2017-02-21', tetrodes=range(1, 9))
experiment.add_session('16-26-35', None, 'noiseburst', 'laser_tuning_curve')#ref=19 
#experiment.add_session('16-31-12', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('16-34-45', 'a', 'tc', 'laser_tuning_curve')#ref=19; 168 trials
experiment.add_session('16-39-07', 'a', 'behavior', '2afc')#ref=19

'''
experiment.add_site(660, date='2017-02-22', tetrodes=range(1, 9))
experiment.add_session('15-19-46', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-24-18', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-31-56', 'a', 'behavior', '2afc')
'''

experiment.add_site(660, date='2017-02-23', tetrodes=range(1, 9))
experiment.add_session('14-59-44', None, 'noiseburst', 'laser_tuning_curve')#ref=29
#experiment.add_session('15-03-39', None, 'noiseburst', 'laser_tuning_curve')#ref=19
experiment.add_session('15-08-28', 'a', 'tc', 'laser_tuning_curve')#ref=29; 170 trials
experiment.add_session('15-14-12', 'a', 'behavior', '2afc')#ref=29

'''
experiment.add_site(700, date='2017-02-24', tetrodes=range(1, 9))
experiment.add_session('15-20-16', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('15-24-52', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-31-22', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-38-38', 'a', 'behavior', '2afc')
'''


experiment.add_site(700, date='2017-02-25', tetrodes=range(1, 9))
experiment.add_session('15-00-21', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('15-04-00', 'a', 'tc', 'laser_tuning_curve')#ref=29; 169 trials
experiment.add_session('15-08-57', 'a', 'behavior', '2afc')#ref=29

'''
experiment.add_site(740, date='2017-02-26', tetrodes=range(1, 9))
#experiment.add_session('16-29-18', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-32-13', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-34-49', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-40-04', 'a', 'behavior', '2afc')
'''

experiment.add_site(740, date='2017-02-27', tetrodes=range(1, 9))
experiment.add_session('17-00-46', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('17-04-47', 'a', 'tc', 'laser_tuning_curve')#ref=29; 163 trials
experiment.add_session('17-09-21', 'a', 'behavior', '2afc')#ref=29


experiment.add_site(780, date='2017-02-28', tetrodes=range(1, 9))
experiment.add_session('16-22-18', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('16-24-53', 'a', 'tc', 'laser_tuning_curve')#ref=29; 171 trials
experiment.add_session('16-29-37', 'a', 'behavior', '2afc')#ref=29

'''
experiment.add_site(820, date='2017-03-01', tetrodes=range(1, 9))
experiment.add_session('15-32-08', None, 'noiseburst', 'laser_tuning_curve')#rig2
experiment.add_session('15-40-35', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-45-34', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-50-06', 'a', 'behavior', '2afc')


experiment.add_site(820, date='2017-03-02', tetrodes=range(1, 9))
experiment.add_session('14-03-06', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-06-38', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-11-47', 'a', 'behavior', '2afc')
'''

experiment.add_site(820, date='2017-03-03', tetrodes=range(1, 9))
experiment.add_session('15-53-45', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('15-56-28', 'a', 'tc', 'laser_tuning_curve')#ref=29; 160 trials
experiment.add_session('16-17-38', 'b', 'tc', 'laser_tuning_curve')#ref=29; 310 trials
experiment.add_session('16-24-05', 'a', 'behavior', '2afc')#ref=29

'''
experiment.add_site(860, date='2017-03-04', tetrodes=range(1, 9))
#experiment.add_session('17-05-33', None, 'noiseburst', 'laser_tuning_curve')#ref 27
experiment.add_session('17-08-15', None, 'noiseburst', 'laser_tuning_curve')#ref 29
experiment.add_session('17-10-34', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-18-08', 'a', 'behavior', '2afc')#unplugged during behavior

experiment.add_site(860, date='2017-03-05', tetrodes=range(1, 9))
experiment.add_session('14-38-38', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-43-42', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-52-42', 'a', 'behavior', '2afc')

experiment.add_site(860, date='2017-03-06', tetrodes=range(1, 9))
experiment.add_session('15-55-25', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-59-30', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-10-14', 'a', 'behavior', '2afc')

'''
experiment.add_site(860, date='2017-03-07', tetrodes=range(1, 9))
experiment.add_session('16-23-33', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('16-26-35', 'a', 'tc', 'laser_tuning_curve')#ref=29; 319 trials
experiment.add_session('16-33-44', 'a', 'behavior', '2afc')#ref=29

'''
experiment.add_site(900, date='2017-03-08', tetrodes=range(1, 9))
#experiment.add_session('15-29-18', None, 'noiseburst', 'laser_tuning_curve')#ref 18
#experiment.add_session('15-44-20', None, 'noiseburst', 'laser_tuning_curve')#ref 21
experiment.add_session('15-50-22', None, 'noiseburst', 'laser_tuning_curve')#ref 9
experiment.add_session('15-53-25', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-01-03', 'a', 'behavior', '2afc')


experiment.add_site(900, date='2017-03-09', tetrodes=range(1, 9))
experiment.add_session('14-41-51', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-44-46', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-53-11', 'a', 'behavior', '2afc')


experiment.add_site(900, date='2017-03-10', tetrodes=range(1, 9))
experiment.add_session('17-50-59', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-54-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-01-53', 'a', 'behavior', '2afc')
'''

experiment.add_site(900, date='2017-03-11', tetrodes=range(1, 9))
experiment.add_session('18-00-51', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('18-03-24', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-09-53', 'a', 'behavior', '2afc')

'''
experiment.add_site(940, date='2017-03-12', tetrodes=range(1, 9))
experiment.add_session('13-33-38', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('13-40-12', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-49-43', 'a', 'behavior', '2afc')


experiment.add_site(940, date='2017-03-13', tetrodes=range(1, 9))
experiment.add_session('15-58-37', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=9
experiment.add_session('16-07-28', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=9, thresholds=50
experiment.add_session('16-18-55', None, 'noiseburst', 'laser_tuning_curve')#rig 2, ref=9, thresholds=50
experiment.add_session('16-37-55', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=29
experiment.add_session('16-45-20', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-54-59', 'a', 'behavior', '2afc')


experiment.add_site(940, date='2017-03-14', tetrodes=range(1, 9))
experiment.add_session('17-17-20', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('17-21-44', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-29-14', 'a', 'behavior', '2afc')
'''


experiment.add_site(940, date='2017-03-15', tetrodes=range(1, 9))
experiment.add_session('15-15-43', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('15-18-46', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-26-11', 'a', 'behavior', '2afc')

'''
experiment.add_site(940, date='2017-03-16', tetrodes=range(1, 9))
experiment.add_session('14-34-40', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('14-41-34', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-50-42', 'a', 'behavior', '2afc')# Unplugged during behavior ~463 trials
'''

experiment.add_site(940, date='2017-03-17', tetrodes=range(1, 9))
experiment.add_session('17-03-17', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('17-06-02', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-16-47', 'a', 'behavior', '2afc')#change to 150 trials per block


experiment.add_site(980, date='2017-03-18', tetrodes=range(1, 9))
experiment.add_session('16-14-29', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('16-17-33', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-26-10', 'a', 'behavior', '2afc')


experiment.add_site(1020, date='2017-03-19', tetrodes=range(1, 9))
experiment.add_session('15-36-50', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('15-39-24', 'a', 'tc', 'laser_tuning_curve')#data didn't save
experiment.add_session('15-52-25', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('16-00-02', 'a', 'behavior', '2afc')


experiment.add_site(1060, date='2017-03-20', tetrodes=range(1, 9))
experiment.add_session('16-15-36', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('16-18-22', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-26-56', 'a', 'behavior', '2afc')


experiment.add_site(1100, date='2017-03-21', tetrodes=range(1, 9))
experiment.add_session('16-47-00', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('16-50-26', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-57-34', 'a', 'behavior', '2afc')


experiment.add_site(1140, date='2017-03-22', tetrodes=range(1, 9))
experiment.add_session('11-47-20', None, 'noiseburst', 'laser_tuning_curve')# ref=10
experiment.add_session('11-50-13', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-57-08', 'a', 'behavior', '2afc')


experiment.add_site(1180, date='2017-03-23', tetrodes=range(1, 9))
experiment.add_session('16-54-31', None, 'noiseburst', 'laser_tuning_curve')# ref=10
experiment.add_session('16-57-13', 'a', 'tc', 'laser_tuning_curve')#plotted like a noiseburst so re-ran tuning curve
experiment.add_session('17-07-00', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('17-14-19', 'a', 'behavior', '2afc')


experiment.add_site(1220, date='2017-03-24', tetrodes=range(1, 9))
experiment.add_session('15-58-35', None, 'noiseburst', 'laser_tuning_curve')# ref=10
experiment.add_session('16-01-23', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-08-30', 'a', 'behavior', '2afc')


experiment.add_site(1260, date='2017-03-25', tetrodes=range(1, 9))
experiment.add_session('10-42-28', None, 'noiseburst', 'laser_tuning_curve')# ref=10
experiment.add_session('10-47-49', None, 'noiseburst', 'laser_tuning_curve')# ref=28
experiment.add_session('10-55-08', 'a', 'tc', 'laser_tuning_curve')# ref=28
experiment.add_session('11-02-31', 'a', 'behavior', '2afc')


experiment.add_site(1260, date='2017-03-26', tetrodes=range(1, 9))
experiment.add_session('11-35-02', None, 'noiseburst', 'laser_tuning_curve')# ref=28
experiment.add_session('11-41-04', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-49-41', 'a', 'behavior', '2afc')

'''

experiment.add_site(1300, date='2017-04-02', tetrodes=range(1, 9))
experiment.add_session('16-10-30', None, 'noiseburst', 'laser_tuning_curve')# ref=28
experiment.add_session('16-16-08', None, 'noiseburst', 'laser_tuning_curve')# ref=16
experiment.add_session('16-19-04', 'a', 'tc', 'laser_tuning_curve')# ref=16
experiment.add_session('16-27-20', 'a', 'behavior', '2afc')



experiment.add_site(1340, date='2017-04-03', tetrodes=range(1, 9))
experiment.add_session('14-46-17', None, 'noiseburst', 'laser_tuning_curve')#ref=29. Moved deeper prior to noiseburst, ran behavior with no ephys recording.
'''

experiment.add_site(1380, date='2017-04-04', tetrodes=range(1, 9))
experiment.add_session('17-33-28', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('17-36-15', 'a', 'tc', 'laser_tuning_curve')# ref=29
experiment.add_session('17-44-52', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1420, date='2017-04-05', tetrodes=range(1, 9))
experiment.add_session('18-25-10', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('18-31-34', 'a', 'tc', 'laser_tuning_curve')# ref=29
experiment.add_session('18-40-39', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1460, date='2017-04-06', tetrodes=range(1, 9))
experiment.add_session('17-03-31', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('17-07-33', 'a', 'tc', 'laser_tuning_curve')# ref=29
experiment.add_session('17-14-48', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1500, date='2017-04-07', tetrodes=range(1, 9))
#experiment.add_session('16-06-00', None, 'noiseburst', 'laser_tuning_curve')# ref=29
experiment.add_session('16-10-09', None, 'noiseburst', 'laser_tuning_curve')# ref=11
experiment.add_session('16-13-08', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('16-25-58', 'a', 'behavior', '2afc')# 200 trials/block


experiment.add_site(1500, date='2017-04-08', tetrodes=range(1, 9))
experiment.add_session('14-30-38', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#experiment.add_session('14-41-07', None, 'noiseburst', 'laser_tuning_curve')# ref=18
experiment.add_session('14-44-42', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('14-51-45', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1540, date='2017-04-09', tetrodes=range(1, 9))
experiment.add_session('13-39-23', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#experiment.add_session('13-43-07', None, 'noiseburst', 'laser_tuning_curve')# ref=3
experiment.add_session('13-46-46', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('13-53-41', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1580, date='2017-04-10', tetrodes=range(1, 9))
experiment.add_session('18-21-31', None, 'noiseburst', 'laser_tuning_curve')# ref=11
experiment.add_session('18-24-10', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('18-31-07', 'a', 'behavior', '2afc')# 200 trials/block

'''
experiment.add_site(1620, date='2017-04-11', tetrodes=range(1, 9))
#experiment.add_session('16-46-53', None, 'noiseburst', 'laser_tuning_curve')# ref=11 (bad noise disruption)
experiment.add_session('16-50-15', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#experiment.add_session('16-53-03', 'a', 'tc', 'laser_tuning_curve')# ref=11 (bad noise disruption)
experiment.add_session('19-12-25', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('19-18-53', 'a', 'behavior', '2afc')# 200 trials/block, unplugged during behavior at 580 trials
'''

experiment.add_site(1620, date='2017-04-12', tetrodes=range(1, 9))
experiment.add_session('14-47-16', None, 'noiseburst', 'laser_tuning_curve')# ref=11
experiment.add_session('14-50-37', 'a', 'tc', 'laser_tuning_curve')# ref=11
experiment.add_session('14-57-54', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1660, date='2017-04-13', tetrodes=range(1, 9))
experiment.add_session('14-07-27', None, 'noiseburst', 'laser_tuning_curve')# ref=9
experiment.add_session('14-10-46', 'a', 'tc', 'laser_tuning_curve')# ref=9
experiment.add_session('14-19-13', 'a', 'behavior', '2afc')# 200 trials/block

'''
experiment.add_site(1700, date='2017-04-14', tetrodes=range(1, 9))
experiment.add_session('14-38-00', None, 'noiseburst', 'laser_tuning_curve')# ref=9
experiment.add_session('14-40-21', 'a', 'tc', 'laser_tuning_curve')# ref=9
experiment.add_session('14-47-32', 'a', 'behavior', '2afc')# 200 trials/block


experiment.add_site(1700, date='2017-04-17', tetrodes=range(1, 9))
experiment.add_session('18-28-51', None, 'noiseburst', 'laser_tuning_curve')# ref=9
experiment.add_session('18-32-12', 'a', 'tc', 'laser_tuning_curve')# ref=9
experiment.add_session('18-39-26', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1700, date='2017-04-18', tetrodes=range(1, 9))
experiment.add_session('18-53-51', None, 'noiseburst', 'laser_tuning_curve')# ref=9
experiment.add_session('18-56-43', 'a', 'tc', 'laser_tuning_curve')# ref=9
experiment.add_session('19-05-02', 'a', 'behavior', '2afc')# 150 trials/block


experiment.add_site(1700, date='2017-04-19', tetrodes=range(1, 9))
experiment.add_session('18-41-45', None, 'noiseburst', 'laser_tuning_curve')# ref=9
experiment.add_session('18-44-34', 'a', 'tc', 'laser_tuning_curve')# ref=9
experiment.add_session('18-52-26', 'a', 'behavior', '2afc')# 150 trials/block
'''

experiment.maxDepth = 1700


tetrodeLengthList = [110, 110, 220, 220, 220, 330, 0, 130] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (500, 1660)
