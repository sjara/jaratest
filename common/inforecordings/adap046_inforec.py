from jaratoolbox import celldatabase

subject = 'adap046'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-30',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior'])
experiments.append(exp0)

#1700, 1800, 1900, 2000, 2100, 2200um not sound responsive
exp0.add_site(2300, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('13-29-42', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT5-8 offset response 
exp0.add_session('13-37-47', 'a', 'tc', 'am_tuning_curve') 

exp0.add_site(2380, tetrodes=[1,3,4,5,6,7,8])
#exp0.add_session('13-58-12', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT5-8 offset response, TT4 responsive 
exp0.add_session('13-59-56', 'b', 'tc', 'am_tuning_curve') 
exp0.add_session('14-17-30', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2470, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('14-27-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT5-8 offset response, TT2 responsi8ve 
exp0.add_session('14-30-56', 'c', 'tc', 'am_tuning_curve') 

exp0.add_site(2600, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('14-56-01', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT4 responsi8ve 
exp0.add_session('14-57-56', 'd', 'tc', 'am_tuning_curve') 

exp0.add_site(2700, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('15-19-19', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT2&4 clear onset response 
exp0.add_session('15-21-43', 'e', 'tc', 'am_tuning_curve') 

exp0.add_site(2780, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('15-40-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT2-4 clear onset response 
exp0.add_session('15-42-27', 'f', 'tc', 'am_tuning_curve') 

exp0.add_site(2860, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-01-48', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT3,4,6,8 clear onset response 
exp0.add_session('16-04-26', 'g', 'tc', 'am_tuning_curve') 

exp0.add_site(2960, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-23-41', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1,3,4,6,8 response 
exp0.add_session('16-26-17', 'h', 'tc', 'am_tuning_curve') 
