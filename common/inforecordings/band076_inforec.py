from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band076'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-10-03', 'right_AC', info=['lateralDiD','TT8ant','soundleft'])
experiments.append(exp0)


    # noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(360) -> SNRs (300) -> noiseAmps (150)

exp0.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('14-33-28', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1100, tetrodes=[1,2,4,6])
exp0.add_session('14-56-35', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[2,4])
exp0.add_session('15-10-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-15-28', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-20-50', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-37-34', 'c', 'tuningCurve', 'am_tuning_curve') #Copious bug squashing happened for EI, so checking to see if the cell is still there
exp0.add_session('16-42-48', 'd', 'AM', 'am_tuning_curve')
exp0.add_session('16-59-57', 'e', 'signalBandwidths', 'bandwidth_am') #22 kHz @ 32
exp0.add_session('17-20-13', 'f', 'SNRs', 'bandwidth_am')
exp0.add_session('17-39-00', 'f', 'noiseAmps', 'am_tuning_curve')
#Do the noise amps am need to be changed to bandwidth?

exp0.maxDepth = 1200
