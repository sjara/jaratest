from jaratoolbox import celldatabase

subject = 'chad015'
experiments=[]

exp1 = celldatabase.Experiment(subject, '2019-07-17', 'right AC', info=['midLateralDiD', 'facingAnterior', 'soundLeft'])
experiments.append(exp1)
#Using probe: C39C


# exp1.add_site(885, tetrodes=[2,3,4,5,6,7,8])
# exp1.add_session('16-00-40', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 18 (Tetrode 1, channel 1)
# Minimal indication of sound response


# exp1.add_site(983, tetrodes=[2,3,4,5,6,7,8])
# exp1.add_session('16-10-50', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'b'
# Reference set to 18 (Tetrode 1, channel 1)
# Minimal indication of sound response

exp1.add_site(1022, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('16-19-22', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'c'
# Reference set to 18 (Tetrode 1, channel 1)
# Sound response on tetrode 2.

exp1.add_session('16-27-34', 'd', 'tc', 'am_tuning_curve')
# Reference set to 18 (Tetrode 1, channel 1)
# 1 intensity (70dB)

exp1.add_session('16-40-29', 'e', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_session('17-05-27', 'f', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_session('17-09-53', 'g', 'many-standards', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.add_session('17-19-56', 'h', 'oddball', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)
# Target tone (26800Hz) and standard (17000Hz) are closer together than previous oddball sequence.

exp1.add_session('17-25-08', 'i', 'standard', 'oddball_sequence')
# Reference set to 18 (Tetrode 1, channel 1)

exp1.maxDepth = 1022


exp2 = celldatabase.Experiment(subject, '2019-08-06', 'left AC', info=['farLateralDiD', 'facingAnterior', 'soundRight'])
experiments.append(exp2)
#Using probe: C39C

exp2.add_site(814, tetrodes=[1,2,3,4,5,6,8])
exp2.add_session('14-17-16', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('14-23-34', 'b', 'tc', 'am_tuning_curve')
# 3 intensities
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('14-56-24', 'c', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Intensity 70db

exp2.add_session('15-05-42', 'd', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Intensity 70db

exp2.add_session('15-29-03', 'e', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Intensity 60db

exp2.add_session('15-36-34', 'f', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Intensity 60db

exp2.add_site(880, tetrodes=[1,2,3,4,5,6,8])
exp2.add_session('16-14-18', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'g'
# Reference set to 14 (Tetrode 5, channel 1)

exp2.add_session('16-20-46', 'h', 'tc', 'am_tuning_curve')
# 3 intensities
# Reference set to 14 (Tetrode 5, channel 1)

exp2.add_session('16-57-48', 'i', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Intensity 60db

exp2.add_session('17-04-17', 'j', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Intensity 60db

exp2.add_session('17-11-54', 'k', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Intensity 70db

exp2.add_session('17-18-26', 'l', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Intensity 70db

exp2.add_site(930, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('17-48-52', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'm'
# Reference set to 9 (Tetrode 5, channel 3)

exp2.add_session('17-55-21', 'n', 'tc', 'am_tuning_curve')
# 3 intensities
# Reference set to 9 (Tetrode 5, channel 3)

exp2.add_session('18-21-54', 'o', 'ascending', 'threetones_sequence')
# Reference set to 9 (Tetrode 5, channel 3)

exp2.add_session('18-29-34', 'p', 'descending', 'threetones_sequence')
# Reference set to 9 (Tetrode 5, channel 3)

exp2.add_site(1030, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('18-44-36', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'q'
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('18-49-51', 'r', 'tc', 'am_tuning_curve')
# 3 intensities
# Reference set to 12 (Tetrode 7, channel 1)

exp2.add_session('19-16-44', 's', 'ascending', 'threetones_sequence')
# Reference set to 9 (Tetrode 5, channel 3)

exp2.add_session('19-23-25', 't', 'descending', 'threetones_sequence')
# Reference set to 9 (Tetrode 5, channel 3)

exp2.maxDepth = 1030



exp3 = celldatabase.Experiment(subject, '2019-08-08', 'left AC', info=['midLateralDiD', 'facingAnterior', 'soundRight'])
experiments.append(exp3)
#Using probe: C39C

exp3.add_site(802, tetrodes=[2])
exp3.add_session('11-54-23', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('12-03-15', 'b', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('12-30-53', 'c', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('12-37-28', 'd', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)


exp3.add_site(875, tetrodes=[1,2,3,4,6,8])
exp3.add_session('13-09-46', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'e'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('13-14-14', 'f', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)
# 3 intensities

exp3.add_session('13-37-15', 'g', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('13-44-02', 'h', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)


exp3.add_site(950, tetrodes=[1,2,4,5,6,8])
exp3.add_session('13-55-20', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'i'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('14-00-26', 'j', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)
# 3 intensities

exp3.add_session('14-35-03', 'k', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp3.add_session('14-42-18', 'l', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 2.

exp3.add_session('14-50-07', 'm', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 8.

exp3.add_session('14-56-50', 'n', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 8.


exp3.add_site(1025, tetrodes=[1,2,3,4,5,6,8])
exp3.add_session('15-15-20', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'o'
# Reference set to 14 (Tetrode 5, channel 1)

exp3.add_session('15-22-20', 'p', 'tc', 'am_tuning_curve')
# Reference set to 14 (Tetrode 5, channel 1)
# 3 intensities


exp3.add_session('15-55-52', 'q', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 8.

exp3.add_session('16-04-21', 'r', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 8.

exp3.add_session('16-12-28', 's', 'ascending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 1.

exp3.add_session('16-19-19', 't', 'descending', 'threetones_sequence')
# Reference set to 14 (Tetrode 5, channel 1)
# Frequencies chosen based on tetrode 1.


exp3.add_site(1100, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('16-37-12', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'u'
# Reference set to 12 (Tetrode 7, channel 1)

exp3.add_session('16-42-30', 'v', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)
# 3 intensities


exp3.add_site(1101, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('16-53-49', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'w'
# No reference

exp3.add_session('17-25-51', 'x', 'tc', 'am_tuning_curve')
# No reference
# 3 intensities

exp3.add_session('17-50-13', 'y', 'ascending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrode 7.

exp3.add_session('17-56-37', 'z', 'descending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrode 7.


exp3.maxDepth = 1101



exp4 = celldatabase.Experiment(subject, '2019-08-09', 'left AC', info=['midMedialDiD', 'facingAnterior', 'soundRight'])
experiments.append(exp4)
#Using probe: C39C

exp4.add_site(802, tetrodes=[1,2,3,4,5,6,8])

exp4.add_session('16-43-11', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'a'
# Reference set to 12 (Tetrode 7, channel 1)

exp4.add_session('16-54-32', 'b', 'tc', 'am_tuning_curve')
# Reference set to 12 (Tetrode 7, channel 1)
# 3 intensities

exp4.add_session('17-18-26', 'd', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrode 2.
# The behavioral data suffix does indeed correspond to the ascending sequence. I accidently saved it as 'd' instead of 'c'.

exp4.add_session('17-25-34', 'c', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrode 2.

exp4.add_session('17-35-47', 'e', 'ascending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrode 8.

exp4.add_session('17-43-10', 'f', 'descending', 'threetones_sequence')
# Reference set to 12 (Tetrode 7, channel 1)
# Frequencies chosen based on tetrode 8.

exp4.add_site(877, tetrodes=[1,2,3,4,5,6,7,8])

exp4.add_session('17-59-49', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'h'
# No reference
# The behavioral data suffix does indeed correspond to the noiseburst. I accidently saved it as 'h' instead of 'g'.

exp4.add_session('18-08-03', 'g', 'tc', 'am_tuning_curve')
# No reference
# 3 intensities

exp4.add_session('18-39-02', 'i', 'ascending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 2,5.

exp4.add_session('18-46-10', 'j', 'descending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 2,5.

exp4.add_session('19-02-13', 'k', 'ascending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 4.

exp4.add_session('19-10-15', 'l', 'descending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 4.


exp4.add_site(950, tetrodes=[1,2,3,4,5,6,7,8])

exp4.add_session('19-23-55', None, 'noiseburst', 'am_tuning_curve')
# Behavior suffix 'm'
# No reference

exp4.add_session('19-29-00', 'n', 'tc', 'am_tuning_curve')
# No reference
# 3 intensities

exp4.add_session('19-52-32', 'o', 'ascending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 2,3.

exp4.add_session('20-01-35', 'p', 'descending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 2,3.

exp4.add_session('20-31-52', 'q', 'ascending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 6.

exp4.add_session('20-39-31', 'r', 'descending', 'threetones_sequence')
# No reference
# Frequencies chosen based on tetrodes 6.

exp4.maxDepth = 950






