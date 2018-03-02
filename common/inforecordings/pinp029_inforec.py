from jaratoolbox import celldatabase

subject = 'pinp029'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-11-08',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# Probe at 2000 at 1056hrs, waiting 10 mins
# exp0.add_site(2052, tetrodes=[1, 2, 3, 4, 5, 7, 8])
exp0.add_site(2052, tetrodes=[1, 2])
exp0.add_session('11-59-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-02-00', 'a', 'tc', 'am_tuning_curve')
exp0.add_session('12-34-35', 'b', 'am', 'am_tuning_curve')

# exp0.add_site(2155, tetrodes=[1, 2, 3, 4, 5, 7, 8])
exp0.add_site(2155, tetrodes=[1, 2])
exp0.add_session('13-06-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-09-13', 'c', 'tc', 'am_tuning_curve')
exp0.add_session('13-42-08', 'd', 'am', 'am_tuning_curve')

# exp0.add_site(2255, tetrodes=[1, 2, 3, 4, 6, 7, 8])
exp0.add_site(2255, tetrodes=[1, 2])
exp0.add_session('14-13-54', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-17-05', 'e', 'tc', 'am_tuning_curve')
exp0.add_session('14-49-53', 'f', 'am', 'am_tuning_curve')

# exp0.add_site(2356, tetrodes=[1, 2, 3, 4, 6, 7, 8])
exp0.add_site(2356, tetrodes=[1, 2])
exp0.add_session('15-24-27', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-26-48', 'g', 'tc', 'am_tuning_curve')
exp0.add_session('16-00-41', 'h', 'am', 'am_tuning_curve')
exp0.maxDepth = 2356

exp1 = celldatabase.Experiment(subject,
                               '2017-11-09',
                               brainarea='rightAstr',
                               info=['DiD', 'facingPosterior'])
experiments.append(exp1)

# Probe at 2055 at 1058hrs, waiting 10 mins
# exp1.add_site(2055, tetrodes=[1, 2, 3, 4, 6, 7, 8])
# exp1.add_session('11-18-50', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2176, tetrodes=[1, 2, 3, 4, 5, 7, 8])
exp1.add_site(2176, tetrodes=[5, 7, 8])
exp1.add_session('11-30-22', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-34-47', 'a', 'tc', 'am_tuning_curve')
exp1.add_session('12-08-57', 'b', 'am', 'am_tuning_curve')

# exp1.add_site(2304, tetrodes=[1, 2, 3, 4, 6, 7, 8])
exp1.add_site(2304, tetrodes=[6, 7, 8])
exp1.add_session('12-59-06', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-01-22', 'c', 'tc', 'am_tuning_curve')
exp1.add_session('13-38-51', 'd', 'am', 'am_tuning_curve')

# exp1.add_site(2450, tetrodes=[1, 2, 3])
# exp1.add_session('14-06-24', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('14-09-32', 'e', 'tc', 'am_tuning_curve')
# exp1.add_session('14-41-57', 'f', 'am', 'am_tuning_curve')

# exp1.add_site(2603, tetrodes=[1, 2, 3])
# exp1.add_session('14-06-24', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('14-09-32', 'e', 'tc', 'am_tuning_curve')
# exp1.add_session('14-41-57', 'f', 'am', 'am_tuning_curve')

# exp1.add_site(2706, tetrodes=[1, 2, 3])
# exp1.add_session('14-06-24', None, 'noiseburst', 'am_tuning_curve') #No more responses, stopping here
exp1.maxDepth = 2706

exp2 = celldatabase.Experiment(subject,
                               '2017-11-10',
                               brainarea='rightAstr',
                               info=['posteriorDiI', 'facingPosterior'])
experiments.append(exp2)

# Probe at 2039 at 1112hrs, waiting 10 mins

# exp2.add_site(2039, tetrodes=[1, 2, 3, 4, 5, 7, 8])
exp2.add_site(2039, tetrodes=[7, 8])
exp2.add_session('11-40-16', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-42-40', 'a', 'tc', 'am_tuning_curve')
exp2.add_session('12-16-54', 'b', 'am', 'am_tuning_curve')

# exp2.add_site(2204, tetrodes=[1, 2, 3, 4])
# exp2.add_session('12-45-46', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('12-55-12', 'c', 'tc', 'am_tuning_curve')
# exp2.add_session('13-27-43', 'd', 'am', 'am_tuning_curve')

# exp2.add_site(2350, tetrodes=[1, 2, 3, 4, 5])
# exp2.add_session('14-02-29', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('14-05-24', 'e', 'tc', 'am_tuning_curve')
# exp2.add_session('14-39-39', 'f', 'am', 'am_tuning_curve')

# exp2.add_site(2508, tetrodes=[1, 2, 3, 4, 6, 7, 8])
exp2.add_site(2508, tetrodes=[7, 8])
exp2.add_session('15-03-53', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-06-37', 'g', 'tc', 'am_tuning_curve')
exp2.add_session('15-56-02', 'h', 'am', 'am_tuning_curve')
exp2.maxDepth = 2508
