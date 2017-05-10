from jaratoolbox import celldatabase

subject = 'adap043'
experiments = []
#craniotomy AP -1.2 to -2.2mm, ML 3 to 4mm (outer edge could be near AC)
#noise burst is 100ms white noise at 60dB
#tc is 2-40kHz (16 freqs) at 30-60dB (4 intensity)

exp0 = celldatabase.Experiment(subject,
                               '2017-05-09',
                               brainarea='leftAStr',
                               info=['anteriorDiI', 'facingPosterior'])
experiments.append(exp0)

#1500, 1600, 1700, 1800, 1900, 2000 not sound responsive
exp0.add_site(2150, tetrodes=[1,2,3,4,7,8])
exp0.add_session('14-17-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan3 in TT6, TT1-4 supressed by noise?
exp0.add_session('14-21-33', 'a', 'tc', 'am_tuning_curve') #TT1-4 tuned roughly 8.1-12.1kHz


exp0.add_site(2250, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('14-48-56', None, 'noiseburst', 'am_tuning_curve') #ref to chan25 in TT3, TT6&7 offset response?
exp0.add_session('14-51-02', 'b', 'tc', 'am_tuning_curve') 


exp0.add_site(2320, tetrodes=[1,2,3,5,6,7,8])
exp0.add_session('15-32-07', None, 'noiseburst', 'am_tuning_curve') #ref to chan20 in TT4, TT6&8 sound responsive
exp0.add_session('15-33-48', 'c', 'tc', 'am_tuning_curve') #TT6&8 tuned differently


exp0.add_site(2430, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('15-53-59', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT5-8 sound responsive
exp0.add_session('15-55-38', 'd', 'tc', 'am_tuning_curve') #TT5-8 tuned differently

exp0.add_site(2500, tetrodes=[1,2,4,5,6,7,8])
exp0.add_session('16-16-41', None, 'noiseburst', 'am_tuning_curve') #ref to chan32 in TT3, TT4-8 sound responsive
exp0.add_session('16-19-05', 'e', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2570, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-39-32', None, 'noiseburst', 'am_tuning_curve') #ref to chan30 in TT3, TT4-8 sound responsive
exp0.add_session('16-41-55', 'f', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2670, tetrodes=[1,2,3,4,5,6,7,8])
exp0.add_session('16-59-27', None, 'noiseburst', 'am_tuning_curve') #ref to chan30 in TT3, TT6-8 sound responsive
exp0.add_session('17-03-27', 'g', 'tc', 'am_tuning_curve') #TT4-8 tuned differently

exp0.add_site(2770, tetrodes=[2,3,4,5,6,7,8])
exp0.add_session('17-24-00', None, 'noiseburst', 'am_tuning_curve') #ref to chan18 in TT1, TT3-7 sound responsive
exp0.add_session('17-28-41', 'h', 'tc', 'am_tuning_curve') #TT3-8 tuned differently

#Mouse kept trying to touch array with his paw, because saline kept dripping into his left eye. End experiment, reinforce left side guard

