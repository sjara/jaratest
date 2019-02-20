from jaratoolbox import celldatabase as celldb
reload(celldb)

subject = 'band002'
experiments = []

exp0 = celldb.Experiment(subject, '2016-08-11', 'left_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp0)

#exp0.add_site(837, tetrodes = [1,2,4,6])
#exp0.add_session('09-48-08', None, 'noisebursts', 'am_tuning_curve') #looks like inhibitory response on TT2? Slight excitatory response on TT4

exp0.add_site(900, tetrodes = [2,4,6])
exp0.add_session('09-53-50', 'a', 'noisebursts', 'am_tuning_curve') #decent sound response on TT4
exp0.add_session('09-55-51', 'b', 'tuningCurve', 'am_tuning_curve') #TT4 and TT6 really like 18-22kHz
exp0.add_session('10-06-41', 'c', 'AM', 'am_tuning_curve') #sustained reponses on TT4, onset on TT6, ??? on TT2
exp0.add_session('10-14-24', 'd', 'bandwidth', 'bandwidth_am') #18kHz, 64Hz mod for TT4 cell(s)

#exp0.add_site(1007, tetrodes = [2,3,4,6])
#exp0.add_session('10-36-29', 'e', 'noisebursts', 'am_tuning_curve') #decent inhibitory response on TT4, weak sound responses on TT2,3

exp0.add_site(1060, tetrodes = [2,4,6])
exp0.add_session('10-41-04', 'f', 'noisebursts', 'am_tuning_curve') #inhibitory response on TT4,6, weak excitatory on TT2
exp0.add_session('10-43-46', 'g', 'tuningCurve', 'am_tuning_curve') #TT6 seems responsive to everything, but more to high freq. TT2 and 4 like 18kHz
exp0.add_session('10-54-47', 'h', 'AM', 'am_tuning_curve') #TT4 mostly onset response, TT6 has sustained response, TT2 ??? response
exp0.add_session('11-02-59', 'i', 'bandwidth', 'bandwidth_am')

exp0.add_site(1135, tetrodes = [2,3,4,5,6])
exp0.add_session('11-24-18', 'j', 'noisebursts', 'am_tuning_curve') #pretty good sound response on TT4, looks like inhibitory again on TT2,6
exp0.add_session('11-26-40', 'k', 'tuningCurve', 'am_tuning_curve') #looks like two cells on TT4: one tuned to 7kHz, one tuned to 18kHz
exp0.add_session('11-38-07', 'l', 'AM', 'am_tuning_curve')
exp0.add_session('11-47-03', 'm', 'bandwidth', 'bandwidth_am') #18kHz, 4Hz mod for stronger TT4 response

exp0.add_site(1250, tetrodes = [2,3,4,5,6])
exp0.add_session('12-16-11', 'n', 'noisebursts', 'am_tuning_curve') #adequate sound responses on TT2,3,4,6
exp0.add_session('12-18-16', 'o', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-29-07', 'p', 'AM', 'am_tuning_curve') #22kHz, 16Hz mod to try to target TT2,6
exp0.add_session('12-36-23', 'q', 'bandwidth', 'bandwidth_am')

exp0.maxDepth = 1250


exp1 = celldb.Experiment(subject, '2016-08-12', 'left_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp1)

exp1.add_site(1177, tetrodes = [2,4,6])
exp1.add_session('10-35-41', None, 'noisebursts', 'am_tuning_curve') #Great sound response on TT6, ok one on TT2
exp1.add_session('10-37-28', 'a', 'tuningCurve', 'am_tuning_curve') #we might be losing our TT6 cell, but we picked up two huge TT2 cells!
exp1.add_session('10-48-21', 'b', 'AM', 'am_tuning_curve') #strong sustained responses on TT2
exp1.add_session('10-55-43', 'c', 'bandwidth', 'bandwidth_am') #7kHz 32Hz mod for TT2 cell

exp1.add_site(1248, tetrodes = [2,3,4,6])
exp1.add_session('11-17-48', 'd', 'noisebursts', 'am_tuning_curve') #great responses on TT2,4, ok on TT3,6
exp1.add_session('11-19-51', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-30-47', 'f', 'AM', 'am_tuning_curve') #TT2,4,6 have some responses to 14kHz, TT2 has good sustained response
exp1.add_session('11-39-44', 'g', 'bandwidth', 'bandwidth_am') #14kHz for more cells, 32Hz mod for TT2

exp1.add_site(1380, tetrodes = [1,2,3,4,6])
exp1.add_session('12-06-33', 'h', 'noisebursts', 'am_tuning_curve') #pretty good responses on TT1,2,4, ok on TT3,6
exp1.add_session('12-08-44', 'i', 'tuningCurve', 'am_tuning_curve') #Different ranges, but all respond to 14kHz
exp1.add_session('12-19-40', 'j', 'AM', 'am_tuning_curve') #Ok sustained responses on TT1,4
exp1.add_session('12-27-34', 'k', 'bandwidth', 'bandwidth_am') #14kHz, 32Hz for TT1,4

exp1.add_site(1556, tetrodes = [1,2,4,5,6])
exp1.add_session('12-55-50', 'l', 'noisebursts', 'am_tuning_curve') #onset on TT1,2, on/off on TT4, sustained on TT5,6
exp1.add_session('12-58-22', 'm', 'tuningCurve', 'am_tuning_curve') #10kHz seems pretty popular
exp1.add_session('13-09-44', 'n', 'AM', 'am_tuning_curve') #None have particularly sustained responses, going with 64Hz for most spikes
exp1.add_session('13-17-21', 'o', 'bandwidth', 'bandwidth_am')

exp1.maxDepth = 1556




