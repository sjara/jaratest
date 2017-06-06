from jaratoolbox import celldatabase

subject = 'adap047'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-06-02',
                               brainarea='rightAstr',
                               info=['middleDiI', 'facingPosterior'])
experiments.append(exp0)

#Mouse on the rig at 11:45, waiting 10 mins for brain to settle

# exp0.add_site(1539, tetrodes=range(1, 9))
# exp0.add_session('12-20-21', 'a', 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-23-34', 'b', 'tc', 'am_tuning_curve')

#1800-2000um no sound response, pretty quiet
exp0.add_site(2000, tetrodes=range(1, 9))
exp0.add_session('12-49-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-23-34', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2058, tetrodes=range(1, 9))
exp0.add_session('13-00-13', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-02-04', 'c', 'tc', 'am_tuning_curve')

exp0.add_site(2114, tetrodes=range(1, 9))
exp0.add_session('13-51-39', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-54-35', 'd', 'tc', 'am_tuning_curve')

exp0.add_site(2180, tetrodes=range(1, 9))
exp0.add_session('14-17-23', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-19-31', 'e', 'tc', 'am_tuning_curve')

exp0.add_site(2381, tetrodes=range(1, 9))
exp0.add_session('14-42-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-44-45', 'f', 'tc', 'am_tuning_curve')

exp0.add_site(2482, tetrodes=range(1, 9))
exp0.add_session('15-08-43', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-10-58', 'g', 'tc', 'am_tuning_curve')

exp0.add_site(2585, tetrodes=range(1, 9))
exp0.add_session('15-38-03', None, 'noiseburst', 'am_tuning_curve') #No more sound response, done for the day
# EXPERIMENT ABOVE COLLECTED WIth ONLY THE L SPEAKER ACTIVE


exp1 = celldatabase.Experiment(subject,
                               '2017-06-06',
                               brainarea='rightAstr',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp1)

#Mouse on the rig at 10:03, waiting 10 mins for brain to settle

exp1.add_site(1938, tetrodes=range(1, 9))
exp1.add_session('10-42-36', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('10-45-09', 'a', 'tc', 'am_tuning_curve')

# exp1.add_site(2157, tetrodes=range(1, 9))
# exp1.add_session('11-10-28', None, 'noiseburst', 'am_tuning_curve')
# # exp1.add_session('10-45-09', 'a', 'tc', 'am_tuning_curve')

exp1.add_site(2426, tetrodes=range(1, 9))
exp1.add_session('11-16-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-19-17', 'b', 'tc', 'am_tuning_curve')

exp1.add_site(2512, tetrodes=range(1, 9))
exp1.add_session('11-42-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-45-48', 'c', 'tc', 'am_tuning_curve')

exp1.add_site(2610, tetrodes=range(1, 9))
exp1.add_session('12-06-06', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-08-26', 'd', 'tc', 'am_tuning_curve')

exp1.add_site(2681, tetrodes=range(1, 9))
exp1.add_session('12-43-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-46-16', 'e', 'tc', 'am_tuning_curve')
