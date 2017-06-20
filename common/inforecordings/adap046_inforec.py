from jaratoolbox import celldatabase

subject = 'adap046'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-30',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior','medial:1,2,3,4', 'lateral:5,6,7,8'])
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


exp1 = celldatabase.Experiment(subject,
                               '2017-05-31',
                               brainarea='leftAStr',
                               info=['medialDiI', 'facingPosterior','medial:1,2,3,4', 'lateral:None'])
experiments.append(exp1)

#1800, 2000, 2100, 2200, 2300, 2400, 2500, 2600um not sound responsive
exp1.add_site(2660, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('13-22-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT5-8 offset response 
exp1.add_session('13-25-04', 'a', 'tc', 'am_tuning_curve') 

exp1.add_site(2780, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('13-45-12', None, 'noiseburst', 'am_tuning_curve') #ref to chan32 in TT3, TT1,5-8 offset response 
exp1.add_session('13-48-23', 'b', 'tc', 'am_tuning_curve') 

#pretty quiet at 2850, 2900um
exp1.add_site(2950, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('14-12-19', None, 'noiseburst', 'am_tuning_curve') #ref to chan32 in TT3, TT5-8 same offset response 
exp1.add_session('14-13-57', 'c', 'tc', 'am_tuning_curve') 

#pretty quiet at and pass 3000um except the same very late offset response
#exp1.add_site(3070, tetrodes=[1,2,3,4,5,6,7,8])
#exp1.add_session('14-40-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan32 in TT3, TT5-8 offset response 


exp2 = celldatabase.Experiment(subject,
                               '2017-06-01',
                               brainarea='rightAStr',
                               info=['posteriorDiD', 'facingPosterior','medial:3,4', 'lateral:5,6,7,8'])
experiments.append(exp2)

exp2.add_site(2280, tetrodes=[3,4,5,6,7,8])
exp2.add_session('12-46-02', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT4&7 responsive 
exp2.add_session('12-47-35', 'a', 'tc', 'am_tuning_curve') 

exp2.add_site(2350, tetrodes=[3,4,5,6,7,8])
exp2.add_session('13-06-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT3&7 responsive 
exp2.add_session('13-08-01', 'b', 'tc', 'am_tuning_curve') 

exp2.add_site(2430, tetrodes=[3,4,5,6,7,8])
exp2.add_session('13-26-14', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT5&6 responsive 
exp2.add_session('13-28-01', 'c', 'tc', 'am_tuning_curve') 

exp2.add_site(2510, tetrodes=[3,4,5,6,7,8])
exp2.add_session('13-47-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5&7 responsive 
#exp2.add_session('13-51-26', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-52-57', 'd', 'tc', 'am_tuning_curve') 

exp2.add_site(2600, tetrodes=[3,4,5,6,7,8])
exp2.add_session('14-40-55', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5&7 responsive 
exp2.add_session('14-42-36', 'e', 'tc', 'am_tuning_curve') 

exp2.add_site(2830, tetrodes=[3,4,5,6,7,8])
exp2.add_session('15-47-40', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT3&7 weakly responsive 
exp2.add_session('15-50-06', 'f', 'tc', 'am_tuning_curve') 

'''
# -- 20170615 Histology shows this site too posterior -- #
exp3 = celldatabase.Experiment(subject,
                               '2017-06-02',
                               brainarea='leftAStr',
                               info=['posteriorDiD', 'facingPosterior'])
experiments.append(exp3)

#1800, 2000, 2100, 2200, 2300, 2400, 2500, 2600um not sound responsive
# very quiet the whole way down?! went all the way down to 3600um very little spiking and no sound response


# -- 20170615 Histology shows this site may be from hippocampus -- #
exp4 = celldatabase.Experiment(subject,
                               '2017-06-05',
                               brainarea='leftAStr',
                               info=['posterior-medialDiI', 'facingPosterior'])
experiments.append(exp4)

exp4.add_site(2330, tetrodes=[7,8])
exp4.add_session('14-32-02', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT7 sound responsive 
exp4.add_session('14-34-30', 'a', 'tc', 'am_tuning_curve') 
# went down to 3200um no more sound response

# -- 20170615 Histology shows this site was in AStr, not sure why didnot get sound response -- #
exp5 = celldatabase.Experiment(subject,
                               '2017-06-06',
                               brainarea='leftAStr',
                               info=['medialDiD', 'facingPosterior'])
experiments.append(exp5)

#exp5.add_site(2270, tetrodes=[1,2,3,4])
#exp5.add_session('14-32-45', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7,no obvious sound response
#exp5.add_session('14-34-44', 'a', 'tc', 'am_tuning_curve') #Tuning with chord 6.2-19.2kHz, TT2 show tuned response
#exp5.add_session('14-38-23', 'b', 'tc', 'am_tuning_curve') #no obvious tuning?!

# went down to 3300um no sound response, at 3200um or so suddenly saw high spikes very active, may have gotten to amygdala??
#exp5.add_site(3230, tetrodes=[1,2,3,4,5,6,7,8])
#exp5.add_session('15-45-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, activity looked very different than before, large spikes a bit rhythmic, slightly suppressed by sound.
'''

exp6 = celldatabase.Experiment(subject,
                               '2017-06-06',
                               brainarea='leftAStr',
                               info=['medial-anteriorDiI', 'facingPosterior','medial:5,6,7,8', 'lateral:1,2,3,4'])
experiments.append(exp6)
exp6.add_site(2680, tetrodes=[1,2,3,4,5,6])
#exp6.add_session('16-45-04', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, very slight sound suppression on TT1?
exp6.add_session('16-47-55', 'c', 'tc', 'am_tuning_curve') #TT4 weird tuning?
exp6.add_session('17-06-06', None, 'noiseburst', 'am_tuning_curve') #TT4 offset respnose?

exp6.add_site(2910, tetrodes=[1,2,3,4,5])
#exp6.add_session('17-34-03', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT4 sound responsive
exp6.add_session('17-39-05', None, 'noiseburst', 'am_tuning_curve') #may have lost the very responsive cell, TT4 now only weakly sound responsive
exp6.add_session('17-40-14', 'd', 'tc', 'am_tuning_curve') #TT4 weird tuning?


exp7 = celldatabase.Experiment(subject,
                               '2017-06-07',
                               brainarea='leftAStr',
                               info=['anteriorDiD', 'facingPosterior','medial:5,6,7,8', 'lateral:1,2,3,4'])
experiments.append(exp7)
exp7.add_site(2490, tetrodes=[1,2,3,4,5,6])
exp7.add_session('13-56-20', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, sound response on TT2,4,6
exp7.add_session('13-58-02', 'a', 'tc', 'am_tuning_curve') 

exp7.add_site(2560, tetrodes=[1,2,3,4,5,6])
#exp7.add_session('14-16-21', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, sound response on TT4,5
exp7.add_session('14-17-57', 'b', 'tc', 'am_tuning_curve') 
exp7.add_session('14-34-48', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(2620, tetrodes=[1,2,3,4,5,6,8])
exp7.add_session('14-38-29', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, sound response on TT1-4
exp7.add_session('14-40-08', 'c', 'tc', 'am_tuning_curve')
 
exp7.add_site(2690, tetrodes=[1,2,3,4,5,6,8])
exp7.add_session('15-01-51', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, sound response on TT2-4
exp7.add_session('15-30-07', 'd', 'tc', 'am_tuning_curve') 

exp7.add_site(2750, tetrodes=[1,2,3,4,5,6])
exp7.add_session('15-49-05', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, sound response on TT1-4
exp7.add_session('15-51-18', 'e', 'tc', 'am_tuning_curve') 
exp7.add_session('16-10-22', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(2810, tetrodes=[1,2,3,4,5,6])
exp7.add_session('16-17-08', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, sound response on TT1-4
exp7.add_session('16-20-38', 'f', 'tc', 'am_tuning_curve') 

exp7.add_site(2900, tetrodes=[1,2,3,4,5,6])
exp7.add_session('16-39-01', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, sound response on TT1-4
exp7.add_session('16-40-50', 'g', 'tc', 'am_tuning_curve') 
