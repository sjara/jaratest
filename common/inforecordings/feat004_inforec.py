from jaratoolbox import celldatabase

subject = 'feat004'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2022-01-11', brainArea='rightAC', probe = 'NPv1-2872', recordingTrack='DiD', info=['ateromedialDiD', 'soundLeft']) #reference = tip
experiments.append(exp0)
# 12:57 in booth
# 1:05 lowered probe
# 1:06 broke probe
# 1:10 replaced probe
# 1:15 lowered probe, in brain
# 1:30 max depth
# 1:48 started recording
# 2:40 done recording
# 
exp0.add_site(2318) #2318.7
exp0.maxDepth = 2318
exp0.add_session('13-48-00','a','AM','am_tuning_curve') 
exp0.add_session('13-55-58','b','pureTones','am_tuning_curve')
exp0.add_session('14-06-21','a','VOT','2afc_speech') # 4 stimuli 20211209 stim
exp0.add_session('14-20-08','b','FT','2afc_speech') # 4 stimuli 20211209 stim
