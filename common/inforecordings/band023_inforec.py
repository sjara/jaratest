from jaratoolbox import celldatabase

subject = 'band023'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-03-20', brainarea='right_thalamus', info=['anteriorDiI','sitesAnt','sound_left'])
experiments.append(exp0)

exp0.add_site(3301, tetrodes = [1,2,5,7])
exp0.add_session('09-50-03', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('09-53-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('10-04-39', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('10-11-28', 'c', 'bandwidth', 'bandwidth_am') #22kHz, 32Hz for TT2 (only sound responsive one anyway)
exp0.add_session('10-31-21', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(3418, tetrodes= [1,2,4,7,8])
exp0.add_session('10-40-40', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('10-43-49', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('10-55-45', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('11-03-16', 'g', 'bandwidth', 'bandwidth_am') #15kHz, 64Hz for TT2
exp0.add_session('11-23-39', 'h', 'bandwidth', 'bandwidth_am') #5kHz, 64Hz for TT4
exp0.add_session('11-48-57', 'i', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(3510, tetrodes = [1,2,4,8])
exp0.add_session('11-58-58', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-02-09', 'j', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-14-19', 'k', 'AM', 'am_tuning_curve')
exp0.add_session('12-31-05', 'l', 'bandwidth', 'bandwidth_am') #26kHz, 64Hz for TT1,2
exp0.add_session('12-50-19', 'm', 'bandwidth', 'bandwidth_am') #14kHz, 64Hz for TT4
exp0.add_session('13-09-42', 'n', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(3605, tetrodes = [1,2,3,4,7,8])
exp0.add_session('13-17-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-20-28', 'o', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-31-05', 'p', 'AM', 'am_tuning_curve')
exp0.add_session('13-39-03', 'q', 'bandwidth', 'bandwidth_am') #18kHz, 64Hz for TT4
exp0.add_session('14-01-34', 'r', 'bandwidth', 'bandwidth_am') #4.5kHz, 32Hz for TT3
exp0.add_session('14-26-10', 's', 'noiseAmps', 'am_tuning_curve')
exp0.add_session('14-31-29', 't', 'bandwidth', 'bandwidth_am') #27kHz, 64Hz for TT1

exp0.maxDepth = 3605


exp1 = celldatabase.Experiment(subject, '2017-03-22', brainarea='right_thalamus', info=['middleDiD','sitesAnt','sound_left'])
experiments.append(exp1)

# exp1.add_site(3300, tetrodes = [2,4,6])
# exp1.add_session('09-20-44', None, 'noisebursts', 'am_tuning_curve') #two decent sound responsive spikes on TT4
# exp1.add_session('09-23-13', 'a', 'tuningCurve', 'am_tuning_curve') #not that great sound responses
# exp1.add_session('09-34-22', 'b', 'AM', 'am_tuning_curve')

exp1.add_site(3390, tetrodes = [2,4,6])
exp1.add_session('09-41-43', None, 'noisebursts', 'am_tuning_curve') #good sound response on TT2, good spikes on TT4 with ok sound response
exp1.add_session('09-45-10', 'c', 'tuningCurve', 'am_tuning_curve') #Ok clusters on TT4 tuned to 17kHz and 8kHz
exp1.add_session('09-55-52', 'd', 'AM', 'am_tuning_curve')
exp1.add_session('10-01-24', 'e', 'bandwidth', 'bandwidth_am') #17kHz, 64Hz for good TT4 cluster
exp1.add_session('10-21-49', 'f', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(3460, tetrodes = [2,4,6])
exp1.add_session('10-32-31', None, 'noisebursts', 'am_tuning_curve') #strong sound response from ok TT2 cluster, good sound response from good TT4 cluster
exp1.add_session('10-35-03', 'g', 'tuningCurve', 'am_tuning_curve') #good clusters on TT2 and 4 like 18kHz, ok cluster on TT6 likes 26kHz
exp1.add_session('10-46-43', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('10-53-47', 'i', 'bandwidth', 'bandwidth_am') #17kHz, 64Hz for TT2 and 4
exp1.add_session('11-13-33', 'j', 'bandwidth', 'bandwidth_am') #26kHz, 64Hz for TT6
exp1.add_session('11-32-01', 'k', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(3540, tetrodes = [2,4,6,8])
exp1.add_session('12-18-22', None, 'noisebursts', 'am_tuning_curve') #on and off responses on TT4,6!
exp1.add_session('12-21-32', 'l', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-33-05', 'm', 'AM', 'am_tuning_curve')
exp1.add_session('12-39-51', 'n', 'bandwidth', 'bandwidth_am') #18kHz, 64H for TT2 cell
exp1.add_session('12-59-40', 'o', 'bandwidth', 'bandwidth_am') #6.5kHz, 16Hz for big TT4 spike
exp1.add_session('13-20-06', 'p', 'bandwidth', 'bandwidth_am') #12kHz, 64Hz for TT6
exp1.add_session('13-40-07', 'q', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 3540


exp2 = celldatabase.Experiment(subject, '2017-03-23', brainarea='right_thalamus', info=['posteriorDiI','sitesAnt','sound_left'])
experiments.append(exp2)

exp2.add_site(3300, tetrodes = [2,3,4,5,6,8])
exp2.add_session('10-13-11', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-17-10', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-27-50', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('10-34-32', 'c', 'bandwidth', 'bandwidth_am') #26kHz, 64Hz for TT3,4 cells
exp2.add_session('10-54-47', 'd', 'bandwidth', 'bandwidth_am') #17kHz, 64Hz for TT4,6 cells
exp2.add_session('11-13-06', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(3532, tetrodes = [2,3,4,5,6,7,8])
exp2.add_session('11-21-51', None, 'noisebursts', 'am_tuning_curve') #big spikes that actually do something!
exp2.add_session('11-25-34', 'f', 'tuningCurve', 'am_tuning_curve') #big spikes aren't tuned to anything!!!
exp2.add_session('11-36-10', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('11-44-33', 'h', 'bandwidth', 'bandwidth_am') #26kHz, 8Hz for ok TT3 spike
exp2.add_session('12-02-59', 'i', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 3532


exp3 = celldatabase.Experiment(subject, '2017-03-24', brainarea='left_thalamus', info=['anteriorDiI','TT1ant','sound_left'])
experiments.append(exp3)

exp3.add_site(3000, tetrodes = [1,2,3,4,5,7,8])
exp3.add_session('10-23-22', None, 'noisebursts', 'am_tuning_curve') #lots of sound responses, decent clusters
exp3.add_session('10-26-51', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('10-37-39', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('10-48-00', 'c', 'bandwidth', 'bandwidth_am') #13kHz, 64Hz for TT3,4
exp3.add_session('11-09-03', 'd', 'bandwidth', 'bandwidth_am') #8kHz, 64Hz for other TT4 cluster
exp3.add_session('11-27-30', 'e', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(3106, tetrodes = [4,5,6,7,8])
exp3.add_session('11-36-24', None, 'noisebursts', 'am_tuning_curve') #good, sound responsive clusters!
exp3.add_session('11-39-07', 'f', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('11-49-44', 'g', 'AM', 'am_tuning_curve')
exp3.add_session('11-56-21', 'h', 'bandwidth', 'bandwidth_am') #10kHz, 64Hz for TT4
exp3.add_session('12-14-57', 'i', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(3350, tetrodes = [3,4,6,7,8])
exp3.add_session('12-23-06', None, 'noisebursts', 'am_tuning_curve') #TT3,4 have big neurons that appear to do something
exp3.add_session('12-26-18', 'j', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-37-33', 'k', 'AM', 'am_tuning_curve')
exp3.add_session('12-42-45', 'l', 'bandwidth', 'bandwidth_am') #15kHz, 64Hz for two good TT3 clusters
exp3.add_session('13-01-14', 'm', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 3350


exp4 = celldatabase.Experiment(subject, '2017-03-26', brainarea='left_thalamus', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp4)

# exp4.add_site(3135, tetrodes = [1,3,4,7,8])
# exp4.add_session('14-30-25', None, 'noisebursts', 'am_tuning_curve') #no sound responses

exp4.add_site(3200, tetrodes = [1,3,4,6,7,8])
exp4.add_session('14-35-21', None, 'noisebursts', 'am_tuning_curve') #some sound responses on TT7,8
exp4.add_session('14-37-14', 'a', 'tuningCurve', 'am_tuning_curve') #no good tuning
exp4.add_session('14-48-06', 'b', 'AM', 'am_tuning_curve')

exp4.add_site(3350, tetrodes = [1,3,4,5,7,8])
exp4.add_session('14-59-16', None, 'noisebursts', 'am_tuning_curve') #good sound responses at last!
exp4.add_session('15-02-38', 'c', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-13-39', 'd', 'AM', 'am_tuning_curve')
exp4.add_session('15-19-49', 'e', 'bandwidth', 'bandwidth_am') #8kHz, 16Hz for really nice TT1 cell
exp4.add_session('15-40-41', 'f', 'bandwidth', 'bandwidth_am') #12kHz, 64Hz for TT4 cells
exp4.add_session('16-01-19', 'g', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(3550, tetrodes = [1,2,3,4,7])
exp4.add_session('16-09-48', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-13-03', 'h', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-24-03', 'i', 'AM', 'am_tuning_curve')
exp4.add_session('16-31-32', 'j', 'bandwidth', 'bandwidth_am') #12kHz, 64Hz for TT1 cell
exp4.add_session('16-52-55', 'k', 'bandwidth', 'bandwidth_am') #8kHz, 64Hz for TT3
exp4.add_session('17-11-30', 'l', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 3550


exp5 = celldatabase.Experiment(subject, '2017-03-27', brainarea='left_thalamus', info=['posteriorDiI','TT1ant','sound_left'])
experiments.append(exp5)

exp5.add_site(3200, tetrodes = [1,2,3,4,6,7,8])
exp5.add_session('10-15-14', None, 'noisebursts', 'am_tuning_curve') #very interesting responses on TT2 and 7
exp5.add_session('10-18-14', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('10-29-00', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('10-36-05', 'c', 'bandwidth', 'bandwidth_am') #4kHz, 64Hz for larger peak of TT2 cluster
exp5.add_session('10-54-29', 'd', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(3360, tetrodes = [1,2,3,4,5,7])
exp5.add_session('11-03-38', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('11-05-38', 'e', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('11-16-15', 'f', 'AM', 'am_tuning_curve')
exp5.add_session('11-22-43', 'g', 'bandwidth', 'bandwidth_am') #17kHz, 64Hz for TT1 response, as well as TT2 trough
exp5.add_session('11-41-30', 'h', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(3550, tetrodes = [1,2,3,4,5,6,7])
exp5.add_session('11-51-01', None, 'noisebursts', 'am_tuning_curve') #some strong off responses
exp5.add_session('11-53-00', 'i', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-05-04', 'j', 'AM', 'am_tuning_curve')
exp5.add_session('12-11-59', 'k', 'bandwidth', 'bandwidth_am') #8kHz, 64Hz for big inhibitory TT1 response
exp5.add_session('12-41-29', 'l', 'bandwidth', 'bandwidth_am') #5.5kHz, 64Hz for TT3
exp5.add_session('13-01-36', 'm', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(3760, tetrodes = [2,4,5,7])
exp5.add_session('13-19-10', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-21-09', 'n', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-31-47', 'o', 'AM', 'am_tuning_curve')
exp5.add_session('13-37-38', 'p', 'bandwidth', 'bandwidth_am') #7kHz, 64Hz for TT2
exp5.add_session('14-06-17', 'q', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 3760
