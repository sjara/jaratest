from jaratoolbox import celldatabase

subject = 'adap067'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''
'''
experiment = celldatabase.Experiment(subject,
                               '2017-09-04',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-09-04', tetrodes=range(1, 9))
experiment.add_session('12-37-16', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('12-42-30', None, 'noiseburst', 'laser_tuning_curve')#ref=20
experiment.add_session('12-46-50', None, 'noiseburst', 'laser_tuning_curve')#ref=29
experiment.add_session('15-22-21', 'a', 'tc', 'laser_tuning_curve')


experiment = celldatabase.Experiment(subject,
                               '2017-09-05',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(540, date='2017-09-05', tetrodes=range(1, 9))
experiment.add_session('14-13-06', None, 'noiseburst', 'laser_tuning_curve')#ref=18
experiment.add_session('14-16-36', 'a', 'tc', 'laser_tuning_curve')
'''

experiment = celldatabase.Experiment(subject,
                               '2017-09-06',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(580, date='2017-09-06', tetrodes=range(1, 9))
#experiment.add_session('13-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=10
experiment.add_session('13-48-09', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-51-45', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-59-23', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(620, date='2017-09-07', tetrodes=range(1, 9))
#experiment.add_session('15-10-13', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('15-14-43', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-18-01', 'a', 'tc', 'laser_tuning_curve')#ref=13
experiment.add_session('15-25-24', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(660, date='2017-09-08', tetrodes=range(1, 9))
experiment.add_session('13-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-46-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-54-15', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(700, date='2017-09-09', tetrodes=range(1, 9))
experiment.add_session('13-29-53', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-32-25', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-39-35', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(740, date='2017-09-10', tetrodes=range(1, 9))
experiment.add_session('13-03-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-05-49', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-12-59', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(780, date='2017-09-11', tetrodes=range(1, 9))
experiment.add_session('12-05-37', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('12-08-44', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-15-25', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(820, date='2017-09-12', tetrodes=range(1, 9))
experiment.add_session('15-26-39', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('15-30-16', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-37-13', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(860, date='2017-09-13', tetrodes=range(1, 9))
experiment.add_session('14-38-55', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-41-51', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-48-32', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(900, date='2017-09-14', tetrodes=range(1, 9))
experiment.add_session('14-01-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-04-37', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-11-14', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(940, date='2017-09-15', tetrodes=range(1, 9))
experiment.add_session('13-40-29', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('13-43-12', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-49-51', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(980, date='2017-09-16', tetrodes=range(1, 9))
experiment.add_session('12-38-16', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('12-40-56', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-47-47', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(1020, date='2017-09-17', tetrodes=range(1, 9))
experiment.add_session('14-50-45', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-54-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-02-00', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1060, date='2017-09-18', tetrodes=range(1, 9))
experiment.add_session('12-25-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('12-27-31', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-34-40', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1100, date='2017-09-19', tetrodes=range(1, 9))
experiment.add_session('13-39-38', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('13-42-19', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-50-55', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1140, date='2017-09-20', tetrodes=range(1, 9))
experiment.add_session('13-24-32', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('13-27-39', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-34-32', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1180, date='2017-09-21', tetrodes=range(1, 9))
experiment.add_session('17-10-05', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('17-13-11', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-20-04', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1220, date='2017-09-22', tetrodes=range(1, 9))
experiment.add_session('13-06-29', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('13-09-13', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('13-16-33', 'a', 'behavior', '2afc')#150 trials/block, 


experiment.add_site(1260, date='2017-09-23', tetrodes=range(1, 9))
experiment.add_session('15-07-42', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('15-10-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-16-45', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1300, date='2017-09-24', tetrodes=range(1, 9))
experiment.add_session('14-37-01', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('14-39-21', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-46-01', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1340, date='2017-09-25', tetrodes=range(1, 9))
experiment.add_session('15-23-57', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('15-27-41', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-35-03', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1380, date='2017-09-26', tetrodes=range(1, 9))
experiment.add_session('14-39-03', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('14-41-48', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-48-49', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1420, date='2017-09-27', tetrodes=range(1, 9))
experiment.add_session('14-54-03', None, 'noiseburst', 'laser_tuning_curve')#ref=13
experiment.add_session('14-57-24', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-04-24', 'a', 'behavior', '2afc')#200 trials/block, 



experiment.add_site(1460, date='2017-09-28', tetrodes=range(1, 9))
#experiment.add_session('16-03-37', None, 'noiseburst', 'laser_tuning_curve')#ref=22
experiment.add_session('16-06-41', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('16-10-03', 'a', 'tc', 'laser_tuning_curve')#ref=14
#experiment.add_session('16-16-46', 'b', 'tc', 'laser_tuning_curve')#ref=15
experiment.add_session('16-22-32', 'a', 'behavior', '2afc')#200 trials/block, 


experiment.add_site(1500, date='2017-09-29', tetrodes=range(1, 9))
experiment.add_session('16-46-46', None, 'noiseburst', 'laser_tuning_curve')#ref=15
experiment.add_session('16-49-13', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-56-02', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1540, date='2017-09-30', tetrodes=range(1, 9))
experiment.add_session('14-16-13', None, 'noiseburst', 'laser_tuning_curve')#ref=15
experiment.add_session('14-18-33', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-26-49', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1580, date='2017-10-01', tetrodes=range(1, 9))
experiment.add_session('15-33-21', None, 'noiseburst', 'laser_tuning_curve')#ref=15
experiment.add_session('15-35-56', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-43-35', 'a', 'behavior', '2afc')#150 trials/block, 



experiment.add_site(1620, date='2017-10-02', tetrodes=range(1, 9))
#experiment.add_session('17-45-43', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('17-48-42', None, 'noiseburst', 'laser_tuning_curve')#ref=21
experiment.add_session('17-51-01', 'a', 'tc', 'laser_tuning_curve')#ref=21
experiment.add_session('17-58-26', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1660, date='2017-10-03', tetrodes=range(1, 9))
experiment.add_session('16-54-29', None, 'noiseburst', 'laser_tuning_curve')#ref=21
experiment.add_session('16-56-58', 'a', 'tc', 'laser_tuning_curve')#ref=21
experiment.add_session('17-03-25', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1700, date='2017-10-04', tetrodes=range(1, 9))
experiment.add_session('15-18-31', None, 'noiseburst', 'laser_tuning_curve')#ref=21
experiment.add_session('15-21-33', 'a', 'tc', 'laser_tuning_curve')#ref=21
experiment.add_session('15-29-21', 'a', 'behavior', '2afc')#150 trials/block,


'''
# Somehow on this date the 2afc behavior file was not saved
experiment.add_site(1740, date='2017-10-05', tetrodes=range(1, 9))
experiment.add_session('16-26-19', None, 'noiseburst', 'laser_tuning_curve')#ref=9
#experiment.add_session('16-28-57', None, 'noiseburst', 'laser_tuning_curve')#ref=21
experiment.add_session('16-32-20', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('16-39-09', 'a', 'behavior', '2afc')#150 trials/block,
'''


experiment.add_site(1780, date='2017-10-06', tetrodes=range(1, 9))
experiment.add_session('16-11-13', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('16-13-46', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('16-20-52', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1820, date='2017-10-07', tetrodes=range(1, 9))
experiment.add_session('16-34-53', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('16-37-21', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('16-44-49', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1860, date='2017-10-09', tetrodes=range(1, 9))
experiment.add_session('15-28-07', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('15-30-29', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('15-36-47', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(1900, date='2017-10-10', tetrodes=range(1, 9))
experiment.add_session('14-32-09', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('14-34-51', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('14-41-44', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(1940, date='2017-10-11', tetrodes=range(1, 9))
experiment.add_session('15-41-44', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('15-44-00', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('15-50-19', 'a', 'behavior', '2afc')#150 trials/block,


experiment.add_site(1980, date='2017-10-12', tetrodes=range(1, 9))
experiment.add_session('14-33-07', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('14-35-24', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('14-42-07', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2020, date='2017-10-15', tetrodes=range(1, 9))
experiment.add_session('14-54-08', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('14-56-24', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('15-03-37', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2060, date='2017-10-16', tetrodes=range(1, 9))
experiment.add_session('15-43-21', None, 'noiseburst', 'laser_tuning_curve')#ref=11
experiment.add_session('15-45-46', 'a', 'tc', 'laser_tuning_curve')#ref=11
experiment.add_session('15-52-01', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2100, date='2017-10-17', tetrodes=range(1, 9))
#experiment.add_session('15-29-23', None, 'noiseburst', 'laser_tuning_curve')#ref=11
#experiment.add_session('15-33-20', None, 'noiseburst', 'laser_tuning_curve')#ref=6
experiment.add_session('15-57-32', None, 'noiseburst', 'laser_tuning_curve')#ref=24
#experiment.add_session('15-36-22', 'a', 'tc', 'laser_tuning_curve')#ref=6
experiment.add_session('16-00-23', 'b', 'tc', 'laser_tuning_curve')#ref=6
experiment.add_session('16-06-27', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2140, date='2017-10-18', tetrodes=range(1, 9))
experiment.add_session('15-25-02', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('15-27-52', 'a', 'tc', 'laser_tuning_curve')#ref=14
experiment.add_session('15-36-58', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2180, date='2017-10-19', tetrodes=range(1, 9))
experiment.add_session('16-43-16', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('16-45-37', 'a', 'tc', 'laser_tuning_curve')#ref=14
experiment.add_session('16-52-00', 'a', 'behavior', '2afc')#150 trials/block,



experiment.add_site(2220, date='2017-10-20', tetrodes=range(1, 9))
experiment.add_session('14-52-54', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('14-55-29', 'a', 'tc', 'laser_tuning_curve')#ref=14
experiment.add_session('15-03-07', 'a', 'behavior', '2afc')#150 trials/block,

'''
experiment.add_site(2260, date='2017-10-23', tetrodes=range(1, 9))
experiment.add_session('16-37-22', None, 'noiseburst', 'laser_tuning_curve')#ref=14
experiment.add_session('16-44-45', None, 'noiseburst', 'laser_tuning_curve')#ref=22, no longer has sound response
'''

experiment.maxDepth = 2220


tetrodeLengthList = [270, 0, 50, 270, 500, 270, 40, 40] #0 is the longest tetrode, other numbers means tetrode is x mm shorter than longest tetrode.
targetRangeLongestTt = (580, 2220)
