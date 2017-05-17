from jaratoolbox import celldatabase

subject = 'adap044'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-16',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior'])
experiments.append(exp0)

#1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700um not sound responsive
exp0.add_site(2800, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('15-25-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT8 sound responsive 
exp0.add_session('15-26-50', 'a', 'tc', 'am_tuning_curve') 

#2850um not sound responsive
exp0.add_site(2900, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('15-52-55', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT7 weakly sound responsive 
exp0.add_session('15-55-20', 'b', 'tc', 'am_tuning_curve') 

exp0.add_site(2960, tetrodes=[1,2,3,5,6,7,8])
#exp0.add_session('16-14-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan17 in TT4, TT7  sound responsive 
exp0.add_session('16-17-16', 'c', 'tc', 'am_tuning_curve') 
exp0.add_session('16-34-13', None, 'noiseburst', 'am_tuning_curve') #TT2&7 sound responsive

#3000, 3050um not sound responsive
exp0.add_site(3100, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-51-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT1 weakly sound responsive 
exp0.add_session('16-54-07', 'd', 'tc', 'am_tuning_curve') 

