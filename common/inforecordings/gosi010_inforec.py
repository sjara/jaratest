from jaratoolbox import celldatabase

subject = 'gosi010'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out.
'''

'''
experiment = celldatabase.Experiment(subject,
                               '2017-04-20',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(540, date='2017-', tetrodes=range(1, 9))
experiment.add_session('15-51-55', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('15-56-54', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-05-28', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

experiment = celldatabase.Experiment(subject,
                               '2017-04-21',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(540, date='2017-04-21', tetrodes=range(1, 9))
experiment.add_session('16-08-47', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('16-16-12', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-28-52', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(580, date='2017-04-22', tetrodes=range(1, 9))
experiment.add_session('17-45-27', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('17-49-44', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-56-30', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(620, date='2017-04-23', tetrodes=range(1, 9))
#experiment.add_session('16-17-06', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('16-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=10, new cable
#experiment.add_session('16-20-07', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-46-26', 'b', 'tc', 'laser_tuning_curve')#newcable
experiment.add_session('16-54-42', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(660, date='2017-04-24', tetrodes=range(1, 9))
experiment.add_session('14-11-25', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('14-14-23', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-21-26', 'a', 'behavior', '2afc')#150 trials/block

'''
experiment = celldatabase.Experiment(subject,
                               '2017-04-25',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(700, date='2017-04-25', tetrodes=range(1, 9))
experiment.add_session('11-59-37', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('12-02-19', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-09-23', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''



experiment.add_site(700, date='2017-04-26', tetrodes=range(1, 9))
experiment.add_session('14-31-49', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('14-35-43', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-43-14', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(740, date='2017-04-27', tetrodes=range(1, 9))
experiment.add_session('13-51-10', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('13-54-45', 'a', 'tc', 'laser_tuning_curve')#abnormal noise
#experiment.add_session('14-13-23', 'b', 'tc', 'laser_tuning_curve')#same abnormal noise
experiment.add_session('14-26-59', 'a', 'behavior', '2afc')#150 trials/block


experiment.add_site(780, date='2017-04-28', tetrodes=range(1, 9))
experiment.add_session('14-30-12', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('14-33-00', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-41-34', 'a', 'behavior', '2afc')#150 trials/block

'''


experiment.add_site(820, date='2017-04-29', tetrodes=range(1, 9))
experiment.add_session('16-03-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('16-07-41', 'a', 'tc', 'laser_tuning_curve')#ref=17
experiment.add_session('16-14-30', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''


experiment.add_site(820, date='2017-04-30', tetrodes=range(1, 9))
experiment.add_session('17-55-37', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('17-58-11', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-06-50', 'a', 'behavior', '2afc')#200 trials/block

'''

experiment.add_site(860, date='2017-05-01', tetrodes=range(1, 9))
#experiment.add_session('12-15-38', None, 'noiseburst', 'laser_tuning_curve')#ref=17, ephys crash
experiment.add_session('12-32-24', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-40-10', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''


experiment.add_site(860, date='2017-05-02', tetrodes=range(1, 9))
experiment.add_session('12-02-27', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-05-40', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-12-36', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(900, date='2017-05-03', tetrodes=range(1, 9))
experiment.add_session('14-48-35', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('14-51-01', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-58-15', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(940, date='2017-05-04', tetrodes=range(1, 9))
experiment.add_session('12-19-44', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-29-41', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-37-04', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(980, date='2017-05-05', tetrodes=range(1, 9))
experiment.add_session('14-26-10', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('14-28-58', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-36-12', 'a', 'behavior', '2afc')#200 trials/block,


experiment.add_site(1020, date='2017-05-06', tetrodes=range(1, 9))
experiment.add_session('15-27-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('15-31-21', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-38-02', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1060, date='2017-05-07', tetrodes=range(1, 9))
experiment.add_session('12-47-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-50-09', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-56-35', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1100, date='2017-05-08', tetrodes=range(1, 9))
#experiment.add_session('12-14-05', None, 'noiseburst', 'laser_tuning_curve')#ref=17, weird blot, response in blocks
experiment.add_session('12-17-23', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-20-05', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-26-44', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1140, date='2017-05-09', tetrodes=range(1, 9))
experiment.add_session('12-05-21', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-09-39', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-16-13', 'a', 'behavior', '2afc')#200 trials/block,


experiment.add_site(1180, date='2017-05-10', tetrodes=range(1, 9))
experiment.add_session('14-36-51', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('14-44-02', 'a', 'tc', 'laser_tuning_curve')#ref=18
experiment.add_session('14-53-20', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1220, date='2017-05-11', tetrodes=range(1, 9))
experiment.add_session('14-14-45', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('14-18-15', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-25-20', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1260, date='2017-05-12', tetrodes=range(1, 9))
experiment.add_session('13-35-44', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('13-40-44', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-47-33', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1300, date='2017-05-13', tetrodes=range(1, 9))
experiment.add_session('16-13-11', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('16-16-26', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-23-04', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1340, date='2017-05-14', tetrodes=range(1, 9))
experiment.add_session('15-11-38', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('15-14-27', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-21-10', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1380, date='2017-05-15', tetrodes=range(1, 9))
experiment.add_session('12-17-03', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('12-19-33', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-26-04', 'a', 'behavior', '2afc')#150 trials/block,

'''

experiment.add_site(1420, date='2017-05-16', tetrodes=range(1, 9))
experiment.add_session('11-45-06', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('11-47-51', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-54-29', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''


experiment.add_site(1420, date='2017-05-17', tetrodes=range(1, 9))
experiment.add_session('14-06-43', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('14-10-13', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-17-30', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1460, date='2017-05-18', tetrodes=range(1, 9))
experiment.add_session('14-39-44', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('14-42-42', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-49-17', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1500, date='2017-05-19', tetrodes=range(1, 9))
experiment.add_session('16-48-01', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('16-50-56', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-57-49', 'a', 'behavior', '2afc')#200 trials/block, 

experiment.add_site(1540, date='2017-05-22', tetrodes=range(1, 9))
experiment.add_session('11-45-17', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('11-47-51', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-54-58', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(1580, date='2017-05-23', tetrodes=range(1, 9))
experiment.add_session('10-30-34', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('10-33-23', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('10-40-22', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(1620, date='2017-05-24', tetrodes=range(1, 9))
#experiment.add_session('10-17-44', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('10-21-18', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('10-25-07', 'a', 'tc', 'laser_tuning_curve')#ref=17
experiment.add_session('10-31-52', 'a', 'behavior', '2afc')#200 trials/block, 

'''
experiment.add_site(1660, date='2017-05-25', tetrodes=range(1, 9))
experiment.add_session('12-55-17', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('12-57-39', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-04-36', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials



experiment.add_site(1660, date='2017-05-26', tetrodes=range(1, 9))
experiment.add_session('10-19-04', None, 'noiseburst', 'laser_tuning_curve')#ref=17
experiment.add_session('10-22-30', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('10-29-52', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

experiment.maxDepth = 1660


tetrodeLengthList = [330, 485, 580, 0, 660, 680, 485, 680] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (540, 1620)
