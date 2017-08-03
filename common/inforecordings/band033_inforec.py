from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band033'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-07-27', 'right_AC', info='medialDiI')
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':2.3,
    '1.0':3.9,
    '1.5':6.4,
    '2.0':10.0
} #looks like I got quite a bit of dye on the fiber

exp0.add_site(1400, tetrodes=[2,4,6,8])
exp0.add_session('13-28-16', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-29-46', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1425, tetrodes=[2,4,6,8])
exp0.add_session('13-34-10', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1450, tetrodes=[4,8])
exp0.add_session('13-37-09', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('13-38-23', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1475, tetrodes=[1,2,8])
exp0.add_session('13-45-30', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1500, tetrodes=[1,2,6,8])
exp0.add_session('13-50-34', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1525, tetrodes=[1,2,8])
exp0.add_session('13-55-40', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1550, tetrodes=[2,6,8])
exp0.add_session('14-18-42', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1575, tetrodes=[2,3,8])
exp0.add_session('14-24-16', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1600, tetrodes=[2,3,8])
exp0.add_session('14-30-28', None, 'laserPulse', 'am_tuning_curve')

exp0.add_site(1625, tetrodes=[1,2,3,4,7,8])
exp0.add_session('14-37-01', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-38-32', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-40-31', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-47-32', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('14-51-53', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('14-53-56', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('14-57-25', 'c', 'bandwidth', 'bandwidth_am') #18kHz, 8Hz
exp0.add_session('15-15-52', 'd', 'bandwidth', 'bandwidth_am') #12khz, 8Hz
exp0.add_session('15-34-14', 'e', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1700, tetrodes=[1,2,4,7,8])
exp0.add_session('15-44-31', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-46-04', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-47-33', 'f', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-53-01', 'g', 'AM', 'am_tuning_curve')
exp0.add_session('15-57-14', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('15-59-20', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('16-03-16', 'h', 'bandwidth', 'bandwidth_am')
exp0.add_session('16-22-22', 'i', 'noiseAmps', 'am_tuning_curve')


exp1 = celldatabase.Experiment(subject, '2017-08-02', 'left_AC', info='medialDiI')
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':1.5,
    '1.0':2.15,
    '1.5':3.0,
    '2.0':3.7,
    '2.5':4.6,
    '3.0':5.7,
    '3.5':6.7
}

exp1.add_site(1200, tetrodes=[1,2,3,4,6,8])
exp1.add_session('11-55-38', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('11-57-24', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
exp1.add_session('12-05-42', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1260, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('12-11-37', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-13-01', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-15-48', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-21-16', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-25-30', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-27-34', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-31-16', 'c', 'bandwidth', 'bandwidth_am')
exp1.add_session('12-50-42', 'd', 'harmonics', 'bandwidth_am')
exp1.add_session('12-57-34', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1300, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('13-08-44', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1325, tetrodes=[1,2,3,4,5,6,7,8])
exp1.add_session('13-14-19', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-15-41', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-18-51', 'f', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-24-19', 'g', 'AM', 'am_tuning_curve')
exp1.add_session('13-28-34', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-30-39', None, 'laserTrain', 'am_tuning_curve')
# lost laser responsive cell. Recordings really noisy as well due to lack of ground

exp1.add_site(1350, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('13-38-15', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-39-31', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-41-51', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-47-41', 'i', 'AM', 'am_tuning_curve')
exp1.add_session('13-52-20', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('13-55-39', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('14-00-27', 'j', 'bandwidth', 'bandwidth_am')
exp1.add_session('14-18-58', 'k', 'harmonics', 'bandwidth_am')
exp1.add_session('14-40-59', 'l', 'noiseAmps', 'am_tuning_curve')
exp1.add_session('14-46-47', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-00-45', 'm', 'harmonics', 'bandwidth_am')


exp1.add_site(1400, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-32-09', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1425, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-42-17', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1450, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-51-12', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1475, tetrodes=[1,2,3,4,6,7,8])
exp1.add_session('15-55-21', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1500, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('15-59-30', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1525, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('16-05-31', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1550, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('16-09-11', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1575, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('16-15-33', None, 'laserPulse', 'am_tuning_curve')

exp1.add_site(1600, tetrodes=[1,2,3,4,5,6,7])
exp1.add_session('16-22-06', None, 'laserPulse', 'am_tuning_curve')
