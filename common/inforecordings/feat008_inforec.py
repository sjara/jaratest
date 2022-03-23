from jaratoolbox import celldatabase

subject = 'feat008'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-03-23', brainArea='AC_right', probe = 'NPv1-4542', recordingTrack='anteriorlateral_DiI', info=['anteriorlateral_DiI', 'soundLeft']) #reference = tip
experiments.append(exp0)
# 14:58 in booth
# 15:00 in brain
# 15:03 reached max depth
# 15:23 started recording
# 16: done

exp0.add_site(3000)
exp0.maxDepth = 3000
exp0.add_session('15-24-01','a','AM','am_tuning_curve') 
exp0.add_session('15-32-03','b','pureTones','am_tuning_curve')
exp0.add_session('15-49-09','a','FTVOTBorders','2afc_speech')


