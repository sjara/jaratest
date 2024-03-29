from jaratoolbox import celldatabase

subject = 'feat001'
experiments = []

# Experiment parameters: subject, date, brainArea, recordingTrack (which is penetrationLocationAndDye), info (which contains [probeOrientation, soundSource, probeConfiguration]).
# Session parameters: sessionTime, behaviorFileSuffix, sessionType paradigmName.


exp0 = celldatabase.Experiment(subject, '2021-11-03', brainarea='rightAC', info = ['eRight', 'soundLeft','NPv1-']) #reference = tip
experiments.append(exp0)
exp0.add_site(3314.0)
exp0.add_session('14-29-00','a','pureTones','am_tuning_curve') #not very PT responsive
exp0.add_session('14-27-10','b','AM','am_tuning_curve') #AM responsive (and looks to be phaselocking up to ~60Hz)

exp1 = celldatabase.Experiment(subject, '2021-11-09', brainarea = 'rightAC', info = ['FacesRight', 'soundLeft','NPv1-']) #reference = tip
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
exp1.add_session('14-16-37','a','FT','2afc_speech') 
#exp1.add_session('14-29-00','','VOT','2afc_speech') #lost saline
#exp1.add_session('14-31-22','','VOT','2afc_speech') #typo on behav paradigm ISI. need to restart
exp1.add_session('14-32-18','b','VOT','2afc_speech')


# Note: For sessions 0 and 1, animal had name of pals027. From here forward, named feat001.

exp2 = celldatabase.Experiment(subject, '2021-11-11', brainarea = 'rightAC', info = ['lateralDiI','facesRight', 'soundLeft','NPv1-']) #reference = tip
experiments.append(exp2)
# In booth 12:15
# Touch brain @ 12:30
# Stopped at 3513.4 @12:53
# Done recording @ 2:05
# 
exp2.add_site(3513) #3513.4
exp2.maxDepth = 3513
exp2.add_session('13-14-41','a','pureTones','am_tuning_curve')
exp2.add_session('13-30-04','b','AM','am_tuning_curve')
exp2.add_session('13-37-55','a','VOT','2afc_speech')
#exp2.add_session('13-51-37','b','FT','2afc_speech') #forgot to change mode to passive exposure. ISI was not acting right when I tried switching to passive after I hit start.
exp2.add_session('13-53-20','b','FT','2afc_speech')


