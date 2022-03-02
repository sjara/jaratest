from jaratoolbox import celldatabase

subject = 'feat006'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-02-21', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='caudomedialDiI', info=['caudomedialDiI', 'soundLeft']) #reference = external
experiments.append(exp0)
# 11:15 in booth
# 11:30 couldn't penetrate brain. Retracted and tried cleaning craniotomy
# 11:45 tried lowering electrodes again. In brain
# 11:53 reached max depth
# 12:20 started recording
# 1:25 done

exp0.add_site(2934)
exp0.maxDepth = 2934
exp0.add_session('12-20-35','a','AM','am_tuning_curve') 
exp0.add_session('12-32-36','b','pureTones','am_tuning_curve')
exp0.add_session('12-49-24','a','FTVOTBorders','2afc_speech')

exp1 = celldatabase.Experiment(subject, '2022-02-22', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='middlemedialDiD', info=['middlemedialDiD', 'soundLeft']) #reference = external
experiments.append(exp1)
# 13:30 in booth
# 13:45 reached max depth
# 14:05 started recording
# 15:15 done

exp1.add_site(2963)
exp1.maxDepth = 2963
exp1.add_session('14-08-43','a','AM','am_tuning_curve') 
exp1.add_session('14-16-56','b','pureTones','am_tuning_curve')
exp1.add_session('14-34-15','a','FTVOTBorders','2afc_speech')


#exp2 = celldatabase.Experiment(subject, '2022-02-23', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='DiI', info=['DiI', 'soundLeft']) #reference = external
#experiments.append(exp2)
# 13:20 in booth
# 13:30 can't penetrate brain, trying cleaning craniotomy
# 14:40 still couldn't get in brain. cancelled recording

exp3 = celldatabase.Experiment(subject, '2022-02-24', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='caudomedialDiI', info=['caudomedialDiI', 'soundRight']) #reference = external
experiments.append(exp3)
# 11:35 in booth
# cleaned L craniotomy
# 12:25 in brain, reached max depth
# 12:41 started recording

exp3.add_site(2959)
exp3.maxDepth = 2959
exp3.add_session('12-40-52','a','AM','am_tuning_curve') 
exp3.add_session('12-49-15','b','pureTones','am_tuning_curve')
exp3.add_session('13-05-39','a','FTVOTBorders','2afc_speech')


exp4 = celldatabase.Experiment(subject, '2022-02-25', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='middlemedialDiD', info=['middlemedialDiD', 'soundRight']) #reference = external
experiments.append(exp4)
# 11:58 in booth
# 12:07 in brain, reached max depth
# 12:27 started recording
# recording looks a bit noisier than I've had lately. Check if this results in noisier kilosort sorting.
# 13:23 Done

exp4.add_site(2956)
exp4.maxDepth = 2956
exp4.add_session('12-27-43','a','AM','am_tuning_curve') 
exp4.add_session('12-35-54','b','pureTones','am_tuning_curve')
exp4.add_session('12-52-43','a','FTVOTBorders','2afc_speech')

exp5 = celldatabase.Experiment(subject, '2022-02-26', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='anteromedialDiI', info=['anteromedialDiI', 'soundRight']) #reference = external
experiments.append(exp5)
# 12:58 in booth
# 13:05 in brain
# 13:08 reached max depth
# 13:28 started recording
# 14:23 Done

exp5.add_site(2983)
exp5.maxDepth = 2983
exp5.add_session('13-28-33','a','AM','am_tuning_curve') 
exp5.add_session('13-36-27','b','pureTones','am_tuning_curve')
exp5.add_session('13-52-41','a','FTVOTBorders','2afc_speech')


exp6 = celldatabase.Experiment(subject, '2022-02-28', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='anterolateralDiD', info=['anterolateralDiD', 'soundRight']) #reference = external
experiments.append(exp6)
# 11:15 in booth
# 11:18 in brain
# 11:21 reached max depth
# 11:41 started recording
# 12:36 Done

exp6.add_site(2941)
exp6.maxDepth = 2941
exp6.add_session('11-41-12','a','AM','am_tuning_curve') 
exp6.add_session('11-48-57','b','pureTones','am_tuning_curve')
exp6.add_session('12-05-09','a','FTVOTBorders','2afc_speech')


exp7 = celldatabase.Experiment(subject, '2022-03-01', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='middlelateralDiI', info=['middlelateralDiI', 'soundRight']) #reference = external
experiments.append(exp7)
# 14:45 in booth
# 15:00 in brain
# 15:07 reached max depth
# 15:26 started recording
# 16:22 Done

exp7.add_site(2958)
exp7.maxDepth = 2958
exp7.add_session('15-26-30','a','AM','am_tuning_curve') 
exp7.add_session('15-33-50','b','pureTones','am_tuning_curve') # fell asleep for the last ~100 trials or so of pure tones
exp7.add_session('15-50-18','a','FTVOTBorders','2afc_speech')


exp8 = celldatabase.Experiment(subject, '2022-03-02', brainArea='AC_left', probe = 'NPv1-8131', recordingTrack='caudolateralDiD', info=['caudolateralDiD', 'soundRight']) #reference = external
experiments.append(exp8)
# 12:45 in booth
# 12:55 lowered electrodes, couldn't penetrate caudolateral part of craniotomy, cleaned that corner of craniotomy
# 13:07 in brain
# 13:10 reached max depth
# 13:32 started recording
# 14: done

exp8.add_site(2973)
exp8.maxDepth = 2973
exp8.add_session('13-32-16','a','AM','am_tuning_curve') 
exp8.add_session('13-39-58','b','pureTones','am_tuning_curve')
exp8.add_session('13-58-01','a','FTVOTBorders','2afc_speech')

