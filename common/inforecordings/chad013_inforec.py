from jaratoolbox import celldatabase

subject = 'chad013' 
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-07-01', 'right AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

# exp0.add_site(1100, tetrodes=[1,2,3,4,5,6,8])
# exp0.add_session('11-27-44', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 12 (Tetrode 7, channel 1)
# Raster plot does not indicate presence of sound responsive cell.

# exp0.add_session('11-57-57', 'b', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)
# 3 intensities

exp0.add_site(1125, tetrodes=[1,2,3,4,5,6,8])
# exp0.add_session('13-46-10', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 12 (Tetrode 7, channel 1)
# Raster plot does not indicate presence of sound responsive cell.

exp0.add_session('13-57-37', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'd'
# Reference set to 3 (Tetrode 6, channel 1)

exp0.add_session('14-05-22', 'e', 'tc', 'am_tuning_curve')
# Reference set to 3 (Tetrode 6, channel 1)
# 1 intensity

exp0.add_session('14-28-44', 'f', 'standard', 'oddball_sequence')

exp0.add_session('14-42-01', 'g', 'oddball', 'oddball_sequence')
# Indication of increased firing rate in response to oddball.

exp0.add_session('15-10-03', 'h', 'oddball', 'oddball_sequence')

exp0.add_session('15-16-10', 'i', 'standard', 'oddball_sequence')

exp0.add_session('15-40-48', 'j', 'oddball', 'oddball_sequence')

exp0.maxDepth = 1125

exp1 = celldatabase.Experiment(subject, '2019-07-02', 'right AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp1)

exp1.add_site(1100, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('16-06-43', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_site(1150, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('16-39-32', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)
# Indication of potential sound responses on multiple tetrodes.

exp1.add_session('17-06-57', 'c', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp1.add_session('17-41-45', 'd', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_session('17-47-04', 'e', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_site(1225, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('18-18-11', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'f'
# Reference set to 25 (Tetrode 3, channel 1)
# Indication of potential sound responses on multiple tetrodes.

exp1.add_session('18-25-13', 'g', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)
# 3 intensities
# Indication of frequency preference on tetrodes 2 and 4.

exp1.add_session('18-49-50', 'h', 'oddball', 'oddball_sequence')
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_session('18-55-50', 'i', 'standard', 'oddball_sequence')
# Reference set to 25 (Tetrode 3, channel 1)

exp1.add_site(1300, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('19-28-10', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'j'
# Reference set to 12 (Tetrode 7, channel 1)
# Indication of potential sound responses on multiple tetrodes.

exp1.add_session('19-35-46', 'k', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)
# 3 intensities
# Indication of frequency preference on tetrodes 1,2,5,6,8.

exp1.add_session('20-03-16', 'l', 'oddball', 'oddball_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Requires analysis of signals from tetrodes 1,2,5,6,8.
# Possible indication of increased firing rate in response to oddball.

exp1.add_session('20-13-25', 'm', 'standard', 'oddball_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Requires analysis of signals from tetrodes 1,2,5,6,8.

exp1.maxDepth = 1300









