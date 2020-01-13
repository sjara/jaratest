from jaratoolbox import celldatabase

subject = 'band090'
experiments = []

experiment = celldatabase.Experiment(subject,
                               '2020-01-13',
                               brainarea='rightAC',
                               info='')

experiments.append(experiment)

experiment.add_site(1000, data='2020-01-13', tetrodes=range(1, 9))
experiment.add_session('14-13-31', None, 'behavior', '2afc')
experiment.add_session('14-16-15', None, 'noisebursts', 'am_tuning_curve')

