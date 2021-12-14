from jaratoolbox import celldatabase

subject = 'npix000'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2021-11-30', brainArea='left_AC', probe = 'NPv1-2881/2872', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp0)
exp0.add_site(1) 
exp0.maxDepth = 1
exp0.add_session('12-14-31','a','pureTones','am_tuning_curve') 
