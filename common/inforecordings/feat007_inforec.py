from jaratoolbox import celldatabase

subject = 'feat007'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-03-10', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='anteromedial_DiI', info=['anteromedial_DiI', 'soundLeft']) #reference = tip
experiments.append(exp0)
# 10:53 in booth
# 10:55 in brain
# 11:00 reached max depth
# 11:19 started recording
# 12:35 done

exp0.add_site(2967)
exp0.maxDepth = 2967
exp0.add_session('11-19-31','a','AM','am_tuning_curve') 
exp0.add_session('11-27-37','b','pureTones','am_tuning_curve')
exp0.add_session('11-44-02','a','FTVOTBorders','2afc_speech')


exp1 = celldatabase.Experiment(subject, '2022-03-11', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='middlemedialDiD', info=['middlemedial_DiD', 'soundLeft']) #reference = tip
experiments.append(exp1)
# 13:53 in booth
# 14:05 lowered electrodes, couldn't penetrate brain. Retracted and cleaned craniotomy.
# 14:20 lowered electrodes, in brain
# 14:25 reached max depth
# 14:45 started recording
# 15:45 done

exp1.add_site(2942)
exp1.maxDepth = 2942
exp1.add_session('14-47-12','a','AM','am_tuning_curve') 
exp1.add_session('14-55-00','b','pureTones','am_tuning_curve') #accidentally hit the start button after I finished recording so there are ~2 extra trials in the behavior data at the end that weren't recorded.
exp1.add_session('15-15-21','a','FTVOTBorders','2afc_speech')
