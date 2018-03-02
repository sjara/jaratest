from jaratoolbox import celldatabase

subject = 'gosi004'
experiments = []

'''
Experiments with <550 valid trials commented out
'''
'''
exp0 = celldatabase.Experiment(subject,
                               '2017-02-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(500, tetrodes=range(1, 9))
exp0.add_session('17-27-51', None, 'noiseburst', 'laser_tuning_curve')
exp0.add_session('17-29-40', None, 'noiseburst', 'laser_tuning_curve')
exp0.add_session('17-36-07', 'a', 'tc', 'laser_tuning_curve')



exp1 = celldatabase.Experiment(subject,
                               '2017-02-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(500, tetrodes=range(1, 9))
exp1.add_session('17-13-41', None, 'noiseburst', 'laser_tuning_curve')
exp1.add_session('17-22-09', 'a', 'tc', 'laser_tuning_curve')

exp2 = celldatabase.Experiment(subject,
                               '2017-02-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(500, tetrodes=range(1, 9))
exp2.add_session('17-05-30', None, 'noiseburst', 'laser_tuning_curve')
exp2.add_session('17-16-32', 'a', 'tc', 'laser_tuning_curve')

exp3 = celldatabase.Experiment(subject,
                               '2017-02-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(500, tetrodes=range(1, 9))
exp3.add_session('14-08-34', None, 'noiseburst', 'laser_tuning_curve')
exp3.add_session('14-12-47', 'a', 'tc', 'laser_tuning_curve')
exp3.add_session('14-21-45', 'a', 'behavior', '2afc')
exp3.add_session('14-37-13', None, 'behavior2', '2afc')#unplugged during behavior
exp3.add_session('15-01-25', '4', 'behavior3', '2afc')


exp4 = celldatabase.Experiment(subject,
                               '2017-02-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(500, tetrodes=range(1, 9))
exp4.add_session('12-30-17', None, 'noiseburst', 'laser_tuning_curve')
exp4.add_session('12-35-55', 'a', 'tc', 'laser_tuning_curve')
exp4.add_session('12-45-11', 'a', 'behavior', '2afc')#unplugged during behavior


exp5 = celldatabase.Experiment(subject,
                               '2017-02-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(500, tetrodes=range(1, 9))
exp5.add_session('15-46-30', None, 'noiseburst', 'laser_tuning_curve')
exp5.add_session('15-49-11', 'a', 'tc', 'laser_tuning_curve')
exp5.add_session('15-54-13', 'a', 'behavior', '2afc')

exp6 = celldatabase.Experiment(subject,
                               '2017-02-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(500, tetrodes=range(1, 9))
exp6.add_session('15-28-18', None, 'noiseburst', 'laser_tuning_curve')
exp6.add_session('15-30-46', 'a', 'tc', 'laser_tuning_curve')
exp6.add_session('15-35-00', 'a', 'behavior', '2afc')
'''

exp7 = celldatabase.Experiment(subject,
                               '2017-02-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(500, tetrodes=range(1, 9))
exp7.add_session('16-50-17', None, 'noiseburst', 'laser_tuning_curve')#ref=17
exp7.add_session('16-52-40', 'a', 'tc', 'laser_tuning_curve') #ref=17
exp7.add_session('16-59-23', 'a', 'behavior', '2afc')#ref=17

'''
exp8 = celldatabase.Experiment(subject,
                               '2017-02-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(500, tetrodes=range(1, 9))
exp8.add_session('16-13-50', None, 'noiseburst', 'laser_tuning_curve')
exp8.add_session('16-19-01', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('16-24-37', 'a', 'behavior', '2afc')

exp9 = celldatabase.Experiment(subject,
                               '2017-02-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(500, tetrodes=range(1, 9))
exp9.add_session('13-56-30', None, 'noiseburst', 'laser_tuning_curve')
exp9.add_session('13-59-31', 'a', 'tc', 'laser_tuning_curve')
exp9.add_session('14-15-31', 'b', 'behavior', '2afc')
'''

exp10 = celldatabase.Experiment(subject,
                               '2017-02-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(500, tetrodes=range(1, 9))
exp10.add_session('14-38-31', None, 'noiseburst', 'laser_tuning_curve')#ref=19
exp10.add_session('14-42-10', 'a', 'tc', 'laser_tuning_curve')#ref=19; 177 trials
exp10.add_session('14-49-01', 'a', 'behavior', '2afc')#ref=19

'''
exp11 = celldatabase.Experiment(subject,
                               '2017-02-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(580, tetrodes=range(1, 9))
#exp11.add_session('15-39-55', None, 'noiseburst', 'laser_tuning_curve')#changed thresholds after this recording
exp11.add_session('16-06-29', None, 'noiseburst', 'laser_tuning_curve')
exp11.add_session('16-16-10', 'a', 'tc', 'laser_tuning_curve')
exp11.add_session('16-23-04', 'a', 'behavior', '2afc')

exp12 = celldatabase.Experiment(subject,
                               '2017-02-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(580, tetrodes=range(1, 9))
exp12.add_session('09-42-49', None, 'noiseburst', 'laser_tuning_curve')
exp12.add_session('09-46-29', 'a', 'tc', 'laser_tuning_curve')
exp12.add_session('09-52-26', 'a', 'behavior', '2afc')
'''

exp13 = celldatabase.Experiment(subject,
                               '2017-02-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(580, tetrodes=range(1, 9))
exp13.add_session('17-35-11', None, 'noiseburst', 'laser_tuning_curve')#ref=19
exp13.add_session('17-38-56', 'a', 'tc', 'laser_tuning_curve')#ref=19; 159 trials
exp13.add_session('18-03-10', 'a', 'behavior', '2afc')#ref=19

exp14 = celldatabase.Experiment(subject,
                               '2017-02-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(580, tetrodes=range(1, 9))
exp14.add_session('16-57-19', None, 'noiseburst', 'laser_tuning_curve')#ref=19
exp14.add_session('17-03-44', 'a', 'tc', 'laser_tuning_curve')#ref=19; 162 trials
exp14.add_session('17-10-22', 'a', 'behavior', '2afc')#ref=19


exp15 = celldatabase.Experiment(subject,
                               '2017-02-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(620, tetrodes=range(1, 9))
exp15.add_session('16-26-35', None, 'noiseburst', 'laser_tuning_curve')#ref=19 
#exp15.add_session('16-31-12', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp15.add_session('16-34-45', 'a', 'tc', 'laser_tuning_curve')#ref=19; 168 trials
exp15.add_session('16-39-07', 'a', 'behavior', '2afc')#ref=19

'''
exp16 = celldatabase.Experiment(subject,
                               '2017-02-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(660, tetrodes=range(1, 9))
exp16.add_session('15-19-46', None, 'noiseburst', 'laser_tuning_curve')
exp16.add_session('15-24-18', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('15-31-56', 'a', 'behavior', '2afc')
'''

exp17 = celldatabase.Experiment(subject,
                               '2017-02-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(660, tetrodes=range(1, 9))
exp17.add_session('14-59-44', None, 'noiseburst', 'laser_tuning_curve')#ref=29
#exp17.add_session('15-03-39', None, 'noiseburst', 'laser_tuning_curve')#ref=19
exp17.add_session('15-08-28', 'a', 'tc', 'laser_tuning_curve')#ref=29; 170 trials
exp17.add_session('15-14-12', 'a', 'behavior', '2afc')#ref=29

'''
exp18 = celldatabase.Experiment(subject,
                               '2017-02-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(700, tetrodes=range(1, 9))
exp18.add_session('15-20-16', None, 'noiseburst', 'laser_tuning_curve')
#exp18.add_session('15-24-52', None, 'noiseburst', 'laser_tuning_curve')
exp18.add_session('15-31-22', 'a', 'tc', 'laser_tuning_curve')
exp18.add_session('15-38-38', 'a', 'behavior', '2afc')
'''

exp19 = celldatabase.Experiment(subject,
                               '2017-02-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(700, tetrodes=range(1, 9))
exp19.add_session('15-00-21', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp19.add_session('15-04-00', 'a', 'tc', 'laser_tuning_curve')#ref=29; 169 trials
exp19.add_session('15-08-57', 'a', 'behavior', '2afc')#ref=29

'''
exp20 = celldatabase.Experiment(subject,
                               '2017-02-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(740, tetrodes=range(1, 9))
#exp20.add_session('16-29-18', None, 'noiseburst', 'laser_tuning_curve')
exp20.add_session('16-32-13', None, 'noiseburst', 'laser_tuning_curve')
exp20.add_session('16-34-49', 'a', 'tc', 'laser_tuning_curve')
exp20.add_session('16-40-04', 'a', 'behavior', '2afc')
'''

exp21 = celldatabase.Experiment(subject,
                               '2017-02-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(740, tetrodes=range(1, 9))
exp21.add_session('17-00-46', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp21.add_session('17-04-47', 'a', 'tc', 'laser_tuning_curve')#ref=29; 163 trials
exp21.add_session('17-09-21', 'a', 'behavior', '2afc')#ref=29

exp22 = celldatabase.Experiment(subject,
                               '2017-02-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(780, tetrodes=range(1, 9))
exp22.add_session('16-22-18', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp22.add_session('16-24-53', 'a', 'tc', 'laser_tuning_curve')#ref=29; 171 trials
exp22.add_session('16-29-37', 'a', 'behavior', '2afc')#ref=29

'''
exp23 = celldatabase.Experiment(subject,
                               '2017-03-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(820, tetrodes=range(1, 9))
exp23.add_session('15-32-08', None, 'noiseburst', 'laser_tuning_curve')#rig2
exp23.add_session('15-40-35', None, 'noiseburst', 'laser_tuning_curve')
exp23.add_session('15-45-34', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('15-50-06', 'a', 'behavior', '2afc')

exp24 = celldatabase.Experiment(subject,
                               '2017-03-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(820, tetrodes=range(1, 9))
exp24.add_session('14-03-06', None, 'noiseburst', 'laser_tuning_curve')
exp24.add_session('14-06-38', 'a', 'tc', 'laser_tuning_curve')
exp24.add_session('14-11-47', 'a', 'behavior', '2afc')
'''

exp25 = celldatabase.Experiment(subject,
                               '2017-03-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(820, tetrodes=range(1, 9))
exp25.add_session('15-53-45', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp25.add_session('15-56-28', 'a', 'tc', 'laser_tuning_curve')#ref=29; 160 trials
exp25.add_session('16-17-38', 'b', 'tc', 'laser_tuning_curve')#ref=29; 310 trials
exp25.add_session('16-24-05', 'a', 'behavior', '2afc')#ref=29

'''
exp26 = celldatabase.Experiment(subject,
                               '2017-03-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(860, tetrodes=range(1, 9))
#exp26.add_session('17-05-33', None, 'noiseburst', 'laser_tuning_curve')#ref 27
exp26.add_session('17-08-15', None, 'noiseburst', 'laser_tuning_curve')#ref 29
exp26.add_session('17-10-34', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('17-18-08', 'a', 'behavior', '2afc')#unplugged during behavior

exp27 = celldatabase.Experiment(subject,
                               '2017-03-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(860, tetrodes=range(1, 9))
exp27.add_session('14-38-38', None, 'noiseburst', 'laser_tuning_curve')
exp27.add_session('14-43-42', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('14-52-42', 'a', 'behavior', '2afc')

exp28 = celldatabase.Experiment(subject,
                               '2017-03-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(860, tetrodes=range(1, 9))
exp28.add_session('15-55-25', None, 'noiseburst', 'laser_tuning_curve')
exp28.add_session('15-59-30', 'a', 'tc', 'laser_tuning_curve')
exp28.add_session('16-10-14', 'a', 'behavior', '2afc')

'''
exp29 = celldatabase.Experiment(subject,
                               '2017-03-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(860, tetrodes=range(1, 9))
exp29.add_session('16-23-33', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp29.add_session('16-26-35', 'a', 'tc', 'laser_tuning_curve')#ref=29; 319 trials
exp29.add_session('16-33-44', 'a', 'behavior', '2afc')#ref=29

'''
exp30 = celldatabase.Experiment(subject,
                               '2017-03-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(900, tetrodes=range(1, 9))
#exp30.add_session('15-29-18', None, 'noiseburst', 'laser_tuning_curve')#ref 18
#exp30.add_session('15-44-20', None, 'noiseburst', 'laser_tuning_curve')#ref 21
exp30.add_session('15-50-22', None, 'noiseburst', 'laser_tuning_curve')#ref 9
exp30.add_session('15-53-25', 'a', 'tc', 'laser_tuning_curve')
exp30.add_session('16-01-03', 'a', 'behavior', '2afc')

exp31 = celldatabase.Experiment(subject,
                               '2017-03-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp31)

exp31.add_site(900, tetrodes=range(1, 9))
exp31.add_session('14-41-51', None, 'noiseburst', 'laser_tuning_curve')
exp31.add_session('14-44-46', 'a', 'tc', 'laser_tuning_curve')
exp31.add_session('14-53-11', 'a', 'behavior', '2afc')

exp32 = celldatabase.Experiment(subject,
                               '2017-03-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp32)

exp32.add_site(900, tetrodes=range(1, 9))
exp32.add_session('17-50-59', None, 'noiseburst', 'laser_tuning_curve')
exp32.add_session('17-54-03', 'a', 'tc', 'laser_tuning_curve')
exp32.add_session('18-01-53', 'a', 'behavior', '2afc')
'''

exp33 = celldatabase.Experiment(subject,
                               '2017-03-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp33)

exp33.add_site(900, tetrodes=range(1, 9))
exp33.add_session('18-00-51', None, 'noiseburst', 'laser_tuning_curve')
exp33.add_session('18-03-24', 'a', 'tc', 'laser_tuning_curve')
exp33.add_session('18-09-53', 'a', 'behavior', '2afc')

'''
exp34 = celldatabase.Experiment(subject,
                               '2017-03-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp34)

exp34.add_site(940, tetrodes=range(1, 9))
exp34.add_session('13-33-38', None, 'noiseburst', 'laser_tuning_curve')
exp34.add_session('13-40-12', 'a', 'tc', 'laser_tuning_curve')
exp34.add_session('13-49-43', 'a', 'behavior', '2afc')


exp35 = celldatabase.Experiment(subject,
                               '2017-03-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp35)

exp35.add_site(940, tetrodes=range(1, 9))
exp35.add_session('15-58-37', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=9
exp35.add_session('16-07-28', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=9, thresholds=50
exp35.add_session('16-18-55', None, 'noiseburst', 'laser_tuning_curve')#rig 2, ref=9, thresholds=50
exp35.add_session('16-37-55', None, 'noiseburst', 'laser_tuning_curve')#rig 3, ref=29
exp35.add_session('16-45-20', 'a', 'tc', 'laser_tuning_curve')
exp35.add_session('16-54-59', 'a', 'behavior', '2afc')


exp36 = celldatabase.Experiment(subject,
                               '2017-03-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp36)

exp36.add_site(940, tetrodes=range(1, 9))
exp36.add_session('17-17-20', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp36.add_session('17-21-44', 'a', 'tc', 'laser_tuning_curve')
exp36.add_session('17-29-14', 'a', 'behavior', '2afc')
'''

exp37 = celldatabase.Experiment(subject,
                               '2017-03-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp37)

exp37.add_site(940, tetrodes=range(1, 9))
exp37.add_session('15-15-43', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp37.add_session('15-18-46', 'a', 'tc', 'laser_tuning_curve')
exp37.add_session('15-26-11', 'a', 'behavior', '2afc')

'''
exp38 = celldatabase.Experiment(subject,
                               '2017-03-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp38)

exp38.add_site(940, tetrodes=range(1, 9))
exp38.add_session('14-34-40', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp38.add_session('14-41-34', 'a', 'tc', 'laser_tuning_curve')
exp38.add_session('14-50-42', 'a', 'behavior', '2afc')# Unplugged during behavior ~463 trials
'''

exp39 = celldatabase.Experiment(subject,
                               '2017-03-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp39)

exp39.add_site(940, tetrodes=range(1, 9))
exp39.add_session('17-03-17', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp39.add_session('17-06-02', 'a', 'tc', 'laser_tuning_curve')
exp39.add_session('17-16-47', 'a', 'behavior', '2afc')#change to 150 trials per block

exp40 = celldatabase.Experiment(subject,
                               '2017-03-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp40)

exp40.add_site(980, tetrodes=range(1, 9))
exp40.add_session('16-14-29', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp40.add_session('16-17-33', 'a', 'tc', 'laser_tuning_curve')
exp40.add_session('16-26-10', 'a', 'behavior', '2afc')


exp41 = celldatabase.Experiment(subject,
                               '2017-03-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp41)

exp41.add_site(1020, tetrodes=range(1, 9))
exp41.add_session('15-36-50', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp41.add_session('15-39-24', 'a', 'tc', 'laser_tuning_curve')#data didn't save
exp41.add_session('15-52-25', 'b', 'tc', 'laser_tuning_curve')
exp41.add_session('16-00-02', 'a', 'behavior', '2afc')


exp42 = celldatabase.Experiment(subject,
                               '2017-03-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp42)

exp42.add_site(1060, tetrodes=range(1, 9))
exp42.add_session('16-15-36', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp42.add_session('16-18-22', 'a', 'tc', 'laser_tuning_curve')
exp42.add_session('16-26-56', 'a', 'behavior', '2afc')

exp43 = celldatabase.Experiment(subject,
                               '2017-03-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp43)

exp43.add_site(1100, tetrodes=range(1, 9))
exp43.add_session('16-47-00', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp43.add_session('16-50-26', 'a', 'tc', 'laser_tuning_curve')
exp43.add_session('16-57-34', 'a', 'behavior', '2afc')

exp44 = celldatabase.Experiment(subject,
                               '2017-03-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp44)

exp44.add_site(1140, tetrodes=range(1, 9))
exp44.add_session('11-47-20', None, 'noiseburst', 'laser_tuning_curve')# ref=10
exp44.add_session('11-50-13', 'a', 'tc', 'laser_tuning_curve')
exp44.add_session('11-57-08', 'a', 'behavior', '2afc')

exp45 = celldatabase.Experiment(subject,
                               '2017-03-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp45)

exp45.add_site(1180, tetrodes=range(1, 9))
exp45.add_session('16-54-31', None, 'noiseburst', 'laser_tuning_curve')# ref=10
exp45.add_session('16-57-13', 'a', 'tc', 'laser_tuning_curve')#plotted like a noiseburst so re-ran tuning curve
exp45.add_session('17-07-00', 'b', 'tc', 'laser_tuning_curve')
exp45.add_session('17-14-19', 'a', 'behavior', '2afc')

exp46 = celldatabase.Experiment(subject,
                               '2017-03-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp46)

exp46.add_site(1220, tetrodes=range(1, 9))
exp46.add_session('15-58-35', None, 'noiseburst', 'laser_tuning_curve')# ref=10
exp46.add_session('16-01-23', 'a', 'tc', 'laser_tuning_curve')
exp46.add_session('16-08-30', 'a', 'behavior', '2afc')

exp47 = celldatabase.Experiment(subject,
                               '2017-03-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp47)

exp47.add_site(1260, tetrodes=range(1, 9))
exp47.add_session('10-42-28', None, 'noiseburst', 'laser_tuning_curve')# ref=10
exp47.add_session('10-47-49', None, 'noiseburst', 'laser_tuning_curve')# ref=28
exp47.add_session('10-55-08', 'a', 'tc', 'laser_tuning_curve')# ref=28
exp47.add_session('11-02-31', 'a', 'behavior', '2afc')

exp48 = celldatabase.Experiment(subject,
                               '2017-03-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp48)

exp48.add_site(1260, tetrodes=range(1, 9))
exp48.add_session('11-35-02', None, 'noiseburst', 'laser_tuning_curve')# ref=28
exp48.add_session('11-41-04', 'a', 'tc', 'laser_tuning_curve')
exp48.add_session('11-49-41', 'a', 'behavior', '2afc')

'''
exp49 = celldatabase.Experiment(subject,
                               '2017-04-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp49)

exp49.add_site(1300, tetrodes=range(1, 9))
exp49.add_session('16-10-30', None, 'noiseburst', 'laser_tuning_curve')# ref=28
exp49.add_session('16-16-08', None, 'noiseburst', 'laser_tuning_curve')# ref=16
exp49.add_session('16-19-04', 'a', 'tc', 'laser_tuning_curve')# ref=16
exp49.add_session('16-27-20', 'a', 'behavior', '2afc')


exp50 = celldatabase.Experiment(subject,
                               '2017-04-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp50)

exp50.add_site(1340, tetrodes=range(1, 9))
exp50.add_session('14-46-17', None, 'noiseburst', 'laser_tuning_curve')#ref=29. Moved deeper prior to noiseburst, ran behavior with no ephys recording.
'''

exp51 = celldatabase.Experiment(subject,
                               '2017-04-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp51)
exp51.add_site(1380, tetrodes=range(1, 9))
exp51.add_session('17-33-28', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp51.add_session('17-36-15', 'a', 'tc', 'laser_tuning_curve')# ref=29
exp51.add_session('17-44-52', 'a', 'behavior', '2afc')# 150 trials/block


exp52 = celldatabase.Experiment(subject,
                               '2017-04-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp52)

exp52.add_site(1420, tetrodes=range(1, 9))
exp52.add_session('18-25-10', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp52.add_session('18-31-34', 'a', 'tc', 'laser_tuning_curve')# ref=29
exp52.add_session('18-40-39', 'a', 'behavior', '2afc')# 150 trials/block

exp53 = celldatabase.Experiment(subject,
                               '2017-04-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp53)

exp53.add_site(1460, tetrodes=range(1, 9))
exp53.add_session('17-03-31', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp53.add_session('17-07-33', 'a', 'tc', 'laser_tuning_curve')# ref=29
exp53.add_session('17-14-48', 'a', 'behavior', '2afc')# 150 trials/block


exp54 = celldatabase.Experiment(subject,
                               '2017-04-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp54)

exp54.add_site(1500, tetrodes=range(1, 9))
#exp54.add_session('16-06-00', None, 'noiseburst', 'laser_tuning_curve')# ref=29
exp54.add_session('16-10-09', None, 'noiseburst', 'laser_tuning_curve')# ref=11
exp54.add_session('16-13-08', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp54.add_session('16-25-58', 'a', 'behavior', '2afc')# 200 trials/block


exp55 = celldatabase.Experiment(subject,
                               '2017-04-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp55)

exp55.add_site(1500, tetrodes=range(1, 9))
exp55.add_session('14-30-38', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#exp55.add_session('14-41-07', None, 'noiseburst', 'laser_tuning_curve')# ref=18
exp55.add_session('14-44-42', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp55.add_session('14-51-45', 'a', 'behavior', '2afc')# 150 trials/block

exp56 = celldatabase.Experiment(subject,
                               '2017-04-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp56)

exp56.add_site(1540, tetrodes=range(1, 9))
exp56.add_session('13-39-23', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#exp56.add_session('13-43-07', None, 'noiseburst', 'laser_tuning_curve')# ref=3
exp56.add_session('13-46-46', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp56.add_session('13-53-41', 'a', 'behavior', '2afc')# 150 trials/block

exp57 = celldatabase.Experiment(subject,
                               '2017-04-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp57)

exp57.add_site(1580, tetrodes=range(1, 9))
exp57.add_session('18-21-31', None, 'noiseburst', 'laser_tuning_curve')# ref=11
exp57.add_session('18-24-10', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp57.add_session('18-31-07', 'a', 'behavior', '2afc')# 200 trials/block

'''
exp58 = celldatabase.Experiment(subject,
                               '2017-04-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp58)

exp58.add_site(1620, tetrodes=range(1, 9))
#exp58.add_session('16-46-53', None, 'noiseburst', 'laser_tuning_curve')# ref=11 (bad noise disruption)
exp58.add_session('16-50-15', None, 'noiseburst', 'laser_tuning_curve')# ref=11
#exp58.add_session('16-53-03', 'a', 'tc', 'laser_tuning_curve')# ref=11 (bad noise disruption)
exp58.add_session('19-12-25', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp58.add_session('19-18-53', 'a', 'behavior', '2afc')# 200 trials/block, unplugged during behavior at 580 trials
'''

exp59 = celldatabase.Experiment(subject,
                               '2017-04-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp59)

exp59.add_site(1620, tetrodes=range(1, 9))
exp59.add_session('14-47-16', None, 'noiseburst', 'laser_tuning_curve')# ref=11
exp59.add_session('14-50-37', 'a', 'tc', 'laser_tuning_curve')# ref=11
exp59.add_session('14-57-54', 'a', 'behavior', '2afc')# 150 trials/block

exp60 = celldatabase.Experiment(subject,
                               '2017-04-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp60)

exp60.add_site(1660, tetrodes=range(1, 9))
exp60.add_session('14-07-27', None, 'noiseburst', 'laser_tuning_curve')# ref=9
exp60.add_session('14-10-46', 'a', 'tc', 'laser_tuning_curve')# ref=9
exp60.add_session('14-19-13', 'a', 'behavior', '2afc')# 200 trials/block

'''
exp61 = celldatabase.Experiment(subject,
                               '2017-04-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp61)

exp61.add_site(1700, tetrodes=range(1, 9))
exp61.add_session('14-38-00', None, 'noiseburst', 'laser_tuning_curve')# ref=9
exp61.add_session('14-40-21', 'a', 'tc', 'laser_tuning_curve')# ref=9
exp61.add_session('14-47-32', 'a', 'behavior', '2afc')# 200 trials/block

exp62 = celldatabase.Experiment(subject,
                               '2017-04-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp62)

exp62.add_site(1700, tetrodes=range(1, 9))
exp62.add_session('18-28-51', None, 'noiseburst', 'laser_tuning_curve')# ref=9
exp62.add_session('18-32-12', 'a', 'tc', 'laser_tuning_curve')# ref=9
exp62.add_session('18-39-26', 'a', 'behavior', '2afc')# 150 trials/block

exp63 = celldatabase.Experiment(subject,
                               '2017-04-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp63)

exp63.add_site(1700, tetrodes=range(1, 9))
exp63.add_session('18-53-51', None, 'noiseburst', 'laser_tuning_curve')# ref=9
exp63.add_session('18-56-43', 'a', 'tc', 'laser_tuning_curve')# ref=9
exp63.add_session('19-05-02', 'a', 'behavior', '2afc')# 150 trials/block

exp64 = celldatabase.Experiment(subject,
                               '2017-04-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp64)

exp64.add_site(1700, tetrodes=range(1, 9))
exp64.add_session('18-41-45', None, 'noiseburst', 'laser_tuning_curve')# ref=9
exp64.add_session('18-44-34', 'a', 'tc', 'laser_tuning_curve')# ref=9
exp64.add_session('18-52-26', 'a', 'behavior', '2afc')# 150 trials/block
'''

for ind, exp in enumerate(experiments):
    for site in exp.sites:
        site.clusterFolder = 'multisession_exp{}site0'.format(ind)

tetrodeLengthList = [110, 110, 220, 220, 220, 330, 0, 130] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (500, 1660)
