from jaratoolbox import celldatabase as cellDB
subject = 'adap012'
experiments = []


experiment = cellDB.Experiment(subject, date ='2016-02-04', brainarea='rightAStr', info='') 
experiments.append(experiment)
site1 = experiment.add_site(depth=2340, date='2016-02-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-22-27', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-24-57', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-31-33', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('12-35-00', 'c', 'tc', 'laser_tuning_curve')
experiment.add_session('12-41-31', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2380, date='2016-02-05', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-58-26', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-01-15', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-09-08', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('13-14-22', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2380, date='2016-02-06', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-28-02', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-30-13', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-39-01', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('14-45-35', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2420, date='2016-02-07', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-01-59', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('15-03-52', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('15-10-08', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('15-18-13', 'c', 'tc', 'laser_tuning_curve')
experiment.add_session('15-23-48', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2420, date='2016-02-08', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('11-47-03', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('11-49-40', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('11-57-55', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('12-05-36', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2420, date='2016-02-09', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-46-27', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-49-40', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-58-42', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('13-05-14', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2460, date='2016-02-10', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-21-26', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-24-00', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-31-47', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('13-33-42', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('13-40-04', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2460, date='2016-02-11', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('09-57-54', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('10-00-46', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('10-09-15', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2500, date='2016-02-12', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('11-18-54', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('11-21-35', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('11-28-08', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('11-33-58', 'c', 'tc', 'laser_tuning_curve')
experiment.add_session('11-39-08', 'd', 'tc', 'laser_tuning_curve')
experiment.add_session('11-45-27', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2500, date='2016-02-13', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-59-55', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('16-01-57', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('16-08-33', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2500, date='2016-02-15', tetrodes=[7,8])
experiment.add_session('12-13-08', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-15-29', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-28-28', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2500, date='2016-02-16', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-34-26', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-36-45', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-42-42', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('13-50-54', 'c', 'tc', 'laser_tuning_curve')
experiment.add_session('13-55-09', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2540, date='2016-02-17', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-33-26', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-36-03', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-44-03', 'b', 'tc', 'laser_tuning_curve')
experiment.add_session('12-52-13', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2540, date='2016-02-18', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-53-38', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-55-25', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-04-25', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2580, date='2016-02-20', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-42-01', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-53-32', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('15-02-25', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2580, date='2016-02-21', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-13-01', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-15-03', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-21-00', 'b', 'tc', 'laser_tuning_curve') 
experiment.add_session('14-27-41', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2580, date='2016-02-22', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-36-19', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('15-58-57', 'b', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('16-04-36', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2580, date='2016-02-25', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-52-56', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-55-58', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-02-36', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-07-32', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2580, date='2016-03-01', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-47-13', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-49-45', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-56-35', 'a', 'behavior', paradigm='2afc')

site1 = experiment.add_site(depth=2660, date='2016-03-02', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-11-23', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('15-18-24', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('15-27-46', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2660, date='2016-03-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-12-18', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('15-16-55', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('15-23-27', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2660, date='2016-03-07', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-21-21', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-24-14', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-31-45', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2740, date='2016-03-08', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-14-52', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-17-59', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-29-12', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2740, date='2016-03-09', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-54-28', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-56-27', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-04-44', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2740, date='2016-03-11', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-29-09', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-30-56', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-37-52', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2820, date='2016-03-15', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-18-38', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-20-29', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-26-57', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2820, date='2016-03-16', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-41-03', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-43-29', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-51-49', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2860, date='2016-03-17', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-33-03', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-35-48', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-43-53', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2860, date='2016-03-18', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-18-00', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-20-01', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-26-30', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2900, date='2016-03-21', tetrodes=[1,2,3,4,5,6,7])
experiment.add_session('13-33-40', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-36-34', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-43-09', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2900, date='2016-03-22', tetrodes=[1,2,3,4,5,6,7])
experiment.add_session('12-57-52', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-00-05', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-07-12', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2940, date='2016-03-23', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-47-28', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-49-37', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-57-54', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2940, date='2016-03-24', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-54-33', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-56-41', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-01-29', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2980, date='2016-03-28', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-55-48', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-58-04', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-05-09', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=2980, date='2016-03-29', tetrodes=[1,2,3,4,5,6,7])
experiment.add_session('14-01-04', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('14-03-20', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('14-07-57', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=3020, date='2016-03-31', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-08-18', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('13-10-45', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('13-16-33', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=3060, date='2016-04-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-04-51', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('15-07-14', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('15-19-01', 'a', 'behavior', paradigm='2afc')


site1 = experiment.add_site(depth=3060, date='2016-04-05', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-34-22', None, 'noiseburst', 'laser_tuning_curve') #amp=0.1
experiment.add_session('12-37-38', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
experiment.add_session('12-43-43', 'a', 'behavior', paradigm='2afc')

experiment.maxDepth = 3100

for experiment in experiments:
    for site in experiment.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)

tetrodeLengthList = [560,300,0,560,0,300,180,180] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (2340, 3060)
