from jaratoolbox import celldatabase

subject = 'adap042'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-06-09',
                               brainarea='leftAStr',
                               info=['3/4posteriorDiI', 'facingPosterior','medial:1,2', 'lateral:None'])
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
                               info=['medialDiD', 'facingPosterior','medial:5,6', 'lateral:1,2,3,4'])
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


exp2 = celldatabase.Experiment(subject,
                               '2017-06-13',
                               brainarea='leftAStr',
                               info=['medial-posteriorDiI', 'facingPosterior','medial:3,4,5,6', 'lateral:1,2'])
experiments.append(exp2)

exp2.add_site(2240, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('14-09-15', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT2 weakly sound responsive
exp2.add_session('14-12-09', 'a', 'tc', 'am_tuning_curve') 

exp2.add_site(2310, tetrodes=[1,2,3,4,5,7])
exp2.add_session('14-29-01', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 sound responsive
exp2.add_session('14-30-46', 'b', 'tc', 'am_tuning_curve') 

exp2.add_site(2400, tetrodes=[1,2,3,4,7,8])
exp2.add_session('14-54-10', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 sound responsive
exp2.add_session('14-55-54', 'c', 'tc', 'am_tuning_curve') 

exp2.add_site(2470, tetrodes=[1,2,3,4,5,7])
exp2.add_session('15-15-47', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT3 sound responsive
exp2.add_session('15-17-58', 'd', 'tc', 'am_tuning_curve') 

exp2.add_site(2550, tetrodes=[1,2,3,4,5,7,8])
exp2.add_session('15-37-20', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT3 sound responsive
exp2.add_session('15-39-00', 'e', 'tc', 'am_tuning_curve') 


exp3 = celldatabase.Experiment(subject,
                               '2017-06-14',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior','medial:1,2', 'lateral:3,4'])
experiments.append(exp3)

#1600, 1700um mostly seeing movement/startle-related response
exp3.add_site(2070, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('13-33-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT2 sound responsive
exp3.add_session('13-35-07', 'a', 'tc', 'am_tuning_curve') 

exp3.add_site(2130, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('13-54-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT1-2 sound responsive
exp3.add_session('13-56-07', 'b', 'tc', 'am_tuning_curve') 

exp3.add_site(2200, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('14-19-14', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT1-2,4-8 sound responsive
exp3.add_session('14-22-05', 'c', 'tc', 'am_tuning_curve') 

exp3.add_site(2270, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('14-47-44', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT1-2,4-8 sound responsive
exp3.add_session('14-50-42', 'd', 'tc', 'am_tuning_curve') 

exp3.add_site(2340, tetrodes=[1,2,4,5,6,7,8])
exp3.add_session('15-10-47', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT1-2,4-8 sound responsive
exp3.add_session('15-17-29', 'e', 'tc', 'am_tuning_curve') 

exp3.add_site(2410, tetrodes=[1,2,3,4,5,6,7,8])
exp3.add_session('15-38-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 sound responsive
exp3.add_session('15-40-11', 'f', 'tc', 'am_tuning_curve') 


exp4 = celldatabase.Experiment(subject,
                               '2017-06-19',
                               brainarea='rightAStr',
                               info=['posteriorDiD', 'facingPosterior','medial:1,2,3,4', 'lateral:5,6'])

experiments.append(exp4)

#1500, 1600 mostly seeing movement/startle-related response
#1700, 1800um most lateral TT7/8 has sound response, probably AC, later disappeared
exp4.add_site(2050, tetrodes=[2,3,4,5,6,7,8])
exp4.add_session('15-28-22', None, 'noiseburst', 'am_tuning_curve') #ref to chan27 in TT1, TT8 sound responsive
exp4.add_session('15-30-12', 'a', 'tc', 'am_tuning_curve') 

exp4.add_site(2150, tetrodes=[2,3,4,5,6,7,8])
exp4.add_session('15-48-06', None, 'noiseburst', 'am_tuning_curve') #ref to chan27 in TT1, TT4-8 sound responsive
exp4.add_session('15-49-44', 'b', 'tc', 'am_tuning_curve') 

exp4.add_site(2220, tetrodes=[1,2,3,4,5,7,8])
exp4.add_session('16-11-28', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT2-4 sound responsive
exp4.add_session('16-13-18', 'c', 'tc', 'am_tuning_curve') 

exp4.add_site(2290, tetrodes=[1,2,3,4,7,8])
exp4.add_session('16-34-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT3&7 sound responsive
exp4.add_session('16-35-54', 'd', 'tc', 'am_tuning_curve') 

exp4.add_site(2355, tetrodes=[1,2,3,4,7,8])
exp4.add_session('16-55-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT3&7 sound responsive
exp4.add_session('16-57-16', 'e', 'tc', 'am_tuning_curve') 

exp4.add_site(2420, tetrodes=[1,2,3,4,5,6,7,8])
exp4.add_session('17-16-13', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT2,3,4,6 sound responsive
exp4.add_session('17-17-49', 'f', 'tc', 'am_tuning_curve') 

exp4.add_site(2490, tetrodes=[1,2,3,4,5,6,7,8])
exp4.add_session('17-37-21', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2,3,4,6 sound responsive
exp4.add_session('17-38-45', 'g', 'tc', 'am_tuning_curve') 


exp5 = celldatabase.Experiment(subject,
                               '2017-06-20',
                               brainarea='leftAStr',
                               info=['medialDiO', 'facingPosterior','medial:1,2,3,4', 'lateral:None'])
experiments.append(exp5)

#1700, 1800, 1900um not sound responsive
exp5.add_site(2040, tetrodes=[2,3,4,5,6,7,8])
exp5.add_session('15-32-09', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5 offset response 
exp5.add_session('15-34-08', 'a', 'tc', 'am_tuning_curve') 

exp5.add_site(2110, tetrodes=[1,2,3,4,5,7,8])
exp5.add_session('15-54-04', None, 'noiseburst', 'am_tuning_curve') #ref to chan2 in TT6, TT1-5 offset response 
exp5.add_session('15-55-51', 'b', 'tc', 'am_tuning_curve') 

exp5.add_site(2190, tetrodes=[1,2,3,5,6,7,8])
exp5.add_session('16-15-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan20 in TT4, TT3&5 offset response 
exp5.add_session('16-17-25', 'c', 'tc', 'am_tuning_curve') 

exp5.add_site(2250, tetrodes=[1,2,3,4,5,7,8])
exp5.add_session('16-36-35', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT2 responsive
exp5.add_session('16-38-18', 'd', 'tc', 'am_tuning_curve') 

exp5.add_site(2340, tetrodes=[1,2,3,4,5,7,8])
exp5.add_session('16-59-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT2 responsive
exp5.add_session('17-00-57', 'e', 'tc', 'am_tuning_curve') 
