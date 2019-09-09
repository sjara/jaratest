from jaratoolbox import celldatabase

subject = 'chad013'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-07-01', 'right AC', info=['midMedial' 'facingLeft' 'soundLeft'])
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

exp1 = celldatabase.Experiment(subject, '2019-07-02', 'right AC', info=['midMedial' 'facingLeft' 'soundLeft'])
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


exp2 = celldatabase.Experiment(subject, '2019-07-05', 'right AC', info=['midLateral' 'facingLeft' 'soundLeft'])
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


exp3 = celldatabase.Experiment(subject, '2019-07-11', 'right AC', info=['midLateral' 'facingLeft' 'soundLeft'])
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

exp3.maxDepth = 977

exp4 = celldatabase.Experiment(subject, '2019-07-14', 'right AC', info=['midLateral' 'facingLeft' 'soundLeft'])
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

exp4.maxDepth = 1484


exp5 = celldatabase.Experiment(subject, '2019-07-15', 'right AC', info=['midLateral' 'facingLeft' 'soundLeft'])
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


exp6 = celldatabase.Experiment(subject, '2019-07-15', 'right AC', info=['farLateral', 'facingLeft', 'soundLeft'])
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

exp6.maxDepth = 1000


exp7 = celldatabase.Experiment(subject, '2019-07-16', 'right AC', info=['farLateral', 'facingLeft', 'soundLeft'])
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



exp8 = celldatabase.Experiment(subject, '2019-08-12', 'left AC', info=['midMedial', 'facingLeft', 'soundRight'])
experiments.append(exp8)
#Using probe: C39C

exp8.add_site(1319, tetrodes=[1,2,3,4,5,6,7,8])
exp8.add_session('17-10-18', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp8.add_session('17-16-45', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)

exp8.add_site(1320, tetrodes=[2,3,4,5,6,7,8])
exp8.add_session('17-29-56', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)


exp8.add_session('17-38-44', 'd', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 2 intensities: 60, 70dB
# Frequency preference of tetrode 2.

exp8.add_session('18-01-45', 'e', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrodes 2.

exp8.add_session('18-10-51', 'f', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrodes 2.


exp8.maxDepth = 1320



exp9 = celldatabase.Experiment(subject, '2019-08-13', 'left AC', info=['midLateral', 'facingLeft', 'soundRight'])
experiments.append(exp9)
#Using probe: D65D


exp9.add_site(1100, tetrodes=[2,5,6,7,8])
exp9.add_session('18-56-36', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp9.add_session('19-01-47', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 2 intensities: 60, 70dB

exp9.add_session('19-20-54', 'c', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrodes 2.

exp9.add_session('19-28-22', 'd', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrodes 2.

exp9.maxDepth = 1100




exp10 = celldatabase.Experiment(subject, '2019-08-15', 'left AC', info=['midLateral', 'facingLeft', 'soundRight'])
experiments.append(exp10)
#Using probe: C39A

exp10.add_site(1351, tetrodes=[1,2,3,4,6,7,8])

exp10.add_session('13-20-20', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 14 (Tetrode 5, channel 1)

exp10.add_session('13-27-06', 'b', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)
# 2 intensities: 60, 70dB

exp10.add_session('13-44-35', 'c', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,4.
# 12,000 trials / 40 presentations of oddball

exp10.add_session('13-52-01', 'd', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,4.
# 12,000 trials / 40 presentations of oddball

exp10.add_session('14-06-14', 'e', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,4.
# 18,000 trials / 60 presentations of oddball


exp10.add_session('14-15-59', 'f', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,4.
# 18,000 trials / 60 presentations of oddball

exp10.add_site(1430, tetrodes=[1,2,4,5,6,7,8])

exp10.add_session('14-44-57', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'g'
# Reference set to 25 (Tetrode 3, channel 1)

exp10.add_session('14-49-09', 'h', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp10.add_session('15-06-13', 'i', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 4.

exp10.add_session('15-17-06', 'j', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 4.

exp10.add_site(1464, tetrodes=[1,2,3,4,5,6,7,8])

exp10.add_session('15-39-16', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'k'
# Reference set to 25 (Tetrode 3, channel 1)

exp10.add_site(1667, tetrodes=[1,2,4,5,6,7,8])

exp10.add_session('16-01-15', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'l'
# Reference set to 25 (Tetrode 3, channel 1)

exp10.add_session('16-05-33', 'm', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp10.add_session('16-27-35', 'n', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 6.

exp10.add_session('16-37-45', 'o', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 6.

exp10.maxDepth = 1667



exp11 = celldatabase.Experiment(subject, '2019-08-18', 'left AC', info=['farMedial', 'facingLeft', 'soundRight'])
experiments.append(exp11)
#Using probe: C39A

exp11.add_site(1100, tetrodes=[1,6,7,8])

exp11.add_session('17-08-49', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp11.add_session('17-15-14', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

exp11.add_session('17-41-02', 'c', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 8.

exp11.add_session('17-50-49', 'd', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 8.


exp11.add_site(1175, tetrodes=[1,2,3,4,5,6,7,8])

exp11.add_session('18-19-49', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 18 (Tetrode 1, channel 1)

exp11.add_session('18-24-07', 'f', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

exp11.add_session('18-40-33', 'g', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp11.add_session('18-49-41', 'h', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp11.maxDepth = 1175



exp12 = celldatabase.Experiment(subject, '2019-08-19', 'left AC', info=['midMedial', 'facingLeft', 'soundRight'])
experiments.append(exp12)
#Using probe: DD46

exp12.add_site(801, tetrodes=[1,2])

exp12.add_session('11-54-39', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 25 (Tetrode 3, channel 1)
# The spike viewer for tetrodes 1,2 looked pretty noisey so I decided to keep moving.

exp12.add_site(959, tetrodes=[1,2])

exp12.add_session('12-28-47', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 25 (Tetrode 3, channel 1)
# The spike viewer for tetrodes 1,2 looked pretty noisey so I decided to keep moving.

exp12.add_site(1251, tetrodes=[1,2,3,4,5,6,8])

exp12.add_session('12-52-25', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 14 (Tetrode 5, channel 1)

exp12.add_session('12-56-33', 'd', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp12.add_session('13-13-29', 'e', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp12.add_session('13-19-40', 'f', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp12.add_site(1305, tetrodes=[1,2,3,4,5,6,8])

exp12.add_session('14-03-38', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'g'
# Reference set to 14 (Tetrode 5, channel 1)

exp12.add_session('14-07-57', 'h', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp12.add_session('14-26-06', 'i', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp12.add_session('14-35-28', 'j', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp12.add_session('14-45-44', 'k', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 4.

exp12.add_session('14-59-08', 'l', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 4.

exp12.add_site(1380, tetrodes=[1,2,3,4,5,6,8])

exp12.add_session('15-24-12', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'm'
# Reference set to 14 (Tetrode 5, channel 1)
# Indication of sound responses on tetrodes 1,2,4.

exp12.add_session('15-28-39', 'n', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp12.add_session('15-47-33', 'o', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,3,4.

exp12.add_session('16-00-59', 'p', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 2,3,4.


exp12.add_site(1455, tetrodes=[1,2,3,4,5,6,7,8])

exp12.add_session('17-17-49', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'q'
# Reference set to 25 (Tetrode 3, channel 1)
# Indication of sound responses on tetrodes 1,2,4.

exp12.add_session('17-22-08', 'r', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp12.add_session('17-41-16', 's', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2,4.

exp12.add_session('18-01-10', 't', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2,4.

exp12.maxDepth = 1455



exp13 = celldatabase.Experiment(subject, '2019-08-20', 'left AC', info=['midLateral', 'facingLeft', 'soundRight'])
experiments.append(exp13)
#Using probe: D65D

exp13.add_site(925, tetrodes=[1,2,3,4,7,8])

exp13.add_session('12-00-34', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 3 (Tetrode 6, channel 1)
# Strong indication of sound responses on tetrode 1. 

exp13.add_session('12-05-59', 'b', 'tc', 'am_tuning_curve')
# Reference set to 3 (Tetrode 6, channel 1)

exp13.add_session('12-21-20', 'c', 'ascending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 1.

exp13.add_session('12-30-52', 'd', 'descending', 'threetones_sequence')
# Reference set to 3 (Tetrode 6, channel 1)
# Frequencies chosen based on tetrode 1.


exp13.add_site(1000, tetrodes=[1,2,4,5,6,7,8])

exp13.add_session('13-01-17', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 25 (Tetrode 3, channel 1)
# Indication of sound responses on tetrode 4. 

exp13.add_session('13-06-06', 'f', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp13.add_session('13-29-41', 'g', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2.

exp13.add_session('13-40-45', 'h', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrodes 1,2.


exp13.add_site(1075, tetrodes=[1,2,3,4,6,8])

exp13.add_session('16-34-36', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'i'
# Reference set to 14 (Tetrode 5, channel 1)

exp13.add_session('16-40-48', 'j', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp13.add_session('16-58-20', 'k', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 1,4.

exp13.add_session('17-08-25', 'l', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrodes 1,4.


exp13.add_site(1150, tetrodes=[1,2,3,4,5,6,8])

exp13.add_session('17-48-43', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'm'
# Reference set to 12 (Tetrode 7, channel 1)

exp13.add_session('17-52-39', 'n', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)

exp13.add_session('18-12-30', 'o', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 3,4.

exp13.add_session('18-22-13', 'p', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 3,4.


exp13.add_site(1150, tetrodes=[1,2,3,4,5,6,8])

exp13.add_session('18-43-36', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'q'
# Reference set to 12 (Tetrode 7, channel 1)

exp13.add_session('18-48-23', 'r', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)

exp13.add_session('19-11-37', 's', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 2,3,4.

exp13.add_session('19-21-37', 't', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrodes 2,3,4.

exp13.maxDepth = 1150




exp14 = celldatabase.Experiment(subject, '2019-08-22', 'left AC', info=['midLateral', 'facingLeft', 'soundRight'])
experiments.append(exp14)
#Using probe: C39C

exp14.add_site(1200, tetrodes=[1,2,3,4,5,6,7,8])

exp14.add_session('16-51-54', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 14 (Tetrode 5, channel 1)

exp14.add_session('16-56-31', 'b', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp14.add_session('17-13-03', 'c', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp14.add_session('17-23-36', 'd', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp14.maxDepth = 1200


exp15 = celldatabase.Experiment(subject, '2019-08-25', 'left AC', info=['midMedial', 'facingLeft', 'soundRight'])
experiments.append(exp15)
#Using probe: C39C


exp15.add_site(1275, tetrodes=[2,3,4,5,6,7,8])

exp15.add_session('18-27-55', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)

exp15.add_session('18-35-13', 'b', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

# I removed probe, cleaned craniotomy with dura hook and re-inserted probe at new location (midLateral).

exp15.add_site(1205, tetrodes=[1,2,3,4,5,6,7,8])

exp15.add_session('19-35-21', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)

exp15.add_session('19-42-26', 'd', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)

exp15.add_session('20-01-29', 'e', 'ascending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp15.add_session('20-12-31', 'f', 'descending', 'threetones_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Frequencies chosen based on tetrode 2.

exp15.maxDepth = 1275



exp16 = celldatabase.Experiment(subject, '2019-08-26', 'left AC', info=['midLateral', 'facingLeft', 'soundRight'])
experiments.append(exp16)
#Using probe: D65D

exp16.add_site(1200, tetrodes=[1,2,3,4,5,6,7,8])

exp16.add_session('13-46-54', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 25 (Tetrode 3, channel 1)

exp16.add_session('13-50-50', 'b', 'tc', 'am_tuning_curve')
# Reference set to 25 (Tetrode 3, channel 1)

exp16.add_session('14-06-28', 'c', 'ascending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 1,2,6.

exp16.add_session('14-16-03', 'd', 'descending', 'threetones_sequence')
# Reference set to 25 (Tetrode 3, channel 1)
# Frequencies chosen based on tetrode 1,2,6.


exp16.add_site(1276, tetrodes=[1,2,3,4,5,6,7,8])

exp16.add_session('14-39-20', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 12 (Tetrode 7, channel 1)

exp16.add_session('14-44-29', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'f'
# Reference set to 22 (Tetrode 2, channel 1)

exp16.add_session('14-50-50', 'g', 'tc', 'am_tuning_curve')
# Reference set to 22 (Tetrode 2, channel 1)

exp16.add_session('15-07-08', 'h', 'ascending', 'threetones_sequence')
# Reference set to 22 (Tetrode 2, channel 1)
# Frequencies chosen based on tetrode 1.

exp16.add_session('15-16-27', 'i', 'descending', 'threetones_sequence')
# Reference set to 22 (Tetrode 2, channel 1)
# Frequencies chosen based on tetrode 1.

exp16.add_site(1350, tetrodes=[1,2,3,4,5,6,7,8])

exp16.add_session('15-40-28', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'j'
# Reference set to 14 (Tetrode 5, channel 1)

exp16.add_session('15-45-08', 'k', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp16.add_session('16-16-56', 'l', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 1,4.

exp16.add_session('16-27-09', 'm', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 1,4.


exp16.add_site(1425, tetrodes=[1,3,4,5,6,7,8])

exp16.add_session('16-50-30', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'n'
# Reference set to 23 (Tetrode 2, channel 3)

exp16.add_site(1500, tetrodes=[1,2,3,4,6,7,8])

exp16.add_session('17-13-48', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'o'
# Reference set to 14 (Tetrode 5, channel 1)

exp16.add_site(1575, tetrodes=[1,2,3,4,5,6,7,8])

exp16.add_session('17-27-52', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'p'
# Reference set to 11 (Tetrode 8, channel 1)

exp16.maxDepth = 1575



















