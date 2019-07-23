from jaratoolbox import celldatabase

subject = 'pinp021'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-07-26',
                               brainarea='rightThal',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

#Mouse on the rig at 1333hrs, waiting 10 mins for brain to settle
#Tetrodes at 1248um
# 1348 - tetrodes at 2510um, waiting for brain to settle

# exp0.add_site(2910, tetrodes=range(1, 9)).remove_tetrodes([5, 7, 8])
# exp0.add_session('14-16-29', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3104, tetrodes=range(1, 9)).remove_tetrodes([7])
# exp0.add_session('14-21-53', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3205, tetrodes=range(1, 9))
# exp0.add_session('14-37-33', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3305, tetrodes=range(1, 9))
# exp0.add_session('14-45-25', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3405, tetrodes=range(1, 9))
# exp0.add_session('14-52-54', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(3502, tetrodes=range(1, 9))
# exp0.add_session('15-09-26', None, 'noiseburst', 'am_tuning_curve') #Something!
# exp0.add_session('15-11-59', None, 'laserpulse', 'am_tuning_curve') #Maybe!
# exp0.add_session('15-14-17', None, 'lasertrain', 'am_tuning_curve') #Clustering says no way jose!


# exp0.add_site(3708, tetrodes=range(1, 9))
# exp0.add_session('15-31-43', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('15-34-34', None, 'laserpulse', 'am_tuning_curve') #There is nothing here. I am going to remove the probes, let the animal rest, and possibly do another penetration today farther back.
exp0.maxDepth = 3708


exp1 = celldatabase.Experiment(subject,
                               '2017-07-27',
                               brainarea='rightThal',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp1)

#Mouse on the rig at 1242hrs, waiting 10 mins for brain to settle
#Tetrodes at 2510um

# exp1.add_site(2510, tetrodes=range(1, 9)).remove_tetrodes([1, 2, 4])
# exp1.add_session('12-56-29', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(3151, tetrodes=range(1, 9)).remove_tetrodes([8])
# exp1.add_session('13-10-21', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(3209, tetrodes=range(1, 9))
# exp1.add_session('13-15-22', None, 'noiseburst', 'am_tuning_curve')

# exp1.add_site(3347, tetrodes=range(1, 9)).remove_tetrodes([7, 8])
# exp1.add_session('13-36-01', None, 'noiseburst', 'am_tuning_curve')

exp1.add_site(3466, tetrodes=range(1, 9))
# exp1.add_session('13-40-43', None, 'noiseburst', 'am_tuning_curve')#nothing
exp1.add_session('13-45-57', None, 'laserpulse', 'am_tuning_curve')#Laser responses
exp1.add_session('13-48-01', None, 'lasertrain', 'am_tuning_curve')#

exp1.add_session('13-49-32', None, 'noiseburst', 'am_tuning_curve')#nothing much

exp1.add_session('13-54-15', 'a', 'tc', 'am_tuning_curve') # I have to stop here.
exp1.maxDepth = 3466

exp2 = celldatabase.Experiment(subject,
                               '2017-07-28',
                               brainarea='rightThal',
                               info=['posteriorDiI', 'facingPosterior'])
experiments.append(exp2)

#Mouse on the rig at 1150hrs, waiting 10 mins for brain to settle

# exp2.add_site(2506, tetrodes=range(1, 9))
# exp2.add_session('12-16-40', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(2949, tetrodes=range(1, 9))
# exp2.add_session('12-27-10', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(3104, tetrodes=range(1, 9))
# exp2.add_session('12-37-44', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(3202, tetrodes=range(1, 9))
# exp2.add_session('12-45-06', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(3302, tetrodes=range(1, 9))
# exp2.add_session('12-56-28', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(3407, tetrodes=range(1, 9))
# exp2.add_session('13-29-02', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('13-31-30', None, 'laserpulse', 'am_tuning_curve')

# exp2.add_site(3506, tetrodes=range(1, 9))
# exp2.add_session('13-42-49', None, 'noiseburst', 'am_tuning_curve')

# exp2.add_site(3556, tetrodes=range(1, 9))
# exp2.add_session('13-55-39', None, 'noiseburst', 'am_tuning_curve')

exp2.add_site(3650, tetrodes=range(1, 9))
exp2.add_session('14-04-26', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-06-39', None, 'laserpulse', 'am_tuning_curve') #Strange, some LOCKED laser responses to the laser offset

exp2.add_session('14-10-52', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-15-02', 'a', 'tc', 'am_tuning_curve')

exp2.add_site(3787, tetrodes=range(1, 9))
exp2.add_session('15-01-40', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-05-40', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-13-11', None, 'lasertrain', 'am_tuning_curve')

exp2.add_session('15-17-20', 'b', 'tc', 'am_tuning_curve')

# exp2.add_site(3905, tetrodes=range(1, 9))
# exp2.add_session('16-04-09', None, 'noiseburst', 'am_tuning_curve') #Nothing really. I'm done
exp2.maxDepth = 3905

# exp3 = celldatabase.Experiment(subject,
#                                '2017-08-08',
#                                brainarea='rightThal',
#                                info=['posteriorDiD', 'facingPosterior'])
# experiments.append(exp3)

#Electrodes have impedences around 3.2-3.3MOhms
#Rested for 110 mins at 997um
#Absolutely nothing all the way to 3702um. I am done with this animal. I am going to euthanize today.
