from jaratoolbox import celldatabase

subject = 'feat002'
experiments = []

# Experiment parameters: subject, date, brainArea, probe, recordingTrack 
# (penetrationLocationAndDye), info (which contains [probeOrientation, soundSource]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2021-11-', brainArea='left_AC', probe = 'NPv1-2881' recordingTrack='_DiI', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp0)
# in booth
# touched brain
# reached maxDepth
# started recording
# done


exp0.add_site() # 3314.0
exp0.maxDepth = 
exp0.add_session('','a','pureTones','am_tuning_curve')
exp0.add_session('','b','AM','am_tuning_curve') 
exp0.add_session('','a','FT','2afc_speech')
exp0.add_session('','b','VOT','2afc_speech')



