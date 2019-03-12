from jaratoolbox import celldatabase

subject = 'chad010' 
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-02-17', 'right_AC', info=['farMedialDiD' 'facingAnterior' 'soundLeft'])
experiments.append(exp0)

exp0.add_site(1250, tetrodes=[1,2,3,4,6])

exp0.add_session('16-21-05', 'b', 'tc', 'am_tuning_curve')
#Reference set to 14 (Tetrode 5, channel 1)

exp0.add_session('16-37-06', None, 'noiseburst', 'am_tuning_curve')  # Behavior suffix 'c'
#Reference set to 14 (Tetrode 5, channel 1)

exp0.maxDepth = 1500
