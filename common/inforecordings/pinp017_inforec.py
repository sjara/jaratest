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
exp0.maxDepth = 1338

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
exp1.maxDepth = 1604

exp2 = celldatabase.Experiment(subject,
                               '2017-03-24',
                               brainarea='rightAC',
                               info=['lateralDiI', 'facingLateral'])
experiments.append(exp2)

# exp2.add_site(1350, tetrodes=[1, 2, 4, 5, 6, 7, 8])
# exp2.add_session('14-27-32', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('14-28-49', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('14-30-01', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('14-42-04', 'a', 'minitc', 'am_tuning_curve')

exp2.add_site(1401, tetrodes=[1, 2, 4, 5, 6, 7, 8])
exp2.add_session('15-07-17', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-08-50', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-11-02', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-14-57', 'b', 'am', 'am_tuning_curve')
exp2.add_session('15-30-05', 'c', 'tc', 'am_tuning_curve')
exp2.add_session('16-01-57', None, 'laserpulse2', 'am_tuning_curve')
exp2.add_session('16-03-20', None, 'lasertrain2', 'am_tuning_curve')

# exp2.add_site(1470, tetrodes=[1, 2, 4, 5, 6, 7, 8])
# exp2.add_session('16-08-12', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('16-09-41', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('16-10-47', None, 'lasertrain', 'am_tuning_curve')

exp2.add_site(1525, tetrodes=[1, 2, 4, 5, 6, 7, 8])
exp2.add_session('16-15-34', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-17-08', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-19-13', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-22-04', 'd', 'am', 'am_tuning_curve')
exp2.add_session('16-38-06', 'e', 'tc', 'am_tuning_curve')
exp2.add_session('17-11-42', None, 'laserpulse2', 'am_tuning_curve')
exp2.add_session('17-13-27', None, 'lasertrain2', 'am_tuning_curve')
exp2.maxDepth = 1525

exp3 = celldatabase.Experiment(subject,
                               '2017-03-28',
                               brainarea='rightThal',
                               info=['medialDiI', 'facingLateral'])
experiments.append(exp3)

exp3.add_site(3074, tetrodes=range(1, 9))
exp3.add_session('13-00-11', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-02-00', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('13-03-19', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('13-07-20', 'a', 'am', 'am_tuning_curve')
exp3.add_session('13-24-53', 'b', 'tc', 'am_tuning_curve')
exp3.add_session('13-56-13', None, 'laserpulse2', 'am_tuning_curve')
exp3.add_session('13-57-45', None, 'lasertrain2', 'am_tuning_curve')

# exp3.add_site(3210, tetrodes=range(1, 9))
# exp3.add_session('14-18-25', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('14-19-34', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('14-20-46', None, 'lasertrain', 'am_tuning_curve')

exp3.add_site(3210, tetrodes=range(1, 9))
exp3.add_session('14-32-03', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-34-29', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('14-35-38', None, 'lasertrain', 'am_tuning_curve')
# exp3.add_session('14-39-05', 'c', 'am', 'am_tuning_curve')
exp3.add_session('14-55-03', 'd', 'tc', 'am_tuning_curve')
exp3.add_session('15-27-31', None, 'laserpulse2', 'am_tuning_curve')
exp3.add_session('15-28-39', None, 'lasertrain2', 'am_tuning_curve')
exp3.add_session('15-37-30', 'e', 'am', 'am_tuning_curve')

# exp3.add_site(3311, tetrodes=range(1, 9))
# exp3.add_session('16-19-05', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('16-20-22', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('16-22-35', None, 'lasertrain', 'am_tuning_curve')

# exp3.add_site(3349, tetrodes=range(1, 9))
# exp3.add_session('16-29-21', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('16-30-40', None, 'laserpulse', 'am_tuning_curve')
# exp3.add_session('16-32-28', None, 'laserpulse', 'am_tuning_curve')
#Nothing here, stopping for the day
exp3.maxDepth = 3349

exp4 = celldatabase.Experiment(subject,
                               '2017-03-30',
                               brainarea='rightThal',
                               info=['medialDiD', 'facingLateral'])
experiments.append(exp4)

#This site has long-latency laser responses that follow a fast train, but there is some strange jitter in the train that we should come back to. 
# exp4.add_site(3404, tetrodes=[8])
# exp4.add_session('14-01-20', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-03-03', None, 'laserpulse', 'am_tuning_curve')
# exp4.add_session('14-06-31', None, 'lasertrain', 'am_tuning_curve')
# exp4.add_session('14-12-43', None, 'lasertrain10Hz', 'am_tuning_curve')

#Nothing
# exp4.add_site(3455, tetrodes=range(1, 9))
# exp4.add_session('14-24-41', None, 'noiseburst', 'am_tuning_curve')

# exp4.add_site(3512, tetrodes=range(1, 9))
# exp4.add_session('14-26-57', None, 'noiseburst', 'am_tuning_curve')

# exp4.add_site(3567, tetrodes=range(1, 9))
# exp4.add_session('14-28-40', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-30-04', None, 'laserpulse', 'am_tuning_curve')
# #weirdo long latency laser responses

# exp4.add_site(3621, tetrodes=range(1, 9))
# exp4.add_session('14-32-22', None, 'noiseburst', 'am_tuning_curve')

# exp4.add_site(3703, tetrodes=range(1, 9))
# exp4.add_session('14-33-49', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-35-19', None, 'laserpulse', 'am_tuning_curve')
# # SUPER strange laser response. We need to find out where we are later when we do this histo. 

# exp4.add_site(3755, tetrodes=range(1, 9))
# exp4.add_session('14-44-22', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-45-56', None, 'laserpulse', 'am_tuning_curve')
#Even longer latency to laser pulse response
exp4.maxDepth = 3755

exp5 = celldatabase.Experiment(subject,
                               '2017-03-31',
                               brainarea='rightThal',
                               info=['lateralDiI', 'facingLateral'])
experiments.append(exp5)
# exp5.add_site(3261, tetrodes=range(1, 9))
# exp5.add_session('14-47-13', None, 'noiseburst', 'am_tuning_curve')

# exp5.add_site(3360, tetrodes=range(1, 9))
# exp5.add_session('14-51-03', None, 'noiseburst', 'am_tuning_curve')

# exp5.add_site(3560, tetrodes=range(1, 9))
# exp5.add_session('14-55-03', None, 'noiseburst', 'am_tuning_curve')

# exp5.add_site(3783, tetrodes=range(1, 9))
# exp5.add_session('15-00-13', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('15-02-02', None, 'noiseburst', 'am_tuning_curve') #long latency laser responses
exp5.maxDepth = 3783
