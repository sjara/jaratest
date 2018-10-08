from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band076'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-10-03', 'right_AC', info=['medialDiD','TT8ant','soundleft'])
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

exp1 = celldatabase.Experiment(subject, '2018-10-07', 'right_AC', info=['midDiO','TT8ant','soundleft'])
experiments.append(exp1)


    # noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(360) -> SNRs (300) -> noiseAmps (150)
#Large amount of tissue that needed to be cleaned uo. Seems layer may exist under the surface as resistance was hit ~950
exp1.add_site(944, tetrodes=[7,8]) #Movement seems to be causing large oscillations in the ephys readings
exp1.add_session('16-19-13', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-21-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-26-45', 'b', 'AM', 'am_tuning_curve')
#Frequency tuned, AM seems to cause supression of cell
exp1.add_session('16-37-41', 'c', 'signalBandwidths', 'bandwidth_am') #6 kHz @ 32
exp1.add_session('16-58-00', 'd', 'SNRs', 'bandwidth_am')
exp1.add_session('17-15-58', 'e', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 944
