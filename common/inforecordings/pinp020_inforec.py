#coding=utf-8

from jaratoolbox import celldatabase

subject = 'pinp020'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# exp0.add_site(994, tetrodes=range(1, 9))
# exp0.add_session('10-32-12', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(1581, tetrodes=range(1, 9))
# exp0.add_session('10-37-18', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2100, tetrodes=range(1, 9))
# exp0.add_session('10-41-12', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2607, tetrodes=range(1, 9))
# exp0.add_session('10-44-48', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2702, tetrodes=range(1, 9))
exp0.add_session('10-57-28', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-01-52', 'a', 'am', 'am_tuning_curve')
exp0.add_session('11-19-15', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2802, tetrodes=range(1, 9))
exp0.add_session('12-06-40', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-09-17', 'c', 'am', 'am_tuning_curve')
exp0.add_session('12-24-37', 'd', 'tc', 'am_tuning_curve')

exp0.maxDepth = 2802

exp1 = celldatabase.Experiment(subject,
                               '2017-05-10',
                               brainarea='rightAstr',
                               info=['DiD', 'facingPosterior'])
experiments.append(exp1)

# exp1.add_site(2580, tetrodes=range(1, 9))
exp1.add_site(2580, tetrodes=[1, 2, 3, 4, 5, 6])
# exp1.add_session('18-31-39', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('18-52-26', 'a', 'am', 'am_tuning_curve')
exp1.add_session('19-08-46', 'b', 'tc', 'am_tuning_curve')
exp1.add_session('19-42-17', 'c', 'am', 'am_tuning_curve') #Recording am again, first one looked strange
exp1.add_session('19-58-05', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(2682, tetrodes=range(1, 9))
exp1.add_site(2682, tetrodes=[1, 2, 3, 4, 5, 6])
exp1.add_session('20-20-55', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('20-23-54', 'd', 'am', 'am_tuning_curve')
exp1.add_session('20-40-14', 'e', 'tc', 'am_tuning_curve')

# exp1.add_site(2784, tetrodes=range(1, 9))
exp1.add_site(2784, tetrodes=[1, 2, 3, 4, 5, 6])
exp1.add_session('21-23-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('21-25-23', 'f', 'am', 'am_tuning_curve')

exp1.maxDepth = 2784

exp2 = celldatabase.Experiment(subject,
                               '2017-05-11',
                               brainarea='rightAstr',
                               info=['PosteriorDiI', 'facingPosterior'])
experiments.append(exp2)

# exp2.add_site(2001, tetrodes=range(1, 9))
# exp2.add_session('13-06-06', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2100, tetrodes=range(1, 9))
# exp2.add_session('13-10-18', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2153, tetrodes=range(1, 9))
# exp2.add_session('13-33-26', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2303, tetrodes=range(1, 9))
# exp2.add_session('13-35-33', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2731, tetrodes=range(1, 9))
# exp2.add_session('13-47-34', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2766, tetrodes=range(1, 9))
# exp2.add_session('13-51-48', None, 'noiseburst', 'am_tuning_curve')

# Went to 3250um, no more units, finishing the experiment
exp2.maxDepth = 3250

# exp3 = celldatabase.Experiment(subject,
#                                '2017-05-12',
#                                brainarea='leftAstr',
#                                info=['AnteriorDiI', 'facingPosterior'])
# experiments.append(exp3)

# exp3.add_site(1538, tetrodes=range(1, 9))
# exp3.add_session('14-48-40', None, 'noiseburst', 'am_tuning_curve')

# exp3.add_site(2100, tetrodes=range(1, 9))
# exp3.add_session('14-55-26', None, 'noiseburst', 'am_tuning_curve')

# exp3.add_site(2301, tetrodes=range(1, 9))
# exp3.add_session('14-59-41', None, 'noiseburst', 'am_tuning_curve')

# exp3.add_site(2430, tetrodes=range(1, 9))
# exp3.add_session('15-25-15', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('15-27-53', 'a', 'am', 'am_tuning_curve')
# exp3.add_session('15-46-05', 'b', 'tc', 'am_tuning_curve')

# exp3.add_site(2601, tetrodes=range(1, 9))
# exp3.add_session('16-32-41', None, 'noiseburst', 'am_tuning_curve')

# exp3.add_site(2705, tetrodes=range(1, 9))
# exp3.add_session('16-35-21', None, 'noiseburst', 'am_tuning_curve')

#Going back up...

# exp3.add_site(2458, tetrodes=range(1, 9))
# exp3.add_session('16-39-18', None, 'noiseburst', 'am_tuning_curve')
