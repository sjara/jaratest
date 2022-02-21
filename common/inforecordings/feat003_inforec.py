from jaratoolbox import celldatabase

subject = 'feat003'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

#exp0 = celldatabase.Experiment(subject, '2021-12-07', brainArea='AC_left', probe = 'NPv1-2881/2872', recordingTrack='DiD', info=['facesLeft', 'soundRight']) #reference = tip
#experiments.append(exp0)
#4:15 in booth
# Probes just barely didn't fit in craniotomy. Animal bled a lot after cleaning up granulation tissue. cancelled recording.

#exp1 = celldatabase.Experiment(subject, '2021-12-09', brainArea='AC_left', probe = 'NPv1-2881/2872', recordingTrack='DiD', info=['facesLeft', 'soundRight']) #reference = tip
#experiments.append(exp1)
# 11:15 in booth
# Zeroed at medial probe, Lateral probe touched surface @ 386m
# Probes couldn't penetrate brain. Could be because need to clean tissue.

exp2 = celldatabase.Experiment(subject, '2021-12-13', brainArea='AC_left', probe = 'NPv1-2881/2872', recordingTrack='anterolateralDiI', info=['facesLeft', 'soundRight']) #reference = tip
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

exp3 = celldatabase.Experiment(subject, '2021-12-14', brainArea='AC_left', probe = 'NPv1-2881/2872', recordingTrack='anteromedialDiD', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp3)
# 12:25 in booth
# 12:30 in brain. zeroed at medial probe. lateral probe touched brain 446.3
# 12:36 reached max depth
# 12:54 started recording
# 1:35 done recording
#
exp3.add_site(2706) #2706.0
exp3.maxDepth = 2706
exp3.add_session('12-54-15','a','pureTones','am_tuning_curve')
exp3.add_session('13-04-03','b','AM','am_tuning_curve')
exp3.add_session('13-11-34','a','FT','2afc_speech') # 4 stimuli 20211209 stim
exp3.add_session('13-24-30','b','VOT','2afc_speech') # 4 stimuli 20211209 stim

#exp4 = celldatabase.Experiment(subject, '2021-12-15', brainArea='AC_left', probe = 'NPv1-2881/2872', recordingTrack='DiD', info=['facesLeft', 'soundRight']) #reference = tip
#experiments.append(exp4)
# 10\:45 in booth
# 1:48 in brain. zeroed at medial probe. lateral probe touched brain 251.5
# 2:00 reached max depth
# Was getting some bending from lateral probe, couldn't lower any further.
# 2:15 Waited for tissues to settle, still no signals. Ended session.

#exp4.add_site(812) #811.5
#exp4.maxDepth = 812

#exp5 = celldatabase.Experiment(subject, '2021-12-17', brainArea='AC_right', probe = 'NPv1-2881/2872', recordingTrack='caudolateralDiI', info=['facesLeft', 'soundLeft']) #reference = tip
#experiments.append(exp5)
# 10:45 in booth
# 10:54 touched brain at medial probe, zeroed.
# 11:10. couldn't penetrate brain.Cancelled recording session.
