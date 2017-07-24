from jaratoolbox import celldatabase

subject = 'adap041'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-07-07',
                               brainarea='rightAStr',
                               info=['anteriorDiI', 'facingPosterior','medial:1,2,3,4', 'lateral:5,6'])
experiments.append(exp0)

#Mouse on the rig at 1339hrs, waiting 10 mins for brain to settle
#Tetrodes at 2002um - had to remove some membrane from brain surface

exp0.add_site(2002, tetrodes=range(1, 9))
exp0.add_session('13-51-08', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-53-42', 'a', 'tc', 'am_tuning_curve')

exp0.add_site(2110, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 4])
exp0.add_session('14-22-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-24-07', 'b', 'tc', 'am_tuning_curve')

exp0.add_site(2200, tetrodes=range(1, 9))
exp0.add_session('14-52-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-54-58', 'c', 'tc', 'am_tuning_curve')

exp0.add_site(2309, tetrodes=range(1, 9)).remove_tetrodes([2, 3, 4])
exp0.add_session('15-18-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-27-19', 'd', 'tc', 'am_tuning_curve')

exp0.add_site(2411, tetrodes=range(1, 9)).remove_tetrodes([4])
exp0.add_session('15-52-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-56-28', 'e', 'tc', 'am_tuning_curve')

exp0.add_site(2518, tetrodes=range(1, 9))
exp0.add_session('16-23-27', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-26-18', 'f', 'tc', 'am_tuning_curve')

exp0.add_site(2602, tetrodes=range(1, 9))
exp0.add_session('17-03-57', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-05-58', 'g', 'tc', 'am_tuning_curve')

exp0.add_site(2725, tetrodes=range(1, 9))
exp0.add_session('17-39-49', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-41-57', 'h', 'tc', 'am_tuning_curve')

exp0.add_site(2824, tetrodes=range(1, 9))
exp0.add_session('18-04-36', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-07-13', 'i', 'tc', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject,
                               '2017-07-08',
                               brainarea='leftAStr',
                               info=['anteriorDiI', 'facingPosterior','medial:7,8', 'lateral:3,4,5,6'])
experiments.append(exp1)

#Mouse on the rig at 2012hrs, waiting 10 mins for brain to settle
#Tetrodes at 1969um - had to remove some membrane from brain surface

exp1.add_site(2055, tetrodes=range(1, 9))
exp1.add_session('20-33-05', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('20-37-11', 'a', 'tc', 'am_tuning_curve')

exp1.add_site(2153, tetrodes=range(1, 9))
exp1.add_session('21-00-12', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('21-02-33', 'b', 'tc', 'am_tuning_curve')

exp1.add_site(2253, tetrodes=range(1, 9))
exp1.add_session('21-36-58', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('21-40-02', 'c', 'tc', 'am_tuning_curve')

exp1.add_site(2403, tetrodes=range(1, 9))
exp1.add_session('22-14-22', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('22-18-02', 'd', 'tc', 'am_tuning_curve')

exp1.add_site(2550, tetrodes=range(1, 9))
exp1.add_session('22-41-03', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('22-43-15', 'e', 'tc', 'am_tuning_curve')

# exp1.add_site(2656, tetrodes=range(1, 9))
# exp1.add_session('23-08-07', None, 'noiseburst', 'am_tuning_curve')
#No sound response here

exp1.add_site(2703, tetrodes=range(1, 9))
exp1.add_session('23-18-45', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('23-21-00', 'f', 'tc', 'am_tuning_curve')

site = exp1.add_site(2858, tetrodes=range(1, 9))
exp1.add_session('23-59-01', None, 'noiseburst', 'am_tuning_curve')
site.date = '2017-07-09'
exp1.add_session('00-01-41', 'a', 'tc', 'am_tuning_curve')

# site = exp1.add_site(2979, tetrodes=range(1, 9))
# site.date = '2017-07-09'
# exp1.add_session('00-32-27', None, 'noiseburst', 'am_tuning_curve')
#Nothing here, removing for the day


exp2 = celldatabase.Experiment(subject,
                               '2017-07-09',
                               brainarea='rightAStr',
                               info=['centralDiD', 'facingPosterior', 'medial:None', 'lateral:None'])
experiments.append(exp2)

#Mouse on the rig at 1934hrs, waiting 10 mins for brain to settle
#Tetrodes at 1995um - had to remove some membrane from brain surface

#No neurons down to 2741??
exp2.add_site(2741, tetrodes=range(1, 9)).remove_tetrodes([2])
exp2.add_session('20-24-33', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('20-27-15', 'b', 'tc', 'am_tuning_curve')

exp2.add_site(2872, tetrodes=range(1, 9)).remove_tetrodes([1])
exp2.add_session('21-03-04', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('21-05-00', 'c', 'tc', 'am_tuning_curve')

exp2.add_site(2955, tetrodes=range(1, 9))
exp2.add_session('21-28-31', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('21-30-37', 'd', 'tc', 'am_tuning_curve')
 #Getting worried about being in amygdala here. I am going to remove the trodes and do the other side of the brain tonight

 #Looks like I may have made a zeroing error on the experiment above. When I removed the tetrodes, they came out at 1000um. So all distances above could be 1000um shallower than I recorded... I still can't do another penetration right now and say for sure where I am, so I will still move to the other side.



exp3 = celldatabase.Experiment(subject,
                               '2017-07-09',
                               brainarea='leftAStr',
                               info=['centralDiD', 'facingPosterior', 'medial:None', 'lateral:5,6,7,8'])
experiments.append(exp3)

#Mouse on the rig at 2209hrs, waiting 10 mins for brain to settle
#Tetrodes at 1995um - had to remove some membrane from brain surface

exp3.add_site(2056, tetrodes=range(1, 9))
exp3.add_session('22-20-35', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('22-22-44', 'e', 'tc', 'am_tuning_curve')

exp3.add_site(2158, tetrodes=range(1, 9))
exp3.add_session('22-52-49', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('22-54-49', 'f', 'tc', 'am_tuning_curve')

exp3.add_site(2294, tetrodes=range(1, 9))
exp3.add_session('23-30-35', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('23-32-37', 'g', 'tc', 'am_tuning_curve')

site = exp3.add_site(2394, tetrodes=range(1, 9))
site.date = '2017-07-10'
exp3.add_session('00-06-39', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('00-09-39', 'a', 'tc', 'am_tuning_curve')

site = exp3.add_site(2502, tetrodes=range(1, 9))
site.remove_tetrodes([7])
site.date = '2017-07-10'
exp3.add_session('00-39-30', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('00-41-25', 'b', 'tc', 'am_tuning_curve')

site = exp3.add_site(2605, tetrodes=range(1, 9))
site.date = '2017-07-10'
exp3.add_session('01-10-31', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('01-12-47', 'c', 'tc', 'am_tuning_curve')


exp4 = celldatabase.Experiment(subject,
                               '2017-07-10',
                               brainarea='rightAStr',
                               info=['centralDiO', 'facingPosterior','medial:1,2,3,4,5,6,7,8', 'lateral:None'])
experiments.append(exp4)

#Mouse on the rig at 2221hrs, waiting 10 mins for brain to settle
#Tetrodes at 1974um. When I was positioning the ground wire it slipped and drove some distance into the opposite (left) craniotomy. I removed it right away. There is some bleeding that I need to watch carefully. It seems to be mostly under control for now though.

exp4.add_site(2101, tetrodes=range(1, 9)).remove_tetrodes([4])
exp4.add_session('22-49-18', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('22-51-46', 'd', 'tc', 'am_tuning_curve')

# exp4.add_site(2190, tetrodes=range(1, 9))
# exp4.add_session('23-35-15', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('23-37-41', 'e', 'tc', 'am_tuning_curve')

exp4.add_site(2203, tetrodes=range(1, 9)).remove_tetrodes([4])
exp4.add_session('23-57-27', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('23-59-46','f', 'tc', 'am_tuning_curve')

site = exp4.add_site(2326, tetrodes=range(1, 9))
site.remove_tetrodes([4])
site.date = '2017-07-11'
exp4.add_session('00-25-09', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('00-27-08', 'a', 'tc', 'am_tuning_curve')

site = exp4.add_site(2402, tetrodes=range(1, 9))
site.date = '2017-07-11'
site.remove_tetrodes([4])
exp4.add_session('00-54-08', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('00-56-19', 'b', 'tc', 'am_tuning_curve')

site = exp4.add_site(2542, tetrodes=range(1, 9))
site.date = '2017-07-11'
site.remove_tetrodes([4])
exp4.add_session('01-31-02', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('01-33-12', 'c', 'tc', 'am_tuning_curve')

# site = exp4.add_site(2647, tetrodes=range(1, 9))
# site.date = '2017-07-11'
# exp4.add_session('01-55-41', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('01-58-04', 'd', 'tc', 'am_tuning_curve') #Mysterious problems at the end of the recording, and I think I left the beahvior running past the ephys - too many trials

#I am needing to remove the electrodes to see what is the problem, so I will stop the recording on this side. 




exp5 = celldatabase.Experiment(subject,
                               '2017-07-16',
                               brainarea='rightAStr',
                               info=['posteriorDiI', 'facingPosterior','medial:5,6', 'lateral:None'])
#I broke shank 4 (TT7/8) off when I was applying the dye :(

experiments.append(exp5)

#Mouse on the rig at 1209hrs, waiting 10 mins for brain to settle
#Tetrodes at 1948um.

exp5.add_site(2723, tetrodes=range(1, 9))
exp5.add_session('13-34-06', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('13-43-20', 'a', 'tc', 'am_tuning_curve')

exp5.add_site(2802, tetrodes=range(1, 9))
exp5.add_session('14-07-09', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('14-09-19', 'b', 'tc', 'am_tuning_curve')

exp5.add_site(2891, tetrodes=range(1, 9))
exp5.add_session('14-36-11', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('14-38-10', 'c', 'tc', 'am_tuning_curve')

#exp5.add_site(3023, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3, 4])
#exp5.add_session('15-04-12', None, 'noiseburst', 'am_tuning_curve') #No more sound response - I am done here for the day

exp5.add_site(2834, tetrodes=range(1, 9)).remove_tetrodes([1, 4])
exp5.add_session('15-22-10', None, 'noiseburst', 'am_tuning_curve') #On the way out I discovered some neurons
exp5.add_session('15-24-06', 'd', 'tc', 'am_tuning_curve') #Why not?

#exp5.add_site(2641, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 3, 4])
#exp5.add_session('15-46-46', None, 'noiseburst', 'am_tuning_curve') #More neurons but not sound responsive, done for real now

exp6 = celldatabase.Experiment(subject,
                               '2017-07-18',
                               brainarea='rightAStr',
                               info=['posteriorDiD', 'facingPosterior','medial:None','lateral:None'])

experiments.append(exp6)

#Mouse on the rig at 1241hrs, waiting 10 mins for brain to settle
#Tetrodes at 2011um.
exp6.add_site(2011, tetrodes=range(1, 9))
exp6.add_session('12-55-53', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('12-58-21', 'a', 'tc', 'am_tuning_curve')

exp6.add_site(2097, tetrodes=range(1, 9)).remove_tetrodes([5])
exp6.add_session('13-21-08', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('13-23-27', 'b', 'tc', 'am_tuning_curve')

exp6.add_site(2186, tetrodes=range(1, 9))
exp6.add_session('13-48-57', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('13-53-57', 'c', 'tc', 'am_tuning_curve')

exp6.add_site(2290, tetrodes=range(1, 9))
exp6.add_session('14-18-26', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('14-20-40', 'd', 'tc', 'am_tuning_curve')

exp6.add_site(2389, tetrodes=range(1, 9))
exp6.add_session('14-42-57', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('14-46-02', 'e', 'tc', 'am_tuning_curve')

exp6.add_site(2492, tetrodes=range(1, 9))
exp6.add_session('15-12-17', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-14-16', 'f', 'tc', 'am_tuning_curve')

#I have gone down to 2806 with no more responses, so I am going to stop recording on this penetration. 

exp7 = celldatabase.Experiment(subject,
                               '2017-07-19',
                               brainarea='rightAStr',
                               info=['posteriorDiO', 'facingPosterior','medial:None','lateral:None'])

experiments.append(exp7)

#Mouse on the rig at 1434hrs, waiting 10 mins for brain to settle
#Tetrodes at 1999um.
exp7.add_site(1999, tetrodes=range(1, 9)).remove_tetrodes([5])
exp7.add_session('14-50-39', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('14-52-45', 'a', 'tc', 'am_tuning_curve')

exp7.add_site(2102, tetrodes=range(1, 9))
exp7.add_session('15-15-57', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('15-18-00', 'b', 'tc', 'am_tuning_curve')

exp7.add_site(2205, tetrodes=range(1, 9))
exp7.add_session('15-40-34', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('15-43-03', 'c', 'tc', 'am_tuning_curve')

exp7.add_site(2309, tetrodes=range(1, 9))
exp7.add_session('16-05-40', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('16-08-14', 'd', 'tc', 'am_tuning_curve')

exp7.add_site(2406, tetrodes=range(1, 9))
exp7.add_session('16-32-49', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('16-34-47', 'e', 'tc', 'am_tuning_curve')

exp7.add_site(2525, tetrodes=range(1, 9))
exp7.add_session('16-52-56', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('16-55-00', 'f', 'tc', 'am_tuning_curve')
#I am removing the electrodes for the day
