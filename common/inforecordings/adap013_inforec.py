from jaratoolbox import celldatabase as cellDB
subject = 'adap013'
experiments = []

exp = cellDB.Experiment(subject, date ='2016-02-11', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-13-47', 'a', 'tc', 'tuning_curve')
site1.add_session('15-23-56', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-22', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-34-29', 'a', 'tc', 'tuning_curve')
site1.add_session('12-44-19', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-24', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-16-44', 'a', 'tc', 'tuning_curve')
site1.add_session('10-27-12', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-26', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-45-11', 'a', 'tc', 'tuning_curve')
site1.add_session('10-59-09', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-02-28', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-35-15', 'a', 'tc', 'tuning_curve')
site1.add_session('15-44-01', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-01', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-31-17', 'a', 'tc', 'tuning_curve')
site1.add_session('11-43-31', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-02', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-20-53', 'a', 'tc', 'tuning_curve')
site1.add_session('14-29-49', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-16', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=1.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-47-24', 'a', 'tc', 'tuning_curve')
site1.add_session('13-57-37', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-18', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-26-01', 'a', 'tc', 'tuning_curve')
site1.add_session('13-36-20', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-20', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-01-26', 'a', 'tc', 'tuning_curve')
site1.add_session('14-10-47', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-21', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-22-32', 'a', 'tc', 'tuning_curve')
site1.add_session('15-33-19', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-23', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-17-23', 'a', 'tc', 'tuning_curve')
site1.add_session('14-27-04', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-28', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.500, tetrodes=[1,2,4,5,6,7,8])
site1.add_session('13-44-01', 'a', 'tc', 'tuning_curve')
site1.add_session('13-57-56', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-03-30', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-43-52', 'a', 'tc', 'tuning_curve')
site1.add_session('13-58-51', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-01', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-56-47', 'a', 'tc', 'tuning_curve')
site1.add_session('15-06-29', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-05', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-18-41', 'a', 'tc', 'tuning_curve')
site1.add_session('14-27-44', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-07', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-18-33', 'a', 'tc', 'tuning_curve')
site1.add_session('14-34-19', 'a', 'behavior', '2afc')

exp = cellDB.Experiment(subject, date ='2016-04-14', brainarea='rightAStr', info='')
experiments.append(exp)
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-06-33', 'a', 'tc', 'tuning_curve')
site1.add_session('17-19-26', 'a', 'behavior', '2afc')

for exp in experiments:
    for site in exp.sites:
        site.clusterFolder = 'multisession_{}_site1'.format(site.date)
