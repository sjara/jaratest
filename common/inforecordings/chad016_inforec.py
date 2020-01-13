from jaratoolbox import celldatabase

subject = 'chad016'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-08-29', 'left AC', info=['farLateral' 'facingLeft' 'soundRight'])
experiments.append(exp0)
# Using probe D65D

exp0.add_site(900, tetrodes=[1,2,4,7,8])

exp0.add_session('13-36-25', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 3 (Tetrode 6, channel 1)

exp0.add_session('13-48-05', 'b', 'tc', 'am_tuning_curve')
# Reference set to 3 (Tetrode 6, channel 1)

exp0.add_session('14-05-54', 'c', 'ascending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 2,4,7,8.

exp0.add_session('14-15-45', 'd', 'descending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 2,4,7,8.git commit chad011_inforec.py -m "Updated inforec"

exp0.add_site(975, tetrodes=[2,3,4,5,6,7,8])

exp0.add_session('15-05-21', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 18 (Tetrode 1, channel 1)


exp0.add_site(1051, tetrodes=[2,4,6,7,8])

exp0.add_session('15-16-43', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'f'
# Reference set to 18 (Tetrode 1, channel 1)

exp0.add_session('15-21-27', 'g', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

exp0.add_session('15-38-03', 'h', 'ascending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 2,4,6,7,8.

exp0.add_session('15-48-40', 'i', 'descending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 2,4,6,7,8.

exp0.add_site(1155, tetrodes=[2,4,6,7,8])

exp0.add_session('16-16-50', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'j'
# Reference set to 25 (Tetrode 3, channel 1)

exp0.add_session('16-23-46', 'k', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp0.add_session('16-39-49', 'l', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 2,6,8.

exp0.add_session('16-49-09', 'm', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 2,6,8.

exp0.maxDepth = 1155



exp1 = celldatabase.Experiment(subject, '2019-08-30', 'left AC', info=['farLateral' 'facingLeft' 'soundRight'])
experiments.append(exp1)
# Using probe D65D

exp1.add_site(1030, tetrodes=[1,2,3,4,5,6,7,8])

exp1.add_session('16-27-07', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_session('16-32-32', 'b', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_session('16-49-30', 'c', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 1,2,3,4,5,6,7,8.

exp1.add_session('16-59-06', 'd', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 1,2,3,4,5,6,7,8.


exp1.add_site(1115, tetrodes=[1,2,3,4,5,6,7,8])

exp1.add_session('17-19-30', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_session('17-25-48', 'f', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_session('17-43-47', 'g', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2,3,4,5,6,7,8.

exp1.add_session('18-06-09', 'h', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2,3,4,5,6,7,8.

exp1.maxDepth = 1155



exp2 = celldatabase.Experiment(subject, '2019-09-01', 'left AC', info=['farLateral' 'facingLeft' 'soundRight'])
experiments.append(exp2)
# Using probe D65D

exp2.add_site(1202, tetrodes=[1,2,3,4,5,6,7,8])

exp2.add_session('15-32-58', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_site(1275, tetrodes=[1,2,3,4,5,6,7,8])

exp2.add_session('15-46-34', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('15-51-17', 'c', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('16-07-55', 'd', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 4,6.

exp2.add_session('16-18-48', 'e', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 4,6.


exp2.maxDepth = 1275


exp3 = celldatabase.Experiment(subject, '2019-09-04', 'left AC', info=['midLateral' 'facingLeft' 'soundRight'])
experiments.append(exp3)
# Using probe 41DD

exp3.add_site(900, tetrodes=[1,2,3,4,5,6,7,8])

exp3.add_session('14-25-42', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 25 (Tetrode 3, channel 1)

exp3.add_session('14-32-01', 'b', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp3.add_session('14-50-55', 'c', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)

exp3.add_session('15-01-20', 'd', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)


exp3.add_site(975, tetrodes=[1,2,3,4,5,6,7,8])


exp3.add_session('15-21-19', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('15-26-31', 'f', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('15-43-58', 'g', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('15-53-12', 'h', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)


exp3.add_site(1038, tetrodes=[1,2,3,4,5,6,7,8])

exp3.add_session('16-15-40', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'i'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('16-20-14', 'j', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('16-37-38', 'k', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('16-47-21', 'l', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)


exp3.maxDepth = 1038









