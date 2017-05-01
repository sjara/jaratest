from jaratoolbox import celldatabase as cellDB
subject = 'adap017'
experiments = []

exp = cellDB.Experiment(subject, date ='2016-03-16', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-39-32', 'a', 'tc', 'tuning_curve')
site1.add_session('17-49-15', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-18', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-17-33', 'a', 'tc', 'tuning_curve')
site1.add_session('17-27-07', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-22', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-33-18', 'a', 'tc', 'tuning_curve')
site1.add_session('14-43-23', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-24', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-35-15', 'a', 'tc', 'tuning_curve')
site1.add_session('15-47-08', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-29', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-07', 'a', 'tc', 'tuning_curve')
site1.add_session('16-56-05', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-31', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-18-46', 'a', 'tc', 'tuning_curve')
site1.add_session('15-45-00', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-04', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-52', 'a', 'tc', 'tuning_curve')
site1.add_session('16-57-16', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-06', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-25-26', 'a', 'tc', 'tuning_curve')
site1.add_session('17-36-02', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-08', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-32-00', 'a', 'tc', 'tuning_curve')
site1.add_session('18-49-50', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-13', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-51-52', 'a', 'tc', 'tuning_curve')
site1.add_session('16-01-53', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-15', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-49-44', 'a', 'tc', 'tuning_curve')
site1.add_session('15-59-09', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-19', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-06-15', 'a', 'tc', 'tuning_curve')
site1.add_session('17-23-02', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-21', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-15-39', 'a', 'tc', 'tuning_curve')
site1.add_session('15-24-53', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-24', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-44-46', 'a', 'tc', 'tuning_curve')
site1.add_session('14-57-22', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-26', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-38-16', 'a', 'tc', 'tuning_curve')
site1.add_session('18-01-51', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-28', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-10-36', 'a', 'tc', 'tuning_curve')
site1.add_session('14-23-22', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-05-02', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-07-08', 'a', 'tc', 'tuning_curve')
site1.add_session('17-17-00', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-05-04', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-08-26', 'a', 'tc', 'tuning_curve')
site1.add_session('16-17-52', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-05-05', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-37-41', 'a', 'tc', 'tuning_curve')
site1.add_session('15-47-52', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-05-09', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=5.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-37-27', 'a', 'tc', 'tuning_curve')
site1.add_session('17-46-38', 'a', 'behavior', '2afc')

for exp in experiments:
    for site in exp.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)
