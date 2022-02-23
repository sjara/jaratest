from jaratoolbox import celldatabase

subject = 'feat004'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2022-01-11', brainArea='AC_right', probe = 'NPv1-2872', recordingTrack='DiD', info=['anteromedialDiD', 'soundLeft']) #reference = tip
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

#exp1 = celldatabase.Experiment(subject, '2022-01-12', brainArea='rightAC', probe = 'NPv1-2872', recordingTrack='DiI', info=['DiI', 'soundLeft']) #reference = tip
#experiments.append(exp0)
# 2:08 in booth
# 2:10 lowered probes
# 2:50 couldn't penetrate brain. Ended experiment

#exp2 = celldatabase.Experiment(subject, '2022-01-18', brainArea='rightAC', probe = 'NPv1-2872', recordingTrack='DiI', info=['aterolateralDiI', 'soundLeft']) #reference = tip
#experiments.append(exp2)
# 13:35 in booth
# 13:40 lowered probe
# 14:42 couldn't penetrate brain. Ended experiment.
# Cleaned R craniotomy

exp3 = celldatabase.Experiment(subject, '2022-01-19', brainArea='AC_left', probe = 'NPv1-2872', recordingTrack='caudomedialDiD', info=['caudomedialDiD', 'soundRight']) #reference = tip
experiments.append(exp3)
# 12:40 in booth
# Couldn't penetrate R craniotomy again, moving to left craniotomy.
# Cleaned left craniotomy. It has healed over a lot since surgery and only about a third of the original craniotomy is useable.
# 1:35 lowered probes, in brain
# 1:40 reached max depth
# 2:00 started recording
# 3:00 ended recording

exp3.add_site(2504) #2504.6
exp3.maxDepth = 2504
exp3.add_session('14-02-47','a','pureTones','am_tuning_curve') # this session presented binaurally accidentally
exp3.add_session('14-18-17','b','AM','am_tuning_curve')
exp3.add_session('14-29-00','a','FT','2afc_speech') # 4 stimuli 20220115 stim
exp3.add_session('14-42-03','b','VOT','2afc_speech') # 4 stimuli 20220115 stim

exp4 = celldatabase.Experiment(subject, '2022-01-21', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='caudolateralDiI', info=['caudolateralDiI', 'soundRight']) #reference = tip
experiments.append(exp4)
# 8:25 in booth
# 8:35 lowered probes, in brain
# 8:40 broke probe
# 9:10 new probe in brain
# 9:15 reached max depth
# 9:32 started recording
# 10:35 ended recording

exp4.add_site(2700) #2700.5
exp4.maxDepth = 2700
exp4.add_session('09-33-00','a','pureTones','am_tuning_curve')
exp4.add_session('09-49-46','b','AM','am_tuning_curve')
exp4.add_session('09-58-15','a','FTVOTBorders','2afc_speech') # matrix borders 20220115 stim
