from jaratoolbox import celldatabase

subject = 'adap047'
experiments = []

# exp0 = celldatabase.Experiment(subject,
#                                '2017-06-02',
#                                brainarea='rightAstr',
#                                info=['middleDiI', 'facingPosterior'])
# experiments.append(exp0)

# #Mouse on the rig at 11:45, waiting 10 mins for brain to settle

# # exp0.add_site(1539, tetrodes=range(1, 9))
# # exp0.add_session('12-20-21', 'a', 'noiseburst', 'am_tuning_curve')
# # exp0.add_session('12-23-34', 'b', 'tc', 'am_tuning_curve')

# #1800-2000um no sound response, pretty quiet
# exp0.add_site(2000, tetrodes=range(1, 9))
# exp0.add_session('12-49-17', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-23-34', 'b', 'tc', 'am_tuning_curve')

# exp0.add_site(2058, tetrodes=range(1, 9))
# exp0.add_session('13-00-13', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('13-02-04', 'c', 'tc', 'am_tuning_curve')

# exp0.add_site(2114, tetrodes=range(1, 9))
# exp0.add_session('13-51-39', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('13-54-35', 'd', 'tc', 'am_tuning_curve')

# exp0.add_site(2180, tetrodes=range(1, 9))
# exp0.add_session('14-17-23', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('14-19-31', 'e', 'tc', 'am_tuning_curve')

# exp0.add_site(2381, tetrodes=range(1, 9))
# exp0.add_session('14-42-17', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('14-44-45', 'f', 'tc', 'am_tuning_curve')

# exp0.add_site(2482, tetrodes=range(1, 9))
# exp0.add_session('15-08-43', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('15-10-58', 'g', 'tc', 'am_tuning_curve')

# exp0.add_site(2585, tetrodes=range(1, 9))
# exp0.add_session('15-38-03', None, 'noiseburst', 'am_tuning_curve') #No more sound response, done for the day
# EXPERIMENT ABOVE COLLECTED WIth ONLY THE L SPEAKER ACTIVE


exp1 = celldatabase.Experiment(subject,
                               '2017-06-06',
                               brainarea='rightAStr',
                               info=['anteriorDiD', 'facingPosterior', 'medial:None','lateral:1,2'])
experiments.append(exp1)

#Mouse on the rig at 10:03, waiting 10 mins for brain to settle

exp1.add_site(1938, tetrodes=range(1, 9)).remove_tetrodes(6)
exp1.add_session('10-42-36', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('10-45-09', 'a', 'tc', 'am_tuning_curve')

# exp1.add_site(2157, tetrodes=range(1, 9))
# exp1.add_session('11-10-28', None, 'noiseburst', 'am_tuning_curve')
# # exp1.add_session('10-45-09', 'a', 'tc', 'am_tuning_curve')

exp1.add_site(2426, tetrodes=range(1, 9)).remove_tetrodes(3)
exp1.add_session('11-16-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-19-17', 'b', 'tc', 'am_tuning_curve')

exp1.add_site(2512, tetrodes=range(1, 9)).remove_tetrodes([1, 4])
exp1.add_session('11-42-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-45-48', 'c', 'tc', 'am_tuning_curve')

exp1.add_site(2610, tetrodes=range(1, 9)).remove_tetrodes(1)
exp1.add_session('12-06-06', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-08-26', 'd', 'tc', 'am_tuning_curve')

exp1.add_site(2681, tetrodes=range(1, 9)).remove_tetrodes([1, 3])
exp1.add_session('12-43-50', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-46-16', 'e', 'tc', 'am_tuning_curve')

exp2 = celldatabase.Experiment(subject,
                               '2017-06-08',
                               brainarea='leftAStr',
                               info=['centralDiI', 'facingPosterior','medial:3,4,5,6,7,8', 'lateral:1,2'])
experiments.append(exp2)

#Mouse on the rig at 1:45p, waiting 10 mins for brain to settle

exp2.add_site(2012, tetrodes=range(1, 9))
exp2.add_session('14-50-24', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-52-52', 'a', 'tc', 'am_tuning_curve')

exp2.add_site(2110, tetrodes=range(1, 9))
exp2.add_session('15-26-04', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('15-29-02', 'b', 'tc', 'am_tuning_curve')

exp2.add_site(2220, tetrodes=range(1, 9))
exp2.add_session('15-59-41', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-02-07', 'c', 'tc', 'am_tuning_curve')

exp2.add_site(2325, tetrodes=range(1, 9))
exp2.add_session('16-30-31', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-32-39', 'd', 'tc', 'am_tuning_curve')

exp3 = celldatabase.Experiment(subject,
                               '2017-06-13',
                               brainarea='leftAStr',
                               info=['anteriorDiD', 'facingPosterior','medial:3,4,5,6,7,8', 'lateral:1,2'])
experiments.append(exp3)

#Mouse on the rig at 1:45p, waiting 10 mins for brain to settle

exp3.add_site(2368, tetrodes=range(1, 9)).remove_tetrodes([3, 4, 5])
exp3.add_session('11-07-15', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('11-10-17', 'a', 'tc', 'am_tuning_curve')

exp3.add_site(2432, tetrodes=range(1, 9)).remove_tetrodes([3, 4, 6, 7])
exp3.add_session('11-30-14', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('11-32-12', 'b', 'tc', 'am_tuning_curve')

# exp3.add_site(2709, tetrodes=range(1, 9))
# exp3.add_session('12-07-09', None, 'noiseburst', 'am_tuning_curve') #No sound response up to here

# exp3.add_site(2709, tetrodes=range(1, 9))
# exp3.add_session('12-12-36', None, 'noiseburst', 'am_tuning_curve') #No sound response up to here

# exp3.add_site(2739, tetrodes=range(1, 9))
# exp3.add_session('12-15-37', None, 'noiseburst', 'am_tuning_curve')

exp3.add_site(2763, tetrodes=range(1, 9)).remove_tetrodes([3, 4])
exp3.add_session('12-20-55', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-23-00', 'c', 'tc', 'am_tuning_curve')

exp3.add_site(2830, tetrodes=range(1, 9)).remove_tetrodes([1, 3, 4])
exp3.add_session('12-44-51', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('12-47-32', 'd', 'tc', 'am_tuning_curve') #No response really. I'm done here. 

exp4 = celldatabase.Experiment(subject,
                               '2017-06-19',
                               brainarea='rightAStr',
                               info=['centralDiO', 'facingPosterior','medial:3,4,5,6','lateral:7,8'])
experiments.append(exp4)

#I had to remove some tissue on top of the brain for the probes to go in. I hop that the estimate of surface is still good. It looked like the tissue I referenced against was below the surface of the skull, but by about as much as one skull thickness - so we are probably ok
#Mouse on rig at 19:35, waiting 10 mins for tissue to settle.

exp4.add_site(1941, tetrodes=range(1, 9)).remove_tetrodes(3)
exp4.add_session('19-52-46', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('19-55-48', 'a', 'tc', 'am_tuning_curve')

exp4.add_site(2015, tetrodes=range(1, 9))
exp4.add_session('20-29-43', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('20-32-53', 'b', 'tc', 'am_tuning_curve')

exp4.add_site(2107, tetrodes=range(1, 9)).remove_tetrodes(2)
exp4.add_session('20-55-30', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('20-58-31', 'c', 'tc', 'am_tuning_curve')

exp4.add_site(2204, tetrodes=range(1, 9))
exp4.add_session('21-28-57', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('21-32-41', 'd', 'tc', 'am_tuning_curve')

exp4.add_site(2303, tetrodes=range(1, 9)).remove_tetrodes(2)
exp4.add_session('22-01-33', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('22-03-30', 'e', 'tc', 'am_tuning_curve')

exp4.add_site(2404, tetrodes=range(1, 9)).remove_tetrodes(2)
exp4.add_session('22-33-16', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('22-35-32', 'f', 'tc', 'am_tuning_curve')

exp4.add_site(2505, tetrodes=range(1, 9)).remove_tetrodes(2)
exp4.add_session('22-59-45', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('23-02-16', 'g', 'tc', 'am_tuning_curve')

exp4.add_site(2604, tetrodes=range(1, 9)).remove_tetrodes(2)
exp4.add_session('23-25-53', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('23-28-25', 'h', 'tc', 'am_tuning_curve')

exp4.add_site(2707, tetrodes=range(1, 9))
exp4.add_session('23-54-22', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('23-56-28', 'i', 'tc', 'am_tuning_curve')

site = exp4.add_site(2812, tetrodes=range(1, 9))
site.remove_tetrodes(2)
site.date = '2017-06-20'
exp4.add_session('00-19-18', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('00-23-24', 'a', 'tc', 'am_tuning_curve')

exp5 = celldatabase.Experiment(subject,
                               '2017-06-21',
                               brainarea='leftAStr',
                               info=['centralDiO', 'facingPosterior','medial:3,4,5,6,7,8', 'lateral:1,2'])
experiments.append(exp5)

#I had to remove some tissue on top of the brain for the probes to go in. I hop that the estimate of surface is still good. It looked like the tissue I referenced against was below the surface of the skull, but by about as much as one skull thickness - so we are probably ok (This is copied but applies to this experiment as well)
#

exp5.add_site(2052, tetrodes=range(1, 9))
exp5.add_session('23-00-10', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('23-02-32', 'a', 'tc', 'am_tuning_curve')

exp5.add_site(2256, tetrodes=range(1, 9))
exp5.add_session('23-25-01', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('23-28-01', 'b','tc', 'am_tuning_curve')

exp5.add_site(2350, tetrodes=range(1, 9))
exp5.add_session('23-50-43', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('23-52-51', 'c','tc', 'am_tuning_curve')

site = exp5.add_site(2455, tetrodes=range(1, 9))
site.date = '2017-06-22'
exp5.add_session('00-12-03', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('00-14-00', 'a','tc', 'am_tuning_curve')

#site = exp5.add_site(2554, tetrodes=range(1, 9))
#site.date = '2017-06-22'
#exp5.add_session('00-34-21', None, 'noiseburst', 'am_tuning_curve') #No more sound response - done for the night
