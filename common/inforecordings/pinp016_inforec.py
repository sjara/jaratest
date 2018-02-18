from jaratoolbox import celldatabase

subject = 'pinp016'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-03-07',
                               brainarea='rightAC',
                               info=['medialDiI', 'facingLateral'])
experiments.append(exp0)

# exp0site0 = exp0.add_site(1391, tetrodes=range(1, 9))
# exp0site0.tetrodes.remove(1)
# exp0site0.tetrodes.remove(3)
# exp0site0.tetrodes.remove(4)
# exp0.add_session('13-56-23', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('13-59-17', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('14-01-57', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('14-06-13', 'a', 'am', 'am_tuning_curve') #Nothing really here

# exp0.add_site(1469, tetrodes=range(1, 9))
# exp0.add_session('14-25-26', None, 'noiseburst', 'am_tuning_curve')

# exp0site1 = exp0.add_site(1670, tetrodes=range(1, 9))
# exp0site1.tetrodes.remove(3)
# exp0.add_session('14-30-34', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('14-33-38', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('14-35-29', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('14-39-14', 'b', 'am', 'am_tuning_curve') #Still nothing much...

# exp0.add_site(2123, tetrodes=range(1, 9))
# exp0.add_session('14-58-17', None, 'noiseburst', 'am_tuning_curve')#responses
# exp0.add_session('15-00-20', None, 'laserpulse', 'am_tuning_curve')#responses
# exp0.add_session('15-02-54', None, 'lasertrain', 'am_tuning_curve')#responses
# exp0.add_session('15-05-49', 'c', 'am', 'am_tuning_curve')#pretty much everything is gone...

# exp0.add_site(2502, tetrodes=range(1, 9))
# exp0.add_session('15-25-21', None, 'noiseburst', 'am_tuning_curve') #Nothing here.
exp0.maxDepth = 2502

#I am removing the probes and calling it a day. I think I am too medial, and the probes are starting to look pretty weird.

exp1 = celldatabase.Experiment(subject,
                               '2017-03-08',
                               brainarea='rightAC',
                               info=['DiD', 'facingLateral'])
experiments.append(exp1)

# exp1.add_site(1201, tetrodes=range(1, 9))
# exp1.add_session('11-51-02', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(1304, tetrodes=range(1, 9))
# exp1.add_session('11-54-22', None, 'noiseburst', 'am_tuning_curve')

exp1.add_site(1601, tetrodes=[1, 2, 4, 5, 6, 7, 8])
exp1.add_session('11-57-19', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-59-45', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-02-38', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-05-25', 'a', 'am', 'am_tuning_curve')
exp1.add_session('12-23-38', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-25-29', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-31-53', 'b', 'tc', 'am_tuning_curve') #Mouse ripped plastic guard off at some point in this session. Also ground wire was out after this, not sure if grounding was ok. After lookingat the raster it looks like all is bad.
exp1.maxDepth = 1601

exp2 = celldatabase.Experiment(subject,
                               '2017-03-09',
                               brainarea='rightAC',
                               info=['lateralDiI', 'facingMedial'])
experiments.append(exp2)

exp2site0 = exp2.add_site(1153, tetrodes=[8])
exp2.add_session('12-14-24', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-16-44', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-18-05', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-20-56', 'a', 'am', 'am_tuning_curve')
exp2.add_session('12-36-53', 'b', 'tc', 'am_tuning_curve')
#I stopped and restarted the recording by accident, so I am going to move to a new site.

# exp2.add_site(1360, tetrodes=range(1, 9))
# exp2.add_session('13-15-25', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('13-18-03', None, 'laserpulse', 'am_tuning_curve')

# exp2.add_site(1457, tetrodes=range(1, 9))
# exp2.add_session('13-21-37', None, 'noiseburst', 'am_tuning_curve')

#Below is the only good site so far today
exp2.add_site(1904, tetrodes=range(1, 9))
exp2.add_session('13-33-35', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-36-23', None, 'laserpulse', 'am_tuning_curve') #good stuff
exp2.add_session('13-37-43', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-40-36', 'c', 'am', 'am_tuning_curve')
exp2.add_session('13-57-18', None, 'lasertrain2', 'am_tuning_curve')
exp2.add_session('14-00-24', 'd', 'tc', 'am_tuning_curve')
exp2.add_session('14-39-44', None, 'lasertrain3', 'am_tuning_curve')

exp2.add_site(2051, tetrodes=[1, 2, 3, 4, 5, 6, 8])
exp2.add_session('14-52-19', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-55-28', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-57-27', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-01-38', 'e', 'am', 'am_tuning_curve')
exp2.add_session('15-17-28', 'f', 'tc', 'am_tuning_curve') #opened door at 1178 trials to put saline
exp2.add_session('15-50-19', None, 'lasertrain2', 'am_tuning_curve')
#Done for the day
exp2.maxDepth = 2051

exp3 = celldatabase.Experiment(subject,
                               '2017-03-10',
                               brainarea='rightAC',
                               info=['extralateralDiD', 'facingMedial'])
experiments.append(exp3)

exp3.add_site(1811, tetrodes=[1, 2, 4, 6, 8])
exp3.add_session('13-24-58', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-27-11', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('13-28-47', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('13-31-56', 'a', 'am', 'am_tuning_curve')
exp3.add_session('13-49-24', 'b', 'tc', 'am_tuning_curve')
exp3.add_session('14-22-28', None, 'lasertrain2', 'am_tuning_curve')

exp3.add_site(1936, tetrodes=range(1, 9))
exp3.add_session('14-32-38', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-37-00', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('14-39-15', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('14-44-53', 'c', 'am', 'am_tuning_curve')
exp3.add_session('15-00-53', None, 'laserpulse2', 'am_tuning_curve')
exp3.add_session('15-03-35', 'd', 'tc', 'am_tuning_curve')

exp3.add_site(1970, tetrodes=range(1, 9))
exp3.add_session('15-37-41', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-39-11', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('15-40-29', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('15-43-57', 'e', 'am', 'am_tuning_curve') #Thresholds might be low for this data
exp3.add_session('15-59-00', None, 'lasertrain2', 'am_tuning_curve')

# exp3.add_site(2091, tetrodes=range(1, 9))
# exp3.add_session('16-09-06', None, 'noiseburst', 'am_tuning_curve') #Not getting any more sound responses, and the connector package is nearing the well. I am removing the probes now
exp3.maxDepth = 2091

exp4 = celldatabase.Experiment(subject,
                               '2017-03-14',
                               brainarea='rightThal',
                               info=['medialDiI', 'facingLateral'])
experiments.append(exp4)

# exp4.add_site(2765, tetrodes=range(1, 9))
# exp4.add_session('14-25-03', None, 'noiseburst', 'am_tuning_curve')

# exp4.add_site(2970, tetrodes=range(1, 9))
# exp4.add_session('14-27-14', None, 'noiseburst', 'am_tuning_curve')

# exp4.add_site(3203, tetrodes=range(1, 9))
# exp4.add_session('14-43-58', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('14-45-16', None, 'laserpulse', 'am_tuning_curve')

# exp4.add_site(3403, tetrodes=range(1, 9))
# exp4.add_session('14-51-16', None, 'noiseburst', 'am_tuning_curve') #good sound responses
# exp4.add_session('14-53-56', None, 'laserpulse', 'am_tuning_curve') #No laser responses

# exp4.add_site(3657, tetrodes=range(1, 9))
# exp4.add_session('14-59-38', None, 'laserpulse', 'am_tuning_curve')

exp4.add_site(3703, tetrodes=range(1, 9))
exp4.add_session('15-09-08', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('15-11-12', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('15-13-09', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('15-17-58', 'a', 'am', 'am_tuning_curve') #Really weird noise-like signals
exp4.add_session('15-41-36', 'b', 'am', 'am_tuning_curve')

exp4.add_session('15-57-38', None, 'lasertrain2', 'am_tuning_curve')
exp4.add_session('15-59-37', None, 'laserpulse2', 'am_tuning_curve')
exp4.add_session('16-03-26', 'c', 'tc', 'am_tuning_curve') #opened door at 964 trials
exp4.add_session('16-35-36', None, 'laserpulse3', 'am_tuning_curve')
exp4.add_session('16-37-06', None, 'lasertrain3', 'am_tuning_curve')


# exp4.add_site(3802, tetrodes=range(1, 9))
# exp4.add_session('16-42-04', None, 'noiseburst', 'am_tuning_curve')
# exp4.add_session('16-43-56', None, 'laserpulse', 'am_tuning_curve') #small sound responses, but no laser responses. Calling it a day
exp4.maxDepth = 3802


exp5 = celldatabase.Experiment(subject,
                               '2017-03-15',
                               brainarea='rightThal',
                               info=['medialDiD', 'facingLateral'])
experiments.append(exp5)

# exp5.add_site(3608, tetrodes=range(1, 9))
# exp5.add_session('14-25-46', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('14-27-42', None, 'laserpulse', 'am_tuning_curve')

# exp5.add_site(3766, tetrodes=range(1, 9))
# exp5.add_session('14-30-35', None, 'noiseburst', 'am_tuning_curve')
# exp5.add_session('14-31-52', None, 'laserpulse', 'am_tuning_curve')

# exp5.add_site(3613, tetrodes=range(1, 9))
# exp5.add_session('14-37-23', None, 'laserpulse', 'am_tuning_curve')
# exp5.add_session('14-39-21', None, 'noiseburst', 'am_tuning_curve')
#I am removing the electrodes at this point, the ground can be hit by the animal.
#I am going to do the Lateral DiI penetration now.
exp5.maxDepth = 3613

exp6 = celldatabase.Experiment(subject,
                               '2017-03-15',
                               brainarea='rightThal',
                               info=['lateralDiI', 'facingLateral'])
experiments.append(exp6)

# exp6.add_site(3553, tetrodes=range(1, 9))
# exp6.add_session('15-05-07', None, 'noiseburst', 'am_tuning_curve')
# exp6.add_session('15-06-49', None, 'laserpulse', 'am_tuning_curve')
# exp6.add_session('15-08-48', None, 'lasertrain', 'am_tuning_curve')

# exp6.add_site(3604, tetrodes=range(1, 9))
# exp6.add_session('15-19-45', None, 'noiseburst', 'am_tuning_curve')
# exp6.add_session('15-21-18', None, 'laserpulse', 'am_tuning_curve')

# exp6.add_site(3650, tetrodes=range(1, 9))
# exp6.add_session('15-23-31', None, 'laserpulse', 'am_tuning_curve')

# exp6.add_site(3676, tetrodes=range(1, 9))
# exp6.add_session('15-24-58', None, 'laserpulse', 'am_tuning_curve')

exp6site0 = exp6.add_site(3704, tetrodes=range(1, 9))
exp6site0.tetrodes.remove(7)
exp6.add_session('15-32-22', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('15-33-55', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-35-12', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('15-38-46', 'a', 'am', 'am_tuning_curve')
exp6.add_session('15-58-07', None, 'laserpulse2', 'am_tuning_curve')
exp6.add_session('16-00-24', None, 'lasertrain2', 'am_tuning_curve')
exp6.add_session('16-03-28', 'b', 'tc', 'am_tuning_curve') #had to wake the animal up at 1276 trials

exp6site1 = exp6.add_site(3797, tetrodes=range(1, 9))
exp6site1.tetrodes.remove(7)
exp6.add_session('16-36-16', None, 'laserpulse', 'am_tuning_curve')
exp6.add_session('16-37-53', None, 'lasertrain', 'am_tuning_curve')
exp6.add_session('16-39-52', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('16-41-48', 'c', 'am', 'am_tuning_curve')
exp6.add_session('17-00-23', None, 'laserpulse2', 'am_tuning_curve')
exp6.add_session('17-02-47', None, 'lasertrain2', 'am_tuning_curve')
exp6.add_session('17-05-48', 'd', 'tc', 'am_tuning_curve') #Woke mouse at 540 trials
exp6.maxDepth = 3797

exp7 = celldatabase.Experiment(subject,
                               '2017-03-16',
                               brainarea='rightThal',
                               info='extraLateralDiD') #probe facing medial.
experiments.append(exp7)
# exp7.add_site(3512, tetrodes=range(1, 9))
# exp7.add_session('14-32-29', None, 'laserpulse', 'am_tuning_curve') #artifacts from the laser for sure

# exp7.add_site(3670, tetrodes=range(1, 9))
# exp7.add_session('14-37-23', None, 'laserpulse', 'am_tuning_curve')
# exp7.add_session('14-38-47', None, 'lasertrain', 'am_tuning_curve')
# exp7.add_session('14-40-39', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3707, tetrodes=range(1, 9))
exp7.add_session('14-43-59', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('14-45-19', None, 'laserpulse', 'am_tuning_curve')
exp7.add_session('14-47-14', None, 'lasertrain', 'am_tuning_curve')
exp7.add_session('14-50-54', 'a', 'am', 'am_tuning_curve')
exp7.add_session('15-05-59', 'b', 'tc', 'am_tuning_curve')
exp7.add_session('15-38-20', None, 'laserpulse2', 'am_tuning_curve')
exp7.add_session('15-39-44', None, 'lasertrain2', 'am_tuning_curve')

exp7.add_site(3800, tetrodes=range(1, 9))
exp7.add_session('15-45-57', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('15-47-35', None, 'laserpulse', 'am_tuning_curve')
exp7.add_session('15-49-33', None, 'lasertrain', 'am_tuning_curve')
exp7.add_session('15-53-18', 'c', 'am', 'am_tuning_curve')
exp7.add_session('16-13-51', 'd', 'tc', 'am_tuning_curve')
exp7.add_session('16-46-39', None, 'laserpulse2', 'am_tuning_curve')
exp7.add_session('16-49-08', None, 'lasertrain2', 'am_tuning_curve')
exp7.maxDepth = 3800
