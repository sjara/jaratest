from jaratoolbox import celldatabase

subject = 'adap043'
experiments = []
#craniotomy AP -1.2 to -2.2mm, ML 3 to 4mm (outer edge could be near AC)
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='leftAStr',
                               info=['anteriorDiI', 'facingPosterior','medial:5,6,7,8','lateral:1,2,3,4'])
experiments.append(exp0)

#1500, 1600, 1700, 1800, 1900, 2000, 2100 not sound responsive
exp0.add_site(2150, tetrodes=[1,2,3,4,7,8])
exp0.add_session('14-17-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 supressed by noise?
exp0.add_session('14-21-33', 'a', 'tc', 'am_tuning_curve') #TT1-4 tuned roughly 8.1-12.1kHz


exp0.add_site(2250, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-48-56', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT6&7 offset response?
exp0.add_session('14-51-02', 'b', 'tc', 'am_tuning_curve') 


exp0.add_site(2320, tetrodes=[1,2,3,5,6,7,8])
exp0.add_session('15-32-07', None, 'noiseburst', 'am_tuning_curve') #ref to chan20 in TT4, TT6&8 sound responsive
exp0.add_session('15-33-48', 'c', 'tc', 'am_tuning_curve') #TT6&8 tuned differently


exp0.add_site(2430, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('15-53-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5-8 sound responsive
exp0.add_session('15-55-38', 'd', 'tc', 'am_tuning_curve') #TT5-8 tuned differently

exp0.add_site(2500, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-16-41', None, 'noiseburst', 'am_tuning_curve') #ref to chan32 in TT3, TT4-8 sound responsive
exp0.add_session('16-19-05', 'e', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2570, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-39-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan30 in TT3, TT4-8 sound responsive
exp0.add_session('16-41-55', 'f', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2670, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-59-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan30 in TT3, TT6-8 sound responsive
exp0.add_session('17-03-27', 'g', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2770, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('17-24-00', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT3-7 sound responsive
exp0.add_session('17-28-41', 'h', 'tc', 'am_tuning_curve') #TT3-8 tuned differently

#Mouse kept trying to touch array with his paw, because saline kept dripping into his left eye. End experiment, reinforce left side guard


exp1 = celldatabase.Experiment(subject,
                               '2017-05-10',
                               brainarea='leftAStr',
                               info=['anterior-meidalDiD', 'facingPosterior','medial:5,6,7,8','lateral:1,2,3,4'])
experiments.append(exp1)

#1500, 1700, 1800, 1900, 2000, 2050, 2100um not sound responsive
exp1.add_site(2350, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('13-27-51', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT6 sound responsive 
exp1.add_session('13-30-09', 'a', 'tc', 'am_tuning_curve') #TT6 tuned low freq


exp1.add_site(2420, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('13-52-49', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT6 sound responsive 
exp1.add_session('13-57-56', 'b', 'tc', 'am_tuning_curve') #TT6 tuned low freq


exp1.add_site(2520, tetrodes=[1,2,3,4,5,6,8])
#exp1.add_session('14-18-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan6 in TT7, TT5&6 sound responsive 
exp1.add_session('14-20-12', 'c', 'tc', 'am_tuning_curve') #4-TT6 tuned
exp1.add_session('14-38-43', None, 'noiseburst', 'am_tuning_curve') #noise burst after tuning, TT4-6 sound responsive 

exp1.add_site(2600, tetrodes=[2,3,4,5,6,7,8])
#exp1.add_session('14-45-22', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT4,5&8 start to be sound responsive 
exp1.add_session('14-48-55', 'd', 'tc', 'am_tuning_curve') #TT4,5,6,8 tuned
exp1.add_session('15-04-50', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT4,5,6&8 sound responsive 

exp1.add_site(2670, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('15-10-06', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT(2),4,5,6,8 sound responsive 
exp1.add_session('15-11-37', 'e', 'tc', 'am_tuning_curve') #TT4,5,6,8 tuned

exp1.add_site(2740, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('15-39-30', None, 'noiseburst', 'am_tuning_curve') #ref to chan27 in TT1, TT2,4,5,6,8 sound responsive 
exp1.add_session('15-41-11', 'f', 'tc', 'am_tuning_curve') 

exp1.add_site(2840, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('16-05-29', None, 'noiseburst', 'am_tuning_curve') #ref to chan27 in TT1, TT3,4,5,6,7,8 sound responsive 
exp1.add_session('16-07-44', 'g', 'tc', 'am_tuning_curve') 

exp1.add_site(2940, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('16-27-20', None, 'noiseburst', 'am_tuning_curve') #ref to chan31 in TT2, TT3,4,5,6,7,8 sound responsive 
exp1.add_session('16-29-06', 'h', 'tc', 'am_tuning_curve') #TT4,5,6,8 tuned


exp2 = celldatabase.Experiment(subject,
                               '2017-05-11',
                               brainarea='rightAStr',
                               info=['anteriorDiI', 'facingPosterior','medial:1,2,3,4','lateral:5,6,7,8'])
experiments.append(exp2)

#1800, 1900, 2000, 2050, 2100, 2200, 2300, 2350, 2400, 2450, 2500, 2550, 2600um not sound responsive
exp2.add_site(2660, tetrodes=[2,3,4,5,6,7,8])
#exp2.add_session('10-54-56', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 inTT1, TT6 sound responsive 
exp2.add_session('10-57-40', 'a', 'tc', 'am_tuning_curve') #TT3&6 tuned around 9.9
exp2.add_session('11-13-03', None, 'noiseburst', 'am_tuning_curve')


exp2.add_site(2720, tetrodes=[2,3,4,5,6,7,8])
#exp2.add_session('11-18-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 inTT1 TT6 sound responsive 
exp2.add_session('11-20-59', 'b', 'tc', 'am_tuning_curve') #TT6 tuned 
exp2.add_session('11-37-22', None, 'noiseburst', 'am_tuning_curve')


exp2.add_site(2780, tetrodes=[2,3,4,5,6,7,8])
#exp2.add_session('11-41-43', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 inTT1, TT6(2,4) sound responsive 
exp2.add_session('11-44-38', 'c', 'tc', 'am_tuning_curve') #TT6 tuned 
exp2.add_session('12-00-13', None, 'noiseburst', 'am_tuning_curve')


exp2.add_site(2870, tetrodes=[1,2,3,4,5,6,7,8])
#exp2.add_session('12-04-28', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 inTT1, TT2,4,6,8 sound responsive 
exp2.add_session('12-05-35', 'd', 'tc', 'am_tuning_curve') #TT6 tuned 
exp2.add_session('12-20-54', None, 'noiseburst', 'am_tuning_curve')


exp3 = celldatabase.Experiment(subject,
                               '2017-05-12',
                               brainarea='rightAStr',
                               info=['anterior-medialDiD','three-shanks','facingPosterior','medial:None','lateral:None'])
experiments.append(exp3)

#1800, 2000, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2450, 2500um not sound responsive
exp3.add_site(2535, tetrodes=[1,2,3,4,6])
exp3.add_session('10-42-03', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 inTT5, TT2 sound responsive 
exp3.add_session('10-43-57', 'a', 'tc', 'am_tuning_curve')

#2570, 2640um not sound responsive
exp3.add_site(2700, tetrodes=[1,2,3,4,6])
exp3.add_session('11-18-18', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 inTT5, TT2&4 sound responsive 
exp3.add_session('11-21-58', 'b', 'tc', 'am_tuning_curve')

exp3.add_site(2760, tetrodes=[2,3,4,5,6])
exp3.add_session('11-41-45', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 inTT1, TT2&4 sound responsive 
exp3.add_session('11-43-25', 'c', 'tc', 'am_tuning_curve')

exp3.add_site(2830, tetrodes=[2,3,4,5,6])
exp3.add_session('12-05-19', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 inTT1, TT2,3,4 sound responsive 
exp3.add_session('12-07-12', 'd', 'tc', 'am_tuning_curve')#a bit shorter since saline may have dried up and start to see noise 

exp3.add_site(2915, tetrodes=[1,2,3,4,5,6])
#exp3.add_session('12-26-17', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 inTT5, TT1,3,4 sound responsive 
exp3.add_session('12-27-52', 'e', 'tc', 'am_tuning_curve')
exp3.add_session('12-44-08', None, 'noiseburst', 'am_tuning_curve')


exp4 = celldatabase.Experiment(subject,
                               '2017-05-15',
                               brainarea='rightAStr',
                               info=['anterior-medialDiD', 'four-shanks', 'facingPosterior','medial:1,2,3,4','lateral:5,6,7,8'])
experiments.append(exp4)

#1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300um not sound responsive
exp4.add_site(2360, tetrodes=[1,3,4,5,6,7,8])
#exp4.add_session('14-45-28', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 inTT2, TT4 sound responsive 
exp4.add_session('14-53-35', 'a', 'tc', 'am_tuning_curve') #ref to chan26 inTT2, TT4,6,8 sound responsive 
exp4.add_session('15-04-49', None, 'noiseburst', 'am_tuning_curve')


exp4.add_site(2440, tetrodes=[1,3,4,5,6,7,8])
#exp4.add_session('15-09-13', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 inTT2, TT4,6,8 sound responsive 
exp4.add_session('15-13-04', 'b', 'tc', 'am_tuning_curve') #ref to chan26 inTT2, TT4,6,8 sound responsive 
exp4.add_session('15-28-30', None, 'noiseburst', 'am_tuning_curve')


exp4.add_site(2500, tetrodes=[1,3,4,5,6,7,8])
#exp4.add_session('15-38-15', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 inTT2, TT4,6,8 sound responsive 
exp4.add_session('15-40-10', 'c', 'tc', 'am_tuning_curve') #ref to chan26 inTT2, all TTs sound responsive 
exp4.add_session('15-56-04', None, 'noiseburst', 'am_tuning_curve')


exp4.add_site(2570, tetrodes=[1,3,4,5,6,7,8])
exp4.add_session('16-02-19', 'd', 'tc', 'am_tuning_curve') #ref to chan26 inTT2, sound responsive 
exp4.add_session('16-17-27', None, 'noiseburst', 'am_tuning_curve')


exp4.add_site(2640, tetrodes=[1,2,3,4,5,6,7,8])
exp4.add_session('16-24-56', 'e', 'tc', 'am_tuning_curve') #ref to chan31 inTT2, sound responsive 
exp4.add_session('16-41-28', None, 'noiseburst', 'am_tuning_curve')


exp4.add_site(2720, tetrodes=[1,2,3,4,5,6,7,8])
exp4.add_session('16-54-11', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('16-55-51', 'f', 'tc', 'am_tuning_curve') #ref to chan31 inTT2, sound responsive 




