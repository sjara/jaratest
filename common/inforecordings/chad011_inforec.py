from jaratoolbox import celldatabase

subject = 'chad011' 
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-12-26', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('14-44-31', None, 'noiseburst', 'am_tuning_curve')
#Santiago deleted spikes data file.

#The most anterior shank touched the surface of the brain before the other shanks; the probe was zeroed when all four shanks touched the surface of brain.

exp0 = celldatabase.Experiment(subject, '2018-12-27', 'right_AC', info=['midLateralDiD' 'facingAnterior' 'soundLeft'])
#The probe is near the anterior limit of the craniotomy.
experiments.append(exp0)

exp0.add_site(1112.1, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('13-35-48', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-35-48', None, 'noiseburst', 'am_tuning_curve')

exp0 = celldatabase.Experiment(subject, '2019-01-01', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
#The probe is near the anterior limit of the craniotomy.
experiments.append(exp0)

exp0.add_site(1000, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('14-29-34', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-29-34', None, 'noiseburst', 'am_tuning_curve')
#I suspect some of the upper layer of the cortex may have been scrambled when the craniotomy was created and perhaps subsequently while removing excess tissue over the brain prior to doing recordings. For this reason I chose to begin recording at 1000 instead of 1100, figuring I may be deeper in the brain than would normally be expected at that depth.

exp0.add_site(1003, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('15-04-36', 'b', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-04-36', None, 'noiseburst', 'am_tuning_curve')

exp0 = celldatabase.Experiment(subject, '2019-01-08', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#Reference is set to channel 18 (i.e. Tetrode 1, electrode 1)
#exp0.add_session('15-36-00', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-36-00', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(1101, tetrodes=[1,2,3,4,5,7,8])
#Reference is set to channel 12. 
#exp0.add_session('16-19-21', 'b', 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-19-21', None, 'noiseburst', 'am_tuning_curve')

exp0 = celldatabase.Experiment(subject, '2019-01-11', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1200, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('15-08-06', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-08-06', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(1250, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('15-35-10', 'b', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-35-10', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('16-19-21', 'c', 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-19-21', None, 'noiseburst', 'am_tuning_curve')

#exp0.add_session('16-30-34', 'd', 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-30-34', None, 'noiseburst', 'am_tuning_curve')

exp0 = celldatabase.Experiment(subject, '2019-01-15', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1150, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('15-34-37', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-34-37', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(1245, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('15-49-53', 'b', 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-49-53', None, 'noiseburst', 'am_tuning_curve')
#I'm not seeing much signal to indicate the presence of neurons; I suspect the probe is too far posterior.

exp0 = celldatabase.Experiment(subject, '2019-01-17', 'right_AC', info=['midMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1100, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('11-52-53', 'a', 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-52-53', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(1150, tetrodes=[1,2,3,4,5,7,8])
#exp0.add_session('12-21-37', 'b', 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-21-37', None, 'noiseburst', 'am_tuning_curve')

