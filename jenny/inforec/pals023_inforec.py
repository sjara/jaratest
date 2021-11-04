from jaratoolbox import celldatabase

subject = 'pals023'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Site parameters: depth, tetrodes.


exp0 = celldatabase.Experiment(subject,
                               '2021-08-13',
                               brainarea='rightAC',
                               info = 'A4x2-tet')
experiments.append(exp0)


# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_site(644.6,tetrodes = range(1,9))
exp0.add_session('17-58-12','a','AM','am_tuning_curve')
exp0.add_session('18-05-51','b','PureTones','am_tuning_curve')
exp0.maxDepth = 644.6

exp1 = celldatabase.Experiment(subject, '2021-08-20', brainarea = 'rightAC', info = 'A4x2-tet')
experiments.append(exp1)
exp1.add_site(1083.6,tetrodes = range(1,9))
exp1.add_session('15-29-48','a','AM','am_tuning_curve')
exp1.add_session('15-37-46','b','PureTones','am_tuning_curve') #got really noisy, lost saline in well. 
exp1.add_session('15-49-38','c','PureTones','am_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2021-09-24', brainarea = 'rightAC', info = 'NP1')
experiments.append(exp2)
exp2.add_site(1429.2)
exp2.add_session('15-27-02','a','AM','am_tuning_curve')
exp2.add_session('15-27-02','b','PureTones','am_tuning_curve') #accidentally didn't start a new session. Ephys is saved in "recording1" and "recording2" folders within this session
exp2.add_session('15-44-34','c','PureTones','am_tuning_curve')

exp3 = celldatabase.Experiment(subject, '2021-10-14', brainarea = 'rightAC', info = 'NP1')
experiments.append(exp3)
exp3.add_site(528.5)
exp3.add_session('15-06-31','a','AM','am_tuning_curve')
exp3.add_session('15-14-22','b','PureTones','am_tuning_curve') 
