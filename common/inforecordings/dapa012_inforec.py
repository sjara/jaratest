from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa012'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-02-27', 'left_AudStr', info='AnteriorMiddleDiI')
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


exp1 = celldatabase.Experiment(subject, '2018-02-28', 'left_AudStr', info='AntMidMiddleDiI')
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
exp1.add_session('14-46-44', 'r', 'laserTuningCurve', 'laser_am_tuning_curve')
#Stopped early because noise started showing up
