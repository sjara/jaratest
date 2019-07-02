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


