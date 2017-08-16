from jaratoolbox import celldatabase

subject = 'pinp024'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-08-15',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

#Mouse on the rig at 1401hrs, waiting 10 mins for brain to settle
#Tetrodes at 18538um

exp0.add_site(1853, tetrodes=range(1, 9))
exp0.add_session('14-20-39', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-24-06', 'a', 'tc', 'am_tuning_curve')
exp0.add_session('14-42-31', 'b', 'am', 'am_tuning_curve')

exp0.add_site(1956, tetrodes=range(1, 9))
exp0.add_session('15-03-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-06-22', 'c', 'tc', 'am_tuning_curve')
exp0.add_session('15-24-08', 'd', 'am', 'am_tuning_curve')

exp0.add_site(2061, tetrodes=range(1, 9))
exp0.add_session('15-50-33', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-54-24', 'e', 'tc', 'am_tuning_curve')
exp0.add_session('16-11-30', 'f', 'am', 'am_tuning_curve')

exp0.add_site(2159, tetrodes=range(1, 9))
exp0.add_session('16-31-03', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-37-07', 'g', 'tc', 'am_tuning_curve')
exp0.add_session('16-54-24', 'h', 'am', 'am_tuning_curve')

exp0.add_site(2253, tetrodes=range(1, 9))
exp0.add_session('17-13-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-18-53', 'i', 'tc', 'am_tuning_curve')
exp0.add_session('17-35-48', 'j', 'am', 'am_tuning_curve')

exp0.add_site(2355, tetrodes=range(1, 9))
exp0.add_session('17-55-45', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-58-04', 'k', 'tc', 'am_tuning_curve')
exp0.add_session('18-18-42', 'l', 'am', 'am_tuning_curve')

exp0.add_site(2458, tetrodes=range(1, 9))
exp0.add_session('18-41-08', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-43-32', 'm', 'tc', 'am_tuning_curve')
exp0.add_session('19-10-44', 'n', 'am', 'am_tuning_curve')

exp0.add_site(2556, tetrodes=range(1, 9))
exp0.add_session('19-37-04', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('19-39-32', 'p', 'tc', 'am_tuning_curve')
# exp0.add_session('19-10-44', 'n', 'am', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject,
                               '2017-08-16',
                               brainarea='rightAstr',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp1)

#Mouse on the rig at 0955hrs, waiting 10 mins for brain to settle
#Tetrodes at 1913um

exp1.add_site(1913, tetrodes=range(1, 9))
exp1.add_session('10-07-33', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('10-09-44', 'a', 'tc', 'am_tuning_curve')
exp1.add_session('10-43-47', 'b', 'am', 'am_tuning_curve')

exp1.add_site(2068, tetrodes=range(1, 9))
exp1.add_session('11-12-31', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-14-47', 'c', 'tc', 'am_tuning_curve')
#Didn't do AM

exp1.add_site(2163, tetrodes=range(1, 9))
exp1.add_session('11-49-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-52-21', 'd', 'tc', 'am_tuning_curve')
exp1.add_session('12-15-13', 'e', 'am', 'am_tuning_curve')

exp1.add_site(2265, tetrodes=range(1, 9))
exp1.add_session('13-48-16', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-50-42', 'f', 'tc', 'am_tuning_curve')
exp1.add_session('14-23-44', 'g', 'am', 'am_tuning_curve')
