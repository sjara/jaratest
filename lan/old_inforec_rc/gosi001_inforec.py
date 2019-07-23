from jaratoolbox import celldatabase

subject = 'gosi001'
experiments = []

'''
Experiments with less than three full blocks of valid trials commented out
'''

'''
exp0 = celldatabase.Experiment(subject,
                               '2017-04-20',
                               brainarea='rightAC',
                               info='')

experiments.append(exp0)

exp0.add_site(500, tetrodes=range(1, 9))
exp0.add_session('16-14-54', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp0.add_session('16-17-55', 'a', 'tc', 'laser_tuning_curve')
exp0.add_session('16-25-17', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

exp1 = celldatabase.Experiment(subject,
                               '2017-04-21',
                               brainarea='rightAC',
                               info='')

experiments.append(exp1)

exp1.add_site(500, tetrodes=range(1, 9))
exp1.add_session('14-21-06', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp1.add_session('14-23-45', 'a', 'tc', 'laser_tuning_curve')
exp1.add_session('14-30-49', 'a', 'behavior', '2afc')#150 trials/block


exp2 = celldatabase.Experiment(subject,
                               '2017-04-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp2)

exp2.add_site(540, tetrodes=range(1, 9))
exp2.add_session('17-50-04', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp2.add_session('17-56-30', 'a', 'tc', 'laser_tuning_curve')
exp2.add_session('18-03-21', 'a', 'behavior', '2afc')#150 trials/block

'''
exp3 = celldatabase.Experiment(subject,
                               '2017-04-23',
                               brainarea='rightAC',
                               info='')

experiments.append(exp3)

exp3.add_site(580, tetrodes=range(1, 9))
exp3.add_session('16-20-42', None, 'noiseburst', 'laser_tuning_curve')#ref=5, rig 2
exp3.add_session('16-23-14', 'a', 'tc', 'laser_tuning_curve')#rig 2, speaker malfunction, commented out because no behavior was recorded as a result of the speaker malfunction
'''

exp4 = celldatabase.Experiment(subject,
                               '2017-04-24',
                               brainarea='rightAC',
                               info='')

experiments.append(exp4)

exp4.add_site(580, tetrodes=range(1, 9))
exp4.add_session('12-18-57', None, 'noiseburst', 'laser_tuning_curve')#ref=5
#exp4.add_session('12-23-13', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp4.add_session('12-26-54', 'a', 'tc', 'laser_tuning_curve')#ref=5
exp4.add_session('12-34-03', 'a', 'behavior', '2afc')#150 trials/block

'''
exp5 = celldatabase.Experiment(subject,
                               '2017-04-25',
                               brainarea='rightAC',
                               info='')

experiments.append(exp5)

exp5.add_site(620, tetrodes=range(1, 9))
exp5.add_session('11-50-46', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp5.add_session('11-54-29', 'a', 'tc', 'laser_tuning_curve')
exp5.add_session('12-01-53', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''

exp6 = celldatabase.Experiment(subject,
                               '2017-04-26',
                               brainarea='rightAC',
                               info='')

experiments.append(exp6)

exp6.add_site(620, tetrodes=range(1, 9))
exp6.add_session('14-21-16', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp6.add_session('14-24-15', 'a', 'tc', 'laser_tuning_curve')
exp6.add_session('14-30-54', 'a', 'behavior', '2afc')#150 trials/block


exp7 = celldatabase.Experiment(subject,
                               '2017-04-27',
                               brainarea='rightAC',
                               info='')

experiments.append(exp7)

exp7.add_site(660, tetrodes=range(1, 9))
exp7.add_session('13-40-13', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp7.add_session('13-43-20', 'a', 'tc', 'laser_tuning_curve')
exp7.add_session('13-50-28', 'a', 'behavior', '2afc')#150 trials/block


exp8 = celldatabase.Experiment(subject,
                               '2017-04-28',
                               brainarea='rightAC',
                               info='')

experiments.append(exp8)

exp8.add_site(700, tetrodes=range(1, 9))
exp8.add_session('14-41-34', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp8.add_session('14-44-53', 'a', 'tc', 'laser_tuning_curve')
exp8.add_session('14-51-37', 'a', 'behavior', '2afc')#200 trials/block


exp9 = celldatabase.Experiment(subject,
                               '2017-04-29',
                               brainarea='rightAC',
                               info='')

experiments.append(exp9)

exp9.add_site(740, tetrodes=range(1, 9))
exp9.add_session('16-05-27', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp9.add_session('16-08-00', 'a', 'tc', 'laser_tuning_curve')
exp9.add_session('16-14-32', 'a', 'behavior', '2afc')#200 trials/block


exp10 = celldatabase.Experiment(subject,
                               '2017-04-30',
                               brainarea='rightAC',
                               info='')

experiments.append(exp10)

exp10.add_site(780, tetrodes=range(1, 9))
exp10.add_session('17-57-51', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp10.add_session('18-00-54', 'a', 'tc', 'laser_tuning_curve')
exp10.add_session('18-07-50', 'a', 'behavior', '2afc')#200 trials/block


exp11 = celldatabase.Experiment(subject,
                               '2017-05-01',
                               brainarea='rightAC',
                               info='')

experiments.append(exp11)

exp11.add_site(820, tetrodes=range(1, 9))
exp11.add_session('12-06-06', None, 'noiseburst', 'laser_tuning_curve')#ref=20
exp11.add_session('12-08-58', 'a', 'tc', 'laser_tuning_curve')#ref=20
exp11.add_session('12-20-04', 'a', 'behavior', '2afc')#150 trials/block

'''
exp12 = celldatabase.Experiment(subject,
                               '2017-05-02',
                               brainarea='rightAC',
                               info='')

experiments.append(exp12)

exp12.add_site(900, tetrodes=range(1, 9))
exp12.add_session('11-50-04', None, 'noiseburst', 'laser_tuning_curve')#ref=20
exp12.add_session('11-53-43', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp12.add_session('11-57-16', 'a', 'tc', 'laser_tuning_curve')#ref=13
exp12.add_session('12-04-25', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''

exp13 = celldatabase.Experiment(subject,
                               '2017-05-03',
                               brainarea='rightAC',
                               info='')

experiments.append(exp13)

exp13.add_site(900, tetrodes=range(1, 9))
exp13.add_session('14-50-11', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp13.add_session('14-52-36', 'a', 'tc', 'laser_tuning_curve')
exp13.add_session('14-59-23', 'a', 'behavior', '2afc')#200 trials/block,


exp14 = celldatabase.Experiment(subject,
                               '2017-05-04',
                               brainarea='rightAC',
                               info='')

experiments.append(exp14)

exp14.add_site(940, tetrodes=range(1, 9))
exp14.add_session('12-21-30', None, 'noiseburst', 'laser_tuning_curve')#ref=13
exp14.add_session('12-24-07', 'a', 'tc', 'laser_tuning_curve')
exp14.add_session('12-30-35', 'a', 'behavior', '2afc')#150 trials/block,


exp15 = celldatabase.Experiment(subject,
                               '2017-05-05',
                               brainarea='rightAC',
                               info='')

experiments.append(exp15)

exp15.add_site(980, tetrodes=range(1, 9))
exp15.add_session('14-28-44', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp15.add_session('14-31-19', 'a', 'tc', 'laser_tuning_curve')#ref=29
exp15.add_session('14-37-59', 'a', 'behavior', '2afc')#200 trials/block,


exp16 = celldatabase.Experiment(subject,
                               '2017-05-06',
                               brainarea='rightAC',
                               info='')

experiments.append(exp16)

exp16.add_site(1020, tetrodes=range(1, 9))
exp16.add_session('15-31-07', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp16.add_session('15-33-20', 'a', 'tc', 'laser_tuning_curve')
exp16.add_session('15-40-06', 'a', 'behavior', '2afc')#200 trials/block,


exp17 = celldatabase.Experiment(subject,
                               '2017-05-07',
                               brainarea='rightAC',
                               info='')

experiments.append(exp17)

exp17.add_site(1060, tetrodes=range(1, 9))
exp17.add_session('12-49-20', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp17.add_session('12-51-42', 'a', 'tc', 'laser_tuning_curve')
exp17.add_session('12-58-18', 'a', 'behavior', '2afc')#150 trials/block,


exp18 = celldatabase.Experiment(subject,
                               '2017-05-08',
                               brainarea='rightAC',
                               info='')

experiments.append(exp18)

exp18.add_site(1100, tetrodes=range(1, 9))
exp18.add_session('12-19-31', None, 'noiseburst', 'laser_tuning_curve')#ref=29
#exp18.add_session('12-22-04', 'a', 'tc', 'laser_tuning_curve')#ref=29, tuning on all TT
exp18.add_session('12-30-10', 'b', 'tc', 'laser_tuning_curve')#ref=26
exp18.add_session('12-37-13', 'a', 'behavior', '2afc')#200 trials/block,

'''
exp19 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='rightAC',
                               info='')

experiments.append(exp19)

exp19.add_site(1140, tetrodes=range(1, 9))
exp19.add_session('12-09-09', None, 'noiseburst', 'laser_tuning_curve')#ref=26
exp19.add_session('12-11-29', 'a', 'tc', 'laser_tuning_curve')#ref=26
exp19.add_session('12-18-57', 'a', 'behavior', '2afc')#200 trials/block, commented out becuase behavior data didn't save
'''


exp20 = celldatabase.Experiment(subject,
                               '2017-05-10',
                               brainarea='rightAC',
                               info='')

experiments.append(exp20)

exp20.add_site(1180, tetrodes=range(1, 9))
exp20.add_session('14-43-18', None, 'noiseburst', 'laser_tuning_curve')#ref=26
exp20.add_session('14-49-34', 'a', 'tc', 'laser_tuning_curve')#ref=26
exp20.add_session('14-56-19', 'a', 'behavior', '2afc')#200 trials/block, 


exp21 = celldatabase.Experiment(subject,
                               '2017-05-11',
                               brainarea='rightAC',
                               info='')

experiments.append(exp21)

exp21.add_site(1220, tetrodes=range(1, 9))
exp21.add_session('14-17-12', None, 'noiseburst', 'laser_tuning_curve')#ref=26
exp21.add_session('14-20-49', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp21.add_session('14-26-25', 'a', 'tc', 'laser_tuning_curve')#ref=5
exp21.add_session('14-32-58', 'a', 'behavior', '2afc')#200 trials/block, 


exp22 = celldatabase.Experiment(subject,
                               '2017-05-12',
                               brainarea='rightAC',
                               info='')

experiments.append(exp22)

exp22.add_site(1260, tetrodes=range(1, 9))
exp22.add_session('13-39-38', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp22.add_session('13-42-20', 'a', 'tc', 'laser_tuning_curve')
exp22.add_session('13-48-47', 'a', 'behavior', '2afc')#200 trials/block, 


exp23 = celldatabase.Experiment(subject,
                               '2017-05-13',
                               brainarea='rightAC',
                               info='')

experiments.append(exp23)

exp23.add_site(1300, tetrodes=range(1, 9))
exp23.add_session('16-15-23', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp23.add_session('16-17-57', 'a', 'tc', 'laser_tuning_curve')
exp23.add_session('16-24-43', 'a', 'behavior', '2afc')#200 trials/block, 


exp24 = celldatabase.Experiment(subject,
                               '2017-05-14',
                               brainarea='rightAC',
                               info='')

experiments.append(exp24)

exp24.add_site(1340, tetrodes=range(1, 9))
exp24.add_session('15-13-36', None, 'noiseburst', 'laser_tuning_curve')#ref=5
#exp24.add_session('15-16-58', None, 'noiseburst', 'laser_tuning_curve')#ref=29
exp24.add_session('15-20-41', 'a', 'tc', 'laser_tuning_curve')#ref=5
exp24.add_session('15-27-21', 'a', 'behavior', '2afc')#200 trials/block, 


exp25 = celldatabase.Experiment(subject,
                               '2017-05-15',
                               brainarea='rightAC',
                               info='')

experiments.append(exp25)

exp25.add_site(1380, tetrodes=range(1, 9))
exp25.add_session('12-18-50', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp25.add_session('12-21-18', 'a', 'tc', 'laser_tuning_curve')
exp25.add_session('12-28-04', 'a', 'behavior', '2afc')#150 trials/block, 

'''
exp26 = celldatabase.Experiment(subject,
                               '2017-05-16',
                               brainarea='rightAC',
                               info='')

experiments.append(exp26)

exp26.add_site(1420, tetrodes=range(1, 9))
exp26.add_session('11-46-28', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp26.add_session('11-49-05', 'a', 'tc', 'laser_tuning_curve')
exp26.add_session('11-55-32', 'a', 'behavior', '2afc')#200 trials/block, less than three full blocks of valid trials
'''


exp27 = celldatabase.Experiment(subject,
                               '2017-05-17',
                               brainarea='rightAC',
                               info='')

experiments.append(exp27)

exp27.add_site(1420, tetrodes=range(1, 9))
exp27.add_session('14-09-18', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp27.add_session('14-11-44', 'a', 'tc', 'laser_tuning_curve')
exp27.add_session('14-19-43', 'a', 'behavior', '2afc')#200 trials/block, 


exp28 = celldatabase.Experiment(subject,
                               '2017-05-18',
                               brainarea='rightAC',
                               info='')

experiments.append(exp28)

exp28.add_site(1460, tetrodes=range(1, 9))
exp28.add_session('14-41-07', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp28.add_session('14-43-58', 'a', 'tc', 'laser_tuning_curve')
exp28.add_session('14-50-48', 'a', 'behavior', '2afc')#200 trials/block, 


exp29 = celldatabase.Experiment(subject,
                               '2017-05-19',
                               brainarea='rightAC',
                               info='')

experiments.append(exp29)

exp29.add_site(1500, tetrodes=range(1, 9))
exp29.add_session('17-53-49', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp29.add_session('17-56-34', 'a', 'tc', 'laser_tuning_curve')
exp29.add_session('18-03-13', 'a', 'behavior', '2afc')#200 trials/block, 


'''
exp30 = celldatabase.Experiment(subject,
                               '2017-05-22',
                               brainarea='rightAC',
                               info='')

experiments.append(exp30)

exp30.add_site(1540, tetrodes=range(1, 9))
#exp30.add_session('10-21-40', None, 'noiseburst', 'laser_tuning_curve')#ref=5
exp30.add_session('10-25-20', None, 'noiseburst', 'laser_tuning_curve')#ref=9
exp30.add_session('10-34-07', 'a', 'tc', 'laser_tuning_curve')#ref=9
exp30.add_session('10-40-49', 'a', 'behavior', '2afc')#150 trials/block, less than three full blocks of valid trials
'''


for ind, exp in enumerate(experiments):
    for site in exp.sites:
        site.clusterFolder = 'multisession_exp{}site0'.format(ind)

tetrodeLengthList = [0, 190, 40, 230, 140, 300, 300, 210] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (500, 1500)
