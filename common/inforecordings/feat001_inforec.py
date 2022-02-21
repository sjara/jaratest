from jaratoolbox import celldatabase

subject = 'feat001'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (penetrationLocationAndDye),
#    info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.

exp0 = celldatabase.Experiment(subject, '2021-11-03', brainArea='AC_right', probe = 'NPv1-2881', info=['facesRight', 'soundLeft']) #reference = tip
experiments.append(exp0)
exp0.add_site(3314) # 3314.0
exp0.maxDepth = 3314
exp0.add_session('14-29-00','a','pureTones','am_tuning_curve') #not very PT responsive
exp0.add_session('14-37-10','b','AM','am_tuning_curve') #AM responsive (and looks to be phaselocking up to ~60Hz)

exp1 = celldatabase.Experiment(subject, '2021-11-09', brainArea='AC_right', probe = 'NPv1-2881',info=['facesRight', 'soundLeft']) #reference = tip
experiments.append(exp1)
# In booth 12:00pm
# Touch brain @ 12:15
# Santiago played with spikes... until we stopped :)
# Stopped at 3242 at 1:20
#
exp1.add_site(3242) #3242.2
exp1.maxDepth = 3242
exp1.add_session('13-29-05','a','AMtest','am_tuning_curve') #1 min recording presenting AM at 8Hz
exp1.add_session('13-50-09','b','pureTones','am_tuning_curve')
exp1.add_session('14-05-35','c','AM','am_tuning_curve')
#exp1.add_session('14-14-45',,'FT','2afc_speech') #forgot to change isi
exp1.add_session('14-16-37','a','FT','2afc_speech') # 2 stimuli
#exp1.add_session('14-29-00','','VOT','2afc_speech') #lost saline
#exp1.add_session('14-31-22','','VOT','2afc_speech') #typo on behav paradigm ISI. need to restart
exp1.add_session('14-32-18','b','VOT','2afc_speech') # 2 stimuli


# Note: For sessions 0 and 1, animal had name of pals027. From here forward, named feat001.

exp2 = celldatabase.Experiment(subject, '2021-11-11', brainArea='AC_right', probe = 'NPv1-2881', recordingTrack='lateral_DiI', info=['facesRight', 'soundLeft']) #reference = tip
experiments.append(exp2)
# In booth 12:15
# Touch brain @ 12:30
# Stopped at 3513.4 @12:53
# Done recording @ 2:05
#
exp2.add_site(3513) #3513.4
exp2.maxDepth = 3513
exp2.add_session('13-14-41','a','pureTones','am_tuning_curve')
exp2.add_session('13-30-04','b','AM','am_tuning_curve') # 2 stimuli
exp2.add_session('13-37-55','a','VOT','2afc_speech') # 2 stimuli
#exp2.add_session('13-51-37','b','FT','2afc_speech') #forgot to change mode to passive exposure. ISI was not acting right when I tried switching to passive after I hit start.
exp2.add_session('13-53-20','b','FT','2afc_speech')



exp3 = celldatabase.Experiment(subject, '2021-11-16', brainArea='AC_left', probe = 'NPv1-2881', recordingTrack='anteromedial_DiD', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp3)
#3:26 touched brain
#3:39 reached maxDepth
#3:58 Started recording
#4:45 Done recording
exp3.add_site(3532) #3532.6
exp3.maxDepth = 3532
exp3.add_session('15-58-31','a','AM','am_tuning_curve')
#exp3.add_session('16-06-22','b','pureTones','am_tuning_curve') #lost saline
exp3.add_session('16-10-10','b','pureTones','am_tuning_curve')
exp3.add_session('16-22-10','a','FT','2afc_speech') # 2 stimuli
exp3.add_session('16-34-17','b','VOT','2afc_speech') # 2 stimuli


exp4 = celldatabase.Experiment(subject, '2021-11-17', brainArea='AC_left', probe = 'NPv1-2881', recordingTrack='caudomedial_DiI', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp4)
#11:10 in booth
#11:15 touched brain
#11:27 reached maxDepth
#11:43 Started recording
#12:42 Done recording
exp4.add_site(3408) #3408.6
exp4.maxDepth = 3408
exp4.add_session('11-43-40','a','pureTones','am_tuning_curve')
exp4.add_session('11-58-54','b','AM','am_tuning_curve')
#exp4.add_session('12-06-31','a','VOT','2afc_speech') #lost saline partway through
exp4.add_session('12-19-03','b','FT','2afc_speech') # 2 stimuli
exp4.add_session('12-30-49','c','VOT','2afc_speech') # 2 stimuli


exp5 = celldatabase.Experiment(subject, '2021-11-18', brainArea='AC_left', probe = 'NPv1-2881', recordingTrack='middlelateral_DiD', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp5)
#11:15 in booth
#11:20 touched brain
#11:25 reached maxDepth
#11:41 Started recording
#12:24 Done recording
exp5.add_site(3563) #3563.0
exp5.maxDepth = 3563
exp5.add_session('11-41-15','a','AM','am_tuning_curve')
exp5.add_session('11-48-19','b','pureTones','am_tuning_curve')
exp5.add_session('12-01-03','a','VOT','2afc_speech') # 2 stimuli
exp5.add_session('12-13-26','b','FT','2afc_speech') # 2 stimuli


exp6 = celldatabase.Experiment(subject, '2021-11-19', brainArea='AC_left', probe = 'NPv1-2881', recordingTrack='anterolateral_DiI', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp6)
#12:35 in booth
#12:40 touched brain
#12:45 Open-ephys crashed and can't get it to reopen.
#12:50 Fixed open-ephys problem. The issue was the probe had been unplugged
#12:58 reached maxDepth
#1:28 Started recording
#2:15 Done recording
exp6.add_site(3320) #3320.5
exp6.maxDepth = 3320
#exp6.add_session('13-27-17','a','pureTones','am_tuning_curve') #lost saline
exp6.add_session('13-28-26','a','pureTones','am_tuning_curve')
exp6.add_session('13-43-41','b','AM','am_tuning_curve')
exp6.add_session('13-50-57','a','FT','2afc_speech') # 2 stimuli
exp6.add_session('14-02-49','b','VOT','2afc_speech') # 2 stimuli

exp7 = celldatabase.Experiment(subject, '2021-11-19', brainArea='AC_left', probe = 'NPv1-2881', recordingTrack='caudolateral_DiI', info=['facesLeft', 'soundRight']) #reference = tip
experiments.append(exp7)
#3:15 in booth
#3:20 touched brain
#3:25 reached maxDepth
#3:42 Started recording
#4:32 Done recording
exp7.add_site(3434) #3434.2
exp7.maxDepth = 3434
exp7.add_session('15-42-54','c','AM','am_tuning_curve')
exp7.add_session('15-50-18','d','pureTones','am_tuning_curve')
exp7.add_session('16-06-24','c','VOT','2afc_speech') #psycurve mode w/4 stimulicd
exp7.add_session('16-20-10','d','FT','2afc_speech') #psycurve mode w/4 stimuli
