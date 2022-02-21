from jaratoolbox import celldatabase

subject = 'feat005'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2022-02-07', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='anterolateralDiI', info=['anterolateralDiI', 'soundRight']) #reference = external
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
exp0.add_session('13-35-09','c','pureTones','am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2022-02-08', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='anteromedialDiD', info=['anteromedialDiD', 'soundRight']) #reference = tip
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

#exp2 = celldatabase.Experiment(subject, '2022-02-09', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='middlemedialDiI', info=['middlemedialDiD', 'soundRight']) #reference = tip
#experiments.append(exp2)
# 13:10 in booth
# 13:20 lowered electrodes, couldn't penetrate brain. Tried cleaning craniotomy some
# 14:41 Couldn't penetrate still after cleaning Ending recording.

#exp3 = celldatabase.Experiment(subject, '2022-02-10', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='middleDiD', info=['middleDiD', 'soundRight']) #reference = tip
#experiments.append(exp3)
# 11:20 in booth
# 11:25 lowered electrodes
# 12:11 couldn't penetrate brain. ended session.

exp4 = celldatabase.Experiment(subject, '2022-02-11', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='anterolateralDiI', info=['anterolateralDiI', 'soundLeft']) #reference = external
experiments.append(exp4)
# 9:01 in booth
# 9:03 lowered electrodes
# Couldn't penetrate brain. Cleaned up craniotomy. Some dura was present, was able to remove.
# 9:58 tried lowering electrodes again, in brain!
# 10:00 reached max depth
# 10:20 started recording
# 11:17 done

exp4.add_site(3154)
exp4.maxDepth = 3154
exp4.add_session('10-20-41','a','pureTones','am_tuning_curve')
exp4.add_session('10-36-40','b','AM','am_tuning_curve')
exp4.add_session('10-45-54','a','FTVOTBorders','2afc_speech')

exp5 = celldatabase.Experiment(subject, '2022-02-14', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='anterolateralDiD', info=['anterolateralDiD', 'soundLeft']) #reference = external
experiments.append(exp5)
# 11:38 in booth
# 11:43 lowered electrodes, in brain
# 11:45 reached max depth
# 12:05 started recording
# 1:10 done

exp5.add_site(2959)
exp5.maxDepth = 2959
exp5.add_session('12-07-29','a','pureTones','am_tuning_curve')
exp5.add_session('12-23-06','b','AM','am_tuning_curve')
exp5.add_session('12-31-43','a','FTVOTBorders','2afc_speech')


exp6 = celldatabase.Experiment(subject, '2022-02-15', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='caudomedialDiI', info=['caudomedialDiI', 'soundLeft']) #reference = external
experiments.append(exp6)
# 12:35 in booth
# 12:40 shaved off medial edge of R well to get better access across craniotomy
# 12:53 lowered electrodes, in brain
# 12:57 reached max depth
# 1:17 started recording
# 2:20 done

exp6.add_site(2983)
exp6.maxDepth = 2983
exp6.add_session('13-17-47','a','pureTones','am_tuning_curve')
exp6.add_session('13-34-44','b','AM','am_tuning_curve')
exp6.add_session('13-44-06','a','FTVOTBorders','2afc_speech')

exp7 = celldatabase.Experiment(subject, '2022-02-16', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='caudomedialDiD', info=['caudomedialDiD', 'soundLeft']) #reference = external
experiments.append(exp7)
# 1:45 in booth
# 1:53 lowered electrodes, in brain
# 2:05 reached max depth
# 2:25 started recording
# 3:22 done

exp7.add_site(2986)
exp7.maxDepth = 2986
exp7.add_session('14-25-31','a','AM','am_tuning_curve')
exp7.add_session('14-34-22','b','pureTones','am_tuning_curve')
exp7.add_session('14-51-25','a','FTVOTBorders','2afc_speech')

#exp8 = celldatabase.Experiment(subject, '2022-02-17', brainArea='AC_right', probe = 'NPv1-8131', recordingTrack='DiI', info=['DiI', 'soundLeft']) #reference = external
#experiments.append(exp8)
# 12:02 in booth
# 12:05 lowered electrodes, couldn't penetrate brain
# 12:30 tried cleaning craniotomy and penetrating again, still couldn't get in brain. cancelled recording
