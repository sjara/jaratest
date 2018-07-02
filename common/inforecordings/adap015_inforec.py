from jaratoolbox import celldatabase as cellDB
subject = 'adap015'
experiments = []

experiment = cellDB.Experiment(subject, date ='2016-02-04', brainarea='rightAStr', info='')
experiments.append(experiment)
site1 = experiment.add_site(depth=2000+320*3.250, date='2016-02-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-30-47', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-41-31', 'a', 'behavior', '2afc')

site1 = experiment.add_site(depth=2000+320*3.375, date='2016-02-07', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-16-27', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-27-13', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.625, date='2016-02-11', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-08-56', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-18-34', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.75, date='2016-02-15', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-21-04', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-40-25', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.875, date='2016-02-17', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('16-01-53', 'a', 'tc', 'tuning_curve')
experiment.add_session('16-15-41', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.000, date='2016-02-19', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('10-29-18', 'a', 'tc', 'tuning_curve')
experiment.add_session('10-42-16', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.000, date='2016-02-22', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-40-12', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-55-18', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.125, date='2016-02-24', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-06-29', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-21-23', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.125, date='2016-02-25', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-03-50', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-13-16', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.125, date='2016-02-29', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-46-11', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-55-06', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.25, date='2016-03-01', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-01-59', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-12-01', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.25, date='2016-03-17', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('11-03-39', 'a', 'tc', 'tuning_curve')
experiment.add_session('11-13-12', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.25, date='2016-03-18', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('10-40-02', 'a', 'tc', 'tuning_curve')
experiment.add_session('10-49-54', 'a', 'behavior', '2afc')

experiment.maxDepth = 2000+320*4.25

for experiment in experiments:
    for site in experiment.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)


tetrodeLengthList = [1260, 260, 540, 340, 0, 240, 110, 320] #[1.260,0.260,0.540,0.340,0.000,0.240,0.110,0.320] #0 is the longest tetrode, other numbers means tetrode is x mm shorter than longest tetrode.
targetRangeLongestTt = (2000, 3000) #(2.00, 3.00)
