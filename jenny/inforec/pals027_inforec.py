from jaratoolbox import celldatabase

subject = 'pals027'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2021-11-03', brainarea='rightAC', info = 'NP1', reference= 'tip')
experiments.append(exp0)
exp0.add_site(3314.0)
exp0.add_session('14-29-00','a','PureTones','am_tuning_curve') #not very PT responsive
exp0.add_session('14-27-10','b','AM','am_tuning_curve') #AM responsive (and looks to be phaselocking up to ~60Hz)

