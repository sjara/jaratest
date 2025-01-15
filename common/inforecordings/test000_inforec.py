#Making an inforec
from jaratoolbox import celldatabase
import importlib
importlib.reload(celldatabase)


subject = 'feat005'
experiments = []


exp0 = celldatabase.Experiment(subject, '2022-02-07', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='anterolateralDiI', info=['anterolateralDiI', 'soundRight']) #reference = external
experiments.append(exp0)

exp0.add_site(3020)
exp0.maxDepth = 3020
#exp0.add_session('12-34-34','a','pureTones','am_tuning_curve') #got noisy, if have time at end, redo puretones. presented binaurally.
exp0.add_session('12-52-53','b','AM','am_tuning_curve') #presented binaurally.
exp0.add_session('13-03-30','a','FTVOTBorders','2afc_speech') #presented right
exp0.add_session('13-35-09','c','pureTones','am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2022-02-08', brainArea='AC_left', probe = 'NPv1-2761', recordingTrack='anteromedialDiD', info=['anteromedialDiD', 'soundRight']) #reference = tip
experiments.append(exp1)

exp1.add_site(3005)
exp1.maxDepth = 3005
exp1.add_session('15-20-39','a','pureTones','am_tuning_curve')
exp1.add_session('15-36-32','b','AM','am_tuning_curve')
exp1.add_session('15-45-22','a','FTVOTBorders','2afc_speech')




exp4 = celldatabase.Experiment(subject, '2022-02-11', brainArea='AC_right',
                               probe = 'NPv1-8131', recordingTrack='anterolateralDiI',
                               info=['anterolateralDiI', 'soundLeft']) #reference = external
experiments.append(exp4)

exp4.add_site(3154)
exp4.maxDepth = 3154
exp4.add_session('10-20-41','a','pureTones','am_tuning_curve')
exp4.add_session('10-36-40','b','AM','am_tuning_curve')
exp4.add_session('10-45-54','a','FTVOTBorders','2afc_speech')


exp5 = celldatabase.Experiment(subject, '2022-02-14', brainArea='AC_right',
                               probe = 'NPv1-8131', recordingTrack='anterolateralDiD',
                               info=['anterolateralDiD', 'soundLeft']) #reference = external
experiments.append(exp5)

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



'''
subject = 'feat001'
experiments=[]


exp3 = celldatabase.Experiment(subject, '2021-11-16', brainArea='left_AC', probe = 'NPv1-2881', recordingTrack='anteromedial_DiD', info=['facesLeft', 'soundRight']) #reference = tip
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


exp4 = celldatabase.Experiment(subject, '2021-11-17', brainArea='left_AC', probe = 'NPv1-2881', recordingTrack='caudomedial_DiI', info=['facesLeft', 'soundRight']) #reference = tip
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


exp5 = celldatabase.Experiment(subject, '2021-11-18', brainArea='left_AC', probe = 'NPv1-2881', recordingTrack='middlelateral_DiD', info=['facesLeft', 'soundRight']) #reference = tip
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


exp6 = celldatabase.Experiment(subject, '2021-11-19', brainArea='left_AC', probe = 'NPv1-2881', recordingTrack='anterolateral_DiI', info=['facesLeft', 'soundRight']) #reference = tip
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



exp7 = celldatabase.Experiment(subject, '2021-11-19', brainArea='left_AC', probe = 'NPv1-2881', recordingTrack='caudolateral_DiI', info=['facesLeft', 'soundRight']) #reference = tip
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
'''


'''
'''





'''
subject = 'test000'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-06-25', 'right_AudStr', info=['posteriorDiD', 'FacingPosterior'])
experiments.append(exp0)
#Comment about speakers used, power of laser, and specific probe used

exp0.laserCalibration = {
'OutputDecimal':LevelDecimal
#0.5-4.0
}

#tetrode 6 is the reference, threshold is
exp0.add_site(2500, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('12-26-26', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-31-02', None, 'laser', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('12-41-13', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-43-43', None, 'laser', 'am_tuning_curve')
exp0.add_session('12-50-44', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-58-17', 'b', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('14-36-29', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-41-19', None, 'laser', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('14-36-29', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-41-19', None, 'laser', 'am_tuning_curve')

exp0.maxDepth = 2600
'''
