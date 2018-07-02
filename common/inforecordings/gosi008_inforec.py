from jaratoolbox import celldatabase

subject = 'gosi008'
experiments = []

'''
Experiments with <550 valid trials commented out
'''

'''
experiment = celldatabase.Experiment(subject,
                               '2017-02-22',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-',tetrodes=range(1, 9))
#experiment.add_session('16-57-56', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('17-03-59', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('17-36-07', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('17-23-40', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('17-28-05', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('17-31-21', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-34-44', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-37-46', 'a', 'tc', 'laser_tuning_curve')

experiment = celldatabase.Experiment(subject,
                               '2017-02-23',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(500, date='2017-',tetrodes=range(1, 9))
#experiment.add_session('17-15-26', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-26-04', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-29-23', 'a', 'tc', 'laser_tuning_curve')

experiment = celldatabase.Experiment(subject,
                               '2017-02-24',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(540, date='2017-',tetrodes=range(1, 9))
#experiment.add_session('15-11-17', None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('15-16-08', 'a', 'tc', 'laser_tuning_curve')
#experiment.add_session('15-37-39', None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-48-58',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-00-55', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('16-07-26', 'a', 'behavior', '2afc')
'''

experiment = celldatabase.Experiment(subject,
                                    '2017-02-25',
                                    brainarea='rightAC',
                                    info='')

experiments.append(experiment)

experiment.add_site(540, date='2017-02-25',tetrodes=range(1, 9))
experiment.add_session('15-04-53',  None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('15-08-06', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-17-49', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('15-23-03', 'a', 'behavior', '2afc')


experiment.add_site(580, date='2017-02-26',tetrodes=range(1, 9))
#experiment.add_session('16-47-57',  None, 'noiseburst', 'laser_tuning_curve')
#experiment.add_session('16-50-36', 'a', 'tc', 'laser_tuning_curve')
#experiment.add_session('16-55-34', 'a', 'behavior', '2afc')
experiment.add_session('17-45-02',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-47-48', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-54-27', 'a', 'behavior', '2afc')


experiment.add_site(580, date='2017-02-27',tetrodes=range(1, 9))
experiment.add_session('17-16-06',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-18-45', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-31-04', 'a', 'behavior', '2afc')

'''
experiment.add_site(620, date='2017-02-28',tetrodes=range(1, 9))
experiment.add_session('16-30-25',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-33-04', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-37-49', 'a', 'behavior', '2afc')
'''


experiment.add_site(620, date='2017-03-01',tetrodes=range(1, 9))
experiment.add_session('15-54-23',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-56-54', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-01-31', 'a', 'behavior', '2afc')

'''

experiment.add_site(660, date='2017-03-02',tetrodes=range(1, 9))
experiment.add_session('14-17-03',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-20-02', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-26-03', 'a', 'behavior', '2afc')
'''


experiment.add_site(660, date='2017-03-03',tetrodes=range(1, 9))
experiment.add_session('16-30-04',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-32-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-39-44', 'a', 'behavior', '2afc')


experiment.add_site(700, date='2017-03-04',tetrodes=range(1, 9))
experiment.add_session('17-15-33',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('17-20-19', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-27-42', 'a', 'behavior', '2afc')

'''

experiment.add_site(740, date='2017-03-05',tetrodes=range(1, 9))
experiment.add_session('14-56-21',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-00-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-14-21', 'a', 'behavior', '2afc')


experiment.add_site(740, date='2017-03-06',tetrodes=range(1, 9))
#experiment.add_session('16-17-36',  None, 'noiseburst', 'laser_tuning_curve')#ref 6
#experiment.add_session('16-22-44',  None, 'noiseburst', 'laser_tuning_curve')#ref 14
experiment.add_session('16-28-50',  None, 'noiseburst', 'laser_tuning_curve')#ref 30
experiment.add_session('16-33-23', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-46-55', 'a', 'behavior', '2afc')
'''


experiment.add_site(740, date='2017-03-07',tetrodes=range(1, 9))
experiment.add_session('16-19-22',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('16-21-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-28-27', 'a', 'behavior', '2afc')

'''

experiment.add_site(780, date='2017-03-08',tetrodes=range(1, 9))
experiment.add_session('15-36-09',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('15-39-19', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-47-47', 'a', 'behavior', '2afc')
'''


experiment.add_site(780, date='2017-03-09',tetrodes=range(1, 9))
experiment.add_session('14-52-38',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('14-55-42', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-03-26', 'a', 'behavior', '2afc')


experiment.add_site(820, date='2017-03-10',tetrodes=range(1, 9))
experiment.add_session('17-56-52',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('18-00-34', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-07-43', 'a', 'behavior', '2afc')

'''

experiment.add_site(860, date='2017-03-11',tetrodes=range(1, 9))
experiment.add_session('18-05-03',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('18-07-28', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-14-11', 'a', 'behavior', '2afc')


experiment.add_site(860, date='2017-03-12',tetrodes=range(1, 9))
experiment.add_session('13-43-30',  None, 'noiseburst', 'laser_tuning_curve')
experiment.add_session('13-56-09', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('14-03-54', 'a', 'behavior', '2afc')


experiment.add_site(860, date='2017-03-13',tetrodes=range(1, 9))
#experiment.add_session('16-40-17',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
#experiment.add_session('16-44-50',  None, 'noiseburst', 'laser_tuning_curve') #ref=26
experiment.add_session('16-48-12',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-51-28', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-58-25', 'a', 'behavior', '2afc')
'''

experiment.add_site(860, date='2017-03-14',tetrodes=range(1, 9))
experiment.add_session('17-24-46',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('17-27-54', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-34-28', 'a', 'behavior', '2afc')


experiment.add_site(900, date='2017-03-15',tetrodes=range(1, 9))
#experiment.add_session('15-24-29',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('15-28-22',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
experiment.add_session('15-31-59', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-41-10', 'a', 'behavior', '2afc')


experiment.add_site(940, date='2017-03-16',tetrodes=range(1, 9))
experiment.add_session('14-53-56',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
#experiment.add_session('14-57-55',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
experiment.add_session('15-56-33', 'a', 'tc', 'laser_tuning_curve') #ref=5
experiment.add_session('15-06-26', 'a', 'behavior', '2afc')


experiment.add_site(940, date='2017-03-17',tetrodes=range(1, 9))
experiment.add_session('17-14-26',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('17-17-56', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-24-35', 'a', 'behavior', '2afc')


experiment.add_site(980, date='2017-03-18',tetrodes=range(1, 9))
experiment.add_session('16-19-03',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-23-56', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-32-39', 'a', 'behavior', '2afc')

experiment.add_site(1020, date='2017-03-19',tetrodes=range(1, 9))
experiment.add_session('15-41-28',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('15-43-55', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('15-53-19', 'a', 'behavior', '2afc')

experiment.add_site(1060, date='2017-03-20',tetrodes=range(1, 9))
experiment.add_session('16-22-15',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-25-08', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-33-21', 'a', 'behavior', '2afc')

experiment.add_site(1100, date='2017-03-21',tetrodes=range(1, 9))
experiment.add_session('16-52-14',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-54-40', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-01-32', 'a', 'behavior', '2afc')

experiment.add_site(1140, date='2017-03-22',tetrodes=range(1, 9))
experiment.add_session('11-54-24',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('11-56-42', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('12-03-04', 'a', 'behavior', '2afc')


experiment.add_site(1140, date='2017-03-23',tetrodes=range(1, 9))
experiment.add_session('16-57-30',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-59-57', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('17-10-43', 'a', 'behavior', '2afc')


experiment.add_site(1180, date='2017-03-24',tetrodes=range(1, 9))
experiment.add_session('16-00-46',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('16-03-58', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('16-12-58', 'a', 'behavior', '2afc')


experiment.add_site(1220, date='2017-03-25',tetrodes=range(1, 9))
experiment.add_session('10-53-20',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
experiment.add_session('10-58-49',  None, 'noiseburst', 'laser_tuning_curve') #ref=17
experiment.add_session('11-02-42', 'a', 'tc', 'laser_tuning_curve')#ref=17
experiment.add_session('11-10-50', 'a', 'behavior', '2afc')#ref=17


experiment.add_site(1260, date='2017-03-26',tetrodes=range(1, 9))
experiment.add_session('11-40-13',  None, 'noiseburst', 'laser_tuning_curve') #ref=17
experiment.add_session('11-43-45', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('11-52-12', 'a', 'behavior', '2afc')


experiment.add_site(1260, date='2017-04-02',tetrodes=range(1, 9))
experiment.add_session('18-11-55',  None, 'noiseburst', 'laser_tuning_curve') #ref=2
experiment.add_session('18-17-03', 'a', 'tc', 'laser_tuning_curve')
experiment.add_session('18-25-58', 'a', 'behavior', '2afc')

'''
experiment.add_site(1260, date='2017-04-03',tetrodes=range(1, 9))
experiment.add_session('14-18-47',  None, 'noiseburst', 'laser_tuning_curve') #ref=19. Moved deeper after noiseburst, ran behavior with no ephys recording.
'''

experiment.add_site(1300, date='2017-04-04',tetrodes=range(1, 9))
experiment.add_session('18-53-01',  None, 'noiseburst', 'laser_tuning_curve') #ref=none
experiment.add_session('19-04-38',  None, 'noiseburst', 'laser_tuning_curve') #ref=10
experiment.add_session('19-08-45', 'a', 'tc', 'laser_tuning_curve') #ref=10
experiment.add_session('19-16-52', 'a', 'behavior', '2afc') #ref=10

'''
experiment.add_site(1300, date='2017-04-05',tetrodes=range(1, 9))
experiment.add_session('14-27-31',  None, 'noiseburst', 'laser_tuning_curve') #ref=6 86 trials. 
experiment.add_session('14-40-14', 'a', 'tc', 'laser_tuning_curve') #ref=6  Moved deeper after noiseburst, ran behavior with no ephys recording.
'''

experiment.maxDepth = 1300


#For gosi008 implant tetrode 6 was bad, use an arbitrary number of length just to exclude cells form this tetrode (should have not included it in the exps) 
tetrodeLengthList = [0, 170, 120, 60, 110, 1000, 120, 110] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (540, 1260)
