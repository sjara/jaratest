from jaratoolbox import celldatabase


subject = 'd1pi026'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-07-03', 'right_AudStr',
                               recordingTrack='Anterior', probe='A4x2-tet',
                               info=['FacingPosterior'])
#experiments.append(exp0)
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
# exp0.add_site(2073, egroups=[3,4,6,7,8])
# exp0.add_session('12-10-39', None, 'noiseburst', 'am_tuning_curve')

# exp0.add_site(2180, egroups=[3,8])
# exp0.add_session('12-19-13', None, 'noiseburst', 'am_tuning_curve')
#Threshold was set to 44mV

# exp0.add_site(2502, egroups=[3,8])
# exp0.add_session('12-19-13', None, 'noiseburst', 'am_tuning_curve')

exp0.maxDepth = 2502

exp1 = celldatabase.Experiment(subject, '2018-07-05', 'right_AudStr',
                               recordingTrack='AnteriorMid', probe='A4x2-tet',
                               info=['FacingPosterior'])
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
exp1.add_site(2904, egroups=[1,2,4,5,6,7,8])
exp1.add_session('13-19-10', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-25-00', None, 'lasertrain', 'am_tuning_curve')

#Tetrode 5 has reference
exp1.add_site(2950, egroups=[1,2,3,4,6,8])
exp1.add_session('13-37-48', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-39-29', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-46-07', None, 'laserpulse', 'am_tuning_curve')

# exp1.add_site(3000, egroups=[1,2,3,4,6,8]) #While lowering, the noise completely faded out. Cause unknown
# exp1.add_session('13-56-13', None, 'noiseburst', 'am_tuning_curve')
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

exp3 = celldatabase.Experiment(subject, '2018-07-09', 'right_AudStr',
                               recordingTrack='PosteriorMid', probe='A4x2-tet',
                               info=['FacingPosterior'])
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

#When the probe was first inserted and then removed, some tissue came out with it and stuck. This was washed away y sooking in saline and removng with the needle, but could jave an affect on the impedance
#Tetrode 5 has reference; threshold set to 55mV
exp3.add_site(2900, egroups=[1,2,3,4,6,7,8])
exp3.add_session('13-53-22', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-58-35', None, 'laserPulse', 'am_tuning_curve')# initial burst on raster, but no second line so likey not caused by photoelectric effect
exp3.add_session('14-10-46', None, 'laserTrain', 'am_tuning_curve')#two possible light sensitive neurons, both on tetrode 3

# exp3.add_site(2950, egroups=[1,2,3,4,6,7,8])
# exp3.add_session('14-25-33', None, 'noiseburst', 'am_tuning_curve')
#In an effort to find a sound responsive cell, I'm moving on without testing light sensitivity

# exp3.add_site(3000, egroups=[1,2,3,4,6,7,8])
# exp3.add_session('14-30-57', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('14-34-26', None, 'tc', 'am_tuning_curve')

exp3.add_site(3050, egroups=[1,2,3,4,6,7,8])
exp3.add_session('14-30-57', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('14-43-53', None, 'laserPulse', 'am_tuning_curve')

# exp3.add_site(3100, egroups=[1,2,3,4,6,7,8])
# exp3.add_session('14-50-09', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('14-53-27', None, 'am', 'am_tuning_curve')

exp3.add_site(3150, egroups=[1,2,3,4,8])
exp3.add_session('15-01-30', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-08-36', None, 'noiseburst', 'am_tuning_curve')#6 now has reference Had spike on reference, so it's beng retested

#7 has the reference
# exp3.add_site(3200, egroups=[1,2,3,4,5,8])
# exp3.add_session('15-15-22', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('15-19-13', None, 'am', 'am_tuning_curve')

exp3.add_site(3250, egroups=[1,2,3,4,5,8])
exp3.add_session('15-38-05', None, 'noiseburst', 'am_tuning_curve')

#5 has the reference
# exp3.add_site(3300, egroups=[1,2,3,7,8])
# exp3.add_session('15-45-06', None, 'noiseburst', 'am_tuning_curve')
# exp3.add_session('15-47-28', None, 'tc', 'am_tuning_curve')
# exp3.add_session('15-47-28', None, 'am', 'am_tuning_curve')

exp3.maxDepth = 3300

# exp4 = celldatabase.Experiment(subject, '2018-07-12', 'right_AudStr', info=['FacingPosterior', 'PosteriorMid'])
# experiments.append(exp4)
#
# #Used left speaker; 2.5 mW for laser; probe DAF9; Rig 1
#
# exp4.laserCalibration = {
#     '0.5':1.0,
#     '1.0':1.6,
#     '1.5':2.3,
#     '2.0':3.0,
#     '2.5':3.8,
#     '3.0':4.8,
#     '3.5':5.85,
#     '4.0':6.65
# }

#Aborted due to hemorrhaging after cleaning the craniotomy. Gel foam was needed to reduce the bleeding and was left under the silguard

exp5 = celldatabase.Experiment(subject, '2018-07-24', 'left_AudStr',
                               recordingTrack='Anterior', probe='A4x2-tet',
                               info=['FacingPosterior', 'Anterior'])
experiments.append(exp5)

#Used left speaker; 2.5 mW for laser; probe D621 Rig 1; DiD

exp5.laserCalibration = {
    '0.5':0.90,
    '1.0':1.50,
    '1.5':2.25,
    '2.0':2.95,
    '2.5':3.95,
    '3.0':4.90,
    '3.5':6.00,
    '4.0':6.75
}

#Tetrode 6 has reference; threshold set to 55mV
exp5.add_site(2900, egroups=[1,2,3,4,5])
exp5.add_session('16-44-08', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('16-45-41', None, 'laserpulse', 'am_tuning_curve')#Possible photoelectric effect
#exp5.add_session('16-52-20', 'a', 'tuningTest', 'am_tuning_curve') Behavior not saved

exp5.add_site(2950, egroups=[1,2,3,4,5])
exp5.add_session('17-00-11', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('17-04-20', None, 'laserpulse', 'am_tuning_curve')#Stopped at 50 trials from artifacting
exp5.add_session('17-06-26', None, 'laserpulse', 'am_tuning_curve')#Reduced laser power to 1.5 mW in an attempt to reduce the PEE. No luck. Returning to 2.5 mW
exp5.add_session('17-10-37', 'b', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3000, egroups=[1,2,3,4,5])
exp5.add_session('17-27-57', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('17-30-06', 'c', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3050, egroups=[1,2,3,4,5])
exp5.add_session('17-42-53', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('17-44-20', 'd', 'tuningTest', 'am_tuning_curve') #Possibly sound-responsive cell

exp5.add_site(3100, egroups=[1,2,3,4,5])
exp5.add_session('17-57-06', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('17-58-58', 'e', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3150, egroups=[1,2,3,4,5])
exp5.add_session('18-14-40', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('18-20-21', 'f', 'tuningTest', 'am_tuning_curve')
exp5.add_session('18-34-11', None, 'laserpulse', 'am_tuning_curve') #Possibly light responsive

exp5.maxDepth = 3150

exp6 = celldatabase.Experiment(subject, '2018-07-26', 'left_AudStr',
                               recordingTrack='midline', probe='A4x2-tet',
                               info=['FacingPosterior', 'midline'])
experiments.append(exp6)

#Used left speaker; 2.5 mW for laser; probe D621 Rig 1; DiI

exp6.laserCalibration = {
    '0.5':1.00,
    '1.0':1.75,
    '1.5':2.50,
    '2.0':3.45,
    '2.5':4.55,
    '3.0':5.75,
    '3.5':6.65,
    '4.0':7.50
}

#Tetrode 4 has reference; threshold set to 55mV
exp6.add_site(2900, egroups=[1,2,3,5,6,7,8])
exp6.add_session('15-40-15', None, 'noiseburst', 'am_tuning_curve')
exp6.add_session('15-48-01', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(2950, egroups=[1,2,3,5,6,7,8])
exp6.add_session('15-52-26', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3000, egroups=[1,2,5,6,7,8])
exp6.add_session('15-58-22', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3050, egroups=[1,2,5,6,7,8])
exp6.add_session('16-01-49', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3100, egroups=[1,2,5,6,7,8])
exp6.add_session('16-05-34', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3150, egroups=[1,2,5,6,7])#3 Has the reference
exp6.add_session('16-08-31', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3200, egroups=[5,6,7]) #Shank 1 with egroups 1 and 2 broke off
exp6.add_session('16-18-32', None, 'noiseburst', 'am_tuning_curve')

exp6.add_site(3250, egroups=[4,5,6,7,8])
exp6.add_session('16-25-22', None, 'noiseburst', 'am_tuning_curve')

exp6.maxDepth = 3250 #Had to stop because broken shank was close to impacting the other shanks

exp7 = celldatabase.Experiment(subject, '2018-07-27', 'left_AudStr',
                               recordingTrack='Posterior', probe='A4x2-tet',
                               info=['FacingPosterior', 'Posterior'])
experiments.append(exp7)

#Used left speaker; 2.5 mW for laser; probe D621 Rig 1; DiD

exp7.laserCalibration = {
    '0.5':0.85,
    '1.0':1.45,
    '1.5':2.10,
    '2.0':2.80,
    '2.5':3.80,
    '3.0':4.70,
    '3.5':5.80,
    '4.0':6.50
}

#Tetrode 3 has reference; threshold set to 51mV
exp7.add_site(2900, egroups=[5,6,7,8])
exp7.add_session('13-54-31', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(2950, egroups=[5,6,7,8])
exp7.add_session('13-58-43', None, 'noiseburst', 'am_tuning_curve')

#Threshold set to 55mV
exp7.add_site(3000, egroups=[5,6,7,8])
exp7.add_session('14-01-40', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3050, egroups=[5,6,7,8])
exp7.add_session('14-04-37', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3100, egroups=[5,6,7,8])
exp7.add_session('14-08-09', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3150, egroups=[5,6,7,8])
exp7.add_session('14-13-43', None, 'noiseburst', 'am_tuning_curve')#Not sound-responsive, but testing to see if in striatum
exp7.add_session('14-15-43', None, 'laserpulse', 'am_tuning_curve')#Definitely laser-responsive. Increase in activation followed by refractory periods

exp7.add_site(3200, egroups=[5,6,7,8])
exp7.add_session('14-18-14', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3250, egroups=[5,6,7,8])
exp7.add_session('14-21-31', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3300, egroups=[5,6,7,8])
exp7.add_session('14-24-45', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3350, egroups=[5,6,7,8])
exp7.add_session('14-28-38', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3400, egroups=[5,6,7,8])
exp7.add_session('14-47-30', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3450, egroups=[5,6,7,8])
exp7.add_session('14-54-06', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('14-55-56', None, 'laserpulse', 'am_tuning_curve')
exp7.add_session('14-58-15', None, 'lasertrain', 'am_tuning_curve')
exp7.add_session('15-00-46', None, 'noiseburst', 'am_tuning_curve')#100 trials
exp7.add_session('15-03-23', None, 'laserpulse', 'am_tuning_curve')
exp7.add_session('15-06-22', None, 'lasertrain', 'am_tuning_curve')
exp7.add_session('15-10-24', 'a', 'tuningTest', 'am_tuning_curve') #No sound-responsive cells. They are still light-responsive

exp7.add_site(3500, egroups=[5,6,7,8])
exp7.add_session('15-33-34', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3550, egroups=[5,6,7,8])
exp7.add_session('15-37-04', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3600, egroups=[5,6,7,8])
exp7.add_session('15-49-01', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3650, egroups=[5,6,7,8])
exp7.add_session('15-58-37', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3700, egroups=[5,6,7,8])
exp7.add_session('16-08-45', None, 'noiseburst', 'am_tuning_curve')

exp7.add_site(3750, egroups=[5,6,7,8])
exp7.add_session('16-14-24', None, 'noiseburst', 'am_tuning_curve')
exp7.add_session('16-16-04', None, 'laserpulse', 'am_tuning_curve')#Still light-responsive

exp7.add_site(3800, egroups=[5,6,7,8])
exp7.add_session('16-08-45', None, 'noiseburst', 'am_tuning_curve')

exp7.maxDepth = 3800 #T5 and T6 saw the most neurons
