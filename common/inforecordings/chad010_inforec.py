from jaratoolbox import celldatabase

subject = 'chad010' 
experiments=[]

#2019-02-08: Forced to abort recording process due to excessive bleeding from the craniotomy.


exp0 = celldatabase.Experiment(subject, '2019-02-12', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1150, tetrodes=[1,2,3,4,5,6,7,8])
#exp0.add_session('15-13-44', 'a', 'tc', 'am_tuning_curve')
#Reference set to 3 (Tetrode 6, channel 1)
#Having problems with ground; the lfp is fluctuating between virtually no noise or signal to tons of noise.
#Raster plot does not show clear indication of cell presence

exp0.maxDepth = 1150

exp1 = celldatabase.Experiment(subject, '2019-02-14', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp1)

exp1.add_site(1145, tetrodes=[1,2,3,4,5,6,7,8])
#exp1.add_session('12-51-36', 'a', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)
#Raster plot does not show clear indication of cell presence

exp1.add_site(1250, tetrodes=[1])
#exp1.add_session('13-17-16', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Reference set to 14 (Tetrode 5, channel 1)
#Raster plot does not show clear indication of cell presence

exp1.maxDepth = 1250

exp2 = celldatabase.Experiment(subject, '2019-02-17', 'right_AC', info=['farMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp2)

exp2.add_site(1130, tetrodes=[1,2])
exp2.add_session('16-06-20', 'a', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)

exp2.add_site(1250, tetrodes=[1,2,3,4,6])
exp2.add_session('16-21-05', 'b', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)

exp2.add_session('16-37-06', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'c'
#Reference set to 14 (Tetrode 5, channel 1)
#Good sound responsive cell on tetrode 2.

exp2.add_session('17-37-10', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'd'
#Reference set to 14 (Tetrode 5, channel 1)

exp2.add_session('17-45-31', 'e', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)
#Indication of frequency preference on tetrode 1.

exp2.add_site(1400, tetrodes=[1,2])
exp2.add_session('18-36-59', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'f'
#Reference set to 11 (Tetrode 8, channel 1)
#Indication of sound responsive cell on tetrode 2.

exp2.add_session('18-45-43', 'g', 'tc', 'am_tuning_curve')
#Reference set to 11 (Tetrode 8, channel 1)
#Indication of frequency preference on tetrodes 1,2.

exp2.add_site(1500, tetrodes=[1,2])
exp2.add_session('19-33-17', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'h'
#Reference set to 3 (Tetrode 6, channel 1)
#Indication of sound responsive cell on tetrodes 1,2.

#exp2.add_session('19-39-23', 'i', 'tc', 'am_tuning_curve')
#Reference set to 3 (Tetrode 6, channel 1)
#Index error when attempting to generate raster.

exp2.maxDepth = 1500

exp3 = celldatabase.Experiment(subject, '2019-02-19', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp3)

exp3.add_site(1395, tetrodes=[8])
exp3.add_session('14-42-18', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Reference set to 5 (Tetrode 7, channel 2)
#Could be noise or non-sound-responsive cell.

exp3.add_site(1450, tetrodes=[8])
exp3.add_session('14-54-19', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Reference set to 6 (Tetrode 7, channel 3)
#Could be noise or non-sound-responsive cell.

exp3.add_site(1200, tetrodes=[2,8])
exp3.add_session('15-47-59', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'c'
#Reference set to 14 (Tetrode 5, channel 1)
#Could be noise or non-sound-responsive cell.

exp3.add_site(1300, tetrodes=[2,8])
exp3.add_session('15-57-17', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'd'
#Reference set to 6 (Tetrode 7, channel 3)
#Could be noise or non-sound-responsive cell.

exp3.maxDepth = 1450

