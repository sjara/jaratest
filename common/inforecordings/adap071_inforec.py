from jaratoolbox import celldatabase

subject = 'adap071'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''
'''
exp0 = celldatabase.Experiment(subject,
                               '2017-08-29',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(500, tetrodes=range(1, 9))
exp0.add_session('15-11-04', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp0.add_session('15-22-21', 'a', 'tc', 'laser_tuning_curve')
'''

exp1 = celldatabase.Experiment(subject,
                               '2017-09-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(500, tetrodes=range(1, 9))
exp1.add_session('16-18-57', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp1.add_session('16-23-07', 'a', 'tc', 'laser_tuning_curve')
exp1.add_session('16-30-45', 'a', 'behavior', '2afc')#150 trials/block, 


exp2 = celldatabase.Experiment(subject,
                               '2017-09-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(540, tetrodes=range(1, 9))
exp2.add_session('14-53-39', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp2.add_session('14-56-23', 'a', 'tc', 'laser_tuning_curve')
exp2.add_session('15-03-53', 'a', 'behavior', '2afc')#150 trials/block, 

exp3 = celldatabase.Experiment(subject,
                               '2017-09-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(580, tetrodes=range(1, 9))
exp3.add_session('12-41-19', None, 'noiseburst', 'laser_tuning_curve')#ref=9
exp3.add_session('12-46-13', None, 'noiseburst', 'laser_tuning_curve')#ref=7
exp3.add_session('12-49-00', 'a', 'tc', 'laser_tuning_curve')#ref=7
exp3.add_session('12-56-22', 'a', 'behavior', '2afc')#150 trials/block, 


exp4 = celldatabase.Experiment(subject,
                               '2017-09-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(620, tetrodes=range(1, 9))
exp4.add_session('14-11-38', None, 'noiseburst', 'laser_tuning_curve')#ref=7
exp4.add_session('14-16-36', 'a', 'tc', 'laser_tuning_curve')#ref=7
exp4.add_session('14-23-52', 'a', 'behavior', '2afc')#150 trials/block, 


exp5 = celldatabase.Experiment(subject,
                               '2017-09-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(660, tetrodes=range(1, 9))
exp5.add_session('15-42-13', None, 'noiseburst', 'laser_tuning_curve')#ref=7
exp5.add_session('15-45-02', 'a', 'tc', 'laser_tuning_curve')#ref=7
exp5.add_session('15-53-36', 'a', 'behavior', '2afc')#150 trials/block, 


exp6 = celldatabase.Experiment(subject,
                               '2017-09-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(700, tetrodes=range(1, 9))
exp6.add_session('15-25-35', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp6.add_session('15-29-37', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp6.add_session('15-32-54', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp6.add_session('15-40-02', 'a', 'behavior', '2afc')#150 trials/block, 


exp7 = celldatabase.Experiment(subject,
                               '2017-09-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(740, tetrodes=range(1, 9))
exp7.add_session('16-21-59', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp7.add_session('16-25-05', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp7.add_session('16-28-17', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp7.add_session('16-32-33', 'a', 'tc', 'laser_tuning_curve')#ref=13
exp7.add_session('16-39-22', 'a', 'behavior', '2afc')#200 trials/block, 


exp8 = celldatabase.Experiment(subject,
                               '2017-09-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(780, tetrodes=range(1, 9))
exp8.add_session('14-55-42', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp8.add_session('14-58-28', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('15-05-59', 'a', 'behavior', '2afc')#150 trials/block, 


exp9 = celldatabase.Experiment(subject,
                               '2017-09-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(820, tetrodes=range(1, 9))
exp9.add_session('15-03-01', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp9.add_session('15-06-03', 'a', 'tc', 'laser_tuning_curve')
exp9.add_session('15-13-15', 'a', 'behavior', '2afc')#200 trials/block, 


exp10 = celldatabase.Experiment(subject,
                               '2017-09-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(860, tetrodes=range(1, 9))
exp10.add_session('14-06-45', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp10.add_session('14-09-43', 'a', 'tc', 'laser_tuning_curve')
exp10.add_session('14-16-54', 'a', 'behavior', '2afc')#150 trials/block, 


exp11 = celldatabase.Experiment(subject,
                               '2017-09-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(900, tetrodes=range(1, 9))
exp11.add_session('14-40-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp11.add_session('14-42-48', 'a', 'tc', 'laser_tuning_curve')
exp11.add_session('14-51-44', 'a', 'behavior', '2afc')#150 trials/block, 


exp12 = celldatabase.Experiment(subject,
                               '2017-09-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(940, tetrodes=range(1, 9))
exp12.add_session('16-25-03', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp12.add_session('16-28-04', 'a', 'tc', 'laser_tuning_curve')
exp12.add_session('16-34-56', 'a', 'behavior', '2afc')#150 trials/block, 

'''
exp13 = celldatabase.Experiment(subject,
                               '2017-09-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(980, tetrodes=range(1, 9))
exp13.add_session('15-41-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp13.add_session('15-43-59', 'a', 'tc', 'laser_tuning_curve')
exp13.add_session('15-52-45', 'a', 'behavior', '2afc')#200 trials/block, commented out becuase not enough trials
'''

exp14 = celldatabase.Experiment(subject,
                               '2017-09-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(980, tetrodes=range(1, 9))
exp14.add_session('15-04-40', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp14.add_session('15-07-16', 'a', 'tc', 'laser_tuning_curve')
exp14.add_session('15-13-37', 'a', 'behavior', '2afc')#150 trials/block, 


exp15 = celldatabase.Experiment(subject,
                               '2017-09-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(1020, tetrodes=range(1, 9))
exp15.add_session('14-50-29', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp15.add_session('15-45-59', 'a', 'tc', 'laser_tuning_curve')
exp15.add_session('14-53-44', 'a', 'behavior', '2afc')#150 trials/block,

 
exp16 = celldatabase.Experiment(subject,
                               '2017-09-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(1060, tetrodes=range(1, 9))
exp16.add_session('13-43-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp16.add_session('13-46-07', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('13-53-25', 'a', 'behavior', '2afc')#150 trials/block,


exp17 = celldatabase.Experiment(subject,
                               '2017-09-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(1100, tetrodes=range(1, 9))
exp17.add_session('15-21-34', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp17.add_session('15-24-15', 'a', 'tc', 'laser_tuning_curve')
exp17.add_session('15-33-13', 'a', 'behavior', '2afc')#150 trials/block, open ephys crashed right after I stopped recording


exp18 = celldatabase.Experiment(subject,
                               '2017-09-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(1140, tetrodes=range(1, 9))
exp18.add_session('14-38-46', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp18.add_session('14-42-04', 'a', 'tc', 'laser_tuning_curve')
exp18.add_session('14-49-00', 'a', 'behavior', '2afc')#150 trials/block


exp19 = celldatabase.Experiment(subject,
                               '2017-09-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(1180, tetrodes=range(1, 9))
exp19.add_session('14-28-28', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp19.add_session('14-31-36', 'a', 'tc', 'laser_tuning_curve')
exp19.add_session('14-40-14', 'a', 'behavior', '2afc')#150 trials/block


exp20 = celldatabase.Experiment(subject,
                               '2017-09-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(1220, tetrodes=range(1, 9))
exp20.add_session('18-14-51', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp20.add_session('18-17-24', 'a', 'tc', 'laser_tuning_curve')
exp20.add_session('18-23-50', 'a', 'behavior', '2afc')#150 trials/block


exp21 = celldatabase.Experiment(subject,
                               '2017-09-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(1260, tetrodes=range(1, 9))
exp21.add_session('14-17-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp21.add_session('14-19-35', 'a', 'tc', 'laser_tuning_curve')
exp21.add_session('14-26-21', 'a', 'behavior', '2afc')#150 trials/block


exp22 = celldatabase.Experiment(subject,
                               '2017-09-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(1300, tetrodes=range(1, 9))
exp22.add_session('16-19-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp22.add_session('16-21-36', 'a', 'tc', 'laser_tuning_curve')
exp22.add_session('16-28-04', 'a', 'behavior', '2afc')#150 trials/block


exp23 = celldatabase.Experiment(subject,
                               '2017-09-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(1340, tetrodes=range(1, 9))
exp23.add_session('15-50-21', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp23.add_session('15-53-52', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('16-01-26', 'a', 'behavior', '2afc')#150 trials/block


exp24 = celldatabase.Experiment(subject,
                               '2017-09-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(1380, tetrodes=range(1, 9))
exp24.add_session('16-38-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
#exp24.add_session('16-40-56', 'a', 'tc', 'laser_tuning_curve') noisy ref=13
#exp24.add_session('16-46-57', 'b', 'tc', 'laser_tuning_curve') noisy ref=13
exp24.add_session('16-54-43', 'c', 'tc', 'laser_tuning_curve') #ref=12
exp24.add_session('16-58-56', 'a', 'behavior', '2afc')#150 trials/block


exp25 = celldatabase.Experiment(subject,
                               '2017-09-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(1420, tetrodes=range(1, 9))
exp25.add_session('15-58-57', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp25.add_session('16-02-36', 'a', 'tc', 'laser_tuning_curve')
exp25.add_session('16-10-35', 'a', 'behavior', '2afc')#150 trials/block


exp26 = celldatabase.Experiment(subject,
                               '2017-09-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(1460, tetrodes=range(1, 9))
exp26.add_session('16-25-10', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp26.add_session('16-28-59', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('16-35-51', 'a', 'behavior', '2afc')#200 trials/block


exp27 = celldatabase.Experiment(subject,
                               '2017-09-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(1500, tetrodes=range(1, 9))
exp27.add_session('17-54-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp27.add_session('17-56-47', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('18-03-16', 'a', 'behavior', '2afc')#200 trials/block


exp28 = celldatabase.Experiment(subject,
                               '2017-09-29',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(1540, tetrodes=range(1, 9))
exp28.add_session('13-40-34', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp28.add_session('13-45-03', 'a', 'tc', 'laser_tuning_curve')
exp28.add_session('13-51-45', 'a', 'behavior', '2afc')#200 trials/block

'''
exp29 = celldatabase.Experiment(subject,
                               '2017-09-30',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(1540, tetrodes=range(1, 9))
#exp29.add_session('15-46-26', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp29.add_session('15-49-18', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp29.add_session('15-51-29', 'a', 'tc', 'laser_tuning_curve')


exp30 = celldatabase.Experiment(subject,
                               '2017-10-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(1540, tetrodes=range(1, 9))
exp30.add_session('14-13-47', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp30.add_session('14-16-42', 'a', 'tc', 'laser_tuning_curve')
'''

for ind, exp in enumerate(experiments):
    for site in exp.sites:
        site.clusterFolder = 'multisession_exp{}site0'.format(ind)

