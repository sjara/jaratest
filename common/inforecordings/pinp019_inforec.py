from jaratoolbox import celldatabase

subject = 'pinp019'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-04-26',
                               brainarea='rightThal',
                               info=['medialDiI', 'facingLateral'])
experiments.append(exp0)

# exp0.add_site(3125, tetrodes=range(1, 9))
# exp0.add_session('14-19-08', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-20-53', None, 'laserpulse', 'am_tuning_curve') #No laser response

# exp0.add_site(3255, tetrodes=range(1, 9))
# exp0.add_session('14-25-18', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-27-03', None, 'laserpulse', 'am_tuning_curve') #No laser response

# exp0.add_site(3353, tetrodes=range(1, 9))
# exp0.add_session('14-29-48', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-32-20', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('14-34-20', None, 'laserpulse2.5mW', 'am_tuning_curve') #No laser response

# exp0.add_site(3449, tetrodes=range(1, 9))
# exp0.add_session('14-36-53', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-38-32', None, 'laserpulse', 'am_tuning_curve') #No laser responses

# exp0.add_site(3549, tetrodes=range(1, 9))
# exp0.add_session('14-53-36', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-55-14', None, 'laserpulse', 'am_tuning_curve') #No laser responses

# exp0.add_site(3658, tetrodes=range(1, 9))
# exp0.add_session('15-00-16', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('15-01-30', None, 'laserpulse', 'am_tuning_curve') #No laser response

exp0.add_site(3552, tetrodes=range(1, 9))
exp0.add_session('15-07-21', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
exp0.add_session('15-09-22', None, 'laserpulse', 'am_tuning_curve') #No laser response
exp0.add_session('15-11-03', None, 'lasertrain', 'am_tuning_curve') #No laser response
exp0.add_session('15-12-59', 'a', 'am', 'am_tuning_curve')
exp0.maxDepth = 3552

exp1 = celldatabase.Experiment(subject,
                               '2017-04-27',
                               brainarea='rightThal',
                               info=['DiD', 'facingLateral'])
experiments.append(exp1)

exp1.add_site(3868, tetrodes=range(1, 9)).remove_tetrodes([6, 8])
exp1.add_session('15-32-40', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-33-59', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-35-16', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-37-25', 'a', 'tc', 'am_tuning_curve')
exp1.add_session('16-13-57', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3925, tetrodes=range(1, 9))
exp1.add_session('16-35-34', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-37-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-38-44', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-41-01', 'c', 'tc', 'am_tuning_curve')
exp1.add_session('17-14-41', 'd', 'am', 'am_tuning_curve')

exp1.add_site(4003, tetrodes=range(1, 9))
exp1.add_session('17-34-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-36-24', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-37-38', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-39-34', 'e', 'tc', 'am_tuning_curve')
exp1.add_session('18-12-29', 'f', 'am', 'am_tuning_curve')
exp1.maxDepth = 4003

exp2 = celldatabase.Experiment(subject,
                               '2017-05-02',
                               brainarea='rightThal',
                               info=['lateralDiI', 'facingLateral'])
experiments.append(exp2)

# exp2.add_site(3905, tetrodes=range(1, 9))
# exp2.add_session('11-32-32', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('11-36-19', 'a', 'am', 'am_tuning_curve')
#I got all the way here and no response to sounds. Too lateral??
exp2.maxDepth = 3905

exp3 = celldatabase.Experiment(subject,
                               '2017-05-03',
                               brainarea='rightThal',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp3)

exp3.add_site(3452, tetrodes=range(1, 9)).remove_tetrodes([7])
exp3.add_session('14-19-13', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-21-47', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('14-23-08', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('14-25-11', 'a', 'am', 'am_tuning_curve')
exp3.add_session('14-41-00', 'b', 'tc', 'am_tuning_curve')
exp3.maxDepth = 3452
