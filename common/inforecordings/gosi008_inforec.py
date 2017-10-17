from jaratoolbox import celldatabase

subject = 'gosi008'
experiments = []

'''
Experiments with <550 valid trials commented out
'''

'''
exp0 = celldatabase.Experiment(subject,
                               '2017-02-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(500, tetrodes=range(1, 9))
#exp0.add_session('16-57-56', None, 'noiseburst', 'laser_tuning_curve')
#exp0.add_session('17-03-59', None, 'noiseburst', 'laser_tuning_curve')
#exp0.add_session('17-36-07', None, 'noiseburst', 'laser_tuning_curve')
#exp0.add_session('17-23-40', None, 'noiseburst', 'laser_tuning_curve')
#exp0.add_session('17-28-05', None, 'noiseburst', 'laser_tuning_curve')
#exp0.add_session('17-31-21', None, 'noiseburst', 'laser_tuning_curve')
exp0.add_session('17-34-44', None, 'noiseburst', 'laser_tuning_curve')
exp0.add_session('17-37-46', 'a', 'tc', 'laser_tuning_curve')

exp1 = celldatabase.Experiment(subject,
                               '2017-02-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(500, tetrodes=range(1, 9))
#exp1.add_session('17-15-26', None, 'noiseburst', 'laser_tuning_curve')
exp1.add_session('17-26-04', None, 'noiseburst', 'laser_tuning_curve')
exp1.add_session('17-29-23', 'a', 'tc', 'laser_tuning_curve')

exp2 = celldatabase.Experiment(subject,
                               '2017-02-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(540, tetrodes=range(1, 9))
#exp2.add_session('15-11-17', None, 'noiseburst', 'laser_tuning_curve')
#exp2.add_session('15-16-08', 'a', 'tc', 'laser_tuning_curve')
#exp2.add_session('15-37-39', None, 'noiseburst', 'laser_tuning_curve')
exp2.add_session('15-48-58',  None, 'noiseburst', 'laser_tuning_curve')
exp2.add_session('16-00-55', 'b', 'tc', 'laser_tuning_curve')
exp2.add_session('16-07-26', 'a', 'behavior', '2afc')
'''

exp3 = celldatabase.Experiment(subject,
                               '2017-02-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(540, tetrodes=range(1, 9))
exp3.add_session('15-04-53',  None, 'noiseburst', 'laser_tuning_curve')
#exp3.add_session('15-08-06', 'a', 'tc', 'laser_tuning_curve')
exp3.add_session('15-17-49', 'b', 'tc', 'laser_tuning_curve')
exp3.add_session('15-23-03', 'a', 'behavior', '2afc')

exp4 = celldatabase.Experiment(subject,
                               '2017-02-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(580, tetrodes=range(1, 9))
#exp4.add_session('16-47-57',  None, 'noiseburst', 'laser_tuning_curve')
#exp4.add_session('16-50-36', 'a', 'tc', 'laser_tuning_curve')
#exp4.add_session('16-55-34', 'a', 'behavior', '2afc')
exp4.add_session('17-45-02',  None, 'noiseburst', 'laser_tuning_curve')
exp4.add_session('17-47-48', 'a', 'tc', 'laser_tuning_curve')
exp4.add_session('17-54-27', 'a', 'behavior', '2afc')

exp5 = celldatabase.Experiment(subject,
                               '2017-02-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(580, tetrodes=range(1, 9))
exp5.add_session('17-16-06',  None, 'noiseburst', 'laser_tuning_curve')
exp5.add_session('17-18-45', 'a', 'tc', 'laser_tuning_curve')
exp5.add_session('17-31-04', 'a', 'behavior', '2afc')

'''
exp6 = celldatabase.Experiment(subject,
                               '2017-02-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(620, tetrodes=range(1, 9))
exp6.add_session('16-30-25',  None, 'noiseburst', 'laser_tuning_curve')
exp6.add_session('16-33-04', 'a', 'tc', 'laser_tuning_curve')
exp6.add_session('16-37-49', 'a', 'behavior', '2afc')
'''

exp7 = celldatabase.Experiment(subject,
                               '2017-03-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(620, tetrodes=range(1, 9))
exp7.add_session('15-54-23',  None, 'noiseburst', 'laser_tuning_curve')
exp7.add_session('15-56-54', 'a', 'tc', 'laser_tuning_curve')
exp7.add_session('16-01-31', 'a', 'behavior', '2afc')

'''
exp8 = celldatabase.Experiment(subject,
                               '2017-03-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(660, tetrodes=range(1, 9))
exp8.add_session('14-17-03',  None, 'noiseburst', 'laser_tuning_curve')
exp8.add_session('14-20-02', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('14-26-03', 'a', 'behavior', '2afc')
'''

exp9 = celldatabase.Experiment(subject,
                               '2017-03-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(660, tetrodes=range(1, 9))
exp9.add_session('16-30-04',  None, 'noiseburst', 'laser_tuning_curve')
exp9.add_session('16-32-55', 'a', 'tc', 'laser_tuning_curve')
exp9.add_session('16-39-44', 'a', 'behavior', '2afc')

exp10 = celldatabase.Experiment(subject,
                               '2017-03-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(700, tetrodes=range(1, 9))
exp10.add_session('17-15-33',  None, 'noiseburst', 'laser_tuning_curve')
exp10.add_session('17-20-19', 'a', 'tc', 'laser_tuning_curve')
exp10.add_session('17-27-42', 'a', 'behavior', '2afc')

'''
exp11 = celldatabase.Experiment(subject,
                               '2017-03-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(740, tetrodes=range(1, 9))
exp11.add_session('14-56-21',  None, 'noiseburst', 'laser_tuning_curve')
exp11.add_session('15-00-55', 'a', 'tc', 'laser_tuning_curve')
exp11.add_session('15-14-21', 'a', 'behavior', '2afc')

exp12 = celldatabase.Experiment(subject,
                               '2017-03-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(740, tetrodes=range(1, 9))
#exp12.add_session('16-17-36',  None, 'noiseburst', 'laser_tuning_curve')#ref 6
#exp12.add_session('16-22-44',  None, 'noiseburst', 'laser_tuning_curve')#ref 14
exp12.add_session('16-28-50',  None, 'noiseburst', 'laser_tuning_curve')#ref 30
exp12.add_session('16-33-23', 'a', 'tc', 'laser_tuning_curve')
exp12.add_session('16-46-55', 'a', 'behavior', '2afc')
'''

exp13 = celldatabase.Experiment(subject,
                               '2017-03-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(740, tetrodes=range(1, 9))
exp13.add_session('16-19-22',  None, 'noiseburst', 'laser_tuning_curve')
exp13.add_session('16-21-55', 'a', 'tc', 'laser_tuning_curve')
exp13.add_session('16-28-27', 'a', 'behavior', '2afc')

'''
exp14 = celldatabase.Experiment(subject,
                               '2017-03-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(780, tetrodes=range(1, 9))
exp14.add_session('15-36-09',  None, 'noiseburst', 'laser_tuning_curve')
exp14.add_session('15-39-19', 'a', 'tc', 'laser_tuning_curve')
exp14.add_session('15-47-47', 'a', 'behavior', '2afc')
'''

exp15 = celldatabase.Experiment(subject,
                               '2017-03-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(780, tetrodes=range(1, 9))
exp15.add_session('14-52-38',  None, 'noiseburst', 'laser_tuning_curve')
exp15.add_session('14-55-42', 'a', 'tc', 'laser_tuning_curve')
exp15.add_session('15-03-26', 'a', 'behavior', '2afc')

exp16 = celldatabase.Experiment(subject,
                               '2017-03-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(820, tetrodes=range(1, 9))
exp16.add_session('17-56-52',  None, 'noiseburst', 'laser_tuning_curve')
exp16.add_session('18-00-34', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('18-07-43', 'a', 'behavior', '2afc')

'''
exp17 = celldatabase.Experiment(subject,
                               '2017-03-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(860, tetrodes=range(1, 9))
exp17.add_session('18-05-03',  None, 'noiseburst', 'laser_tuning_curve')
exp17.add_session('18-07-28', 'a', 'tc', 'laser_tuning_curve')
exp17.add_session('18-14-11', 'a', 'behavior', '2afc')

exp18 = celldatabase.Experiment(subject,
                               '2017-03-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(860, tetrodes=range(1, 9))
exp18.add_session('13-43-30',  None, 'noiseburst', 'laser_tuning_curve')
exp18.add_session('13-56-09', 'a', 'tc', 'laser_tuning_curve')
exp18.add_session('14-03-54', 'a', 'behavior', '2afc')

exp19 = celldatabase.Experiment(subject,
                               '2017-03-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(860, tetrodes=range(1, 9))
#exp19.add_session('16-40-17',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
#exp19.add_session('16-44-50',  None, 'noiseburst', 'laser_tuning_curve') #ref=26
exp19.add_session('16-48-12',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp19.add_session('16-51-28', 'a', 'tc', 'laser_tuning_curve')
exp19.add_session('16-58-25', 'a', 'behavior', '2afc')
'''

exp20 = celldatabase.Experiment(subject,
                               '2017-03-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(860, tetrodes=range(1, 9))
exp20.add_session('17-24-46',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp20.add_session('17-27-54', 'a', 'tc', 'laser_tuning_curve')
exp20.add_session('17-34-28', 'a', 'behavior', '2afc')

exp21 = celldatabase.Experiment(subject,
                               '2017-03-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(900, tetrodes=range(1, 9))
#exp21.add_session('15-24-29',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp21.add_session('15-28-22',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
exp21.add_session('15-31-59', 'a', 'tc', 'laser_tuning_curve')
exp21.add_session('15-41-10', 'a', 'behavior', '2afc')

exp22 = celldatabase.Experiment(subject,
                               '2017-03-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(940, tetrodes=range(1, 9))
exp22.add_session('14-53-56',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
#exp22.add_session('14-57-55',  None, 'noiseburst', 'laser_tuning_curve') #ref=12
exp22.add_session('15-56-33', 'a', 'tc', 'laser_tuning_curve') #ref=5
exp22.add_session('15-06-26', 'a', 'behavior', '2afc')

exp23 = celldatabase.Experiment(subject,
                               '2017-03-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(940, tetrodes=range(1, 9))
exp23.add_session('17-14-26',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp23.add_session('17-17-56', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('17-24-35', 'a', 'behavior', '2afc')

exp24 = celldatabase.Experiment(subject,
                               '2017-03-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(980, tetrodes=range(1, 9))
exp24.add_session('16-19-03',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp24.add_session('16-23-56', 'a', 'tc', 'laser_tuning_curve')
exp24.add_session('16-32-39', 'a', 'behavior', '2afc')

exp25 = celldatabase.Experiment(subject,
                               '2017-03-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(1020, tetrodes=range(1, 9))
exp25.add_session('15-41-28',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp25.add_session('15-43-55', 'a', 'tc', 'laser_tuning_curve')
exp25.add_session('15-53-19', 'a', 'behavior', '2afc')

exp26 = celldatabase.Experiment(subject,
                               '2017-03-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(1060, tetrodes=range(1, 9))
exp26.add_session('16-22-15',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp26.add_session('16-25-08', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('16-33-21', 'a', 'behavior', '2afc')

exp27 = celldatabase.Experiment(subject,
                               '2017-03-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(1100, tetrodes=range(1, 9))
exp27.add_session('16-52-14',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp27.add_session('16-54-40', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('17-01-32', 'a', 'behavior', '2afc')

exp28 = celldatabase.Experiment(subject,
                               '2017-03-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(1140, tetrodes=range(1, 9))
exp28.add_session('11-54-24',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp28.add_session('11-56-42', 'a', 'tc', 'laser_tuning_curve')
exp28.add_session('12-03-04', 'a', 'behavior', '2afc')

exp29 = celldatabase.Experiment(subject,
                               '2017-03-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(1140, tetrodes=range(1, 9))
exp29.add_session('16-57-30',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp29.add_session('16-59-57', 'a', 'tc', 'laser_tuning_curve')
exp29.add_session('17-10-43', 'a', 'behavior', '2afc')

exp30 = celldatabase.Experiment(subject,
                               '2017-03-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(1180, tetrodes=range(1, 9))
exp30.add_session('16-00-46',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp30.add_session('16-03-58', 'a', 'tc', 'laser_tuning_curve')
exp30.add_session('16-12-58', 'a', 'behavior', '2afc')

exp31 = celldatabase.Experiment(subject,
                               '2017-03-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp31)

exp31.add_site(1220, tetrodes=range(1, 9))
exp31.add_session('10-53-20',  None, 'noiseburst', 'laser_tuning_curve') #ref=5
exp31.add_session('10-58-49',  None, 'noiseburst', 'laser_tuning_curve') #ref=17
exp31.add_session('11-02-42', 'a', 'tc', 'laser_tuning_curve')#ref=17
exp31.add_session('11-10-50', 'a', 'behavior', '2afc')#ref=17

exp32 = celldatabase.Experiment(subject,
                               '2017-03-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp32)

exp32.add_site(1260, tetrodes=range(1, 9))
exp32.add_session('11-40-13',  None, 'noiseburst', 'laser_tuning_curve') #ref=17
exp32.add_session('11-43-45', 'a', 'tc', 'laser_tuning_curve')
exp32.add_session('11-52-12', 'a', 'behavior', '2afc')


exp33 = celldatabase.Experiment(subject,
                               '2017-04-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp33)

exp33.add_site(1260, tetrodes=range(1, 9))
exp33.add_session('18-11-55',  None, 'noiseburst', 'laser_tuning_curve') #ref=2
exp33.add_session('18-17-03', 'a', 'tc', 'laser_tuning_curve')
exp33.add_session('18-25-58', 'a', 'behavior', '2afc')

'''
exp34 = celldatabase.Experiment(subject,
                               '2017-04-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp34)

exp34.add_site(1260, tetrodes=range(1, 9))
exp34.add_session('14-18-47',  None, 'noiseburst', 'laser_tuning_curve') #ref=19. Moved deeper after noiseburst, ran behavior with no ephys recording.
'''

exp35 = celldatabase.Experiment(subject,
                               '2017-04-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp35)

exp35.add_site(1300, tetrodes=range(1, 9))
exp35.add_session('18-53-01',  None, 'noiseburst', 'laser_tuning_curve') #ref=none
exp35.add_session('19-04-38',  None, 'noiseburst', 'laser_tuning_curve') #ref=10
exp35.add_session('19-08-45', 'a', 'tc', 'laser_tuning_curve') #ref=10
exp35.add_session('19-16-52', 'a', 'behavior', '2afc') #ref=10

'''
exp36 = celldatabase.Experiment(subject,
                               '2017-04-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp36)

exp36.add_site(1300, tetrodes=range(1, 9))
exp36.add_session('14-27-31',  None, 'noiseburst', 'laser_tuning_curve') #ref=6 86 trials. 
exp36.add_session('14-40-14', 'a', 'tc', 'laser_tuning_curve') #ref=6  Moved deeper after noiseburst, ran behavior with no ephys recording.
'''

#For gosi008 implant tetrode 6 was bad, use an arbitrary number of length just to exclude cells form this tetrode (should have not included it in the exps) 
tetrodeLengthList = [0, 170, 120, 60, 110, 1000, 120, 110] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (540, 1260)
