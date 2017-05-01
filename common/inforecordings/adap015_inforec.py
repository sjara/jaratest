from jaratoolbox import celldatabase as cellDB
subject = 'adap015'
experiments = []

exp = cellDB.Experiment(subject, date ='2016-02-04', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-30-47', 'a', 'tc', 'tuning_curve')
site1.add_session('15-41-31', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-07', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-16-27', 'a', 'tc', 'tuning_curve')
site1.add_session('15-27-13', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-11', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-08-56', 'a', 'tc', 'tuning_curve')
site1.add_session('17-18-34', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-15', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-21-04', 'a', 'tc', 'tuning_curve')
site1.add_session('15-40-25', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-17', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-01-53', 'a', 'tc', 'tuning_curve')
site1.add_session('16-15-41', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-19', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-29-18', 'a', 'tc', 'tuning_curve')
site1.add_session('10-42-16', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-22', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-40-12', 'a', 'tc', 'tuning_curve')
site1.add_session('17-55-18', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-24', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-06-29', 'a', 'tc', 'tuning_curve')
site1.add_session('17-21-23', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-25', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-03-50', 'a', 'tc', 'tuning_curve')
site1.add_session('17-13-16', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-29', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-46-11', 'a', 'tc', 'tuning_curve')
site1.add_session('15-55-06', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-01', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-01-59', 'a', 'tc', 'tuning_curve')
site1.add_session('14-12-01', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-17', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-03-39', 'a', 'tc', 'tuning_curve')
site1.add_session('11-13-12', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-18', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-40-02', 'a', 'tc', 'tuning_curve')
site1.add_session('10-49-54', 'a', 'behavior', '2afc')

for exp in experiments:
    for site in exp.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)
