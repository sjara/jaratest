from jaratoolbox import celldatabase

subject = 'pinp022'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-09-01',
                               brainarea='rightThal',
                               info=['anteriorDiD', 'facingPosterior'])
experiments.append(exp0)

exp0.add_site(3022, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-12-33', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-16-32', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3282, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-33-10', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3353, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-38-52', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3420, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-48-27', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3505, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-51-19', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3558, tetrodes=[5, 6, 7, 8])
exp0.add_session('12-55-32', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3652, tetrodes=[5, 6, 7, 8])
exp0.add_session('13-16-11', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-18-17', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3763, tetrodes=[5, 6, 7, 8])
exp0.add_session('13-33-42', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(3852, tetrodes=[5, 6, 7, 8])
exp0.add_session('13-48-23', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-50-42', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-55-10', None, 'lasertrain', 'am_tuning_curve')

# I am done. max depth is 3960. I pulled the probe out and there were many sites that were above 10Mohms. I should have checked the impedence data before I started today.
