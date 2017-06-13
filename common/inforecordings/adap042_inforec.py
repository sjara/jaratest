from jaratoolbox import celldatabase

subject = 'adap042'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-06-09',
                               brainarea='leftAStr',
                               info=['3/4posteriorDiI', 'facingPosterior'])
experiments.append(exp0)

'''
exp0.add_site(1750, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('14-01-04', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1&2(most lateral) sound responsive - could be in AC? 

exp0.add_site(1850, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('14-06-57', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1&2 no longer sound responsive, TT8(most medial) weakly sound repsonsive, may be near hippocampus?

exp0.add_site(1950, tetrodes=[1,2,4,7,8])
exp0.add_session('14-10-21', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT7&8 sound responsive
exp0.add_session('14-13-17', 'a', 'tc', 'am_tuning_curve') #since there's no sound response a bit deeper than this site, this could have been in AC or hippocampus?
'''
#2050um only TT7 sound responsive, 2150, 2200, 2250, 2300, 2350um no sound response

exp0.add_site(2470, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('14-59-52', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2 sound responsive
exp0.add_session('15-01-24', 'b', 'tc', 'am_tuning_curve') 

exp0.add_site(2530, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('15-19-47', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2 weakly sound responsive
exp0.add_session('15-21-50', 'c', 'tc', 'am_tuning_curve') 
#2600, 2650, 2700, 2750, 2800, 2900, 3000, 3100um not sound responsive


exp1 = celldatabase.Experiment(subject,
                               '2017-06-12',
                               brainarea='leftAStr',
                               info=['medial-posteriorDiI', 'facingPosterior'])
experiments.append(exp1)

#1600um TT1(most lateral) sound responsive, very large spikes - possibly AC
#1700um no more sound response, 1800, 1900, 2000um late response after 0.15 either offset of movement-related
exp1.add_site(2100, tetrodes=[1,4,5,6,7,8])
exp1.add_session('15-32-45', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT5&6 potential sound suppression
exp1.add_session('15-36-36', 'a', 'tc', 'am_tuning_curve') 

exp1.add_site(2300, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('16-00-16', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT4&7 sound responsive
exp1.add_session('16-01-45', 'b', 'tc', 'am_tuning_curve') 

exp1.add_site(2370, tetrodes=[1,2,3,4,5,7,8])
exp1.add_session('16-19-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 sound responsive
exp1.add_session('16-21-34', 'c', 'tc', 'am_tuning_curve') 

exp1.add_site(2450, tetrodes=[1,2,3,4,7])
exp1.add_session('16-44-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan2 in TT6, TT2-4 sound responsive
exp1.add_session('16-46-48', 'd', 'tc', 'am_tuning_curve') 

exp1.add_site(2520, tetrodes=[1,2,3,4,5,7,8])
exp1.add_session('17-08-04', None, 'noiseburst', 'am_tuning_curve') #ref to chan2 in TT6, TT2-4 sound responsive
exp1.add_session('17-10-03', 'e', 'tc', 'am_tuning_curve') 

exp1.add_site(2600, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('17-38-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan4 in TT8, TT1-4&6 sound responsive
exp1.add_session('17-40-40', 'f', 'tc', 'am_tuning_curve') 

exp1.add_site(2680, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('18-00-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan4 in TT8, TT1-6 sound responsive
exp1.add_session('18-02-47', 'g', 'tc', 'am_tuning_curve') 

