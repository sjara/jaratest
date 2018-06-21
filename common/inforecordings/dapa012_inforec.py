from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa012'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-02-27', 'left_AudStr', info=['facingPosterior', 'AnteriorMiddleDiI'])
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe CEC4

exp0.laserCalibration = {
    '0.5':0.8,
    '1.0':1.3,
    '1.5':1.85,
    '2.0':2.0,
    '2.5':2.45,
    '3.0':3.0,
    '3.5':3.5,
    '4.0':4.3
}

#Tetrode 6 has reference; threshold set to 55mV
exp0.add_site(2500, tetrodes=[1,2,7])
exp0.add_session('10-39-31', None, 'noisebursts', 'am_tuning_curve')
#Lots of noise on shanks 1 and 2. When noisebursts presented, there was extra noise with each burst.
#This occured even with the probe just submerged in the saline in the well. When I removed the mouse,
#I tested the ground and adjusted the mesh around the right speaker, since Anna mentioned it might be
#touching the axle in the wheel. When I tested the probe in saline, it was working as expected.
#I put the mouse back in the rig and tested the probe in the saline above its head, and it worked
#As expected. While listening to the monitor at Nick's suggestion, I realized that touching
#The mesh on both speakers to the wheel caused the sound to come through the monitor. As such,
#I moved the mesh back so that neither was touching the bar going through the wheel, and it seemed
#To fix the problem (the sound no longer came through the monitor)
exp0.add_session('12-09-29', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[1,2,7,8])
exp0.add_session('12-16-30', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-18-18', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[1,2,7])
exp0.add_session('12-25-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-29-35', 'b', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2650, tetrodes=[1,2,7,8])
exp0.add_session('12-37-14', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-39-14', 'c', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2700, tetrodes=[1,2,7,8])
exp0.add_session('12-46-57', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2750, tetrodes=[1,2,3,4,5,7,8])
exp0.add_session('12-51-58', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-53-45', 'd', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2800, tetrodes=[1,2,3,4,7])
exp0.add_session('13-00-55', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-03-44', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2850, tetrodes=[1,2,3,4,])
exp0.add_session('13-11-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-15-31', 'f', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, tetrodes=[1,2,3,4,])
exp0.add_session('13-21-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-23-02', 'g', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,3,4,])
exp0.add_session('13-30-04', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-31-36', 'h', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3050, tetrodes=[1,2,3,4,])
exp0.add_session('13-38-23', None, 'noisebursts', 'am_tuning_curve')
#Grounding was messed up again; sound is showing up on probe

#After removing the mouse and letting the probe soak in trypsin for a bit, the
#noise issues were gone again
exp0.maxDepth = 3050

exp1 = celldatabase.Experiment(subject, '2018-02-28', 'left_AudStr', info=['facingPosterior', 'AntMidMiddleDiD'])
experiments.append(exp1)
#Used both speakers; 2.5 mW for laser; probe CEC4

exp1.laserCalibration = {
    '0.5':0.7,
    '1.0':0.9,
    '1.5':1.2,
    '2.0':1.45,
    '2.5':1.7,
    '3.0':2.0,
    '3.5':2.35,
    '4.0':2.7
}

#Tetrode 7 has reference; threshold set to 55mV
exp1.add_site(2500, tetrodes=[2])
exp1.add_session('10-34-54', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-37-58', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2550, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('10-48-52', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2600, tetrodes=[1,2])
exp1.add_session('10-54-58', None, 'noisebursts', 'am_tuning_curve')
#exp1.add_session('10-37-58', 'a', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2650, tetrodes=[1,2,4,5])
exp1.add_session('10-59-37', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-01-44', 'b', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-05-46', 'c', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-21-14', 'd', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2700, tetrodes=[2,3])
exp1.add_session('11-55-47', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2750, tetrodes=[1,2,4])
exp1.add_session('11-59-33', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-01-19', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-04-09', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-18-42', 'g', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(2800, tetrodes=[1,2,4])
exp1.add_session('12-52-27', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-53-53', 'h', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2850, tetrodes=[1,2])
exp1.add_session('12-58-44', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-00-21', 'i', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(2900, tetrodes=[1,2])
exp1.add_session('13-05-34', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(2950, tetrodes=[1,2])
exp1.add_session('13-08-19', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-09-58', 'j', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3000, tetrodes=[1,2])
exp1.add_session('13-14-33', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(3050, tetrodes=[1,2,3])
exp1.add_session('13-19-24', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-20-57', 'k', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[1,2])
exp1.add_session('13-25-59', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-27-38', 'l', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(3150, tetrodes=[1,2])
exp1.add_session('13-31-55', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-33-45', 'm', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-36-48', 'n', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-53-15', 'o', 'laserTuningCurve', 'laser_am_tuning_curve')

exp1.add_site(3250, tetrodes=[1,2])
exp1.add_session('14-25-44', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(3300, tetrodes=[1,2,4])
exp1.add_session('14-28-14', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-29-39', 'p', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-32-23', 'q', 'tuningCurve', 'am_tuning_curve')
#exp1.add_session('14-46-44', 'r', 'laserTuningCurve', 'laser_am_tuning_curve')
#Stopped early because noise started showing up

exp1.maxDepth = 3300

exp2 = celldatabase.Experiment(subject, '2018-03-04', 'left_AudStr', info=['facingPosterior', 'PostMidMiddleDiI'])
experiments.append(exp2)
#Used both speakers; 2.5 mW for laser; probe CEC4

exp2.laserCalibration = {
    '0.5':0.65,
    '1.0':0.8,
    '1.5':1.0,
    '2.0':1.2,
    '2.5':1.40,
    '3.0':1.65,
    '3.5':1.9,
    '4.0':2.1
}

#Probe impedances were a bit high
#Tetrode 7 has reference; threshold set to 55mV
exp2.add_site(2500, tetrodes=[])
exp2.add_session('10-34-54', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-37-58', 'a', 'tuningCurve', 'am_tuning_curve')

exp2.maxDepth = 2500

exp3 = celldatabase.Experiment(subject, '2018-03-13', 'right_AudStr', info=['facingPosterior','PostMidMiddleDiI'])
experiments.append(exp3)
#Used both speakers; 2.5 mW for laser; first probe CEC4; second probe D621 (Anna's probe)

exp3.laserCalibration = {
    '0.5':0.85,
    '1.0':1.35,
    '1.5':1.9,
    '2.0':3.2,
    '2.5':3.3,
    '3.0':4.3,
    '3.5':5.55,
    '4.0':6.3
}

#Probe impedances were a bit high
#Tetrode 2 has reference; threshold set to 47mV due to signal looking pretty small
#despite measured impedances being well within normal range; signals still looked bad,
#so switched probes

#new signals look much better at first, but it quickly became apparent that
#the sounds were being picked up by the probe; after a while of troubleshooting
#the left speaker, which seemed to be the problem (unplugging the speaker from the amp
#caused feedback through the probe), the probe was still very noisy, but the sound was
#no longer being picked up
#tetrode 6 has reference
exp3.add_site(2650, tetrodes=[7])
exp3.add_session('15-44-47', None, 'noisebursts', 'am_tuning_curve')

#tetrode 5 has reference
exp3.add_site(2800, tetrodes=[8])
exp3.add_session('15-55-03', None, 'noisebursts', 'am_tuning_curve')
#Definitely seems to be picking up movement artifacts; mouse was jumping with noise at first,
#but stopped halfway through, matching the pattern in the raster
#exp3.add_session('10-37-58', 'a', 'tuningCurve', 'am_tuning_curve')

#tetrode 6 has reference
exp3.add_site(2900, tetrodes=[7,8])
exp3.add_session('16-01-38', None, 'noisebursts', 'am_tuning_curve')

exp3.maxDepth = 2900

exp4 = celldatabase.Experiment(subject, '2018-03-14', 'right_AudStr', info=['facingPosterior','AntMidMiddleDiD'])
experiments.append(exp4)
#Used both speakers; 2.5 mW for laser; Used probe D621 (Anna's probe)

exp4.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.3,
    '2.0':1.6,
    '2.5':1.85,
    '3.0':2.25,
    '3.5':2.6,
    '4.0':3.0
}

#reference on tetrode 6
exp4.add_site(2600, tetrodes=[8])
exp4.add_session('10-20-42', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-22-53', 'a', 'tuningCurve', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2650, tetrodes=[5,6])
exp4.add_session('10-31-14', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-32-55', 'b', 'tuningCurve', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2700, tetrodes=[6,8])
exp4.add_session('10-40-01', None, 'noisebursts', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2800, tetrodes=[5])
exp4.add_session('10-48-50', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-51-11', 'c', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-55-31', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-09-26', 'e', 'laserTuningCurve', 'laser_am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2850, tetrodes=[5,6,8])
#exp4.add_session('11-41-06', None, 'noisebursts', 'am_tuning_curve') #messed up paradigm
exp4.add_session('11-42-26', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-46-05', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-50-17', 'g', 'tuningCurve', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2900, tetrodes=[5,6,8])
exp4.add_session('12-08-54', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-10-46', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-13-43', 'i', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-27-51', 'j', 'laserTuningCurve', 'laser_am_tuning_curve')

#reference on tetrode 7
exp4.add_site(2950, tetrodes=[5,6,8])
exp4.add_session('13-00-18', None, 'noisebursts', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(3000, tetrodes=[5,6,8])
exp4.add_session('13-05-21', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-06-52', 'k', 'tuningCurve', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(3050, tetrodes=[5,6,8])
exp4.add_session('13-12-54', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-14-23', 'l', 'tuningCurve', 'am_tuning_curve')

#reference on tetrode 7
exp4.add_site(3100, tetrodes=[5,6,8])
exp4.add_session('13-22-06', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('13-23-27', 'm', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-26-16', 'n', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-40-30', 'o', 'laserTuningCurve', 'laser_am_tuning_curve')

#reference on tetrode 7
exp4.add_site(3150, tetrodes=[5,6,8])
exp4.add_session('14-15-06', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-16-28', 'p', 'tuningCurve', 'am_tuning_curve')
#exp4.add_session('13-26-16', 'n', 'tuningCurve', 'am_tuning_curve')
#exp4.add_session('13-40-30', 'o', 'laserTuningCurve', 'laser_am_tuning_curve')

exp4.maxDepth = 3150