from jaratoolbox import celldatabase

subject='adap024'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2016-08-24')
experiments.append(exp0)

exp0.add_site(0) #3.5 turns
exp0.add_session('14-40-47', 'a', 'tuning', paradigm='tuning_curve')
exp0.add_session('14-56-09', 'a', 'behav1', paradigm='2afc')
exp0.add_session('15-29-40', 'a', 'light', paradigm='lightDiscrim')
exp0.add_session('15-46-41', 'b', 'behav2', paradigm='2afc')


