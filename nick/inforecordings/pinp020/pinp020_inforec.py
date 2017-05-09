from jaratoolbox import celldatabase

subject = 'pinp020'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# exp0.add_site(994, tetrodes=range(1, 9))
# exp0.add_session('10-32-12', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(1581, tetrodes=range(1, 9))
# exp0.add_session('10-37-18', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2100, tetrodes=range(1, 9))
# exp0.add_session('10-41-12', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2607, tetrodes=range(1, 9))
# exp0.add_session('10-44-48', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2702, tetrodes=range(1, 9))
exp0.add_session('10-57-28', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-01-52', 'a', 'am', 'am_tuning_curve')
exp0.add_session('11-19-15', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2802, tetrodes=range(1, 9))
exp0.add_session('12-06-40', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-09-17', 'c', 'am', 'am_tuning_curve')
exp0.add_session('12-24-37', 'd', 'tc', 'am_tuning_curve')
