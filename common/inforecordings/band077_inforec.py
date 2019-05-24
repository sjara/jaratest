from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band077'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-10-30', 'right_AC', info=['medialDiI','TT8ant','soundleft'])
experiments.append(exp0)

#noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(420) -> SNRs (300) -> noiseAmps (150)


exp0.add_site(1500, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('15-24-56', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-27-47', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-32-34', 'h', 'AM', 'am_tuning_curve')
exp0.add_session('16-10-00', 'i', 'signalBandwidths', 'bandwidth_am') #15 kHz @ 64
exp0.add_session('16-33-37', 'j', 'SNRs', 'bandwidth_am')
exp0.add_session('17-00-32', 'k', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1500


exp1 = celldatabase.Experiment(subject, '2018-11-01', 'right_AC', info=['medialmidDiO','TT8ant','soundleft'])
experiments.append(exp1)

#noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(420) -> SNRs (300) -> noiseAmps (150)
exp1.add_site(900, tetrodes=[2,6,8])
exp1.add_session('14-20-56', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('14-22-29', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('14-27-33', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('14-34-53', 'c', 'signalBandwidths', 'bandwidth_am') #15 kHz @ 64
exp1.add_session('14-57-23', 'd', 'SNRs', 'bandwidth_am')
exp1.add_session('15-19-49', 'e', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1000, tetrodes=[5,7,8])
# exp1.add_session('15-42-35', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('15-44-16', 'f', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('15-51-47', 'g', 'AM', 'am_tuning_curve')

exp1.add_site(1100, tetrodes=[5,7,8])
exp1.add_session('16-08-23', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('16-10-06', 'h', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('16-16-32', 'i', 'AM', 'am_tuning_curve')
exp1.add_session('16-23-54', 'j', 'signalBandwidths', 'bandwidth_am') #15 kHz @ 64
exp1.add_session('16-46-05', 'k', 'SNRs', 'bandwidth_am')
exp1.add_session('17-07-35', 'l', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1200, tetrodes=[4,6,7,8])
# exp1.add_session('17-27-45', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('17-29-26', 'm', 'tuningCurve', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[4,8])
# exp1.add_session('17-48-46', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('17-50-51', 'n', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('17-57-55', 'o', 'AM', 'am_tuning_curve')
#
# exp1.add_site(1400, tetrodes=[5,6,7,8])
# exp1.add_session('18-12-21', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('18-13-59', 'p', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('18-18-30', 'q', 'AM', 'am_tuning_curve')

exp1.maxDepth = 1400


exp2 = celldatabase.Experiment(subject, '2018-11-06', 'right_AC', info=['midlateralDiD','TT8ant','soundleft'])
experiments.append(exp2)

#noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(420) -> SNRs (300) -> noiseAmps (150)
exp2.add_site(900, tetrodes=[1,2,3,4,5,6,7,8])
exp2.add_session('12-00-28', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-02-24', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-07-04', 'b', 'AM', 'am_tuning_curve')
#Repeating with no reference instead of 2 as reference. Even with no reference there appears to be a spike on all tetrodes
exp2.add_session('12-22-00', 'c', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-27-10', 'd', 'AM', 'am_tuning_curve')
exp2.add_session('12-47-07', 'e', 'signalBandwidths', 'bandwidth_am') #15 kHz @ 64
exp2.add_session('13-22-36', 'f', 'SNRs', 'bandwidth_am')
exp2.add_session('14-05-07', 'g', 'noiseAmps', 'am_tuning_curve')
exp2.add_session('14-12-19', 'h', 'signalBandwidths', 'bandwidth_am') #10 kHz @ 64
exp2.add_session('14-36-37', 'i', 'SNRs', 'bandwidth_am')
exp2.add_session('15-00-02', 'j', 'signalBandwidths', 'bandwidth_am') #12 kHz @ 64
exp2.add_session('15-24-00', 'k', 'SNRs', 'bandwidth_am')
exp2.add_session('15-42-28', None, 'noisebursts', 'am_tuning_curve')

# #Tetride 3 has the reference
# exp2.add_site(1000, tetrodes=[1,2,4,5,6,7,8])
# exp2.add_session('15-51-30', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-54-03', 'l', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('15-58-57', 'm', 'AM', 'am_tuning_curve')
# #Bad tuning on clusters

exp2.maxDepth = 1000


exp3 = celldatabase.Experiment(subject, '2018-11-20', 'left_AC', info=['lateralDiD','TT8ant','soundright'])
experiments.append(exp3)

#noisebursts(50) -> tuningCurve(240) -> AM(150) -> signalBandwidths(420) -> SNRs (300) -> noiseAmps (150)
exp3.add_site(900, tetrodes=[6,7,8])
exp3.add_session('14-12-54', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-14-44', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-17-43', 'b', 'AM', 'am_tuning_curve')
#No sustained response

exp3.add_site(1000, tetrodes=[1,2,4,6,7,8])
exp3.add_session('14-29-30', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-30-57', 'c', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-34-17', 'd', 'AM', 'am_tuning_curve')

exp3.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('15-00-40', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-02-06', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('15-07-09', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('15-39-07', 'g', 'signalBandwidths', 'bandwidth_am') #5.5 kHz @ 64
exp3.add_session('16-05-48', 'h', 'SNRs', 'bandwidth_am')
exp3.add_session('16-22-43', 'i', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
exp3.add_session('16-37-25', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-40-37', 'j', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-45-20', 'k', 'AM', 'am_tuning_curve')
exp3.add_session('16-53-06', 'l', 'signalBandwidths', 'bandwidth_am') #5 kHz @ 64
exp3.add_session('17-15-52', 'm', 'SNRs', 'bandwidth_am')
exp3.add_session('17-33-40', 'n', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1200
