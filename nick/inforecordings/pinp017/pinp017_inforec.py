from jaratoolbox import celldatabase

subject = 'pinp017'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-03-22',
                               brainarea='rightAC',
                               info='medialDiI')
experiments.append(exp0)

exp0.add_site(1143, tetrodes=range(1, 9))
exp0.add_session('15-05-37', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-10-41', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-12-04', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-14-02', 'a', 'am', 'am_tuning_curve')
exp0.add_session('15-28-38', 'b', 'tc', 'am_tuning_curve')
exp0.add_session('16-04-44', None, 'laserpulse2', 'am_tuning_curve')
exp0.add_session('16-06-27', None, 'lasertrain2', 'am_tuning_curve')

exp0.add_site(1247, tetrodes=range(1, 9))
exp0.add_session('16-11-37', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-12-59', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-14-14', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-17-21', 'c', 'am', 'am_tuning_curve')
exp0.add_session('16-34-32', 'd', 'tc', 'am_tuning_curve')
exp0.add_session('17-08-04', None, 'laserpulse2', 'am_tuning_curve')
exp0.add_session('17-09-22', None, 'lasertrain2', 'am_tuning_curve')

exp0.add_site(1338, tetrodes=range(2, 9))
exp0.add_session('17-20-03', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-21-38', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-23-37', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-27-07', 'e', 'am', 'am_tuning_curve')
exp0.add_session('17-42-17', 'f', 'tc', 'am_tuning_curve')
exp0.add_session('18-13-31', None, 'laserpulse2', 'am_tuning_curve')
exp0.add_session('18-15-07', None, 'lasertrain', 'am_tuning_curve')
