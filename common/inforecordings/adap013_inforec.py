from jaratoolbox import celldatabase as cellDB
subject = 'adap013'
experiments = []

experiment = cellDB.Experiment(subject, date ='2016-02-11', brainarea='rightAStr', info='')
experiments.append(experiment)
site1 = experiment.add_site(depth=2000+320*1.25, date='2016-02-11', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-13-47', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-23-56', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.375, date='2016-02-22', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('12-34-29', 'a', 'tc', 'tuning_curve')
experiment.add_session('12-44-19', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.50, date='2016-02-24', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('10-16-44', 'a', 'tc', 'tuning_curve')
experiment.add_session('10-27-12', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.625, date='2016-02-26', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('10-45-11', 'a', 'tc', 'tuning_curve')
experiment.add_session('10-59-09', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.625, date='2016-02-28', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-35-15', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-44-01', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.75, date='2016-03-01', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('11-31-17', 'a', 'tc', 'tuning_curve')
experiment.add_session('11-43-31', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.75, date='2016-03-02', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-20-53', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-29-49', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*1.875, date='2016-03-16', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-47-24', 'a', 'tc', 'tuning_curve')
experiment.add_session('13-57-37', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.000, date='2016-03-18', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-26-01', 'a', 'tc', 'tuning_curve')
experiment.add_session('13-36-20', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.125, date='2016-03-20', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-01-26', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-10-47', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.250, date='2016-03-21', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('15-22-32', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-33-19', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.375, date='2016-03-23', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-17-23', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-27-04', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.500, date='2016-03-28', tetrodes=[1,2,4,5,6,7,8])
experiment.add_session('13-44-01', 'a', 'tc', 'tuning_curve')
experiment.add_session('13-57-56', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.625, date='2016-03-30', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('13-43-52', 'a', 'tc', 'tuning_curve')
experiment.add_session('13-58-51', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.75, date='2016-04-01', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-56-47', 'a', 'tc', 'tuning_curve')
experiment.add_session('15-06-29', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*2.875, date='2016-04-05', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-18-41', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-27-44', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.000, date='2016-04-07', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('14-18-33', 'a', 'tc', 'tuning_curve')
experiment.add_session('14-34-19', 'a', 'behavior', '2afc')


site1 = experiment.add_site(depth=2000+320*3.50, date='2016-04-14', tetrodes=[1,2,3,4,5,6,7,8])
experiment.add_session('17-06-33', 'a', 'tc', 'tuning_curve')
experiment.add_session('17-19-26', 'a', 'behavior', '2afc')

experiment.maxDepth = 2000+320*3.5

for experiment in experiments:
    for site in experiment.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)

tetrodeLengthList = [420, 530, 0, 80, 490, 140, 230, 360] #[0.420,0.530,0.000,0.080,0.490,0.140,0.230,0.360] #0 is the longest tetrode, other numbers means tetrode is x mm shorter than longest tetrode.
targetRangeLongestTt = (2000, 3110) #(2.0,3.11)
