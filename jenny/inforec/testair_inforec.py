from jaratoolbox import celldatabase

subject = 'testair'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Site parameters: depth, tetrodes.

exp0 = celldatabase.Experiment(subject,
                               '2021-08-02',
                               brainarea='air',
                               info='A4x2-tet')
experiments.append(exp0)

# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.
exp0.add_site(000, tetrodes=range(1, 9))
