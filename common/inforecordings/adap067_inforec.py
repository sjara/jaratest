from jaratoolbox import celldatabase

subject = 'adap067'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''
'''
exp0 = celldatabase.Experiment(subject,
                               '2017-09-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(500, tetrodes=range(1, 9))
exp0.add_session('12-37-16', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp0.add_session('12-42-30', None, 'noiseburst', 'laser_tuning_curve')#ref=20
exp0.add_session('12-46-50', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp0.add_session('15-22-21', 'a', 'tc', 'laser_tuning_curve')


exp1 = celldatabase.Experiment(subject,
                               '2017-09-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(540, tetrodes=range(1, 9))
exp1.add_session('14-13-06', None, 'noiseburst', 'laser_tuning_curve')#ref=18
exp1.add_session('14-16-36', 'a', 'tc', 'laser_tuning_curve')
'''

exp2 = celldatabase.Experiment(subject,
                               '2017-09-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(580, tetrodes=range(1, 9))
#exp2.add_session('13-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=10
exp2.add_session('13-48-09', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp2.add_session('13-51-45', 'a', 'tc', 'laser_tuning_curve')
exp2.add_session('13-59-23', 'a', 'behavior', '2afc')#150 trials/block, 


exp3 = celldatabase.Experiment(subject,
                               '2017-09-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(620, tetrodes=range(1, 9))
#exp3.add_session('15-10-13', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp3.add_session('15-14-43', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp3.add_session('15-18-01', 'a', 'tc', 'laser_tuning_curve')#ref=13
exp3.add_session('15-25-24', 'a', 'behavior', '2afc')#150 trials/block, 


exp4 = celldatabase.Experiment(subject,
                               '2017-09-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(660, tetrodes=range(1, 9))
exp4.add_session('13-43-36', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp4.add_session('13-46-55', 'a', 'tc', 'laser_tuning_curve')
exp4.add_session('13-54-15', 'a', 'behavior', '2afc')#150 trials/block, 


exp5 = celldatabase.Experiment(subject,
                               '2017-09-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(700, tetrodes=range(1, 9))
exp5.add_session('13-29-53', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp5.add_session('13-32-25', 'a', 'tc', 'laser_tuning_curve')
exp5.add_session('13-39-35', 'a', 'behavior', '2afc')#150 trials/block, 


exp6 = celldatabase.Experiment(subject,
                               '2017-09-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(740, tetrodes=range(1, 9))
exp6.add_session('13-03-12', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp6.add_session('13-05-49', 'a', 'tc', 'laser_tuning_curve')
exp6.add_session('13-12-59', 'a', 'behavior', '2afc')#150 trials/block, 


exp7 = celldatabase.Experiment(subject,
                               '2017-09-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(780, tetrodes=range(1, 9))
exp7.add_session('12-05-37', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp7.add_session('12-08-44', 'a', 'tc', 'laser_tuning_curve')
exp7.add_session('12-15-25', 'a', 'behavior', '2afc')#150 trials/block, 


exp8 = celldatabase.Experiment(subject,
                               '2017-09-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(820, tetrodes=range(1, 9))
exp8.add_session('15-26-39', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp8.add_session('15-30-16', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('15-37-13', 'a', 'behavior', '2afc')#150 trials/block, 


exp9 = celldatabase.Experiment(subject,
                               '2017-09-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(860, tetrodes=range(1, 9))
exp9.add_session('14-38-55', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp9.add_session('14-41-51', 'a', 'tc', 'laser_tuning_curve')
exp9.add_session('14-48-32', 'a', 'behavior', '2afc')#150 trials/block, 


exp10 = celldatabase.Experiment(subject,
                               '2017-09-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(900, tetrodes=range(1, 9))
exp10.add_session('14-01-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp10.add_session('14-04-37', 'a', 'tc', 'laser_tuning_curve')
exp10.add_session('14-11-14', 'a', 'behavior', '2afc')#150 trials/block, 


exp11 = celldatabase.Experiment(subject,
                               '2017-09-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(940, tetrodes=range(1, 9))
exp11.add_session('13-40-29', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp11.add_session('13-43-12', 'a', 'tc', 'laser_tuning_curve')
exp11.add_session('13-49-51', 'a', 'behavior', '2afc')#150 trials/block, 


exp12 = celldatabase.Experiment(subject,
                               '2017-09-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(980, tetrodes=range(1, 9))
exp12.add_session('12-38-16', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp12.add_session('12-40-56', 'a', 'tc', 'laser_tuning_curve')
exp12.add_session('12-47-47', 'a', 'behavior', '2afc')#150 trials/block, 


exp13 = celldatabase.Experiment(subject,
                               '2017-09-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(1020, tetrodes=range(1, 9))
exp13.add_session('14-50-45', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp13.add_session('14-54-03', 'a', 'tc', 'laser_tuning_curve')
exp13.add_session('15-02-00', 'a', 'behavior', '2afc')#150 trials/block, 


exp14 = celldatabase.Experiment(subject,
                               '2017-09-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(1060, tetrodes=range(1, 9))
exp14.add_session('12-25-00', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp14.add_session('12-27-31', 'a', 'tc', 'laser_tuning_curve')
exp14.add_session('12-34-40', 'a', 'behavior', '2afc')#150 trials/block, 


exp15 = celldatabase.Experiment(subject,
                               '2017-09-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(1100, tetrodes=range(1, 9))
exp15.add_session('13-39-38', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp15.add_session('13-42-19', 'a', 'tc', 'laser_tuning_curve')
exp15.add_session('13-50-55', 'a', 'behavior', '2afc')#150 trials/block, 


exp16 = celldatabase.Experiment(subject,
                               '2017-09-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(1140, tetrodes=range(1, 9))
exp16.add_session('13-24-32', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp16.add_session('13-27-39', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('13-34-32', 'a', 'behavior', '2afc')#150 trials/block, 


exp17 = celldatabase.Experiment(subject,
                               '2017-09-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(1180, tetrodes=range(1, 9))
exp17.add_session('17-10-05', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp17.add_session('17-13-11', 'a', 'tc', 'laser_tuning_curve')
exp17.add_session('17-20-04', 'a', 'behavior', '2afc')#150 trials/block, 


exp18 = celldatabase.Experiment(subject,
                               '2017-09-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(1220, tetrodes=range(1, 9))
exp18.add_session('13-06-29', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp18.add_session('13-09-13', 'a', 'tc', 'laser_tuning_curve')
exp18.add_session('13-16-33', 'a', 'behavior', '2afc')#150 trials/block, 


exp19 = celldatabase.Experiment(subject,
                               '2017-09-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(1260, tetrodes=range(1, 9))
exp19.add_session('15-07-42', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp19.add_session('15-10-03', 'a', 'tc', 'laser_tuning_curve')
exp19.add_session('15-16-45', 'a', 'behavior', '2afc')#150 trials/block, 


exp20 = celldatabase.Experiment(subject,
                               '2017-09-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(1300, tetrodes=range(1, 9))
exp20.add_session('14-37-01', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp20.add_session('14-39-21', 'a', 'tc', 'laser_tuning_curve')
exp20.add_session('14-46-01', 'a', 'behavior', '2afc')#150 trials/block, 


exp21 = celldatabase.Experiment(subject,
                               '2017-09-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(1340, tetrodes=range(1, 9))
exp21.add_session('15-23-57', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp21.add_session('15-27-41', 'a', 'tc', 'laser_tuning_curve')
exp21.add_session('15-35-03', 'a', 'behavior', '2afc')#150 trials/block, 


exp22 = celldatabase.Experiment(subject,
                               '2017-09-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(1380, tetrodes=range(1, 9))
exp22.add_session('14-39-03', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp22.add_session('14-41-48', 'a', 'tc', 'laser_tuning_curve')
exp22.add_session('14-48-49', 'a', 'behavior', '2afc')#150 trials/block, 


exp23 = celldatabase.Experiment(subject,
                               '2017-09-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(1420, tetrodes=range(1, 9))
exp23.add_session('14-54-03', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp23.add_session('14-57-24', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('15-04-24', 'a', 'behavior', '2afc')#200 trials/block, 


exp24 = celldatabase.Experiment(subject,
                               '2017-09-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(1460, tetrodes=range(1, 9))
#exp24.add_session('16-03-37', None, 'noiseburst', 'laser_tuning_curve')#ref=22
exp24.add_session('16-06-41', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp24.add_session('16-10-03', 'a', 'tc', 'laser_tuning_curve')#ref=14
#exp24.add_session('16-16-46', 'b', 'tc', 'laser_tuning_curve')#ref=15
exp24.add_session('16-22-32', 'a', 'behavior', '2afc')#200 trials/block, 


exp25 = celldatabase.Experiment(subject,
                               '2017-09-29',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(1500, tetrodes=range(1, 9))
exp25.add_session('16-46-46', None, 'noiseburst', 'laser_tuning_curve')#ref=15
exp25.add_session('16-49-13', 'a', 'tc', 'laser_tuning_curve')
exp25.add_session('16-56-02', 'a', 'behavior', '2afc')#150 trials/block, 


exp26 = celldatabase.Experiment(subject,
                               '2017-09-30',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(1540, tetrodes=range(1, 9))
exp26.add_session('14-16-13', None, 'noiseburst', 'laser_tuning_curve')#ref=15
exp26.add_session('14-18-33', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('14-26-49', 'a', 'behavior', '2afc')#150 trials/block, 


exp27 = celldatabase.Experiment(subject,
                               '2017-10-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(1580, tetrodes=range(1, 9))
exp27.add_session('15-33-21', None, 'noiseburst', 'laser_tuning_curve')#ref=15
exp27.add_session('15-35-56', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('15-43-35', 'a', 'behavior', '2afc')#150 trials/block, 


exp28 = celldatabase.Experiment(subject,
                               '2017-10-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(1620, tetrodes=range(1, 9))
#exp28.add_session('17-45-43', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp28.add_session('17-48-42', None, 'noiseburst', 'laser_tuning_curve')#ref=21
exp28.add_session('17-51-01', 'a', 'tc', 'laser_tuning_curve')#ref=21
exp28.add_session('17-58-26', 'a', 'behavior', '2afc')#150 trials/block,


exp29 = celldatabase.Experiment(subject,
                               '2017-10-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(1660, tetrodes=range(1, 9))
exp29.add_session('16-54-29', None, 'noiseburst', 'laser_tuning_curve')#ref=21
exp29.add_session('16-56-58', 'a', 'tc', 'laser_tuning_curve')#ref=21
exp29.add_session('17-03-25', 'a', 'behavior', '2afc')#150 trials/block,


exp30 = celldatabase.Experiment(subject,
                               '2017-10-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(1700, tetrodes=range(1, 9))
exp30.add_session('15-18-31', None, 'noiseburst', 'laser_tuning_curve')#ref=21
exp30.add_session('15-21-33', 'a', 'tc', 'laser_tuning_curve')#ref=21
exp30.add_session('15-29-21', 'a', 'behavior', '2afc')#150 trials/block,

'''
# Somehow on this date the 2afc behavior file was not saved
exp31 = celldatabase.Experiment(subject,
                               '2017-10-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp31)

exp31.add_site(1740, tetrodes=range(1, 9))
exp31.add_session('16-26-19', None, 'noiseburst', 'laser_tuning_curve')#ref=9
#exp31.add_session('16-28-57', None, 'noiseburst', 'laser_tuning_curve')#ref=21
exp31.add_session('16-32-20', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp31.add_session('16-39-09', 'a', 'behavior', '2afc')#150 trials/block,
'''

exp32 = celldatabase.Experiment(subject,
                               '2017-10-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp32)

exp32.add_site(1780, tetrodes=range(1, 9))
exp32.add_session('16-11-13', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp32.add_session('16-13-46', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp32.add_session('16-20-52', 'a', 'behavior', '2afc')#150 trials/block,


exp33 = celldatabase.Experiment(subject,
                               '2017-10-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp33)

exp33.add_site(1820, tetrodes=range(1, 9))
exp33.add_session('16-34-53', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp33.add_session('16-37-21', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp33.add_session('16-44-49', 'a', 'behavior', '2afc')#150 trials/block,


exp34 = celldatabase.Experiment(subject,
                               '2017-10-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp34)

exp34.add_site(1860, tetrodes=range(1, 9))
exp34.add_session('15-28-07', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp34.add_session('15-30-29', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp34.add_session('15-36-47', 'a', 'behavior', '2afc')#150 trials/block,


exp35 = celldatabase.Experiment(subject,
                               '2017-10-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp35)

exp35.add_site(1900, tetrodes=range(1, 9))
exp35.add_session('14-32-09', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp35.add_session('14-34-51', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp35.add_session('14-41-44', 'a', 'behavior', '2afc')#150 trials/block,


exp36 = celldatabase.Experiment(subject,
                               '2017-10-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp36)

exp36.add_site(1940, tetrodes=range(1, 9))
exp36.add_session('15-41-44', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp36.add_session('15-44-00', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp36.add_session('15-50-19', 'a', 'behavior', '2afc')#150 trials/block,


exp37 = celldatabase.Experiment(subject,
                               '2017-10-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp37)

exp37.add_site(1980, tetrodes=range(1, 9))
exp37.add_session('14-33-07', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp37.add_session('14-35-24', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp37.add_session('14-42-07', 'a', 'behavior', '2afc')#150 trials/block,


exp38 = celldatabase.Experiment(subject,
                               '2017-10-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp38)

exp38.add_site(2020, tetrodes=range(1, 9))
exp38.add_session('14-54-08', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp38.add_session('14-56-24', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp38.add_session('15-03-37', 'a', 'behavior', '2afc')#150 trials/block,


exp39 = celldatabase.Experiment(subject,
                               '2017-10-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp39)

exp39.add_site(2060, tetrodes=range(1, 9))
exp39.add_session('15-43-21', None, 'noiseburst', 'laser_tuning_curve')#ref=11
exp39.add_session('15-45-46', 'a', 'tc', 'laser_tuning_curve')#ref=11
exp39.add_session('15-52-01', 'a', 'behavior', '2afc')#150 trials/block,


exp40 = celldatabase.Experiment(subject,
                               '2017-10-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp40)

exp40.add_site(2100, tetrodes=range(1, 9))
#exp40.add_session('15-29-23', None, 'noiseburst', 'laser_tuning_curve')#ref=11
#exp40.add_session('15-33-20', None, 'noiseburst', 'laser_tuning_curve')#ref=6
exp40.add_session('15-57-32', None, 'noiseburst', 'laser_tuning_curve')#ref=24
#exp40.add_session('15-36-22', 'a', 'tc', 'laser_tuning_curve')#ref=6
exp40.add_session('16-00-23', 'b', 'tc', 'laser_tuning_curve')#ref=6
exp40.add_session('16-06-27', 'a', 'behavior', '2afc')#150 trials/block,


exp41 = celldatabase.Experiment(subject,
                               '2017-10-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp41)

exp41.add_site(2140, tetrodes=range(1, 9))
exp41.add_session('15-25-02', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp41.add_session('15-27-52', 'a', 'tc', 'laser_tuning_curve')#ref=14
exp41.add_session('15-36-58', 'a', 'behavior', '2afc')#150 trials/block,


exp42 = celldatabase.Experiment(subject,
                               '2017-10-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp42)

exp42.add_site(2180, tetrodes=range(1, 9))
exp42.add_session('16-43-16', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp42.add_session('16-45-37', 'a', 'tc', 'laser_tuning_curve')#ref=14
exp42.add_session('16-52-00', 'a', 'behavior', '2afc')#150 trials/block,


exp43 = celldatabase.Experiment(subject,
                               '2017-10-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp43)

exp43.add_site(2220, tetrodes=range(1, 9))
exp43.add_session('14-52-54', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp43.add_session('14-55-29', 'a', 'tc', 'laser_tuning_curve')#ref=14
exp43.add_session('15-03-07', 'a', 'behavior', '2afc')#150 trials/block,

'''
exp44 = celldatabase.Experiment(subject,
                               '2017-10-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp44)

exp44.add_site(2260, tetrodes=range(1, 9))
exp44.add_session('16-37-22', None, 'noiseburst', 'laser_tuning_curve')#ref=14
exp44.add_session('16-44-45', None, 'noiseburst', 'laser_tuning_curve')#ref=22, no longer has sound response
'''

for ind, exp in enumerate(experiments):
    for site in exp.sites:
        site.clusterFolder = 'multisession_exp{}site0'.format(ind)

