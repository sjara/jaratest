from jaratoolbox import celldatabase

subject = 'pinp018'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-04-06',
                               brainarea='rightAC',
                               info=['medialDiI', 'facingLateral'])
experiments.append(exp0)

# exp0.add_site(1021, tetrodes=range(1, 9))
# exp0.add_session('14-26-00', None, 'noiseburst', 'am_tuning_curve') #Noise burst response
# exp0.add_session('14-33-52', None, 'laserpulse', 'am_tuning_curve') # No laser response

# exp0.add_site(1103, tetrodes=range(1, 9))
# exp0.add_session('14-38-53', None, 'laserpulse', 'am_tuning_curve') #Super weak if anything
# exp0.add_session('14-41-09', None, 'noiseburst', 'am_tuning_curve') #Fading sound response, some off

# exp0.add_site(1150, tetrodes=range(1, 9))
# exp0.add_session('14-43-35', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('14-44-48', None, 'noiseburst', 'am_tuning_curve') #Still sound responses


# exp0.add_site(1202, tetrodes=range(1, 9))
# exp0.add_session('14-49-08', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('14-50-35', None, 'noiseburst', 'am_tuning_curve') #Still sound response


# exp0.add_site(1252, tetrodes=range(1, 9))
# exp0.add_session('14-54-41', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('14-57-00', None, 'noiseburst', 'am_tuning_curve') #Still sound response

# exp0.add_site(1303, tetrodes=range(1, 9))
# exp0.add_session('15-18-50', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('15-20-14', None, 'noiseburst', 'am_tuning_curve') #Weak sound response

# exp0.add_site(1354, tetrodes=range(1, 9))
# exp0.add_session('15-22-50', None, 'laserpulse', 'am_tuning_curve') #No laser response
# exp0.add_session('15-24-46', None, 'noiseburst', 'am_tuning_curve') #Long latency sound response

# exp0.add_site(1403, tetrodes=range(1, 9))
# exp0.add_session('15-26-19', None, 'laserpulse', 'am_tuning_curve') #No laser response

# exp0.add_site(1454, tetrodes=range(1, 9))
# exp0.add_session('15-29-24', None, 'laserpulse', 'am_tuning_curve') #No laser response

# exp0.add_site(1710, tetrodes=range(1, 9))
# exp0.add_session('15-33-43', None, 'noiseburst', 'am_tuning_curve') 
exp0.maxDepth = 1710

exp1 = celldatabase.Experiment(subject,
                               '2017-04-11',
                               brainarea='rightAC',
                               info=['DiD', 'facingLateral'])
experiments.append(exp1)

exp1.add_site(905, tetrodes=range(2, 9))
exp1.add_session('12-01-56', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-03-55', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-05-58', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-09-22', 'a', 'am', 'am_tuning_curve')
exp1.add_session('12-25-09', 'b', 'tc', 'am_tuning_curve')
exp1.add_session('12-57-00', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('12-58-13', None, 'lasertrain2', 'am_tuning_curve')

exp1.add_site(966, tetrodes=range(2, 9))
exp1.add_session('13-03-14', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-04-42', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-06-24', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-10-08', 'c', 'am', 'am_tuning_curve')
exp1.add_session('13-25-04', 'd', 'tc', 'am_tuning_curve')
exp1.add_session('13-57-17', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('13-58-33', None, 'lasertrain2', 'am_tuning_curve')

exp1.add_site(1016, tetrodes=range(2, 9))
exp1.add_session('14-06-03', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-07-45', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('14-08-57', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-11-53', 'e', 'am', 'am_tuning_curve')
exp1.add_session('14-28-22', 'f', 'tc', 'am_tuning_curve')
exp1.add_session('15-17-54', None, 'laserpulse2', 'am_tuning_curve')
exp1.add_session('15-19-21', None, 'lasertrain2', 'am_tuning_curve') #Went too long

exp1.add_site(1076, tetrodes=range(2, 9))
exp1.add_session('15-29-08', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-30-21', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-32-18', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-34-07', 'g', 'tc', 'am_tuning_curve')
exp1.add_session('16-06-06', 'h', 'am', 'am_tuning_curve')


# exp1.add_site(1136, tetrodes=range(2, 9))
# exp1.add_session('16-33-52', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('16-35-11', None, 'noiseburst', 'am_tuning_curve')
exp1.maxDepth = 1136


exp2 = celldatabase.Experiment(subject,
                               '2017-04-12',
                               brainarea='rightAC',
                               info=['lateralDiI', 'facingLateral'])
experiments.append(exp2)

exp2.add_site(937, tetrodes=[2, 4, 5, 6, 7, 8])
exp2.add_session('13-44-37', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-47-02', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-48-59', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-52-15', 'a', 'am', 'am_tuning_curve')
exp2.add_session('14-07-26', 'b', 'tc', 'am_tuning_curve')
exp2.add_session('14-42-20', None, 'laserpulse2', 'am_tuning_curve')
exp2.add_session('14-43-39', None, 'lasertrain2', 'am_tuning_curve')

exp2.add_site(1023, tetrodes=[2, 3, 4, 5, 6, 7, 8])
exp2.add_session('14-52-47', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-54-11', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-55-24', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-58-16', 'c', 'am', 'am_tuning_curve')
exp2.add_session('15-13-28', 'd', 'tc', 'am_tuning_curve')
exp2.maxDepth = 1023
