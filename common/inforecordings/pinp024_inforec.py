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
exp1.add_session('12-25-13', 'e', 'am', 'am_tuning_curve')

exp1.add_site(2265, tetrodes=range(1, 9))
exp1.add_session('13-48-16', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-50-42', 'f', 'tc', 'am_tuning_curve')
exp1.add_session('14-23-44', 'g', 'am', 'am_tuning_curve')

exp2 = celldatabase.Experiment(subject,
                               '2017-08-17',
                               brainarea='rightAstr',
                               info=['anteriorDiO', 'facingPosterior'])
experiments.append(exp2)

#Mouse on the rig at 0955hrs, waiting 10 mins for brain to settle
#Tetrodes at 1913um

exp2.add_site(2010, tetrodes=range(1, 9))
exp2.add_session('10-56-57', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('10-59-16', 'a', 'tc', 'am_tuning_curve')
exp2.add_session('11-37-58', 'b', 'am', 'am_tuning_curve')

exp2.add_site(2135, tetrodes=range(1, 9))
exp2.add_session('12-01-43', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-04-19', 'c', 'tc', 'am_tuning_curve')
exp2.add_session('12-38-17', 'd', 'am', 'am_tuning_curve')

exp2.add_site(2265, tetrodes=range(1, 9))
exp2.add_session('13-01-39', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-03-54', 'e', 'tc', 'am_tuning_curve')
exp2.add_session('13-36-39', 'f', 'am', 'am_tuning_curve')

exp2.add_site(2372, tetrodes=range(1, 9))
exp2.add_session('14-03-12', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-42-35', 'g', 'tc', 'am_tuning_curve')
exp2.add_session('15-16-02', 'h', 'am', 'am_tuning_curve')

exp2.add_site(2508, tetrodes=range(1, 9))
exp2.add_session('15-57-56', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-03-45', 'i', 'tc', 'am_tuning_curve')
exp2.add_session('16-36-11', 'j', 'am', 'am_tuning_curve')

exp3 = celldatabase.Experiment(subject,
                               '2017-08-22',
                               brainarea='rightAstr',
                               info=['posteriorDiI', 'facingPosterior'])
experiments.append(exp3)

#Mouse on the rig at 1100hrs, waiting 30 mins for brain to settle

exp3.add_site(2003, tetrodes=range(1, 9)).remove_tetrodes([5])
exp3.add_session('11-27-27', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('11-30-49', 'a', 'tc', 'am_tuning_curve')
exp3.add_session('12-06-05', 'b', 'am', 'am_tuning_curve')

exp3.add_site(2136, tetrodes=range(1, 9))
exp3.add_session('12-54-42', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-59-50', 'c', 'tc', 'am_tuning_curve')
exp3.add_session('13-33-22', 'd', 'am', 'am_tuning_curve')

exp3.add_site(2276, tetrodes=range(1, 9))
exp3.add_session('13-57-57', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-01-44', 'e', 'tc', 'am_tuning_curve')
exp3.add_session('14-34-27', 'f', 'am', 'am_tuning_curve')

exp3.add_site(2407, tetrodes=range(1, 9))
exp3.add_session('15-00-31', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-02-54', 'g', 'am', 'am_tuning_curve')
# exp3.add_session('14-34-27', 'f', 'am', 'am_tuning_curve')

exp4 = celldatabase.Experiment(subject,
                               '2017-08-23',
                               brainarea='rightAstr',
                               info=['posteriorDiD', 'facingPosterior'])
experiments.append(exp4)

#Mouse on the rig at 1130hrs, waiting 15 mins for brain to settle

exp4.add_site(2011, tetrodes=[2, 5, 6, 7, 8])
exp4.add_session('11-44-19', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('11-50-05', 'a', 'tc', 'am_tuning_curve')
exp4.add_session('12-23-02', 'b', 'am', 'am_tuning_curve')

exp4.add_site(2158, tetrodes=[2, 4, 5, 6, 7, 8])
exp4.add_session('13-04-05', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-09-05', 'c', 'tc', 'am_tuning_curve')
exp4.add_session('13-43-26', 'd', 'am', 'am_tuning_curve')

exp4.add_site(2308, tetrodes=[4, 5, 6, 7, 8])
exp4.add_session('14-14-41', None, 'noiseburst', 'am_tuning_curve') #2000 trials...
exp4.add_session('14-52-37', 'e', 'tc', 'am_tuning_curve')
exp4.add_session('15-25-09', 'f', 'am', 'am_tuning_curve')

exp4.add_site(2638, tetrodes=[6, 7, 8])
exp4.add_session('16-10-51', None, 'noiseburst', 'am_tuning_curve') #2000 trials...
exp4.add_session('16-13-59', 'g', 'tc', 'am_tuning_curve')
exp4.add_session('16-47-37', 'h', 'am', 'am_tuning_curve')
