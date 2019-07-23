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

