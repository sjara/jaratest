from jaratoolbox import celldatabase

subject = 'chad011' 
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-12-26', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('14-44-31', None, 'noiseburst', 'am_tuning_curve')
#Santiago deleted spikes data file.
#The most anterior shank touched the surface of the brain before the other shanks; the probe was zeroed when all four shanks touched the surface of brain.

exp0.maxDepth = 1100

exp1 = celldatabase.Experiment(subject, '2018-12-27', 'right_AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
#The probe is near the anterior limit of the craniotomy.
experiments.append(exp1)

exp1.add_site(1112.1, tetrodes=[1,2,3,4,5,7,8])
#exp1.add_session('13-35-48', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp1.maxDepth = 1112.1

exp2 = celldatabase.Experiment(subject, '2019-01-01', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
#The probe is near the anterior limit of the craniotomy.
experiments.append(exp2)

exp2.add_site(1000, tetrodes=[1,2,3,4,5,7,8])
#exp2.add_session('14-29-34', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#I suspect some of the upper layer of the cortex may have been scrambled when the craniotomy was created and perhaps subsequently while removing excess tissue over the brain prior to doing recordings. For this reason I chose to begin recording at 1000 instead of 1100, figuring I may be deeper in the brain than would normally be expected at that depth.
#Raster plot does not show clear indication of cell presence.

exp2.add_site(1003, tetrodes=[1,2,3,4,5,7,8])
#exp2.add_session('15-04-36', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Raster plot does not show clear indication of cell presence.

exp2.maxDepth = 1003

exp3 = celldatabase.Experiment(subject, '2019-01-08', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp3)

exp3.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
exp3.add_session('15-36-00', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Reference is set to channel 18 (i.e. Tetrode 1, electrode 1)
#Raster plot does not show clear indication of cell presence.

exp3.add_site(1101, tetrodes=[1,2,3,4,5,7,8])
#exp3.add_session('16-19-21', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Reference is set to channel 12. 
#Raster plot does not show clear indication of cell presence.

exp3.maxDepth = 1101

exp4 = celldatabase.Experiment(subject, '2019-01-11', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp4)

exp4.add_site(1200, tetrodes=[1,2,3,4,5,7,8])
#exp4.add_session('15-08-06', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp4.add_site(1250, tetrodes=[1,2,3,4,5,7,8])
#exp4.add_session('15-35-10', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Raster plot does not show clear indication of cell presence.

exp4.add_site(1300, tetrodes=[1,2,3,4,5,7,8])
#exp4.add_session('16-19-21', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'c'
#Raster plot does not show clear indication of cell presence.

#exp4.add_session('16-30-34', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'd'
#Raster plot does not show clear indication of cell presence.

exp4.maxDepth = 1300

exp5 = celldatabase.Experiment(subject, '2019-01-15', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp5)

exp5.add_site(1150, tetrodes=[1,2,3,4,5,7,8])
#exp5.add_session('15-34-37', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp5.add_site(1245, tetrodes=[1,2,3,4,5,7,8])
#exp5.add_session('15-49-53', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#I'm not seeing much signal to indicate the presence of neurons; I suspect the probe is too far posterior.

exp5.maxDepth = 1245

exp6 = celldatabase.Experiment(subject, '2019-01-17', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp6)

exp6.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#exp6.add_session('11-52-53', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp6.add_site(1150, tetrodes=[1,2,3,4,5,7,8])
#exp6.add_session('12-21-37', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Raster plot does not show clear indication of cell presence.

exp6.maxDepth = 1150

exp7 = celldatabase.Experiment(subject, '2019-01-22', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp7)
#Using probe: C39A

exp7.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#exp7.add_session('15-27-49', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp7.add_site(1125, tetrodes=[2,8])
#exp7.add_session('15-56-05', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Raster plot does not show clear indication of cell presence.

exp7.maxDepth = 1125

exp8 = celldatabase.Experiment(subject, '2019-01-25', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp8)
#Using probe: C39A

exp8.add_site(1200, tetrodes=[4,5,6])
exp8.add_session('15-24-17', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Reference set to 28 (Tetrode 1, channel 3)
#Potential presence of non-sound-responsive cell.

exp8.add_site(1250, tetrodes=[2,4,5,6])
exp8.add_session('15-36-33', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Reference set to 25 (Tetrode 3, channel 1)
#Potential presence of non-sound-responsive cell (especially on tetrode 6).

exp8.add_site(1300, tetrodes=[5])
#exp8.add_session('15-56-56', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'c'
#Reference set to 25 (Tetrode 3, channel 1)
#Raster plot does not show clear indication of cell presence.

exp8.add_site(1350, tetrodes=[5])
#exp8.add_session('16-02-53', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'd'
#Reference set to 25 (Tetrode 3, channel 1)
#Raster plot does not show clear indication of cell presence.

exp8.add_site(1550, tetrodes=[1,2,3,4,5,6,7,8])
exp8.add_session('17-10-49', 'e', 'tc', 'am_tuning_curve')
#Reference set to 17 (Tetrode 4, channel 2)
#Potential presence of sound-responsive cell.

exp8.add_session('17-28-15', 'f', 'tc', 'am_tuning_curve')
#Reference set to 17 (Tetrode 4, channel 2)

exp8.maxDepth = 1550

exp9 = celldatabase.Experiment(subject, '2019-03-05', 'left_AC', info=['midMedialDiD' 'facingPosterior' 'soundLeft'])
experiments.append(exp9)
#Using probe: C39C

exp9.add_site(1100, tetrodes=[2,3,4,6])
exp9.add_session('16-18-24', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Reference set to 14 (Tetrode 5, channel 1)
#Potential presence of sound responsive cell.

exp9.add_session('16-42-45', 'b', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)
#Potential presence of sound responsive cell on tetrode 2.

exp9.add_site(1105, tetrodes=[2,3,4,6])
exp9.add_session('17-24-48', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'c'
#Reference set to 14 (Tetrode 5, channel 1)
#Indication of sound responsive cell on tetrode 2.

exp9.add_session('17-30-52', 'd', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)
#Indication of frequency preference cell on tetrode 2.

exp9.add_site(1106, tetrodes=[2,3,4,6])
exp9.add_session('17-43-49', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'e'
#Reference set to 14 (Tetrode 5, channel 1)

exp9.add_session('17-48-23', 'f', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)

exp9.maxDepth = 1106

exp10 = celldatabase.Experiment(subject, '2019-04-05', 'left_AC', info=['midLateralDiD' 'facingPosterior' 'soundLeft'])
experiments.append(exp10)
#Using probe: C39C
#Probe inserted: 2:10pm

exp10.add_site(1100, tetrodes=[3,4,6])
#exp10.add_session('14-51-12', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Reference set to 14 (Tetrode 5, channel 1)
#Raster plot does not show good indication of cell presence

#exp10.add_session('15-12-51', 'b', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)
#Raster plot does not show good indication of cell presence

#I keep getting noise on tetrodes 3,4,6 that looks like cells in the spike detector but the fluctuations in the lfp match across channels from said tetrodes.

exp10.maxDepth = 1500

exp11 = celldatabase.Experiment(subject, '2019-04-08', 'left_AC', info=['midMedialDiD' 'facingPosterior' 'soundLeft'])
experiments.append(exp11)
#Using probe: C39C
#Probe inserted: 3:10pm

#Lots of noise with fluctuations in the lfp matching across channels.

exp11.maxDepth = 1500
