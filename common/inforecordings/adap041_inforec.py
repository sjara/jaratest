from jaratoolbox import celldatabase

subject = 'adap041'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-07-07',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

#Mouse on the rig at 1339hrs, waiting 10 mins for brain to settle
#Tetrodes at 2002um - had to remove some membrane from brain surface

exp0.add_site(2002, tetrodes=range(1, 9))
exp0.add_session('13-51-08', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-53-42', 'a', 'tc', 'am_tuning_curve')

exp0.add_site(2110, tetrodes=range(1, 9))
exp0.add_session('14-22-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-24-07', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2200, tetrodes=range(1, 9))
exp0.add_session('14-52-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-54-58', 'c', 'tc', 'am_tuning_curve')

exp0.add_site(2309, tetrodes=range(1, 9))
exp0.add_session('15-18-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-27-19', 'd', 'tc', 'am_tuning_curve')

exp0.add_site(2411, tetrodes=range(1, 9))
exp0.add_session('15-52-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-56-28', 'e', 'tc', 'am_tuning_curve')

exp0.add_site(2518, tetrodes=range(1, 9))
exp0.add_session('16-23-27', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-26-18', 'f', 'tc', 'am_tuning_curve')

exp0.add_site(2602, tetrodes=range(1, 9))
exp0.add_session('17-03-57', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-05-58', 'g', 'tc', 'am_tuning_curve')

exp0.add_site(2725, tetrodes=range(1, 9))
exp0.add_session('17-39-49', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-41-57', 'h', 'tc', 'am_tuning_curve')

exp0.add_site(2824, tetrodes=range(1, 9))
exp0.add_session('18-04-36', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-07-13', 'i', 'tc', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject,
                               '2017-07-08',
                               brainarea='leftAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp1)

#Mouse on the rig at 2012hrs, waiting 10 mins for brain to settle
#Tetrodes at 1969um - had to remove some membrane from brain surface

exp1.add_site(2055, tetrodes=range(1, 9))
exp1.add_session('20-33-05', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('20-37-11', 'a', 'tc', 'am_tuning_curve')

exp1.add_site(2153, tetrodes=range(1, 9))
exp1.add_session('21-00-12', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('21-02-33', 'b', 'tc', 'am_tuning_curve')

exp1.add_site(2253, tetrodes=range(1, 9))
exp1.add_session('21-36-58', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('21-40-02', 'c', 'tc', 'am_tuning_curve')

exp1.add_site(2403, tetrodes=range(1, 9))
exp1.add_session('22-14-22', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('22-18-02', 'd', 'tc', 'am_tuning_curve')

exp1.add_site(2550, tetrodes=range(1, 9))
exp1.add_session('22-41-03', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('22-43-15', 'e', 'tc', 'am_tuning_curve')

# exp1.add_site(2656, tetrodes=range(1, 9))
# exp1.add_session('23-08-07', None, 'noiseburst', 'am_tuning_curve')
#No sound response here

exp1.add_site(2703, tetrodes=range(1, 9))
exp1.add_session('23-18-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('23-21-00', 'f', 'tc', 'am_tuning_curve')

site = exp1.add_site(2858, tetrodes=range(1, 9))
exp1.add_session('23-59-01', None, 'noiseburst', 'am_tuning_curve')
site.date = '2017-07-09'
exp1.add_session('00-01-41', 'a', 'tc', 'am_tuning_curve')

# site = exp1.add_site(2979, tetrodes=range(1, 9))
# site.date = '2017-07-09'
# exp1.add_session('00-32-27', None, 'noiseburst', 'am_tuning_curve')
#Nothing here, removing for the day
