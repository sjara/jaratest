from jaratoolbox import celldatabase

subject = 'pinp015'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2017-01-26',
                               brainarea='rightAC',
                               info=['medialDiI'])
experiments.append(exp0)

exp0.add_site(894, tetrodes=range(1, 9))
exp0.add_session('13-28-05', None, 'noiseburst', 'am_tuning_curve').comment('some response on TT2')
exp0.add_session('13-30-32', None, 'laserpulse', 'am_tuning_curve') #Shor latency response on TT2
#For real
exp0.add_session('13-34-14', 'a', 'rlf', 'am_tuning_curve')
exp0.add_session('13-39-55', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('13-45-56', 'b', 'tc', 'am_tuning_curve')
exp0.add_session('14-04-02', 'c', 'am', 'am_tuning_curve')
exp0.add_session('14-20-14', None, 'lasertrain', 'am_tuning_curve')


exp0.add_site(957, tetrodes=[1, 2, 3, 4, 7, 8])
exp0.add_session('14-27-09', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-29-53', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-34-47', 'd', 'rlf', 'am_tuning_curve')
exp0.add_session('14-41-33', 'e', 'tc', 'am_tuning_curve')
exp0.add_session('14-58-29', 'f', 'am', 'am_tuning_curve')
exp0.add_session('15-14-43', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-18-52', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(1060, tetrodes=range(1, 9))
exp0.add_session('15-28-30', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-30-28', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-34-53', 'g', 'rlf', 'am_tuning_curve')
exp0.add_session('15-40-05', 'h', 'tc', 'am_tuning_curve')
exp0.add_session('15-57-52', 'i', 'am', 'am_tuning_curve')
exp0.add_session('16-15-07', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(1146, tetrodes=[1, 2, 4, 6, 7, 8])
exp0.add_session('16-20-45', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('16-23-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('16-27-29', 'j', 'rlf', 'am_tuning_curve')
exp0.add_session('16-33-05', 'k', 'tc', 'am_tuning_curve')
exp0.add_session('16-49-40', 'l', 'am', 'am_tuning_curve') #only 30 trials each
exp0.add_session('16-59-01',None, 'lasertrain', 'am_tuning_curve')
exp0.maxDepth = 1146

exp1 = celldatabase.Experiment(subject,
                               '2017-01-27',
                               brainarea='rightThal',
                               info=['medialDiI'])
experiments.append(exp1)

#I have to remove the electrodes
# exp1.add_site(3821, tetrodes=range(1, 9))
# exp1.add_session('13-04-07', None, 'noiseburst', 'am_tuning_curve')
# exp1.add_session('13-00-58', None, 'laserpulse', 'am_tuning_curve') #There are no laser responses here
exp1.maxDepth = 3821


exp2 = celldatabase.Experiment(subject,
                               '2017-02-02',
                               brainarea='rightAC',
                               info=['DiD'])
experiments.append(exp2)

#I have to remove the electrodes
exp2.add_site(975, tetrodes=range(1, 9))
exp2.add_session('11-25-47', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('11-28-13', None, 'laserpulse', 'am_tuning_curve') #Had to turn the laser down mid session
exp2.add_session('11-30-16', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-35-18', 'a', 'rlf', 'am_tuning_curve')
exp2.add_session('11-38-52', 'b', 'tc', 'am_tuning_curve')
exp2.add_session('11-56-10', 'c', 'am', 'am_tuning_curve')
exp2.add_session('12-12-03', None, 'laserpulse', 'am_tuning_curve') #Better laser pulse session, 70 trials
exp2.add_session('12-13-43', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-18-41', 'd', 'amfast', 'am_tuning_curve') #64-512Hz, 4 freqs

exp2.add_site(1087, tetrodes=range(1, 9))
exp2.add_session('12-48-20', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-52-08', 'e', 'rlf', 'am_tuning_curve')
exp2.add_session('12-57-10', 'f', 'tc', 'am_tuning_curve')
exp2.add_session('13-14-01', 'g', 'am', 'am_tuning_curve')
exp2.add_session('13-30-09', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-34-00', None, 'laserpulse', 'am_tuning_curve')

exp2.add_site(1175, tetrodes=range(1, 9))
exp2.add_session('13-42-34', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-46-31', 'h', 'rlf', 'am_tuning_curve')
exp2.add_session('13-52-25', 'i', 'tc', 'am_tuning_curve')
exp2.add_session('14-09-58', 'j', 'am', 'am_tuning_curve')
exp2.add_session('14-26-52', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('14-30-40', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('14-34-32', 'k', 'amfast', 'am_tuning_curve') # 64-512, 4 freqs
exp2.add_session('14-42-42', None, 'noiseburst', 'am_tuning_curve')

exp2.add_site(1275, tetrodes=range(1, 9))
exp2.add_session('15-00-54', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-05-34', None, 'lasertrain_2.8', 'am_tuning_curve') #Check the clusters from this session later, laser artifacts??
exp2.add_session('15-07-57', 'l', 'rlf', 'am_tuning_curve')
exp2.add_session('15-13-12', 'm', 'tc', 'am_tuning_curve')
exp2.add_session('15-34-57', 'n', 'amfast', 'am_tuning_curve')
exp2.add_session('15-50-50', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('15-54-49', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('15-57-48', None, 'noiseburst', 'am_tuning_curve')

exp2.add_site(1378, tetrodes=range(1, 9))
exp2.add_session('16-03-42', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-06-36', None, 'lasertrain', 'am_tuning_curve') #LFPs are going the other way???
exp2.add_session('16-10-09', 'o', 'rlf', 'am_tuning_curve')
exp2.add_session('16-15-16', 'p', 'tc', 'am_tuning_curve')
exp2.add_session('16-33-50', 'q', 'am', 'am_tuning_curve')
exp2.add_session('16-50-01', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-54-10', None, 'laserpulse', 'am_tuning_curve')

# exp2.add_site(1503, tetrodes=range(1, 9))
# exp2.add_session('17-02-17', None, 'noiseburst', 'am_tuning_curve')
# exp2.add_session('17-05-42', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('17-09-16', 'r', 'rlf', 'am_tuning_curve') #not much going on, I am removing the trodes
exp2.maxDepth = 1503

exp3 = celldatabase.Experiment(subject,
                               '2017-02-08',
                               brainarea='rightAC',
                               info=['lateralDiI'])
experiments.append(exp3)

# exp3.add_site(1815, tetrodes=range(1, 9))
# # exp3.add_session('11-23-08', None, 'noiseburst', 'am_tuning_curve') NEW OPEN EPHYS FILE FORMAT
# exp3.add_session('12-08-45', None, 'noiseburst', 'am_tuning_curve') #There have been sites with great spikes, but no sound responses. I am removing the electrodes
exp3.maxDepth = 1815

exp4 = celldatabase.Experiment(subject,
                               '2017-02-15',
                               brainarea='rightThal',
                               info=['medialDiD'])
experiments.append(exp4)

# exp4.add_site(1506, tetrodes=range(1, 9))
# exp4.add_session('12-09-25', None, 'noiseburst', 'am_tuning_curve')#Noise response
# exp4.add_session('12-12-26', None, 'laserpulse', 'am_tuning_curve')#No laser response, laser at 3
# exp4.add_session('12-14-50', None, 'laserpulse2', 'am_tuning_curve')#No laser response, laser at 5
# #Use the above sessions to show no laser artifact in the brain??

# exp4.add_site(1912, tetrodes=range(1, 9))
# exp4.add_session('12-20-12', None, 'noiseburst', 'am_tuning_curve') #Nothing

# exp4.add_site(2040, tetrodes=range(1, 9))
# exp4.add_session('12-24-16', None, 'noiseburst', 'am_tuning_curve') #something maybe??
# exp4.add_session('12-26-55', None, 'laserpulse', 'am_tuning_curve') #Nothing

exp4.add_site(2902, tetrodes=range(1, 9))
exp4.add_session('12-49-10', None, 'noiseburst', 'am_tuning_curve') #strong sound response
exp4.add_session('12-51-41', None, 'laserpulse', 'am_tuning_curve') #strong laser response
exp4.add_session('12-53-55', None, 'lasertrain', 'am_tuning_curve')
# exp4.add_session('12-58-26', 'a', 'tc', 'am_tuning_curve')
exp4.add_session('13-21-56', 'b', 'am', 'am_tuning_curve')
exp4.add_session('13-40-07', None, 'lasertrain2', 'am_tuning_curve')
exp4.add_session('13-49-13', 'c', 'tc', 'am_tuning_curve') #Better, larger tuning curve
exp4.add_session('14-26-43', None, 'lasertrain3', 'am_tuning_curve')

exp4.add_site(3009, tetrodes=range(1, 9))
exp4.add_session('14-31-49', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('14-36-06', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('14-39-18', 'd', 'tc', 'am_tuning_curve') #Better, larger tuning curve
exp4.add_session('15-13-17', None, 'lasertrain2', 'am_tuning_curve')
exp4.add_session('15-16-49', 'e', 'am', 'am_tuning_curve')

exp4.add_site(3110, tetrodes=range(1, 9))
exp4.add_session('15-44-26', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('15-48-00', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('15-51-47', 'f', 'tc', 'am_tuning_curve') #Better, larger tuning curve
exp4.add_session('16-26-20', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('16-31-24', 'g', 'am', 'am_tuning_curve')
exp4.add_session('16-47-10', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('16-50-58', None, 'laserpulse', 'am_tuning_curve')
exp4.maxDepth = 3110
