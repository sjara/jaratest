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



exp1 = celldatabase.Experiment(subject,
                               '2017-05-01',
                               brainarea='leftAStr',
                               info=['medialDiD', 'facingPosterior'])
experiments.append(exp1)

#2200, 2300, 2400, 2500 no noise response

exp1.add_site(2550, tetrodes=[1,2,3,4,5,6])
exp1.add_session('12-32-21', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT1 (most lateral) noise responsive
exp1.add_session('12-34-29', 'a', 'tc', 'am_tuning_curve') #ref to chan11 in TT8, TT1 tuned, moving on. 

#2650, 2750um no noise response
exp1.add_site(2810, tetrodes=[1,2,3,4,5,6,7,8]) #at 2800um TTs 5&6 came on.
exp1.add_session('13-06-05', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT5&6 offset responsive
exp1.add_session('13-08-01', 'b', 'tc', 'am_tuning_curve') 

#2900,3000,3100,3200,3300,3400,3500,3600, 3700um all very quiet



exp2 = celldatabase.Experiment(subject,
                               '2017-05-01',
                               brainarea='rightAStr',
                               info=['posteriorDiD', 'facingPosterior'])
experiments.append(exp2)
exp2.add_site(1954, tetrodes=[1,2,3,4,5,7,8]) #at 1800um TT1,2(medial),4 LFP very rhythmic
exp2.add_session('14-06-28', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1,2,4 responsive
exp2.add_session('14-12-11', 'c', 'tc', 'am_tuning_curve') 

exp2.add_site(2050, tetrodes=[1,2,3,4,5,6,8]) #TT2 LFP very rhythmic 
exp2.add_session('14-31-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT1,2,4,6 responsive
exp2.add_session('14-33-34', 'd', 'tc', 'am_tuning_curve') 

exp2.add_site(2112, tetrodes=[1,2,3,4,5,6,8]) #TT2&4 LFP very rhythmic 
exp2.add_session('14-54-53', None, 'noiseburst', 'am_tuning_curve') #ref to chan12 in TT7, TT1,2,4,6 responsive
exp2.add_session('14-59-04', 'e', 'tc', 'am_tuning_curve') 

exp2.add_site(2200, tetrodes=[1,2,3,4,5,6,8]) #TT2&4 LFP very rhythmic 
exp2.add_session('15-19-05', None, 'noiseburst', 'am_tuning_curve') #ref to chan5 in TT7, TT1,2,3,4,6 weakly responsive
exp2.add_session('15-22-04', 'f', 'tc', 'am_tuning_curve') 

exp2.add_site(2300, tetrodes=[1,2,3,4,5,6,8]) #TT2&4 LFP very rhythmic 
exp2.add_session('15-42-13', None, 'noiseburst', 'am_tuning_curve') #ref to chan5 in TT7, TT1,2,3,4,5,6 responsive
exp2.add_session('15-44-17', 'g', 'tc', 'am_tuning_curve') 

exp2.add_site(2400, tetrodes=[1,2,3,4,5,6,7,8]) #TT2&4&6 LFP very rhythmic 
exp2.add_session('16-04-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan11/4 in TT8, allTTs responsive??
exp2.add_session('16-12-25', 'h', 'tc', 'am_tuning_curve') 

exp2.add_site(2600, tetrodes=[1,2,3,4,5,6,7,8]) #TT2&4&6 LFP very rhythmic 
exp2.add_session('16-39-49', None, 'noiseburst', 'am_tuning_curve') #ref to chan11/4 in TT8, allTTs responsive??
exp2.add_session('16-41-26', 'i', 'tc', 'am_tuning_curve') 

exp2.add_site(2800, tetrodes=[1,2,3,4,5,6,7,8]) #TT1,2 LFP rhythmic 
exp2.add_session('17-07-52', None, 'noiseburst', 'am_tuning_curve') #ref to chan2 in TT6
exp2.add_session('17-09-48', 'j', 'tc', 'laser_tuning_curve') 

exp2.add_site(2950, tetrodes=[1,2,3,4,5,6,7,8]) #TT1,2 LFP rhythmic 
exp2.add_session('17-34-06', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6
exp2.add_session('17-35-44', 'k', 'tc', 'am_tuning_curve') 

#3000, 3100 very weak, inconsistent sound response. stop and pull up.

'''
exp3 = celldatabase.Experiment(subject,
                               '2017-05-01',
                               brainarea='leftAStr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp3)

#2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600um, TT1&2 have sparse spikes that died away quickly, all the way down no sites were sound responsive
'''

exp4 = celldatabase.Experiment(subject,
                               '2017-05-02',
                               brainarea='leftAStr',
                               info=['posteriorDiI', 'facingPosterior'])
experiments.append(exp4)

exp4.add_site(1450, tetrodes=[1,2,6,7,8]) #TT8 LFP rhythmic
exp4.add_session('13-03-22', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT8 (most medial) responsive
exp4.add_session('13-06-12', 'a', 'tc', 'am_tuning_curve') 

exp4.add_site(1550, tetrodes=[6,7,8]) #TT8 LFP rhythmic
exp4.add_session('13-26-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT8 (most medial) responsive
exp4.add_session('13-28-26', 'b', 'tc', 'am_tuning_curve') 

exp4.add_site(1650, tetrodes=[1,5,6,7,8]) #TT8 LFP rhythmic
exp4.add_session('13-47-46', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT6-8 responsive
exp4.add_session('13-50-09', 'c', 'tc', 'am_tuning_curve') 

exp4.add_site(1750, tetrodes=[4,5,6,7,8]) #TT5-8 LFP rhythmic
exp4.add_session('14-24-31', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT5-8 responsive
exp4.add_session('14-26-24', 'd', 'tc', 'am_tuning_curve') 

exp4.add_site(1860, tetrodes=[4,5,6,7,8]) #TT4-8 LFP rhythmic
exp4.add_session('14-47-18', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5-8 responsive
exp4.add_session('14-49-01', 'e', 'tc', 'am_tuning_curve') 

exp4.add_site(1950, tetrodes=[2,3,4,5,6,7,8]) #TT4-8 LFP rhythmic
exp4.add_session('15-11-23', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT2-8 responsive
exp4.add_session('15-13-09', 'f', 'tc', 'am_tuning_curve') 

exp4.add_site(2050, tetrodes=[2,3,4,5,6,7,8]) #TT5-8 LFP rhythmic
exp4.add_session('15-32-28', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT4-6 responsive
exp4.add_session('15-34-24', 'g', 'tc', 'am_tuning_curve') 

exp4.add_site(2150, tetrodes=[1,3,4,5,6,7,8]) #TT5-8 LFP rhythmic
exp4.add_session('15-58-11', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 in TT2, TT3-8 responsive
exp4.add_session('16-00-04', 'h', 'tc', 'am_tuning_curve') 

exp4.add_site(2250, tetrodes=[1,3,4,5,6,7,8]) #TT4-8 LFP rhythmic
exp4.add_session('16-20-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan26 in TT2, TT3-7 responsive
exp4.add_session('16-23-30', 'i', 'tc', 'am_tuning_curve') 

exp4.add_site(2350, tetrodes=[1,2,3,4,5,6,7]) #TT4-8 LFP rhythmic
exp4.add_session('16-41-35', None, 'noiseburst', 'am_tuning_curve') #ref to chan4 in TT8, TT2-7 responsive
exp4.add_session('16-44-25', 'j', 'tc', 'am_tuning_curve') 

exp4.add_site(2450, tetrodes=[1,2,3,4,5,6,7]) #TT4-8 LFP rhythmic
exp4.add_session('17-01-33', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT1-6 responsive
exp4.add_session('17-03-15', 'k', 'tc', 'am_tuning_curve') 

exp4.add_site(2600, tetrodes=[1,2,3,4,5,6,7]) #TT4-8 LFP rhythmic
exp4.add_session('17-21-55', None, 'noiseburst', 'am_tuning_curve') #ref to chan11 in TT8, TT2-5 responsive
exp4.add_session('17-23-19', 'l', 'tc', 'am_tuning_curve') 
