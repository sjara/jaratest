from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'd1pi033'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-04-17', 'right_AudStr', info=['FacingPosterior', 'PosteriorDiD'])
experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.5 mW; Probe CEC2; Rig 2

exp0.laserCalibration = {
    '0.5':1.48,
    '1.0':1.93,
    '1.5':2.50,
    '2.0':3.10,
    '2.5':3.58,
    '3.0':4.50,
    '3.5':5.55,
    '4.0':6.75
}


#Tetrode 3 has reference; threshold set to 55mV
exp0.add_site(2900, tetrodes=[8])
exp0.add_session('13-45-51', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-48-40', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-50-39', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('13-52-22', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-00-16', 'b', 'tuningCurve(tc)', 'am_tuning_curve')
exp0.add_session('14-35-58', 'c', 'AM', 'am_tuning_curve')
#Sound response and tuning, but no real laser response

exp0.add_site(3000, tetrodes=[1,2,7,8])
exp0.add_session('15-02-13', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-06-34', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-11-01', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-12-34', 'd', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-20-20', 'e', 'tuningCurve(tc)', 'am_tuning_curve')
exp0.add_session('15-50-20', 'f', 'AM', 'am_tuning_curve')
#Sound and laser response on 2 and 8

exp0.add_site(3100, tetrodes=[1,2])
exp0.add_session('16-43-34', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-46-00', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-51-36', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-55-47', 'g', 'tuningTest', 'am_tuning_curve')
exp0.add_session('17-02-24', 'h', 'tuningCurve(tc)', 'am_tuning_curve')
exp0.add_session('17-31-50', 'i', 'AM', 'am_tuning_curve')
#Sound and laser responsive, though laser may have been phtoelectric effect

#Shank 4 broke off in brain, likely from adhereing to the bone it was close to
exp0.maxDepth = 3100
