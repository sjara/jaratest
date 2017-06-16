from jaratoolbox import celldatabase

subject = 'adap044'
experiments = []
#craniotomy AP -1 to -2mm, ML 2.9 to 4.1mm 
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-16',
                               brainarea='rightAStr',
                               info=['medialDiI', 'facingPosterior', 'medial:1,2','lateral:3,4,5,6'])
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


exp1 = celldatabase.Experiment(subject,
                               '2017-05-17',
                               brainarea='rightAStr',
                               info=['3/4posteriorDiD', 'facingPosterior','medial:1,2,3,4','lateral:5,6,7,8'])
experiments.append(exp1)

#1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300um not sound responsive
exp1.add_site(2410, tetrodes=[2,4,5,6,7,8])
exp1.add_session('13-12-49', None, 'noiseburst', 'am_tuning_curve') #ref to chan21 in TT1, TT2&4 weakly sound responsive 
exp1.add_session('13-15-13', 'a', 'tc', 'am_tuning_curve') 

exp1.add_site(2500, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-43-17', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT1,3&4 sound responsive 
exp1.add_session('13-44-50', 'b', 'tc', 'am_tuning_curve') 

exp1.add_site(2570, tetrodes=[1,2,3,4,5,7])
exp1.add_session('14-08-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan10 in TT6, TT1,3&4 sound responsive 
exp1.add_session('14-11-26', 'c', 'tc', 'am_tuning_curve') 

exp1.add_site(2640, tetrodes=[1,2,3,4,5,7,8])
exp1.add_session('14-34-02', None, 'noiseburst', 'am_tuning_curve') #ref to chan10 in TT6, TT1,3&4 sound responsive 
exp1.add_session('14-36-48', 'd', 'tc', 'am_tuning_curve') 

exp1.add_site(2720, tetrodes=[1,2,3,4,5,7,8])
exp1.add_session('15-02-17', None, 'noiseburst', 'am_tuning_curve') #ref to chan10 in TT6, TT3 weakly sound responsive 
exp1.add_session('15-04-36', 'e', 'tc', 'am_tuning_curve') 

exp1.add_site(2800, tetrodes=[1,2,3,4,8])
#exp1.add_session('15-25-02', None, 'noiseburst', 'am_tuning_curve') #ref to chan10 in TT6, TT3 sound responsive 
exp1.add_session('15-27-18', 'f', 'tc', 'am_tuning_curve') 
exp1.add_session('15-47-10', None, 'noiseburst', 'am_tuning_curve')

exp1.add_site(2900, tetrodes=[1,2,3,4,5,6])
exp1.add_session('15-53-07', None, 'noiseburst', 'am_tuning_curve') #ref to chan4 in TT8, TT2&4 sound responsive 
exp1.add_session('15-55-44', 'g', 'tc', 'am_tuning_curve') 

exp1.add_site(3000, tetrodes=[1,2,3,4,5,6])
exp1.add_session('16-19-15', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT1,2,3,4,6 sound responsive 
exp1.add_session('16-21-42', 'h', 'tc', 'am_tuning_curve') 

exp1.add_site(3120, tetrodes=[1,2,3,4,5,6])
#exp1.add_session('16-44-53', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT1-6 sound responsive 
exp1.add_session('16-46-38', 'i', 'tc', 'am_tuning_curve') 
exp1.add_session('17-03-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT1-6 sound responsive 


exp2 = celldatabase.Experiment(subject,
                               '2017-05-18',
                               brainarea='leftAStr',
                               info=['posteriorDiI', 'facingPosterior','medial:1,2,3,4', 'lateral:None'])
experiments.append(exp2)

'''
exp2.add_site(1700, tetrodes=[1,3,4,5,6,7,8]) #T7&8 LFP rhythmic
exp2.add_session('13-50-58', None, 'noiseburst', 'am_tuning_curve') #ref to chan22 in TT2, TT7&8 sound responsive - may have been in cortex or hippocampus? 
exp2.add_session('13-54-18', 'a', 'tc', 'am_tuning_curve') 
'''
#It's pretty quiet the whole way down for this penetration
#1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500um not sound responsive
exp2.add_site(2580, tetrodes=[1,2,3,4]) #T7&8 LFP not rhythmic now
exp2.add_session('14-51-24', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT4 weakly sound responsive 
exp2.add_session('14-54-19', 'b', 'tc', 'am_tuning_curve') 

#exp2.add_site(2760, tetrodes=[1,2,3,4,5,6,7,8]) #T7&8 LFP not rhythmic now
#exp2.add_session('15-34-45', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT2&4 weak sound responsive 
#exp2.add_session('15-38-48', 'c', 'tc', 'am_tuning_curve') #no tuning, have lost the cell

#kept going and test sound response every 50um or so. pretty quiet. went down to 3000um started to see more activity, but no sound response, end at 3400um.


exp3 = celldatabase.Experiment(subject,
                               '2017-05-19',
                               brainarea='leftAStr',
                               info=['medial-posteriorDiD', 'facingPosterior','medial:5,6','lateral:1,2,3,4'])
experiments.append(exp3)


exp3.add_site(2450, tetrodes=[1,2,3,4,5,6]) 
exp3.add_session('09-53-19', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT2,4,6 sound responsive  
exp3.add_session('09-57-11', 'a', 'tc', 'am_tuning_curve') 

exp3.add_site(2520, tetrodes=[1,2,3,4,5,6,8]) 
exp3.add_session('10-20-08', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT2,4 sound responsive  
exp3.add_session('10-21-28', 'b', 'tc', 'am_tuning_curve') 

exp3.add_site(2600, tetrodes=[1,2,3,4,6]) 
exp3.add_session('10-39-17', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT2,4,6 sound responsive  
exp3.add_session('10-41-18', 'c', 'tc', 'am_tuning_curve') 

exp3.add_site(2670, tetrodes=[1,2,3,4,5,6,8]) 
#exp3.add_session('11-00-00', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT3,4,6 sound responsive  
exp3.add_session('11-01-50', 'd', 'tc', 'am_tuning_curve') #TT1,2,3,4,6,8 tuned
exp3.add_session('11-17-38', None, 'noiseburst', 'am_tuning_curve')

exp3.add_site(2734, tetrodes=[1,2,3,4,5,6,8]) 
exp3.add_session('11-21-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan6 in TT7, TT2,3,4 sound responsive  
exp3.add_session('11-23-13', 'e', 'tc', 'am_tuning_curve')

exp3.add_site(2800, tetrodes=[1,2,3,4,5,6,8]) 
exp3.add_session('11-40-04', None, 'noiseburst', 'am_tuning_curve') #ref to chan6 in TT7, TT2,3,4,8 sound responsive  
exp3.add_session('11-43-08', 'f', 'tc', 'am_tuning_curve')

exp3.add_site(2870, tetrodes=[1,2,3,4,6,7,8]) 
exp3.add_session('12-06-16', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 in TT5, TT1,2,3,4,8 sound responsive  
exp3.add_session('12-07-49', 'g', 'tc', 'am_tuning_curve')

exp3.add_site(2930, tetrodes=[1,2,3,4,6,7,8]) 
exp3.add_session('12-32-41', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 in TT5, TT1,2,3,4,8 sound responsive  
exp3.add_session('12-34-19', 'h', 'tc', 'am_tuning_curve')

exp3.add_site(3000, tetrodes=[1,2,3,4,5,6,7,8]) 
exp3.add_session('12-53-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan8 in TT5, TT4,7,8 sound responsive  
exp3.add_session('12-56-01', 'i', 'tc', 'am_tuning_curve')


exp4 = celldatabase.Experiment(subject,
                               '2017-05-22',
                               brainarea='rightAStr',
                               info=['medialposteriorDiI', 'facingPosterior','medial:1,2,3,4','lateral:5,6,7,8'])
experiments.append(exp4)

exp4.add_site(2300, tetrodes=[1,2,3,4,5,6,8])
#exp4.add_session('13-56-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT4 sound responsive 
#exp4.add_session('13-58-41', 'a', 'tc', 'am_tuning_curve') 
#exp4.add_session('14-14-26', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, all TTs sound responsive?? ref may be sound-responsive
exp4.add_session('14-16-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT2,3,4,6 sound responsive
exp4.add_session('14-18-30', 'b', 'tc', 'am_tuning_curve') 

exp4.add_site(2450, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('14-41-39', None, 'noiseburst', 'am_tuning_curve') #ref to chan15 in TT7, TT2,3,4,6 sound responsive 
exp4.add_session('14-44-41', 'c', 'tc', 'am_tuning_curve') 

exp4.add_site(2600, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('15-06-55', None, 'noiseburst', 'am_tuning_curve') #ref to chan15 in TT7, TT1-6 sound responsive 
exp4.add_session('15-09-25', 'd', 'tc', 'am_tuning_curve') 

exp4.add_site(2750, tetrodes=[1,2,3,4,5,6,8])
exp4.add_session('15-28-54', None, 'noiseburst', 'am_tuning_curve') #ref to chan15 in TT7, TT1-6 sound responsive 
exp4.add_session('15-32-54', 'e', 'tc', 'am_tuning_curve') 

exp4.add_site(2850, tetrodes=[1,2,3,4,5,6])
exp4.add_session('16-01-25', None, 'noiseburst', 'am_tuning_curve') #ref to chan15 in TT7, TT1-6 sound responsive 
exp4.add_session('16-02-55', 'f', 'tc', 'am_tuning_curve') 


exp5 = celldatabase.Experiment(subject,
                               '2017-05-23',
                               brainarea='leftAStr',
                               info=['medialDiI', 'facingPosterior','medial:3,4,5,6', 'lateral:1,2'])
experiments.append(exp5)

exp5.add_site(2320, tetrodes=[1,2,3,4,5,6,7,8])
exp5.add_session('13-54-58', None, 'noiseburst', 'am_tuning_curve') #ref to chan7 in TT8, TT5 interesting offset response
exp5.add_session('14-00-15', 'a', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2470, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('14-24-07', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT4&8 responsive
exp5.add_session('14-25-48', 'b', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2530, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('14-50-43', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2,3,4&8 responsive
exp5.add_session('14-53-48', 'c', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2620, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('15-18-26', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT4,7&8 responsive
exp5.add_session('15-19-57', 'd', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2700, tetrodes=[1,2,3,4,6,7,8])
exp5.add_session('15-48-16', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT4,7&8 responsive
exp5.add_session('15-50-42', 'e', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2800, tetrodes=[1,2,3,4,5,6,7,8])
exp5.add_session('16-14-54', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2-8 responsive
exp5.add_session('16-19-51', 'f', 'tc', 'am_tuning_curve') #may have lost some cell in TT5

exp5.add_site(2880, tetrodes=[1,2,3,4,5,6,7,8])
exp5.add_session('16-38-44', None, 'noiseburst', 'am_tuning_curve') #ref to chan14 in TT5, TT2-8 responsive
exp5.add_session('16-40-00', 'g', 'tc', 'am_tuning_curve') #may have lost some cell in TT5
