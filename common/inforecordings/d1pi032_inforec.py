from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'd1pi032'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-02-19', 'right_AudStr', info=['FacingPosterior', 'AnteriorDiD'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2 mW; Probe CEC2; Rig 2

exp0.laserCalibration = {
    '0.5':1.48,
    '1.0':2.00,
    '1.5':2.58,
    '2.0':3.15,
    '2.5':3.58,
    '3.0':4.40,
    '3.5':5.35,
    '4.0':6.10
}


#Tetrode 2 has reference; threshold set to 55mV
exp0.add_site(2900, tetrodes=[1,3,4,5,6,7,8])
exp0.add_session('17-40-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-47-11', None, 'lasertrain', 'am_tuning_curve')

#Tetrode 2 has reference; threshold set to 55mV
exp0.add_site(3000, tetrodes=[1,3,4,5,6,7,8])
exp0.add_session('18-10-15', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-11-39', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3100, tetrodes=[1,3,4,5,6,7,8])
exp0.add_session('18-37-36', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,3,4,5,6,7,8])
exp0.add_session('18-51-02', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-52-52', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-54-50', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-04-34', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('19-36-18', 'b', 'am', 'am_tuning_curve')
# Cell on tetrode 8 of interest, not necessarily D1

exp0.maxDepth = 3200


exp1 = celldatabase.Experiment(subject, '2019-02-22', 'right_AudStr', info=['FacingPosterior', 'MiddleDiI'])
experiments.append(exp1)

#100 noiseburst, 50 laser train, 100 laser pulse, 240 tuningCurve, 330 AM, 2880 tc
#Used left speaker;laser (445 nm) set to 2 mW; Probe CEC2; Rig 2

exp1.laserCalibration = {
    '0.5':1.5,
    '1.0':2.05,
    '1.5':2.8,
    '2.0':3.4,
    '2.5':4.15,
    '3.0':5.2,
    '3.5':6.35,
    '4.0':7.5
}

exp1.add_site(2900, tetrodes=[1,3,6,7,8])
exp1.add_session('13-34-49', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-37-06', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-40-48', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-45-52', 'a', 'shortTuningCurve', 'am_tuning_curve')
exp1.add_session('13-54-38', 'b', 'am', 'am_tuning_curve')
exp1.add_session('14-10-51', 'c', 'tuningCurve', 'am_tuning_curve')
#possible sound and laser responsive cell

exp1.add_site(3000, tetrodes=[1,3,4,5,6,7,8])
exp1.add_session('15-37-23', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-41-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-45-18', 'd', 'shortTuningCurve', 'am_tuning_curve')

exp1.add_site(3100, tetrodes=[1,3,4,5,6,7,8])
exp1.add_session('16-07-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-10-58', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-12-40', 'e', 'shortTuningCurve', 'am_tuning_curve')

exp1.add_site(3200, tetrodes=[2,3,4,5,6,7,8])
exp1.add_session('16-31-29', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-33-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-35-05', 'f', 'shortTuningCurve', 'am_tuning_curve')
exp1.add_session('16-42-48', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-13-03', 'h', 'am', 'am_tuning_curve')

exp1.add_site(3300, tetrodes=[2,3,5,6,7,8])
exp1.add_session('17-33-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-35-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-36-57', 'i', 'shortTuningCurve', 'am_tuning_curve')

exp1.add_site(3400, tetrodes=[1,2,4,5,6,7])
exp1.add_session('18-00-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-02-08', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-04-13', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-07-16', 'j', 'shortTuningCurve', 'am_tuning_curve')
exp1.add_session('18-11-06', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('18-41-18', 'l', 'am', 'am_tuning_curve')

exp1.maxDepth = 3400


exp2 = celldatabase.Experiment(subject, '2019-02-28', 'right_AudStr', info=['FacingPosterior', 'MiddleDiD'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2 mW; Probe CEC2; Rig 2

exp1.laserCalibration = {
    '0.5':1.6,
    '1.0':2.34,
    '1.5':3.08,
    '2.0':3.85,
    '2.5':4.50,
    '3.0':5.85,
    '3.5':6.8,
    '4.0':8.3,
}

exp1.add_site(2900, tetrodes=[1,3,6,7,8])
exp1.add_session('13-34-49', None, 'noiseburst', 'am_tuning_curve')
