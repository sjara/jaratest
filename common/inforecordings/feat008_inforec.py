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


exp1 = celldatabase.Experiment(subject, '2022-03-24', brainArea='AC_right', probe = 'NPv1-4542', recordingTrack='anteriormedial_DiD', info=['anteriormedial_DiD', 'soundLeft']) #reference = tip
experiments.append(exp1)
# 10:40 in booth
# 10:43 in brain
# 10:45 reached max depth
# 11:08 started recording
# 12:06 done

exp1.add_site(2947)
exp1.maxDepth = 2947
exp1.add_session('11-08-58','a','AM','am_tuning_curve') 
exp1.add_session('11-18-25','b','pureTones','am_tuning_curve')
exp1.add_session('11-35-22','a','FTVOTBorders','2afc_speech')


exp2 = celldatabase.Experiment(subject, '2022-03-25', brainArea='AC_right', probe = 'NPv1-4542', recordingTrack='caudomedial_DiI', info=['caudomedial_DiI', 'soundLeft']) #reference = tip
experiments.append(exp2)
# 12:00 in booth
# 12:07 in brain
# 12:09 reached max depth
# 12:28 started recording
# 13:24 done

exp2.add_site(2954)
exp2.maxDepth = 2954
exp2.add_session('12-28-02','a','AM','am_tuning_curve') 
exp2.add_session('12-35-45','b','pureTones','am_tuning_curve')
exp2.add_session('12-51-59','a','FTVOTBorders','2afc_speech')

