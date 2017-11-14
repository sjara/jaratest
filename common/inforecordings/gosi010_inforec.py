from jaratoolbox import celldatabase

subject = 'gosi010'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out.
'''

'''
exp0 = celldatabase.Experiment(subject,
                               '2017-04-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(540, tetrodes=range(1, 9))
exp0.add_session('15-51-55', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp0.add_session('15-56-54', 'a', 'tc', 'laser_tuning_curve')
exp0.add_session('16-05-28', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

exp1 = celldatabase.Experiment(subject,
                               '2017-04-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(540, tetrodes=range(1, 9))
exp1.add_session('16-08-47', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp1.add_session('16-16-12', 'a', 'tc', 'laser_tuning_curve')
exp1.add_session('16-28-52', 'a', 'behavior', '2afc')#150 trials/block


exp2 = celldatabase.Experiment(subject,
                               '2017-04-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(580, tetrodes=range(1, 9))
exp2.add_session('17-45-27', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp2.add_session('17-49-44', 'a', 'tc', 'laser_tuning_curve')
exp2.add_session('17-56-30', 'a', 'behavior', '2afc')#150 trials/block


exp3 = celldatabase.Experiment(subject,
                               '2017-04-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(620, tetrodes=range(1, 9))
#exp3.add_session('16-17-06', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp3.add_session('16-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=10, new cable
#exp3.add_session('16-20-07', 'a', 'tc', 'laser_tuning_curve')
exp3.add_session('16-46-26', 'b', 'tc', 'laser_tuning_curve')#newcable
exp3.add_session('16-54-42', 'a', 'behavior', '2afc')#150 trials/block


exp4 = celldatabase.Experiment(subject,
                               '2017-04-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(660, tetrodes=range(1, 9))
exp4.add_session('14-11-25', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp4.add_session('14-14-23', 'a', 'tc', 'laser_tuning_curve')
exp4.add_session('14-21-26', 'a', 'behavior', '2afc')#150 trials/block

'''
exp5 = celldatabase.Experiment(subject,
                               '2017-04-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(700, tetrodes=range(1, 9))
exp5.add_session('11-59-37', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp5.add_session('12-02-19', 'a', 'tc', 'laser_tuning_curve')
exp5.add_session('12-09-23', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''

exp6 = celldatabase.Experiment(subject,
                               '2017-04-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(700, tetrodes=range(1, 9))
exp6.add_session('14-31-49', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp6.add_session('14-35-43', 'a', 'tc', 'laser_tuning_curve')
exp6.add_session('14-43-14', 'a', 'behavior', '2afc')#150 trials/block


exp7 = celldatabase.Experiment(subject,
                               '2017-04-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(740, tetrodes=range(1, 9))
exp7.add_session('13-51-10', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp7.add_session('13-54-45', 'a', 'tc', 'laser_tuning_curve')#abnormal noise
#exp7.add_session('14-13-23', 'b', 'tc', 'laser_tuning_curve')#same abnormal noise
exp7.add_session('14-26-59', 'a', 'behavior', '2afc')#150 trials/block


exp8 = celldatabase.Experiment(subject,
                               '2017-04-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(780, tetrodes=range(1, 9))
exp8.add_session('14-30-12', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp8.add_session('14-33-00', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('14-41-34', 'a', 'behavior', '2afc')#150 trials/block

'''
exp9 = celldatabase.Experiment(subject,
                               '2017-04-29',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(820, tetrodes=range(1, 9))
exp9.add_session('16-03-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp9.add_session('16-07-41', 'a', 'tc', 'laser_tuning_curve')#ref=17
exp9.add_session('16-14-30', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

exp10 = celldatabase.Experiment(subject,
                               '2017-04-30',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(820, tetrodes=range(1, 9))
exp10.add_session('17-55-37', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp10.add_session('17-58-11', 'a', 'tc', 'laser_tuning_curve')
exp10.add_session('18-06-50', 'a', 'behavior', '2afc')#200 trials/block

'''
exp11 = celldatabase.Experiment(subject,
                               '2017-05-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(860, tetrodes=range(1, 9))
#exp11.add_session('12-15-38', None, 'noiseburst', 'laser_tuning_curve')#ref=17, ephys crash
exp11.add_session('12-32-24', 'a', 'tc', 'laser_tuning_curve')
exp11.add_session('12-40-10', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''

exp12 = celldatabase.Experiment(subject,
                               '2017-05-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(860, tetrodes=range(1, 9))
exp12.add_session('12-02-27', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp12.add_session('12-05-40', 'a', 'tc', 'laser_tuning_curve')
exp12.add_session('12-12-36', 'a', 'behavior', '2afc')#150 trials/block,


exp13 = celldatabase.Experiment(subject,
                               '2017-05-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(900, tetrodes=range(1, 9))
exp13.add_session('14-48-35', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp13.add_session('14-51-01', 'a', 'tc', 'laser_tuning_curve')
exp13.add_session('14-58-15', 'a', 'behavior', '2afc')#150 trials/block,


exp14 = celldatabase.Experiment(subject,
                               '2017-05-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(940, tetrodes=range(1, 9))
exp14.add_session('12-19-44', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp14.add_session('12-29-41', 'a', 'tc', 'laser_tuning_curve')
exp14.add_session('12-37-04', 'a', 'behavior', '2afc')#150 trials/block,


exp15 = celldatabase.Experiment(subject,
                               '2017-05-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(980, tetrodes=range(1, 9))
exp15.add_session('14-26-10', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp15.add_session('14-28-58', 'a', 'tc', 'laser_tuning_curve')
exp15.add_session('14-36-12', 'a', 'behavior', '2afc')#200 trials/block,

exp16 = celldatabase.Experiment(subject,
                               '2017-05-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(1020, tetrodes=range(1, 9))
exp16.add_session('15-27-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp16.add_session('15-31-21', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('15-38-02', 'a', 'behavior', '2afc')#150 trials/block,


exp17 = celldatabase.Experiment(subject,
                               '2017-05-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(1060, tetrodes=range(1, 9))
exp17.add_session('12-47-24', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp17.add_session('12-50-09', 'a', 'tc', 'laser_tuning_curve')
exp17.add_session('12-56-35', 'a', 'behavior', '2afc')#150 trials/block,


exp18 = celldatabase.Experiment(subject,
                               '2017-05-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(1100, tetrodes=range(1, 9))
#exp18.add_session('12-14-05', None, 'noiseburst', 'laser_tuning_curve')#ref=17, weird blot, response in blocks
exp18.add_session('12-17-23', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp18.add_session('12-20-05', 'a', 'tc', 'laser_tuning_curve')
exp18.add_session('12-26-44', 'a', 'behavior', '2afc')#200 trials/block,


exp19 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(1140, tetrodes=range(1, 9))
exp19.add_session('12-05-21', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp19.add_session('12-09-39', 'a', 'tc', 'laser_tuning_curve')
exp19.add_session('12-16-13', 'a', 'behavior', '2afc')#200 trials/block,


exp20 = celldatabase.Experiment(subject,
                               '2017-05-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(1180, tetrodes=range(1, 9))
exp20.add_session('14-36-51', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp20.add_session('14-44-02', 'a', 'tc', 'laser_tuning_curve')#ref=18
exp20.add_session('14-53-20', 'a', 'behavior', '2afc')#200 trials/block,


exp21 = celldatabase.Experiment(subject,
                               '2017-05-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(1220, tetrodes=range(1, 9))
exp21.add_session('14-14-45', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp21.add_session('14-18-15', 'a', 'tc', 'laser_tuning_curve')
exp21.add_session('14-25-20', 'a', 'behavior', '2afc')#200 trials/block,


exp22 = celldatabase.Experiment(subject,
                               '2017-05-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(1260, tetrodes=range(1, 9))
exp22.add_session('13-35-44', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp22.add_session('13-40-44', 'a', 'tc', 'laser_tuning_curve')
exp22.add_session('13-47-33', 'a', 'behavior', '2afc')#200 trials/block,


exp23 = celldatabase.Experiment(subject,
                               '2017-05-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(1300, tetrodes=range(1, 9))
exp23.add_session('16-13-11', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp23.add_session('16-16-26', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('16-23-04', 'a', 'behavior', '2afc')#200 trials/block,


exp24 = celldatabase.Experiment(subject,
                               '2017-05-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(1340, tetrodes=range(1, 9))
exp24.add_session('15-11-38', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp24.add_session('15-14-27', 'a', 'tc', 'laser_tuning_curve')
exp24.add_session('15-21-10', 'a', 'behavior', '2afc')#200 trials/block,


exp25 = celldatabase.Experiment(subject,
                               '2017-05-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(1380, tetrodes=range(1, 9))
exp25.add_session('12-17-03', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp25.add_session('12-19-33', 'a', 'tc', 'laser_tuning_curve')
exp25.add_session('12-26-04', 'a', 'behavior', '2afc')#150 trials/block,

'''
exp26 = celldatabase.Experiment(subject,
                               '2017-05-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(1420, tetrodes=range(1, 9))
exp26.add_session('11-45-06', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp26.add_session('11-47-51', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('11-54-29', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

exp27 = celldatabase.Experiment(subject,
                               '2017-05-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(1420, tetrodes=range(1, 9))
exp27.add_session('14-06-43', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp27.add_session('14-10-13', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('14-17-30', 'a', 'behavior', '2afc')#200 trials/block, 


exp28 = celldatabase.Experiment(subject,
                               '2017-05-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(1460, tetrodes=range(1, 9))
exp28.add_session('14-39-44', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp28.add_session('14-42-42', 'a', 'tc', 'laser_tuning_curve')
exp28.add_session('14-49-17', 'a', 'behavior', '2afc')#200 trials/block, 


exp29 = celldatabase.Experiment(subject,
                               '2017-05-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(1500, tetrodes=range(1, 9))
exp29.add_session('16-48-01', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp29.add_session('16-50-56', 'a', 'tc', 'laser_tuning_curve')
exp29.add_session('16-57-49', 'a', 'behavior', '2afc')#200 trials/block, 


exp30 = celldatabase.Experiment(subject,
                               '2017-05-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(1540, tetrodes=range(1, 9))
exp30.add_session('11-45-17', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp30.add_session('11-47-51', 'a', 'tc', 'laser_tuning_curve')
exp30.add_session('11-54-58', 'a', 'behavior', '2afc')#150 trials/block, 


exp31 = celldatabase.Experiment(subject,
                               '2017-05-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp31)

exp31.add_site(1580, tetrodes=range(1, 9))
exp31.add_session('10-30-34', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp31.add_session('10-33-23', 'a', 'tc', 'laser_tuning_curve')
exp31.add_session('10-40-22', 'a', 'behavior', '2afc')#200 trials/block, 


exp32 = celldatabase.Experiment(subject,
                               '2017-05-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp32)

exp32.add_site(1620, tetrodes=range(1, 9))
#exp32.add_session('10-17-44', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp32.add_session('10-21-18', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp32.add_session('10-25-07', 'a', 'tc', 'laser_tuning_curve')#ref=17
exp32.add_session('10-31-52', 'a', 'behavior', '2afc')#200 trials/block, 

'''
exp33 = celldatabase.Experiment(subject,
                               '2017-05-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp33)

exp33.add_site(1660, tetrodes=range(1, 9))
exp33.add_session('12-55-17', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp33.add_session('12-57-39', 'a', 'tc', 'laser_tuning_curve')
exp33.add_session('13-04-36', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials


exp34 = celldatabase.Experiment(subject,
                               '2017-05-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp34)

exp34.add_site(1660, tetrodes=range(1, 9))
exp34.add_session('10-19-04', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp34.add_session('10-22-30', 'a', 'tc', 'laser_tuning_curve')
exp34.add_session('10-29-52', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

for ind, exp in enumerate(experiments):
    for site in exp.sites:
        site.clusterFolder = 'multisession_exp{}site0'.format(ind)

tetrodeLengthList = [330, 485, 580, 0, 660, 680, 485, 680] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (540, 1620)
