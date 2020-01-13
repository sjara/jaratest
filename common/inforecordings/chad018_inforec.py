from jaratoolbox import celldatabase

subject = 'chad018'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-09-09', 'left AC', info=['Lateral' 'facingLeft' 'soundRight'])
experiments.append(exp0)
# Using probe C39C

exp0.add_site(1150, tetrodes=[1,2,3,4,5,6,7,8])

exp0.add_session('16-28-13', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp0.add_session('16-34-19', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

exp0.add_session('16-51-31', 'c', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp0.add_session('17-10-30', 'd', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp0.maxDepth = 1150


exp1 = celldatabase.Experiment(subject, '2019-09-10', 'left AC', info=['Lateral' 'facingLeft' 'soundRight'])
experiments.append(exp1)
# Using probe C39C

exp1.add_site(1050, tetrodes=[1,2,3,4,5,6,7,8])

exp1.add_session('15-40-52', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)


exp1.add_site(1127, tetrodes=[1,2,3,4,5,6,7,8])

exp1.add_session('16-00-24', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_site(1274, tetrodes=[1,2,3,4,5,6,7,8])

exp1.add_session('16-24-00', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)


exp1 = celldatabase.Experiment(subject, '2019-09-10', 'left AC', info=['Medial' 'facingLeft' 'soundRight'])
experiments.append(exp1)
# Using probe C39C





















