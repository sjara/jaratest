from jaratoolbox import celldatabase

subject = 'd1pi032'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-02-19', 'right_AudStr',
                               recordingTrack='AnteriorDiD', probe='A4x2-tet',
                               info=['FacingPosterior'])
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
exp0.add_site(2900, egroups=[1,3,4,5,6,7,8])
exp0.add_session('17-40-01', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-47-11', None, 'lasertrain', 'am_tuning_curve')

#Tetrode 2 has reference; threshold set to 55mV
exp0.add_site(3000, egroups=[1,3,4,5,6,7,8])
exp0.add_session('18-10-15', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-11-39', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(3100, egroups=[1,3,4,5,6,7,8])
exp0.add_session('18-37-36', None, 'noiseburst', 'am_tuning_curve')

exp0.add_site(3200, egroups=[1,3,4,5,6,7,8])
exp0.add_session('18-51-02', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-52-52', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('18-54-50', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('19-04-34', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('19-36-18', 'b', 'am', 'am_tuning_curve')
# Cell on tetrode 8 of interest, not necessarily D1

exp0.maxDepth = 3200


exp1 = celldatabase.Experiment(subject, '2019-02-22', 'right_AudStr',
                               recordingTrack='MiddleDiI', probe='A4x2-tet',
                               info=['FacingPosterior'])
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

exp1.add_site(2900, egroups=[1,3,6,7,8]) #Recorded by Anna when grad students were visiting. Different number of trials were used compared to normal
exp1.add_session('13-34-49', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-37-06', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-40-48', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-45-52', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-54-38', 'b', 'am', 'am_tuning_curve')
exp1.add_session('14-10-51', 'c', 'tuningCurve', 'am_tuning_curve')
#possible sound and laser responsive cell

exp1.add_site(3000, egroups=[1,3,4,5,6,7,8])
exp1.add_session('15-37-23', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-41-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-45-18', 'd', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3100, egroups=[1,3,4,5,6,7,8])
exp1.add_session('16-07-41', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-10-58', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-12-40', 'e', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3200, egroups=[2,3,4,5,6,7,8])
exp1.add_session('16-31-29', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-33-07', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-35-05', 'f', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-42-48', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-13-03', 'h', 'am', 'am_tuning_curve')

exp1.add_site(3300, egroups=[2,3,5,6,7,8])
exp1.add_session('17-33-11', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-35-26', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-36-57', 'i', 'tuningTest', 'am_tuning_curve')

exp1.add_site(3400, egroups=[1,2,4,5,6,7])
exp1.add_session('18-00-17', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-02-08', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('18-04-13', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('18-07-16', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('18-11-06', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('18-41-18', 'l', 'am', 'am_tuning_curve')

exp1.maxDepth = 3400

# exp2 = celldatabase.Experiment(subject, '2019-02-28', 'right_AudStr',  'MiddleDiD',
#                                    info=['FacingPosterior'])
# experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2 mW; Probe CEC2; Rig 2

# exp2.laserCalibration = {
#     '0.5':1.6,
#     '1.0':2.34,
#     '1.5':3.08,
#     '2.0':3.85,
#     '2.5':4.50,
#     '3.0':5.85,
#     '3.5':6.8,
#     '4.0':8.3,
# }

exp3 = celldatabase.Experiment(subject, '2019-03-05', 'left_AudStr',
                               recordingTrack='MiddleDiD', probe='A4x2-tet',
                               info=['FacingPosterior'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':1.5,
    '1.0':2.0,
    '1.5':2.5,
    '2.0':3.1,
    '2.5':3.55,
    '3.0':4.6,
    '3.5':5.53,
    '4.0':6.7
}


exp3.add_site(2900, egroups=[2,3,4,6,7,8])
exp3.add_session('17-13-11', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-15-40', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-19-59', 'a', 'tuningTest', 'am_tuning_curve')

exp3.add_site(3000, egroups=[1,2,3,4,6,7,8])
exp3.add_session('17-40-25', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-44-28', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-47-14', 'b', 'tuningTest', 'am_tuning_curve') #slight white noise tuning on tetrode 8, cluster 2

exp3.add_site(3100, egroups=[1,2,3,4,6,7,8])
exp3.add_session('18-07-54', None, 'noiseburst', 'am_tuning_curve') #by end of noiseburst, cells were gone

#exp3.add_site(3200, egroups=[2,3,4,5,6,7,8])
#No cells

#exp3.add_site(3300, egroups=[2,3,4,5,6,7,8])
#No cells

exp3.add_site(3400, egroups=[2,3,4,5,6])
exp3.add_session('18-41-17', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('18-43-20', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('18-46-46', 'c', 'tuningTest', 'am_tuning_curve')

exp3.maxDepth = 3400
