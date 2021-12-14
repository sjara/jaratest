from jaratoolbox import celldatabase

subject = 'feat003'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2021-12-07', brainArea='leftAC', probe = 'NPv1-2881/2872', recordingTrack='DiD', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp0)
#4:15 in booth
# Probes just barely didn't fit in craniotomy. Animal bled a lot after cleaning up granulation tissue. cancelled recording.

exp1 = celldatabase.Experiment(subject, '2021-12-09', brainArea='leftAC', probe = 'NPv1-2881/2872', recordingTrack='DiD', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp1)
# 11:15 in booth
# Zeroed at medial probe, Lateral probe touched surface @ 386m
# Probes couldn't penetrate brain. Could be because need to clean tissue.

exp2 = celldatabase.Experiment(subject, '2021-12-13', brainArea='leftAC', probe = 'NPv1-2881/2872', recordingTrack='anteromedialDiI', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp2)
# 2:35 in booth
# Cleaned L craniotomy. A decent amount of bleeding. Seems there's a 
# 3:15 lowered probes
# 3:17 in brain. zerod at medial probe lateral probe touched brain 379.8
# 3:23 max depth
# 3:45 Started recording
# 4:28 done recording
# 
exp2.add_site(2521) #2520.9
exp2.maxDepth = 2521
exp2.add_session('15-44-37','a','AM','am_tuning_curve') 
exp2.add_session('15-54-15','b','pureTones','am_tuning_curve')
exp2.add_session('16-04-30','a','VOT','2afc_speech') # 4 stimuli 20211209 stim
exp2.add_session('16-17-52','b','FT','2afc_speech') # 4 stimuli 20211209 stim

