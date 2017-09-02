from jaratoolbox import celldatabase

subject = 'pinp025'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-09-01',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# Probe at 1583, waiting 10 mins

exp0.add_site(2012, tetrodes=range(1, 9)).remove_tetrodes([1])
# exp0.add_session('16-42-05', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-45-07', 'a', 'tc', 'am_tuning_curve')
exp0.add_session('17-18-45', 'b', 'am', 'am_tuning_curve')
exp0.add_session('17-34-28', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2111, tetrodes=range(1, 9)).remove_tetrodes([1])
exp0.add_session('17-41-12', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-43-34', 'c', 'tc', 'am_tuning_curve')
exp0.add_session('18-17-49', 'd', 'am', 'am_tuning_curve')

exp0.add_site(2229, tetrodes=range(1, 9)).remove_tetrodes([1])
exp0.add_session('18-51-47', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-54-55','e', 'tc', 'am_tuning_curve')
exp0.add_session('19-30-23', 'f', 'am', 'am_tuning_curve')
# Done for the day
