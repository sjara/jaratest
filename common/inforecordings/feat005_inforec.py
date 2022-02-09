from jaratoolbox import celldatabase

subject = 'feat005'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-02-07', brainArea='leftAC', probe = 'NPv1-2761', recordingTrack='anterolateralDiI', info=['anterolateralDiI', 'soundRight']) #reference = external
experiments.append(exp0)
# 11:10 in booth
# 11:15 lowered electodes
# 11:30 couldn't penetrate brain. Retracted and tried cleaning craniotomy
# 12:05 tried lowering electrodes again. In brain
# 12:07 Reached max depth
# 12:34 Started recording
# trode 291 last one with spikes. (mayyybe 299)
# 13:35 Done recording

exp0.add_site(3020)
exp0.maxDepth = 3020
#exp0.add_session('12-34-34','a','pureTones','am_tuning_curve') #got noisy, if have time at end, redo puretones. presented binaurally.
exp0.add_session('12-52-53','b','AM','am_tuning_curve') #presented binaurally.
exp0.add_session('13-03-30','a','FTVOTBorders','2afc_speech') #presented right
exp0.add_session('13-35-09','d','pureTones','am_tuning_curve') 


exp1 = celldatabase.Experiment(subject, '2022-02-08', brainArea='leftAC', probe = 'NPv1-2761', recordingTrack='anteromedialDiD', info=['anteromedialDiD', 'soundRight']) #reference = external
experiments.append(exp1)
# 14:48 in booth
# 14:50 lowered electodes
# 14:54 Reached max depth
# 15:20 Started recording
# Electrode 295 last one I see with spikes.
# 16:16 Done recording

exp1.add_site(3005)
exp1.maxDepth = 3005
exp1.add_session('15-20-39','a','pureTones','am_tuning_curve') 
exp1.add_session('15-36-32','b','AM','am_tuning_curve')
exp1.add_session('15-45-22','a','FTVOTBorders','2afc_speech')
