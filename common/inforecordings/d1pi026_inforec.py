from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'd1pi026'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-07-03', 'right_AudStr', info=['FacingPosterior', 'Anterior'])
experiments.append(exp0)
#Used left speaker; 2.5 mW for laser; probe DAF8; Rig 1

exp0.laserCalibration = {
    '0.51':1.50,
    '1.0':2.70,
    '1.5':4.2,
    '1.99':5.98,
    '2.5':7.28,
    '3.01':9.28,
}

#Tetrode 5 has reference; threshold set to 55mV
exp0.add_site(2073, tetrodes=[3,4,6,7,8])
exp0.add_session('12-10-39', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(2180, tetrodes=[3,8])
exp0.add_session('12-19-13', None, 'noiseburst', 'am_tuning_curve')
#Threshold was set to 44mV

exp0.add_site(2502, tetrodes=[3,8])
exp0.add_session('12-19-13', None, 'noiseburst', 'am_tuning_curve')

exp0.maxDepth = 2502

exp1 = celldatabase.Experiment(subject, '2018-07-05', 'right_AudStr', info=['FacingPosterior', 'AnteriorMid'])
experiments.append(exp1)

#Used left speaker; 2.5 mW for laser; probe DAF8; Rig 1

exp1.laserCalibration = {
    '0.5':0.8,
    '1.0':1.30,
    '1.5':1.8,
    '2.0':2.35,
    '2.5':2.9,
    '3.0':3.70,
    '3.5':4.45,
    '4.0':5.30
}

#Tetrode 3 has reference; threshold set to 55mV
exp1.add_site(2904, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('13-19-10', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-25-00', None, 'lasertrain', 'am_tuning_curve')

#Tetrode 5 has reference
exp1.add_site(2950, tetrodes=[1,2,3,4,6,8])
exp1.add_session('13-37-48', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-39-29', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-46-07', None, 'laserpulse', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[1,2,3,4,6,8]) #While lowering, the noise completely faded out. Cause unknown
exp1.add_session('13-56-13', None, 'noiseburst', 'am_tuning_curve')
#No response in ephys whatsoever. Experiment was ended for the day as the cause was unknown.Raising the probe caused no response to return either

exp1.maxDepth = 3000

# exp2 = celldatabase.Experiment(subject, '2018-07-06', 'right_AudStr', info=['FacingPosterior', 'PosteriorMid'])
# experiments.append(exp2)
#
# #Used left speaker; 2.5 mW for laser; probe DAF8; Rig 1
#
# exp2.laserCalibration = {
#     '0.5':0.80,
#     '1.0':1.20,
#     '1.5':1.65,
#     '2.0':2.15,
#     '2.5':2.70,
#     '3.0':3.50,
#     '3.5':4.30,
#     '4.0':5.20
# }
#There is an odd affect of noise similar to what Ale was experiencing before the rig was fixed.
#Mouse was removed
#Probe seems to be the issue, it broke upon removal so we are unable to investigat ethe probe specifically

exp3 = celldatabase.Experiment(subject, '2018-07-09', 'right_AudStr', info=['FacingPosterior', 'PosteriorMid'])
experiments.append(exp3)

#Used left speaker; 2.5 mW for laser; probe DAF9; Rig 1

exp3.laserCalibration = {
    '0.5':1.0,
    '1.0':1.6,
    '1.5':2.3,
    '2.0':3.1,
    '2.5':4.2,
    '3.0':5.15,
    '3.5':6.15,
    '4.0':6.9
}

#When the probewas first inserted and then removed, some tissue dame out with it and stuck. This was washed away y sooking in saline and removng with the needle, but could jave an affect on the impedance
#Tetrode 5 has reference; threshold set to 55mV
exp3.add_site(2900, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('13-53-22', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-58-35', None, 'laserPulse', 'am_tuning_curve')# initial burst on raster, but no second line so likey not caused by photoelectric effect
exp3.add_session('14-10-46', None, 'laserTrain', 'am_tuning_curve')#two possible light sensitive neurons, both on tetrode 3

exp3.add_site(2950, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('14-25-33', None, 'noiseburst', 'am_tuning_curve')
#In an effort to find a sound responsie cell, I'm moving on without testing light sensitivity

exp3.add_site(3000, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('14-30-57', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-34-26', None, 'tc', 'am_tuning_curve')

exp3.add_site(3050, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('14-30-57', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-43-53', None, 'laserPulse', 'am_tuning_curve')

exp3.add_site(3100, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('14-50-09', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-53-27', None, 'am', 'am_tuning_curve')

exp3.add_site(3150, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('15-01-30', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-08-36', None, 'noiseburst', 'am_tuning_curve')#6 now has reference Had spike on reference, so it's beng retested

#7 has the reference
exp3.add_site(3200, tetrodes=[1,2,3,4,5,8])
exp3.add_session('15-15-22', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-19-13', None, 'am', 'am_tuning_curve')

exp3.add_site(3250, tetrodes=[1,2,3,4,5,8])
exp3.add_session('15-38-05', None, 'noiseburst', 'am_tuning_curve')

#5 has the reference
exp3.add_site(3300, tetrodes=[1,2,3,7,8])
exp3.add_session('15-45-06', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-47-28', None, 'tc', 'am_tuning_curve')
exp3.add_session('15-47-28', None, 'am', 'am_tuning_curve')

exp3.maxDepth = 3300

exp4 = celldatabase.Experiment(subject, '2018-07-12', 'right_AudStr', info=['FacingPosterior', 'PosteriorMid'])
experiments.append(exp4)

#Used left speaker; 2.5 mW for laser; probe DAF9; Rig 1

exp4.laserCalibration = {
    '0.5':1.0,
    '1.0':1.6,
    '1.5':2.3,
    '2.0':3.0,
    '2.5':3.8,
    '3.0':4.8,
    '3.5':5.85,
    '4.0':6.65
}

#Aborted due to hemorrhaging after cleaning the craniotomy. Gel foam was needed to reduce the bleeding and was left under the silguard
