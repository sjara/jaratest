from jaratoolbox import celldatabase

subject = 'pinp025'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-09-01',
                               brainarea='rightAstr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# Probe at 1583, waiting 10 mins

##### REMOVING 5, 6, 7, and 8 because they are outside the str

# exp0.add_site(2012, tetrodes=range(1, 9)).remove_tetrodes([1, 5, 6, 7, 8])
# # exp0.add_session('16-42-05', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('16-45-07', 'a', 'tc', 'am_tuning_curve')
# exp0.add_session('17-18-45', 'b', 'am', 'am_tuning_curve')
# exp0.add_session('17-34-28', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2111, tetrodes=range(1, 9)).remove_tetrodes([1, 5, 6, 7, 8])
# exp0.add_session('17-41-12', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('17-43-34', 'c', 'tc', 'am_tuning_curve')
# exp0.add_session('18-17-49', 'd', 'am', 'am_tuning_curve')

# exp0.add_site(2229, tetrodes=range(1, 9)).remove_tetrodes([1, 5, 6, 7, 8])
# exp0.add_session('18-51-47', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('18-54-55','e', 'tc', 'am_tuning_curve')
# exp0.add_session('19-30-23', 'f', 'am', 'am_tuning_curve')
# Done for the day
exp0.maxDepth = 2229



exp1 = celldatabase.Experiment(subject,
                               '2017-09-04',
                               brainarea='rightAstr',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp1)

#Probe in at 10:36am
#Probe at 1909, waiting 10 mins

# exp1.add_site(1990, tetrodes=range(1, 9)).remove_tetrodes([1, 3, 4, 5, 6, 7, 8])
exp1.add_site(1990, tetrodes=[2])
exp1.add_session('11-07-18', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-11-46', 'a', 'tc', 'am_tuning_curve')
exp1.add_session('11-45-00', 'b', 'am', 'am_tuning_curve')

# exp1.add_site(2051, tetrodes=range(1, 9)).remove_tetrodes([1, 3, 4, 5, 6, 7, 8])
exp1.add_site(2051, tetrodes=[2])
exp1.add_session('12-09-49', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-12-35', 'c', 'tc', 'am_tuning_curve')
exp1.add_session('12-58-30', 'd', 'am', 'am_tuning_curve')

# exp1.add_site(2163, tetrodes=range(1, 9)).remove_tetrodes([1, 3, 4, 5, 6, 7, 8])
exp1.add_site(2163, tetrodes=[2])
exp1.add_session('13-24-25', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-29-30', 'e', 'tc', 'am_tuning_curve')
exp1.add_session('14-01-52', 'f', 'am', 'am_tuning_curve')

# exp1.add_site(2271, tetrodes=range(1, 9)).remove_tetrodes([1, 3, 4, 5, 6, 7, 8])
exp1.add_site(2271, tetrodes=[2])
exp1.add_session('14-22-48', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-25-44', 'g', 'tc', 'am_tuning_curve')
exp1.add_session('14-58-44', 'h', 'am', 'am_tuning_curve')

# exp1.add_site(2406, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('15-25-59', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('15-29-10', 'i', 'tc', 'am_tuning_curve')
# exp1.add_session('16-02-16', 'j', 'am', 'am_tuning_curve')

# exp1.add_site(2598, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('16-31-14', None, 'noiseburst', 'am_tuning_curve')
# # exp1.add_session('15-29-10', 'i', 'tc', 'am_tuning_curve')
# # exp1.add_session('16-02-16', 'j', 'am', 'am_tuning_curve')
exp1.maxDepth = 2598

# exp2 = celldatabase.Experiment(subject,
#                                '2017-09-05',
#                                brainarea='rightAstr',
#                                info=['posteriorDiI', 'facingPosterior'])
# experiments.append(exp2)

# #Probe in at 10:53am
# #Probe at 2000, waiting 10 mins

# ###### This recording missed the striatum entirely

# exp2.add_site(2000, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
# exp2.add_session('11-21-50', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('11-24-39', 'a', 'tc', 'am_tuning_curve')
# exp2.add_session('11-58-01', 'b', 'am', 'am_tuning_curve')

# exp2.add_site(2112, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
# exp2.add_session('12-23-22', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('12-26-50', 'c', 'tc', 'am_tuning_curve')
# exp2.add_session('13-00-29', 'd', 'am', 'am_tuning_curve')

# exp2.add_site(2226, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
# exp2.add_session('13-28-06', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('13-33-23', 'e', 'tc', 'am_tuning_curve')
# exp2.add_session('14-06-41', 'f', 'am', 'am_tuning_curve')

# exp2.add_site(2352, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
# exp2.add_session('14-34-04', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('14-37-34', 'g', 'tc', 'am_tuning_curve')
# exp2.add_session('15-14-10', 'h', 'am', 'am_tuning_curve')

# exp2.add_site(2464, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3])
# exp2.add_session('15-56-18', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('16-01-11', 'i', 'tc', 'am_tuning_curve')
# exp2.add_session('16-35-04', 'j', 'am', 'am_tuning_curve')
