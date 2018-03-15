from jaratoolbox import celldatabase

subject = 'pinp026'
experiments = []

#Laser calibration
# 0.5 - 0.85
# 1.0 - 1.05
# 1.5 - 1.35
# 2.0 - 1.70
# 2.5 - 2.05
# 3.0 - 2.45

exp0 = celldatabase.Experiment(subject,
                               '2017-11-14',
                               brainarea='rightThal',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

# Probe at 2000 at 1056hrs, waiting 10 mins
# exp0.add_site(3010, tetrodes=[2, 4, 8])
# exp0.add_session('12-18-56', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-21-42', None, 'laserpulse', 'am_tuning_curve') #Laser responses but to offset

# exp0.add_site(3056, tetrodes=[2, 4, 8])
# exp0.add_session('12-32-39', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-35-06', None, 'laserpulse', 'am_tuning_curve') #

# exp0.add_site(3184, tetrodes=[2, 4, 8])
# exp0.add_session('12-43-17', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('12-45-41', None, 'laserpulse', 'am_tuning_curve') #

# exp0.add_site(3255, tetrodes=[2, 4, 8])
# exp0.add_session('12-52-24', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('12-45-41', None, 'laserpulse', 'am_tuning_curve') #

# exp0.add_site(3312, tetrodes=[2, 4, 8])
# exp0.add_session('13-00-52', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3404, tetrodes=[2, 4, 8])
# exp0.add_session('13-05-56', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3456, tetrodes=[1, 2, 4, 8])
# exp0.add_session('13-37-58', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3514, tetrodes=[1, 2, 4, 8])
# exp0.add_session('13-44-01', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3561, tetrodes=[1, 2, 4, 8])
# exp0.add_session('13-48-19', None, 'laserpulse', 'am_tuning_curve')

# exp0.add_site(3621, tetrodes=[1, 2, 4, 8])
# exp0.add_session('13-54-04', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3708, tetrodes=[1, 2, 3, 4, 7, 8])
exp0.add_session('14-05-52', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-08-22', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-11-54', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-16-57', 'a', 'tc', 'am_tuning_curve')
exp0.add_session('14-49-43', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3779, tetrodes=[1, 2, 3, 4, 7, 8])
exp0.add_session('15-14-05', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-16-45', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-19-03', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-24-01', 'c', 'tc', 'am_tuning_curve')
exp0.add_session('16-00-45', 'd', 'am', 'am_tuning_curve')

exp0.add_site(3861, tetrodes=[1, 2, 3, 4, 6, 7, 8])
exp0.add_session('16-30-02', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-32-56', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-37-15', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-42-49', 'e', 'tc', 'am_tuning_curve')
exp0.add_session('17-17-39', 'f', 'am', 'am_tuning_curve')

# exp0.add_site(3935, tetrodes=[1, 2, 3, 4, 6, 7, 8])
# exp0.add_session('17-45-50', None, 'noiseburst', 'am_tuning_curve')
# exp0.add_session('17-48-07', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('17-50-25', None, 'lasertrain', 'am_tuning_curve') #No more laser response

# exp0.add_site(4008, tetrodes=[1, 2, 3, 4, 6, 7, 8])
# exp0.add_session('18-19-47', None, 'laserpulse', 'am_tuning_curve') #No more laser responses, done for the day
exp0.maxDepth = 4008

exp1 = celldatabase.Experiment(subject,
                               '2017-11-15',
                               brainarea='rightThal',
                               info=['DiD', 'facingPosterior'])
experiments.append(exp1)

# exp1.add_site(2910, tetrodes=[1, 2, 3, 4, 6, 8])
# exp1.add_session('12-18-23', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('12-20-49', None, 'laserpulse', 'am_tuning_curve')

# exp1.add_site(2974, tetrodes=[1, 2, 3, 4, 6, 8])
# exp1.add_session('12-32-06', None, 'laserpulse', 'am_tuning_curve')

exp1.add_site(3040, tetrodes=[1, 2, 3, 4, 6, 8])
exp1.add_session('12-41-25', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('12-43-40', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('12-45-54', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('12-51-53', 'a', 'tc', 'am_tuning_curve')
exp1.add_session('13-25-01', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3111, tetrodes=[1, 2, 3, 4, 5, 6, 8])
exp1.add_session('13-50-12', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-54-39', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('14-02-24', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('14-08-54', 'c', 'tc', 'am_tuning_curve')
exp1.add_session('14-42-26', 'd', 'am', 'am_tuning_curve')

exp1.add_site(3252, tetrodes=[1, 2, 3, 4, 5, 6, 8])
exp1.add_session('15-09-36', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-15-03', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-17-18', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('15-27-31', 'e', 'tc', 'am_tuning_curve')
exp1.add_session('16-00-45', 'f', 'am', 'am_tuning_curve')

exp1.add_site(3327, tetrodes=[1, 2, 3, 4, 5, 6, 8])
exp1.add_session('16-20-31', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-22-59', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-25-06', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-30-50', 'g', 'tc', 'am_tuning_curve')
exp1.add_session('17-03-57', 'h', 'am', 'am_tuning_curve')

exp1.add_site(3421, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp1.add_session('17-25-22', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-27-39', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-29-58', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-35-54', 'i', 'tc', 'am_tuning_curve')
exp1.add_session('18-12-22', 'j', 'am', 'am_tuning_curve')

# exp1.add_site(3526, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
# exp1.add_session('18-31-10', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('18-33-47', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('18-35-54', None, 'lasertrain', 'am_tuning_curve') #Not good enough

#Final depth 3605um
exp1.maxDepth = 3605

exp2 = celldatabase.Experiment(subject,
                               '2017-11-16',
                               brainarea='rightThal',
                               info=['posteriorDiI', 'facingPosterior'])
experiments.append(exp2)

exp2.add_site(2952, tetrodes=[1, 2, 3, 4, 6, 8])
exp2.add_session('10-33-50', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('10-36-13', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('10-38-53', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('10-44-08', 'a', 'tc', 'am_tuning_curve')
exp2.add_session('11-19-22', 'b', 'am', 'am_tuning_curve')

exp2.add_site(3046, tetrodes=[1, 2, 4, 5, 6, 7, 8])
exp2.add_session('11-43-52', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('11-46-57', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-49-32', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-54-24', 'c', 'tc', 'am_tuning_curve')
exp2.add_session('12-28-58', 'd', 'am', 'am_tuning_curve')

exp2.add_site(3122, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp2.add_session('13-04-12', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-06-23', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-10-38', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-16-42', 'e', 'tc', 'am_tuning_curve')
exp2.add_session('13-50-04', 'f', 'am', 'am_tuning_curve')

exp2.add_site(3256, tetrodes=[1, 2, 4, 5, 6, 7, 8])
exp2.add_session('14-10-13', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-14-04', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('14-16-11', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-23-21', 'g', 'tc', 'am_tuning_curve')
exp2.add_session('14-56-42', 'h', 'am', 'am_tuning_curve')
exp2.maxDepth = 3256
