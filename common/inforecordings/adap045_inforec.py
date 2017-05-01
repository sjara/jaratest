from jaratoolbox import celldatabase

subject = 'adap045'
experiments = []
#craniotomy AP -1.2 to -2.2mm, ML 3 to 4mm (outer edge could be near AC)
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-04-30',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior'])
experiments.append(exp0)

exp0.add_site(1700, tetrodes=range(1, 9))
exp0.add_session('14-47-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan28 in TT1, TT8 most lateral noise responsive, could be in AC??
exp0.add_session('14-53-19', 'a', 'tc', 'am_tuning_curve') #ref to chan25 in TT3, TT8 tuned, moving on. 

exp0.add_site(1900, tetrodes=range(1, 3))
exp0.add_session('15-14-36', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1&2 (most medial) noise responsive
exp0.add_session('15-17-11', 'b', 'tc', 'am_tuning_curve') #ref to chan14 in TT5, TT1 noisy but appeared to have some tuning. 

exp0.add_site(2050, tetrodes=range(1, 3))
exp0.add_session('15-46-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1 noise responsive
exp0.add_session('15-51-53', 'c', 'tc', 'am_tuning_curve') #ref to chan14 in TT5, TT1 tuned.

#2200um TT3&4 started to have spikes, but not noise responsive
#2300um still no noise response
exp0.add_site(2360, tetrodes=range(1, 7))
exp0.add_session('16-21-34', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT4 noise responsive
exp0.add_session('16-23-03', 'd', 'tc', 'am_tuning_curve') #ref to chan12 in TT7, TT4 tuned. 

exp0.add_site(2500, tetrodes=[1,2,3,4,6,8]) #at 2500um all TTs except TT5&7 have spikes
exp0.add_session('16-50-40', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT8 may be noise responsive
exp0.add_session('16-52-08', 'e', 'tc', 'am_tuning_curve') #ref to chan14 in TT5, TT8 tuned. 

exp0.add_site(2650, tetrodes=[1,2,3,4,6,7,8]) #at 2650um all TTs except TT5 have spikes
exp0.add_session('17-12-14', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 in TT5, TT7&8 may be noise responsive
exp0.add_session('17-15-16', 'f', 'tc', 'am_tuning_curve') #ref to chan8 in TT5,  no obvious tuning.

exp0.add_site(2800, tetrodes=[1,2,3,4,5,6,7,8]) #at 2800um all TTs except TT5 have spikes
exp0.add_session('17-41-35', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, all TTs may be noise responsive
exp0.add_session('17-43-49', 'g', 'tc', 'am_tuning_curve') #ref to chan14 in TT5, all TTs tuned...

#2950um, all TTs have spikes, no noise response
exp0.add_site(3000, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('18-10-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT5&6 weakly noise responsive
exp0.add_session('18-12-09', 'h', 'tc', 'am_tuning_curve') #ref to chan22 in TT2

exp0.add_site(3123, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('18-33-18', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT6 noise responsive
exp0.add_session('18-35-40', 'i', 'tc', 'am_tuning_curve') 

exp0.add_site(3250, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('18-54-49', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 in TT2, TT3-8 may be noise responsive
exp0.add_session('18-56-45', 'j', 'tc', 'am_tuning_curve') 

#3350um, 3450um, 3500um, 3550um no obvious noise response, stop and pull up.

