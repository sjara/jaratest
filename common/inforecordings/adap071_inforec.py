from jaratoolbox import celldatabase

subject = 'adap071'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''
'''
experiment = celldatabase.Experiment(subject,
                               '2017-08-29',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-08-29', tetrodes=range(1, 9))
experiment.add_session('15-11-04', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('15-22-21', 'a', 'tc', 'laser_tuning_curve')
'''

experiment = celldatabase.Experiment(subject,
                               '2017-09-01',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-09-01', tetrodes=range(1, 9))
experiment.add_session('16-18-57', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('16-23-07', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-30-45', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(540, date='2017-09-02', tetrodes=range(1, 9))
experiment.add_session('14-53-39', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('14-56-23', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-03-53', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(580, date='2017-09-03', tetrodes=range(1, 9))
experiment.add_session('12-41-19', None, 'noiseburst', 'laser_tuning_curve')#ref=9
experiment.add_session('12-46-13', None, 'noiseburst', 'laser_tuning_curve')#ref=7
experiment.add_session('12-49-00', 'a', 'tc', 'laser_tuning_curve')#ref=7
experiment.add_session('12-56-22', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(620, date='2017-09-04', tetrodes=range(1, 9))
experiment.add_session('14-11-38', None, 'noiseburst', 'laser_tuning_curve')#ref=7
experiment.add_session('14-16-36', 'a', 'tc', 'laser_tuning_curve')#ref=7
experiment.add_session('14-23-52', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(660, date='2017-09-05', tetrodes=range(1, 9))
experiment.add_session('15-42-13', None, 'noiseburst', 'laser_tuning_curve')#ref=7
experiment.add_session('15-45-02', 'a', 'tc', 'laser_tuning_curve')#ref=7
experiment.add_session('15-53-36', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(700, date='2017-09-06', tetrodes=range(1, 9))
experiment.add_session('15-25-35', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('15-29-37', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('15-32-54', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('15-40-02', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(740, date='2017-09-07', tetrodes=range(1, 9))
experiment.add_session('16-21-59', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('16-25-05', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('16-28-17', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('16-32-33', 'a', 'tc', 'laser_tuning_curve')#ref=13
experiment.add_session('16-39-22', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(780, date='2017-09-08', tetrodes=range(1, 9))
experiment.add_session('14-55-42', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-58-28', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-05-59', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(820, date='2017-09-09', tetrodes=range(1, 9))
experiment.add_session('15-03-01', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-06-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-13-15', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(860, date='2017-09-10', tetrodes=range(1, 9))
experiment.add_session('14-06-45', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-09-43', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-16-54', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(900, date='2017-09-11', tetrodes=range(1, 9))
experiment.add_session('14-40-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-42-48', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-51-44', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(940, date='2017-09-12', tetrodes=range(1, 9))
experiment.add_session('16-25-03', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('16-28-04', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-34-56', 'a', 'behavior', '2afc')#150 trials/block, 

'''
experiment.add_site(980, date='2017-09-13', tetrodes=range(1, 9))
experiment.add_session('15-41-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-43-59', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-52-45', 'a', 'behavior', '2afc')#200 trials/block, commented out becuase not enough trials
'''


experiment.add_site(980, date='2017-09-14', tetrodes=range(1, 9))
experiment.add_session('15-04-40', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-07-16', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-13-37', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(1020, date='2017-09-15', tetrodes=range(1, 9))
experiment.add_session('14-50-29', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-45-59', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-53-44', 'a', 'behavior', '2afc')#150 trials/block,

 

experiment.add_site(1060, date='2017-09-16', tetrodes=range(1, 9))
experiment.add_session('13-43-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-46-07', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-53-25', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(1100, date='2017-09-18', tetrodes=range(1, 9))
experiment.add_session('15-21-34', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-24-15', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-33-13', 'a', 'behavior', '2afc')#150 trials/block, open ephys crashed right after I stopped recording


experiment.add_site(1140, date='2017-09-19', tetrodes=range(1, 9))
experiment.add_session('14-38-46', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-42-04', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-49-00', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1180, date='2017-09-20', tetrodes=range(1, 9))
experiment.add_session('14-28-28', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-31-36', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-40-14', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1220, date='2017-09-21', tetrodes=range(1, 9))
experiment.add_session('18-14-51', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('18-17-24', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-23-50', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(1260, date='2017-09-22', tetrodes=range(1, 9))
experiment.add_session('14-17-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-19-35', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-26-21', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1300, date='2017-09-23', tetrodes=range(1, 9))
experiment.add_session('16-19-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('16-21-36', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-28-04', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1340, date='2017-09-24', tetrodes=range(1, 9))
experiment.add_session('15-50-21', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-53-52', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-01-26', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1380, date='2017-09-25', tetrodes=range(1, 9))
experiment.add_session('16-38-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
#experiment.add_session('16-40-56', 'a', 'tc', 'laser_tuning_curve') noisy ref=13
#experiment.add_session('16-46-57', 'b', 'tc', 'laser_tuning_curve') noisy ref=13
experiment.add_session('16-54-43', 'c', 'tc', 'laser_tuning_curve') #ref=12
experiment.add_session('16-58-56', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1420, date='2017-09-26', tetrodes=range(1, 9))
experiment.add_session('15-58-57', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('16-02-36', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-10-35', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(1460, date='2017-09-27', tetrodes=range(1, 9))
experiment.add_session('16-25-10', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('16-28-59', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-35-51', 'a', 'behavior', '2afc')#200 trials/block


experiment.add_site(1500, date='2017-09-28', tetrodes=range(1, 9))
experiment.add_session('17-54-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('17-56-47', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-03-16', 'a', 'behavior', '2afc')#200 trials/block


experiment.add_site(1540, date='2017-09-29', tetrodes=range(1, 9))
experiment.add_session('13-40-34', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('13-45-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-51-45', 'a', 'behavior', '2afc')#200 trials/block

'''
experiment.add_site(1540, date='2017-09-30', tetrodes=range(1, 9))
#experiment.add_session('15-46-26', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('15-49-18', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('15-51-29', 'a', 'tc', 'laser_tuning_curve')


experiment.add_site(1540, date='2017-10-01', tetrodes=range(1, 9))
experiment.add_session('14-13-47', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('14-16-42', 'a', 'tc', 'laser_tuning_curve')
'''

experiment.maxDepth = 1540


tetrodeLengthList = [80, 80, 50, 50, 20, 20, 0, 50] #0 is the longest tetrode, other numbers means tetrode is x mm shorter than longest tetrode.
targetRangeLongestTt = (500, 1500)
