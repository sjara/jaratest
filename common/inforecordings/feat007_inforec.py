from jaratoolbox import celldatabase

subject = 'feat007'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-03-10', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='anteromedial_DiI', info=['anteromedial_DiI', 'soundLeft']) #reference = external
experiments.append(exp0)
# 10:53 in booth
# 10:55 in brain
# 11:00 reached max depth
# 11:19 started recording
# 1:25 done

exp0.add_site(2967)
exp0.maxDepth = 2967
exp0.add_session('11-19-31','a','AM','am_tuning_curve') 
exp0.add_session('11-27-37','b','pureTones','am_tuning_curve')
exp0.add_session('11-44-02','a','FTVOTBorders','2afc_speech')

