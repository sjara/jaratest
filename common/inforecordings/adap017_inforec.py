from jaratoolbox import celldatabase as cellDB
subject = 'adap017'
experiments = []

experiment = cellDB.Experiment(subject, date ='2016-03-16', brainarea='rightAStr', info='')
experiments.append(experiment)
site1 = experiment.add_site(depth=2000+320*2.75, date='2016-03-16', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-39-32', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-49-15', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.875, date='2016-03-18', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-17-33', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-27-07', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.00, date='2016-03-22', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-33-18', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-43-23', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.125, date='2016-03-24', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-35-15', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-47-08', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.25, date='2016-03-29', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('16-46-07', 'a', 'tc', 'tuning_curve')
experiment.add_session('16-56-05', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.375, date='2016-03-31', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-18-46', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-45-00', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.50, date='2016-04-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('16-46-52', 'a', 'tc', 'tuning_curve')
experiment.add_session('16-57-16', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.625, date='2016-04-06', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-25-26', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-36-02', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.75, date='2016-04-08', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('18-32-00', 'a', 'tc', 'tuning_curve')
experiment.add_session('18-49-50', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.875, date='2016-04-13', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-51-52', 'a', 'tc', 'tuning_curve')
experiment.add_session('16-01-53', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.000, date='2016-04-15', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-49-44', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-59-09', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.125, date='2016-04-19', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-06-15', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-23-02', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.25, date='2016-04-21', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-15-39', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-24-53', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.375, date='2016-04-24', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-44-46', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-57-22', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.50, date='2016-04-26', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-38-16', 'a', 'tc', 'tuning_curve')
experiment.add_session('18-01-51', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.625, date='2016-04-28', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-10-36', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-23-22', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.75, date='2016-05-02', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-07-08', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-17-00', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.875, date='2016-05-04', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('16-08-26', 'a', 'tc', 'tuning_curve')
experiment.add_session('16-17-52', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*4.875, date='2016-05-05', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-37-41', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-47-52', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*5.00, date='2016-05-09', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-37-27', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-46-38', 'a', 'behavior', '2afc')

experiment.maxDepth = 2000+320*5.00

for experiment in experiments:
    for site in experiment.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)


tetrodeLengthList = [504, 0, 209, 209, 209, 705, 459, 504] #[0.504,0.000,0.209,0.209,0.209,0.705,0.459,0.504] #0 is the longest tetrode, other numbers means tetrode is x mm shorter than longest tetrode.
targetRangeLongestTt = (2000, 3170) #(2.0,3.17)
