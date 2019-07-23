from jaratoolbox import celldatabase

subject = 'pinp028'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-10-17',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# Probe at 2365, waiting 10 mins

exp0.add_site(2365, tetrodes=range(1, 9)).remove_tetrodes([6])
exp0.add_session('14-44-53', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-49-44', 'a', 'am', 'am_tuning_curve')
exp0.add_session('15-06-24', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2501, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
exp0.add_session('15-44-32', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-50-08', 'c', 'am', 'am_tuning_curve')
exp0.add_session('16-05-54', 'd', 'tc', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject,
                               '2017-10-27',
                               brainarea='rightAstr',
                               info=['anteriorDiD', 'facingPosterior'])

experiments.append(exp1)

#waiting at 2015um

#nothing here
# exp1.add_site(2108, tetrodes=[1, 3, 4, 5, 6, 7, 8])
# exp1.add_session('12-57-54', None, 'noiseburst', 'am_tuning_curve')

#Nothing
# exp1.add_site(2207, tetrodes=[1, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-08-53', None, 'noiseburst', 'am_tuning_curve')

#nothing
# exp1.add_site(2268, tetrodes=[2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-21-24', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2351, tetrodes=[2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-26-10', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2451, tetrodes=[2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-37-33', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2551, tetrodes=[2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-45-17', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2626, tetrodes=[2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('13-52-56', None, 'noiseburst', 'am_tuning_curve')

exp1.add_site(2721, tetrodes=[1, 2, 3])
# exp1.add_session('14-25-29', None, 'noiseburst', 'am_tuning_curve') #Bad ref, missing a spike
# exp1.add_session('14-31-40', 'a', 'am', 'am_tuning_curve') #Bad ref, missing a spike
exp1.add_session('14-50-30', None, 'noiseburst', 'am_tuning_curve') 
exp1.add_session('14-53-12', 'b', 'am', 'am_tuning_curve') 
exp1.add_session('15-09-46', 'c', 'tc', 'am_tuning_curve')

exp1.add_site(2832, tetrodes=[1, 2])
exp1.add_session('15-51-40', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-55-15', 'd', 'tc', 'am_tuning_curve')
exp1.add_session('16-36-38', 'e', 'am', 'am_tuning_curve')
