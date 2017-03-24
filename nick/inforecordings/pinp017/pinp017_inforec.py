from jaratoolbox import celldatabase

subject = 'pinp017'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-03-22',
                               brainarea='rightAC',
                               info=['medialDiI', 'facingLateral'])
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

exp1 = celldatabase.Experiment(subject,
                               '2017-03-23',
                               brainarea='rightAC',
                               info=['medialDiD', 'facingLateral'])
experiments.append(exp1)

exp1.add_site(1281, tetrodes=range(1, 9))
exp1.add_session('12-52-23', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-54-27', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-55-40', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-58-33', 'a', 'am', 'am_tuning_curve')
exp1.add_session('13-15-29', 'b', 'tc', 'am_tuning_curve')
exp1.add_session('13-48-43', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('13-49-53', None, 'lasertrain2', 'am_tuning_curve')

exp1.add_site(1414, tetrodes=range(1, 9))
exp1.add_session('13-53-16', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-56-38', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-58-03', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-01-51', 'c', 'am', 'am_tuning_curve')
exp1.add_session('14-19-12', 'd', 'tc', 'am_tuning_curve')
exp1.add_session('15-08-45', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('15-09-56', None, 'lasertrain2', 'am_tuning_curve')

exp1.add_site(1518, tetrodes=range(1, 9))
exp1.add_session('15-14-31', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-15-52', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-17-16', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-20-13', 'e', 'am', 'am_tuning_curve')
exp1.add_session('15-37-29', 'f', 'tc', 'am_tuning_curve')
exp1.add_session('16-08-47', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('16-10-01', None, 'lasertrain2', 'am_tuning_curve')

exp1.add_site(1604, tetrodes=range(1, 9))
exp1.add_session('16-14-38', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-15-57', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-17-15', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-20-49', 'g', 'am', 'am_tuning_curve')
exp1.add_session('16-38-29', 'h', 'tc', 'am_tuning_curve')
# removed the trodes, forgetting to take the last 2 laser sessions. Hopefully all is well
