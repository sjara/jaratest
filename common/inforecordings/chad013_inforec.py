from jaratoolbox import celldatabase

subject = 'chad013' 
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-07-01', 'right AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)
# Using probe M680

# exp0.add_site(1100, tetrodes=[1,2,3,4,5,6,8])
# exp0.add_session('11-27-44', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 12 (Tetrode 7, channel 1)
# Raster plot does not indicate presence of sound responsive cell.

# exp0.add_session('11-57-57', 'b', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)
# 3 intensities

exp0.add_site(1125, tetrodes=[1,2,3,4,5,6,8])
exp0.add_session('13-46-10', None, 'noiseburst', 'am_tuning_curve')
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
# Using probe M680

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


exp2 = celldatabase.Experiment(subject, '2019-07-05', 'right AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp2)
# Using probe M680

exp2.add_site(1100, tetrodes=[3,4,5,6,7,8])
exp2.add_session('15-02-21', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# Indication of sound responsive cells on tetrodes 4,6,7,8.

exp2.add_session('15-08-13', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities
# Indication of frequency preference on tetrode 4.

exp2.add_session('16-40-26', 'c', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp2.add_session('16-44-43', 'd', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp2.add_site(1175, tetrodes=[3,4,5,6,7,8])
exp2.add_session('17-03-12', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Indication of sound responsive cells on tetrodes 4,6.

exp2.add_session('17-11-29', 'f', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities
# Indication of sound responsive cells on tetrodes 4,6.

exp2.add_session('17-57-58', 'g', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp2.add_session('18-03-45', 'h', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp2.maxDepth = 1400


exp3 = celldatabase.Experiment(subject, '2019-07-11', 'right AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp3)
#Using probe: C39C

exp3.add_site(977, tetrodes=[2,8])
exp3.add_session('15-50-47', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# Indication of sound responsive cell on tetrodes 2.

exp3.add_session('16-06-10', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp2.maxDepth = 977

exp4 = celldatabase.Experiment(subject, '2019-07-14', 'right AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp4)
#Using probe: C39C

# exp4.add_site(1252, tetrodes=[2,8])
# exp4.add_session('15-27-44', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# No indication of good sound responsive cells

exp4.add_site(1328, tetrodes=[2,4,6,7])
exp4.add_session('15-33-41', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)
# Possible sound response on tetrode 2.

exp4.add_session('15-47-05', 'c', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp4.add_session('16-15-40', 'd', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Possible indication of increased response to oddball on tetrode 8, but there's also noise.

exp4.add_session('16-26-45', 'e', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp4.add_site(1484, tetrodes=[2,3,4,6,7,8])
exp4.add_session('16-56-35', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'f'
# Reference set to 18 (Tetrode 1, channel 1)
# Indication of sound responses on tetrodes 5,7,8.

exp4.add_session('17-02-36', 'g', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp4.add_session('17-27-33', 'h', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# No indication of increased response to oddball. ):

exp2.maxDepth = 1484


exp5 = celldatabase.Experiment(subject, '2019-07-15', 'right AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp5)
#Using probe: C39C

exp5.add_site(1043, tetrodes=[2,8])
exp5.add_session('11-07-14', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# Possible indication weak sound response on tetrode 8.

exp5.add_site(1100, tetrodes=[2,6,8])
exp5.add_session('11-15-45', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)


exp5.add_site(1132, tetrodes=[2,6,8])
exp5.add_session('11-21-34', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)


exp5.add_site(1200, tetrodes=[2,5,6])
exp5.add_session('11-53-58', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'd'
# Reference set to 18 (Tetrode 1, channel 1)

exp5.maxDepth = 1200


exp6 = celldatabase.Experiment(subject, '2019-07-15', 'right AC', info=['farLateralDiD', 'facingAnterior', 'soundLeft'])
experiments.append(exp6)
#Using probe: C39C

exp6.add_site(873, tetrodes=[2,3,4,5,6,7,8])
exp6.add_session('14-52-37', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'

exp6.add_session('15-10-35', 'f', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp6.add_session('15-41-30', 'g', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp6.add_session('15-48-32', 'h', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp6.add_session('15-54-16', 'i', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp6.add_session('17-05-13', 'j', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 1 intensity

exp6.add_session('17-13-36', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'k'

exp5.maxDepth = 1000


exp7 = celldatabase.Experiment(subject, '2019-07-16', 'right AC', info=['farLateralDiD', 'facingAnterior', 'soundLeft'])
experiments.append(exp7)
#Using probe: C39C

exp7.add_site(934, tetrodes=[3,4,6,7,8])
exp7.add_session('15-27-00', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# Indication of sound responses on tetrodes 2,4,8.

exp7.add_session('15-31-25', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities

exp7.add_site(1006, tetrodes=[3,4,6,7,8])
exp7.add_session('16-17-30', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)

exp7.add_session('16-21-49', 'd', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 3 intensities
# Moderate frequency tuning on tetrodes 6,7; strong frequency tuning on tetrode 8.

exp7.add_session('16-45-47', 'e', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Strong increased response to oddball.

exp7.add_session('16-51-38', 'f', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp7.add_session('17-01-45', 'g', 'many-standards', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp7.add_session('17-09-04', 'h', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp7.maxDepth = 1006





