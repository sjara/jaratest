from jaratoolbox import celldatabase

subject = 'gosi001'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''

'''
experiment = celldatabase.Experiment(subject,
                               '2017-04-20',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-04-20', tetrodes=range(1, 9))
experiment.add_session('16-14-54', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('16-17-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-25-17', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

experiment = celldatabase.Experiment(subject,
                               '2017-04-21',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-04-21', tetrodes=range(1, 9))
experiment.add_session('14-21-06', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-23-45', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-30-49', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(540, date='2017-04-22', tetrodes=range(1, 9))
experiment.add_session('17-50-04', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('17-56-30', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-03-21', 'a', 'behavior', '2afc')#150 trials/block

'''

experiment.add_site(580, date='2017-04-23', tetrodes=range(1, 9))
experiment.add_session('16-20-42', None, 'noiseburst', 'laser_tuning_curve')#ref=5, rig 2
experiment.add_session('16-23-14', 'a', 'tc', 'laser_tuning_curve')#rig 2, speaker malfunction, commented out because no behavior was recorded as a result of the speaker malfunction
'''


experiment.add_site(580, date='2017-04-24', tetrodes=range(1, 9))
experiment.add_session('12-18-57', None, 'noiseburst', 'laser_tuning_curve')#ref=5
#experiment.add_session('12-23-13', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('12-26-54', 'a', 'tc', 'laser_tuning_curve')#ref=5
experiment.add_session('12-34-03', 'a', 'behavior', '2afc')#150 trials/block

'''

experiment.add_site(620, date='2017-04-25', tetrodes=range(1, 9))
experiment.add_session('11-50-46', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('11-54-29', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-01-53', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''

experiment.add_site(620, date='2017-04-26', tetrodes=range(1, 9))
experiment.add_session('14-21-16', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-24-15', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-30-54', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(660, date='2017-04-27', tetrodes=range(1, 9))
experiment.add_session('13-40-13', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('13-43-20', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-50-28', 'a', 'behavior', '2afc')#150 trials/block



experiment.add_site(700, date='2017-04-28', tetrodes=range(1, 9))
experiment.add_session('14-41-34', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-44-53', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-51-37', 'a', 'behavior', '2afc')#200 trials/block



experiment.add_site(740, date='2017-04-29', tetrodes=range(1, 9))
experiment.add_session('16-05-27', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('16-08-00', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-14-32', 'a', 'behavior', '2afc')#200 trials/block


experiment.add_site(780, date='2017-04-30', tetrodes=range(1, 9))
experiment.add_session('17-57-51', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('18-00-54', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-07-50', 'a', 'behavior', '2afc')#200 trials/block



experiment.add_site(820, date='2017-05-01', tetrodes=range(1, 9))
experiment.add_session('12-06-06', None, 'noiseburst', 'laser_tuning_curve')#ref=20
experiment.add_session('12-08-58', 'a', 'tc', 'laser_tuning_curve')#ref=20
experiment.add_session('12-20-04', 'a', 'behavior', '2afc')#150 trials/block

'''

experiment.add_site(900, date='2017-05-02', tetrodes=range(1, 9))
experiment.add_session('11-50-04', None, 'noiseburst', 'laser_tuning_curve')#ref=20
experiment.add_session('11-53-43', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('11-57-16', 'a', 'tc', 'laser_tuning_curve')#ref=13
experiment.add_session('12-04-25', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''


experiment.add_site(900, date='2017-05-03', tetrodes=range(1, 9))
experiment.add_session('14-50-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-52-36', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-59-23', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(940, date='2017-05-04', tetrodes=range(1, 9))
experiment.add_session('12-21-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('12-24-07', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-30-35', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(980, date='2017-05-05', tetrodes=range(1, 9))
experiment.add_session('14-28-44', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('14-31-19', 'a', 'tc', 'laser_tuning_curve')#ref=29
experiment.add_session('14-37-59', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1020, date='2017-05-06', tetrodes=range(1, 9))
experiment.add_session('15-31-07', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('15-33-20', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-40-06', 'a', 'behavior', '2afc')#200 trials/block,



experiment.add_site(1060, date='2017-05-07', tetrodes=range(1, 9))
experiment.add_session('12-49-20', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('12-51-42', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-58-18', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1100, date='2017-05-08', tetrodes=range(1, 9))
experiment.add_session('12-19-31', None, 'noiseburst', 'laser_tuning_curve')#ref=29
#experiment.add_session('12-22-04', 'a', 'tc', 'laser_tuning_curve')#ref=29, tuning on all TT
experiment.add_session('12-30-10', 'b', 'tc', 'laser_tuning_curve')#ref=26
experiment.add_session('12-37-13', 'a', 'behavior', '2afc')#200 trials/block,

'''

experiment.add_site(1140, date='2017-05-09', tetrodes=range(1, 9))
experiment.add_session('12-09-09', None, 'noiseburst', 'laser_tuning_curve')#ref=26
experiment.add_session('12-11-29', 'a', 'tc', 'laser_tuning_curve')#ref=26
experiment.add_session('12-18-57', 'a', 'behavior', '2afc')#200 trials/block, commented out becuase behavior data didn't save
'''


experiment.add_site(1180, date='2017-05-10', tetrodes=range(1, 9))
experiment.add_session('14-43-18', None, 'noiseburst', 'laser_tuning_curve')#ref=26
experiment.add_session('14-49-34', 'a', 'tc', 'laser_tuning_curve')#ref=26
experiment.add_session('14-56-19', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1220, date='2017-05-11', tetrodes=range(1, 9))
experiment.add_session('14-17-12', None, 'noiseburst', 'laser_tuning_curve')#ref=26
experiment.add_session('14-20-49', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-26-25', 'a', 'tc', 'laser_tuning_curve')#ref=5
experiment.add_session('14-32-58', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1260, date='2017-05-12', tetrodes=range(1, 9))
experiment.add_session('13-39-38', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('13-42-20', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-48-47', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(1300, date='2017-05-13', tetrodes=range(1, 9))
experiment.add_session('16-15-23', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('16-17-57', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-24-43', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(1340, date='2017-05-14', tetrodes=range(1, 9))
experiment.add_session('15-13-36', None, 'noiseburst', 'laser_tuning_curve')#ref=5
#experiment.add_session('15-16-58', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('15-20-41', 'a', 'tc', 'laser_tuning_curve')#ref=5
experiment.add_session('15-27-21', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(1380, date='2017-05-15', tetrodes=range(1, 9))
experiment.add_session('12-18-50', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('12-21-18', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-28-04', 'a', 'behavior', '2afc')#150 trials/block, 

'''
experiment.add_site(1420, date='2017-05-16', tetrodes=range(1, 9))
experiment.add_session('11-46-28', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('11-49-05', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-55-32', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

experiment.add_site(1420, date='2017-05-17', tetrodes=range(1, 9))
experiment.add_session('14-09-18', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-11-44', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-19-43', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1460, date='2017-05-18', tetrodes=range(1, 9))
experiment.add_session('14-41-07', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('14-43-58', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-50-48', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1500, date='2017-05-19', tetrodes=range(1, 9))
experiment.add_session('17-53-49', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('17-56-34', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-03-13', 'a', 'behavior', '2afc')#200 trials/block, 


'''
experiment.add_site(1540, date='2017-05-22', tetrodes=range(1, 9))
#experiment.add_session('10-21-40', None, 'noiseburst', 'laser_tuning_curve')#ref=5
experiment.add_session('10-25-20', None, 'noiseburst', 'laser_tuning_curve')#ref=9
experiment.add_session('10-34-07', 'a', 'tc', 'laser_tuning_curve')#ref=9
experiment.add_session('10-40-49', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''

experiment.maxDepth = 1540


tetrodeLengthList = [0, 190, 40, 230, 140, 300, 300, 210] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (500, 1500)
