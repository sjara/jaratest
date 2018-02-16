from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band021'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-02-22', brainarea='left_thalamus', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp0)

#crazy hippocampus lfp cleared up, now lots of spikes on TT2 while others quiet.
# exp0.add_site(3010, tetrodes = [2])
# exp0.add_session('11-42-47', None, 'noisebursts', 'am_tuning_curve')
