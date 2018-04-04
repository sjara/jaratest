from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa013'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2018-04-03', 'left_AudStr', info=['FacingPosterior', 'AnteriorDiI'])
experiments.append(exp0)
#Used both speakers; 2.5 mW for laser; probe DAF4

exp0.laserCalibration = {
    '0.5':0.85,
    '1.0':1.3,
    '1.5':1.65,
    '2.0':2.0,
    '2.5':2.3,
    '3.0':2.85,
    '3.5':3.35,
    '4.0':4.05
}

#Tetrode 7 has reference; threshold set to 55mV
exp0.add_site(2500, tetrodes=[5,6,8])
exp0.add_session('13-13-44', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-18-20', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2550, tetrodes=[5,6,8])
exp0.add_session('13-24-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-26-17', 'b', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2600, tetrodes=[5,6,8])
exp0.add_session('13-32-24', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2650, tetrodes=[5,6,8])
exp0.add_session('13-38-09', None, 'noisebursts', 'am_tuning_curve')
#exp0.add_session('13-39-44', 'c', 'tuningCurve', 'am_tuning_curve') forgot to save behavior

exp0.add_site(2700, tetrodes=[1,2,4,5,6,8])
exp0.add_session('13-54-28', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-56-53', 'c', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2750, tetrodes=[1,2,4,5,6,8])
exp0.add_session('14-07-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-09-12', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-12-42', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-27-48', 'f', 'laserTuningCurve', 'laser_am_tuning_curve') #had to open the door a couple times to add saline

exp0.add_site(2800, tetrodes=[1,2,4,5,6,8])
exp0.add_session('15-03-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-04-38', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-08-05', 'h', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-22-14', 'i', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(2850, tetrodes=[1,2,4,5])
exp0.add_session('16-00-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-01-39', 'j', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2900, tetrodes=[1,2,4,5,6,8])
exp0.add_session('16-08-34', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-10-06', 'k', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-13-16', 'l', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-27-15', 'm', 'laserTuningCurve', 'laser_am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,4,8])
exp0.add_session('17-00-31', None, 'noisebursts', 'am_tuning_curve')
