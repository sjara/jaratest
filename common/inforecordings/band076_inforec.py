from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band076'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-10-03', 'right_AC', info=['medialDiD','TT8ant','soundleft'])
experiments.append(exp0)


    # noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(360) -> SNRs (300) -> noiseAmps (150)

# exp0.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
# exp0.add_session('14-33-28', None, 'noisebursts', 'am_tuning_curve')
# 
# exp0.add_site(1100, tetrodes=[1,2,4,6])
# exp0.add_session('14-56-35', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1200, tetrodes=[2,4])
exp0.add_session('15-10-24', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-15-28', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-20-50', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('16-37-34', 'c', 'tuningCurve', 'am_tuning_curve') #Copious bug squashing happened for EI, so checking to see if the cell is still there
exp0.add_session('16-42-48', 'd', 'AM', 'am_tuning_curve')
exp0.add_session('16-59-57', 'e', 'signalBandwidths', 'bandwidth_am') #22 kHz @ 32
exp0.add_session('17-20-13', 'f', 'SNRs', 'bandwidth_am')
exp0.add_session('17-39-00', 'f', 'noiseAmps', 'am_tuning_curve')


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
exp1.add_session('17-15-58', 'e', 'noiseAmps', 'am_tuning_curve') #MATT MAKE SURE YOU'RE ACTUALLY USING AM_TUNING

exp1.maxDepth = 944

#MATT MAKE SURE YOU'RE ACTUALLY USING AM_TUNING FOR NOISE AMPS
#MATT MAKE SURE YOU'RE ACTUALLY USING AM_TUNING FOR NOISE AMPS
#MATT MAKE SURE YOU'RE ACTUALLY USING AM_TUNING FOR NOISE AMPS
#MATT MAKE SURE YOU'RE ACTUALLY USING AM_TUNING FOR NOISE AMPS
#Got it boss

exp2 = celldatabase.Experiment(subject, '2018-10-09', 'right_AC', info=['lateralDiD','TT8ant','soundleft'])
experiments.append(exp2)


    # noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(360) -> SNRs (300) -> noiseAmps (150)

# exp2.add_site(950, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-04-39', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-06-24', 'a', 'tuningCurve', 'am_tuning_curve')
#No freq tuning

# exp2.add_site(1050, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-20-52', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-23-04', 'b', 'tuningCurve', 'am_tuning_curve')
#No freq tuning

#Tetrode 3 has the reference
# exp2.add_site(1150, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-37-38', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1250, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('14-43-35', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-45-05', 'c', 'tuningCurve', 'am_tuning_curve') #Weird tuning responses
# 
# #Tetrode 1 has the reference
# exp2.add_site(1350, tetrodes=[2,3,4,5,6,7,8])
# exp2.add_session('15-20-34', None, 'noisebursts', 'am_tuning_curve')
# 
# #tetrode 3 has the reference
# exp2.add_site(1450, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('16-00-17', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1550, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('16-27-27', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-30-28', 'd', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(1600, tetrodes=[1,2,4,5,6,7,8])
exp2.add_session('16-43-49', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-45-23', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-50-09', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('17-03-55', 'g', 'signalBandwidths', 'bandwidth_am') #10 kHz @ 32
exp2.add_session('17-24-27', 'h', 'SNRs', 'bandwidth_am')
exp2.add_session('17-43-51', 'i', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1600

exp3 = celldatabase.Experiment(subject, '2018-10-15', 'left_AC', info=['medialDiD','TT8ant','soundright'])
experiments.append(exp3)


    #noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(360) -> SNRs (300) -> noiseAmps (150)

exp3.add_site(908, tetrodes=[6,8])
exp3.add_session('13-53-30', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-56-47', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-01-49', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('14-09-28', 'c', 'signalBandwidths', 'bandwidth_am') #15 kHz @ 64
exp3.add_session('14-34-04', 'd', 'SNRs', 'bandwidth_am')
exp3.add_session('14-53-13', 'e', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[7])
exp3.add_session('15-13-59', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-16-18', 'f', 'tuningCurve', 'am_tuning_curve') #Only did 156 trials because I'm a stupid idiot face
exp3.add_session('15-19-56', 'g', 'AM', 'am_tuning_curve') #Did 240 trials because I'm still a stupid idiot face
exp3.add_session('15-29-23', 'h', 'signalBandwidths', 'bandwidth_am') #22 kHz @ 64
exp3.add_session('15-50-44', 'i', 'SNRs', 'bandwidth_am')
exp3.add_session('16-11-27', 'j', 'noiseAmps', 'am_tuning_curve')

# exp3.add_site(1200, tetrodes=[5])
# exp3.add_session('16-31-28', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('16-33-26', 'k', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('16-39-18', 'l', 'AM', 'am_tuning_curve')
# #No significant AM tuning

exp3.maxDepth = 1200

#noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(420) -> SNRs (300) -> noiseAmps (150)
# now 420 signalBandwidths because added pure tone trials

exp4 = celldatabase.Experiment(subject, '2018-10-18', 'left_AC', info=['midDiO','TT8ant','soundright'])
experiments.append(exp4)

exp4.add_site(900, tetrodes=[1,2,4,5,6,7,8])
exp4.add_session('14-44-57', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-47-50', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-52-37', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('15-05-19', 'c', 'signalBandwidths', 'bandwidth_am') #18 kHz @ 64
exp4.add_session('15-28-16', 'd', 'SNRs', 'bandwidth_am')
exp4.add_session('15-51-45', 'e', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1000, tetrodes=[4,6,8])
exp4.add_session('16-18-09', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-21-30', 'f', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-25-54', 'g', 'AM', 'am_tuning_curve')
exp4.add_session('16-40-14', 'h', 'signalBandwidths', 'bandwidth_am') #18 kHz @ 64
exp4.add_session('17-02-38', 'i', 'SNRs', 'bandwidth_am')
exp4.add_session('17-18-44', 'j', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1000
